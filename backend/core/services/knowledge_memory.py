import os
import json
from typing import Dict, Any, List

class KnowledgeMemory:
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(__file__), "../../../data/memory")
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        self.memory_file = os.path.join(self.base_dir, "global_memory.json")
        self.memory = {}
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            except Exception:
                self._initialize_empty()
        else:
            self._initialize_empty()

    def _initialize_empty(self):
        self.memory = {
            "workspaces": {},
            "preferences": {}
        }
        self._save_memory()

    def _save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=4)

    def set_preference(self, key: str, value: Any):
        self.memory["preferences"][key] = value
        self._save_memory()

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self.memory["preferences"].get(key, default)

    def _ensure_workspace(self, workspace_id: str):
        if workspace_id not in self.memory["workspaces"]:
            self.memory["workspaces"][workspace_id] = {
                "datasets": {},
                "chats": [],
                "reports": []
            }

    def add_dataset(self, workspace_id: str, dataset_name: str, metadata: dict = None):
        self._ensure_workspace(workspace_id)
        if dataset_name not in self.memory["workspaces"][workspace_id]["datasets"]:
            self.memory["workspaces"][workspace_id]["datasets"][dataset_name] = {
                "metadata": metadata or {},
                "models": [],
                "eda_summary": ""
            }
        else:
            if metadata:
                self.memory["workspaces"][workspace_id]["datasets"][dataset_name]["metadata"].update(metadata)
        self._save_memory()

    def add_model(self, workspace_id: str, dataset_name: str, model_info: dict):
        self._ensure_workspace(workspace_id)
        if dataset_name in self.memory["workspaces"][workspace_id]["datasets"]:
            self.memory["workspaces"][workspace_id]["datasets"][dataset_name]["models"].append(model_info)
            self._save_memory()

    def update_eda(self, workspace_id: str, dataset_name: str, eda_summary: str):
        self._ensure_workspace(workspace_id)
        if dataset_name in self.memory["workspaces"][workspace_id]["datasets"]:
            self.memory["workspaces"][workspace_id]["datasets"][dataset_name]["eda_summary"] = eda_summary
            self._save_memory()

    def add_chat(self, workspace_id: str, role: str, content: str):
        self._ensure_workspace(workspace_id)
        self.memory["workspaces"][workspace_id]["chats"].append({
            "role": role,
            "content": content
        })
        self._save_memory()

    def add_report(self, workspace_id: str, report_content: str):
        self._ensure_workspace(workspace_id)
        self.memory["workspaces"][workspace_id]["reports"].append(report_content)
        self._save_memory()

    def get_workspace_context(self, workspace_id: str) -> dict:
        return self.memory["workspaces"].get(workspace_id, {})
        
    def clear_memory(self):
        self._initialize_empty()

knowledge_memory = KnowledgeMemory()
