from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

class DatasetFingerprint(BaseModel):
    columns: List[str]
    column_types: Dict[str, str]
    missing_value_ratio: float
    dataset_shape: List[int]
    business_domain: str
    target_variable: Optional[str] = None
    # No raw data or PII should be stored here

class ExecutionMetrics(BaseModel):
    execution_time_sec: int
    memory_usage_mb: float
    success_score: float = Field(..., ge=0.0, le=100.0)

class Episode(BaseModel):
    episode_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    workspace_id: str
    dataset_id: str
    dataset_fingerprint: DatasetFingerprint
    dataset_profile: Dict[str, Any]
    business_domain: str
    user_goal: str
    detected_intent: str
    questions_generated: List[str]
    hypotheses_generated: List[str]
    evidence_summary: Dict[str, Any]
    chosen_hypothesis: str
    confidence_score: float
    workflow_plan: List[Dict[str, Any]]
    engines_used: List[str]
    llms_used: List[str]
    capabilities_used: List[str]
    execution_metrics: ExecutionMetrics
    privacy_flags: List[str]
    outcome: str
    user_feedback: Optional[str] = None
    lessons_learned: List[str] = Field(default_factory=list)

class EpisodeScores(BaseModel):
    success_score: float
    reusability_score: float
    confidence_score: float
    learning_score: float
    popularity_score: float

class EpisodeRecommendation(BaseModel):
    episode: Episode
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    recommended_workflow: List[Dict[str, Any]]
    adaptation_reasoning: str
