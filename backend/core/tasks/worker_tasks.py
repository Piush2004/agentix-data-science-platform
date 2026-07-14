import os
import json
import time
from core.services.data_service import data_service
from core.services.platform_services import PlatformService
from core.engines.orchestration import WorkflowController, init_state
from core.redis_client import get_redis
import numpy as np

def clean_task(dataset_name: str):
    return PlatformService.clean(dataset_name)

def eda_task(dataset_name: str):
    return PlatformService.eda(dataset_name)

def predict_task(dataset_name: str, target_col: str = None):
    return PlatformService.predict(dataset_name, target_col)

def xai_task(dataset_name: str):
    return PlatformService.xai(dataset_name)

def reports_task(dataset_name: str):
    return PlatformService.reports(dataset_name)

def start_workflow_task(dataset_name: str, current_state: dict):
    PlatformService.current_state = current_state
    workflow = build_workflow()
    for s in workflow.stream(PlatformService.current_state):
        node_name = list(s.keys())[0]
        PlatformService.current_state.update(s[node_name])
        try:
            redis = get_redis()
            if redis:
                safe_state = {k: str(v) for k, v in PlatformService.current_state.items() if k not in ['raw_df', 'cleaned_df', 'engineered_df']}
                redis.setex('platform:current_state', 3600, json.dumps(safe_state))
        except:
            pass
        time.sleep(1.5)
    return {"status": "Workflow completed"}
