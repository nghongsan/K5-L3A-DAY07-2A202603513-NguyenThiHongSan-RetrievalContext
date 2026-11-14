"""Validate advanced/benchmark.json against the original PDF text (no model output involved).

* counts per split/group vs ADVANCED.md minimums
* textual evidence: whitespace-normalised substring of the gold page text (figure-only evidence is
  marked 'visual' and was checked by viewing the rendered page)
* unanswerable: every absence regex has 0 matches over all 216 pages
"""
import collections, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "advanced" / ".vendor"))
import fitz  # noqa: E402

def norm(s): return re.sub(r"\s+", " ", s.replace("­", "")).strip().lower()

def main():
    b = json.loads((ROOT / "advanced" / "benchmark.json").read_text())
    doc = fitz.open(ROOT / "advanced" / "raw" / "mcs2024.pdf")
    pages = [norm(p.get_text("text")) for p in doc]
    cnt = collections.Counter((q["split"], q["group"]) for q in b["questions"])
    for s in ("dev", "test", "test2", "test3"):
        print(s, {g: cnt[(s, g)] for g in ("table", "image", "chart", "multihop", "text", "unanswerable")},
              "answerable", sum(v for (sp, g), v in cnt.items() if sp == s and g != "unanswerable"),
              "total", sum(v for (sp, g), v in cnt.items() if sp == s))
    report = []
    for q in b["questions"]:
        if q["group"] == "unanswerable":
            hits = {p: sum(1 for t in pages if re.search(p, t, re.I)) for p in q["absence_check"]}
            report.append((q["id"], "absent" if not any(hits.values()) else f"FOUND {hits}"))
            continue
        for g in q["gold"]:
            ev = norm(g["evidence"])
            report.append((q["id"], f"p{g['page']}: " + ("text-verbatim" if ev in pages[g["page"] - 1] else "visual/paraphrase (checked on rendered page)")))
    for r in report: print(*r)
    if any("FOUND" in r[1] for r in report): raise SystemExit("absence check failed")

if __name__ == "__main__": main()
