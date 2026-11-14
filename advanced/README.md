# Thử thách nâng cao — USGS Mineral Commodity Summaries 2024

**Trạng thái: CHƯA ĐẠT.** Test lần 1 (V6) = 25/30 (83.3%); test2 (bộ test mới, L2_e5_gemini35lite, chạy 1 lần) = **26/30 (86.7%)** < 27/30. Không nhận điểm bonus.

## Tài liệu
- U.S. Geological Survey, 2024, *Mineral Commodity Summaries 2024*, 212 p. (PDF 216 trang vật lý). DOI https://doi.org/10.3133/mcs2024 — PDF: https://pubs.usgs.gov/periodicals/mcs2024/mcs2024.pdf
- SHA-256 `a4da4050fc9a63a98538960a531d93c6b758c689f01d66a09a49796f58a5a562`. Tác phẩm của chính phủ Mỹ (USGS) → public domain tại Mỹ.
- Nội dung: bảng (Salient Statistics, World Mine Production and Reserves của ~90 hàng hoá; Table 1–5), biểu đồ (Fig. 2, 4, 7, 8, 10–13), bản đồ (Fig. 3–8), sơ đồ (Fig. 1, 14, C1, C2), ảnh bìa.
- Quy ước trang: `page` = trang vật lý; trang in = trang vật lý − 4.

## Pipeline
1. `src/extract.py` — PyMuPDF lấy text từng trang (216/216); render PNG 150 dpi; `gpt-4.1-mini` (vision) trích **mọi** bảng/biểu đồ/bản đồ/sơ đồ/ảnh có thông tin thành JSON (bảng → markdown đủ hàng/cột; biểu đồ → trục, chú giải, giá trị; bản đồ → lớp chú giải và vùng). 264 phần tử, 0 trang lỗi parse, $0.50. Cache: `extracted/vision/pNNN.json` (đối chiếu được với trang gốc).
2. `src/build_index.py` — 1,270 chunk: 987 text (≤1000 ký tự, overlap 150) + 283 visual (bảng dài tách theo hàng, lặp header). Mỗi chunk có trang, trang in, chương/hàng hoá, loại phần tử, tiêu đề, vị trí trên trang. Embedding `text-embedding-3-small` (1536 d) → Chroma (cosine) + BM25. Thống kê: [index_stats.json](index_stats.json) (OpenAI, dùng cho dev/test lần 1); index e5 dùng cho test2: [index_stats_e5.json](index_stats_e5.json).
3. `src/rag.py` — retriever dense / BM25 / hybrid RRF; tra theo tên "Figure N/Table N" có trong câu hỏi; agent với `search_report`, `view_page` (gửi ảnh trang gốc cho model đối chiếu), `submit_answer`; guard citation; verifier (`gpt-4.1`) kiểm từng khẳng định với đúng các đoạn được cite; câu từ chối chuẩn hoá.
4. `src/run.py` — chạy cấu hình trên một split, lưu trace (mọi tool call, query, kết quả, ảnh đã xem, verifier, câu trả lời, citation, token, chi phí, thời gian, lỗi) + `review_sheet.md`.

Phần chưa xử lý / giới hạn: vision có thể chép sai (ví dụ bảng helium p.92 ghi "550" thay cho "⁵50" — chú thích 5 + giá trị 50); giá trị biểu đồ không in số chỉ đọc gần đúng; không crop vùng ảnh (dẫn chiếu bằng trang + tiêu đề hình/bảng + vị trí).

## Benchmark (`benchmark.json`, kiểm bằng `src/validate_benchmark.py`)
| Split | Bảng | Ảnh/sơ đồ | Biểu đồ | Multi-hop | Text | Thiếu bằng chứng | Tổng |
|---|---|---|---|---|---|---|---|
| dev | 3 | 3 | 3 | 3 | 3 | 7 (4 + 3 bẫy thêm sau test-1) | 22 |
| test (lần 1, đã dùng) | 6 | 5 | 5 | 4 | 4 | 6 | 30 |
| test2 (mới, đã chạy 1 lần) | 6 | 5 | 5 | 4 | 4 | 6 | 30 |

Mỗi câu có trang, vùng (hàng/cột/ô, hình), evidence; evidence text được kiểm nguyên văn trên trang, evidence hình được kiểm trên ảnh trang gốc; câu thiếu bằng chứng kiểm bằng regex toàn tài liệu (test2: thêm đọc top-3 kết quả tìm kiếm ngữ nghĩa).

