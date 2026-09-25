from __future__ import annotations

import json
from typing import Any

import httpx

from .actions import Action
from .state import GraphState


class AzureOpenAIModel:
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment: str,
        api_version: str,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout: float = 30,
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._deployment = deployment
        self._api_version = api_version
        self._client = httpx.AsyncClient(transport=transport, timeout=timeout)
        self._headers = {
            "api-key": api_key,
            "Content-Type": "application/json",
        }

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
        payload = {
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        url = (
            f"{self._endpoint}/openai/deployments/{self._deployment}/chat/completions"
            f"?api-version={self._api_version}"
        )
        resp = await self._client.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)

    async def aclose(self) -> None:
        await self._client.aclose()
