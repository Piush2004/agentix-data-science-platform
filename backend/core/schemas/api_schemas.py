from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class DatasetRequest(BaseModel):
    dataset_name: str

class PredictRequest(BaseModel):
    dataset_name: str
    target_column: Optional[str] = None

class ChatRequest(BaseModel):
    query: str
    dataset_name: Optional[str] = None
    context_keys: Optional[List[str]] = []

class BaseResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

