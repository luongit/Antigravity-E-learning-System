# Quy Chuẩn Tối Ưu Hóa Token & Vận Hành Pipeline (DevOps & Token Efficiency)

## 1. Nguyên Tắc Cắt Giảm Token Context Window
- **Loại trừ tệp binary & tài nguyên nặng:** Tuyệt đối không đọc toàn văn các tệp video (`.mp4`, `.mov`), tệp âm thanh (`.mp3`, `.wav`), font chữ (`.ttf`, `.otf`), ảnh (`.png`, `.jpg`), file nén hoặc file build/cache vào Context Window. Mọi mẫu tệp này đã được cấu hình trong `.antigravityignore`.
- **Chỉ nạp tệp văn bản cần thiết:** Khi cần tham chiếu kịch bản, chỉ đọc tệp kịch bản tương ứng (`script.md`, `voice-script.md`), cấu hình `JSON/YAML`, hoặc mã nguồn logic trong `core/`.

## 2. Quy Tắc Thực Thi Terminal Tinh Gọn (Quiet / Silent Flags)
- **Hạn chế log thừa (Terse Output):** Khi chạy các lệnh kiểm thử, build hoặc cài đặt qua terminal, luôn ưu tiên bổ sung các cờ lệnh im lặng/ngắn gọn (ví dụ: `pytest -q`, `pip install -q`, `npm install --no-audit --no-fund --silent`).
- **Giới hạn số dòng output:** Với các lệnh có khả năng in nhiều dòng output (quét file, log dài), luôn giới hạn bằng các lệnh lọc (`Select-Object -First N`, `head -n N`, hoặc logic script nội bộ) để tránh làm tràn token context.

## 3. Quy Chuẩn Kiểm Thử Browser & Screenshots
- **Mặc định KHÔNG kích hoạt Browser Auto-capture / Screenshots:** Trong toàn bộ quá trình lập trình, kiểm thử logic, sửa lỗi cú pháp, tổng hợp TTS, tạo slide PPTX hay chạy pipeline, KHÔNG tự ý mở browser subagent chụp ảnh màn hình lãng phí token.
- **Phạm vi duy nhất được phép dùng Visual Verification:** Chỉ kích hoạt browser/visual capture khi:
  1. Người dùng yêu cầu rõ ràng; hoặc
  2. Thực thi riêng khâu kiểm tra mỹ thuật hình ảnh của `elearning-images`; hoặc
  3. Kiểm tra chất lượng render frame của engine `HyperFrames` / `Virtual Lab`.
