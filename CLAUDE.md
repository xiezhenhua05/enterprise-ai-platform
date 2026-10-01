# enterprise-ai-platform

Production-style AI platform: RAG (Milvus + BM25 hybrid) → Skill Registry → ReAct / multi-agent → model serving & routing, with observability and security built in from day one.

## Commands
- `make up` / `docker-compose up -d --build` — start the stack
- `make test` — run pytest (must stay green before every commit)
- `make lint`, `make bench`, `make eval`

## Conventions
- Python, FastAPI, code under `app/` (core, api, rag, skills, agent, memory, models, security, observability)
- Every new module gets Prometheus metrics in `app/observability/metrics.py` and tests under `tests/`
- Architecture decisions go in `docs/adr/NNN-title.md`; security threats go in `docs/threat-model.md` as `T<number>`. Always continue from the highest existing number — check the files, never guess.
- Conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`)
- Never commit `.env`, API keys or tokens

## Study workflow (local only)
If the `.study/` folder exists, read it before working on a "Day N" task:
- `.study/spec/dayNN.md` — the specification for that day (may differ from the real code)
- `.study/execution-log.md` — what was actually built and how it differs from the spec. The real code and this log win over the spec.
- `.study/project-state.md` — cumulative summary of modules, ADR and threat numbers

## How I want to work
- I am learning. For core logic, explain the design first and let me write or review it; do not silently generate whole modules.
- Propose a plan before editing multiple files.
- After finishing a task, run the tests and show me the result.
