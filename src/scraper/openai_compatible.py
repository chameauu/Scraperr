from __future__ import annotations

import json
from typing import Any

import httpx

from .actions import Action
from .state import GraphState


class OpenAICompatibleModel:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._transport = transport

    async def decide_action(self, state: GraphState) -> Action:
        prompt = {
            "task": state["task"],
            "step": state["step"],
            "last_error": state["last_error"],
            "observations": state["observations"][-1:] or [],
            "schema": state["schema"],
        }
        response = await self._post_chat(
            system="You are a browser agent. Return ONLY JSON for an Action.",
            user=json.dumps(prompt),
        )
        return Action.model_validate(response)

    async def generate_schema(self, state: GraphState) -> dict:
        prompt = {
            "task": state["task"],
            "observations": state["observations"][-1:] or [],
        }
        response = await self._post_chat(
            system="Generate a JSON Schema for the extraction result. Return ONLY JSON.",
            user=json.dumps(prompt),
        )
        if not isinstance(response, dict):
            raise TypeError("Schema response must be a JSON object")
        return response

    async def extract_data(self, state: GraphState) -> list[dict]:
        prompt = {
            "task": state["task"],
            "observations": state["observations"][-1:] or [],
            "schema": state["schema"],
        }
        response = await self._post_chat(
            system="Extract data and return ONLY JSON as a list of objects.",
            user=json.dumps(prompt),
        )
        if not isinstance(response, list):
            raise TypeError("Extraction response must be a JSON array")
        return response

    async def _post_chat(self, system: str, user: str) -> Any:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            resp = await client.post(
                f"{self._base_url}/chat/completions", json=payload, headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
