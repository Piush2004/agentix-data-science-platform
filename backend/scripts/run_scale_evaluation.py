import os
import sys
import json
import pandas as pd
import numpy as np

# Adjust paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.dataset_understanding import DatasetUnderstandingAgent
from app.agents.data_quality import DataQualityAgent
from app.agents.domain_detection import DomainDetectionAgent
from app.agents.workflow_planner import WorkflowPlanningAgent
from app.core.langgraph_engine import execute_pipeline
from sklearn.datasets import fetch_california_housing, load_iris, load_breast_cancer, load_wine, load_diabetes

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/scale_datasets"))
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Synthesize 15 Datasets
def synthesize_data():
    datasets = []
    
    # Domains and targets
    specs = [
        ("retail_sales_q1.csv", "Predict total spend", "spend", "regression"),
        ("hr_attrition.csv", "Predict employee churn", "churn", "classification"),
        ("supply_chain_delays.csv", "Model shipment delay days", "delay_days", "regression"),
        ("marketing_conversion.csv", "Predict ad click conversion", "converted", "classification"),
        ("manufacturing_defects.csv", "Analyze defect probability", "is_defective", "classification"),
        ("telecom_churn.csv", "Model user churn", "churn", "classification"),
        ("real_estate_prices.csv", "Predict house price", "price", "regression"),
        ("finance_credit_risk.csv", "Analyze credit default risk", "default", "classification"),
        ("education_scores.csv", "Predict student test scores", "score", "regression"),
        ("agriculture_yield.csv", "Model crop yield per acre", "yield", "regression"),
        ("insurance_claims.csv", "Predict claim amount", "claim_amount", "regression"),
        ("energy_consumption.csv", "Model kwH usage", "kwh", "regression"),
        ("ecommerce_returns.csv", "Predict product return probability", "returned", "classification"),
        ("logistics_fuel.csv", "Model fuel consumption", "fuel_gal", "regression"),
        ("gaming_retention.csv", "Predict player retention", "retained", "classification"),
    ]
    
    np.random.seed(42)
    for name, goal, target, type_ in specs:
        n = np.random.randint(500, 1500)
        df = pd.DataFrame({
            "feature_1": np.random.normal(0, 1, n),
            "feature_2": np.random.uniform(0, 100, n),
            "feature_3": np.random.randint(0, 5, n),
            "feature_4": np.random.exponential(1, n)
        })
        
        if type_ == "regression":
            df[target] = df["feature_1"] * 2.5 + df["feature_2"] * 0.1 - df["feature_3"] * 5 + np.random.normal(0, 2, n)
        else:
            # Logistic sigmoid logic
            z = df["feature_1"] * 1.5 - df["feature_2"] * 0.05 + df["feature_3"] * 2
            prob = 1 / (1 + np.exp(-z))
            df[target] = (prob > 0.5).astype(int)
            
        path = os.path.join(DATA_DIR, name)
        df.to_csv(path, index=False)
        datasets.append((name, df, goal))
        
    return datasets

# 2. Load 5 Real-World Datasets
def load_real_data():
    datasets = []
    
    # 1. California Housing
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    path = os.path.join(DATA_DIR, "california_housing.csv")
    df.to_csv(path, index=False)
    datasets.append(("california_housing.csv", df, "Predict median house value"))
    
    # 2. Iris
    data = load_iris(as_frame=True)
    df = data.frame
    path = os.path.join(DATA_DIR, "iris.csv")
    df.to_csv(path, index=False)
    datasets.append(("iris.csv", df, "Classify iris species"))
    
    # 3. Breast Cancer
    data = load_breast_cancer(as_frame=True)
    df = data.frame
    path = os.path.join(DATA_DIR, "breast_cancer.csv")
    df.to_csv(path, index=False)
    datasets.append(("breast_cancer.csv", df, "Detect malignant tumors"))
    
    # 4. Wine
    data = load_wine(as_frame=True)
    df = data.frame
    path = os.path.join(DATA_DIR, "wine.csv")
    df.to_csv(path, index=False)
    datasets.append(("wine.csv", df, "Classify wine cultivators"))
    
    # 5. Diabetes
    data = load_diabetes(as_frame=True)
    df = data.frame
    path = os.path.join(DATA_DIR, "diabetes.csv")
    df.to_csv(path, index=False)
    datasets.append(("diabetes.csv", df, "Predict disease progression"))
    
    return datasets

def run_evaluation():
    datasets = synthesize_data() + load_real_data()
    
    understanding_agent = DatasetUnderstandingAgent()
    quality_agent = DataQualityAgent()
    domain_agent = DomainDetectionAgent()
    planner_agent = WorkflowPlanningAgent()
    
    report_data = []
    
    for filename, df, user_goal in datasets:
        print(f"\n======================================")
        print(f"Evaluating Dataset: {filename}")
        
        # 1. Profile
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
        
        with open(plan_path, "w") as f:
            plan["status"] = "USER_APPROVED"
            json.dump(plan, f, indent=4)
            
        print(f"Goal: {user_goal} | Task: {plan.get('inferred_task')}")
            
        # 5. Execute
        final_state = execute_pipeline(filename, df)
        
        automl = final_state.get("automl_outputs", {})
        metrics = automl.get("metrics", {})
        agents_run = list(final_state.get("agent_status", {}).keys())
        
        print(f"Metrics: {metrics}")
            
        report_data.append({
            "dataset": filename,
            "domain": domain.get("primary_domain", "Unknown"),
            "health_score": quality.get("health_score", 0),
            "workflow_executed": agents_run,
            "automl_metrics": metrics
        })
        
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/scale_evaluation_report.json"))
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print(f"\nEvaluation Complete! Scaled Report saved to {report_path}")

if __name__ == "__main__":
    run_evaluation()
