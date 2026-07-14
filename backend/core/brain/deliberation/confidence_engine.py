from typing import List
from core.brain.deliberation.interfaces import IConfidenceEngine
from core.brain.deliberation.types import HypothesisEvaluation, DeliberationEvidence, ConfidenceScore

class DefaultConfidenceEngine(IConfidenceEngine):
    def calculate(self, evaluations: List[HypothesisEvaluation], evidence: List[DeliberationEvidence]) -> List[ConfidenceScore]:
        scores = []
        
        meta_ev = next((e.data for e in evidence if e.source == "DatasetMetadata"), {})
        has_missing = meta_ev.get("missing_values_count", 0) > 0
        has_dupes = meta_ev.get("duplicate_rows", 0) > 0
        goal_ev = next((e.data for e in evidence if e.source == "UserGoal"), {})
        intent = goal_ev.get("intent", "").lower()
        
        for ev in evaluations:
            base_score = 50.0
            reason = "Default baseline confidence."
            supporting_keys = []
            
            # Privacy penalties
            if ev.privacy_impact == "High":
                base_score -= 30.0
                reason = "High privacy risk utilizing this approach."
                supporting_keys.append("DatasetMetadata.has_pii")
                
            # Alignment with deterministic evidence
            if ev.llm_usage_required:
                if any(kw in intent for kw in ["predict", "math", "classify", "forecast", "regression"]):
                    base_score -= 20.0
                    reason = "LLM is poorly suited for strict math/prediction."
                elif any(kw in intent for kw in ["extract", "summarize", "reason", "understand"]):
                    base_score += 40.0
                    reason = "LLM excels at unstructured parsing."
                    supporting_keys.append("UserGoal.intent")
            
            if ev.execution_cost == 0.0 and ev.estimated_time_sec < 5:
                if not ev.llm_usage_required:
                    base_score += 20.0
                    reason = "Deterministic computation is verified as safe and efficient."
                    
            if ev.memory_impact == "High":
                base_score -= 10.0
                
            # Ensure score remains bounded
            final_score = max(0.0, min(100.0, base_score))
            
            scores.append(ConfidenceScore(
                hypothesis_id=ev.hypothesis_id,
                score=final_score,
                reason=reason,
                supporting_evidence_keys=supporting_keys
            ))
            
        return scores
