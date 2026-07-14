# Project Context & Transition Blueprint

Use this context file to easily resume or migrate work on the **Agentix Data Intelligence Platform** in a new chat.

---

## 1. System Architecture & Boundaries

The application is built on a split architecture:
- **Frontend**: Next.js 15 app router on port `3000` backed by Prisma SQLite for user authentication, settings, RBAC workspaces, session tracking, and recent activity logs.
- **Backend**: FastAPI on port `8000` handling memory caching (via Pandas data frames in `memory_store`), dataset versioning, Exploratory Data Analysis, scikit-learn AutoML model training, SHAP feature importance calculation, and local LLM orchestration (LangGraph + Ollama).

---

## 2. Master API Integration Status

All pages communicate correctly with live APIs. Every mock response has been replaced with live calculations:

- **Dashboard**: Mapped to [route.ts](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/frontend/src/app/api/dashboard/route.ts) on Next.js, proxying metrics from backend `/platform/dashboard-metrics` and system stats from `/platform/system-health`.
- **Upload (Ingestion)**: Handles Parquet, CSV, Excel, and JSON uploads. Saves files locally to disk under [backend/data](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/data) and maintains metadata version histories under [backend/data/versions](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/data/versions).
- **AutoML**: Integrates [automl/page.tsx](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/frontend/src/app/%28app%29/models/automl/page.tsx) with the `/predict` route to fit scikit-learn regressors (Random Forest, Gradient Boosting, Linear Regression) and output live accuracy leaderboards.
- **Explainability (XAI)**: Estimates directional feature contributions mathematically for the first sample in `X_test` and constructs local SHAP waterfall graphs.
- **AI Analyst**: Integrates Ollama chat. If Ollama is offline, it falls back to a live statistical heuristic engine that parses the active dataset to return real correlation pairs, model accuracies, or recommendations.
- **Workflow**: Manages LangGraph pipeline executions. Implemented real prediction and explainability nodes to train models and compute feature importances dynamically.

---

## 3. Key Services Overview

### A. Data Service
File: [data_service.py](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/app/services/data_service.py)
- Manages dataset memory caching, version registration, rollback requests, and local disk persistence. It parses file extensions to read and write formats (CSV, Parquet, Excel, JSON) natively.

### B. Platform Service
File: [platform_services.py](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/app/services/platform_services.py)
- Orchestrates AutoML sweeps, SHAP value derivations, MLOps metrics aggregation, and recent activity logs.

### C. Dataset Processor Service (New)
File: [dataset_processor.py](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/app/services/dataset_processor.py)
- A newly built, format-aware processing utility that exposes the following:
  - `load(dataset_name)`: Fetches data frames from disk.
  - `validate(df)`: Validates format integrity, null density, and checks duplicates.
  - `detect_schema(df)`: Maps columns to numeric, categorical, boolean, or datetime schemas.
  - `generate_metadata(df, name)`: Aggregates row/column counts and file bytes.
  - `generate_statistics(df)`: Calculates skewness, mean, std, quantiles, and category counts.
  - `generate_profile(df, name)`: Combines all parameters to build a comprehensive dashboard index.
  - `store_outputs(name, profile)`: Persists JSON outputs locally under [backend/data/profiles/](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/data/profiles).

---

## 4. Verification Suites

You can test compilation and API schemas by executing these scripts:
```bash
# Verify backend routing and Next.js aggregator status:
python D:\Projects\Agentic Data Intelligence Platform\backend\scratch\verify_backend_endpoints.py

# Verify dedicated platform metrics (MLOps, active agents, storage health):
python D:\Projects\Agentic Data Intelligence Platform\backend\scratch\verify_dedicated_endpoints.py

# Verify format-aware dataset uploads and disk persistence:
python D:\Projects\Agentic Data Intelligence Platform\backend\scratch\verify_uploads_disk_persist.py
```

---

## 5. Next Steps for New Chat
1. **Processor Integration**: Substitute standard dataframe profiling hooks in [platform_services.py](file:///D:/Projects/Agentic%20Data%20Intelligence%20Platform/backend/app/services/platform_services.py#L39) and LangGraph workflow nodes with the newly defined `dataset_processor` class.
2. **Dashboard UI Binding**: Create frontend panels to parse and render the generated profile JSON files (`/data/profiles/{name}_profile.json`).
