from abc import ABC, abstractmethod
from typing import List, Optional
from core.memory.procedural.strategy_mining.types import StrategyCandidate
from core.memory.procedural.strategy_builder.types import ProceduralStrategy

class IStrategyRepository(ABC):
    @abstractmethod
    def save(self, strategy: ProceduralStrategy) -> ProceduralStrategy:
        """Saves a strategy. Does not overwrite existing versions."""
        pass
        
    @abstractmethod
    def get_by_id(self, strategy_id: str) -> Optional[ProceduralStrategy]:
        pass
        
    @abstractmethod
    def get_latest_version(self, domain: str, intent: str) -> Optional[ProceduralStrategy]:
        """Gets the most recent active strategy for a given domain/intent."""
        pass
        
    @abstractmethod
    def get_history(self, domain: str, intent: str) -> List[ProceduralStrategy]:
        """Gets all versions of a strategy for a given domain/intent."""
        pass

class IStrategyVersioning(ABC):
    @abstractmethod
    def resolve_version(self, new_strategy: ProceduralStrategy, history: List[ProceduralStrategy]) -> ProceduralStrategy:
        """Determines if the new strategy is identical, or bumps the version if different."""
        pass

class IStrategyBuilder(ABC):
    @abstractmethod
    def build_from_candidate(self, candidate: StrategyCandidate) -> ProceduralStrategy:
        """Converts a mined candidate into a formal Strategy object."""
        pass
