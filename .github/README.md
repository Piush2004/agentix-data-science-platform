<div align="center">
  <h1>🧠 Agentix</h1>
  <p><strong>The Cognitive Operating System for Enterprise-Scale AI</strong></p>
</div>

<br />

Agentix is not a chatbot or a simple workflow runner. It is an autonomous **Cognitive Engine** built to replicate the structured reasoning of a Senior Data Scientist. It perceives environments, deliberates multiple hypotheses, tests structural validations, remembers past experiences (Episodic Memory), and extracts highly successful patterns into permanent reusable knowledge (Procedural Strategies).

---

## 🌟 Key Capabilities

### 1. The Cognitive Brain
Instead of blindly executing prompts, the Agentix Brain uses a structured 8-stage cognitive cycle:
- **Perception**: Observes constraints, user goals, and datasets.
- **Understanding**: Synthesizes the exact intent and required outcomes.
- **Deliberation (System 2 Thinking)**: Pauses to ask internal questions, gathers evidence, generates multiple hypotheses, and objectively evaluates the best path forward.
- **Reasoning**: Logically deduces execution steps based on deliberation.
- **Planning**: Constructs the final executable workflow graph.
- **Execution**: Coordinates specialized sub-engines.
- **Learning**: Evaluates success and stores the experience.

### 2. Episodic Memory
Agentix remembers every past execution. It fingerprints datasets conceptually (types, distributions, schemas) without needing the raw data. When faced with a new task, it instantly retrieves similar historical episodes to predict success rates and avoid past mistakes.

### 3. Procedural Memory (Strategy Mining)
Offline analytics continuously mine the Episodic Memory store. It mathematically identifies the most successful workflow patterns and elevates them into permanent **Strategies**. These strategies are version-controlled and injected directly into future planning cycles.

---

## 🚀 Quick Start

### Backend (FastAPI Core)
The intelligence layer runs as a high-concurrency microservices backend.

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend (Next.js Dashboard)
The interface is built with React/Next.js for a beautiful, dynamic interaction layer.

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing the Engine

Agentix maintains zero-regression strictness for its cognitive and memory modules.

```bash
cd backend
# Run full suite
python -m pytest core/ -v

# Test Specific Modules
python -m pytest core/brain/tests/ -v
python -m pytest core/memory/episodic/tests/ -v
python -m pytest core/memory/procedural/strategy_builder/tests/ -v
```

---

## 🏗️ Architecture

For a deep dive into the 8-stage cognitive cycle, episodic indexing, and strategy mining algorithms, see our comprehensive architecture docs:
- [Agentix Brain Architecture](backend/core/brain/README.md)
- [Procedural Memory & Strategy Mining](backend/core/memory/procedural/strategy_mining/README.md)

---

## 🤝 Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit Pull Requests, run the CI pipeline, and adhere to our deterministic constraints.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
