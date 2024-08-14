import asyncio
from http.server import HTTPServer
import signal
import sys
from logger import logger
from dotenv import load_dotenv
from kafka_consumer import get_Kafka_consumer, consume 
from ingestor import Ingestor
from concurrent.futures import ThreadPoolExecutor
import os
from server import HealthCheckHandler

load_dotenv()

consumer = None
embedder = None
executor = None
httpd = None

def shutdown_signal_handler(signum, frame):
    logger.info("Received shutdown signal")

    logger.info("Closing consumer...")
    if consumer is not None:
        consumer.close()

    logger.info("Closing DB connection...")
    if embedder is not None:
        asyncio.run(embedder.close())

    logger.info("Shutting down server...")
    if executor is not None and httpd is not None:
        httpd.shutdown()
        executor.shutdown(wait=False)

    sys.exit(0)

consumer = get_Kafka_consumer()
embedder = Ingestor()

signal.signal(signal.SIGINT, shutdown_signal_handler)
signal.signal(signal.SIGTERM, shutdown_signal_handler)

httpd = HTTPServer(('', os.getenv('PORT', 3001)), HealthCheckHandler)
executor = ThreadPoolExecutor(max_workers=1)

logger.info("Starting health check server...")
executor.submit(httpd.serve_forever)

consume(embedder, consumer)
