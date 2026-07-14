from typing import List
from core.memory.procedural.strategy_mining.types import StrategyCandidate
from core.memory.procedural.strategy_builder.types import ProceduralStrategy
from core.memory.procedural.strategy_validation.types import ValidationReport, ValidationStatus
from core.memory.procedural.strategy_validation.interfaces import IStrategyValidationEngine

class DeterministicStrategyValidator(IStrategyValidationEngine):
    def __init__(self, min_episodes: int = 3, min_success_rate: float = 70.0, min_confidence: float = 60.0):
        self.min_episodes = min_episodes
        self.min_success_rate = min_success_rate
        self.min_confidence = min_confidence

    def validate_candidate(self, candidate: StrategyCandidate, existing_strategies: List[ProceduralStrategy]) -> ValidationReport:
        reasons = []
        status = ValidationStatus.APPROVED
        
        # 1. Check Weakness (Success Rate & Confidence)
        if candidate.average_success < self.min_success_rate:
            reasons.append(f"Weak candidate: average success ({candidate.average_success}%) is below minimum ({self.min_success_rate}%).")
            status = ValidationStatus.REJECTED
            
        if candidate.confidence < self.min_confidence:
            reasons.append(f"Weak candidate: confidence ({candidate.confidence}%) is below minimum ({self.min_confidence}%).")
            status = ValidationStatus.REJECTED
            
        # 2. Check Data Sufficiency
        num_episodes = len(candidate.supporting_episode_ids)
        if num_episodes < self.min_episodes and status != ValidationStatus.REJECTED:
            reasons.append(f"Requires more data: Only {num_episodes} supporting episodes. Minimum is {self.min_episodes}.")
            status = ValidationStatus.REQUIRES_MORE_DATA
            
        # 3. Check Conflicts & Overfitting against existing strategies
        for existing in existing_strategies:
            # We only care about active strategies in the same domain/intent
            if not existing.is_active:
                continue
                
            if existing.domain == candidate.cluster_key.business_domain and existing.intent == candidate.cluster_key.detected_intent:
                # If they solve the exact same intent but the existing one is significantly better, this is conflicting/weak
                if existing.success_rate > candidate.average_success + 10.0:
                    reasons.append(f"Conflicting strategy: Existing strategy {existing.strategy_id} has a significantly higher success rate ({existing.success_rate}% vs {candidate.average_success}%).")
                    status = ValidationStatus.REJECTED
                    
                # If they share the exact same workflow and conditions, it's a duplicate (or overfitted slice)
                if existing.workflow == candidate.pattern.workflow_steps:
                    reasons.append(f"Overfitted/Duplicate: Pattern already exists in active strategy {existing.strategy_id}.")
                    status = ValidationStatus.REJECTED
                    
        return ValidationReport(
            candidate_id=candidate.candidate_id,
            status=status,
            reasons=reasons
        )
