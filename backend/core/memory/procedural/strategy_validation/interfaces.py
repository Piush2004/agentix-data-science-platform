from abc import ABC, abstractmethod
from typing import List
from core.memory.procedural.strategy_mining.types import StrategyCandidate
from core.memory.procedural.strategy_builder.types import ProceduralStrategy
from core.memory.procedural.strategy_validation.types import ValidationReport

class IStrategyValidationEngine(ABC):
    @abstractmethod
    def validate_candidate(
        self, 
        candidate: StrategyCandidate, 
        existing_strategies: List[ProceduralStrategy]
    ) -> ValidationReport:
        """
        Validates a strategy candidate against quality thresholds and existing active strategies.
        Checks for weakness, overfitting, and conflicts.
        """
        pass
