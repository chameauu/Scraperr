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

## Run a minimal example

```bash
uv run python examples/run_fake.py
```

## Run with Azure OpenAI

1. Copy the env template and fill in values:

```bash
cp .env.example .env
```

2. Run the Azure example:

```bash
uv run python examples/run_azure.py
```

The example loads `.env` automatically using `python-dotenv`.

## Run with Foundry Responses

1. Add Foundry variables to `.env`:

```
FOUNDRY_ENDPOINT=https://<your-foundry-endpoint>
FOUNDRY_API_KEY=...
FOUNDRY_MODEL=<deployment-name>
```

2. Run the Foundry example:

```bash
uv run python examples/run_foundry.py
```

## Run with Lightpanda + SearxNG

1. Set env vars in `.env`:

```
LIGHTPANDA_CDP_URL=http://localhost:9222
SEARXNG_BASE_URL=http://localhost:8888
SCRAPER_TASK=get latest 10 hackernews articles
```

2. Run the Lightpanda example:

```bash
uv run python examples/run_lightpanda.py
```

You can also pass optional CLI args:

```bash
uv run python examples/run_lightpanda.py --task "get latest 10 hackernews articles" --start-url "https://news.ycombinator.com/"
```

Add `--verbose` to print progress events:

```bash
uv run python examples/run_lightpanda.py --verbose
```

## Environment
 (Optional) Start a local SearxNG instance for search actions using `docker compose up -d`.
- `LIGHTPANDA_CDP_URL`: CDP endpoint for Lightpanda (used by the adapter when implemented)
