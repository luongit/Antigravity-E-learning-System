# 🎬 Thư Viện Video Minh Họa Trám Cảnh (B-Roll Video Library)

Thư mục này dùng để lưu trữ các đoạn video ngắn minh họa theo chủ đề phục vụ cho tính năng **Video Trám Cảnh (B-roll)** của hệ thống E-Learning HyperFrames.

---

## 📂 Cấu Trúc Phân Mục Theo Chủ Đề

Người dùng có thể đưa các video clip (định dạng `.mp4`, `.webm`, `.mov`) vào các thư mục chủ đề tương ứng:

```text
inputs/video-libraries/
├── Công nghệ ảo/             # Video về Công nghệ ảo, biểu đồ ảo...
├── Pháp luật/                # Video minh họa trong ngành luật sư, pháp luật...
├── Sử dụng máy tính/         # Video minh họa các hành động trên máy tính, điện thoại...
└── video chủ đề văn phòng/   # Video minh họa về các cảnh làm việc, công cụ văn phòng...
```

---

## ⚙️ Quy Chuẩn Kỹ Thuật Cho Video Clip

1. **Định dạng khuyến nghị:** `.mp4` (H.264, AAC).
2. **Tỷ lệ khung hình:** 16:9 (Độ phân giải Full HD `1920x1080` hoặc HD `1280x720`).
3. **Thời lượng clip lý tưởng:** Từ **6 giây đến 25 giây** (không cần quá dài, hệ thống sẽ tự động loop hoặc cắt đoạn vừa khớp với thời gian giảng).
4. **Âm thanh:** Video có thể có hoặc không có âm thanh (khi nhúng vào video bài giảng, hệ thống sẽ tự động tắt tiếng video minh họa để ưu tiên trọn vẹn giọng đọc bài giảng).

---

## 🎯 Cơ Chế Tự Động Hoá Trong HyperFrames (Trám Cảnh Ngữ Nghĩa & Thời Lượng Động)

1. **Phân định rõ lúc nào hiện Slide và lúc nào Trám Cảnh:**
   - **Hiện Slide:** Khi giảng viên đọc tiêu đề hoặc phân tích trực tiếp các gạch đầu dòng trên slide (áp dụng nguyên tắc SRT Lockstep: Nói đến đâu hiện đến đó).
   - **Trám Cảnh:** Khi giảng viên **thoát ly khỏi các gạch đầu dòng** để liên hệ thực tế, chia sẻ bối cảnh doanh nghiệp, đặt vấn đề định hướng, hoặc giải thích mở rộng.
2. **Thời lượng trám hoàn toàn động (Dynamic Duration):**
   - Không bị bó buộc 4–6 giây. Thời lượng trám được tính chính xác theo độ dài đoạn lời giảng ngoại cảnh trong file SRT (có thể 4s, 8s, 12s, 15s...).
   - Ngay khi lời giảng quay lại phân tích nội dung slide, video lập tức chuyển mượt về slide.
3. **Cơ chế Ghép Nối Đa Clip (Multi-Clip Chaining):**
   - Khi một đoạn giải thích ngoại cảnh kéo dài (ví dụ 10s–16s) vượt quá độ dài của một clip đơn trong thư viện, hệ thống sẽ tự động ghép nối liên tiếp 2–3 clip video khác nhau cùng chủ đề để tạo nhịp phim tài liệu chuyên nghiệp, tránh góc nhìn đơn điệu.
4. **Hình thức hiển thị duy nhất:**
   - **100% Full Cutaway 16:9 ($1920\times 1080$):** Cắt ngang dòng thời gian, phụ đề đáy và nhãn phân loại hiển thị sắc nét trên nền gradient tối mờ. Tuyệt đối không dùng khung nhỏ PiP nổi ở góc.

