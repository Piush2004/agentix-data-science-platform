import hashlib
from typing import List, Dict
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_mining.interfaces import IPatternDetector
from core.memory.procedural.strategy_mining.types import EpisodeCluster, ExecutionPattern

class DefaultPatternDetector(IPatternDetector):
    def detect_patterns(self, cluster: EpisodeCluster) -> Dict[ExecutionPattern, List[Episode]]:
        pattern_map: Dict[ExecutionPattern, List[Episode]] = {}
        
        for ep in cluster.episodes:
            # Extract workflow steps
            steps = [step.get("step", "unknown") for step in ep.workflow_plan]
            # Extract engines used
            engines = sorted(ep.engines_used)
            
            # Create a unique hash for the pattern
            pattern_str = f"steps:{','.join(steps)}|engines:{','.join(engines)}"
            pattern_hash = hashlib.md5(pattern_str.encode('utf-8')).hexdigest()
            
            pattern = ExecutionPattern(
                pattern_hash=pattern_hash,
                workflow_steps=steps,
                engines_used=engines
            )
            
            # Since pattern uses pattern_hash for equality/hashing
            if pattern not in pattern_map:
                pattern_map[pattern] = []
            pattern_map[pattern].append(ep)
            
        return pattern_map
