# Frequently Asked Questions (FAQ)

### What is Agentix?
Agentix is an AI-powered Data Science Operating System. Unlike traditional chatbots, it acts as an autonomous Cognitive Engine. You give it a business goal, and it autonomously perceives the data, generates hypotheses, deliberates on the best approach, and executes a full data science pipeline.

### How does it work?
Agentix relies on an 11-stage cognitive loop (Perception → Understanding → Deliberation → Episodic Recall → Strategy Recall → Reasoning → Planning → Decision → Execution → Episode Writing → Strategy Learning). It marries deterministic python execution with LLM reasoning.

### Which LLMs are supported?
Through our flexible Gateway, we currently support:
- **Cloud**: OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet)
- **Local**: Ollama (Llama 3, Mistral)

### Can I use OpenAI?
Yes! Simply configure your `.env` file with `OPENAI_API_KEY`. 

### Can I use Ollama?
Yes! Agentix heavily advocates for local, privacy-preserving AI. You can route simple intent-classification tasks to a local Ollama instance to save costs.

### Can I deploy locally?
Absolutely. The repository includes a `docker-compose.yml` file that spins up the FastAPI backend, Next.js frontend, PostgreSQL, and Redis cache entirely on your local machine.

### Can I deploy on the cloud?
Yes. We recommend Vercel for the Next.js frontend and AWS ECS / EKS or Google Cloud Run for the containerized FastAPI backend. Ensure you configure a managed PostgreSQL and Redis instance (e.g., AWS RDS/ElastiCache).
