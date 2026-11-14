"""Unit tests for src/ (mock LLM/retriever only check code paths, never benchmark quality)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agent import Agent, AgentConfig  # noqa: E402
from src.context import ContextPacker, alias, is_hit  # noqa: E402
from src.retrieval import BM25Retriever, HybridRetriever, tokenize  # noqa: E402


def chunk(i, text, page=1, section="4.1", chapter=4):
    return {"id": f"src:B:para800:p{page:04d}:c{i:02d}", "text": text, "source_id": "src", "source": "s", "page": page,
            "metadata": {"chapter": chapter, "section": section, "section_title": "t", "order": i}}


CHUNKS = [
    chunk(0, "A branch is a group of statements that execute based on a condition."),
    chunk(1, "The exponentiation operator ** is right associative.", section="4.4"),
    chunk(2, "A for loop iterates over a container such as a list.", page=2, section="5.2", chapter=5),
    chunk(3, "A while loop repeats while the condition is true.", page=2, section="5.2", chapter=5),
]


class FakeRanker:
    name = "fake"

    def __init__(self, order):
        self.order = order

    def search(self, query, top_k=5, filters=None):
        res = [c for c in (CHUNKS[i] for i in self.order) if not filters or c["metadata"]["chapter"] == filters["chapter"]]
        return [{**c, "score": 1.0 / r, "rank": r, "method": self.name} for r, c in enumerate(res[:top_k], 1)]


class TestRetrieval(unittest.TestCase):
    def test_tokenize_keeps_code_operators(self):
        self.assertIn("**", tokenize("2 ** 3"))
        self.assertIn("loop", tokenize("loops"))

    def test_bm25_ranks_and_filters(self):
        bm = BM25Retriever(CHUNKS)
        self.assertEqual(bm.search("what is a branch")[0]["id"], CHUNKS[0]["id"])
        res = bm.search("loop condition", filters={"chapter": 4})
        self.assertTrue(all(r["metadata"]["chapter"] == 4 for r in res))
        with self.assertRaises(ValueError):
            bm.search("x", filters={"page": 1})

    def test_rrf_is_rank_based(self):
        h = HybridRetriever(FakeRanker([0, 1, 2, 3]), FakeRanker([1, 0, 2, 3]), pool=4)
        res = h.search("q", top_k=4)
        self.assertEqual({res[0]["id"], res[1]["id"]}, {CHUNKS[0]["id"], CHUNKS[1]["id"]})
        self.assertAlmostEqual(res[0]["score"], round(1 / 61 + 1 / 62, 5))


class TestContext(unittest.TestCase):
    def test_budget_dedup_and_neighbours(self):
        p = ContextPacker(CHUNKS)
        ranked = [{**CHUNKS[2], "rank": 1}, {**CHUNKS[2], "rank": 2}, {**CHUNKS[0], "rank": 3}]
        text, chosen = p.pack(ranked, top_k=3, budget=10_000)
        self.assertEqual([c["id"] for c in chosen], [CHUNKS[2]["id"], CHUNKS[0]["id"]])
        _, chosen = p.pack(ranked, top_k=1, budget=10_000, neighbours=True)
        self.assertEqual([c["id"] for c in chosen], [CHUNKS[2]["id"], CHUNKS[3]["id"]])
        text, chosen = p.pack(ranked, top_k=3, budget=50)
        self.assertEqual(chosen, [])

    def test_hit_uses_whitespace_normalisation(self):
        g = [{"source_id": "src", "page": 1, "evidence": "group of   statements\nthat"}]
        self.assertTrue(is_hit(CHUNKS[0], g))
        self.assertFalse(is_hit(CHUNKS[2], g))


class ScriptedLLM:
    def __init__(self, steps):
        self.steps, self.i = steps, 0

    def chat(self, messages, tools=None, max_tokens=0):
        calls = self.steps[self.i]
        self.i += 1
        calls = [{"id": f"c{self.i}{k}", "name": n, "args": a} for k, (n, a) in enumerate(calls)]
        raw = {"role": "assistant", "content": None}
        return {"text": "", "calls": calls, "raw_message": raw, "usage": {"in": 10, "out": 5}}

    def cost(self, usage):
        return 0.0


class TestAgent(unittest.TestCase):
    def make(self, steps, **kw):
        return Agent(AgentConfig("t", top_k=2, call_budget=5000, **kw), ScriptedLLM(steps), FakeRanker([0, 1, 2, 3]), CHUNKS)

    def test_answer_with_valid_citation(self):
        a0 = alias(CHUNKS[0]["id"])
        r = self.make([[("search_textbook", {"query": "branch"})],
                       [("submit_answer", {"answer": f"A group of statements [{a0}].", "citations": [a0], "abstain": False})]]).run("What is a branch?")
        self.assertEqual(r["status"], "answered")
        self.assertEqual(r["n_searches"], 1)
        self.assertIn(a0, r["context_ids"])

    def test_citation_not_in_context_is_rejected(self):
        a3 = alias(CHUNKS[3]["id"])
        r = self.make([[("search_textbook", {"query": "branch"})],
                       [("submit_answer", {"answer": f"x [{a3}]", "citations": [a3], "abstain": False})]]).run("q")
        self.assertEqual(r["status"], "abstain")
        self.assertEqual(r["reason"], "invalid_citations")

    def test_search_limit_and_user_filter(self):
        steps = [[("search_textbook", {"query": "a"})], [("search_textbook", {"query": "b"})],
                 [("submit_answer", {"answer": "none", "citations": [], "abstain": True})]]
        r = self.make(steps, max_searches=1).run("q", {"chapter": 5})
        self.assertEqual(r["n_searches"], 1)
        self.assertTrue(any(e["event"] == "search_limit" for e in r["events"]))
        self.assertEqual(r["events"][0]["filter"], {"chapter": 5})
        self.assertTrue(all(i.startswith("p0002") for i in r["context_ids"]))
        self.assertEqual(r["status"], "abstain")


class TestUserOnlyFilter(unittest.TestCase):
    def test_model_chapter_ignored_when_disabled(self):
        steps = [[("search_textbook", {"query": "loop", "chapter": 5})],
                 [("submit_answer", {"answer": "none", "citations": [], "abstain": True})]]
        a = Agent(AgentConfig("t", top_k=4, call_budget=5000, model_filter=False), ScriptedLLM(steps), FakeRanker([0, 1, 2, 3]), CHUNKS)
        self.assertNotIn("chapter", a.tools[0]["function"]["parameters"]["properties"])
        r = a.run("q")
        self.assertIsNone(r["events"][0]["filter"])
        self.assertEqual(len(r["context_ids"]), 4)


if __name__ == "__main__":
    unittest.main()
