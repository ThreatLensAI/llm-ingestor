import os
from pydantic import BaseModel, ConfigDict
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import StorageContext, Document
from llama_index.core import Settings, VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from json_parser import format_cve_data

class Ingestor:
    class Valves(BaseModel):
        LLAMAINDEX_OLLAMA_BASE_URL: str
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
        self.name = "Ollama Indexer"
        self.index = None
        self.vector_store = None
        self.storage_context = None
        self.valves = self.Valves(
            **{
                "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://localhost:11434"),
                "EMBEDDING_DIM": int(os.getenv("EMBEDDING_DIM", "768")),
                "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "nomic-embed-text:latest"),
                "PGHOST": os.getenv("DB_HOST", "localhost"),
                "PGUSER": os.getenv("DB_USER", "postgres"),
                "PGPASSWORD": os.getenv("DB_PASSWORD", "password"),
                "PGSCHEMA": os.getenv("DB_SCHEMA", "cve"),
                "PGDATABASE": os.getenv("DB_DATABASE", "cve"),
                "PGTABLE": os.getenv("DB_TABLE", "embeddings"),
                "PGPORT": int(os.getenv("DB_PORT", '5432')),
            }
        )

        Settings.embed_model = OllamaEmbedding(
            model_name=self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )

        Settings.chunk_size = 500
        Settings.chunk_overlap = 250

        self.vector_store = PGVectorStore.from_params(
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

        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

    def createEmbedding(self, json_data):
        data = format_cve_data(json_data)
        document_obj = Document(
            text=data
        )
        self.index = VectorStoreIndex.from_documents([document_obj], 
            storage_context=self.storage_context,
            show_progress=False
        )   

    async def close(self):
        await self.vector_store.close()
