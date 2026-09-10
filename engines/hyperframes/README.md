# HyperFrames HTML/SVG Video Engine

Engine dựng cảnh hoạt ảnh Web công nghệ HTML/SVG/GSAP và chuyển đổi sang video MP4 1080p bằng HyperFrames CLI.

## Cơ chế hoạt động:
- Sử dụng công cụ HyperFrames CLI toàn cục hoặc npx.
- Các cảnh HTML/SVG được lưu gọn nhẹ tại `output/<ma-mon-hoc>/video-<x>/hyperframes/` (chỉ gồm các file mã nguồn nhẹ vài chục KB, tuyệt đối không chứa `node_modules`).
- Tự động nạp video B-roll từ `inputs/video-libraries/` cho các đoạn voice ngoại cảnh (hỗ trợ Multi-Clip Chaining).
- Xuất video MP4 trực tiếp vào thư mục học liệu `output/<ma-mon-hoc>/video-<x>/`.
