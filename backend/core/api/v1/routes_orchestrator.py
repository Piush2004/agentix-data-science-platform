from fastapi import APIRouter
from core.schemas.orchestrator_schemas import OrchestratorResponse
from core.langgraph_engine import execute_pipeline
from core.services.data_service import data_service

router = APIRouter()

@router.post("/execute")
def execute_dag(dataset_name: str):
    df = data_service.get_dataset(dataset_name)
    if df is None:
        return {"status": "error", "nodes_executed": 0, "errors": ["Dataset not found"], "agent_status": {}}
        
    result = execute_pipeline(dataset_name, df)
    
    # Clean up DataFrames before returning JSON
    if "raw_df" in result: del result["raw_df"]
    if "cleaned_df" in result: del result["cleaned_df"]
    if "engineered_df" in result: del result["engineered_df"]
    
    return {
        "status": "success",
        "nodes_executed": len(result.get("agent_status", {})),
        "errors": result.get("errors", []),
        "agent_status": result.get("agent_status", {}),
        "profiling": result.get("profiling_outputs", {}),
        "eda": result.get("eda_outputs", {}),
        "automl": result.get("automl_outputs", {}),
        "shap": result.get("shap_outputs", {}),
        "insights": result.get("insights", ""),
        "recommendations": result.get("recommendations", ""),
        "report": result.get("report", "")
    }
