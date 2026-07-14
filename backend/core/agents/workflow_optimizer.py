import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class WorkflowOptimizer:
    """
    Evaluates dataset properties (size, missing values, duplicates, features) 
    before execution to generate decision rules that skip unnecessary compute steps.
    """
    
    def __init__(self):
        self.rules_applied = []

    def evaluate(self, dataset_profile: Dict[str, Any], quality_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs deterministic heuristics over dataset telemetry to build an optimized execution plan.
        """
        self.rules_applied = []
        
        # Extract features
        num_rows = dataset_profile.get("rows", 0)
        num_cols = dataset_profile.get("columns", 0)
        missing_count = quality_report.get("missing_cells", 0)
        duplicate_count = quality_report.get("duplicate_rows", 0)
        
        plan = {
            "skip_cleaning": False,
            "skip_distributed_execution": False,
            "skip_feature_engineering": False,
            "subsample_automl": False,
            "decision_rules": []
        }
        
        # Rule 1: Skip Cleaning
        if missing_count == 0 and duplicate_count == 0:
            plan["skip_cleaning"] = True
            self._log_rule("No missing values or duplicates detected -> Skip Cleaning Agent")

        # Rule 2: Skip Distributed Execution for Small Datasets
        # Assuming datasets < 50,000 rows can be processed in-memory sequentially
        if num_rows < 50000:
            plan["skip_distributed_execution"] = True
            self._log_rule(f"Small dataset ({num_rows} rows) -> Skip Distributed Execution Engine (use local pandas)")

        # Rule 3: Skip Feature Engineering if feature count is extremely small and linear
        if num_cols < 3:
            plan["skip_feature_engineering"] = True
            self._log_rule(f"Low feature count ({num_cols} cols) -> Skip Feature Engineering (Polynomial/PCA overhead unnecessary)")

        # Rule 4: Subsample AutoML for Massive Datasets
        if num_rows > 100000:
            plan["subsample_automl"] = True
            self._log_rule(f"Massive dataset ({num_rows} rows) -> Enable stratified subsampling for AutoML Hyperparameter tuning")

        plan["decision_rules"] = self.rules_applied
        return plan
        
    def _log_rule(self, rule_str: str):
        logger.info(f"[WorkflowOptimizer] {rule_str}")
        self.rules_applied.append(rule_str)

workflow_optimizer = WorkflowOptimizer()
