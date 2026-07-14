from typing import List, Dict, Optional
from core.memory.procedural.strategy_builder.interfaces import IStrategyRepository
from core.memory.procedural.strategy_builder.types import ProceduralStrategy

class InMemoryStrategyRepository(IStrategyRepository):
    def __init__(self):
        # We index by (domain, intent) to maintain history
        self._history: Dict[str, List[ProceduralStrategy]] = {}
        # Simple id lookup
        self._store: Dict[str, ProceduralStrategy] = {}
        
    def _get_key(self, domain: str, intent: str) -> str:
        return f"{domain.lower()}|{intent.lower()}"

    def save(self, strategy: ProceduralStrategy) -> ProceduralStrategy:
        key = self._get_key(strategy.domain, strategy.intent)
        
        if key not in self._history:
            self._history[key] = []
            
        self._history[key].append(strategy)
        self._store[strategy.strategy_id] = strategy
        return strategy

    def get_by_id(self, strategy_id: str) -> Optional[ProceduralStrategy]:
        return self._store.get(strategy_id)

    def get_latest_version(self, domain: str, intent: str) -> Optional[ProceduralStrategy]:
        key = self._get_key(domain, intent)
        strategies = self._history.get(key, [])
        
        # Filter for active strategies and get the one with the highest version
        active_strategies = [s for s in strategies if s.is_active]
        if not active_strategies:
            return None
            
        return max(active_strategies, key=lambda s: s.version)

    def get_history(self, domain: str, intent: str) -> List[ProceduralStrategy]:
        key = self._get_key(domain, intent)
        return sorted(self._history.get(key, []), key=lambda s: s.version)
