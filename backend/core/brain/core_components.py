import logging
from typing import Any, Dict, List
from datetime import datetime

class BrainState:
    """Manages the current state machine of the Brain execution."""
    def __init__(self):
        self.current_phase = "IDLE"
        self.history: List[str] = []

    def transition(self, new_phase: str):
        self.history.append(self.current_phase)
        self.current_phase = new_phase

class BrainContext:
    """Holds the current execution context."""
    def __init__(self, raw_input: Dict[str, Any]):
        self.raw_input = raw_input
        self.metadata: Dict[str, Any] = {}
        self.session_id: str = raw_input.get("session_id", "default_session")

class BrainMemory:
    """Short-term operational memory during the Brain's think cycle."""
    def __init__(self):
        self._memory_store: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._memory_store[key] = value

    def get(self, key: str) -> Any:
        return self._memory_store.get(key)

class BrainEvents:
    """Event bus for internal Brain Pub/Sub."""
    def __init__(self):
        self._listeners: Dict[str, List] = {}

    def subscribe(self, event_type: str, callback: Any):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def emit(self, event_type: str, payload: Any):
        for callback in self._listeners.get(event_type, []):
            callback(payload)

class BrainLogger:
    """Cognitive logger dedicated to Brain thought processes."""
    def __init__(self):
        self.logger = logging.getLogger("Agentix.Brain")
        self.logger.setLevel(logging.INFO)

    def log_thought(self, phase: str, thought: str):
        self.logger.info(f"[{phase}] - {thought}")

class BrainController:
    """Orchestrates the internal execution loop of the Cognitive Brain."""
    def __init__(self, state: BrainState, context: BrainContext, memory: BrainMemory, events: BrainEvents, logger: BrainLogger):
        self.state = state
        self.context = context
        self.memory = memory
        self.events = events
        self.logger = logger
