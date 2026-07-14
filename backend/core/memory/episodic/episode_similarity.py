from typing import List
from core.memory.episodic.interfaces import IEpisodeSimilarity
from core.memory.episodic.types import Episode, DatasetFingerprint, EpisodeRecommendation

class StructuralSimilarityEngine(IEpisodeSimilarity):
    def find_similar(self, current_fingerprint: DatasetFingerprint, intent: str, episodes: List[Episode]) -> List[EpisodeRecommendation]:
        recommendations = []
        
        for ep in episodes:
            score = 0.0
            
            # Domain matches heavily
            if ep.business_domain.lower() == current_fingerprint.business_domain.lower():
                score += 0.3
                
            # Intent matches heavily
            if ep.detected_intent.lower() == intent.lower():
                score += 0.3
                
            # Structural similarity (columns overlap)
            ep_cols = set(ep.dataset_fingerprint.columns)
            cur_cols = set(current_fingerprint.columns)
            if ep_cols and cur_cols:
                jaccard = len(ep_cols.intersection(cur_cols)) / len(ep_cols.union(cur_cols))
                score += (jaccard * 0.2)
                
            # Target variable match
            if ep.dataset_fingerprint.target_variable == current_fingerprint.target_variable and current_fingerprint.target_variable is not None:
                score += 0.2
                
            if score > 0:
                # Add recommendation with a reasoning
                reasoning = "High structural and intent match."
                if ep.execution_metrics.success_score >= 90:
                    reasoning += " Previous execution was highly successful."
                    
                recommendations.append(EpisodeRecommendation(
                    episode=ep,
                    similarity_score=round(score, 2),
                    recommended_workflow=ep.workflow_plan,
                    adaptation_reasoning=reasoning
                ))
                
        # Return top 5
        recommendations.sort(key=lambda x: (x.similarity_score, x.episode.execution_metrics.success_score), reverse=True)
        return recommendations[:5]
