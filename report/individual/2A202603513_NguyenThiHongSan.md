# Báo cáo Day 7 — 2A202603513 Nguyễn Thị Hồng San

Agentic RAG trên kho Day 6 (OpenStax *Introduction to Python Programming*, chương 4–6). Toàn bộ số liệu dưới đây lấy từ file trong [results/](../../results/); lệnh chạy ở [README](../../README.md).

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:** OpenStax, *Introduction to Python Programming* (Das, Lawson, Mayfield, Norouzi), CC BY-NC-SA 4.0, dùng phi thương mại cho bài học, có ghi nguồn. PDF trang vật lý 95–173 (chương 4 Decisions, 5 Loops, 6 Functions), **77 trang nội dung** (loại 3 trang trống). **263 chunk** — đúng index `day06_C` của Day 6 (chia theo đoạn ≤800 ký tự, metadata chương/section/trang). [data/chunks.json](../../data/chunks.json) được dựng bằng `python -m src.data_prep`; script kiểm tra 263 ID khớp collection Chroma Day 6.
- **Vector store, embedding model, phiên bản và số chiều:** Chroma 1.5.9 `PersistentClient`, HNSW, cosine, collection `day06_C` (dùng lại nguyên index Day 6). Embedding `intfloat/multilingual-e5-small`, **384 chiều**, sentence-transformers 6.3.0 trên CPU, prefix `query: ` cho câu hỏi (cùng quy ước `passage: ` lúc index), chuẩn hoá L2. Code kiểm tra metadata collection (model, số chiều) trước khi truy vấn. Không có Day 6 vẫn tái lập được: `python -m src.build_index` dựng lại index; đã kiểm chứng **top-10 giống hệt 28/28 câu dev** so với index Day 6.
- **Agent model, cách chạy và phân chia dev/test:** `gpt-4o-mini` qua OpenAI Chat Completions (tool calling, temperature 0), client viết bằng thư viện chuẩn ([src/llm.py](../../src/llm.py)). Lần chạy dev đầu tiên đi qua OpenRouter (`openai/gpt-4o-mini`) nhưng tài khoản hết credit giữa chừng (HTTP 402) → chạy lại **toàn bộ dev qua OpenAI**; lần chạy OpenRouter giữ ở `results/agent/dev_openrouter_run1/` làm bằng chứng. Split ([data/benchmark.json](../../data/benchmark.json)):

  | Split | Có đáp án | Thiếu evidence | Ghi chú |
  |---|---:|---:|---|
  | dev | 25 | 3 | 25 câu Day 6 (gồm t01–t06 là test Day 6 đã xem → chuyển sang dev) + u01–u03 |
  | test | 6 | 2 | n01–n06 + u04–u05, viết mới và chốt trước mọi lần chạy Day 7 |
  | test2 | 6 | 2 | m01–m06 + v01–v02, viết **sau** test để đánh giá độc lập bản sửa sau test (RULES) |

- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:** câu có đáp án ghi `gold = [{source_id, page, evidence}]`; script kiểm tra mọi evidence nằm trọn trong một chunk đúng trang. *Hit* = cùng nguồn, cùng trang và evidence là chuỗi con của chunk sau khi gộp khoảng trắng + chữ thường (giống Day 6). Câu thiếu evidence là câu gần chủ đề (lambda, try/except, đệ quy, yield, `*args`, dictionary comprehension, walrus); script quét **toàn bộ 263 chunk** và từ khoá phải xuất hiện 0 lần (`absence_check`), không dựa vào top-k. Câu trả lời chấm tay 0/1/2 theo BENCHMARK; nhãn và lý do ở [results/reviews/](../../results/reviews/).

## Retrieval và thử nghiệm

Bốn phương pháp ([src/retrieval.py](../../src/retrieval.py)), cùng corpus, cùng index, query = câu hỏi gốc, filter chương chỉ khi người dùng cung cấp (q12, q17, q18, t04, t06 — quy ước Day 6):

