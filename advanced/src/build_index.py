"""Build the multimodal index for MCS 2024 from advanced/extracted/.

Chunks (advanced/index/chunks.json):
  text   p{page}-t{n}: PyMuPDF text of the page, sentence-packed windows of <=1000 chars (150 overlap)
  visual p{page}-v{n}[a,b..]: one per table/chart/map/diagram/photo from the vision layer; long tables are
         split by rows with the title + header repeated (<=3500 chars per part)
Every chunk carries page, printed_page, section (commodity/chapter heading), kind, element type/title and
a link to the rendered page image (advanced/pages/pNNN.png) for verification.

Embeddings: OpenAI text-embedding-3-small (1536 d) of "[section | page] + chunk text", stored in a
Chroma PersistentClient collection `mcs2024` (cosine) at advanced/index/chroma.

Usage: python advanced/src/build_index.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "advanced" / "src"))
from src.config import load_dotenv  # noqa: E402
from src.llm import _SSL  # noqa: E402

EXT = ROOT / "advanced" / "extracted"
IDX = ROOT / "advanced" / "index"
EMB_MODEL = "text-embedding-3-small"
EMB_PRICE = 0.02  # USD / 1M tokens

_SKIP = re.compile(r"^(U\.S\. Geological Survey|Prepared by|\d+)$")


def section_of(text: str, page: int) -> str:
    for line in text.splitlines()[:6]:
        s = line.strip()
        if s and s.isupper() and len(s) > 3 and "U.S." not in s and not s.startswith("("):
            return s.rstrip("0123456789")
    if page <= 33:
        return "General / introduction"
    return "Appendix" if page >= 211 else ""


def printed(page: int) -> int | None:
    return page - 4 if page >= 5 else None


def text_chunks(page: int, text: str, section: str) -> list[dict]:
    lines = [l.strip() for l in text.splitlines() if l.strip() and not _SKIP.match(l.strip())]
    flat = re.sub(r"\s+", " ", " ".join(lines)).replace("­", "")
    if len(flat) < 40:
        return []
    sents = re.split(r"(?<=[.;:])\s+", flat)
    out, cur = [], ""
    for s in sents:
        if len(cur) + len(s) > 1000 and cur:
            out.append(cur.strip())
            cur = cur[-150:] + " " + s
        else:
            cur += " " + s
    if cur.strip():
        out.append(cur.strip())
    return [{"id": f"p{page:03d}-t{i}", "kind": "text", "page": page, "printed_page": printed(page),
             "section": section, "etype": "text", "title": "", "text": t} for i, t in enumerate(out, 1)]


def visual_chunks(page: int, rec: dict, section: str) -> list[dict]:
    out = []
    for i, e in enumerate(rec.get("elements", []), 1):
        content = e.get("content")
        content = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
        head = f"{e.get('type', '?').upper()}: {e.get('title', '')}\nLocation on page: {e.get('location', '')}"
        notes = e.get("notes")
        notes = notes if isinstance(notes, str) else (json.dumps(notes, ensure_ascii=False) if notes else "")
        body = content + (f"\nNotes: {notes}" if notes else "")
        parts = [body]
        if len(body) > 3500:
            rows, parts, cur = body.splitlines(), [], ""
            header = "\n".join(rows[:3]) if rows and rows[0].lstrip().startswith("|") else ""
            for r in rows:
                if len(cur) + len(r) > 3300 and cur:
                    parts.append(cur)
                    cur = (header + "\n" if header else "") + "(continued)\n"
                cur += r + "\n"
            parts.append(cur)
        for j, p in enumerate(parts):
            cid = f"p{page:03d}-v{i}" + (chr(97 + j) if len(parts) > 1 else "")
            out.append({"id": cid, "kind": "visual", "page": page, "printed_page": printed(page), "section": section,
                        "etype": e.get("type", "?"), "title": e.get("title", ""), "location": e.get("location", ""),
                        "text": head + "\n" + p})
    return out


def embed(texts: list[str]) -> tuple[list[list[float]], int]:
    from emb import embed as _embed
    return _embed(texts)


def embed_input(c: dict) -> str:
    return f"[{c['section']} | page {c['page']} | {c['etype']} {c['title']}]\n{c['text']}"[:24000]


def main() -> None:
    import chromadb

    t0 = time.perf_counter()
    pages = json.loads((EXT / "text_pages.json").read_text())
    chunks: list[dict] = []
    missing = []
    for p in pages:
        sec = section_of(p["text"], p["page"])
        chunks += text_chunks(p["page"], p["text"], sec)
        vf = EXT / "vision" / f"p{p['page']:03d}.json"
        if vf.exists():
            rec = json.loads(vf.read_text())
            if not rec.get("parse_ok"):
                missing.append(p["page"])
            chunks += visual_chunks(p["page"], rec, sec)
        else:
            missing.append(p["page"])
    IDX.mkdir(parents=True, exist_ok=True)
    vecs, tokens = embed([embed_input(c) for c in chunks])
    client = chromadb.PersistentClient(path=str(IDX / "chroma"))
    from emb import settings
    es = settings()
    try:
        client.delete_collection(es["collection"])
    except Exception:  # noqa: BLE001 - collection may not exist yet
        pass
    col = client.create_collection(es["collection"], embedding_function=None,
                                   metadata={"hnsw:space": "cosine", "embedding_model": es["model"], "dimensions": len(vecs[0])})
    for i in range(0, len(chunks), 500):
        b = chunks[i:i + 500]
        col.add(ids=[c["id"] for c in b], embeddings=vecs[i:i + 500], documents=[c["text"] for c in b],
                metadatas=[{"page": c["page"], "kind": c["kind"], "etype": c["etype"], "section": c["section"]} for c in b])
    (IDX / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=0))
    stats = {"chunks": len(chunks), "text_chunks": sum(c["kind"] == "text" for c in chunks),
             "visual_chunks": sum(c["kind"] == "visual" for c in chunks),
             "visual_by_type": {t: sum(c["etype"] == t for c in chunks if c["kind"] == "visual")
                                for t in sorted({c["etype"] for c in chunks if c["kind"] == "visual"})},
             "pages_with_text_chunks": len({c["page"] for c in chunks if c["kind"] == "text"}),
             "pages_with_visual_chunks": len({c["page"] for c in chunks if c["kind"] == "visual"}),
             "vision_missing_or_unparsed_pages": missing, "embedding_provider": es["provider"], "embedding_model": es["model"], "dimensions": len(vecs[0]),
             "embedding_tokens": tokens, "embedding_cost_usd_openai_list_price": round(tokens * EMB_PRICE / 1e6, 4) if es["provider"] == "openai" else 0.0,
             "seconds": round(time.perf_counter() - t0, 1)}
    (IDX / f"index_stats_{es['provider']}.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
