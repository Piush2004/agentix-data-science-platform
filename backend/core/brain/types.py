from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime

class PerceptionObject(BaseModel):
    """Raw observation output from the Perception module."""
    dataset_metadata: Dict[str, Any] = Field(default_factory=dict)
    user_goal: str
    workspace_context: Dict[str, Any] = Field(default_factory=dict)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    current_state: str
    environment: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UnderstandingObject(BaseModel):
    """Synthesized intent and domain context from the Understanding module."""
    perception: PerceptionObject
    business_problem: str
    domain: str
    data_quality_assessment: str
    user_intent: str
    inferred_context: Dict[str, Any] = Field(default_factory=dict)

from core.brain.deliberation.types import DeliberationResult
from core.memory.episodic.types import EpisodeRecommendation
from core.memory.procedural.strategy_recommendation.types import StrategyRecommendation

class ReasoningObject(BaseModel):
    """Logical deductions from the Reasoning module."""
    deliberation: DeliberationResult
    episode_recommendations: List[EpisodeRecommendation] = Field(default_factory=list)
    strategy_recommendation: Optional[StrategyRecommendation] = None
    what_should_happen: List[str]
    what_should_not_happen: List[str]
    reusable_knowledge_keys: List[str]
    required_engines: List[str]
    required_agents: List[str]
    can_use_deterministic_computation: bool

class PlanStep(BaseModel):
    step_id: str
    action: str
    engine: str
    agent: Optional[str] = None
    estimated_cost: float = 0.0
    estimated_time_sec: int = 0
    dependencies: List[str] = Field(default_factory=list)

class ExecutionPlan(BaseModel):
    plan_id: str
    steps: List[PlanStep]
    total_estimated_time_sec: int
    total_estimated_cost: float
    alternatives: List[str] = Field(default_factory=list)

class DecisionObject(BaseModel):
    """The final chosen pathway from the Decision module."""
    reasoning: ReasoningObject
    chosen_plan: ExecutionPlan
    best_engine: str
    best_agent: str
    best_model: str
    best_workflow: str

class LearningRecord(BaseModel):
    """Execution telemetry and feedback for the Learning module."""
    decision: DecisionObject
    success: bool
    execution_statistics: Dict[str, Any] = Field(default_factory=dict)
    user_preferences_extracted: Dict[str, Any] = Field(default_factory=dict)
    failed_steps: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
