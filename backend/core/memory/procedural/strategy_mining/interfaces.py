from abc import ABC, abstractmethod
from typing import List, Dict
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_mining.types import (
    EpisodeCluster,
    EpisodeClusterKey,
    ExecutionPattern,
    PatternFrequency,
    PatternSuccess,
    StrategyCandidate
)

class IEpisodeClusterer(ABC):
    @abstractmethod
    def cluster(self, episodes: List[Episode]) -> List[EpisodeCluster]:
        """Groups episodes by business domain, intent, and target variable."""
        pass

class IPatternDetector(ABC):
    @abstractmethod
    def detect_patterns(self, cluster: EpisodeCluster) -> Dict[ExecutionPattern, List[Episode]]:
        """Identifies distinct workflow and engine execution patterns within a cluster."""
        pass

class IFrequencyAnalyzer(ABC):
    @abstractmethod
    def analyze_frequency(self, pattern_map: Dict[ExecutionPattern, List[Episode]], total_episodes: int) -> List[PatternFrequency]:
        """Calculates how often each pattern appears within the cluster."""
        pass

class ISuccessAnalyzer(ABC):
    @abstractmethod
    def analyze_success(self, pattern_map: Dict[ExecutionPattern, List[Episode]]) -> List[PatternSuccess]:
        """Calculates average success scores and variances for patterns."""
        pass

class IStrategyCandidateGenerator(ABC):
    @abstractmethod
    def generate(self, cluster_key: EpisodeClusterKey, frequencies: List[PatternFrequency], successes: List[PatternSuccess]) -> List[StrategyCandidate]:
        """Synthesizes frequencies and successes into concrete StrategyCandidates."""
        pass
