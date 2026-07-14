import pytest
from fastapi.testclient import TestClient
from core.api.main import app
import json
import os

client = TestClient(app)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")

@pytest.fixture(autouse=True)
def setup_mock_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Mock Quality Report
    with open(os.path.join(DATA_DIR, "testdata_quality_report.json"), "w") as f:
        json.dump({"health_score": 85, "classification": "Good"}, f)
        
    # Mock Recommendations
    with open(os.path.join(DATA_DIR, "testdata_recommendations.json"), "w") as f:
        json.dump({
            "dataset_name": "testdata.csv",
            "header": "Mock header",
            "recommendations": [{"action": "Clean Data"}],
            "total_estimated_time_sec": 0.5
        }, f)
        
    # Mock Workflow Plan
    with open(os.path.join(DATA_DIR, "testdata_workflow_plan.json"), "w") as f:
        json.dump({
            "execution_order": ["Cleaning Agent", "EDA Agent"],
            "status": "PENDING"
        }, f)
        
    yield
    
    # Cleanup
    for f in ["testdata_quality_report.json", "testdata_recommendations.json", "testdata_workflow_plan.json"]:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            os.remove(path)

def test_get_pending_approval():
    response = client.get("/api/v1/approval/pending/testdata.csv")
    assert response.status_code == 200
    data = response.json()
    
    assert data["dataset_name"] == "testdata.csv"
    assert data["health_score"] == 85
    assert len(data["recommendations"]["recommendations"]) == 1

def test_submit_approval():
    response = client.post("/api/v1/approval/submit", json={
        "dataset_name": "testdata.csv",
        "approved_agents": ["Cleaning Agent"] # Dropped EDA
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["new_plan"]["status"] == "USER_APPROVED"
    assert data["new_plan"]["execution_order"] == ["Cleaning Agent"]
