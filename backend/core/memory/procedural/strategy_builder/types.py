from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
import uuid

class StrategyConditions(BaseModel):
    """Conditions under which this strategy is applicable."""
    target_variable_required: bool
    required_columns: List[str] = Field(default_factory=list)
    dataset_shape_constraints: Dict[str, Any] = Field(default_factory=dict)

class ProceduralStrategy(BaseModel):
    """A validated, reusable permanent strategy in Procedural Memory."""
    strategy_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain: str
    intent: str
    conditions: StrategyConditions
    workflow: List[str]
    capabilities: List[str]
    expected_outcome: str
    success_rate: float
    failure_rate: float
    confidence: float
    usage_count: int = 0
    average_execution_time: float = 0.0
    creation_date: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    is_active: bool = False
    
    # To track lineage back to mining
    source_candidate_id: str
