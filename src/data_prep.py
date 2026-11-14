"""Build Day 7 data files from Day 6 artefacts.

* data/chunks.json   : the 263 chunks of Day 6 index `day06_C` in the Day 7 schema.
* data/benchmark.json: Day 7 benchmark (dev = all 25 Day 6 questions + 3 unanswerable;
  test = 6 NEW answerable + 2 unanswerable written for Day 7 before any Day 7 run).

Day 6 test questions (t01-t06) were already seen during Day 6, so they are moved to
dev and a fresh test split is written here (RULES.md: "Nếu đã xem test ... tạo test mới").

Usage:  python -m src.data_prep
"""
from __future__ import annotations

import json
import re

from .config import BENCHMARK_FILE, CHROMA_COLLECTION, CHROMA_PATH, CHUNKS_FILE, DAY6_DIR

SOURCE_ID = "openstax-intro-python"
SOURCE = "OpenStax, Introduction to Python Programming (CC BY-NC-SA 4.0), PDF"

# ---------------------------------------------------------------------------
# New Day 7 test questions, frozen 2026-11-14 BEFORE any Day 7 retrieval/agent run.
# Evidence is copied verbatim from a single chunk on the given physical PDF page.
NEW_TEST = [
    {"id": "n01", "type": "direct", "question": "What does Python's or operator return?",
     "expected_answer": "It takes two condition operands and returns True if either condition is true (False only when both are false).",
     "page": 105, "evidence": "The or operator takes two condition operands and returns True if either"},
    {"id": "n02", "type": "direct", "question": "How many logical operators does Python have, and which are they?",
     "expected_answer": "Three: and, or, and not.",
     "page": 104, "evidence": "Python has three logical operators: and, or, and not."},
    {"id": "n03", "type": "paraphrase",
     "question": "In the miles-per-gallon example, what does the function return when gallons is 0, and why that value?",
     "expected_answer": "It returns -1 (after printing \"Gallons can't be 0\"), a value often used to indicate a problem, to avoid division by zero.",
     "page": 166, "evidence": "if so, returns -1, a value often used to"},
    {"id": "n04", "type": "condition", "question": "What is the difference between a function argument and a function parameter?",
     "expected_answer": "An argument is a value passed as input during a function call; a parameter is the variable representing that input in the function definition.",
     "page": 160, "evidence": "A function argument is a value passed as"},
    {"id": "n05", "type": "condition",
     "question": "When a function that was called by another function finishes, where does control flow go?",
     "expected_answer": "Control flow returns to the calling function.",
     "page": 153, "evidence": "another function finishes execution, control flow returns to the calling function."},
    {"id": "n06", "type": "paraphrase", "question": "Why not simply make every variable global to avoid scope errors?",
     "expected_answer": "Making every variable global makes a program messy: if the whole program can modify a variable, a bug could be anywhere; limiting scope makes programs easier to debug/maintain.",
     "page": 159, "evidence": "every variable global can make a program messy"},
]

# test2: written AFTER the test run (test n06 exposed the model-chosen filter flaw), to evaluate the
# post-test fix independently (RULES.md). Frozen 2026-11-14 before any run on it; pages/evidence differ
# from every dev/test gold.
NEW_TEST2 = [
    {"id": "m01", "type": "direct", "question": "What does the not operator return?",
     "expected_answer": "It takes one condition operand and returns True when the operand is false and False when the operand is true.",
     "page": 106, "evidence": "The not operator takes one condition operand and returns True when the operand is false"},
    {"id": "m02", "type": "condition", "question": "Can for loops and while loops be combined inside one nested loop?",
     "expected_answer": "Yes. The for and while constructs can be mixed in a nested loop construct (e.g. an outer for loop over a list with an inner while loop).",
     "page": 136, "evidence": "The two for and while loop constructs can also be mixed in a nested loop construct."},
    {"id": "m03", "type": "direct", "question": "What happens when a function finishes executing?",
     "expected_answer": "The function returns and provides a result to the calling code.",
     "page": 164, "evidence": "When a function finishes, the function returns and provides a result to the calling code."},
    {"id": "m04", "type": "paraphrase",
     "question": "For printing every multiple of 5 below 50, how does a for loop with range() compare with an equivalent while loop?",
     "expected_answer": "The for loop with range(0, 50, 5) is more compact than the while loop implementation (which needs initialization and an explicit increment).",
     "page": 131, "evidence": "Notice the compactness of the for construction compared to the while"},
    {"id": "m05", "type": "condition", "question": "In the loop-else example that searches a list for the number 10, what happens if 10 is not in the list?",
     "expected_answer": "The loop terminates after evaluating all integers, so the else statement runs and prints \"10 is not in the list.\"",
     "page": 141, "evidence": "hence the else statement will run and print \"10 is not in the list.\""},
    {"id": "m06", "type": "direct", "question": "How does the textbook define a function?",
     "expected_answer": "A function is a named, reusable block of code that performs a task when called.",
     "page": 148, "evidence": "A function is a named, reusable block of code that performs a task when called."},
]

