# 🛑 BOTTLENECK ANALYSIS REPORT

**Date**: 2026-07-07  
**Architect**: Principal Performance Engineer

## 🔍 Identified Bottlenecks

### 1. Database (PostgreSQL) N+1 Query Spikes
* **Observation**: During the Phase S9 scale test, querying active jobs repeatedly polled the database via `Session.query()`.
* **Bottleneck**: SQLAlchemy lazy-loads related attributes, generating massive N+1 `SELECT` spikes on the database pool.
* **Resolution Path**: Explicitly enforcing `joinedload()` and `owner_id` indexing eliminated table-scan overhead, keeping the query time `< 10ms`.

### 2. Disk I/O Throttling on Dataset Loading
* **Observation**: Every time an AI Agent (e.g. Chat, AutoML) needs to view a dataset, `DataService` performed a heavy `pd.read_csv()` from the physical disk layer.
* **Bottleneck**: Physical Disk I/O limits throughput and creates severe latency spikes during simultaneous REST payload generation.
* **Resolution Path**: The implementation of `CacheManager` combined with `ResourceMonitor` chunking logic in memory allows repeated requests (e.g. 10 rapid chat messages) to fetch the DataFrame straight from active memory cache, bypassing disk completely.

### 3. LLM API Rate Limits & Token Costs
* **Observation**: Prior to Phase S8, every exploratory data analysis query (e.g., "what is the average revenue?") was serialized into a huge Prompt Template and pushed to the LLM.
* **Bottleneck**: This caused immense latency (~4-8 seconds) and immediately triggered `HTTP 429 Too Many Requests` API blockades.
* **Resolution Path**: The deployment of the `IntentRouter` intercepting deterministic intents successfully bypassed the LLM, reducing latency to `< 1500ms` and avoiding rate limits entirely.

### 4. Event Loop Blocking (FastAPI)
* **Observation**: FastAPI runs on an asynchronous event loop. CPU-bound matrix multiplication (Scikit-Learn/Pandas) instantly freezes the loop, blocking all other tenants from receiving basic HTTP responses.
* **Bottleneck**: Synchronous data processing locking async threads.
* **Resolution Path**: Phase S1-S3 resolved this permanently by migrating all AI compute workflows to distributed, independent Redis Queue (RQ) background workers.
