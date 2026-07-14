from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../../../data")

class ModifiedPlanRequest(BaseModel):
    dataset_name: str
    approved_agents: List[str]

@router.get("/pending/{dataset_name}")
async def get_pending_approval(dataset_name: str):
    """Fetches the generated workflow plan, recommendations, and quality score for user approval."""
    base_name = dataset_name.split(".")[0]
    rec_path = os.path.join(DATA_DIR, f"{base_name}_recommendations.json")
    quality_path = os.path.join(DATA_DIR, f"{base_name}_quality_report.json")
    
    if not os.path.exists(rec_path):
        raise HTTPException(status_code=404, detail="Recommendations not found. Run workflow planner first.")
        
    with open(rec_path, "r") as f:
        recs = json.load(f)
        
    quality = {}
    if os.path.exists(quality_path):
        with open(quality_path, "r") as f:
            quality = json.load(f)
            
    return {
        "dataset_name": dataset_name,
        "recommendations": recs,
        "health_score": quality.get("health_score", "N/A"),
        "classification": quality.get("classification", "Unknown")
    }

@router.post("/submit")
async def submit_approval(request: ModifiedPlanRequest):
    """Overrides the generated workflow plan with the user's explicit approvals and modifications."""
    base_name = request.dataset_name.split(".")[0]
    plan_path = os.path.join(DATA_DIR, f"{base_name}_workflow_plan.json")
    
    if not os.path.exists(plan_path):
        raise HTTPException(status_code=404, detail="Workflow plan not found.")
        
    with open(plan_path, "r") as f:
        plan = json.load(f)
        
    plan["execution_order"] = request.approved_agents
    plan["status"] = "USER_APPROVED"
    
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=4)
        
    return {"message": "Plan updated and approved successfully.", "new_plan": plan}
