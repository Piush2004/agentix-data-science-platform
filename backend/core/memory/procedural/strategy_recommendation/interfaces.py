from abc import ABC, abstractmethod
from typing import List, Optional
from core.memory.episodic.types import DatasetFingerprint, EpisodeRecommendation
from core.memory.procedural.strategy_builder.types import ProceduralStrategy
from core.memory.procedural.strategy_recommendation.types import StrategyRecommendation

class IStrategyRecommendationEngine(ABC):
    @abstractmethod
    def recommend(
        self,
        current_fingerprint: DatasetFingerprint,
        user_intent: str,
        active_strategy: Optional[ProceduralStrategy],
        episodic_recommendations: List[EpisodeRecommendation]
    ) -> StrategyRecommendation:
        """
        Evaluates an active strategy against current constraints and past episodic recommendations
        to determine whether the brain should REUSE, MODIFY, or IGNORE the strategy.
        """
        pass
