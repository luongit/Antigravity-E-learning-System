# Runtime Workspace & Temporary Execution Artifacts

> **Thư mục này chứa toàn bộ mã script sinh tự động, cấu hình tạm, cache và log phát sinh trong quá trình AI Agent thực thi theo từng trường hợp.**

## 1. Cấu Trúc
- `tasks/`: Chứa các script Python do AI Agent tạo thêm trong quá trình làm việc với từng video cụ thể (ví dụ: `build_full_video1_v3.py`, `build_full_video2.py`, `inspect_v2_slides.py`...).
- `cache/`: Cache ảnh nháp, canny edges, audio chunks, video frames tạm.
- `logs/`: File log chạy tác vụ.
- `archive/`: Lưu trữ các script cũ, thư viện cũ (như Piper TTS) để phục vụ tra cứu lịch sử.

## 2. Quy Tắc Quản Trị
- **AN TOÀN XÓA 100%:** Người dùng hoặc Agent có thể xóa sạch toàn bộ nội dung trong `runtime/tasks/`, `runtime/cache/`, `runtime/logs/` bất kỳ lúc nào mà **KHÔNG ẢNH HƯỞNG GÌ ĐẾN BỘ CORE (`core/`, `.agents/skills/`) HOẶC SẢN PHẨM HOÀN THIỆN TRONG `output/`**.
