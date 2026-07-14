from typing import Dict, Any
from core.memory.episodic.interfaces import IEpisodeValidator

class DefaultEpisodeValidator(IEpisodeValidator):
    def validate(self, data: Dict[str, Any]) -> bool:
        # Check for required core fields
        required_keys = [
            "user_id", "workspace_id", "dataset_id", "dataset_fingerprint",
            "business_domain", "user_goal", "detected_intent", "workflow_plan",
            "execution_metrics", "outcome"
        ]
        
        for key in required_keys:
            if key not in data or data[key] is None:
                return False
                
        # Validate privacy - Ensure no raw data
        if "raw_data" in data or "raw_values" in data:
            return False
            
        return True
