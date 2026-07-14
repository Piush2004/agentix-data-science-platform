# 🧠 Agentix Brain

The Agentix Brain acts as the cognitive operating system of the entire platform. Rather than blindly executing workflows, the Brain mimics a human Data Scientist's thought process.

## 11-Stage Cognitive Loop

### 1. Perception
Observes constraints, user goals, workspaces, and datasets. It strictly observes without making decisions.

### 2. Understanding
Synthesizes exact intent and required outcomes from the observations. 

### 3. Deliberation (System 2 Thinking)
Pauses to ask internal questions, gather deterministic evidence, generate multiple hypotheses, and objectively evaluate the best path forward.

### 4. Episodic Recall
Queries Episodic Memory to find structurally similar past executions based on dataset fingerprints.

### 5. Strategy Recall
Queries Procedural Memory for active, versioned execution strategies and evaluates their constraints against the current dataset. Outputs a `StrategyRecommendation`.

### 6. Reasoning
Deduces logical requirements based on deliberation and memory recall. Determines exactly *what should happen*.

### 7. Planning
Constructs the final executable workflow graph, estimating time, costs, and resource allocation.

### 8. Decision
Selects the optimal pathway. Chooses the best plan, engine, agent, and LLM model.

### 9. Execution
Coordinates specialized sub-engines (Pandas, SQL, Visualization) and monitors runtime execution.

### 10. Episode Writing
Packages the entire cognitive trace and execution metrics into a permanent `Episode` for long-term storage.

### 11. Strategy Learning
Feeds the episode outcome back into Procedural Memory to update strategy success rates, confidence, and usage counts. May autonomously PROMOTE or RETIRE strategies.

## Memory Integration

The Brain relies heavily on **Episodic Memory** to avoid repeating mistakes, and **Procedural Memory** to execute highly optimized workflows discovered through continuous learning.
