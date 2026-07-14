import asyncio
from core.engines.orchestration import WorkflowController
from core.brain.brain import AgentixBrain

workflow_controller = WorkflowController()
brain = None  # Instantiated later via DI

async def execute_pipeline(dataset_name: str, goal: str, user_id: str):
    # API -> WorkflowController -> AgentixBrain -> Cognitive Loop
    await brain.process_workflow_request(dataset_name, goal, user_id)
    return {"status": "success", "message": "Pipeline execution started via Brain"}
