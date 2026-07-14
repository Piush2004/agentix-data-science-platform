import logging
from typing import List, Optional, Dict
from core.memory.episodic.interfaces import IEpisodeStore
from core.memory.episodic.types import Episode

class InMemoryEpisodeStore(IEpisodeStore):
    def __init__(self):
        self._store: Dict[str, Episode] = {}
        self._archived: Dict[str, Episode] = {}
        self.logger = logging.getLogger("Agentix.Memory.EpisodicStore")

    def create(self, episode: Episode) -> Episode:
        self._store[episode.episode_id] = episode
        self.logger.info(f"Created episode {episode.episode_id}")
        return episode

    def read(self, episode_id: str) -> Optional[Episode]:
        self.logger.info(f"Episode retrieved: {episode_id}")
        return self._store.get(episode_id) or self._archived.get(episode_id)

    def update(self, episode_id: str, episode: Episode) -> Episode:
        if episode_id in self._store:
            self._store[episode_id] = episode
            return episode
        raise ValueError(f"Episode {episode_id} not found.")

    def archive(self, episode_id: str) -> bool:
        if episode_id in self._store:
            self._archived[episode_id] = self._store.pop(episode_id)
            return True
        return False

    def delete(self, episode_id: str) -> bool:
        # Never overwrite/delete full history in a real DB, but we allow soft delete
        if episode_id in self._store:
            del self._store[episode_id]
            return True
        return False

    def get_all(self) -> List[Episode]:
        return list(self._store.values())
