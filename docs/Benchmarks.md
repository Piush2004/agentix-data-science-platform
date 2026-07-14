# 📊 Benchmarks

Agentix focuses heavily on execution speed and minimizing LLM latency.

## Performance vs Traditional Chatbots
Traditional AI workflows rely heavily on iterative ReAct (Reason + Act) loops via LLMs, resulting in massive latency. Agentix replaces repetitive LLM calls with deterministic Strategy execution.

### Latency
- **First-run Workflow**: ~15 seconds (Relies on full Deliberation and LLM routing).
- **Strategy-Recall Workflow**: ~0.8 seconds (Bypasses LLM, executes deterministic python engines).

### Memory
- Episodic Memory footprint is negligible due to structural fingerprinting (no raw data storage).
- Procedural Memory utilizes O(1) Redis lookups.

### Scalability
The FastAPI backend is fully stateless. It can scale horizontally infinitely across Kubernetes pods.
