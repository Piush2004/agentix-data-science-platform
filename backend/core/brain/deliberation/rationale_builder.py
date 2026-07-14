from core.brain.deliberation.interfaces import IRationaleBuilder
from core.brain.deliberation.types import DeliberationHypothesis, HypothesisEvaluation, ConfidenceScore, DeliberationRationale

class DefaultRationaleBuilder(IRationaleBuilder):
    def build(self, best_hypothesis: DeliberationHypothesis, evaluation: HypothesisEvaluation, confidence: ConfidenceScore) -> DeliberationRationale:
        
        decision_summary = f"Selected Hypothesis: {best_hypothesis.description}"
        reason = confidence.reason
        evidence_summary = f"Based on deterministic analysis mapping to evidence: {', '.join(confidence.supporting_evidence_keys) if confidence.supporting_evidence_keys else 'General Baseline'}."
        
        return DeliberationRationale(
            decision_summary=decision_summary,
            reason=reason,
            evidence_summary=evidence_summary,
            confidence_score=confidence.score,
            expected_outcome=best_hypothesis.expected_outcome
        )
