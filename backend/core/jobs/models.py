from sqlalchemy import Column, String, DateTime, JSON, Integer
from core.database import Base
from datetime import datetime
import uuid

class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_type = Column(String, index=True) # e.g., 'automl', 'cleaning', 'eda'
    status = Column(String, default="QUEUED", index=True) # QUEUED, RUNNING, COMPLETED, FAILED
    progress = Column(Integer, default=0)
    progress_message = Column(String, nullable=True)
    dataset_name = Column(String, nullable=True)
    owner_id = Column(String, index=True, nullable=True)
    parameters = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
