from typing import Dict, Any
from core.brain.state import StateManager

class ContextManager:
    """Manages context compilation from various data sources."""
    
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        
    def build_context(self, workspace_id: str, dataset_name: str) -> Dict[str, Any]:
        """Compiles the necessary context payload for the planner."""
        state = self.state_manager.get_state(workspace_id)
        return {
            "workspace_id": workspace_id,
            "dataset_name": dataset_name,
            "active_state": state
        }
