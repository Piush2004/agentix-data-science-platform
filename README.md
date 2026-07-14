# Agentix

**AI-powered Data Science Operating System**

Agentix is an autonomous, scalable, and intelligent Operating System for Data Science, powered by the Agentix Cognitive Brain.

## 🚀 Deployment & Infrastructure

Agentix is designed for production. The complete stack can be spun up in seconds using Docker.

```bash
# Clone the repository
git clone https://github.com/agentix/agentix.git
cd agentix

# Setup Environment
cp .env.example .env

# Run the entire cluster
docker-compose up --build -d
```

### 🧠 Architecture Components
- **Frontend**: Next.js (Port 3000) - Designed for Vercel
- **Backend**: FastAPI (Port 8000) - Designed for Docker/Railway/Render
- **Database**: PostgreSQL 15 - Isolated State & Relational Schemas
- **Cache**: Redis 7 - Session management and API Rate Limiting

## 🛡️ Security & Performance
- **JWT Authentication**: Secured context with rotating tokens.
- **Middleware**: GZIP Compression, strict CORS limits, Helmet-equivalent headers, Payload limits (100MB).
- **Resilience**: Integrated retry loops for PostgreSQL and Redis to handle transient container boot sequences.

## 🩺 Monitoring
Available endpoints:
- `/api/v1/system/health` - Basic API Health
- `/api/v1/system/liveness` - K8s Liveness Probe
- `/api/v1/system/readiness` - K8s Readiness Probe (Checks Postgres & Redis)
- `/api/v1/system/system` - PSUtil Hardware telemetry

## 📝 License
Proprietary - Agentix AI 2026
