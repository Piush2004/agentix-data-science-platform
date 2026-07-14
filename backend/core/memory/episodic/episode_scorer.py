from core.memory.episodic.interfaces import IEpisodeScorer
from core.memory.episodic.types import Episode, EpisodeScores

class DefaultEpisodeScorer(IEpisodeScorer):
    def score(self, episode: Episode) -> EpisodeScores:
        success_score = episode.execution_metrics.success_score
        
        # Reusability: High if execution was fast, successful, and memory efficient
        reusability = success_score
        if episode.execution_metrics.execution_time_sec > 60:
            reusability -= 10
        if episode.execution_metrics.memory_usage_mb > 1000:
            reusability -= 10
            
        # Popularity starts at 0, grows over time
        popularity_score = 0.0
        
        # Learning score
        learning = 100.0 if episode.outcome == "FAILED" else 50.0
        
        return EpisodeScores(
            success_score=max(0.0, min(100.0, success_score)),
            reusability_score=max(0.0, min(100.0, reusability)),
            confidence_score=episode.confidence_score,
            learning_score=learning,
            popularity_score=popularity_score
        )
