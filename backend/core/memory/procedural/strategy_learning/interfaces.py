from abc import ABC, abstractmethod
from typing import Tuple
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_builder.types import ProceduralStrategy
from core.memory.procedural.strategy_learning.types import StrategyEvolutionReport
from core.memory.procedural.strategy_builder.interfaces import IStrategyRepository

class IStrategyLearningEngine(ABC):
    @abstractmethod
    def learn_from_episode(
        self, 
        strategy: ProceduralStrategy, 
        episode: Episode,
        repository: IStrategyRepository
    ) -> Tuple[ProceduralStrategy, StrategyEvolutionReport]:
        """
        Updates the strategy based on the outcome of a new episode.
        Versions the strategy in the repository if changes are made.
        Returns the updated Strategy (which may be retired/inactive) and the Evolution Report.
        """
        pass
