"""Run retrieval metrics + the agent for advanced configs on one split.

Gold is used only AFTER each run (page-hit metrics, review sheet). Outputs:
advanced/results/<split>/<config>/{traces.json, summary.json, review_sheet.md}

Usage: python advanced/src/run.py --split dev --configs V0_text_dense V11_agent41_verify41_guard
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "advanced" / "src"))
from rag import Agent, Config, Retriever, load_chunks  # noqa: E402

from src.llm import LLM  # noqa: E402

CONFIGS = {
    # first round (dev)
    "V0_text_dense": Config("V0_text_dense", method="dense", kinds=("text",)),
    "V1_mm_hybrid": Config("V1_mm_hybrid", method="hybrid"),
    "V2_mm_hybrid_view": Config("V2_mm_hybrid_view", method="hybrid", view_page=True),
    "V3_mm_dense_view": Config("V3_mm_dense_view", method="dense", view_page=True),
    "V4_mm_hybrid_view_41": Config("V4_mm_hybrid_view_41", method="hybrid", view_page=True, model="gpt-4.1"),
    # after dev error analysis: figure/table title lookup from the query + prompt v2 (abstain rule, cite named figure)
    "V5_mm_hybrid_title": Config("V5_mm_hybrid_title", method="hybrid", title_lookup=True, prompt_v2=True),
    "V6_mm_hybrid_title_view": Config("V6_mm_hybrid_title_view", method="hybrid", title_lookup=True, prompt_v2=True, view_page=True),
    "V7_mm_hybrid_title_41": Config("V7_mm_hybrid_title_41", method="hybrid", title_lookup=True, prompt_v2=True, model="gpt-4.1"),
    # after test-1 error analysis (evaluated on dev + NEW test2): claim-level verifier on cited passages
    "V8_mm_title_view_verify": Config("V8_mm_title_view_verify", method="hybrid", title_lookup=True, prompt_v2=True, view_page=True,
                                      verify=True, max_turns=14),
    "V9_verify41": Config("V9_verify41", method="hybrid", title_lookup=True, prompt_v2=True, prompt_v3=True, view_page=True,
                          verify=True, verifier_model="gpt-4.1", max_turns=14),
    "V10_agent41_verify41": Config("V10_agent41_verify41", method="hybrid", title_lookup=True, prompt_v2=True, prompt_v3=True,
                                   view_page=True, verify=True, verifier_model="gpt-4.1", model="gpt-4.1", max_turns=14),
    # V10 + robust citation parsing (ids anywhere in the text; valid-but-not-inline ids appended, logged)
    "V11_agent41_verify41_guard": Config("V11_agent41_verify41_guard", method="hybrid", title_lookup=True, prompt_v2=True,
                                         prompt_v3=True, view_page=True, verify=True, verifier_model="gpt-4.1",
                                         model="gpt-4.1", max_turns=14),
    # V11 + standardised abstention text (no speculative claims in refusals)
    "V12_final": Config("V12_final", method="hybrid", title_lookup=True, prompt_v2=True, prompt_v3=True, view_page=True,
                        verify=True, verifier_model="gpt-4.1", model="gpt-4.1", max_turns=14, clean_abstain=True),
    # Gemini (free tier) variant of V12: same pipeline, agent + verifier gemini-2.5-flash, Gemini embeddings (EMB_PROVIDER=gemini)
    "G1_gemini_flash": Config("G1_gemini_flash", method="hybrid", title_lookup=True, prompt_v2=True, prompt_v3=True, view_page=True,
                              verify=True, verifier_model="gemini-2.5-flash", model="gemini-2.5-flash", max_turns=14, clean_abstain=True),
    "G0_gemini_text_dense": Config("G0_gemini_text_dense", method="dense", kinds=("text",), model="gemini-2.5-flash"),
    # Free fallback (OpenAI credit + Gemini embedding quota exhausted; gemini-2.5-flash closed to new users):
    # V12 pipeline with local e5-small embeddings (EMB_PROVIDER=local) and gemini-3.5-flash (free tier) as agent + verifier
    "L1_e5_gemini35": Config("L1_e5_gemini35", method="hybrid", title_lookup=True, prompt_v2=True, prompt_v3=True, view_page=True,
                             verify=True, verifier_model="gemini-3.5-flash", model="gemini-3.5-flash", max_turns=14, clean_abstain=True),
    # gemini-3.5-flash free tier allows only 20 requests/day -> same pipeline on gemini-3.5-flash-lite
    "L2_e5_gemini35lite": Config("L2_e5_gemini35lite", method="hybrid", title_lookup=True, prompt_v2=True, prompt_v3=True, view_page=True,
                                 verify=True, verifier_model="gemini-3.5-flash-lite", model="gemini-3.5-flash-lite", max_turns=14,
                                 clean_abstain=True),
    "L0_e5_text_dense": Config("L0_e5_text_dense", method="dense", kinds=("text",), model="gemini-3.5-flash-lite"),
}


def gold_pages(q: dict) -> set[int]:
    return {g["page"] for g in q.get("gold", [])}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test", "test2"), required=True)
    ap.add_argument("--configs", nargs="+", required=True)
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--out-suffix", default="")
    a = ap.parse_args()
    bench = [q for q in json.loads((ROOT / "advanced" / "benchmark.json").read_text())["questions"] if q["split"] == a.split]
    if a.ids:
        bench = [q for q in bench if q["id"] in a.ids]
    chunks = load_chunks()
    for name in a.configs:
        cfg = CONFIGS[name]
        llm = LLM(model=cfg.model)
        ret = Retriever(chunks, cfg.method, cfg.kinds, title_lookup=cfg.title_lookup)
        agent = Agent(cfg, llm, ret, chunks)
        out = ROOT / "advanced" / "results" / a.split / (name + a.out_suffix)
        out.mkdir(parents=True, exist_ok=True)

        def one(q):
            # retrieval-only ranking for the ORIGINAL question (comparable across configs)
            ranked = ret.search(q["question"], 6)
            r, retried = None, 0
            for attempt in range(2):   # one question-level retry on a system error (logged), never a fake answer
                try:
                    r = agent.run(q["question"])
                    break
                except Exception as exc:  # noqa: BLE001 - report, never fake
                    err = str(exc)[:300]
                    if attempt == 0:
                        retried = 1
                        time.sleep(30)
            if r is None:
                r = {"status": "error", "answer": None, "citations": [], "events": [{"event": "error", "error": err}],
                     "n_searches": 0, "n_views": 0, "context_ids": [], "cited_pages": [], "usage": {}, "cost_usd": 0, "seconds": 0}
            r["question_retries"] = retried
            row = {"query_id": q["id"], "group": q["group"], "split": a.split, "config": name, "model": llm.model,
                   "question": q["question"], "ranking_original_query": [{"rank": c["rank"], "id": c["id"], "page": c["page"]} for c in ranked], **r}
            gp = gold_pages(q)
            if gp:
                pages = [c["page"] for c in ranked]
                row["page_hit1"] = bool(pages[:1] and pages[0] in gp)
                row["page_hit3"] = bool(set(pages[:3]) & gp)
                row["all_gold_pages_top6"] = gp <= set(pages)
                ctx_pages = {ret.by_id[i]["page"] for i in r["context_ids"] if i in ret.by_id}
                row["context_all_gold_pages"] = gp <= ctx_pages
                row["cited_all_gold_pages"] = gp <= set(r["cited_pages"])
            return row

        t0 = time.perf_counter()
        with ThreadPoolExecutor(a.workers) as ex:
            rows = list(ex.map(one, bench))
        ans = [r for r in rows if "page_hit1" in r]
        ok = [r for r in rows if r["status"] != "error"]
        s = {"config": name, "split": a.split, "model": llm.model,
             "settings": {k: (list(v) if isinstance(v, tuple) else v) for k, v in cfg.__dict__.items()},
             "n": len(rows), "errors": len(rows) - len(ok),
             "page_hit1": f"{sum(r['page_hit1'] for r in ans)}/{len(ans)}", "page_hit3": f"{sum(r['page_hit3'] for r in ans)}/{len(ans)}",
             "all_gold_pages_top6": f"{sum(r['all_gold_pages_top6'] for r in ans)}/{len(ans)}",
             "context_all_gold_pages": f"{sum(r['context_all_gold_pages'] for r in ans)}/{len(ans)}",
             "cited_all_gold_pages": f"{sum(r['cited_all_gold_pages'] for r in ans)}/{len(ans)}",
             "answered": sum(r["status"] == "answered" for r in rows), "abstained": sum(r["status"] == "abstain" for r in rows),
             "abstain_on_unanswerable": f"{sum(r['status']=='abstain' for r in rows if r['group']=='unanswerable')}/{sum(r['group']=='unanswerable' for r in rows)}",
             "abstain_on_answerable": f"{sum(r['status']=='abstain' for r in ans)}/{len(ans)}",
             "searches_mean": round(statistics.mean(r["n_searches"] for r in ok), 2) if ok else None,
             "views_mean": round(statistics.mean(r["n_views"] for r in ok), 2) if ok else None,
             "tokens_in": sum(r["usage"].get("in", 0) for r in ok), "tokens_out": sum(r["usage"].get("out", 0) for r in ok),
             "verifier_tokens_in": sum(r["usage"].get("verifier_in", 0) for r in ok),
             "verifier_tokens_out": sum(r["usage"].get("verifier_out", 0) for r in ok),
             "cost_usd_llm": round(sum(r["cost_usd"] for r in ok), 4), "embedding_query_tokens": ret.emb_tokens,
             "median_seconds": statistics.median(r["seconds"] for r in ok) if ok else None, "wall_seconds": round(time.perf_counter() - t0, 1)}
        (out / "traces.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
        (out / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=1))
        sheet(out, bench, rows, ret)
        print(json.dumps({k: v for k, v in s.items() if k != "settings"}, ensure_ascii=False))


def sheet(out: Path, bench: list[dict], rows: list[dict], ret: Retriever) -> None:
    qm = {q["id"]: q for q in bench}
    L = ["# Review sheet (gold shown to the reviewer only)\n"]
    for r in rows:
        q = qm[r["query_id"]]
        L.append(f"## {r['query_id']} [{q['group']}] status={r['status']} ({r.get('reason')})  searches={r['n_searches']} views={r['n_views']}")
        L.append(f"**Q:** {q['question']}  \n**Expected:** {q.get('expected_answer') or 'ABSTAIN — ' + q.get('absence_reason', '')}  ")
        if q.get("gold"):
            L.append("**Gold:** " + "; ".join(f"p.{g['page']} {g['region']}" for g in q["gold"]) + "  ")
        L.append(f"**Queries:** {[e.get('query') for e in r['events'] if e['event']=='search']}  views={[e.get('page') for e in r['events'] if e['event']=='view_page']}  ")
        L.append(f"**Verifier:** {[(e['verdict'], e['problems']) for e in r['events'] if e['event']=='verify']}  ")
        L.append(f"**Answer:** {r.get('answer')}  ")
        for c in r["citations"]:
            ch = ret.by_id.get(c)
            L.append(f"> [{c}] p.{ch['page'] if ch else '?'} {ch['etype'] if ch else ''} {ch['title'][:80] if ch else ''}: "
                     f"{(ch['text'][:300].replace(chr(10), ' ') if ch else 'UNKNOWN')}")
        L.append("")
    (out / "review_sheet.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
