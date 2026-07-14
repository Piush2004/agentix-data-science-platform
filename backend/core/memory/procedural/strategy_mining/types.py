from pydantic import BaseModel, Field
from typing import List, Dict, Any
from core.memory.episodic.types import Episode

class EpisodeClusterKey(BaseModel):
    """The dimensions by which episodes are grouped."""
    business_domain: str
    detected_intent: str
    target_variable: str

    def __hash__(self):
        return hash((self.business_domain, self.detected_intent, self.target_variable))

class EpisodeCluster(BaseModel):
    """A collection of structurally and semantically related Episodes."""
    cluster_key: EpisodeClusterKey
    episodes: List[Episode]

class ExecutionPattern(BaseModel):
    """A distinct sequence of workflow steps/engines used across episodes."""
    pattern_hash: str
    workflow_steps: List[str]
    engines_used: List[str]
    
    def __hash__(self):
        return hash(self.pattern_hash)
        
    def __eq__(self, other):
        return self.pattern_hash == other.pattern_hash

class PatternFrequency(BaseModel):
    """Frequency metrics for a given pattern within a cluster."""
    pattern: ExecutionPattern
    supporting_episode_ids: List[str]
    occurrence_count: int
    frequency_percentage: float

class PatternSuccess(BaseModel):
    """Success metrics for a given pattern."""
    pattern: ExecutionPattern
    average_success_score: float
    success_variance: float

class StrategyCandidate(BaseModel):
    """A viable candidate pattern that could become a permanent strategy."""
    candidate_id: str
    cluster_key: EpisodeClusterKey
    pattern: ExecutionPattern
    supporting_episode_ids: List[str]
    frequency: float
    average_success: float
    confidence: float
