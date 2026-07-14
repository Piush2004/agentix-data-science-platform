from typing import Dict, Any

class StateManager:
    """Manages execution and workspace state."""
    
    def __init__(self):
        self.state_store = {}
        
    def get_state(self, workspace_id: str) -> Dict[str, Any]:
        return self.state_store.get(workspace_id, {})
        
    def update_state(self, workspace_id: str, payload: Dict[str, Any]):
        if workspace_id not in self.state_store:
            self.state_store[workspace_id] = {}
        self.state_store[workspace_id].update(payload)
