# Day 7 — Agentic RAG

> **Bài làm — 2A202603513 Nguyễn Thị Hồng San.** Báo cáo: [report/individual/2A202603513_NguyenThiHongSan.md](report/individual/2A202603513_NguyenThiHongSan.md).
> Thử thách nâng cao (chưa đạt: test 25/30, test2 26/30): [advanced/README.md](advanced/README.md).
> Code: [src/](src/) · dữ liệu và benchmark: [data/chunks.json](data/chunks.json), [data/benchmark.json](data/benchmark.json) · kết quả và trace: [results/](results/).
>
> **Cách chạy** (Python 3.12, cùng môi trường với Day 6):
> ```bash
> pip install -r requirements.txt
> cp .env.example .env                                  # điền LLM_PROVIDER, LLM_MODEL, API key (không commit)
> python -m src.data_prep                               # (tuỳ chọn) dựng lại data/ từ repo Day 6 (DAY6_DIR)
> python -m src.build_index --out index/chroma          # nếu không có Chroma Day 6: dựng lại index e5 giống hệt
> export CHROMA_PATH=index/chroma                       #   (bỏ qua nếu dùng DAY6_DIR/chroma_db)
> python -m unittest discover -s tests -v               # unit test (mock chỉ kiểm tra code)
> python -m src.eval_retrieval --split dev              # so sánh retrieval/context trên dev
> python -m src.run_agent --split dev --configs A0_dense A1_hybrid A2_rerank A4_dense_fix A5_hybrid_fix A6_rerank_fix A7_dense_userfilter
> python -m src.run_agent --split test --configs A0_dense A4_dense_fix            # test chính thức (sau khi chốt A4)
> python -m src.run_agent --split test2 --configs A0_dense A4_dense_fix A7_dense_userfilter   # test mới cho bản sửa sau test
> python -m src.make_reviews --split test   # nhãn tay results/reviews/manual_labels_test.json -> starter/agent_metrics.py
> ```

**Bài cá nhân · Python 3.11+ · tiếp nối Day 6**

Dùng embedding và vector store từ Day 6 để xây một agent biết tìm bằng chứng, trả lời có nguồn và nhận biết khi không đủ thông tin. Bạn tự chọn kiến trúc, số tool và cách tổ chức retrieval.

> **Tùy chọn:** [Gợi ý dùng AI để lập trình](AGENT_SETUP.md) giúp bạn làm lab; phần này không bắt buộc và không tính điểm.

## Bài cần làm

![Agent tìm tài liệu trong kho Day 6 và trả lời có nguồn](assets/retrieval-pipeline.svg)

1. Kết nối dữ liệu, embedding và vector store Day 6.
2. Xây agent dùng model thật và ít nhất một khả năng truy xuất dữ liệu. Agent có thể dùng nhiều tool và nhiều lượt gọi.
3. Thử **ít nhất 3 phương pháp retrieval khác nhau**, trong đó có dense retrieval dùng vector store Day 6. Tự chọn các phương pháp còn lại; xem [gợi ý](GUIDE.md#2-thử-các-phương-pháp-retrieval).
4. Thử nhiều cấu hình, benchmark, phân tích lỗi và chọn cấu hình tốt trên **dev**; sau đó đánh giá trên **test**.

Benchmark tối thiểu có **24 câu**: dev gồm 15 câu có đáp án và 2 câu thiếu bằng chứng; test gồm 5 câu có đáp án và 2 câu thiếu bằng chứng. Xem [benchmark](BENCHMARK.md) và [rubric](RUBRIC.md).

## Thử thách nâng cao · +15 điểm

Index một tài liệu thực tế từ **100 trang** có bảng, ảnh và biểu đồ; xây agent truy xuất và trả lời các câu hỏi về nội dung đó. Hoàn thành [thử thách nâng cao](ADVANCED.md) và đạt **ít nhất 90% benchmark test** để nhận 15 điểm bonus. Phần cơ bản tối đa 85 điểm; toàn bài tối đa 100 điểm.

## Bắt đầu

1. Đọc [hướng dẫn](GUIDE.md), [rubric](RUBRIC.md) và [quy tắc](RULES.md).
2. Tạo repo cá nhân theo [cách nộp bài](SUBMISSION.md), chuẩn bị đầu ra Day 6 và model hỗ trợ tool calling.
3. Dùng hoặc thay thế [starter](starter/README.md); bạn cần kết nối model và vector store thật.
4. Chạy `python -m unittest discover -s tests -v`. Test mock chỉ kiểm tra code, không phải benchmark agent thật.

![Các bước thử nghiệm trên dev và đánh giá trên test](assets/experiment-loop.svg)

Nộp code, cách chạy, cấu hình, benchmark, trace và [báo cáo](report/individual/MSSV_HoTen.md). Thời gian ở [checkpoints](CHECKPOINTS.md) là gợi ý, có thể điều chỉnh theo lớp và phạm vi thử nghiệm.
