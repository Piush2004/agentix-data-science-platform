import pytest
import os
import json
import asyncio
from core.services.decision_engine import DecisionIntelligenceEngine

@pytest.fixture(autouse=True)
def setup_mock_data():
    DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Unapproved Plan
    with open(os.path.join(DATA_DIR, "blocked_workflow_plan.json"), "w") as f:
        json.dump({"execution_order": ["Cleaning Agent"], "status": "PENDING"}, f)
        
    # Approved Plan
    with open(os.path.join(DATA_DIR, "approved_workflow_plan.json"), "w") as f:
        json.dump({
            "execution_order": ["AutoML Agent", "Cleaning Agent", "Feature Engineering Agent"],
            "status": "USER_APPROVED"
        }, f)
        
    # Mock Cached File for Cleaning Agent
    with open(os.path.join(DATA_DIR, "approved_cleaned.csv"), "w") as f:
        f.write("id,value\n1,100")
        
    yield
    
    # Cleanup
    for f in ["blocked_workflow_plan.json", "approved_workflow_plan.json", "approved_cleaned.csv", "execution_logs.json"]:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            os.remove(path)

def test_blocked_execution():
    engine = DecisionIntelligenceEngine()
    res = asyncio.run(engine.execute_approved_plan("blocked.csv"))
    assert res["status"] == "BLOCKED"

def test_approved_execution():
    engine = DecisionIntelligenceEngine()
    res = asyncio.run(engine.execute_approved_plan("approved.csv"))
    
    assert res["status"] == "SUCCESS"
    
    # Check DAG Sorting (Cleaning -> Feature Engineering -> AutoML)
    assert res["optimized_dag"] == ["Cleaning Agent", "Feature Engineering Agent", "AutoML Agent"]
    
    # Check Cache Hit (Cleaning Agent should be SKIPPED)
    trace = res["execution_trace"]
    assert trace[0]["agent"] == "Cleaning Agent"
    assert trace[0]["status"] == "SKIPPED_CACHE_HIT"
    
    # Check Execution (AutoML should be COMPLETED)
    assert trace[2]["agent"] == "AutoML Agent"
    assert trace[2]["status"] == "COMPLETED"
