import requests
import time
import json
import os

BASE_URL = "http://localhost:8000/api/v1"

endpoints_to_test = [
    # Agents
    ("GET", "/agents/"),
    ("GET", "/agents/dataset_understanding"),
    ("POST", "/agents/register", {"name": "Test Agent", "role": "Tester", "endpoint": "http://localhost:8001"}),
    
    # Approval
    ("GET", "/approval/pending/test_dataset"),
    ("POST", "/approval/submit", {"dataset_name": "test_dataset", "status": "APPROVED", "modifications": []}),
    
    # Data
    ("GET", "/data/history"),
    ("GET", "/data/test_dataset/preview"),
    
    # Orchestrator
    ("POST", "/orchestrator/execute", {"dataset_name": "test_dataset", "workflow_plan": {"nodes": []}}),
    
    # Platform
    ("POST", "/platform/profile", {"dataset_name": "test_dataset"}),
    ("GET", "/platform/eda?dataset_name=test_dataset"),
    ("GET", "/platform/xai?dataset_name=test_dataset"),
    ("GET", "/platform/mlops"),
    ("GET", "/platform/dashboard-metrics"),
    ("GET", "/platform/system-health"),
    ("GET", "/platform/model-registry"),
    ("GET", "/platform/experiment-runs"),
    ("GET", "/platform/dataset-versions?dataset_name=test_dataset"),
    ("GET", "/platform/health"),
    ("GET", "/platform/dataset-summary"),
    ("GET", "/platform/model-metrics"),
    ("GET", "/platform/recent-activity"),
    ("GET", "/platform/active-agents"),
    ("GET", "/platform/storage"),
    
    # Platform (Requires existing dataset to not 400, but we can see if it 400s correctly)
    ("POST", "/platform/clean", {"dataset_name": "test_dataset"}),
    ("POST", "/platform/predict", {"dataset_name": "test_dataset", "target_column": "target"}),
    ("POST", "/platform/chat", {"query": "Hello", "dataset_name": "test_dataset"})
]

results = []

for method, path, *body in endpoints_to_test:
    url = f"{BASE_URL}{path}"
    payload = body[0] if body else None
    
    start = time.time()
    try:
        if method == "GET":
            res = requests.get(url, timeout=5)
        else:
            res = requests.post(url, json=payload, timeout=5)
            
        latency = (time.time() - start) * 1000
        
        try:
            resp_data = res.json()
        except:
            resp_data = res.text[:200]
            
        results.append({
            "method": method,
            "endpoint": path,
            "status_code": res.status_code,
            "latency_ms": round(latency, 2),
            "response_snippet": str(resp_data)[:100]
        })
    except Exception as e:
        results.append({
            "method": method,
            "endpoint": path,
            "status_code": "ERROR",
            "latency_ms": 0,
            "response_snippet": str(e)
        })

# Output to json
with open(os.path.join(os.path.dirname(__file__), "api_audit_results.json"), "w") as f:
    json.dump(results, f, indent=4)
    
print("API Audit Completed")
