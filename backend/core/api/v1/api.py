from fastapi import APIRouter, Depends
from core.auth import set_user_context
from core.api.v1 import routes_data, routes_orchestrator, routes_platform, routes_agents, routes_approval, routes_auth

api_router = APIRouter()
api_router.include_router(routes_data.router, prefix="/dataset", tags=["Dataset"], dependencies=[Depends(set_user_context)])
api_router.include_router(routes_orchestrator.router, prefix="/orchestrator", tags=["Orchestration"], dependencies=[Depends(set_user_context)])
api_router.include_router(routes_platform.router, prefix="/platform", tags=["Platform Capabilities"], dependencies=[Depends(set_user_context)])
api_router.include_router(routes_agents.router, dependencies=[Depends(set_user_context)])
api_router.include_router(routes_approval.router, prefix="/approval", tags=["User Approval"], dependencies=[Depends(set_user_context)])
api_router.include_router(routes_auth.router, prefix="/auth", tags=["Authentication"])
from core.api.v1 import routes_system
from core.api.v1 import routes_jobs
api_router.include_router(routes_system.router, prefix="/system", tags=["System"])
api_router.include_router(routes_jobs.router, prefix="/jobs", tags=["Jobs"], dependencies=[Depends(set_user_context)])
