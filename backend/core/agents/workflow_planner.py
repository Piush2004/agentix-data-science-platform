import json
import os
from typing import Dict, Any

class WorkflowPlanningAgent:
    """
    Synthesizes incoming contextual metadata (Data Quality, Dataset Profiles, Domain Taxonomy)
    with the raw user intent to formulate a highly optimized, deterministic step-by-step
    agent execution topology.
    """
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Hardcoded static performance estimates (seconds) for DAG elements
        self.time_map = {
            "Metadata Agent": 0.05, 
            "Cleaning Agent": 0.5, 
            "Feature Engineering Agent": 1.5, 
            "EDA Agent": 2.0, 
            "AutoML Agent": 15.0, 
            "SHAP Agent": 5.0, 
            "Report Agent": 2.5,
            "LLM Agent": 1.5
        }

    def generate_plan(
        self, 
        dataset_name: str,
        user_goal: str, 
        dataset_profile: Dict[str, Any], 
        quality_report: Dict[str, Any], 
        domain_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Dynamically constructs an execution sequence by routing across the platform's multi-agent matrix.
        """
        agents = []
        user_goal_lower = str(user_goal).lower()
        
        ml_task = dataset_profile.get("inference", {}).get("possible_ml_tasks", ["EDA only"])[0]
        needs_cleaning = quality_report.get("cleaning_required", False)
        health_score = quality_report.get("health_score", 100)
        domain = domain_profile.get("primary_domain", "General")
        
        # 0. Brain Memory Search (Historical Success Reuse)
        from core.brain.memory import brain_memory
        optimal_wf = brain_memory.find_optimal_workflow(domain, health_score, ml_task)
        
        if optimal_wf and "model" not in user_goal_lower: 
            # If the user has a generic goal, fallback to historically successful patterns
            unique_agents = optimal_wf["dag"]
            memory_reason = optimal_wf["reason"]
        else:
            memory_reason = "Generated novel execution DAG based on heuristics."
            
            # 1. Cleaning Phase Topology
            if needs_cleaning or any(w in user_goal_lower for w in ["clean", "fix", "impute", "drop"]):
                agents.append("Cleaning Agent")
                
            # 2. Exploratory Phase Topology
            if "model" not in user_goal_lower and "predict" not in user_goal_lower:
                agents.append("EDA Agent")
                
            # 3. Machine Learning Phase Topology
            is_modeling_goal = any(w in user_goal_lower for w in ["predict", "train", "model", "forecast", "classify", "regression"])
            
            if is_modeling_goal or (ml_task in ["Classification", "Regression"] and "report" in user_goal_lower):
                agents.append("Feature Engineering Agent")
                agents.append("AutoML Agent")
                
                # Explainability Injection
                if "explain" in user_goal_lower or "why" in user_goal_lower or "feature" in user_goal_lower or ml_task in ["Classification", "Regression"]:
                    agents.append("SHAP Agent")
                    
            # 4. Reporting & Synthesis Phase
            if "report" in user_goal_lower or "summary" in user_goal_lower or is_modeling_goal:
                agents.append("Report Agent")
            else:
                agents.append("LLM Agent")
                
        # 5. Graph Optimization via WorkflowOptimizer
        from core.agents.workflow_optimizer import workflow_optimizer
        optimization_plan = workflow_optimizer.evaluate(dataset_profile, quality_report)
        
        unique_agents = []
        for agent in agents:
            if agent == "Cleaning Agent" and optimization_plan["skip_cleaning"]:
                continue
            if agent == "Feature Engineering Agent" and optimization_plan["skip_feature_engineering"]:
                continue
            if agent not in unique_agents:
                unique_agents.append(agent)
                
        # 6. Telemetry & Confidence Math
        est_time = sum(self.time_map.get(a, 1.0) for a in unique_agents)
        confidence = 0.95 if len(unique_agents) > 0 else 0.50
        
        plan = {
            "dataset_name": dataset_name,
            "user_goal": user_goal,
            "inferred_domain": domain,
            "inferred_task": ml_task,
            "execution_order": unique_agents,
            "required_agents": unique_agents,
            "optimization_plan": optimization_plan,
            "estimated_time_sec": round(est_time, 2),
            "expected_output": f"{unique_agents[-1]} Payload",
            "confidence": confidence
        }
        
        # 7. Context Persistence
        plan_filename = f"{dataset_name.split('.')[0]}_workflow_plan.json"
        plan_path = os.path.join(self.output_dir, plan_filename)
        with open(plan_path, "w") as f:
            json.dump(plan, f, indent=4)
            
        return {
            "plan_data": plan,
            "plan_path": plan_path,
            "status": "SUCCESS"
        }
