import os
import sys
import json
import asyncio
import pandas as pd
import numpy as np

# Adjust paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.dataset_understanding import DatasetUnderstandingAgent
from app.agents.data_quality import DataQualityAgent
from app.agents.domain_detection import DomainDetectionAgent
from app.agents.workflow_planner import WorkflowPlanningAgent
from app.core.langgraph_engine import execute_pipeline

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/synthetic_datasets"))
os.makedirs(DATA_DIR, exist_ok=True)

def generate_retail_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "customer_id": range(1, n+1),
        "age": np.random.randint(18, 70, n),
        "income": np.random.normal(50000, 15000, n),
        "store_visits": np.random.randint(1, 50, n),
        "online_purchases": np.random.randint(0, 20, n),
    })
    df["total_spend"] = (df["income"] * 0.01) + (df["store_visits"] * 50) + (df["online_purchases"] * 100) + np.random.normal(0, 100, n)
    # Add missing values
    df.loc[10:50, "age"] = np.nan
    path = os.path.join(DATA_DIR, "retail_sales.csv")
    df.to_csv(path, index=False)
    return "retail_sales.csv", df, "Predict customer total spend"

def generate_healthcare_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "patient_id": range(1, n+1),
        "blood_pressure": np.random.normal(120, 15, n),
        "heart_rate": np.random.normal(70, 10, n),
        "cholesterol": np.random.normal(200, 30, n),
        "bmi": np.random.normal(25, 4, n),
    })
    df["risk_score"] = (df["blood_pressure"] * 0.5) + (df["cholesterol"] * 0.3) + (df["bmi"] * 1.5) + np.random.normal(0, 5, n)
    path = os.path.join(DATA_DIR, "healthcare_patients.csv")
    df.to_csv(path, index=False)
    return "healthcare_patients.csv", df, "Model patient risk scores"

def generate_finance_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "transaction_id": range(1, n+1),
        "amount": np.random.exponential(100, n),
        "distance_from_home": np.random.exponential(50, n),
        "previous_declines": np.random.poisson(0.1, n),
    })
    df["fraud_probability"] = (df["amount"] * 0.05) + (df["distance_from_home"] * 0.1) + (df["previous_declines"] * 50) + np.random.normal(0, 2, n)
    path = os.path.join(DATA_DIR, "finance_transactions.csv")
    df.to_csv(path, index=False)
    return "finance_transactions.csv", df, "Analyze transaction fraud probability"

def run_evaluation():
    datasets = [
        generate_retail_data(),
        generate_healthcare_data(),
        generate_finance_data()
    ]
    
    # Initialize Agents
    understanding_agent = DatasetUnderstandingAgent()
    quality_agent = DataQualityAgent()
    domain_agent = DomainDetectionAgent()
    planner_agent = WorkflowPlanningAgent()
    
    report_data = []
    
    for filename, df, user_goal in datasets:
        print(f"\n======================================")
        print(f"Evaluating Dataset: {filename}")
        print(f"Goal: {user_goal}")
        print(f"======================================")
        
        # 1. Understanding
        profile_res = understanding_agent.analyze(df, filename)
        profile = profile_res.get("profile_data", profile_res.get("profile", {}))
        
        # 2. Quality
        quality = quality_agent.analyze(df, filename)["report_data"]
        
        # 3. Domain
        domain = domain_agent.analyze(df, filename).get("report_data", domain_agent.analyze(df, filename))
        
        # 4. Planning
        plan_res = planner_agent.generate_plan(filename, user_goal, profile, quality, domain)
        plan = plan_res["plan_data"]
        plan_path = plan_res["plan_path"]
        
        # 5. Approve the plan explicitly for the Decision Engine
        with open(plan_path, "w") as f:
            plan["status"] = "USER_APPROVED"
            json.dump(plan, f, indent=4)
            
        print(f"Generated Workflow: {plan['execution_order']}")
            
        # 6. Execute through the Brain Orchestrator
        final_state = execute_pipeline(filename, df)
        
        # 7. Collect Results
        automl = final_state.get("automl_outputs", {})
        r2_score = automl.get("metrics", {}).get("R2", "N/A")
        agents_run = list(final_state.get("agent_status", {}).keys())
        errors = final_state.get("errors", {})
        
        print(f"Agents Executed: {agents_run}")
        print(f"AutoML R2 Score: {r2_score}")
        if errors:
            print(f"Errors: {errors}")
            
        report_data.append({
            "dataset": filename,
            "domain": domain.get("primary_domain", "Unknown"),
            "health_score": quality.get("health_score", 0),
            "workflow_executed": agents_run,
            "r2_score": r2_score,
            "errors": errors
        })
        
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/evaluation_report.json"))
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print(f"\nEvaluation Complete! Report saved to {report_path}")

if __name__ == "__main__":
    run_evaluation()
