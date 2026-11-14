# Advanced challenge — config selection (written on dev, BEFORE any test run)

Criteria (in order): pass rate on dev (manual pass/fail per ADVANCED.md, all 19 questions) → abstention 4/4 →
cost/time. Dev labels and reasons: advanced/labels/dev_labels.json.

| Config | Pipeline | Dev pass | Unanswerable | LLM cost (19 q) | Median s/q |
|---|---|---|---|---|---|
| V0_text_dense | PDF text layer only, dense (text-embedding-3-small), gpt-4.1-mini | 12/19 | 3/4 | $0.101 | 5.7 |
| V1_mm_hybrid | text + vision-extracted tables/figures, hybrid RRF | 16/19 | 4/4 | $0.086 | 3.6 |
| V2_mm_hybrid_view | V1 + view_page (original page image) | 15/19 | 3/4 | $0.153 | 5.8 |
| V5_mm_hybrid_title | V1 + Figure/Table title lookup from the query + prompt v2 | 18/19 | 4/4 | $0.087 | 3.5 |
| **V6_mm_hybrid_title_view** | V5 + view_page | **19/19** | 4/4 | $0.144 | 6.0 |
| V7_mm_hybrid_title_41 | V5 with gpt-4.1 | 17/19 | 3/4 | $0.474 | 3.8 |

Chosen: **V6_mm_hybrid_title_view**. Test is run once for V6 (chosen) and V0 (baseline); nothing is changed after.
Note: dev AD-M3 was reworded after V0–V2 (ambiguous); V0/V2/V5–V7 were run with the new wording, V1 with the old.

## Round 2 — after test-1 (written BEFORE any test2 run)

Test-1 (V6, run once): 25/30 = 83.3% (fail). Errors: unsupported claims in answers/refusals (AT-U1 misread sulfur table,
AT-U3 inference as fact, AT-T4 wrong year label), an uncited value (AT-M3), and one gold error of mine (AT-U4 was answerable).
Fixes tuned on dev only (dev gained 3 trap questions AD-U5..U7): claim-level verifier (gpt-4.1) on the cited passages with
element-level expansion of split tables, prompt v3 (no speculation when abstaining), robust citation parsing, standardised
abstention text, gpt-4.1 agent, rate-limit backoff + one question-level retry on system errors.

| Config (dev, 22 q) | Dev pass | Notes |
|---|---|---|
| V6 rerun on 22 q | 19/22 | AD-M2/AD-M3 citation-guard failures, AD-U7 ok, AD-U1 ok |
| V8 (mini + mini verifier) | 19/22 | weak verifier accepted uranium 'withheld' claim |
| V9 (mini + 4.1 verifier) | 19/22 | guard false negative (AD-T2), AD-M3 |
| V10 (4.1 + 4.1 verifier) | 20/22 | guard false negative (AD-M2) |
| V11 run 1 / run 2 | 21/22 / 20/22 | AD-M3 both runs; run 2 AD-U1 speculative refusal |
| **V12_final** | 20/22 (+AD-U6 rerun after 429 fix: pass) → 21/22 | only AD-M3 (ambiguous dev item) |

Chosen for test2: **V12_final**. test2 (30 new questions, frozen before this run) is run once for V12_final and V0_text_dense.

## Round 3 — free fallback (written BEFORE any test2 run, 2026-11-14)

test2 could not be run with V12_final: OpenAI credit exhausted (embedding 429 `insufficient_quota`), Gemini embedding
free tier capped at 1,000 requests/day (index needs 1,270), `gemini-2.5-flash` closed to new users, and
`gemini-3.5-flash` free tier allows only 20 requests/day (L1_e5_gemini35 dev run killed after hitting the
quota; it produced no output and is not used). Same V12 pipeline (hybrid RRF + title lookup + view_page +
claim verifier + standardised abstention), changing only the providers:

| Config (dev, 22 q) | Embeddings | Agent + verifier | Dev pass | Unanswerable | LLM cost | Median s/q |
|---|---|---|---|---|---|---|
| V12_final (round 2) | text-embedding-3-small | gpt-4.1 | 21/22 | 7/7 | $0.69 | 6.9 |
| **L2_e5_gemini35lite** | multilingual-e5-small (local, 384 d) | gemini-3.5-flash-lite (free tier) | **22/22** | 7/7 (6 abstain + AD-U7 states reserves unavailable) | $0 | 28.5 |

Dev labels and reasons: [labels/dev_labels_L2.json](labels/dev_labels_L2.json). Retrieval on dev: page_hit@3 15/15, cited all gold pages 15/15.
Chosen for test2: **L2_e5_gemini35lite**, baseline **L0_e5_text_dense** (text layer only, dense e5, gemini-3.5-flash-lite agent, no view/verifier).
test2 (30 questions, frozen before round 2) is run once for both; nothing is changed after.

## Round 4 — in progress (test3 frozen first)

test3 (30 new questions, same group mix) was written and committed (9d0a1f8) after test2 was labelled and BEFORE any
round-4 change. Changes are motivated only by dev/test2 errors: FIG_LABELS=1 (unlabelled bar charts on pages 16, 19, 20
inherit the page's Figure label so title lookup finds them; fixes the AT2-C1/AT2-C3 refusals) and prompt v4 (page image
beats transcription; no items added by analogy; aimed at AT2-C2/AT2-I5). Candidate: L3_e5_lite_figlabels. Selection rule
(fixed now): choose L3 for test3 only if its dev pass is >= L2's 22/22 minus at most one question; otherwise run L2 on test3.
The dev run was stopped by the gemini-3.5-flash-lite daily quota; no selection made yet, test3 not run.

### Round 4b — model switch forced by quota (rule written BEFORE running L4 on dev)

gemini-3.5-flash-lite is out of free quota (500/day), so the L3 pipeline is run as L4_e5_lite31_figlabels with
gemini-3.1-flash-lite (agent + verifier); everything else identical (FIG_LABELS=1, prompt v4). Rule, fixed now:
run L4 once on dev (22 q) and label by hand; if dev pass >= 21/22, L4 is the config for test3 and test3 is run
exactly once; otherwise no test3 run is made today and the status stays "not passed". test3 is never used to choose.

Result of the rule: L4 dev = 21/22 (labels: labels/dev_labels_L4.json; only AD-M3 failed, the same ambiguous dev item as in earlier rounds) -> L4 is the config for test3.
Extra check on test2 (development data, NOT fully hand-labelled for L4; folder results/test2/L4_e5_lite31_figlabels_devdata/):
AT2-C1, C3, I5 now answered correctly (L2 failed them); AT2-I4, M1, M3 became refusals because the verifier rejected answers whose
cited passages were incomplete (e.g. AT2-M3 cites the p206 table but 'Canada 62%' is in p206-t2); AT2-C2 still wrong (3-way tie).
Net expectation: about the same as L2 (~26/30). No change is made after this point; test3 is run once for L4 (the L0 text-only
baseline cannot be run today: its gemini-3.5-flash-lite quota is exhausted).

Test3 result (run once): L4 = 25/30 = 83.3% (labels/test3_labels.json) -> not passed. No further change was made after the run.
