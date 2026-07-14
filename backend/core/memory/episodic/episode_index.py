from typing import List, Dict
from core.memory.episodic.interfaces import IEpisodeIndex
from core.memory.episodic.types import Episode

class InMemoryEpisodeIndex(IEpisodeIndex):
    def __init__(self):
        self.domain_index: Dict[str, List[Episode]] = {}
        self.intent_index: Dict[str, List[Episode]] = {}

    def index_episode(self, episode: Episode) -> bool:
        # Index by domain
        domain = episode.business_domain.lower()
        if domain not in self.domain_index:
            self.domain_index[domain] = []
        self.domain_index[domain].append(episode)

        # Index by intent
        intent = episode.detected_intent.lower()
        if intent not in self.intent_index:
            self.intent_index[intent] = []
        self.intent_index[intent].append(episode)
        
        return True

    def search_by_domain(self, domain: str) -> List[Episode]:
        return self.domain_index.get(domain.lower(), [])
