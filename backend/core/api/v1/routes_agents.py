from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from core.services.agent_registry import agent_registry, AgentRecord

router = APIRouter(prefix="/agents", tags=["Agent Registry"])

class AgentRegisterSchema(BaseModel):
    name: str
    purpose: str
    capabilities: List[str]
    inputs: List[str]
    outputs: List[str]
    dependencies: List[str]
    exec_cost: float
    version: str = "1.0.0"

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_agents():
    """Returns a list of all registered autonomous agents and their health statuses."""
    return agent_registry.get_all()

@router.get("/{agent_id}", response_model=Dict[str, Any])
def get_agent(agent_id: str):
    """Retrieves specific details, dependencies, and execution telemetry for an agent."""
    agent = agent_registry.get_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found in registry")
    return agent

@router.post("/register", response_model=Dict[str, Any])
def register_agent(payload: AgentRegisterSchema):
    """Allows external or dynamically spawned agents to register their capabilities into the swarm."""
    record = AgentRecord(
        name=payload.name,
        purpose=payload.purpose,
        capabilities=payload.capabilities,
        inputs=payload.inputs,
        outputs=payload.outputs,
        dependencies=payload.dependencies,
        exec_cost=payload.exec_cost,
        version=payload.version
    )
    agent_registry.register(record)
    return {"message": f"Agent {payload.name} registered successfully", "id": record.id}
