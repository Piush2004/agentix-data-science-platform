from typing import List
from core.brain.deliberation.interfaces import IAlternativeAnalyzer
from core.brain.deliberation.types import DeliberationHypothesis, DeliberationEvidence, HypothesisEvaluation

class DefaultAlternativeAnalyzer(IAlternativeAnalyzer):
    def analyze(self, hypotheses: List[DeliberationHypothesis], evidence: List[DeliberationEvidence]) -> List[HypothesisEvaluation]:
        evaluations = []
        
        meta_ev = next((e.data for e in evidence if e.source == "DatasetMetadata"), {})
        dataset_size = meta_ev.get("size_bytes", 0)
        
        for h in hypotheses:
            # Baseline evaluation values
            cost = 0.0
            time_sec = 0
            advantages = []
            disadvantages = []
            memory_impact = "Low"
            risk_level = "Low"
            privacy_impact = "None"
            llm_usage = False
            
            if "LLM" in h.description:
                cost = 0.05
                time_sec = 15
                advantages.append("Handles unstructured edge cases seamlessly.")
                disadvantages.append("Slower and more expensive.")
                llm_usage = True
                if meta_ev.get("has_pii"):
                    privacy_impact = "High"
                    risk_level = "High"
            
            if "Deterministic" in h.description or "unnecessary" in h.description:
                cost = 0.0
                time_sec = 1
                advantages.append("Fast and perfectly reproducible.")
                
            if "Cleaning is strictly required" in h.description:
                if dataset_size > 1024 * 1024 * 100: # 100MB
                    memory_impact = "High"
                    time_sec += 30
                advantages.append("Ensures downstream model integrity.")
                disadvantages.append("Modifies original data distribution.")
            
            if "unnecessary" in h.description:
                advantages.append("Preserves raw data state.")
                disadvantages.append("Models might fail if hidden nans exist.")
                
            if not advantages:
                advantages.append("Standard approach.")
            if not disadvantages:
                disadvantages.append("None significant.")

            evaluations.append(HypothesisEvaluation(
                hypothesis_id=h.id,
                advantages=advantages,
                disadvantages=disadvantages,
                execution_cost=cost,
                estimated_time_sec=time_sec,
                memory_impact=memory_impact,
                risk_level=risk_level,
                privacy_impact=privacy_impact,
                llm_usage_required=llm_usage
            ))
            
        return evaluations
