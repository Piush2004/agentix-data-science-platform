# 🚀 Deployment

Agentix is designed to be easily deployable in modern cloud environments.

## Frontend (Vercel)
The Next.js frontend is heavily optimized for Vercel.
1. Push your repository to GitHub.
2. Import the project in Vercel.
3. Set the Root Directory to `frontend/`.
4. Add the `NEXT_PUBLIC_API_URL` environment variable.
5. Deploy.

## Backend (Docker)
The backend is fully containerized.

### AWS ECS / Azure Container Apps
1. Build the Docker image:
   ```bash
   docker build -t agentix-backend ./backend
   ```
2. Push to ECR / ACR.
3. Deploy as a managed container service.

### Railway / Render
For simpler deployments, connect your GitHub repo to Railway or Render. Specify the `backend/` directory and it will automatically build using the provided Dockerfile.

## Infrastructure
- **PostgreSQL**: We recommend AWS RDS, Supabase, or Neon.
- **Redis**: We recommend AWS ElastiCache or Upstash.
- **Ollama**: If using local models in production, deploy Ollama on a GPU-enabled instance (e.g., AWS g4dn).
