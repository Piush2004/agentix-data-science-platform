from typing import List
from core.memory.episodic.interfaces import IEpisodeRetriever, IEpisodeStore, IEpisodeIndex, IEpisodeSimilarity
from core.memory.episodic.types import Episode, DatasetFingerprint

class DefaultEpisodeRetriever(IEpisodeRetriever):
    def __init__(self, store: IEpisodeStore, index: IEpisodeIndex, similarity: IEpisodeSimilarity):
        self.store = store
        self.index = index
        self.similarity = similarity

    def retrieve_most_relevant(self, fingerprint: DatasetFingerprint, intent: str) -> List[Episode]:
        # Get candidates (could be all, or pre-filtered by domain)
        candidates = self.store.get_all()
        # Find similar
        recommendations = self.similarity.find_similar(fingerprint, intent, candidates)
        # Return episodes that have high success scores from the top recommendations
        return [rec.episode for rec in recommendations if rec.episode.execution_metrics.success_score > 70]
