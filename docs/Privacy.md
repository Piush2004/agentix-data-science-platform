# 🛡️ Privacy

Agentix was built for strict enterprise environments where data privacy is non-negotiable.

## Zero Raw Dataset Storage
Agentix does **not** store raw row-level data in its PostgreSQL or Redis databases.

## Fingerprint Generation
The Episodic Memory system hashes datasets into a `DatasetFingerprint`. 
This fingerprint only contains:
- Column names
- Data types
- Null ratios
- Statistical bounds (min/max/mean)

## Prompt Compression & PII Masking
When routing to frontier models (OpenAI), only the necessary schema metadata is sent. Raw strings and PII are masked deterministically in Python before the prompt is constructed.

## Local Inference
Agentix natively supports Ollama. For ultra-sensitive deployments, the entire cognitive loop can run on local, air-gapped Llama-3 instances.
