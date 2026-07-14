# 💻 Installation

Follow these steps to run Agentix locally.

## Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ (Local or Docker)
- Redis 7+ (Local or Docker)
- Ollama (Optional, for local LLM inference)

## Environment Variables
Create a `.env` file in the root directory:

```ini
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/agentix
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-xxxxxx

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Local Setup

### 1. Database & Cache
We recommend using Docker for supporting infrastructure:
```bash
docker-compose up -d postgres redis
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Production Setup
For production, refer to [Deployment.md](Deployment.md).
