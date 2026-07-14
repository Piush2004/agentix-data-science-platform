import uuid
from typing import List
from core.memory.procedural.strategy_mining.interfaces import IStrategyCandidateGenerator
from core.memory.procedural.strategy_mining.types import (
    EpisodeClusterKey,
    PatternFrequency,
    PatternSuccess,
    StrategyCandidate
)

class DefaultStrategyCandidateGenerator(IStrategyCandidateGenerator):
    def generate(
        self, 
        cluster_key: EpisodeClusterKey, 
        frequencies: List[PatternFrequency], 
        successes: List[PatternSuccess]
    ) -> List[StrategyCandidate]:
        candidates = []
        
        for freq in frequencies:
            # Find matching success metrics
            success_metric = next((s for s in successes if s.pattern == freq.pattern), None)
            
            if not success_metric:
                continue
                
            # Confidence logic: High frequency and high success = high confidence.
            # Variance reduces confidence.
            base_confidence = (freq.frequency_percentage * 0.4) + (success_metric.average_success_score * 0.6)
            variance_penalty = min(20.0, success_metric.success_variance / 100.0)
            confidence = max(0.0, min(100.0, base_confidence - variance_penalty))
            
            # Only consider it a viable candidate if it has some baseline frequency or success
            if freq.occurrence_count >= 2 and success_metric.average_success_score >= 50.0:
                candidate = StrategyCandidate(
                    candidate_id=str(uuid.uuid4()),
                    cluster_key=cluster_key,
                    pattern=freq.pattern,
                    supporting_episode_ids=freq.supporting_episode_ids,
                    frequency=freq.frequency_percentage,
                    average_success=success_metric.average_success_score,
                    confidence=confidence
                )
                candidates.append(candidate)
                
        return sorted(candidates, key=lambda x: x.confidence, reverse=True)
