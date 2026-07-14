import statistics
from typing import List, Dict
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_mining.interfaces import ISuccessAnalyzer
from core.memory.procedural.strategy_mining.types import ExecutionPattern, PatternSuccess

class DefaultSuccessAnalyzer(ISuccessAnalyzer):
    def analyze_success(self, pattern_map: Dict[ExecutionPattern, List[Episode]]) -> List[PatternSuccess]:
        successes = []
        
        for pattern, eps in pattern_map.items():
            scores = [e.execution_metrics.success_score for e in eps]
            
            if not scores:
                avg = 0.0
                var = 0.0
            else:
                avg = statistics.mean(scores)
                var = statistics.variance(scores) if len(scores) > 1 else 0.0
                
            successes.append(PatternSuccess(
                pattern=pattern,
                average_success_score=avg,
                success_variance=var
            ))
            
        return successes
