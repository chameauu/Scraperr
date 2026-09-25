from __future__ import annotations

import json
from typing import Any

import httpx

from .actions import Action
from .state import GraphState


class FoundryResponsesModel:
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        model: str,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout: float = 30,
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._model = model
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
        response = await self._post_responses(
            system=(
                "You are a browser agent. Return ONLY JSON with keys: "
                'type, target, value, reason. Example: {"type":"search",'
                ' "value":"query"}.'
            ),
            user=json.dumps(prompt),
        )
        return Action.model_validate(_normalize_action_payload(response))

    async def generate_schema(self, state: GraphState) -> dict:
        prompt = {
            "task": state["task"],
            "observations": state["observations"][-1:] or [],
        }
        response = await self._post_responses(
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
        response = await self._post_responses(
            system="Extract data and return ONLY JSON as a list of objects.",
            user=json.dumps(prompt),
        )
        if not isinstance(response, list):
            raise TypeError("Extraction response must be a JSON array")
        return response

    async def _post_responses(self, system: str, user: str) -> Any:
        payload = {
            "model": self._model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "text": {"format": {"type": "json_object"}},
        }
        url = f"{self._endpoint}/openai/v1/responses"
        resp = await self._client.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()
        text = _extract_text_output(data)
        if not text.strip():
            raise ValueError("Foundry response contained no output text")
        return json.loads(text)

    async def aclose(self) -> None:
        await self._client.aclose()


def _extract_text_output(payload: dict) -> str:
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content.get("text", "")
    raise ValueError("No text output found in response")


def _normalize_action_payload(payload: Any) -> dict:
    if isinstance(payload, dict):
        if "type" in payload:
            if payload.get("type") == "fetch":
                payload = {**payload, "type": "search"}
            if payload.get("type") == "browse":
                payload = {**payload, "type": "navigate"}
            if payload.get("type") == "goto":
                payload = {**payload, "type": "navigate"}
            return payload
        if "action" in payload:
            normalized = {"type": payload.get("action")}
            if normalized.get("type") == "fetch":
                normalized["type"] = "search"
            if normalized.get("type") == "browse":
                normalized["type"] = "navigate"
            if normalized.get("type") == "goto":
                normalized["type"] = "navigate"
            if "target" in payload:
                normalized["target"] = payload.get("target")
            if "value" in payload:
                normalized["value"] = payload.get("value")
            if "reason" in payload:
                normalized["reason"] = payload.get("reason")
            if isinstance(payload.get("payload"), dict):
                normalized.update(payload["payload"])
            return normalized
    raise ValueError("Invalid action payload returned by model")
