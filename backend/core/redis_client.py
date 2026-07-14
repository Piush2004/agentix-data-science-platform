import redis
import os
import logging
import time

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Configure Production Redis Pool
redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL,
    decode_responses=False,
    socket_connect_timeout=5,
    socket_timeout=5,
    max_connections=50
)

redis_client = redis.Redis(connection_pool=redis_pool)

def wait_for_redis(retries=5, delay=5):
    """Retry logic for Redis connection"""
    for i in range(retries):
        try:
            redis_client.ping()
            logger.info("Successfully connected to Redis.")
            return True
        except Exception as e:
            logger.warning(f"Redis connection failed. Retrying in {delay} seconds... ({i+1}/{retries})")
            time.sleep(delay)
    
    logger.error("Failed to connect to Redis after multiple retries.")
    return False

# Initialize eagerly for early failing in production
if os.getenv("ENVIRONMENT") == "production":
    wait_for_redis()

def get_redis():
    return redis_client
