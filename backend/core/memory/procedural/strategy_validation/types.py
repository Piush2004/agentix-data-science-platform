from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ValidationStatus(str, Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    REQUIRES_MORE_DATA = "Requires More Data"

class ValidationReport(BaseModel):
    """Report generated after evaluating a StrategyCandidate."""
    candidate_id: str
    status: ValidationStatus
    reasons: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
