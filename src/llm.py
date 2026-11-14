"""Real LLM provider with tool calling (standard library only).

Configure with environment variables (or a git-ignored .env):
  LLM_PROVIDER = openai | gemini | openrouter | anthropic
  LLM_MODEL    = model id supporting tool calling (e.g. gpt-4o-mini, gemini-2.5-flash)
  <PROVIDER>_API_KEY = the key (OPENAI_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY)
  LLM_PRICE_IN / LLM_PRICE_OUT = optional USD per 1M tokens to estimate cost.

Errors are raised, never replaced by a fake answer. Keys are never logged.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request

from .config import load_dotenv

PROVIDERS = {
    "openai": ("OPENAI_API_KEY", "https://api.openai.com/v1/chat/completions"),
    "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"),
    "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions"),
    "anthropic": ("ANTHROPIC_API_KEY", "https://api.anthropic.com/v1/messages"),
}

# Public list prices (USD / 1M tokens) used only for estimates; override with env vars.
DEFAULT_PRICES = {
    "gpt-4o-mini": (0.15, 0.60), "gpt-4.1-mini": (0.40, 1.60), "gpt-4.1-nano": (0.10, 0.40), "gpt-4.1": (2.00, 8.00),
    "gemini-2.5-flash": (0.30, 2.50), "gemini-2.0-flash": (0.10, 0.40), "gemini-2.5-flash-lite": (0.10, 0.40),
    "claude-haiku-5-5": (1.00, 5.00),
}


class LLMError(RuntimeError):
    pass


def _ssl_context() -> ssl.SSLContext:
    """Use certifi's CA bundle when available (python.org macOS builds ship without system CAs)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


_SSL = _ssl_context()


def _post(url: str, headers: dict, payload: dict, retries: int = 5) -> dict:
    data = json.dumps(payload).encode()
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=90, context=_SSL) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            # Retry rate limits / transient server errors; never echo the body (may contain account data).
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries:
                ra = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    wait = float(ra) + 1 if ra else min(60, 5 * 2 ** attempt)
                except ValueError:
                    wait = min(60, 5 * 2 ** attempt)
                time.sleep(wait)
                continue
            raise LLMError(f"Provider HTTP {exc.code}; check model name, key and quota.") from exc
        except urllib.error.URLError as exc:
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise LLMError(f"Cannot reach provider: {exc.reason}") from exc
    raise LLMError("unreachable")


class LLM:
    """chat(messages, tools) -> {'text', 'calls': [{'id','name','args'}], 'usage': {'in','out'}}.

    `messages` use the OpenAI Chat Completions format; assistant messages returned in
    `raw_message` must be appended unchanged before tool results.
    """

    def __init__(self, provider: str | None = None, model: str | None = None, temperature: float = 0.0):
        load_dotenv()
        self.provider = provider or os.getenv("LLM_PROVIDER", "openai")
        self.model = model or os.getenv("LLM_MODEL")
        if self.provider not in PROVIDERS:
            raise LLMError(f"Unknown LLM_PROVIDER {self.provider!r}")
        if not self.model:
            raise LLMError("Set LLM_MODEL to a model with tool calling.")
        key_name, self.url = PROVIDERS[self.provider]
        self._key = os.getenv(key_name)
        if not self._key:
            raise LLMError(f"Missing {key_name} (set it in .env, never commit it).")
        self.temperature = temperature
        base = self.model.split("/")[-1]
        price = DEFAULT_PRICES.get(base, (None, None))
        self.price_in = float(os.getenv("LLM_PRICE_IN", price[0] if price[0] is not None else 0))
        self.price_out = float(os.getenv("LLM_PRICE_OUT", price[1] if price[1] is not None else 0))
        self.price_known = price[0] is not None or bool(os.getenv("LLM_PRICE_IN"))

    def cost(self, usage: dict) -> float:
        return (usage.get("in", 0) * self.price_in + usage.get("out", 0) * self.price_out) / 1e6

    def chat(self, messages: list[dict], tools: list[dict] | None = None, max_tokens: int = 1024) -> dict:
        if self.provider == "anthropic":
            return self._anthropic(messages, tools or [], max_tokens)
        payload = {"model": self.model, "messages": messages, "temperature": self.temperature, "max_tokens": max_tokens}
        if self.provider == "gemini" and re.search(r"gemini-(2\.5|[3-9])", self.model):
            # Gemini 2.5+ counts thinking tokens against max_tokens; keep reasoning bounded and leave room for the answer.
            payload["reasoning_effort"] = os.getenv("LLM_REASONING_EFFORT", "low")
            payload["max_tokens"] = max_tokens + 3000
        if tools:
            payload["tools"] = tools
        data = _post(self.url, {"Authorization": f"Bearer {self._key}"}, payload)
        try:
            msg = data["choices"][0]["message"]
        except (KeyError, IndexError) as exc:
            raise LLMError("Malformed provider response (no choices).") from exc
        calls = []
        for c in msg.get("tool_calls") or []:
            try:
                args = json.loads(c["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {"_parse_error": c["function"].get("arguments")}
            calls.append({"id": c["id"], "name": c["function"]["name"], "args": args})
        usage = data.get("usage") or {}
        raw = {"role": "assistant", "content": msg.get("content")}
        if msg.get("tool_calls"):
            raw["tool_calls"] = msg["tool_calls"]
        return {"text": msg.get("content") or "", "calls": calls, "raw_message": raw,
                "usage": {"in": usage.get("prompt_tokens", 0), "out": usage.get("completion_tokens", 0)}}

    def _anthropic(self, messages: list[dict], tools: list[dict], max_tokens: int) -> dict:
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        native: list[dict] = []
        for m in messages:
            if m["role"] == "system":
                continue
            if m["role"] == "assistant":
                blocks = [{"type": "text", "text": m["content"]}] if m.get("content") else []
                for c in m.get("tool_calls", []):
                    blocks.append({"type": "tool_use", "id": c["id"], "name": c["function"]["name"],
                                   "input": json.loads(c["function"]["arguments"] or "{}")})
                native.append({"role": "assistant", "content": blocks})
            elif m["role"] == "tool":
                block = {"type": "tool_result", "tool_use_id": m["tool_call_id"], "content": m["content"]}
                if native and native[-1]["role"] == "user" and isinstance(native[-1]["content"], list):
                    native[-1]["content"].append(block)
                else:
                    native.append({"role": "user", "content": [block]})
            else:
                native.append({"role": "user", "content": m["content"]})
        payload = {"model": self.model, "max_tokens": max_tokens, "system": system, "messages": native,
                   "temperature": self.temperature}
        if tools:
            payload["tools"] = [{"name": t["function"]["name"], "description": t["function"]["description"],
                                 "input_schema": t["function"]["parameters"]} for t in tools]
        data = _post(self.url, {"x-api-key": self._key, "anthropic-version": "2023-06-01"}, payload)
        blocks = data.get("content", [])
        calls = [{"id": b["id"], "name": b["name"], "args": b["input"]} for b in blocks if b["type"] == "tool_use"]
        text = "\n".join(b["text"] for b in blocks if b["type"] == "text")
        raw = {"role": "assistant", "content": text or None}
        if calls:
            raw["tool_calls"] = [{"id": c["id"], "type": "function",
                                  "function": {"name": c["name"], "arguments": json.dumps(c["args"], ensure_ascii=False)}}
                                 for c in calls]
        u = data.get("usage", {})
        return {"text": text, "calls": calls, "raw_message": raw,
                "usage": {"in": u.get("input_tokens", 0), "out": u.get("output_tokens", 0)}}
