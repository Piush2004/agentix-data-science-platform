import logging
from typing import List
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_mining.types import StrategyCandidate
from core.memory.procedural.strategy_mining.interfaces import (
    IEpisodeClusterer, IPatternDetector, IFrequencyAnalyzer, 
    ISuccessAnalyzer, IStrategyCandidateGenerator
)
from core.memory.procedural.strategy_mining.episode_clusterer import DefaultEpisodeClusterer
from core.memory.procedural.strategy_mining.pattern_detector import DefaultPatternDetector
from core.memory.procedural.strategy_mining.frequency_analyzer import DefaultFrequencyAnalyzer
from core.memory.procedural.strategy_mining.success_analyzer import DefaultSuccessAnalyzer
from core.memory.procedural.strategy_mining.strategy_candidates import DefaultStrategyCandidateGenerator

class StrategyMiner:
    """Facade for the Strategy Mining Engine."""
    
    def __init__(
        self,
        clusterer: IEpisodeClusterer = None,
        pattern_detector: IPatternDetector = None,
        frequency_analyzer: IFrequencyAnalyzer = None,
        success_analyzer: ISuccessAnalyzer = None,
        candidate_generator: IStrategyCandidateGenerator = None
    ):
        self.clusterer = clusterer or DefaultEpisodeClusterer()
        self.pattern_detector = pattern_detector or DefaultPatternDetector()
        self.frequency_analyzer = frequency_analyzer or DefaultFrequencyAnalyzer()
        self.success_analyzer = success_analyzer or DefaultSuccessAnalyzer()
        self.candidate_generator = candidate_generator or DefaultStrategyCandidateGenerator()
        self.logger = logging.getLogger("Agentix.Memory.StrategyMiner")

    def mine_strategies(self, episodes: List[Episode]) -> List[StrategyCandidate]:
        self.logger.info(f"Mining strategies from {len(episodes)} episodes.")
        
        all_candidates = []
        
        # 1. Cluster episodes
        clusters = self.clusterer.cluster(episodes)
        self.logger.info(f"Formed {len(clusters)} episode clusters.")
        
        for cluster in clusters:
            if len(cluster.episodes) < 2:
                continue # Skip isolated episodes
                
            # 2. Detect Patterns
            pattern_map = self.pattern_detector.detect_patterns(cluster)
            
            # 3. Analyze Frequency
            frequencies = self.frequency_analyzer.analyze_frequency(pattern_map, len(cluster.episodes))
            
            # 4. Analyze Success
            successes = self.success_analyzer.analyze_success(pattern_map)
            
            # 5. Generate Candidates
            candidates = self.candidate_generator.generate(cluster.cluster_key, frequencies, successes)
            all_candidates.extend(candidates)
            
        self.logger.info(f"Mined {len(all_candidates)} strategy candidates total.")
        return sorted(all_candidates, key=lambda x: x.confidence, reverse=True)
