# Tech Stack

Agentix is built on a modern, scalable, and developer-friendly stack.

## Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui & Radix Primitives
- **State Management**: React Query (Server state) & Zustand (Client state)
- **Data Visualization**: Recharts / D3.js

## Backend
- **Framework**: FastAPI (Python 3.11+)
- **Concurrency**: Asyncio & Uvicorn
- **Validation**: Pydantic V2
- **Testing**: Pytest

## AI & Cognitive Engine
- **Orchestration**: Custom State Machines (Inspired by LangGraph)
- **Local LLMs**: Ollama integration
- **Cloud LLMs**: OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet
- **Embeddings**: SentenceTransformers / BGE

## Database & Storage
- **Relational DB**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 / Prisma
- **Caching & Pub/Sub**: Redis 7
- **Object Storage**: S3-compatible (MinIO for local)

## Deployment & Infrastructure
- **Containerization**: Docker & Docker Compose
- **Frontend Hosting**: Vercel
- **CI/CD**: GitHub Actions

## Developer Tools
- **Linting (Python)**: Ruff, Black, Mypy
- **Linting (TS)**: ESLint, Prettier
- **Observability**: OpenTelemetry
