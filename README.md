# Scraper

An academic web-scraping agent that collects structured data from public websites. The agent accepts a natural-language task, browses web pages, performs actions, validates the extracted data, and returns a structured result.

The project is designed to show how an AI agent can observe a page, make a decision, use browser tools, recover from errors, and finish when the result is valid.

## Purpose

The agent automates the collection of public web data. It can start from a URL or search for relevant pages, interact with them, extract information, and validate the final result.

It works only with public pages. It does not support authentication, CAPTCHA solving, access-control bypass, or anti-bot circumvention. It also uses limits for steps, pages, retries, and execution time.

## How the Workflow Works

The agent follows this cycle:

1. **Observe** the current page and create a compact page representation.
2. **Decide** on one structured action.
3. **Execute** the action through the browser, search, or extraction tool.
4. **Validate** the result and decide whether to continue, recover, finish, or fail.

The agent records observations, actions, errors, and validation results for every step.

## Architecture

```text
User task
    |
    v
LangGraph workflow
    |
    +--> Observe page --> Decide action --> Execute action --> Validate result
                                      ^                         |
                                      |                         +--> Continue
                                      |                         +--> Recover
                                      |                         +--> Finish
                                      |                         +--> Fail
                                      |
                              Browser and search tools
```

### Main Components

- **LangGraph**: Connects the workflow steps and keeps the agent state.
- **Playwright**: Controls the browser through the Chrome DevTools Protocol.
- **Lightpanda**: Provides the browser runtime through CDP.
- **SearXNG**: Helps discover relevant public pages when no starting URL is provided.
- **Model clients**: Choose actions, generate schemas, and extract data.
- **Pydantic**: Validates actions and extracted records.
- **Pytest**: Tests the workflow, recovery, safety, and validation behavior.

## Structured Actions

The model returns one action at each step. Supported actions are:

- `search`
- `navigate`
- `click`
- `type`
- `scroll`
- `extract`
- `back`
- `finish`
- `fail`

The model cannot execute arbitrary JavaScript or shell commands. Actions are validated before they are sent to the browser or another tool.

## Data Extraction

A user can provide an extraction schema, or the model can generate one before extraction. Extracted records are validated with Pydantic.

JSON is the main result format. CSV output is available when the data is tabular. Invalid records are not silently accepted as successful results.

## Recovery and Safety

When an action fails, the agent records the error and takes a new observation when the browser is still usable. It can then select another action when retry limits allow it.

The agent also uses safety checks and execution limits:

- Only HTTP and HTTPS URLs are allowed.
- Local, loopback, link-local, and private network destinations are blocked by default.
- Maximum steps, pages, retries, and time are limited.
- Browser resources are closed after success, failure, timeout, or cancellation.

## Installation

This project uses `uv` for Python dependencies:

```bash
cd docs/scraper
uv sync --dev
```

Install the pre-commit hooks with:

```bash
uv run pre-commit install
```

Or use the helper script:

```bash
./scripts/install-hooks.sh
```

## Run Tests

```bash
uv run pytest
```

The tests cover the graph workflow, action history, compact observations, schema generation, extraction validation, recovery, timeouts, URL safety, search, and model errors.

## Examples

### Run the local example

```bash
uv run python examples/run_fake.py
```

### Run with Azure OpenAI

Copy the environment template and add the required values:

```bash
cp .env.example .env
uv run python examples/run_azure.py
```

The example loads `.env` automatically with `python-dotenv`.

### Run with Foundry Responses

Add the following values to `.env`:

```text
FOUNDRY_ENDPOINT=https://<your-foundry-endpoint>
FOUNDRY_API_KEY=...
FOUNDRY_MODEL=<deployment-name>
```

Then run:

```bash
uv run python examples/run_foundry.py
```

### Run with Lightpanda and SearXNG

Set the browser and search endpoints:

```text
LIGHTPANDA_CDP_URL=http://localhost:9222
SEARXNG_BASE_URL=http://localhost:8888
SCRAPER_TASK=get latest 10 hackernews articles
```

Run the agent:

```bash
uv run python examples/run_lightpanda.py
```

You can also provide the task and starting URL directly:

```bash
uv run python examples/run_lightpanda.py \
  --task "get latest 10 hackernews articles" \
  --start-url "https://news.ycombinator.com/"
```

Use `--verbose` to print progress events:

```bash
uv run python examples/run_lightpanda.py --verbose
```

An optional local SearXNG instance can be started with:

```bash
docker compose up -d
```

## What I Learned

This project helped me understand how to build an AI agent as a stateful workflow instead of one large function. I learned how to connect browser automation with LangGraph and how to make model actions structured and predictable.

I also learned that an autonomous agent needs more than an LLM. It needs clear state, safe tools, execution limits, error recovery, structured output, and a reliable way to validate the final result.
