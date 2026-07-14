import logging
from typing import Dict, Any, List
from core.memory.episodic.interfaces import (
    IEpisodeStore, IEpisodeIndex, IEpisodeSimilarity,
    IEpisodeRetriever, IEpisodeWriter, IEpisodeValidator, IEpisodeScorer
)
from core.memory.episodic.types import DatasetFingerprint, EpisodeRecommendation, Episode

class EpisodicMemoryController:
    """
    Facade for the entire Episodic Memory System.
    Handles retrieving past experiences and storing new ones.
    """
    def __init__(
        self,
        store: IEpisodeStore,
        index: IEpisodeIndex,
        similarity: IEpisodeSimilarity,
        retriever: IEpisodeRetriever,
        writer: IEpisodeWriter,
        validator: IEpisodeValidator,
        scorer: IEpisodeScorer
    ):
        self.store = store
        self.index = index
        self.similarity = similarity
        self.retriever = retriever
        self.writer = writer
        self.validator = validator
        self.scorer = scorer
        self.logger = logging.getLogger("Agentix.Memory.EpisodicController")

    def recall_experiences(self, fingerprint: DatasetFingerprint, intent: str) -> List[EpisodeRecommendation]:
        self.logger.info(f"Recalling experiences for intent '{intent}' and domain '{fingerprint.business_domain}'")
        # Find candidates
        candidates = self.store.get_all()
        # Find similar
        recommendations = self.similarity.find_similar(fingerprint, intent, candidates)
        self.logger.info(f"Found {len(recommendations)} similar episodes.")
        return recommendations

    def record_experience(self, raw_episode_data: Dict[str, Any]) -> Episode:
        self.logger.info("Recording new episode experience.")
        episode = self.writer.write_episode(raw_episode_data)
        scores = self.scorer.score(episode)
        self.logger.info(f"Episode {episode.episode_id} stored with success score {scores.success_score}")
        return episode