## Kết quả
- Dev và lý do chọn cấu hình: [selection.md](selection.md).
- **Test lần 1 (V6, chạy 1 lần): 25/30 = 83.3%** — nhãn từng câu và lý do: [labels/test_labels.json](labels/test_labels.json); trace: `results/test/V6_mm_hybrid_title_view/`. Baseline V0 (chỉ text): trace `results/test/V0_text_dense/` (chưa chấm tay).
  - Theo nhóm: bảng 5/6, ảnh 5/5, biểu đồ 5/5, multi-hop 3/4, text 4/4, thiếu bằng chứng 3/6.
  - Lỗi: AT-T4 ghi sai năm; AT-M3 không cite đoạn chứa "$3 million"; AT-U1 đọc nhầm bảng lưu huỳnh thành sản lượng dầu thô; AT-U3 đưa suy diễn thành sự thật; AT-U4 **lỗi gold của tôi** (p.88 có số cơ sở pin Li-ion = 10) — vẫn tính trượt theo nhãn đã chốt.
  - Lỗi hệ thống: 0. Thời gian trung vị 5.8 s/câu; chi phí $0.21 (30 câu).
- Sau test-1: sửa trên dev (verifier, câu từ chối chuẩn hoá, guard citation, gpt-4.1) → V12 ≈ 21/22 dev; tạo test2 mới. V12 **không chạy được test2**: hết credit OpenAI; Gemini free tier giới hạn 1.000 request embedding/ngày; `gemini-2.5-flash` đóng với người dùng mới; `gemini-3.5-flash` free chỉ 20 request/ngày (ghi ở [run_log.md](run_log.md)).
- **Vòng 3 (miễn phí):** giữ nguyên pipeline V12, chỉ đổi provider: embedding `intfloat/multilingual-e5-small` chạy local (384 d, collection `mcs2024_e5`, `EMB_PROVIDER=local`) + agent/verifier `gemini-3.5-flash-lite` (free tier) = **L2_e5_gemini35lite**. Dev: **22/22** (nhãn: [labels/dev_labels_L2.json](labels/dev_labels_L2.json)); chốt trong [selection.md](selection.md) trước khi chạy test2.
- **test2 (L2, chạy 1 lần): 26/30 = 86.7%** — nhãn và lý do từng câu: [labels/test2_labels.json](labels/test2_labels.json); trace: `results/test2/L2_e5_gemini35lite/`.
  - Theo nhóm: bảng 6/6, ảnh 4/5, biểu đồ 2/5, multi-hop 4/4, text 4/4, thiếu bằng chứng 6/6.
  - Lỗi: AT2-C1, AT2-C3 từ chối nhầm (không lấy được giá trị cột của biểu đồ Figure 8 / Figure 4); AT2-C2 lỗi chép vision (p031: ghi Gold/Platinum/Indium cùng ~100%, ảnh gốc chỉ Indium chạm đỉnh); AT2-I5 khẳng định sai Cu có biểu đồ xanh (ảnh gốc p028: Cu trắng).
  - Điểm yếu chính: **biểu đồ cột** — vision ước lượng giá trị cột không in số kém, và model lite không tự sửa được khi xem ảnh trang.
  - Lỗi hệ thống 0/30; thời gian trung vị 16.2 s/câu; chi phí LLM $0 (free tier), embedding local $0.
  - Baseline L0_e5_text_dense (chỉ text layer, dense): page_hit@3 15/24, cite đủ trang gold 12/24, từ chối nhầm 8/24 (chỉ số tự động, chưa chấm tay) — so với L2: 22/24, 20/24, 2/24.
- Chi phí phần nâng cao: ≈ $5.4 (agent runs $4.9, vision $0.50, embedding $0.01); vòng 3 miễn phí.

## Tái lập
```bash
mkdir -p advanced/raw && curl -L -o advanced/raw/mcs2024.pdf https://pubs.usgs.gov/periodicals/mcs2024/mcs2024.pdf
pip install --target advanced/.vendor pymupdf==1.24.10
PYTHONPATH=advanced/.vendor python -c "import fitz;[p.get_pixmap(dpi=150).save(f'advanced/pages/p{i:03d}.png') for i,p in enumerate(fitz.open('advanced/raw/mcs2024.pdf'),1)]"
python advanced/src/validate_benchmark.py
python advanced/src/extract.py            # dùng cache extracted/vision nếu có
python advanced/src/build_index.py
python advanced/src/run.py --split test2 --configs V12_final V0_text_dense   # khi có API credit
# Vòng 3 miễn phí (đã chạy): .env có GEMINI_API_KEY, LLM_PROVIDER=gemini, EMB_PROVIDER=local
pip install sentence-transformers torch      # e5-small tải từ Hugging Face lần đầu
EMB_PROVIDER=local python advanced/src/build_index.py
EMB_PROVIDER=local python advanced/src/run.py --split dev --configs L2_e5_gemini35lite
EMB_PROVIDER=local python advanced/src/run.py --split test2 --configs L2_e5_gemini35lite L0_e5_text_dense
```
