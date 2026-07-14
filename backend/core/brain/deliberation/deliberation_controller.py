import logging
from typing import List, Dict, Any
from core.brain.types import UnderstandingObject
from core.brain.deliberation.types import DeliberationResult, RankedHypothesis
from core.brain.deliberation.interfaces import (
    IQuestionGenerator, IEvidenceCollector, IHypothesisGenerator,
    IAlternativeAnalyzer, IConfidenceEngine, IRationaleBuilder
)
from core.brain.deliberation.question_generator import DefaultQuestionGenerator
from core.brain.deliberation.evidence_collector import DefaultEvidenceCollector
from core.brain.deliberation.hypothesis_generator import DefaultHypothesisGenerator
from core.brain.deliberation.alternative_analyzer import DefaultAlternativeAnalyzer
from core.brain.deliberation.confidence_engine import DefaultConfidenceEngine
from core.brain.deliberation.rationale_builder import DefaultRationaleBuilder

class DeliberationController:
    """
    Coordinates the internal deliberation cycle of the Agentix Brain.
    """
    def __init__(
        self,
        question_generator: IQuestionGenerator = None,
        evidence_collector: IEvidenceCollector = None,
        hypothesis_generator: IHypothesisGenerator = None,
        alternative_analyzer: IAlternativeAnalyzer = None,
        confidence_engine: IConfidenceEngine = None,
        rationale_builder: IRationaleBuilder = None
    ):
        self.question_generator = question_generator or DefaultQuestionGenerator()
        self.evidence_collector = evidence_collector or DefaultEvidenceCollector()
        self.hypothesis_generator = hypothesis_generator or DefaultHypothesisGenerator()
        self.alternative_analyzer = alternative_analyzer or DefaultAlternativeAnalyzer()
        self.confidence_engine = confidence_engine or DefaultConfidenceEngine()
        self.rationale_builder = rationale_builder or DefaultRationaleBuilder()
        self.logger = logging.getLogger("Agentix.Brain.Deliberation")

    def deliberate(self, understanding: UnderstandingObject) -> DeliberationResult:
        self.logger.info("[DELIBERATION] Starting deliberation cycle.")
        
        # 1. Ask Questions
        questions = self.question_generator.generate(understanding)
        self.logger.info(f"[DELIBERATION] Generated {len(questions)} internal questions.")

        # 2. Collect Evidence deterministically
        evidence = self.evidence_collector.collect(understanding)
        self.logger.info(f"[DELIBERATION] Collected {len(evidence)} pieces of deterministic evidence.")

        # 3. Generate Hypotheses
        hypotheses = self.hypothesis_generator.generate(questions, evidence)
        self.logger.info(f"[DELIBERATION] Formulated {len(hypotheses)} hypotheses.")

        # 4. Analyze Alternatives
        evaluations = self.alternative_analyzer.analyze(hypotheses, evidence)
        
        # 5. Calculate Confidence
        confidences = self.confidence_engine.calculate(evaluations, evidence)

        # Combine into Ranked Hypotheses
        ranked_list: List[RankedHypothesis] = []
        for h in hypotheses:
            ev = next(e for e in evaluations if e.hypothesis_id == h.id)
            conf = next(c for c in confidences if c.hypothesis_id == h.id)
            ranked_list.append(RankedHypothesis(
                hypothesis=h,
                evaluation=ev,
                confidence=conf,
                rank=0 # Temporary
            ))

        # Sort by confidence
        ranked_list.sort(key=lambda x: x.confidence.score, reverse=True)
        for i, rh in enumerate(ranked_list):
            rh.rank = i + 1

        if not ranked_list:
            raise ValueError("Deliberation produced zero viable hypotheses.")

        chosen = ranked_list[0]
        self.logger.info(f"[DELIBERATION] Selected hypothesis '{chosen.hypothesis.description}' with confidence {chosen.confidence.score}")

        # 6. Build Rationale
        rationale = self.rationale_builder.build(chosen.hypothesis, chosen.evaluation, chosen.confidence)

        # Formulate final result
        evidence_summary = {e.source: e.reliability_score for e in evidence}

        return DeliberationResult(
            questions=questions,
            hypotheses=hypotheses,
            evidence_summary=evidence_summary,
            alternatives=ranked_list,
            chosen_hypothesis=chosen,
            rationale=rationale,
            risk_assessment=chosen.evaluation.risk_level,
            recommended_next_action="PROCEED_WITH_CHOSEN_HYPOTHESIS",
            estimated_cost=chosen.evaluation.execution_cost,
            estimated_time=chosen.evaluation.estimated_time_sec
        )