1. **Dense** — e5-small → Chroma `day06_C` (Day 6).
2. **BM25** — Okapi (k1 = 1.5, b = 0.75), tách token có giữ toán tử code (`**`, `==`…), stemming nhẹ; biến thể không stemming để so sánh.
3. **Hybrid RRF** — hợp nhất top-20 dense + top-20 BM25 theo hạng, 1/(60 + rank); không cộng điểm thô khác thang đo.
4. **Hybrid + LLM rerank** — gpt-4o-mini xếp lại top-15 của hybrid theo kiểu listwise; nếu không parse được JSON thì giữ thứ tự hybrid (có ghi log).

Context ([src/context.py](../../src/context.py)): lấy theo hạng, loại trùng, budget tính bằng **ký tự** (gồm header nguồn/trang, ≈ ký tự/4 token), chunk không vừa thì bỏ chứ không cắt; tuỳ chọn thêm chunk lân cận cùng section. Mọi phương pháp đều xuất ranking top-10 để Hit@1/Hit@3/MRR@10 dùng chung cutoff.

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| Baseline `R1_dense` | dense, top-3, filter người dùng, 1500 ký tự | Day 6 dense | dev | 22/25 (88%) | 23/25 (92%) | 23/25 (92%) | 17.9 ms/câu, $0 |
| Phương pháp 2 `R2_bm25` | BM25 + stem, top-3, 1500 | khớp từ khoá/toán tử chính xác | dev | 17/25 (68%) | 24/25 (96%) | 24/25 (96%) | 0.2 ms, $0 |
| (ablation) `R2b_bm25_nostem` | BM25 không stem | stemmer có giúp không? | dev | 19/25 (76%) | 25/25 (100%) | 24/25 | 0.2 ms, $0 |
| Phương pháp 3 `R3_hybrid` | RRF dense+BM25 (pool 20), top-3, 1500 | gộp được ưu điểm cả hai | dev | 19/25 (76%) | 25/25 (100%) | 24/25 (96%) | 18.2 ms, $0 |
| Cải thiện 1 `I1_hybrid_k5` | hybrid, top-5, 2500 ký tự | evidence hay ở hạng 4–5 / bị bỏ vì budget | dev | 19/25 | 25/25 | **25/25 (100%)** | 17.7 ms, $0, context 2090 ký tự |
| Cải thiện 2 `I2_hybrid_k5_nb` | I1 + chunk lân cận, 3500 ký tự | đủ ví dụ/điều kiện | dev | 19/25 | 25/25 | 25/25 | 17.4 ms, context 3352 ký tự (+60%) |
| Phương pháp 4 / Cải thiện 3 `I3_rerank_k3` | hybrid top-15 → LLM rerank, top-3, 1500 | rerank đưa đoạn trả lời lên hạng 1 | dev | 20/25 (80%) | 24/25 (96%) | 24/25 | 1163 ms/câu, $0.0070/28 câu (43k token vào) |
| `I4_rerank_k5` | rerank, top-5, 2500 | | dev | 20/25 | 24/25 | 25/25 | 1144 ms, $0.0070 |
| Cấu hình đã chọn (retrieval của A4 = `R1_dense`) | dense, top-3, 1500 | chốt trên dev | test | 3/6 (50%) | 5/6 (83%) | 4/6 (67%) | 17.6 ms, $0 |
| Baseline `R1_dense` | (cùng retrieval) | | test | 3/6 | 5/6 | 4/6 | — |
| `R3_hybrid` / `I1_hybrid_k5` (tham khảo) | | | test | 4/6 | 5/6 | 5/6 / 5/6 | ~16–31 ms |
| `R1_dense` | | | test2 | 3/6 | 5/6 | 5/6 | 17.8 ms |
| `R2_bm25` / `R3_hybrid` / `I1` (tham khảo) | | | test2 | 1/6 / 2/6 / 2/6 | 4/6 / 3/6 / 3/6 | 4/6 / 3/6 / 5/6 | |

Agent đã chọn và baseline dùng cùng retrieval dense; khác biệt nằm ở prompt, citation guard và filter (mục Agent). Context Evidence Rate của agent (nhiều lượt search) báo ở bảng agent.

