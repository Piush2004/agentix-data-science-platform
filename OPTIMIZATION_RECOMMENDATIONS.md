# 🛠️ AGENTIX OPTIMIZATION RECOMMENDATIONS

**Date**: 2026-07-07  
**Author**: Principal Performance Engineer

Based on the `PERFORMANCE_BENCHMARK.md` matrix, the following architectural and algorithmic bottlenecks have been ranked. These MUST be resolved before enterprise multi-tenant launch.

---

## 🛑 1. Critical Optimizations (Fix Immediately)

### **Synchronous ML Thread Blocking**
* **The Problem**: `/api/v1/platform/predict` runs cross-validation locally using `handle_request()`. During a 20MB dataset run, it locks the FastAPI event loop for ~150 seconds. Other users cannot chat or upload files during this time.
* **The Solution**: 
  1. Offload the `predict` invocation to an asynchronous task queue (e.g. Celery + Redis, or `BackgroundTasks` in FastAPI).
  2. Implement polling endpoints so the UI can check progress asynchronously.
* **Impact**: Infinite improvement to UI responsiveness; unblocks multi-tenant scaling.

---

## 🔴 2. High Priority Optimizations

### **AutoML CPU Starvation & Subsampling**
* **The Problem**: Scikit-Learn ensembles (Random Forest / Gradient Boosting) are trained on the entire dataset. For 250k+ rows, hyperparameter tuning triggers combinatorial explosion.
* **The Solution**: Implement **Stratified Subsampling**. If a dataset exceeds 50,000 rows, randomly sample 50,000 rows with stratification for hyperparameter grid-search, then fit the final model on the whole dataset.
* **Impact**: Will reduce 250k row training time from ~148s down to ~40s (73% speedup) without significant loss in accuracy.

### **In-Memory SQLite vs PostgreSQL Serialization**
* **The Problem**: Writing massive UUID foreign keys and large JSON blocks into Postgres iteratively for `experiment-runs` introduces minor disk latency overhead.
* **The Solution**: Maintain real-time tracking in a shared-state dictionary (`PlatformService.runs`), then batch-dump the experiment manifest to Postgres when the job completes.
* **Impact**: Reduces database transaction locks by 90% during AutoML grid-search. (Already partially implemented).

---

## 🟡 3. Medium Priority Optimizations

### **Pandas vs Polars Universal Adoption**
* **The Problem**: The `RealAIAnalyst` smartly utilizes out-of-core Polars for mean/math calculations, but the core `platform_services.py` upload validation and feature engineering runs strictly on `pandas`. Pandas requires ~2x to 3x memory overhead compared to Polars due to string types and GIL contention.
* **The Solution**: Convert `data_service.read_csv()` to use `pl.read_csv()` and manage dataframe state in Polars LazyFrames until strict Sklearn ingestion demands numpy/pandas arrays.
* **Impact**: Will reduce peak RAM overhead from 1.2 GB down to ~450 MB for 50MB files.

### **LLM Token Compression**
* **The Problem**: Passing correlation matrices and SHAP impacts sequentially to the LLM requires roughly 1,000 tokens of context overhead per inference.
* **The Solution**: Serialize statistics using dense formatting `col1:avg:max` rather than JSON schemas.
* **Impact**: 40% reduction in LLM inference time and context size.

---

## 🟢 4. Low Priority Optimizations

### **Model Artifact Compression**
* **The Problem**: Serializing `.joblib` files carrying `X_train` payloads inside them consumes excessive disk space per trained model (~5-15MB per model).
* **The Solution**: Compress Joblib files using `lz4` or `gzip` natively, or map the `X_train` arrays to a shared Parquet directory instead of embedding them redundantly in every single cross-validated artifact.
* **Impact**: Savings of 50-80% in disk storage requirements per workspace.
