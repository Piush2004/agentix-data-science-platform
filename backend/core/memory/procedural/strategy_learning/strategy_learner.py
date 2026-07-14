import copy
from typing import Tuple
from core.memory.episodic.types import Episode
from core.memory.procedural.strategy_builder.types import ProceduralStrategy
from core.memory.procedural.strategy_builder.interfaces import IStrategyRepository
from core.memory.procedural.strategy_learning.types import LearningReport, StrategyEvolutionReport, EvolutionStatus
from core.memory.procedural.strategy_learning.interfaces import IStrategyLearningEngine

class DeterministicStrategyLearner(IStrategyLearningEngine):
    def learn_from_episode(
        self, 
        strategy: ProceduralStrategy, 
        episode: Episode,
        repository: IStrategyRepository
    ) -> Tuple[ProceduralStrategy, StrategyEvolutionReport]:
        
        # 1. Copy to preserve immutability of the old version
        new_strategy = copy.deepcopy(strategy)
        
        # 2. Extract metrics
        n = max(1, new_strategy.usage_count) # Fallback to 1 if 0 to prevent division by zero conceptually
        ep_success = episode.execution_metrics.success_score
        ep_time = episode.execution_metrics.execution_time_sec
        
        # 3. Calculate new averages
        old_success = new_strategy.success_rate
        new_success = ((old_success * n) + ep_success) / (n + 1)
        
        old_time = new_strategy.average_execution_time
        new_time = ((old_time * n) + ep_time) / (n + 1)
        
        # 4. Update Confidence
        old_confidence = new_strategy.confidence
        # If the episode succeeded above our running average, we gain confidence
        if ep_success >= new_success:
            new_confidence = min(100.0, old_confidence + 2.0)
        else:
            # If it failed or performed worse, we lose confidence
            new_confidence = max(0.0, old_confidence - 5.0)
            
        # 5. Apply updates
        new_strategy.success_rate = new_success
        new_strategy.failure_rate = 100.0 - new_success
        new_strategy.average_execution_time = new_time
        new_strategy.confidence = new_confidence
        new_strategy.usage_count = n + 1
        
        # 6. Evaluate Evolution Status
        status = EvolutionStatus.MAINTAINED
        reasons = ["Strategy updated with new episode metrics."]
        
        if new_success < 50.0 or new_confidence < 60.0:
            status = EvolutionStatus.RETIRED
            new_strategy.is_active = False
            reasons.append(f"Strategy retired due to low success ({new_success:.1f}%) or confidence ({new_confidence:.1f}%).")
        elif new_success >= 90.0 and new_strategy.usage_count >= 5:
            status = EvolutionStatus.PROMOTED
            reasons.append("Strategy promoted to highly reliable due to sustained high success rates.")
            
        # 7. Version and Save
        new_strategy.version += 1
        saved_strategy = repository.save(new_strategy)
        
        # 8. Generate Reports
        learning_report = LearningReport(
            strategy_id=saved_strategy.strategy_id,
            previous_success_rate=old_success,
            new_success_rate=new_success,
            previous_confidence=old_confidence,
            new_confidence=new_confidence,
            execution_time_delta=new_time - old_time
        )
        
        evolution_report = StrategyEvolutionReport(
            strategy_id=saved_strategy.strategy_id,
            status=status,
            version=saved_strategy.version,
            learning_metrics=learning_report,
            reasons=reasons
        )
        
        return saved_strategy, evolution_report
