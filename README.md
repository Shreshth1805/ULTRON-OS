# ULTRON OS

An AI operating system for building software: describe a project in plain
English and a chain of agents (planner → file generator → reviewer →
security scan → performance scan → tester → auto-fixer → reflection →
learner → version snapshot → GitHub publish) builds it for you. A second,
independent capability lets it profile a dataset and recommend/train an
ML model (AutoML). Backend only today — `backend/app` is a FastAPI service;
there is no frontend yet.

## Status

This is a working prototype, not a finished product. Most of the backend
(agents, orchestration, execution, workflow, versioning, skills, GitHub
integration) is real, implemented code — but only part of it is wired into
the running API. Treat anything not listed under **API** below as
in-progress rather than available.

Known limitations:

- **Generated projects run in this app's own environment**, not an
  isolated one. `POST /projects/build` executes and tests generated code
  using this venv's own interpreter (`sys.executable -m ...`), so a
  generated project's imports only work if its dependencies happen to
  already be installed here (FastAPI, pandas, etc. are). There is no
  per-project dependency install yet.
- **Generated test files live next to the source they test** (e.g.
  `app/test_main.py` beside `app/main.py`), which trips up pytest's
  default import-mode when the package has no `__init__.py`. Test
  collection can fail for reasons unrelated to the generated code itself.
- **The LLM doesn't always follow instructions.** File/test/reflection
  generation and parsing are defensive (markdown fences get stripped,
  JSON gets located inside surrounding prose) but not bulletproof.
- **No real sandboxing.** Generated code runs as a real subprocess with
  a timeout, not in a container or restricted environment. Don't point
  this at untrusted prompts.

## Quick start

Requires Python 3.11+ and a [Groq](https://console.groq.com) API key.

```bash
cd backend
python -m venv .venv
./.venv/Scripts/pip install -r requirements.txt   # Windows; use bin/pip on macOS/Linux
```

Create `backend/.env` (see [Environment variables](#environment-variables)
below for the full list):

```env
GROQ_API_KEY=your-key-here
GROQ_MODEL=openai/gpt-oss-120b
SECRET_KEY=some-random-string
```

`GROQ_MODEL` matters — Groq rotates its available model list, so check
`https://api.groq.com/openai/v1/models` with your key (or the Groq
console) for a model you currently have access to rather than assuming
any specific name still exists.

Run the server:

```bash
./.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs.

## API

All routers currently wired into `app/main.py`:

| Prefix | Purpose |
|---|---|
| `POST /chat/` | Conversational chat against the configured Groq model, with per-session in-memory history |
| `POST /projects/build` | The full autonomous build pipeline described above, given a text prompt |
| `/projects` | CRUD for project records (separate from `/projects/build` — this just tracks metadata in the DB) |
| `/ai` | The "software engineer" agent (`orchestration/brain.py`) — chat-style intent routing to code generation, AutoML, etc. |
| `/automl` | Train a model on an uploaded dataset |
| `/memory`, `/semantic-memory` | Conversation memory (older key-value store and newer vector-backed one, both still live) |
| `/knowledge` | Knowledge-base / RAG endpoints |
| `/tools` | Introspection over the registered tool/agent registry |
| `/llm` | Direct access to the model router |
| `/auth` | `POST /auth/register`, `POST /auth/login` — JWT auth backed by a real `users` table |
| `/users` | `GET /users/me` |

Plus `GET /`, `GET /health`, `GET /info` for basic status.

## Environment variables

Set in `backend/.env` (see `app/core/config.py` for the authoritative list
and defaults):

| Variable | Required | Notes |
|---|---|---|
| `GROQ_API_KEY` | yes | No default — the app won't start without it |
| `GROQ_MODEL` | yes (effectively) | Defaults to a model name that may no longer exist on your account; verify against Groq's `/models` endpoint |
| `SECRET_KEY` | recommended | JWT signing key for `/auth`. Defaults to a hardcoded dev value if unset — set a real one before relying on auth |
| `DATABASE_URL` | no | Defaults to local `sqlite:///./ultron.db` |
| `GITHUB_USERNAME`, `GITHUB_TOKEN` | no | Needed only for the GitHub-publish step of `/projects/build`; that step is skipped gracefully if unset |
| `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL` | no | Default to a local HuggingFace sentence-transformers model, downloaded on first run |
| `VECTOR_DB`, `VECTOR_DB_PATH` | no | Chroma, stored locally under `backend/vector_db/` |
| `OPENAI_API_KEY`, `NVIDIA_API_KEY` | no | Declared for future multi-provider support; not currently used by any wired code path |

## Project layout

```
backend/
  app/
    main.py            entry point — the actual set of live routers
    api/                FastAPI routers
    orchestration/      brain.py (chat intent routing) and project_builder.py (the full pipeline)
    agents/             one subpackage per agent (planner, reviewer, security, tester, fixer, ...)
    execution/          runs and auto-fixes generated code
    generators/         LLM-backed file/project-structure generation
    memory/, memory_v2/ two memory systems (v2 is the vector-backed one used by /semantic-memory)
    core/, database/    settings, DB session/engine
  requirements.txt
```

Everything else under `app/` (`bus/`, `workflow/`, `skills/`, `versioning/`,
`learning/`, most of `github/`) is real but not yet reachable from any
live endpoint — future capability, not dead code.
