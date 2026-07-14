from pydantic import BaseModel
from typing import Dict, Any, List

class OrchestratorResponse(BaseModel):
    status: str
    nodes_executed: int
    errors: List[str]
    agent_status: Dict[str, str]
