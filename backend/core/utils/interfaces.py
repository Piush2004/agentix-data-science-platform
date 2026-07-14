from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IRepository(ABC):
    """Base interface for all Repositories."""
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Any]:
        pass
        
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        pass
        
    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Any:
        pass
        
    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

class IEngine(ABC):
    """Base interface for all Execution Engines."""
    
    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the core processing logic of the engine."""
        pass

class IAgent(ABC):
    """Base interface for specialized Agents."""
    
    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Performs cognitive reasoning based on the provided context."""
        pass

class IService(ABC):
    """Base interface for Business Logic Services."""
    
    @abstractmethod
    def handle_request(self, request_dto: Any) -> Any:
        """Processes an incoming API request via business rules."""
        pass
