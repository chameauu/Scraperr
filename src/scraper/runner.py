from __future__ import annotations

from .browser import BrowserAdapter
from .graph import build_graph
from .model import ModelClient
from .runtime import agent_runtime
from .search import SearxNGClient
from .state import GraphState, initial_state


async def run_agent(
    task: str,
    *,
    browser: BrowserAdapter,
    model: ModelClient | None = None,
    search_client: SearxNGClient | None = None,
    decide=None,
) -> GraphState:
    state = initial_state(task)

    async with agent_runtime(browser=browser, model=model, search_client=search_client):
        graph = build_graph(browser, decide=decide, model=model, search_client=search_client)
        return await graph.ainvoke(state)
