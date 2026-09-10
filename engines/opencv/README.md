# OpenCV Whiteboard Video Engine

Engine vẽ tay hoạt ảnh bảng trắng Whiteboard Animation dùng chung cho toàn bộ dự án.

## Cơ chế hoạt động:
- Không sinh thư mục phụ hay cài đặt thư viện vào `output/`.
- Sử dụng mã nguồn trung tâm tại `core/whiteboard_engine.py` kết hợp Python Virtual Environment (`.venv`) ở gốc dự án.
- Đọc ảnh slide Infographic từ `output/<ma-mon-hoc>/video-<x>/images/` và audio từ `output/<ma-mon-hoc>/video-<x>/mp3/`.
- Xuất video MP4 trực tiếp vào thư mục học liệu `output/<ma-mon-hoc>/video-<x>/`.
