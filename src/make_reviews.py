"""Expand manual labels (results/reviews/manual_labels_<split>.json) into the reviews.json
format of starter/agent_metrics.py, then run the aggregation for each labelled config.

Usage:  python -m src.make_reviews --split dev
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

from .config import BENCHMARK_FILE, RESULTS_DIR, ROOT


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test", "test2"), required=True)
    a = ap.parse_args()
    labels = json.loads((RESULTS_DIR / "reviews" / f"manual_labels_{a.split}.json").read_text(encoding="utf-8"))
    answerable = {q["id"]: q["answerable"] for q in json.loads(BENCHMARK_FILE.read_text(encoding="utf-8"))["questions"]}
    for cfg, lab in labels.items():
        if cfg.startswith("_"):
            continue
        tdir = RESULTS_DIR / "agent" / a.split / cfg
        traces = json.loads((tdir / "traces.json").read_text(encoding="utf-8"))
        reviews = []
        for t in traces:
            if t["status"] == "error":
                continue
            qid = t["query_id"]
            bad = set(lab.get("unsupported_citations", {}).get(qid, []))
            r = {"query_id": qid, "citation_support": [c not in bad for c in t["citations"]],
                 "note": lab.get("notes", {}).get(qid, "")}
            if answerable[qid]:
                r["answer_grade"] = lab.get("grades", {}).get(qid, 2 if t["status"] == "answered" else 0)
            else:
                r["abstention_correct"] = lab.get("abstention", {}).get(qid, t["status"] == "abstain")
            reviews.append(r)
        out = RESULTS_DIR / "reviews" / f"{a.split}_{cfg}.json"
        out.write_text(json.dumps(reviews, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        subprocess.run([sys.executable, str(ROOT / "starter" / "agent_metrics.py"), "--cases", str(tdir / "cases.json"),
                        "--traces", str(tdir / "traces.json"), "--reviews", str(out), "--split", a.split,
                        "--output", str(tdir / "metrics.json")], check=True, stdout=subprocess.DEVNULL)
        m = json.loads((tdir / "metrics.json").read_text(encoding="utf-8"))
        g = m["grounded_answer"]
        print(f"{cfg:14s} tool {m['tool_use']['n']}/{m['tool_use']['N']}  grounded 0/1/2={g['0']}/{g['1']}/{g['2']} mean={g['mean']:.2f}  "
              f"cite_valid {m['citation_validity']['n']}/{m['citation_validity']['N']}  cite_cov {m['answer_citation_coverage']['n']}/{m['answer_citation_coverage']['N']}  "
              f"abstain {m['abstention']['n']}/{m['abstention']['N']}  false_abst {m['false_abstention']['n']}/{m['false_abstention']['N']}  errors {m['provider_errors']}")


if __name__ == "__main__":
    main()
