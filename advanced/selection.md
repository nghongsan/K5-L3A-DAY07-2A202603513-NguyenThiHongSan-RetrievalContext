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
