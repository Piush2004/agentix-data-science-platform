from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime

class DeliberationQuestion(BaseModel):
    id: str
    text: str
    category: str

class DeliberationEvidence(BaseModel):
    source: str
    data: Dict[str, Any]
    reliability_score: float = 1.0

class DeliberationHypothesis(BaseModel):
    id: str
    question_id: str
    description: str
    expected_outcome: str
    required_evidence: List[str]

class HypothesisEvaluation(BaseModel):
    hypothesis_id: str
    advantages: List[str]
    disadvantages: List[str]
    execution_cost: float
    estimated_time_sec: int
    memory_impact: str
    risk_level: str
    privacy_impact: str
    llm_usage_required: bool

class ConfidenceScore(BaseModel):
    hypothesis_id: str
    score: float = Field(..., ge=0.0, le=100.0)
    reason: str
    supporting_evidence_keys: List[str]

class RankedHypothesis(BaseModel):
    hypothesis: DeliberationHypothesis
    evaluation: HypothesisEvaluation
    confidence: ConfidenceScore
    rank: int

class DeliberationRationale(BaseModel):
    decision_summary: str
    reason: str
    evidence_summary: str
    confidence_score: float
    expected_outcome: str

class DeliberationResult(BaseModel):
    questions: List[DeliberationQuestion]
    hypotheses: List[DeliberationHypothesis]
    evidence_summary: Dict[str, Any]
    alternatives: List[RankedHypothesis]
    chosen_hypothesis: RankedHypothesis
    rationale: DeliberationRationale
    risk_assessment: str
    recommended_next_action: str
    estimated_cost: float
    estimated_time: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
