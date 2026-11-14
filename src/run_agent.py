"""Run the real agent on a split for one or more configurations.

Gold is used ONLY after the agent finished, to compute Context Evidence Rate and to
build a review sheet for manual grading. Outputs under results/agent/<split>/<config>/:
  traces.json (agent_metrics format + full trace), cases.json, auto_summary.json, review_sheet.md

Usage:
  python -m src.run_agent --split dev --configs A0_dense A1_hybrid A2_rerank
  python -m src.run_agent --split dev --configs A1_hybrid --ids q05 q10   # subset for debugging
"""
from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter

from .agent import Agent, AgentConfig
from .config import BENCHMARK_FILE, RESULTS_DIR
from .context import alias, is_hit
from .llm import LLM, LLMError
from .retrieval import build_retrievers, load_chunks

AGENT_CONFIGS = {
    "A0_dense": AgentConfig("A0_dense", method="dense", top_k=3, call_budget=1500, max_searches=2,
                            notes="Baseline: dense Day 6 tool, top-3/1500 chars per call, <=2 searches."),
    "A1_hybrid": AgentConfig("A1_hybrid", method="hybrid", top_k=5, call_budget=2500, max_searches=3,
                             notes="Hybrid RRF tool, top-5/2500 chars, <=3 searches (best offline retrieval config I1)."),
    "A2_rerank": AgentConfig("A2_rerank", method="hybrid_rerank", top_k=4, call_budget=2000, max_searches=3,
                             notes="Hybrid + LLM rerank, top-4/2000 chars, <=3 searches."),
    "A3_hybrid_nb": AgentConfig("A3_hybrid_nb", method="hybrid", top_k=5, call_budget=2500, max_searches=3,
                                neighbors_tool=True, max_turns=8,
                                notes="A1 + read_neighbors tool to complete examples/conditions."),
    # Improvement after dev error analysis (12/25 false abstentions = answers without inline [id]):
    "A4_dense_fix": AgentConfig("A4_dense_fix", method="dense", top_k=3, call_budget=1500, max_searches=2,
                                prompt="v2", guard_retries=1, notes="A0 + inline-citation prompt + 1 guard retry with error feedback."),
    "A5_hybrid_fix": AgentConfig("A5_hybrid_fix", method="hybrid", top_k=5, call_budget=2500, max_searches=3,
                                 prompt="v2", guard_retries=1, notes="A1 + inline-citation prompt + 1 guard retry with error feedback."),
    "A6_rerank_fix": AgentConfig("A6_rerank_fix", method="hybrid_rerank", top_k=4, call_budget=2000, max_searches=3,
                                 prompt="v2", guard_retries=1, notes="A2 + inline-citation prompt + 1 guard retry."),
    # Post-test fix (test n06: model passed chapter=4 for a chapter-6 question). Evaluated on dev + NEW test2.
    "A7_dense_userfilter": AgentConfig("A7_dense_userfilter", method="dense", top_k=3, call_budget=1500, max_searches=2,
                                       prompt="v2", guard_retries=1, model_filter=False,
                                       notes="A4 without the model-chosen chapter filter (filter only from the user)."),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test", "test2"), required=True)
    ap.add_argument("--configs", nargs="+", required=True)
    ap.add_argument("--ids", nargs="*")
    a = ap.parse_args()
    bench = [q for q in json.loads(BENCHMARK_FILE.read_text(encoding="utf-8"))["questions"] if q["split"] == a.split]
    if a.ids:
        bench = [q for q in bench if q["id"] in a.ids]
    chunks = load_chunks()
    by_alias = {alias(c["id"]): c for c in chunks}
    llm = LLM()
    methods = sorted({AGENT_CONFIGS[c].method for c in a.configs})
    retrievers = build_retrievers(chunks, methods, llm)
    for cname in a.configs:
        cfg = AGENT_CONFIGS[cname]
        agent = Agent(cfg, llm, retrievers[cfg.method], chunks)
        out_dir = RESULTS_DIR / "agent" / a.split / cname
        out_dir.mkdir(parents=True, exist_ok=True)
        traces = []
        for q in bench:      # agent sees only question + user-supplied filter
            try:
                r = agent.run(q["question"], q.get("filter"))
            except Exception as exc:  # noqa: BLE001 - record per-question failure, never fake a result
                kind = "provider" if isinstance(exc, LLMError) else type(exc).__name__
                r = {"status": "error", "answer": None, "citations": [], "events": [{"event": "error", "kind": kind, "error": str(exc)[:300]}],
                     "n_searches": 0, "context_ids": [], "context_chars": 0, "context": "", "usage": {}, "cost_usd": 0, "seconds": 0}
            row = {"query_id": q["id"], "split": a.split, "config": cname, "model": f"{llm.provider}/{llm.model}",
                   "question": q["question"], "filter": q.get("filter"), **r}
            if q["answerable"] and r["status"] != "error":      # post-hoc evaluation only
                ctx = [by_alias[i] for i in r["context_ids"] if i in by_alias]
                row["context_hit"] = any(is_hit(c, q["gold"]) for c in ctx)
                row["cited_gold"] = any(is_hit(by_alias[i], q["gold"]) for i in r["citations"] if i in by_alias)
            traces.append(row)
            print(f"[{cname}] {q['id']:4s} {r['status']:8s} searches={r['n_searches']} cites={r['citations']} "
                  f"ctx_hit={row.get('context_hit')} {r['seconds']}s ${r['cost_usd']}")
        cases = [{"id": q["id"], "split": q["split"], "answerable": q["answerable"]} for q in bench]
        ok = [t for t in traces if t["status"] != "error"]
        ans = [t for t in ok if t["query_id"] in {q["id"] for q in bench if q["answerable"]}]
        una = [t for t in ok if t not in ans]
        summary = {
            "config": cname, "split": a.split, "model": f"{llm.provider}/{llm.model}", "settings": cfg.__dict__,
            "n": len(traces), "errors": len(traces) - len(ok),
            "tool_use": f"{sum(any(e['event']=='search' for e in t['events']) for t in ok)}/{len(ok)}",
            "searches_distribution": dict(sorted(Counter(t["n_searches"] for t in ok).items())),
            "status": dict(Counter(t["status"] for t in traces)),
            "context_evidence_rate": f"{sum(t.get('context_hit', False) for t in ans)}/{len(ans)}",
            "answered_with_gold_citation": f"{sum(t.get('cited_gold', False) for t in ans)}/{len(ans)}",
            "false_abstain_auto": f"{sum(t['status']=='abstain' for t in ans)}/{len(ans)}",
            "abstain_on_unanswerable_auto": f"{sum(t['status']=='abstain' for t in una)}/{len(una)}",
            "guard_rejections": sum(e["event"] == "invalid_or_missing_citations" for t in ok for e in t["events"]),
            "abstain_without_search": sum(t["status"] == "abstain" and t["n_searches"] == 0 for t in ok),
            "search_limit_hits": sum(e["event"] == "search_limit" for t in ok for e in t["events"]),
            "max_turns_hits": sum(e["event"] == "max_turns" for t in ok for e in t["events"]),
            "rerank_parse_failures": sum(1 for t in ok for e in t["events"] if e.get("rerank") and not e["rerank"].get("parse_ok")),
            "avg_context_chars": round(statistics.mean(t["context_chars"] for t in ok)) if ok else 0,
            "tokens_in": sum(t["usage"].get("in", 0) + t["usage"].get("rerank_in", 0) for t in ok),
            "tokens_out": sum(t["usage"].get("out", 0) + t["usage"].get("rerank_out", 0) for t in ok),
            "cost_usd_total": round(sum(t["cost_usd"] for t in ok), 5), "price_known": llm.price_known,
            "median_seconds": statistics.median(t["seconds"] for t in ok) if ok else None,
            "total_seconds": round(sum(t["seconds"] for t in ok), 1),
        }
        (out_dir / "traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (out_dir / "cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (out_dir / "auto_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        write_review_sheet(out_dir, bench, traces, chunks)
        print(json.dumps({k: v for k, v in summary.items() if k != "settings"}, ensure_ascii=False, indent=1))


def write_review_sheet(out_dir, bench, traces, chunks) -> None:
    """Human review aid: question, expected answer, agent answer, and full text of each citation."""
    by_alias = {":".join(c["id"].split(":")[-2:]): c for c in chunks}
    qmap = {q["id"]: q for q in bench}
    lines = ["# Review sheet (grade manually; gold shown for the reviewer only)\n"]
    for t in traces:
        q = qmap[t["query_id"]]
        lines.append(f"## {t['query_id']} — {'answerable' if q['answerable'] else 'UNANSWERABLE'} — status: {t['status']}")
        lines.append(f"**Q:** {q['question']}  ")
        lines.append(f"**Expected:** {q.get('expected_answer') or q.get('absence_reason')}  ")
        lines.append(f"**Queries:** {[e.get('query') for e in t['events'] if e['event']=='search']}  ")
        lines.append(f"**Answer:** {t.get('answer')}  ")
        if t.get("rejected_answer"):
            lines.append(f"**Rejected (citation guard):** {t['rejected_answer']}  ")
        for cid in t["citations"]:
            c = by_alias.get(cid)
            lines.append(f"> [{cid}] p.{c['page'] if c else '?'}: {c['text'][:500].replace(chr(10), ' ') if c else 'UNKNOWN'}")
        lines.append("")
    (out_dir / "review_sheet.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
