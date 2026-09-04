# AgentMesh-AI

**Bounded DAG-based AI agent orchestrator with retries, circuit breakers, tool permissions and audit logs.**

## Why this project matters
This is a portfolio-grade, API-first project designed to demonstrate production-minded AI/automation engineering: bounded decisions, explainability, deterministic tests and no hard-coded paid API dependency.

## Features
- FastAPI service
- Dependency-aware DAG execution
- Retry policy and timeout guard
- Circuit breaker after repeated failures
- Structured audit trail per run
- Zero API keys required for the core demo
- Unit-tested core orchestration

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## Test
```bash
pytest -q
```

## Architecture
```text
Client -> FastAPI -> AgentMesh DAG -> Retry/Timeout/Circuit Breaker -> Audit Log -> JSON result
```

## Portfolio note
This repository is intentionally self-contained and uses no live customer data. Tool/action functions are deterministic demo adapters; replace them with authorized integrations for production use.
