from kafka import KafkaConsumer
import os
import json
from logger import logger
import traceback

def get_Kafka_consumer():
    username = os.getenv("KAFKA_USERNAME", "")
    password = os.getenv("KAFKA_PASSWORD", "")
    consumer = KafkaConsumer(os.getenv('KAFKA_TOPIC', 'cve'),
                             group_id=os.getenv('KAFKA_CONSUMER_GROUP_ID', 'cve'),
                             bootstrap_servers=[os.getenv('KAFKA_SERVICE', 'localhost:9092')],
                             fetch_max_bytes=os.getenv('KAFKA_MAX_SIZE', 10000000),
                             security_protocol='SASL_PLAINTEXT',
                             sasl_mechanism='SCRAM-SHA-512',
                             sasl_plain_username=username,
                             sasl_plain_password=password,
                             enable_auto_commit=False,
                             )
    return consumer

def consume(pipeline, consumer):
    logger.info("Consumer is ready to read messages")

    counter = 0
    for message in consumer:
        try:
            message_str = message.value.decode('utf-8')
            loaded_json = json.loads(message_str)
            pipeline.createEmbedding(loaded_json)

            consumer.commit()
            counter += 1

            if counter % 1000 == 0:
                logger.info(f"Read {counter} messages")

        except Exception as e:
            logger.warning(f"An error occurred in reading kafka message: {traceback.format_exc()} for message : {message_str}")

    consumer.close()
