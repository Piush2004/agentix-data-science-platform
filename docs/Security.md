# 🔒 Security

Agentix handles sensitive enterprise data. Security is our top priority.

## Authentication & Authorization
- *Planned*: OAuth2 and JWT-based authentication.
- *Planned*: Role-Based Access Control (RBAC) to ensure analysts cannot modify Core Strategies.

## Rate Limiting
API endpoints are protected by Redis-backed rate limiting to prevent DDOS and LLM cost-exhaustion attacks.

## Encryption
- Data at rest in PostgreSQL must be encrypted by the managed database provider.
- All intra-service communication requires TLS.

## PII Protection
Agentix implements rigorous PII (Personally Identifiable Information) masking.
1. The `Data Quality Agent` scans incoming datasets.
2. Columns resembling emails, SSNs, or credit cards are strictly masked before any data hits the Deliberation Engine.

## Future Plans
- Zero-Trust Architecture.
- Fully ephemeral workspaces (Data deleted immediately after workflow completion).
