from fastapi import APIRouter, HTTPException
from typing import Optional
from core.schemas.api_schemas import DatasetRequest, ChatRequest, BaseResponse, PredictRequest
from core.services.platform_services import platform_service
import logging

logger = logging.getLogger("agentix_platform")
router = APIRouter()

from rq import Queue
from core.redis_client import get_redis

def get_rq_queue():
    redis_conn = get_redis()
    import fakeredis
    is_sync = isinstance(redis_conn, fakeredis.FakeStrictRedis)
    return Queue(connection=redis_conn, is_async=not is_sync)

import asyncio

async def handle_request(func, *args):
    try:
        loop = asyncio.get_event_loop()
        # Offloading the CPU-bound AI workflow to the ThreadPoolExecutor 
        # to remove all blocking execution from the FastAPI request thread!
        data = await loop.run_in_executor(None, func, *args)
        logger.info(f"Successfully executed {func.__name__}")
        return BaseResponse(status="success", message="OK", data=data)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/profile", response_model=BaseResponse)
async def profile_endpoint(req: DatasetRequest): return await handle_request(platform_service.profile, req.dataset_name)

@router.post("/clean", response_model=BaseResponse)
async def clean_endpoint(req: DatasetRequest): 
    return await handle_request(platform_service.clean, req.dataset_name)

@router.post("/feature-engineering", response_model=BaseResponse)
async def fe_endpoint(req: DatasetRequest): 
    return await handle_request(platform_service.feature_engineering, req.dataset_name)

@router.get("/eda", response_model=BaseResponse)
async def eda_endpoint(dataset_name: str): 
    return await handle_request(platform_service.eda, dataset_name)

@router.post("/predict", response_model=BaseResponse)
async def predict_endpoint(req: PredictRequest): 
    return await handle_request(platform_service.predict, req.dataset_name, req.target_column)

@router.get("/xai", response_model=BaseResponse)
async def xai_endpoint(dataset_name: str): 
    return await handle_request(platform_service.xai, dataset_name)

@router.get("/insights", response_model=BaseResponse)
async def insights_endpoint(dataset_name: str): return await handle_request(platform_service.insights, dataset_name)

@router.get("/recommendations", response_model=BaseResponse)
async def recommendations_endpoint(dataset_name: str): return await handle_request(platform_service.recommendations, dataset_name)

@router.get("/reports", response_model=BaseResponse)
async def reports_endpoint(dataset_name: str): 
    return await handle_request(platform_service.reports, dataset_name)

@router.post("/chat", response_model=BaseResponse)
async def chat_endpoint(req: ChatRequest): return await handle_request(platform_service.chat, req.query, req.dataset_name)

@router.get("/mlops", response_model=BaseResponse)
async def mlops_endpoint(): return await handle_request(platform_service.mlops)

@router.post("/start-workflow", response_model=BaseResponse)
async def start_workflow_endpoint(req: DatasetRequest): return await handle_request(platform_service.start_workflow, req.dataset_name)

@router.get("/workflow-status", response_model=BaseResponse)
async def workflow_status():
    return await handle_request(platform_service.workflow_status)

@router.get("/dashboard-metrics", response_model=BaseResponse)
async def dashboard_metrics_endpoint(): return await handle_request(platform_service.dashboard_metrics)

@router.post("/demo/load", response_model=BaseResponse)
async def load_demo_endpoint(dataset_type: str):
    return await handle_request(platform_service.load_demo, dataset_type)

@router.get("/system-health", response_model=BaseResponse)
def system_health_endpoint(): return await handle_request(platform_service.system_health)

@router.get("/model-registry", response_model=BaseResponse)
def model_registry_endpoint(): return await handle_request(platform_service.model_registry)

@router.get("/experiment-runs", response_model=BaseResponse)
def experiment_runs_endpoint(dataset_name: Optional[str] = None): return await handle_request(platform_service.experiment_runs, dataset_name)

@router.get("/dataset-versions", response_model=BaseResponse)
def dataset_versions_endpoint(dataset_name: str): return await handle_request(platform_service.dataset_versions, dataset_name)

@router.post("/dataset-versions/rollback", response_model=BaseResponse)
def rollback_dataset_version_endpoint(req: DatasetRequest, version: int): return await handle_request(platform_service.rollback_dataset_version, req.dataset_name, version)

@router.get("/health", response_model=BaseResponse)
def health_endpoint(): return await handle_request(platform_service.health)

@router.get("/dataset-summary", response_model=BaseResponse)
def dataset_summary_endpoint(): return await handle_request(platform_service.dataset_summary)

@router.get("/model-metrics", response_model=BaseResponse)
def model_metrics_endpoint(): return await handle_request(platform_service.model_metrics)

@router.get("/recent-activity", response_model=BaseResponse)
def recent_activity_endpoint(): return await handle_request(platform_service.recent_activity)

@router.get("/active-agents", response_model=BaseResponse)
def active_agents_endpoint(): return await handle_request(platform_service.active_agents)

@router.get("/storage", response_model=BaseResponse)
def storage_endpoint(): return await handle_request(platform_service.storage)