**Nhận xét retrieval:** dense có Hit@1 tốt nhất ở cả ba split; BM25/hybrid đẩy Hit@3 dev lên 25/25 nhưng làm giảm Hit@1 dev, và trên test2 (câu diễn đạt lại nhiều) BM25/hybrid tụt rõ (Hit@3 4/6, 3/6) — lợi ích lexical không tổng quát hoá. Stemmer làm BM25 kém đi (17 → 19 Hit@1 khi bỏ). LLM rerank **không cải thiện**: Hit@3 giảm từ 25 xuống 24 (q08 bị đẩy khỏi top-3), có 2/28 lần parse lỗi (quay về thứ tự hybrid), độ trễ ~1.1 s/câu.

**Hai lỗi dev và cách thử**

1. **Retrieval q10, t03 (dense trượt Hit@3) và context bị cắt bởi budget.** q10 (“end value của range()”): dense xếp chunk định nghĩa range ở hạng 4; t03 cần hai ý (list/string) nằm ở chunk khác chunk gold. Giả thuyết: thêm lexical + nới top-k. Kết quả: hybrid Hit@3 23 → 25/25, nhưng ở budget 1500 vẫn mất 1 câu vì chunk evidence không vừa budget (`R3`: Hit@3 25 nhưng Context 24) → I1 (top-5/2500) đưa Context lên 25/25, đổi lại context dài hơn 77%.
2. **Agent từ chối nhầm vì citation guard (lỗi lớn nhất).** Lần chạy đầu A0 (OpenRouter) từ chối **12/25** câu có đáp án dù context chứa evidence 25/25. Đọc trace: model trả danh sách `citations` đúng nhưng không viết `[id]` trong chữ trả lời → guard (đòi ID xuất hiện inline) loại câu trả lời. Giả thuyết: nói rõ yêu cầu inline trong prompt + trả lỗi cho model sửa 1 lần. Kết quả (OpenAI, cùng model): A0 2/25 → A4 **0/25** từ chối nhầm, grounded 1.84 → 2.00; số lần guard phải yêu cầu sửa: 0–1/28 câu. Lưu ý: cùng cấu hình A0 nhưng qua OpenRouter (12/25) và OpenAI (2/25) lệch nhiều ⇒ biến động giữa các lần chạy/route là đáng kể với 25 câu.
3. *(Thấy trên test, bỏ sót trên dev)* **Model tự chọn filter chương sai.** Xem mục test.

**Chọn cấu hình.** Tiêu chí công bố trước ([results/selection_criteria.md](../../results/selection_criteria.md)): abstention 3/3 → grounded cao nhất → ít từ chối nhầm → context/citation → rẻ/nhanh. A2, A4, A6 hoà ở 4 tiêu chí đầu; chọn **A4_dense_fix** vì rẻ hơn ~2.3× và nhanh hơn A6 (A1/A5 đã thua ở tiêu chí từ chối nhầm nên không chấm tay).

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi** ([src/agent.py](../../src/agent.py)):
  - Tool: `search_textbook(query, chapter?)` (pipeline theo cấu hình), `read_neighbors(chunk_id)` (tuỳ chọn, A3 — không chạy), `submit_answer(answer, citations, abstain)`. Filter người dùng luôn bị cưỡng chế trong tool; A0–A6 cho model tự truyền `chapter` (ghi `filter_source: model`), A7 bỏ tham số này.
  - Dừng: `submit_answer`; giới hạn search (A0/A4/A7: 2; hybrid/rerank: 3) → tool trả lỗi, model phải trả lời hoặc từ chối; `max_turns = 7` → tự từ chối (ghi `max_turns`). Không có lần nào chạm `max_turns`.
  - Context: mỗi lượt search trả top-k chunk đóng gói trong budget/lượt (1500 ký tự với dense); context cuối = hợp các chunk model đã thấy (loại trùng). Văn bản tài liệu được đánh dấu là *dữ liệu, không phải chỉ dẫn*.
  - Citation guard: mọi ID phải đến từ tool **và** xuất hiện dạng `[id]` trong câu trả lời; nếu không → (v2) trả lỗi cho sửa 1 lần, sau đó từ chối. Guard chỉ kiểm tra ID; hỗ trợ ngữ nghĩa được chấm tay.
  - Lỗi: lỗi provider/retriever được bắt theo từng câu, ghi `status: error` + loại lỗi, không thay bằng kết quả giả; client retry 429/5xx với backoff.