# Unanswerable, near-topic questions. Absence was checked by a keyword scan over ALL
# 263 corpus chunks (not just top-k): see `absence_check` (0 hits for each keyword).
UNANSWERABLE = [
    {"id": "u01", "split": "dev", "question": "How do I write a lambda (anonymous) function in Python?",
     "absence_reason": "Corpus = chapters 4-6 only; 'lambda' never occurs. 'anonymous' only occurs as a string default value \"Anonymous\" (p.170).",
     "absence_check": ["lambda"]},
    {"id": "u02", "split": "dev", "question": "How does a try/except block handle a ZeroDivisionError?",
     "absence_reason": "No 'try', 'except' or 'ZeroDivision' token in the corpus; calc_mpg avoids division by zero with an if, not exceptions.",
     "absence_check": ["try", "except", "ZeroDivision"]},
    {"id": "u03", "split": "dev", "question": "What is the base case of a recursive function?",
     "absence_reason": "No 'recursion'/'recursive'/'base case' in chapters 4-6 (recursion is a later chapter, not indexed).",
     "absence_check": ["recursion", "recursive", "base case"]},
    {"id": "u04", "split": "test", "question": "What does the yield keyword do inside a generator function?",
     "absence_reason": "No 'yield' or 'generator' token in the corpus.", "absence_check": ["yield", "generator"]},
    {"id": "u05", "split": "test", "question": "How do *args and **kwargs let a function accept a variable number of arguments?",
     "absence_reason": "No '*args', 'kwargs', 'variable number' or 'arbitrary' in the corpus; section 6.6 covers keyword/default arguments only.",
     "absence_check": ["*args", "kwargs", "variable number", "arbitrary"]},
    {"id": "v01", "split": "test2", "question": "How do I write a dictionary comprehension in Python?",
     "absence_reason": "No 'comprehension' or 'dictionary' token in chapters 4-6.", "absence_check": ["comprehension", "dictionary"]},
    {"id": "v02", "split": "test2", "question": "How can the walrus operator := be used in a while loop condition?",
     "absence_reason": "No ':=' or 'walrus' in the corpus.", "absence_check": [":=", "walrus"]},
]


