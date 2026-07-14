from typing import List
from core.memory.procedural.strategy_builder.interfaces import IStrategyVersioning
from core.memory.procedural.strategy_builder.types import ProceduralStrategy

class DefaultStrategyVersioning(IStrategyVersioning):
    def resolve_version(self, new_strategy: ProceduralStrategy, history: List[ProceduralStrategy]) -> ProceduralStrategy:
        if not history:
            new_strategy.version = 1
            return new_strategy
            
        latest = max(history, key=lambda s: s.version)
        
        # Check if identical (excluding metadata like ID, dates, and version)
        if (
            new_strategy.workflow == latest.workflow and
            new_strategy.capabilities == latest.capabilities and
            new_strategy.conditions.model_dump() == latest.conditions.model_dump()
        ):
            # If the strategy is structurally identical, we don't need a new version,
            # but we might update success rates on the latest.
            # For strict versioning though, if we MUST output a strategy, we bump version only if it changed.
            # To simplify, we'll bump the version if we are explicitly instructed to save it.
            # But the prompt says: "Never overwrite previous versions. Implement version history."
            pass
            
        # Always bump version to retain lineage if we are generating a new strategy from mining
        new_strategy.version = latest.version + 1
        return new_strategy
