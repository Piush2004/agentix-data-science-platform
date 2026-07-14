# Project Structure

This document outlines the folder structure of the Agentix repository and explains the responsibility of each major directory.

```text
Agentix/
│
├── frontend/             # Next.js 14 React Application
│   ├── app/              # App router pages and layouts
│   ├── components/       # Reusable UI components (shadcn/ui, tailwind)
│   ├── lib/              # Utility functions and API clients
│   └── public/           # Static assets
│
├── backend/              # FastAPI Application
│   ├── app/              # FastAPI entry points and API routers
│   └── core/             # The cognitive engine and business logic
│       ├── agents/       # Specialized autonomous workers
│       ├── brain/        # Cognitive loop, deliberation, reasoning
│       ├── engines/      # Execution environments (AutoML, Pandas)
│       ├── memory/       # Episodic & Procedural memory subsystems
│       └── services/     # High-level orchestration services
│
├── docs/                 # Documentation Ecosystem
│   ├── api/              # API Reference
│   ├── architecture/     # Deep dives into system design
│   ├── diagrams/         # Mermaid and architecture diagrams
│   ├── deployment/       # Docker, Vercel, AWS setup guides
│   ├── research/         # Theory behind the Cognitive Brain
│   ├── screenshots/      # UI screenshots for README
│   └── tutorials/        # Walkthroughs for end-users
│
├── .github/              # GitHub configurations
│   ├── ISSUE_TEMPLATE/   # Templates for Bugs, Features, Questions
│   └── workflows/        # CI/CD pipelines (Pytest, ESLint)
│
├── examples/             # Example datasets and API payload scripts
├── scripts/              # Utility scripts for database migration/setup
├── tests/                # E2E test suites crossing front/backend
│
├── README.md             # Project landing page
├── ARCHITECTURE.md       # High-level architecture overview
├── CONTRIBUTING.md       # Open-source contribution guidelines
└── docker-compose.yml    # Local multi-container orchestration
```
