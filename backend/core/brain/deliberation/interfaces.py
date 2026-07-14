from abc import ABC, abstractmethod
from typing import List, Dict, Any
from core.brain.types import UnderstandingObject
from core.brain.deliberation.types import (
    DeliberationQuestion,
    DeliberationHypothesis,
    DeliberationEvidence,
    HypothesisEvaluation,
    ConfidenceScore,
    DeliberationRationale
)

class IQuestionGenerator(ABC):
    @abstractmethod
    def generate(self, understanding: UnderstandingObject) -> List[DeliberationQuestion]:
        """Ask internal structural questions about the task and dataset."""
        pass

class IEvidenceCollector(ABC):
    @abstractmethod
    def collect(self, understanding: UnderstandingObject) -> List[DeliberationEvidence]:
        """Collect deterministic evidence without using LLMs."""
        pass

class IHypothesisGenerator(ABC):
    @abstractmethod
    def generate(self, questions: List[DeliberationQuestion], evidence: List[DeliberationEvidence]) -> List[DeliberationHypothesis]:
        """Generate testable hypotheses based on questions and evidence."""
        pass

class IAlternativeAnalyzer(ABC):
    @abstractmethod
    def analyze(self, hypotheses: List[DeliberationHypothesis], evidence: List[DeliberationEvidence]) -> List[HypothesisEvaluation]:
        """Evaluate advantages, disadvantages, costs, and risks of hypotheses."""
        pass

class IConfidenceEngine(ABC):
    @abstractmethod
    def calculate(self, evaluations: List[HypothesisEvaluation], evidence: List[DeliberationEvidence]) -> List[ConfidenceScore]:
        """Assign measurable confidence scores to hypotheses."""
        pass

class IRationaleBuilder(ABC):
    @abstractmethod
    def build(self, best_hypothesis: DeliberationHypothesis, evaluation: HypothesisEvaluation, confidence: ConfidenceScore) -> DeliberationRationale:
        """Create structured, internal-only explanations for decisions."""
        pass
