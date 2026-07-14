# Agentix Architecture

This document describes the high-level architecture of Agentix, an AI-powered Data Science Operating System.

## Overview

Agentix operates on a strict separation of concerns, divided primarily into the Frontend (Next.js) and the Backend (FastAPI). The Backend houses the "Brain" — a cognitive reasoning engine that delegates execution to specialized workers.

## Components

### 1. Frontend (Next.js)
The presentation layer is built with Next.js 14 and React. It utilizes Server-Side Rendering (SSR) for initial load performance and heavily leans into Client-Side fetching via React Query for real-time Agentix Brain updates.

### 2. Backend (FastAPI)
The API layer acts as a strict gateway. It contains zero business logic, merely translating HTTP REST calls into Data Transfer Objects (DTOs) passed into the Service layer.

### 3. Agentix Brain
The Brain is the cognitive orchestrator. It uses an 11-stage pipeline:
`Perception` → `Understanding` → `Deliberation` → `Episodic Recall` → `Strategy Recall` → `Reasoning` → `Planning` → `Decision` → `Execution` → `Episode Writing` → `Strategy Learning`.

### 4. Memory Subsystems
- **Episodic Memory**: Stores "Experiences". It fingerprints incoming datasets deterministically and matches them against historical runs.
- **Procedural Memory (Strategy Engine)**: Offline mining continuously evaluates Episodic Memory to extract, validate, and publish permanent generalized Strategies.

### 5. LangGraph & LLM Routing
Agentix utilizes a custom implementation inspired by LangGraph to manage state machines. LLM routing is deterministic: simple classification uses local models (e.g., Ollama), while complex reasoning utilizes frontier models (e.g., GPT-4 / Claude 3).

### 6. Workflow Engine
The actual execution of data science workflows (Cleaning, AutoML) occurs via specialized deterministic python engines (Pandas, Scikit-learn), invoked by the Brain's sub-agents.

### 7. Monitoring
OpenTelemetry is used to trace requests across the Next.js / FastAPI boundary, feeding into a Prometheus/Grafana stack for observability.

### 8. Deployment
Agentix is completely Dockerized. Production deployments typically utilize Vercel for the Next.js frontend and managed Kubernetes (or AWS ECS) for the FastAPI workers.

## Diagrams

For visual representations of the system, please refer to the `docs/diagrams/` folder.