def build_chunks() -> list[dict]:
    rows = [json.loads(l) for l in (DAY6_DIR / "results" / "chunks_C.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    chunks = []
    for order, r in enumerate(rows):
        chunks.append({
            "id": r["chunk_id"], "text": r["text"], "source_id": SOURCE_ID, "source": SOURCE,
            "page": r["page"],
            "metadata": {"chapter": r["chapter"], "chapter_title": r["chapter_title"], "section": r["section"],
                         "section_title": r["section_title"], "printed_page": r["printed_page"],
                         "order": order, "content_hash": r["content_hash"]},
        })
    return chunks


def check_chroma_ids(chunks: list[dict]) -> str:
    try:
        import chromadb
    except ImportError:
        return "skipped (chromadb not installed in this interpreter)"
    col = chromadb.PersistentClient(path=str(CHROMA_PATH)).get_collection(CHROMA_COLLECTION)
    ids = set(col.get(include=[])["ids"])
    if ids != {c["id"] for c in chunks}:
        raise SystemExit("Chunk IDs differ from the Day 6 Chroma collection; rebuild Day 6 first.")
    return f"ok ({len(ids)} ids match {CHROMA_COLLECTION})"


def norm(text: str) -> str:
    """Same normalisation as Day 6 evaluation: collapse whitespace, lowercase."""
    return re.sub(r"\s+", " ", text).strip().lower()


def hit(chunk: dict, gold: list[dict]) -> bool:
    return any(chunk["source_id"] == g["source_id"] and chunk["page"] == g["page"] and norm(g["evidence"]) in norm(chunk["text"])
               for g in gold)


def build_benchmark(chunks: list[dict]) -> dict:
    day6 = json.loads((DAY6_DIR / "benchmark" / "questions.json").read_text(encoding="utf-8"))
    questions = []
    for q in day6["questions"]:
        questions.append({
            "id": q["id"], "split": "dev", "answerable": True, "type": q["type"], "origin": f"day6-{q['split']}",
            "question": q["question"], "expected_answer": q["expected_answer"], "filter": q.get("filter"),
            "gold": [{"source_id": g["source_id"], "page": g["page"], "evidence": g["evidence_quote"]} for g in q["gold"]],
        })
    for q in NEW_TEST:
        questions.append({
            "id": q["id"], "split": "test", "answerable": True, "type": q["type"], "origin": "day7-new",
            "question": q["question"], "expected_answer": q["expected_answer"], "filter": None,
            "gold": [{"source_id": SOURCE_ID, "page": q["page"], "evidence": q["evidence"]}],
        })
    for q in NEW_TEST2:
        questions.append({
            "id": q["id"], "split": "test2", "answerable": True, "type": q["type"], "origin": "day7-new-test2",
            "question": q["question"], "expected_answer": q["expected_answer"], "filter": None,
            "gold": [{"source_id": SOURCE_ID, "page": q["page"], "evidence": q["evidence"]}],
        })
    for q in UNANSWERABLE:
        questions.append({**q, "answerable": False, "type": "unanswerable", "origin": "day7-new", "filter": None,
                          "expected_behavior": "search_and_abstain"})
    # Validate: every gold evidence sits fully inside one chunk on the right page;
    # every absence keyword occurs nowhere in the corpus.
    lower_texts = [c["text"].lower() for c in chunks]
    for q in questions:
        if q["answerable"]:
            for g in q["gold"]:
                if not any(hit(c, [g]) for c in chunks):
                    raise SystemExit(f"{q['id']}: gold evidence not found in a chunk on page {g['page']}")
        else:
            for kw in q["absence_check"]:
                pat = re.compile(r"(?<!\w)" + re.escape(kw.lower()) + r"(?!\w)")
                if any(pat.search(t) for t in lower_texts):
                    raise SystemExit(f"{q['id']}: absence keyword '{kw}' occurs in corpus")
    return {
        "description": "Day 7 benchmark on OpenStax Introduction to Python Programming ch.4-6 (PDF p.95-173).",
        "frozen_at": "2026-11-14",
        "split_rule": ("dev = all 25 Day 6 questions (incl. former Day 6 test t01-t06, already seen) + u01-u03. "
                       "test = n01-n06 + u04-u05, written for Day 7 before any Day 7 run; their evidence sentences "
                       "and pages differ from every dev gold. test2 = m01-m06 + v01-v02, written after the test run to "
                       "evaluate the post-test fix independently."),
        "hit_rule": "A retrieved chunk is a hit iff same source_id, same page and the full evidence string is a substring of the chunk text after whitespace-collapse + lowercase (Day 6 rule). gold entries are alternatives.",
        "filter_rule": "filter = {chapter: N} is user-supplied context (Day 6 convention); never derived from gold.",
        "questions": questions,
    }


def main() -> None:
    chunks = build_chunks()
    print("chroma id check:", check_chroma_ids(chunks))
    bench = build_benchmark(chunks)
    CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHUNKS_FILE.write_text(json.dumps(chunks, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    BENCHMARK_FILE.write_text(json.dumps(bench, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    qs = bench["questions"]
    for split in ("dev", "test", "test2"):
        a = sum(q["split"] == split and q["answerable"] for q in qs)
        u = sum(q["split"] == split and not q["answerable"] for q in qs)
        print(f"{split}: {a} answerable + {u} unanswerable")
    print(f"wrote {CHUNKS_FILE} ({len(chunks)} chunks) and {BENCHMARK_FILE}")


if __name__ == "__main__":
    main()
