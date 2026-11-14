"""Benchmark retrieval + context configurations on one split (no agent).

Metrics (answerable questions only; unanswerable are excluded from the denominator):
  Hit@1, Evidence Hit@3 (top-3 of the ranking, same hit rule for every method), MRR@10,
  Context Evidence Rate = gold evidence chunk is inside the packed context.
Original question text is used as the query (no rewriting here); the user-supplied
chapter filter is applied when present.

Usage:
  python -m src.eval_retrieval --split dev                       # all configs
  python -m src.eval_retrieval --split dev --configs R1_dense I1_hybrid_k5
"""
from __future__ import annotations

import argparse
import json
import statistics
import time

from .config import BENCHMARK_FILE, RESULTS_DIR
from .context import ContextPacker, alias, is_hit
from .retrieval import build_retrievers, load_chunks

# name: (method, top_k for context, budget chars, neighbours, hypothesis)
CONFIGS = {
    "R1_dense": ("dense", 3, 1500, False, "Baseline: Day 6 dense retrieval, top-3, 1500-char budget."),
    "R2_bm25": ("bm25", 3, 1500, False, "Lexical BM25 catches exact code tokens/keywords (e.g. 'elif', '**') that e5 blurs."),
    "R2b_bm25_nostem": ("bm25_nostem", 3, 1500, False, "Ablation: is the light stemmer helping BM25?"),
    "R3_hybrid": ("hybrid", 3, 1500, False, "RRF of dense+BM25 combines paraphrase recall and exact-term precision."),
    "I1_hybrid_k5": ("hybrid", 5, 2500, False, "Improvement 1: evidence often ranks 4-5; larger top-k/budget raises context evidence rate."),
    "I2_hybrid_k5_nb": ("hybrid", 5, 3500, True, "Improvement 2: adding same-section neighbours gives complete examples/conditions."),
    "I3_rerank_k3": ("hybrid_rerank", 3, 1500, False, "Improvement 3: LLM rerank of hybrid top-15 puts the answering passage first (Hit@1) at small budget."),
    "I4_rerank_k5": ("hybrid_rerank", 5, 2500, False, "Rerank + top-5 context."),
}


def run(split: str, names: list[str], out_dir) -> list[dict]:
    bench = json.loads(BENCHMARK_FILE.read_text(encoding="utf-8"))["questions"]
    qs = [q for q in bench if q["split"] == split]
    chunks = load_chunks()
    packer = ContextPacker(chunks)
    methods = sorted({CONFIGS[n][0] for n in names})
    llm = None
    if "hybrid_rerank" in methods:
        from .llm import LLM
        llm = LLM()
    t0 = time.perf_counter()
    retrievers = build_retrievers(chunks, methods, llm)
    load_s = time.perf_counter() - t0
    summaries = []
    for name in names:
        method, top_k, budget, nb, hyp = CONFIGS[name]
        ret = retrievers[method]
        usage0 = dict(getattr(ret, "usage", {})) if hasattr(ret, "usage") else None
        traces = []
        for q in qs:
            t = time.perf_counter()
            ranked = ret.search(q["question"], top_k=10, filters=q.get("filter"))   # same ranking cutoff for every method
            ctx, chosen = packer.pack(ranked, top_k, budget, nb)
            ms = (time.perf_counter() - t) * 1000
            row = {"query_id": q["id"], "split": split, "answerable": q["answerable"], "question": q["question"],
                   "query": q["question"], "filter": q.get("filter"), "config": name, "method": method,
                   "top_k": top_k, "budget_chars": budget, "neighbours": nb,
                   "results": [{"rank": r["rank"], "id": alias(r["id"]), "page": r["page"], "section": r["metadata"]["section"],
                                "score": r["score"], **({"components": r["components"]} if "components" in r else {}),
                                **({"hybrid_rank": r["hybrid_rank"]} if "hybrid_rank" in r else {}),
                                "hit": is_hit(r, q["gold"]) if q["answerable"] else None} for r in ranked],
                   "context_ids": [alias(c["id"]) for c in chosen], "context_chars": len(ctx), "ms": round(ms, 1)}
            if q["answerable"]:
                hits = [is_hit(r, q["gold"]) for r in ranked]
                row["gold"] = q["gold"]
                row["hit1"] = bool(hits[:1] and hits[0])
                row["hit3"] = any(hits[:3])
                first = next((i for i, h in enumerate(hits[:10], 1) if h), None)
                row["rr"] = 1 / first if first else 0.0
                row["context_hit"] = any(is_hit(c, q["gold"]) for c in chosen)
            else:
                row["top1_score"] = ranked[0]["score"] if ranked else None
            if method == "hybrid_rerank":
                row["rerank"] = ret.last_info
            traces.append(row)
        ans = [t for t in traces if t["answerable"]]
        N = len(ans)
        s = {"config": name, "split": split, "method": method, "top_k": top_k, "budget_chars": budget,
             "neighbours": nb, "hypothesis": hyp, "N": N,
             "hit1": sum(t["hit1"] for t in ans), "hit3": sum(t["hit3"] for t in ans),
             "mrr10": round(sum(t["rr"] for t in ans) / N, 3),
             "context_hit": sum(t["context_hit"] for t in ans),
             "avg_context_chars": round(statistics.mean(t["context_chars"] for t in traces)),
             "median_ms": round(statistics.median(t["ms"] for t in traces), 1),
             "misses_hit3": [t["query_id"] for t in ans if not t["hit3"]],
             "misses_context": [t["query_id"] for t in ans if not t["context_hit"]],
             "model_load_s": round(load_s, 2), "cost_usd": 0.0, "llm_tokens": None,
             "rerank_parse_failures": sum(1 for t in traces if t.get("rerank") and not t["rerank"].get("parse_ok")) if method == "hybrid_rerank" else None}
        if usage0 is not None:
            du = {k: ret.usage[k] - usage0.get(k, 0) for k in ("in", "out", "calls")}
            s["llm_tokens"] = du
            s["cost_usd"] = round(llm.cost(du), 5)
            s["llm_model"] = f"{llm.provider}/{llm.model}"
        summaries.append(s)
        (out_dir / f"traces_{name}.json").write_text(json.dumps(traces, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{name:18s} Hit@1 {s['hit1']}/{N}  Hit@3 {s['hit3']}/{N}  MRR {s['mrr10']}  Ctx {s['context_hit']}/{N}  "
              f"chars {s['avg_context_chars']}  {s['median_ms']}ms  ${s['cost_usd']}  miss3={s['misses_hit3']}")
    return summaries


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test", "test2"), required=True)
    ap.add_argument("--configs", nargs="*", default=list(CONFIGS))
    ap.add_argument("--output", default=None)
    a = ap.parse_args()
    out = RESULTS_DIR / "retrieval" / a.split if a.output is None else __import__("pathlib").Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    sums = run(a.split, a.configs, out)
    path = out / "summary.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    merged = {s["config"]: s for s in old}
    merged.update({s["config"]: s for s in sums})
    path.write_text(json.dumps(list(merged.values()), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
