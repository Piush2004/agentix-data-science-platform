from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class UploadResponse(BaseModel):
    message: str
    dataset_name: str
    rows: int
    columns: int
    column_names: List[str]
    preview: List[Dict[str, Any]]
    column_types: Dict[str, str]
    upload_timestamp: str
    dataset_id: str

class ProcessRequest(BaseModel):
    dataset_name: str
