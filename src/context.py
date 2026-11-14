"""Context selection + evaluation helpers.

Context budget unit: characters of the packed context string (headers included);
approx tokens ~= chars / 4 for English. Chunks are taken in rank order, de-duplicated,
optionally followed by their neighbours (previous/next chunk in the same section),
and skipped (not truncated) when they do not fit, so every kept chunk is verbatim.
"""
from __future__ import annotations

import re


def alias(chunk_id: str) -> str:
    """Short citation id shown to the model: 'openstax-intro-python:B:para800:p0095:c01' -> 'p0095:c01'."""
    return ":".join(chunk_id.split(":")[-2:])


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def is_hit(chunk: dict, gold: list[dict]) -> bool:
    return any(chunk["source_id"] == g["source_id"] and chunk["page"] == g["page"]
               and norm(g["evidence"]) in norm(chunk["text"]) for g in gold)


def block(c: dict) -> str:
    md = c["metadata"]
    return f"[{alias(c['id'])}] (page {c['page']}, ch.{md['chapter']} §{md['section']} {md['section_title']})\n{c['text']}"


class ContextPacker:
    def __init__(self, chunks: list[dict]):
        self.by_order = {c["metadata"]["order"]: c for c in chunks}

    def neighbours(self, c: dict) -> list[dict]:
        o = c["metadata"]["order"]
        out = []
        for j in (o - 1, o + 1):
            n = self.by_order.get(j)
            if n and n["metadata"]["section"] == c["metadata"]["section"]:
                out.append(n)
        return out

    def pack(self, ranked: list[dict], top_k: int, budget: int, neighbours: bool = False) -> tuple[str, list[dict]]:
        chosen: list[dict] = []
        seen: set[str] = set()
        used = 0
        order: list[dict] = []
        for c in ranked[:top_k]:
            order.append(c)
            if neighbours:
                order.extend(self.neighbours(c))
        for c in order:
            if c["id"] in seen:
                continue
            b = block(c)
            extra = len(b) + (2 if chosen else 0)
            if used + extra > budget:
                continue
            seen.add(c["id"])
            chosen.append(c)
            used += extra
        if neighbours:   # present neighbours in reading order next to their anchor
            chosen.sort(key=lambda c: c["metadata"]["order"])
        return "\n\n".join(block(c) for c in chosen), chosen
