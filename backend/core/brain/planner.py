from core.brain.models import ExecutionPlan
from typing import Dict, Any

class BrainPlanner:
    """Generates execution plans and agent routing strategies."""
    
    def generate_plan(self, user_request: str, context: Dict[str, Any]) -> ExecutionPlan:
        """Analyzes request and context to determine the execution plan."""
        # This is an architectural stub. Actual logic would integrate with Intent Router and Decision Engine.
        
        request_lower = str(user_request).lower()
        if "clean" in request_lower:
            return ExecutionPlan(
                target="Cleaning Agent",
                steps=["Metadata Agent", "Cleaning Agent"],
                confidence=0.9
            )
            
        return ExecutionPlan(
            target="LLM Agent",
            steps=["LLM Agent"],
            confidence=0.5
        )
