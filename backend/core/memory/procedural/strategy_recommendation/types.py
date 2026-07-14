from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from core.memory.procedural.strategy_builder.types import ProceduralStrategy

class RecommendationAction(str, Enum):
    REUSE = "Reuse Strategy"
    MODIFY = "Modify Strategy"
    IGNORE = "Ignore Strategy"

class StrategyRecommendation(BaseModel):
    """Recommendation on how to use a given strategy for the current context."""
    strategy_id: Optional[str]
    action: RecommendationAction
    reasoning: str
    suggested_modifications: List[str] = Field(default_factory=list)
    confidence: float
