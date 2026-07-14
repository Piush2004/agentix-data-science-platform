import json
import os
import time
from typing import Dict, Any, List, Optional

class BrainMemory:
    """
    Long-term persistent Knowledge Base mapping dataset profiles to historically successful workflow executions.
    Dynamically adjusts AI recommendations and creates learning loops for the platform.
    """
    def __init__(self, storage_path: str = "data/brain_memory.json"):
        self.storage_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{storage_path}")
        self.memory = {
            "successful_workflows": [],
            "user_preferences": {},
            "execution_metrics": []
        }
        self._load()
        
    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    self.memory = json.load(f)
            except Exception:
                pass
                
    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.memory, f, indent=4)
            
    def record_workflow_success(
        self, 
        dataset_name: str, 
        domain: str, 
        health_score: int, 
        target_task: str, 
        execution_dag: List[str], 
        models_used: List[str],
        execution_time_sec: float
    ):
        """
        Commits a completed workflow to the Knowledge Base.
        """
        health_range = f"{(health_score // 10) * 10}-{((health_score // 10) * 10) + 9}"
        entry = {
            "timestamp": time.time(),
            "dataset_name": dataset_name,
            "domain": domain,
            "health_score_range": health_range,
            "target_task": target_task,
            "execution_dag": execution_dag,
            "models_used": models_used,
            "execution_time_sec": execution_time_sec
        }
        self.memory["successful_workflows"].append(entry)
        self.memory["execution_metrics"].append({
            "dataset": dataset_name, 
            "time": execution_time_sec,
            "dag_length": len(execution_dag)
        })
        self._save()
        
    def set_user_preference(self, key: str, value: Any):
        self.memory["user_preferences"][key] = value
        self._save()
        
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        return self.memory["user_preferences"].get(key, default)
        
    def find_optimal_workflow(self, domain: str, health_score: int, target_task: str) -> Optional[Dict[str, Any]]:
        """
        Searches the Knowledge Base for a previously successful DAG matching the exact domain and health profile.
        Returns the execution DAG and reasoning if found.
        """
        if not self.memory["successful_workflows"]:
            return None
            
        health_range = f"{(health_score // 10) * 10}-{((health_score // 10) * 10) + 9}"
        
        # Sort by most recent
        workflows = sorted(self.memory["successful_workflows"], key=lambda x: x["timestamp"], reverse=True)
        
        # 1. Exact Match (Domain + Health + Task)
        for wf in workflows:
            if wf["domain"] == domain and wf["target_task"] == target_task and wf["health_score_range"] == health_range:
                return {
                    "dag": wf["execution_dag"],
                    "reason": f"A similar {domain} dataset with a {health_range} health score was previously analyzed successfully using this exact workflow."
                }
                
        # 2. Relaxed Match (Domain + Task)
        for wf in workflows:
            if wf["domain"] == domain and wf["target_task"] == target_task:
                return {
                    "dag": wf["execution_dag"],
                    "reason": f"A similar {domain} dataset used this workflow successfully in the past."
                }
                
        return None

brain_memory = BrainMemory()
