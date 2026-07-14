from abc import ABC, abstractmethod
from typing import Any, Dict
from core.brain.types import (
    PerceptionObject,
    UnderstandingObject,
    ReasoningObject,
    ExecutionPlan,
    DecisionObject,
    LearningRecord
)

class IPerception(ABC):
    @abstractmethod
    def observe(self, raw_input: Dict[str, Any]) -> PerceptionObject:
        """Observe everything. Never make decisions."""
        pass

class IUnderstanding(ABC):
    @abstractmethod
    def interpret(self, perception: PerceptionObject) -> UnderstandingObject:
        """Interpret observations into intents and domain understanding."""
        pass

from core.brain.deliberation.types import DeliberationResult

class IReasoning(ABC):
    @abstractmethod
    def reason(self, deliberation: DeliberationResult) -> ReasoningObject:
        """Determine what should/should not happen based on internal deliberation."""
        pass

class IPlanning(ABC):
    @abstractmethod
    def plan(self, reasoning: ReasoningObject) -> ExecutionPlan:
        """Generate execution plans with cost and time estimates."""
        pass

class IDecision(ABC):
    @abstractmethod
    def decide(self, plans: list[ExecutionPlan], reasoning: ReasoningObject) -> DecisionObject:
        """Choose the best plan, engine, agent, and model."""
        pass

class IExecution(ABC):
    @abstractmethod
    def execute(self, decision: DecisionObject) -> Dict[str, Any]:
        """Coordinate engines and monitor execution."""
        pass

class ILearning(ABC):
    @abstractmethod
    def record_outcome(self, decision: DecisionObject, execution_result: Dict[str, Any]) -> LearningRecord:
        """Store statistics, feedback, and user preferences."""
        pass
