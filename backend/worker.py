import os
import sys
import logging
from rq import Worker, Queue, Connection
from core.redis_client import get_redis

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("rq.worker")

# Define all expected task queues
QUEUES = [
    "clean", 
    "eda", 
    "feature_engineering", 
    "predict", 
    "reports", 
    "chat", 
    "xai",
    "default"
]

def run_worker():
    """
    Initializes and starts the Redis Queue (RQ) Worker process.
    Listens to all dedicated queues defined above.
    """
    logger.info("Starting RQ Worker process...")
    redis_conn = get_redis()
    
    with Connection(redis_conn):
        worker = Worker(QUEUES)
        logger.info(f"Worker initialized. Listening to queues: {QUEUES}")
        worker.work()

if __name__ == '__main__':
    run_worker()