| Cấu hình / split | Tool use | Số lượt search (phân bố) | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| A0_dense / dev | 28/28 | 1:19, 2:9 | 2/0/23 — 1.84 | 30/31 | 23/23 | 3/3 | 2/25 |
| A2_rerank / dev | 28/28 | 1:15, 2:6, 3:7 | 0/0/25 — 2.00 | 38/39 | 25/25 | 3/3 | 0/25 |
| **A4_dense_fix / dev** | 28/28 | 1:20, 2:8 | 0/0/25 — **2.00** | 31/32 | 25/25 | 3/3 | 0/25 |
| A6_rerank_fix / dev | 28/28 | 1:18, 2:6, 3:4 | 0/0/25 — 2.00 | 35/36 | 25/25 | 3/3 | 0/25 |
| A7_dense_userfilter / dev | 28/28 | 1:22, 2:6 | 0/0/25 — 2.00 | 33/33 | 25/25 | 3/3 | 0/25 |
| A1_hybrid / dev (tự động) | 28/28 | 1:19, 2:3, 3:6 | — (1 từ chối nhầm) | — | — | 3/3 | 1/25 |
| A5_hybrid_fix / dev (tự động) | 28/28 | 1:20, 2:3, 3:5 | — (2 từ chối nhầm) | — | — | 3/3 | 2/25 |
| **A0_dense / test** (baseline) | 8/8 | 1:5, 2:3 | 0/0/6 — **2.00** | 9/9 | 6/6 | 2/2 | 0/6 |
| **A4_dense_fix / test** (đã chọn) | 8/8 | 1:5, 2:3 | 1/0/5 — **1.67** | 6/6 | 5/5 | 2/2 | 1/6 |
| A0_dense / test2 | 8/8 | 1:4, 2:4 | 1/0/5 — 1.67 | 7/7 | 5/5 | 2/2 | 1/6 |
| A4_dense_fix / test2 | 8/8 | 1:4, 2:4 | 1/0/5 — 1.67 | 9/10 | 6/6 | 2/2 | 0/6 |
| A7_dense_userfilter / test2 | 8/8 | 1:4, 2:4 | 0/0/6 — **2.00** | 7/7 | 6/6 | 2/2 | 0/6 |

Không có lỗi provider trong các lần chạy chính (OpenAI). Context Evidence Rate của agent (tự động, theo gold): dev A0 24/25, A4 25/25, A7 25/25; test A0 5/6, A4 4/6; test2 A0 4/6, A4 4/6, A7 5/6. Chấm context thủ công 0/1/2 trên test (6 câu có đáp án): A0 = 6 câu mức 2; A4 = 5 câu mức 2, 1 câu mức 0 (n06). Auto đếm n05 là trượt nhưng context có **evidence thay thế hợp lệ** (`p0151:c04` nói đúng “control flow moves back to where the function was called”) mà gold của tôi bỏ sót; tương tự m03 ở test2 (`p0165:c00`). Gold **không sửa** sau khi chạy.

| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| test n03 (A4) | có đáp án | `search("miles-per-gallon example gallons is 0", filter={chapter: 6} do model chọn)` → `p0166:c02, p0166:c01, p0166:c00` | “returns -1 … to indicate a problem … avoid division by zero … prints "Gallons can't be 0" [p0166:c01][p0166:c00]” | **2** — đúng và đủ, cả hai citation hỗ trợ (code và câu “a value often used to indicate a problem”). |
| test u05 (A4) | thiếu evidence | 2 lượt search (`*args **kwargs variable number of arguments`, `*args **kwargs`; model lọc chương 6) → chunk về tham số/keyword arguments, không chunk nào nói về `*args` | “The textbook does not provide specific information about how *args and **kwargs …” | **Từ chối đúng** — không thêm khẳng định; quét toàn corpus không có `*args`/`kwargs`. |
| test n06 (A4) | có đáp án | `search("global variables scope errors", filter={chapter: 4}, filter_source: model)` → `p0099:c00, p0117:c03, p0111:c00`; lượt 2 cùng filter sai | Từ chối | **0, lỗi** — model tự lọc chương 4 cho câu chương 6; tìm dense câu gốc không lọc xếp gold `p0159:c00` hạng 1. A0 dùng cùng query nhưng lọc chương 6 → trả lời đúng. |
| test2 m04 (A4) | có đáp án | `search("for loop range", {chapter: 5})`, `search("while loop", {chapter: 5})` → không có p.131 | “for loop … more concise [p0130:c00] … while loop requires manual initialization [p0125:c03]” | **0** — kết luận đúng nhưng không chunk nào được cite nêu ý này (kiến thức chung); `p0125:c03` không hỗ trợ. A7 (không filter, query cụ thể hơn) lấy `p0131:c00/c01` → 2. |
| dev q01 (A0) | có đáp án | `search("bool() convert to False", {chapter: 6})` rồi `search("values that evaluate to False", {chapter: 4})` — model lọc chương sai ở lượt 1, gold p.97 không vào top-3 | Từ chối, nhưng câu từ chối liệt kê kiến thức chung (None, `[]`, `{}`) | **0** — từ chối nhầm, kèm khẳng định không có nguồn. |

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:**
  - Trace agent (mỗi tool call, query, filter, kết quả, context cuối, câu trả lời, citation, token, giây, chi phí): `results/agent/<split>/<config>/traces.json`; tóm tắt tự động `auto_summary.json`; bảng đọc tay `review_sheet.md`; metric từ `starter/agent_metrics.py`: `metrics.json`.
  - Nhãn tay: `results/reviews/manual_labels_<split>.json` (ghi chú từng câu) → `python -m src.make_reviews --split <split>` sinh `results/reviews/<split>_<config>.json` và chạy `agent_metrics.py`.
  - Trace retrieval: `results/retrieval/<split>/traces_<config>.json`, `summary.json`.
  - Chi phí (gpt-4o-mini, $0.15/$0.60 mỗi 1M token vào/ra, ước tính theo usage API): dev 28 câu — A0 $0.0095 (47k/4.1k token, trung vị 2.7 s/câu), A4 $0.0098 (3.2 s), A7 $0.0092 (2.9 s), A1 $0.014, A6 $0.023 (4.2 s), A2 $0.026 (5.0 s); test 8 câu — A0 $0.0031, A4 $0.0033; test2 — A0 $0.0033, A4 $0.0035, A7 $0.0033. Rerank retrieval-only $0.007/28 câu. Embedding và BM25: $0 (CPU). Phần cơ bản < $0.30 (phần nâng cao ≈ $5.4, xem mục cuối).
