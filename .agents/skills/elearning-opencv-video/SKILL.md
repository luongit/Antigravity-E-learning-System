---
name: elearning-opencv-video
description: Giai đoạn 5 - Render video bằng OpenCV từ ảnh slide, MP3 và SRT. Giữ hiệu ứng Canny, tô màu, bàn tay và phụ đề 42px. Dùng khi người dùng đã chọn OpenCV hoặc gọi trực tiếp skill này.
---

# E-Learning Stage 5 — OpenCV: Render Video Whiteboard Animation & Hoạt Ảnh Sư Phạm

Chỉ chạy khi người dùng đã chọn OpenCV hoặc gọi trực tiếp skill này. Nếu chưa rõ engine, đọc [elearning-video](../elearning-video/SKILL.md) để điều phối lựa chọn engine.

Pre-flight: `python core/preflight.py "output/<ma-mon-hoc>/video-<x>" --stage video --engine opencv`. Giữ nguyên engine Python trong `core/whiteboard_engine.py`.

## 1. Vai trò & Mục tiêu
Biến các slide Infographic phẳng và các file âm thanh giọng đọc thành Video bài giảng hoạt họa Whiteboard Animation 1080p sinh động, chuẩn mực sư phạm cao, thu hút người học từ giây đầu tiên.

- **Thư mục đầu vào:**
  - `output/<ma-mon-hoc>/video-<x>/images/` (ảnh slide `slide-1.png`...)
  - `output/<ma-mon-hoc>/video-<x>/mp3/` (file âm thanh `mp3-1.mp3` và phụ đề `mp3-1.srt`...)
- **Thư mục đầu ra:**
  - `output/<ma-mon-hoc>/video-<x>/Video <X> - <Tên Video>.mp4`

---

## 2. Các Nguyên Tắc Kỹ Thuật & Sư Phạm Bất Biến

### 1. Hiệu ứng Whiteboard Sketch 2 Pha Chuẩn
Không dùng hiệu ứng cắt dán hộp cứng hoặc chuyển cảnh đột ngột. Áp dụng cơ chế 2 pha mượt mà:
- **Pha 1 - Nét chì phác thảo (Outline Sketch):** Dùng thuật toán Canny Edge + Dilate tạo nét vẽ đen trên nền trắng, bàn tay cầm bút (`assets/drawing-hand.png`) lướt theo nét vẽ trong $0.9s - 1.2s$.
- **Pha 2 - Tô màu dần (Color Fade-in):** Hòa trộn dần màu nguyên bản từ mờ sang rõ nét trong $0.3s - 0.4s$, bàn tay lướt ra ngoài màn hình.

### 2. Thứ tự Sư phạm Whiteboard Bắt buộc
1. **Vẽ ảnh minh họa trước ($0.0s \to 1.3s$):** Đóng vai trò là mỏ neo thị giác (Visual Anchor).
2. **Vẽ tiêu đề chính ($1.3s \to 2.8s$):** Định vị tên bài học / tên slide.
3. **Hiển thị nội dung chi tiết theo lời giảng:** Từng bước hoặc từng gạch đầu dòng xuất hiện đúng theo timestamp trong audio SRT.

### 3. Nguyên tắc Cắt ảnh Bất biến: Pure White Gap Slicing
- Khi bóc tách các dòng văn bản hoặc khối nội dung động: **BẮT BUỘC** phải dò tìm các hàng/cột pixel **hoàn toàn là màu trắng (#FFFFFF)** nằm giữa các đoạn văn bản/tiêu đề để làm ranh giới cắt hộp (`Bounding Box`).
- **Tuyệt đối KHÔNG** cắt ước lượng tọa độ ngang chừng làm cắt ngang qua thân chữ hoặc lẹm viền văn bản.

### 4. Quy chuẩn Diễn hoạt Vòng tròn (Clockwise Circular Flow)
- Với slide chu trình (như quy trình 5 bước, PDCA): Diễn hoạt tuần tự theo **chiều kim đồng hồ**: Bước 1 (Đỉnh 12h) $\to$ Bước 2 (Góc 2h) $\to$ Bước 3 (Góc 5h) $\to$ Bước 4 (Góc 7h) $\to$ Bước 5 (Góc 10h). Tuyệt đối không quét ngang trái $\to$ phải làm đảo lộn thứ tự logic.

### 5. Đa dạng hóa Hình thức Chuyển động (Motion Variety)
Không lạm dụng duy nhất một hiệu ứng cho toàn bộ các slide. Agent tự động nhận diện bố cục để chọn:
- **Move / Slide-in (Trượt mượt có hướng):** `Move Left`, `Move Right`, `Move Top`, `Move Bottom` cho các bước quy trình, danh sách mục tiêu.
- **Pop / Scale-up nhẹ (90% $\to$ 100%):** Dành cho hộp cảnh báo, trọng tâm, dấu hỏi lớn.
- **Smooth Fade-in:** Mờ dần hiện rõ dứt khoát trong 0.2s–0.35s.
- **Whiteboard Hand-drawing (Vẽ tay):** Dành cho sơ đồ tư duy, cây phân nhánh, hình minh họa vector.

### 6. Quy chuẩn Phụ đề Subtitle 48px & Phân đoạn Ngắn
- **Typography:** Font chuẩn `assets/fonts/BeVietnamPro-Bold.ttf`, cỡ chữ **48px**.
- **Định dạng:** Chữ màu đen (#1A202C), không viền stroke, không dùng hộp nền che khuất tranh, căn giữa ở đáy màn hình ($y \approx 960$).
- **Đồng bộ:** Hiển thị từng cụm phân đoạn ngắn (6–8 từ) theo timestamp audio SRT.

### 7. Quy chuẩn Camera: Cố định 100% (Static Camera)
- Không lia máy, không zoom ra/vào gây mất tập trung. Khung hình 16:9 cố định hoàn toàn, các chi tiết tự chuyển động bên trong khung hình tĩnh.
- **Giữ cảnh cuối (Final Hold):** Giữ nguyên toàn cảnh slide hoàn chỉnh ít nhất $0.5s - 1.0s$ trước khi chuyển cảnh tiếp theo.

---

## 3. Kiến Trúc Lệnh Thực Thi

Agent tận dụng module `core/whiteboard_engine.py` để render từng slide thành video tạm, sau đó dùng FFmpeg/PyAV ghép âm thanh và nối thành video hoàn chỉnh:

```python
from core.whiteboard_engine import (
    create_sketch_image,
    apply_sketch_to_color_reveal,
    draw_subtitle_42px
)
# Render từng frame 1080p theo timestamp SRT -> Ghi vào video stream MP4 -> Mux audio MP3
```

Video thành phẩm được lưu tại:  
`output/<ma-mon-hoc>/video-<x>/Video <X> - <Tên Video>.mp4`
