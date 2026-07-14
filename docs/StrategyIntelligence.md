# Strategy Intelligence

Strategy Intelligence is the system that governs Procedural Memory within Agentix.

## Strategy Mining
Strategy Mining runs as an offline background process. It takes thousands of Episodic Memories and mathematically clusters them by intent, business domain, and structural dataset properties.

It looks for:
- Frequently repeated workflows.
- Frequently skipped steps.
- High success ratios.

## Strategy Builder
Once a pattern is identified by the Miner, the Builder transforms it into a permanent `ProceduralStrategy`. It applies strict thresholds (e.g., must have >3 supporting episodes, >70% success rate).

## Strategy Validation
The Validator ensures no conflicting strategies exist and handles versioning.

## Strategy Recommendation
During active Brain execution, the Recommender intercepts the cognitive loop. If it finds a Strategy matching the current goal, it overrides the LLM hallucination and injects deterministic execution logic.

## Strategy Learning
After every execution, the strategy's confidence and success metrics are dynamically updated. Highly successful strategies are PROMOTED. Poor strategies are RETIRED.
