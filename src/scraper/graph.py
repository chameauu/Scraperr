from __future__ import annotations

from collections.abc import Awaitable, Callable

from langgraph.graph import END, START, StateGraph

from .actions import Action
from .browser import BrowserAdapter
from .execute import execute_action
from .model import ModelClient
from .observe import observe
from .state import GraphState
from .validate import validate

decide_fn = Callable[[GraphState], Awaitable[Action]]
progress_fn = Callable[[dict], Awaitable[None]]


def build_graph(
    browser: BrowserAdapter,
    decide: decide_fn | None,
    model: ModelClient | None = None,
    search_client=None,
    progress: progress_fn | None = None,
    observe_timeout_s: float | None = None,
):
    builder = StateGraph(GraphState)

    async def observe_node(state: GraphState):
        if progress is not None:
            await progress({"kind": "pre_observe", "step": state["step"]})
        try:
            updates = await observe(browser, state, timeout_s=observe_timeout_s)
        except TimeoutError:
            if progress is not None:
                await progress({"kind": "observe_timeout", "step": state["step"]})
            return {"last_error": "observe_timeout"}
        if progress is not None:
            await progress({"kind": "observe", "step": updates["step"]})
        return updates

    async def decide_node(state: GraphState):
        if decide is not None:
            action = await decide(state)
        elif model is not None:
            action = await model.decide_action(state)
        else:
            raise ValueError("decide or model must be provided")
        if progress is not None:
            await progress({"kind": "decide", "action": action.model_dump()})
        return {
            "last_action": action.model_dump(),
            "actions": state["actions"] + [action.model_dump()],
        }

    async def schema_node(state: GraphState):
        if state["schema"] is not None or model is None:
            return {}
        schema = await model.generate_schema(state)
        return {"schema": schema}

    async def execute_node(state: GraphState):
        action = Action.model_validate(state["last_action"])
        if progress is not None:
            await progress({"kind": "pre_execute", "action": action.model_dump()})
        updates = await execute_action(
            browser, state, action, model=model, search_client=search_client
        )
        if progress is not None:
            await progress({"kind": "execute", "action": action.model_dump()})
        return updates

    def route_after_validate(state: GraphState):
        return "end" if state["status"] in {"completed", "failed"} else "observe"

    async def start_node(state: GraphState):
        if state.get("start_url"):
            action = Action(type="navigate", target=state["start_url"])
            if progress is not None:
                await progress({"kind": "pre_execute", "action": action.model_dump()})
            updates = await execute_action(
                browser, state, action, model=model, search_client=search_client
            )
            if progress is not None:
                await progress({"kind": "execute", "action": action.model_dump()})
            return {
                **updates,
                "last_action": action.model_dump(),
                "actions": state["actions"] + [action.model_dump()],
            }
        return {}

    builder.add_node("start", start_node)
    builder.add_node("observe", observe_node)
    builder.add_node("schema", schema_node)
    builder.add_node("decide", decide_node)
    builder.add_node("execute", execute_node)

    async def validate_node_async(state: GraphState):
        updates = validate(state)
        if progress is not None:
            await progress({"kind": "validate", **updates})
        return updates

    builder.add_node("validate", validate_node_async)

    builder.add_edge(START, "start")
    builder.add_edge("start", "observe")

    def route_after_observe(state: GraphState):
        return "validate" if state.get("last_error") else "schema"

    builder.add_conditional_edges(
        "observe",
        route_after_observe,
        {
            "schema": "schema",
            "validate": "validate",
        },
    )
    builder.add_edge("schema", "decide")
    builder.add_edge("decide", "execute")
    builder.add_edge("execute", "validate")
    builder.add_conditional_edges(
        "validate",
        route_after_validate,
        {
            "observe": "observe",
            "end": END,
        },
    )

    return builder.compile()
