# 🔌 API Documentation

Agentix exposes a RESTful API powered by FastAPI.

## Authentication
*(Currently disabled in local development. Future support for JWT & OAuth2).*

---

## 1. Upload Dataset
`POST /api/v1/datasets/upload`

**Request:**
Multipart form-data containing the file (`.csv`, `.json`).

**Response:**
```json
{
  "dataset_id": "uuid-1234",
  "metadata": {
    "rows": 1000,
    "columns": ["age", "income"]
  }
}
```

---

## 2. Data Cleaning
`POST /api/v1/workflows/clean`

**Request:**
```json
{
  "dataset_id": "uuid-1234",
  "strategy": "impute_mean"
}
```

**Response:**
```json
{
  "status": "success",
  "execution_time_ms": 450,
  "cleaned_dataset_url": "/downloads/cleaned_uuid-1234.csv"
}
```

---

## 3. AutoML Processing
`POST /api/v1/workflows/automl`

**Request:**
```json
{
  "dataset_id": "uuid-1234",
  "target_column": "income",
  "task_type": "regression"
}
```

**Response:**
```json
{
  "status": "success",
  "model_accuracy": 0.94,
  "artifacts": ["model.pkl"]
}
```

---

*(More endpoints for EDA, Explainability, and AI Chat available in OpenAPI schema at `/docs`)*.
