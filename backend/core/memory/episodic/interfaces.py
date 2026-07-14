from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from core.memory.episodic.types import Episode, DatasetFingerprint, EpisodeRecommendation, EpisodeScores

class IEpisodeStore(ABC):
    @abstractmethod
    def create(self, episode: Episode) -> Episode: pass

    @abstractmethod
    def read(self, episode_id: str) -> Optional[Episode]: pass

    @abstractmethod
    def update(self, episode_id: str, episode: Episode) -> Episode: pass

    @abstractmethod
    def archive(self, episode_id: str) -> bool: pass

    @abstractmethod
    def delete(self, episode_id: str) -> bool: pass

    @abstractmethod
    def get_all(self) -> List[Episode]: pass

class IEpisodeIndex(ABC):
    @abstractmethod
    def index_episode(self, episode: Episode) -> bool: pass

    @abstractmethod
    def search_by_domain(self, domain: str) -> List[Episode]: pass

class IEpisodeSimilarity(ABC):
    @abstractmethod
    def find_similar(self, current_fingerprint: DatasetFingerprint, intent: str, episodes: List[Episode]) -> List[EpisodeRecommendation]: pass

class IEpisodeRetriever(ABC):
    @abstractmethod
    def retrieve_most_relevant(self, fingerprint: DatasetFingerprint, intent: str) -> List[Episode]: pass

class IEpisodeScorer(ABC):
    @abstractmethod
    def score(self, episode: Episode) -> EpisodeScores: pass

class IEpisodeValidator(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool: pass

class IEpisodeWriter(ABC):
    @abstractmethod
    def write_episode(self, raw_data: Dict[str, Any]) -> Episode: pass
