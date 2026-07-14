from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EvolutionStatus(str, Enum):
    PROMOTED = "Promoted"     # Confidence/success grew, status strengthened
    RETIRED = "Retired"       # Confidence/success dropped below threshold, deactivated
    MAINTAINED = "Maintained" # General updates, remains active

class LearningReport(BaseModel):
    """Report generated after integrating a new episode into a strategy."""
    strategy_id: str
    previous_success_rate: float
    new_success_rate: float
    previous_confidence: float
    new_confidence: float
    execution_time_delta: float

class StrategyEvolutionReport(BaseModel):
    """Final report detailing how the strategy evolved (or was retired)."""
    strategy_id: str
    status: EvolutionStatus
    version: int
    learning_metrics: LearningReport
    reasons: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
