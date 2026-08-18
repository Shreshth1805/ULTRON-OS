# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## What this is

ULTRON OS: an AI operating system for building software. A user describes
a project in plain English and a chain of agents plans it, generates its
files, executes and tests them, auto-fixes failures, reviews/scans them,
reflects on the result, and can publish it to GitHub — plus a separate
AutoML capability that profiles a dataset and trains a model. `backend/`
is a FastAPI service; there is no frontend yet. See [README.md](README.md)
for setup and the current API surface.

## Commands

Backend (Python 3.11+), venv at `backend/.venv`:
```bash
cd backend
python -m venv .venv
./.venv/Scripts/pip install -r requirements.txt          # first time / after requirements.txt changes
./.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000   # dev server
```

There is no real automated test suite. The loose `test_*.py` scripts in
`backend/` (`test_brain.py`, `test_groq.py`, `test_planner.py`, etc.) are
manual smoke scripts — they print output for inspection, they don't
assert anything — run individually with `./.venv/Scripts/python test_brain.py`.
Do not assume a `pytest` run over `backend/` validates anything.

`requirements.txt` must stay in sync with what `app/main.py`'s import
chain actually pulls in — it drifted badly from reality before (missing
~12 packages the live code needed to even boot, while listing several
nothing imports). If you add an import anywhere reachable from `app.main`,
add its package here; don't assume something already installed elsewhere
on the machine will be there for a fresh clone.

## Architecture

### Only part of `app/` is actually running — check reachability before touching anything

`app/main.py` is the single source of truth for what's live: every
`app.include_router(...)` call there. A large fraction of `backend/app/`
(`execution/`, `bus/`, `workflow/`, `skills/`, `versioning/`, `learning/`,
most of `github/`, and roughly half of `agents/`) is real, coherent,
implemented code that is **not yet reachable from any live endpoint** —
it's an unfinished feature roadmap, not dead code, so don't delete it on
sight. But also don't assume something exists just because the folder
does; trace the actual import chain from `main.py` (and see the dynamic-
dispatch note below) before relying on a module being wired up.

Two things make "is this reachable" non-obvious:

1. **`tools/registry.py`'s `get_agent(name)`** lazily imports agent
   modules by string name inside a big if/elif chain, not via top-level
   imports — so a plain static import graph misses these edges. Any
   module only reached through `get_agent("some_agent")` still counts as
   live if the calling code itself is reachable from `main.py`.
2. **Two separate pipelines both claim "build a project"**:
   `orchestration/orchestrator.py` (live — driven by chat intents through
   `orchestration/brain.py`, itself reached via `POST /ai`) uses a generic
   `WorkflowTask`/dependency-graph engine (`workflow_engine.py`) and
   drives the more mature `agents/software_engineer/engineer.py`.
   `orchestration/project_builder.py` (live via `POST /projects/build`)
   is a separate, more hand-written imperative pipeline that additionally
   does performance review and version-snapshotting, but generates files
   with a much simpler one-call-per-file generator
   (`generators/file_generator.py`) with no shared context between files.
   They are not the same code path — don't assume a fix to one applies
   to the other.

### `get_agent()` must tolerate any agent being unavailable

`get_agent()` catches `Exception` broadly (not just `ImportError`) and
returns `None` on any load failure, because several agent modules build
a real client at *import time* (e.g. `memory_v2/embeddings.py` loads a
HuggingFace embedding model on import; `github/client.py` constructs a
`Github()` client and raises if no token is configured) — a config
problem in one agent should degrade that agent to unavailable, not crash
every caller. Any new code that calls `get_agent(...)` must handle a
`None` result; any new agent with an eager import-time dependency should
expect to be skipped gracefully when that dependency is missing, not
crash the process.

### LLM access goes through one proxy

Use `from app.core.llm import llm; llm.invoke(prompt_or_messages)` —
it routes through `llm/model_router.py` → `llm/registry.py`, which is
what's actually configured with the Groq client. Don't reach for
`core/groq.py`'s `groq_model` directly or build a new provider wrapper;
this proxy is the one every live agent already uses.

### LLM output needs fence-stripping before it's treated as code or JSON

Models routinely wrap responses in ` ```lang ... ``` ` even when told not
to. Anything that writes an LLM response to disk as a file, or parses it
as JSON, must go through `app.utils.text.strip_code_fence(...)` first —
skipping this produces syntactically invalid generated files (a `SyntaxError`
on the literal ` ```python ` line) that looks like a code-generation
failure but is actually a plumbing bug. Every current write site
(`generators/file_generator.py`, `generators/project_generator.py`,
`agents/tester/generator.py`, `execution/fixer.py`, `agents/fixer/parser.py`,
`agents/reflection/analyzer.py`) already does this — keep it that way in
any new one.

### Prompt templates using `.format()` must escape literal braces

A prompt built with `TEMPLATE.format(**kwargs)` will try to interpret
*every* `{`/`}` in the template as a placeholder — including braces in an
embedded "return JSON like this: `{...}`" example. Escape them as `{{`/`}}`,
or don't use `.format()` for that template (an f-string only parses the
outer braces, so embedding a whole constant via `f"{SOME_PROMPT}"` is
safe regardless of what's inside `SOME_PROMPT`). Get this wrong and the
prompt call raises `KeyError` with a mangled key before the LLM is even
invoked.

### Generated projects execute in this app's own venv, not an isolated one

`execution/runner.py` and `agents/tester/runner.py` run generated code via
`sys.executable -m <module>` / `sys.executable -m pytest`, both with
`cwd` set to the generated project's root and a timeout (so a generated
entry point that starts a real server via `uvicorn.run(...)` doesn't hang
the request forever). Using `-m` from the project root — rather than
running the entry file as a bare script — is what lets a generated
project's own internal imports (`uvicorn.run("app.main:app")`,
`from app.main import app` in a generated test) resolve, since `-m` puts
the project root on `sys.path`. But there is still no per-project
dependency isolation: a generated project only runs successfully if its
imports happen to already be installed in `backend/.venv`. Don't assume
arbitrary generated projects will execute correctly.

### Don't trust an LLM response to match the format you asked for

Beyond markdown fences (above), a model asked for "just a file list, one
path per line" can still return install/run instructions instead of
paths, and a model asked to test one file in isolation will guess at
that file's import path if you don't tell it explicitly. Both bit
`project_builder`'s pipeline in practice:
`generators/project_generator.get_structure()` filters every candidate
line through `app.utils.text.looks_like_file_path()` rather than trusting
anything non-blank; `agents/tester/prompts.TEST_PROMPT` explicitly states
the file's real dotted module path rather than leaving the model to
infer it; `generators/file_generator.generate()` is told the project's
full file list so it doesn't redefine something another file already
owns. The pattern to follow for new generation code: validate/constrain
what a "return only X" instruction actually produced rather than
assuming compliance, and give the model any structural fact it would
otherwise have to guess (paths, module names, what else exists) instead
of hoping it infers correctly.

### `GROQ_MODEL` is not a stable constant

Groq periodically retires model names. If chat/build requests start
failing with `groq.NotFoundError: model ... does not exist`, that's
almost always a stale `GROQ_MODEL` value, not a code bug — check
`https://api.groq.com/openai/v1/models` with the configured key for a
model currently available to that account before debugging further.

### Two memory systems coexist

`memory/` (older, key-value, used by `orchestration/brain.py`) and
`memory_v2/` (newer, Chroma-vector-backed, used by `POST /semantic-memory`)
are both live and independent — they are not layered on each other.
Know which one a given code path is touching before changing either.
