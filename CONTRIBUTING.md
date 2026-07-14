# Contributing to Agentix

First off, thank you for considering contributing to Agentix! 

## Getting Started

### 1. Fork & Clone
1. Fork the repository to your GitHub account.
2. Clone locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Agentix.git
   cd Agentix
   ```

### 2. Local Installation
- **Backend**:
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- **Frontend**:
  ```bash
  cd frontend
  npm install
  ```

## Development Workflow

### Branch Naming
Please use the following conventions:
- `feature/description-of-feature`
- `bugfix/description-of-bug`
- `docs/description-of-docs`

### Coding Standards
- **Python**: Adhere to PEP 8. Use `black` for formatting and `ruff` for linting. Include Type Hints.
- **TypeScript**: Adhere to the ESLint configuration. Run `npm run lint` before committing.

### Commit Messages
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat: added new deliberation capability`
- `fix: resolved memory leak in episodic storage`
- `docs: updated api endpoints`

## Pull Request Process

1. Ensure your branch is up to date with `develop`.
2. Run the test suite: `pytest backend/core/ -v`
3. Push to your fork and submit a Pull Request against the `develop` branch.
4. Fill out the mandatory PR template completely.
5. A maintainer will review your code within 48 hours.

## Architectural Constraints
- **Zero LLM usage in Core Memory**: All strategy evaluation must remain deterministic.
- **Pydantic Validation**: All data passing between cognitive layers MUST be strongly typed.
