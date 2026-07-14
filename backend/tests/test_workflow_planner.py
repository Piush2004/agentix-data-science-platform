import pytest
import os
from core.agents.workflow_planner import WorkflowPlanningAgent

def test_workflow_planner_modeling():
    agent = WorkflowPlanningAgent(output_dir="data")
    
    # Mocking upstream profile states
    profile = {"inference": {"possible_ml_tasks": ["Classification"]}}
    quality = {"cleaning_required": True}
    domain = {"primary_domain": "Retail"}
    user_goal = "Train a model to predict churn."
    
    res = agent.generate_plan("churn.csv", user_goal, profile, quality, domain)
    
    plan = res["plan_data"]
    
    assert "Cleaning Agent" in plan["execution_order"]
    assert "Feature Engineering Agent" in plan["execution_order"]
    assert "AutoML Agent" in plan["execution_order"]
    assert "SHAP Agent" in plan["execution_order"]
    assert "Report Agent" in plan["execution_order"]
    
    assert plan["inferred_domain"] == "Retail"
    assert plan["estimated_time_sec"] >= 24.5 # 0.5 + 1.5 + 15 + 5 + 2.5
    assert os.path.exists(res["plan_path"])
    
def test_workflow_planner_eda_only():
    agent = WorkflowPlanningAgent(output_dir="data")
    
    # Mocking a pristine analytical dataset
    profile = {"inference": {"possible_ml_tasks": ["EDA only"]}}
    quality = {"cleaning_required": False}
    domain = {"primary_domain": "Healthcare"}
    user_goal = "Show me the distributions."
    
    res = agent.generate_plan("health.csv", user_goal, profile, quality, domain)
    
    plan = res["plan_data"]
    
    # Should completely bypass Cleaning and ML
    assert "Cleaning Agent" not in plan["execution_order"]
    assert "AutoML Agent" not in plan["execution_order"]
    
    # Should include EDA
    assert "EDA Agent" in plan["execution_order"]
    assert "LLM Agent" in plan["execution_order"]
    assert plan["expected_output"] == "LLM Agent Payload"
