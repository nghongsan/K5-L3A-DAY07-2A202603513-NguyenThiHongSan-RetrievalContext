"""Embedding provider for the advanced index (OpenAI or Gemini, OpenAI-compatible endpoints).

EMB_PROVIDER=openai -> text-embedding-3-small, collection `mcs2024`
EMB_PROVIDER=gemini -> gemini-embedding-001 (GEMINI_API_KEY), collection `mcs2024_gemini`
EMB_PROVIDER=local  -> intfloat/multilingual-e5-small on this machine (free, no quota; the Day 6 model),
                       "query: "/"passage: " prefixes, normalised, collection `mcs2024_e5`. Inputs are truncated
                       at 512 tokens by the model (long table parts are still fully indexed by BM25).
Retries on 429/5xx with backoff (free tiers are rate limited). Keys are never logged.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.config import load_dotenv  # noqa: E402
from src.llm import _SSL  # noqa: E402

PROVIDERS = {
    "openai": ("OPENAI_API_KEY", "https://api.openai.com/v1/embeddings", "text-embedding-3-small", "mcs2024", 96),
    "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/embeddings",
               "gemini-embedding-001", "mcs2024_gemini", 50),
    "local": (None, None, "intfloat/multilingual-e5-small", "mcs2024_e5", 64),
}
_LOCAL = {}


def _local_model(name: str):
    if name not in _LOCAL:
        from sentence_transformers import SentenceTransformer
        _LOCAL[name] = SentenceTransformer(name, device="cpu")
    return _LOCAL[name]


def settings() -> dict:
    load_dotenv()
    p = os.getenv("EMB_PROVIDER", "openai")
    key_name, url, model, collection, batch = PROVIDERS[p]
    return {"provider": p, "key_name": key_name, "url": url, "model": os.getenv("EMB_MODEL", model),
            "collection": collection, "batch": batch}


def embed(texts: list[str], retries: int = 6, query: bool = False) -> tuple[list[list[float]], int]:
    s = settings()
    if s["provider"] == "local":
        m = _local_model(s["model"])
        prefix = "query: " if query else "passage: "
        inp = [prefix + t for t in texts]
        vecs = m.encode(inp, batch_size=s["batch"], normalize_embeddings=True, show_progress_bar=len(texts) > 100)
        tokens = sum(len(m.tokenizer(t, truncation=True, max_length=512)["input_ids"]) for t in inp)
        return [v.tolist() for v in vecs], tokens
    key = os.environ.get(s["key_name"])
    if not key:
        raise RuntimeError(f"Missing {s['key_name']}")
    vecs, tokens = [], 0
    for i in range(0, len(texts), s["batch"]):
        body = json.dumps({"model": s["model"], "input": texts[i:i + s["batch"]]}).encode()
        for attempt in range(retries + 1):
            req = urllib.request.Request(s["url"], data=body, headers={"Authorization": f"Bearer {key}",
                                                                      "Content-Type": "application/json"})
            try:
                d = json.load(urllib.request.urlopen(req, context=_SSL, timeout=120))
                break
            except urllib.error.HTTPError as exc:
                if exc.code in (429, 500, 502, 503, 504) and attempt < retries:
                    time.sleep(min(65, 5 * 2 ** attempt))
                    continue
                raise RuntimeError(f"Embedding HTTP {exc.code}") from exc
        vecs += [x["embedding"] for x in sorted(d["data"], key=lambda x: x.get("index", 0))]
        tokens += (d.get("usage") or {}).get("total_tokens", 0) or (d.get("usage") or {}).get("prompt_tokens", 0)
    return vecs, tokens
