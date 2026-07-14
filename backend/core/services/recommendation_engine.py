import json
import os
from typing import Dict, Any, List

class RecommendationEngine:
    """
    Translates raw workflow execution graphs into human-readable Recommendation Cards.
    Forces the platform to seek user approval before initiating heavy computational nodes.
    """
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_recommendations(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses a workflow plan and generates explicit approval cards.
        """
        agents_to_run = plan.get("execution_order", [])
        dataset_name = plan.get("dataset_name", "Unknown Dataset")
        domain = plan.get("inferred_domain", "Unknown Domain")
        
        recommendations = []
        
        for agent in agents_to_run:
            card = self._build_card(agent, domain, plan)
            if card:
                recommendations.append(card)
                
        payload = {
            "dataset_name": dataset_name,
            "header": f"I detected a {domain} dataset. Here is my recommended execution strategy:",
            "recommendations": recommendations,
            "total_estimated_time_sec": sum(r["estimated_duration_sec"] for r in recommendations)
        }
        
        rec_filename = f"{dataset_name.split('.')[0]}_recommendations.json"
        rec_path = os.path.join(self.output_dir, rec_filename)
        with open(rec_path, "w") as f:
            json.dump(payload, f, indent=4)
            
        return payload
        
    def _build_card(self, agent_name: str, domain: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates specific reasoning and risk metrics for each computational node.
        """
        if agent_name == "Cleaning Agent":
            return {
                "action": "Clean Data",
                "reason": "Dataset contains missing values or corrupt data structures based on quality diagnostics.",
                "expected_benefit": "Prevents downstream machine learning models from crashing.",
                "estimated_duration_sec": 0.5,
                "confidence": 0.99,
                "risk": "Low (Uses standard imputation)"
            }
        elif agent_name == "EDA Agent":
            return {
                "action": "Generate Exploratory Analytics",
                "reason": f"Understand the statistical distributions of the {domain} data.",
                "expected_benefit": "Identifies hidden correlations and outliers mathematically.",
                "estimated_duration_sec": 2.0,
                "confidence": 0.95,
                "risk": "None"
            }
        elif agent_name == "Feature Engineering Agent":
            return {
                "action": "Engineer Features",
                "reason": "Prepare categorical variables and scale numericals for algorithmic ingestion.",
                "expected_benefit": "Significantly improves predictive accuracy metrics (R2 / F1).",
                "estimated_duration_sec": 1.5,
                "confidence": 0.90,
                "risk": "Medium (May drop un-encodable text strings)"
            }
        elif agent_name == "AutoML Agent":
            task = plan.get("inferred_task", "Machine Learning")
            return {
                "action": f"Train {task} Models",
                "reason": f"Discovered target columns suitable for predictive {task}.",
                "expected_benefit": "Produces a mathematically optimized champion predictive model.",
                "estimated_duration_sec": 15.0,
                "confidence": 0.85,
                "risk": "High (Computationally expensive)"
            }
        elif agent_name == "SHAP Agent":
            return {
                "action": "Generate SHAP Explanations",
                "reason": "Neural networks and tree models act as opaque black boxes.",
                "expected_benefit": "Provides exact mathematical attribution for why predictions are made.",
                "estimated_duration_sec": 5.0,
                "confidence": 0.95,
                "risk": "Medium (Requires heavy memory overhead)"
            }
        elif agent_name == "Report Agent":
            return {
                "action": "Build Executive Report",
                "reason": "Raw mathematical metrics require business translation.",
                "expected_benefit": "Outputs a clean, boardroom-ready Markdown artifact.",
                "estimated_duration_sec": 2.5,
                "confidence": 0.99,
                "risk": "Low"
            }
        return None
