# Backend Architecture

The backend of Agentix follows a Domain-Driven Design (DDD) architecture centered around the Agentix Cognitive Brain.

## Directory Structure
- `backend/core/api/` - FastAPI controllers and routes. Thin wrappers around services.
- `backend/core/services/` - Business logic and use case coordination.
- `backend/core/repositories/` - Data access layer. All SQL alchemy operations are isolated here.
- `backend/core/brain/` - The Cognitive Loop (Perception, Understanding, Deliberation, Reasoning, Planning, Decision, Execution, Learning).
- `backend/core/memory/` - Episodic and Procedural memory interfaces and implementations.
- `backend/core/engines/` - Execution engines and orchestration controllers.
- `backend/core/agents/` - Specialized LangGraph agents.
- `backend/core/workflows/` - Isolated, executable workflow DAGs.
- `backend/core/models/` - SQLAlchemy models.
- `backend/core/schemas/` - Pydantic schemas for DTOs.
- `backend/core/auth/` - Authentication and authorization.

## Execution Flow
1. Client makes HTTP request to `core/api/v1/routes_*.py`
2. Route delegates to `core/services/*_service.py`
3. Service calls `core/repositories/*_repository.py` for state
4. Service delegates heavy AI tasks to `core/engines/orchestration.py` -> `AgentixBrain`
5. `AgentixBrain` triggers the cognitive loop and accesses `core/memory/`.
