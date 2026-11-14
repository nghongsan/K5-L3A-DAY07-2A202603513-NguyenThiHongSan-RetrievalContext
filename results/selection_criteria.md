# Tiêu chí chọn cấu hình (công bố trước khi chạy test)

Viết ngày 2026-11-14, trước mọi lần chạy retrieval/agent trên split **test**.

Cấu hình agent được chọn trên **dev** theo thứ tự ưu tiên:

1. **Abstention trên câu thiếu evidence** = 3/3 (bắt buộc; câu trả lời bịa bị coi là lỗi nặng nhất).
2. **Grounded answer** (chấm tay 0/1/2 trên 25 câu dev có đáp án): trung bình cao nhất.
3. **Từ chối nhầm** câu có đáp án: thấp nhất.
4. **Context Evidence Rate** và citation hợp lệ: cao nhất.
5. Hoà nhau → chọn cấu hình **rẻ hơn / nhanh hơn** (token, giây trung vị mỗi câu).

Baseline so sánh trên test: `A0_dense` (dense Day 6, top-3, 1500 ký tự, prompt v1, ≤2 search).
Sau khi chốt, test chỉ chạy **một lần** cho baseline và cấu hình đã chọn; không chỉnh gì sau khi xem test.

## Quyết định (chốt trên dev, trước khi chạy test)

| Cấu hình (dev, OpenAI gpt-4o-mini) | Abstention | Grounded mean /2 | Từ chối nhầm | Context Evidence | Citation hợp lệ | Chi phí 28 câu | Trung vị s/câu |
|---|---|---|---|---|---|---|---|
| A0_dense (baseline) | 3/3 | 1.84 | 2/25 | 24/25 | 30/31 | $0.0095 | 2.7 |
| A2_rerank | 3/3 | 2.00 | 0/25 | 25/25 | 38/39 | $0.0263 | 5.0 |
| A4_dense_fix | 3/3 | 2.00 | 0/25 | 25/25 | 31/32 | $0.0098 | 3.2 |
| A6_rerank_fix | 3/3 | 2.00 | 0/25 | 25/25 | 35/36 | $0.0225 | 4.2 |
| A1_hybrid (chỉ số tự động) | 3/3 | ≤1.92 | 1/25 | 25/25 | – | $0.0142 | 3.1 |
| A5_hybrid_fix (chỉ số tự động) | 3/3 | ≤1.84 | 2/25 | 24/25 | – | $0.0143 | 3.7 |

A2, A4, A6 hoà ở tiêu chí 1–4 → tiêu chí 5: **chọn `A4_dense_fix`** (dense Day 6, top-3, 1500 ký tự/lần search,
≤2 search, prompt v2 yêu cầu citation inline, 1 lần citation-guard retry) — rẻ hơn ~2.3× và nhanh hơn A6.
A1/A5 không chấm tay vì đã thua ở tiêu chí 3 (có từ chối nhầm, nên grounded mean tối đa < 2.00).
Test sẽ chạy một lần cho `A0_dense` và `A4_dense_fix`.

## Sau test (ghi trước khi chạy test2)

Test chính thức: A0 grounded 2.00, A4 1.67 (n06 từ chối nhầm vì model tự chọn `chapter=4` cho câu chương 6).
Sửa sau test: `A7_dense_userfilter` = A4 nhưng bỏ tham số `chapter` khỏi tool (filter chỉ từ người dùng).
Vì bản sửa được gợi ý bởi test, kết quả test **không** được dùng để đánh giá A7; thay vào đó tạo **test2**
(m01-m06 + v01-v02, chốt trước khi chạy). A7 chỉ được kiểm tra trên dev (không chỉnh thêm), sau đó chạy
một lần trên test2 cùng A0 và A4.
