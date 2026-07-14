from typing import List, Dict
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_mining.interfaces import IFrequencyAnalyzer
from core.memory.procedural.strategy_mining.types import ExecutionPattern, PatternFrequency

class DefaultFrequencyAnalyzer(IFrequencyAnalyzer):
    def analyze_frequency(self, pattern_map: Dict[ExecutionPattern, List[Episode]], total_episodes: int) -> List[PatternFrequency]:
        frequencies = []
        
        if total_episodes == 0:
            return frequencies
            
        for pattern, eps in pattern_map.items():
            count = len(eps)
            percentage = (count / total_episodes) * 100.0
            
            frequencies.append(PatternFrequency(
                pattern=pattern,
                supporting_episode_ids=[e.episode_id for e in eps],
                occurrence_count=count,
                frequency_percentage=percentage
            ))
            
        return frequencies