- **Kết quả trước/sau, ví dụ lỗi, đánh đổi và giới hạn:**
  - Trên **test chính thức, cấu hình đã chọn A4 kém baseline A0** (1.67 vs 2.00; 1 vs 0 từ chối nhầm). Nguyên nhân không phải bản sửa citation mà là **filter chương do model tự đoán** (n06). Tín hiệu đã có trên dev (q01 của A0, q03 của A4 cũng bị model lọc sai chương) nhưng tôi không phát hiện vì A4 vẫn tự cứu được ở dev.
  - **Sửa sau test:** A7 bỏ tham số `chapter` khỏi tool (filter chỉ từ người dùng, đúng GUIDE). Vì bản sửa được gợi ý bởi test, tôi tạo **test2** mới (chốt trước khi chạy) thay vì dùng lại test: A7 đạt 2.00 (6/6), A0 1.67, A4 1.67; A7 cũng giữ 2.00 trên dev, chi phí và thời gian ngang A4. Nếu cần chọn lại, A7 là cấu hình đề xuất.
  - Đánh đổi: hybrid/rerank tăng Hit@3 trên dev nhưng tốn 1.5–2.7× token agent, chậm hơn, và không tổng quát hoá sang test2; dense + top-3/1500 ký tự rẻ nhất mà context đủ cho agent nhờ cho phép search lần 2.
  - **Giới hạn:** test 6+2 và test2 6+2 câu → mỗi câu = 17 điểm phần trăm, khác biệt 1 câu không có ý nghĩa thống kê; biến động lớn giữa các lần chạy (A0: 12/25 vs 2/25 từ chối nhầm trên hai route) và chỉ chạy một lần mỗi cấu hình; gold chỉ có một evidence nên thiếu evidence thay thế (n05, m03) — metric tự động đánh giá thấp; câu thiếu evidence được kiểm bằng quét từ khoá, chỉ đúng trong phạm vi chương 4–6; cross-encoder reranker bị crash (bus error) trong môi trường torch của Day 6 nên rerank dùng LLM; nhãn được chấm với hỗ trợ của AI (Claude Code đọc đầy đủ từng citation, lý do ghi trong `manual_labels_*.json`) — cần sinh viên rà lại trước khi nộp; chỉ có một người chấm.

## Thử thách nâng cao (nếu thực hiện)

**Đã thực hiện nhưng CHƯA ĐẠT ngưỡng: test lần 1 25/30 = 83.3%; test2 (bộ test mới) 26/30 = 86.7% (< 27/30). Không nhận bonus.** Chi tiết, code và cách chạy: [advanced/README.md](../../advanced/README.md).

- **Tài liệu, nguồn, quyền sử dụng, số trang và phiên bản:** USGS, *Mineral Commodity Summaries 2024* (DOI 10.3133/mcs2024), 216 trang PDF (212 trang in), public domain (tác phẩm chính phủ Mỹ); SHA-256 `a4da4050…a562`; PDF không nộp kèm, tải lại bằng link gốc.
- **Cách xử lý text, bảng, ảnh, biểu đồ; phạm vi index và phần chưa xử lý:** text layer PyMuPDF cho cả 216 trang; mỗi trang render 150 dpi và được `gpt-4.1-mini` (vision) trích bảng (markdown), biểu đồ (trục, chú giải, giá trị), bản đồ (lớp chú giải theo vùng), sơ đồ (hộp, mũi tên, số) → 264 phần tử, 0 lỗi parse ($0.50). Index 1,270 chunk (987 text + 283 visual), embedding `text-embedding-3-small` → Chroma + BM25 + RRF; tra theo tên Figure/Table nêu trong câu hỏi. Agent có `view_page` để model xem ảnh trang gốc, verifier `gpt-4.1` kiểm từng khẳng định với đoạn được cite. Chưa xử lý: crop vùng ảnh (dẫn chiếu bằng trang + tiêu đề + vị trí); lỗi chép của vision (ví dụ "550" thay cho chú thích ⁵ + 50 ở bảng helium); giá trị biểu đồ không in số chỉ đọc gần đúng.
- **Cách chia benchmark, schema evidence, model và cấu hình đã chốt trên dev:** dev 22 câu (15 có đáp án, 3/nhóm + 7 thiếu bằng chứng), test 30 câu (6 bảng, 5 ảnh/sơ đồ, 5 biểu đồ, 4 multi-hop, 4 text, 6 thiếu bằng chứng), chia trước khi chạy. Mỗi câu ghi trang vật lý + trang in, vùng (hàng/cột, hình), evidence, phép tính; evidence text kiểm nguyên văn, evidence hình kiểm trên ảnh trang. Cấu hình chốt cho test lần 1: V6 (text + visual, hybrid + tra tiêu đề, `view_page`, `gpt-4.1-mini`) — 19/19 trên dev lúc đó ([advanced/selection.md](../../advanced/selection.md)).

