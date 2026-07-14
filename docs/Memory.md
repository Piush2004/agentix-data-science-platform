# 💾 Memory Systems

Agentix shifts from simple context-window RAG to a layered cognitive memory structure inspired by human psychology.

## 1. Episodic Memory

Episodic Memory records unique, individual experiences. 

**How it works:**
- Every executed workflow becomes an `Episode`.
- Instead of raw data, datasets are deterministically hashed into a `DatasetFingerprint` (schema, types, sparsity).
- When a new task arrives, the Brain queries Episodic Memory using structural similarity.
- It returns `EpisodeRecommendations` to help the Brain predict success and avoid known failure modes.

## 2. Procedural Memory

Procedural Memory represents "learned skills." It takes thousands of Episodic memories and extracts universal truths.

**How it works:**
- **Strategy Mining**: An offline process clusters episodes and finds highly successful workflow graphs.
- **Strategy Builder**: Validates the mined patterns and creates permanent, versioned `ProceduralStrategies`.
- **Strategy Recommendation**: Injects known strategies into the active Brain planning cycle.
- **Strategy Learning**: After every execution, the strategy's confidence and success rate are mathematically updated. Poor strategies are automatically retired.

## 3. Semantic Memory (Future Roadmap)

*Status: Planned for v0.5*

Semantic Memory will translate structural fingerprints into deep Knowledge Graphs (Neo4j). This will allow Agentix to understand complex domain relationships (e.g., knowing that "Sales Revenue" and "Monthly Gross Income" are semantically identical across disparate datasets).
