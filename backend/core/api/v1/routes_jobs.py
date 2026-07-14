from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from core.jobs.service import job_service
from core.services.platform_services import platform_service

router = APIRouter()

class JobSubmitRequest(BaseModel):
    task_type: str
    dataset_name: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

@router.post("/submit")
def submit_job(req: JobSubmitRequest):
    """
    Submits a background job for long-running AI workflows.
    Returns a job_id immediately.
    """
    task_map = {
        "clean": platform_service.clean,
        "eda": platform_service.eda,
        "feature_engineering": platform_service.feature_engineering,
        "predict": platform_service.predict,
        "reports": platform_service.reports,
        "chat": platform_service.chat
    }

    if req.task_type not in task_map:
        raise HTTPException(status_code=400, detail="Invalid task_type")

    func = task_map[req.task_type]
    
    # Extract specific positional arguments expected by the platform_services methods
    args = []
    if req.task_type == "predict":
        args = [req.dataset_name, req.parameters.get("target_column") if req.parameters else None]
    elif req.task_type == "chat":
        args = [req.parameters.get("query") if req.parameters else "", req.dataset_name]
    else:
        args = [req.dataset_name]

    job_id = job_service.submit(
        task_type=req.task_type,
        func=func,
        dataset_name=req.dataset_name,
        parameters=req.parameters,
        *args
    )

    return {"status": "success", "job_id": job_id}

@router.get("/status/{job_id}")
def get_job_status(job_id: str):
    """
    Retrieves the status and potential result of a background job.
    """
    status_data = job_service.get_status(job_id)
    if "error" in status_data and status_data["error"] == "Job not found":
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {"status": "success", "data": status_data}
