# Scraper (Agent Core)

This is the **agent-core only** scaffold for the lightweight web-scraping project.

## Scope (current)

- LangGraph state machine with explicit observe → decide → execute → validate loop
- Lightpanda adapter surface (stubbed)
- Tests for happy-path, recovery, and schema-generation flow

## Not yet included

- FastAPI API
- CLI
- PostgreSQL persistence
- SearXNG search tool integration

## Setup (uv)

```bash
cd docs/scraper
uv sync --dev
```

## Pre-commit hooks

Install the git hook to run checks before every commit:

```bash
uv run pre-commit install
```

Or run the helper script:

```bash
./scripts/install-hooks.sh
```

## Run tests

```bash
uv run pytest
```

## Environment

- `LIGHTPANDA_CDP_URL`: CDP endpoint for Lightpanda (used by the adapter when implemented)
