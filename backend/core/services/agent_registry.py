from typing import Dict, Any, List

class AgentRecord:
    def __init__(self, name: str, purpose: str, capabilities: List[str], inputs: List[str], outputs: List[str], dependencies: List[str], exec_cost: float, version: str="1.0.0"):
        self.id = name.lower().replace(" ", "_")
        self.name = name
        self.purpose = purpose
        self.capabilities = capabilities
        self.inputs = inputs
        self.outputs = outputs
        self.dependencies = dependencies
        self.exec_cost = exec_cost
        self.avg_runtime = 0.0
        self.execution_count = 0
        self.status = "Idle" # Idle, Running, Failed
        self.health = "Healthy" # Healthy, Degraded, Offline
        self.version = version
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "purpose": self.purpose,
            "capabilities": self.capabilities,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "dependencies": self.dependencies,
            "exec_cost": self.exec_cost,
            "avg_runtime": round(self.avg_runtime, 4),
            "status": self.status,
            "health": self.health,
            "version": self.version
        }
        
    def update_runtime(self, new_runtime: float):
        total = self.avg_runtime * self.execution_count
        self.execution_count += 1
        self.avg_runtime = (total + new_runtime) / self.execution_count

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, AgentRecord] = {}
        self._seed_default_agents()
        
    def _seed_default_agents(self):
        defaults = [
            ("Metadata Agent", "Extracts dataset shapes, types, and null counts", ["Schema Detection", "Type Inference"], ["raw_dataframe"], ["metadata_json"], [], 0.01),
            ("Privacy Agent", "Detects and masks PII/sensitive data", ["PII Masking", "Pseudonymization"], ["raw_dataframe"], ["masked_dataframe", "privacy_report"], ["Metadata Agent"], 0.05),
            ("EDA Agent", "Calculates statistical correlations and distributions", ["Correlation Matrix", "Skewness"], ["dataframe"], ["eda_summary"], ["Metadata Agent"], 0.10),
            ("Cleaning Agent", "Imputes missing values and handles outliers", ["Imputation", "Outlier Removal"], ["dataframe", "metadata_json"], ["cleaned_dataframe"], ["Metadata Agent"], 0.15),
            ("Feature Engineering Agent", "Encodes categoricals and scales features", ["One-Hot Encoding", "Standard Scaling"], ["cleaned_dataframe"], ["engineered_dataframe"], ["Cleaning Agent"], 0.20),
            ("AutoML Agent", "Trains and validates predictive models", ["Model Selection", "Cross Validation"], ["engineered_dataframe"], ["champion_model", "metrics"], ["Feature Engineering Agent"], 5.00),
            ("Visualization Agent", "Generates charts and plots", ["Matplotlib", "Seaborn"], ["dataframe", "eda_summary"], ["charts"], ["EDA Agent"], 0.10),
            ("SHAP Agent", "Extracts mathematical feature importances", ["SHAP Values", "Explainability"], ["champion_model", "engineered_dataframe"], ["shap_report"], ["AutoML Agent"], 1.50),
            ("Report Agent", "Generates executive markdown reports", ["Summarization"], ["metrics", "shap_report", "eda_summary"], ["markdown_report"], ["SHAP Agent"], 0.50),
            ("Memory Agent", "Interfaces with Knowledge Memory for context persistence", ["Vector Embeddings", "Retrieval"], ["query", "workspace_id"], ["historical_context"], [], 0.05),
            ("LLM Agent", "Main reasoning engine for natural language generation", ["Text Generation", "Reasoning"], ["context", "query"], ["answer"], [], 0.25)
        ]
        
        for p in defaults:
            record = AgentRecord(name=p[0], purpose=p[1], capabilities=p[2], inputs=p[3], outputs=p[4], dependencies=p[5], exec_cost=p[6])
            self.agents[record.id] = record
            
    def register(self, record: AgentRecord):
        self.agents[record.id] = record
        
    def get_all(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self.agents.values()]
        
    def get_by_id(self, agent_id: str) -> Dict[str, Any]:
        if agent_id in self.agents:
            return self.agents[agent_id].to_dict()
        return None
        
    def update_status(self, agent_id: str, status: str, health: str = None):
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            if health:
                self.agents[agent_id].health = health

agent_registry = AgentRegistry()
