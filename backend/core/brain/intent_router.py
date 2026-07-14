import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class IntentRouter:
    """
    Intelligently routes natural language queries to the optimal execution engine.
    Reduces API costs and latency by intercepting deterministic tasks (Stats, SQL, Python)
    and redirecting them away from expensive LLM inference loops.
    """
    
    def __init__(self):
        self.stats_keywords = {"average", "mean", "median", "sum", "count", "max", "min", "standard deviation", "variance"}
        self.sql_keywords = {"select", "from", "where", "group by", "order by", "join"}
        self.workflow_keywords = {"plan", "workflow", "pipeline", "orchestrate", "sequence"}
        
        # Token metrics tracking (Simulated for reporting)
        self.tokens_saved = 0
        
    def _estimate_tokens(self, df_shape: tuple) -> int:
        """Estimates token footprint of a dataset context."""
        rows, cols = df_shape
        # Rough heuristic: 1 token per cell + metadata overhead
        return (rows * cols) + 500
        
    def route_query(self, query: str, df_shape: tuple = (0,0)) -> Dict[str, Any]:
        """
        Parses the query and returns the destination engine and token savings.
        """
        query_lower = query.lower()
        
        # 1. SQL Engine
        if any(keyword in query_lower for keyword in self.sql_keywords) and "select " in query_lower:
            estimated_cost = self._estimate_tokens(df_shape)
            self.tokens_saved += estimated_cost
            return {
                "engine": "SQL",
                "reason": "Explicit SQL syntax detected.",
                "tokens_saved": estimated_cost
            }
            
        # 2. Pandas (Statistics & Aggregation)
        if any(keyword in query_lower for keyword in self.stats_keywords):
            estimated_cost = self._estimate_tokens(df_shape)
            self.tokens_saved += estimated_cost
            return {
                "engine": "Pandas",
                "reason": "Statistical aggregation keyword detected (e.g., mean, sum).",
                "tokens_saved": estimated_cost
            }
            
        # 3. Agentix Brain (Workflow Planning)
        if any(keyword in query_lower for keyword in self.workflow_keywords):
            return {
                "engine": "Agentix Brain",
                "reason": "Workflow orchestration or execution planning requested.",
                "tokens_saved": 0
            }
            
        # 4. Python (Deterministic Algorithms)
        if "calculate" in query_lower or "compute" in query_lower:
            estimated_cost = self._estimate_tokens(df_shape)
            self.tokens_saved += estimated_cost
            return {
                "engine": "Python",
                "reason": "Deterministic calculation requested.",
                "tokens_saved": estimated_cost
            }
            
        # 5. Default Fallback: LLM (Business Reasoning)
        return {
            "engine": "LLM",
            "reason": "Complex business reasoning or open-ended question detected.",
            "tokens_saved": 0
        }
        
    def get_token_savings(self) -> int:
        return self.tokens_saved

intent_router = IntentRouter()
