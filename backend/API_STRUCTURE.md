# API Structure

The FastAPI routing layer has been modularized inside `core/api/v1/`.

## Routes
- `routes_agents.py` - AI agent configuration and monitoring.
- `routes_approval.py` - User-in-the-loop workflow approval endpoints.
- `routes_auth.py` - JWT and OAuth2 integration.
- `routes_data.py` - Dataset upload, EDA processing, and retrieval.
- `routes_orchestrator.py` - Webhook and internal orchestration endpoints.
- `routes_platform.py` - Global platform health and configuration.

All endpoints adhere strictly to the schema definitions in `core.schemas`. No business logic resides in these routes.
