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


def build_graph(browser: BrowserAdapter, decide: decide_fn, model: ModelClient | None = None):
    builder = StateGraph(GraphState)

    async def observe_node(state: GraphState):
        return await observe(browser, state)

    async def decide_node(state: GraphState):
        action = await decide(state)
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
        return await execute_action(browser, state, action)

    def validate_node(state: GraphState):
        return validate(state)

    def route_after_validate(state: GraphState):
        return "end" if state["status"] in {"completed", "failed"} else "observe"

    builder.add_node("observe", observe_node)
    builder.add_node("schema", schema_node)
    builder.add_node("decide", decide_node)
    builder.add_node("execute", execute_node)
    builder.add_node("validate", validate_node)

    builder.add_edge(START, "observe")
    builder.add_edge("observe", "schema")
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
