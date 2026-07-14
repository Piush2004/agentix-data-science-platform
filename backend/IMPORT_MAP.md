# Import Map

All legacy imports from `app.*` have been strictly remapped to `core.*`.

- `app.api.*` -> `core.api.*`
- `app.services.*` -> `core.services.*`
- `app.db.*` -> `core.repositories.*`
- `app.models.*` -> `core.models.*`
- `app.schemas.*` -> `core.schemas.*`
- `app.core.*` -> `core.*`
- `app.tasks.*` -> `core.tasks.*`

## Deprecated Global Modules
- `orchestrator` -> Deprecated. Use `core.engines.orchestration.WorkflowController`.
- `ai_service` -> Deprecated. Use `core.ai_service.OllamaService` (internal reference only).
