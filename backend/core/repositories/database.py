import os
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentix.db")

# Connection Pooling & Configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,  # Health Check before using a connection
        pool_recycle=1800    # Recycle connections every 30 minutes
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db(retries=5, delay=5):
    """Retry logic for database connection"""
    for i in range(retries):
        try:
            with engine.connect() as conn:
                logger.info("Successfully connected to the database.")
                return True
        except OperationalError as e:
            logger.warning(f"Database connection failed. Retrying in {delay} seconds... ({i+1}/{retries})")
            time.sleep(delay)
    
    logger.error("Failed to connect to the database after multiple retries.")
    return False

def init_db():
    """Automatic Migration (Creates tables if they do not exist)"""
    if wait_for_db():
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized.")
