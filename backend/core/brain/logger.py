import logging
import os

class BrainLogger:
    """Manages centralized logging for all Brain decisions and dispatches."""
    
    def __init__(self):
        log_path = os.path.join(os.path.dirname(__file__), "../../../data/brain.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("AgentixBrain")
        
    def log_decision(self, workspace_id: str, action: str, details: str):
        self.logger.info(f"[Workspace: {workspace_id}] Action: {action} | Details: {details}")

brain_logger = BrainLogger()
