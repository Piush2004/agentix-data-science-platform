from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from core.repositories.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    datasets = relationship("Dataset", back_populates="owner", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="owner", uselist=False, cascade="all, delete-orphan")
    workflow_runs = relationship("WorkflowRun", back_populates="owner", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="owner", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="owner", cascade="all, delete-orphan")

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    llm_provider = Column(String, default="ollama")
    openai_api_key = Column(String, nullable=True)
    theme = Column(String, default="dark")
    
    owner = relationship("User", back_populates="settings")

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    filepath = Column(String, nullable=False)
    rows = Column(Integer, default=0)
    columns = Column(Integer, default=0)
    size_bytes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="datasets")
    reports = relationship("EDAReport", back_populates="dataset", cascade="all, delete-orphan")
    models = relationship("ModelRecord", back_populates="dataset", cascade="all, delete-orphan")
    metadata_records = relationship("DatasetMetadata", back_populates="dataset", cascade="all, delete-orphan")
    feature_engineering = relationship("FeatureEngineering", back_populates="dataset", cascade="all, delete-orphan")

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dataset = relationship("Dataset", back_populates="metadata_records")

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=True)
    status = Column(String, default="running") # running, completed, failed
    execution_time = Column(Float, default=0.0)
    logs = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="workflow_runs")

class EDAReport(Base):
    __tablename__ = "eda_reports"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dataset = relationship("Dataset", back_populates="reports")

class ModelRecord(Base):
    __tablename__ = "model_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    algorithm = Column(String, nullable=False)
    accuracy = Column(String, nullable=False)
    hyperparameters = Column(Text, nullable=True)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    filepath = Column(String, nullable=True) # To store pickle file location
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dataset = relationship("Dataset", back_populates="models")
    predictions = relationship("Prediction", back_populates="model", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_id = Column(String, ForeignKey("model_records.id"), nullable=False)
    input_data = Column(Text, nullable=False) # JSON encoded
    output_data = Column(Text, nullable=False) # JSON encoded
    created_at = Column(DateTime, default=datetime.utcnow)
    
    model = relationship("ModelRecord", back_populates="predictions")

class FeatureEngineering(Base):
    __tablename__ = "feature_engineering"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    action_applied = Column(String, nullable=False)
    columns_affected = Column(Text, nullable=False) # JSON list
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dataset = relationship("Dataset", back_populates="feature_engineering")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context_used = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="chat_history")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="notifications")
