import os

# 1. Backend Dockerfile
backend_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "core.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# 2. Frontend Dockerfile
frontend_dockerfile = """
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
"""

# 3. docker-compose.yml
docker_compose = """
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://agentix:agentixpass@db:5432/agentix
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=agentix
      - POSTGRES_PASSWORD=agentixpass
      - POSTGRES_DB=agentix
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agentix"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
"""

# 4. .env.example
env_example = """
# Agentix Environment Configuration

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agentix

# Redis Cache & Session
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET=generate-a-secure-random-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# AI Models
OPENAI_API_KEY=sk-your-openai-api-key
NVIDIA_API_KEY=nvapi-your-nvidia-api-key
OLLAMA_HOST=http://localhost:11434

# App Config
ENVIRONMENT=development # production, development
UPLOAD_DIRECTORY=./uploads
MAX_UPLOAD_SIZE_MB=50

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
"""

# 5. GitHub Actions Workflow
github_actions = """
name: Agentix CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpassword
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Pytest
      env:
        DATABASE_URL: postgresql://testuser:testpassword@localhost:5432/testdb
        REDIS_URL: redis://localhost:6379/0
      run: |
        cd backend
        python -m pytest tests/

  frontend-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    - name: Build
      run: |
        cd frontend
        npm run build

  docker-build:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-build]
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker Compose
      run: docker-compose build
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\\n")
    print(f"Created {path}")

write_file("backend/Dockerfile", backend_dockerfile)
write_file("frontend/Dockerfile", frontend_dockerfile)
write_file("docker-compose.yml", docker_compose)
write_file(".env.example", env_example)
write_file(".env.production.example", env_example.replace("ENVIRONMENT=development", "ENVIRONMENT=production"))
write_file(".github/workflows/ci.yml", github_actions)

print("Infrastructure files created.")
