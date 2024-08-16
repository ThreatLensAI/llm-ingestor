import logging
from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import os
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.chat_engine.types import ChatMode
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.base.llms.types import ChatMessage

class Pipeline:
    class Valves(BaseModel):
        LLAMAINDEX_OLLAMA_BASE_URL: str
        LLAMAINDEX_MODEL_NAME: str
        LLAMAINDEX_EMBEDDING_MODEL_NAME: str
        PGHOST: str
        PGPORT: int
        PGUSER: str
        PGPASSWORD: str
        PGDATABASE: str
        PGSCHEMA: str
        PGTABLE: str
        EMBEDDING_DIM: int

    def __init__(self):
        self.name = "CVE Chatbot"
        self.index = None
        self.valves = self.Valves(
            **{
                "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://localhost:11434"),
                "LLAMAINDEX_MODEL_NAME": os.getenv("LLAMAINDEX_MODEL_NAME", "gemma:2b"),
                "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "nomic-embed-text:latest"),
                "EMBEDDING_DIM": int(os.getenv("EMBEDDING_DIM", "768")),
                "PGHOST": os.getenv("DB_HOST", "localhost"),
                "PGUSER": os.getenv("DB_USER", "postgres"),
                "PGPASSWORD": os.getenv("DB_PASSWORD", "password"),
                "PGSCHEMA": os.getenv("DB_SCHEMA", "cve"),
                "PGDATABASE": os.getenv("DB_DATABASE", "cve"),
                "PGTABLE": os.getenv("DB_TABLE", "embeddings"),
                "PGPORT": int(os.getenv("DB_PORT", '5432')),
            }
        )

    async def on_startup(self):
        print(f"on_startup:{__name__}")

        Settings.embed_model = OllamaEmbedding(
            model_name=self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )
        Settings.llm = Ollama(
            model=self.valves.LLAMAINDEX_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )

        Settings.chunk_size = 500
        Settings.chunk_overlap = 250

        vector_store = PGVectorStore.from_params(
            database=self.valves.PGDATABASE,
            host=self.valves.PGHOST,
            password=self.valves.PGPASSWORD,
            port=self.valves.PGPORT,
            user=self.valves.PGUSER,
            schema_name=self.valves.PGSCHEMA,
            table_name=self.valves.PGTABLE,
            embed_dim=self.valves.EMBEDDING_DIM,
            hybrid_search=True,
            text_search_config="english",
            hnsw_kwargs={
                "hnsw_m": 16,
                "hnsw_ef_construction": 64,
                "hnsw_ef_search": 40,
                "hnsw_dist_method": "vector_cosine_ops",
            },
        )

        global index
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.propagate = True
        root_logger.addHandler(logging.StreamHandler())

        hybrid_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store
        )

        self.engine = hybrid_index.as_chat_engine(
            vector_store_query_mode="hybrid",
            chat_mode=ChatMode.CONTEXT,
            sparse_top_k=5
        )


    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")
        print(f"model_id:{model_id}")

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("######################################")
        
        chatMessages = []
        for message in messages:
            chatMessages.append(ChatMessage.from_str(content=message["content"], role=message["role"]))
        
        response = self.engine.stream_chat(user_message, chatMessages)

        # print(response.print_response_stream())

        return response.response_gen