| Nhóm test (V6, chạy 1 lần) | Đạt / tổng | Tỷ lệ | Lỗi / nhận xét |
|---|---|---|---|
| Bảng | 5/6 | 83% | AT-T4: phép tính đúng nhưng ghi "2013" thay cho 2019 |
| Ảnh, sơ đồ | 5/5 | 100% | — |
| Biểu đồ | 5/5 | 100% | — |
| Multi-hop | 3/4 | 75% | AT-M3: "$3 million" nằm ở đoạn văn p.78 nhưng chỉ cite bảng p.78 |
| Text | 4/4 | 100% | — |
| Thiếu bằng chứng | 3/6 | 50% | AT-U1 đọc nhầm bảng lưu huỳnh thành dầu thô; AT-U3 suy diễn thành sự thật; AT-U4 lỗi gold của tôi (p.88 có số cơ sở pin = 10), vẫn tính trượt |
| **Toàn bộ** | **25/30** | **83.3%** | 0 lỗi hệ thống; trung vị 5.8 s/câu; $0.21 cho 30 câu |

- **Trace, nhãn và evidence từng câu; thời gian, chi phí, lỗi hệ thống:** trace `advanced/results/<split>/<config>/traces.json` + `review_sheet.md`; nhãn test [advanced/labels/test_labels.json](../../advanced/labels/test_labels.json). Tổng chi phí phần nâng cao ≈ $5.4.
- **Giới hạn, cách tái lập và đường dẫn benchmark:** [advanced/benchmark.json](../../advanced/benchmark.json). Sau test lần 1, tôi chỉ sửa trên dev (verifier `gpt-4.1`, câu từ chối chuẩn hoá, guard citation, agent `gpt-4.1`; V12 ≈ 21/22 dev) và viết **test2** mới 30 câu (chốt trước khi chạy) đúng quy tắc "đã dùng test để chỉnh thì tạo test mới". V12 không chạy được test2 vì hết credit OpenAI, Gemini free tier hết hạn mức embedding (1.000/ngày) và `gemini-3.5-flash` free chỉ 20 request/ngày (`advanced/run_log.md`). Vì vậy tôi giữ nguyên pipeline V12 và chỉ đổi provider sang miễn phí: embedding `multilingual-e5-small` chạy local + agent/verifier `gemini-3.5-flash-lite` (**L2_e5_gemini35lite**), dev 22/22, chốt trước khi chạy test2 ([advanced/selection.md](../../advanced/selection.md)).

| Nhóm test2 (L2, chạy 1 lần) | Đạt / tổng | Tỷ lệ | Lỗi / nhận xét |
|---|---|---|---|
| Bảng | 6/6 | 100% | — |
| Ảnh, sơ đồ | 4/5 | 80% | AT2-I5: khẳng định sai Cu có biểu đồ xanh (ảnh gốc p.28: Cu trắng) |
| Biểu đồ | 2/5 | 40% | AT2-C1, AT2-C3 từ chối nhầm (không lấy được giá trị cột); AT2-C2 lỗi chép vision (Gold/Platinum/Indium cùng ~100%, ảnh gốc chỉ Indium chạm đỉnh) |
| Multi-hop | 4/4 | 100% | — |
| Text | 4/4 | 100% | — |
| Thiếu bằng chứng | 6/6 | 100% | — |
| **Toàn bộ** | **26/30** | **86.7%** | 0 lỗi hệ thống; trung vị 16.2 s/câu; $0 (free tier + embedding local) |

Nhãn test2: [advanced/labels/test2_labels.json](../../advanced/labels/test2_labels.json). So với test lần 1, câu thiếu bằng chứng cải thiện rõ (3/6 → 6/6 nhờ verifier và câu từ chối chuẩn hoá), nhưng **biểu đồ cột** là điểm yếu còn lại: bản chép vision ước lượng sai giá trị cột không in số và model lite không tự sửa khi xem ảnh trang. Hai lần test khác cấu hình (V6 `gpt-4.1-mini` vs L2 e5 + Gemini lite) và mỗi lần chạy một lần, nên không so sánh trực tiếp được.
