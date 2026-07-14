from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class BrainInput(BaseModel):
    dataset_name: Optional[str] = None
    user_request: Optional[str] = None
    workspace_id: str

class ExecutionPlan(BaseModel):
    target: str
    steps: List[str]
    confidence: float

class BrainOutput(BaseModel):
    plan: Optional[ExecutionPlan] = None
    recommendations: List[str]
    context: Dict[str, Any]
    status: str
