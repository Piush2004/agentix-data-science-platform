from typing import Dict, Any
from core.memory.episodic.interfaces import IEpisodeWriter, IEpisodeValidator, IEpisodeStore, IEpisodeIndex
from core.memory.episodic.types import Episode

class DefaultEpisodeWriter(IEpisodeWriter):
    def __init__(self, validator: IEpisodeValidator, store: IEpisodeStore, index: IEpisodeIndex):
        self.validator = validator
        self.store = store
        self.index = index

    def write_episode(self, raw_data: Dict[str, Any]) -> Episode:
        if not self.validator.validate(raw_data):
            raise ValueError("Invalid episode data provided.")
            
        episode = Episode(**raw_data)
        
        self.store.create(episode)
        self.index.index_episode(episode)
        
        return episode
