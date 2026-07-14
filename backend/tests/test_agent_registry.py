import pytest
from fastapi.testclient import TestClient
from core.api.main import app
from core.services.agent_registry import agent_registry

client = TestClient(app)

def test_agent_registry_seeding():
    agents = agent_registry.get_all()
    assert len(agents) == 11
    
    metadata_agent = [a for a in agents if a["id"] == "metadata_agent"][0]
    assert metadata_agent["name"] == "Metadata Agent"
    assert "Schema Detection" in metadata_agent["capabilities"]
    assert metadata_agent["status"] == "Idle"

def test_api_get_all_agents():
    response = client.get("/api/v1/agents/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 11

def test_api_get_single_agent():
    response = client.get("/api/v1/agents/eda_agent")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "EDA Agent"
    assert data["exec_cost"] == 0.1

def test_api_register_agent():
    payload = {
        "name": "Custom Marketing Agent",
        "purpose": "Calculates LTV",
        "capabilities": ["LTV Calculation", "Churn Prediction"],
        "inputs": ["dataframe"],
        "outputs": ["ltv_report"],
        "dependencies": ["Cleaning Agent"],
        "exec_cost": 2.5
    }
    response = client.post("/api/v1/agents/register", json=payload)
    assert response.status_code == 200
    assert "Custom Marketing Agent registered successfully" in response.json()["message"]
    
    # Verify via registry
    custom = agent_registry.get_by_id("custom_marketing_agent")
    assert custom["purpose"] == "Calculates LTV"
