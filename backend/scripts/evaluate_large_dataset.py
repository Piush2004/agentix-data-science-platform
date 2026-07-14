import os
import sys
import json
import pandas as pd
import urllib.request
import time

# Adjust paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.dataset_understanding import DatasetUnderstandingAgent
from app.agents.data_quality import DataQualityAgent
from app.agents.domain_detection import DomainDetectionAgent
from app.agents.workflow_planner import WorkflowPlanningAgent
from app.core.langgraph_engine import execute_pipeline

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/large_datasets"))
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_nyc_taxi_data():
    """
    Downloads the NYC Yellow Taxi trip data for Jan 2023 (parquet is ~50MB).
    Converts it to CSV (which will be >100MB) for Agentix processing.
    """
    parquet_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    parquet_path = os.path.join(DATA_DIR, "yellow_tripdata_2023-01.parquet")
    csv_path = os.path.join(DATA_DIR, "nyc_taxi_2023.csv")
    
    if not os.path.exists(csv_path):
        print(f"Downloading NYC Taxi Data (Parquet) from {parquet_url}...")
        urllib.request.urlretrieve(parquet_url, parquet_path)
        print("Download complete. Reading parquet and converting to CSV...")
        
        # Read the parquet. It has ~3 million rows. We'll sample 500,000 to keep it manageable but >20MB.
        # Wait, 500,000 rows of NYC taxi is ~40MB in CSV format.
        df = pd.read_parquet(parquet_path)
        df_sampled = df.sample(n=500000, random_state=42)
        
        # Clean up column names and some extreme outliers just so AutoML doesn't crash on inf
        df_sampled = df_sampled.dropna()
        
        print(f"Saving to CSV... Shape: {df_sampled.shape}")
        df_sampled.to_csv(csv_path, index=False)
        
        # Remove the parquet file to save space
        os.remove(parquet_path)
        print(f"CSV saved at {csv_path}. Size: {os.path.getsize(csv_path) / (1024*1024):.2f} MB")
    else:
        print(f"CSV already exists at {csv_path}. Size: {os.path.getsize(csv_path) / (1024*1024):.2f} MB")
        
    return csv_path

def run_large_dataset_evaluation():
    csv_path = fetch_nyc_taxi_data()
    filename = os.path.basename(csv_path)
    
    # We load the dataframe
    print("Loading dataframe into memory...")
    # Sample down to 50k for actual processing so it doesn't OOM during AutoML random forest
    # Wait, the user wants to test large datasets. We will pass the full 500k rows (40MB).
    # If RF OOMs, the error will be caught gracefully by Agentix.
    df = pd.read_csv(csv_path)
    
    # We want to predict fare_amount
    user_goal = "Predict the total fare amount based on trip metrics"
    
    understanding_agent = DatasetUnderstandingAgent()
    quality_agent = DataQualityAgent()
    domain_agent = DomainDetectionAgent()
    planner_agent = WorkflowPlanningAgent()
    
    print(f"\n======================================")
    print(f"Evaluating Large Dataset: {filename} ({os.path.getsize(csv_path)/(1024*1024):.2f} MB)")
    print(f"Goal: {user_goal}")
    print(f"======================================")
    
    start_time = time.time()
    
    # 1. Profile
    print("Running Understanding Agent...")
    profile_res = understanding_agent.analyze(df, filename)
    profile = profile_res.get("profile_data", profile_res.get("profile", {}))
    
    # 2. Quality
    print("Running Quality Agent...")
    quality = quality_agent.analyze(df, filename)["report_data"]
    
    # 3. Domain
    print("Running Domain Agent...")
    domain = domain_agent.analyze(df, filename).get("report_data", domain_agent.analyze(df, filename))
    
    # 4. Planning
    print("Running Workflow Planning Agent...")
    plan_res = planner_agent.generate_plan(filename, user_goal, profile, quality, domain)
    plan = plan_res["plan_data"]
    plan_path = plan_res["plan_path"]
    
    with open(plan_path, "w") as f:
        plan["status"] = "USER_APPROVED"
        json.dump(plan, f, indent=4)
        
    print(f"Generated Workflow: {plan['execution_order']}")
        
    # 5. Execute
    print("Dispatching to Orchestrator...")
    final_state = execute_pipeline(filename, df)
    
    automl = final_state.get("automl_outputs", {})
    metrics = automl.get("metrics", {})
    agents_run = list(final_state.get("agent_status", {}).keys())
    errors = final_state.get("errors", {})
    
    exec_time = time.time() - start_time
    
    print(f"\nExecution Complete in {exec_time:.2f} seconds.")
    print(f"Agents Executed: {agents_run}")
    print(f"AutoML Metrics: {metrics}")
    
    if errors:
        print(f"Errors Encountered: {errors}")
        
    # Save Report
    report_data = {
        "dataset": filename,
        "size_mb": os.path.getsize(csv_path)/(1024*1024),
        "rows": len(df),
        "columns": len(df.columns),
        "domain": domain.get("primary_domain", "Unknown"),
        "health_score": quality.get("health_score", 0),
        "workflow_executed": agents_run,
        "automl_metrics": metrics,
        "errors": errors,
        "execution_time_sec": exec_time
    }
    
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/large_dataset_evaluation_report.json"))
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print(f"\nReport saved to {report_path}")

if __name__ == "__main__":
    run_large_dataset_evaluation()
