from typing import List, Dict
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_mining.interfaces import IEpisodeClusterer
from core.memory.procedural.strategy_mining.types import EpisodeCluster, EpisodeClusterKey

class DefaultEpisodeClusterer(IEpisodeClusterer):
    def cluster(self, episodes: List[Episode]) -> List[EpisodeCluster]:
        clusters_map: Dict[EpisodeClusterKey, List[Episode]] = {}
        
        for ep in episodes:
            target = ep.dataset_fingerprint.target_variable or "none"
            key = EpisodeClusterKey(
                business_domain=ep.business_domain.lower(),
                detected_intent=ep.detected_intent.lower(),
                target_variable=target.lower()
            )
            
            if key not in clusters_map:
                clusters_map[key] = []
            clusters_map[key].append(ep)
            
        return [EpisodeCluster(cluster_key=k, episodes=v) for k, v in clusters_map.items()]
