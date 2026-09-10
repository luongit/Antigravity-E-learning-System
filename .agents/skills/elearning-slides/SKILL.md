---
name: elearning-slides
description: Giai đoạn 3 - Tạo Slide bài giảng PowerPoint: Đóng gói toàn bộ ảnh slide thành file PowerPoint (.pptx) chuẩn tỷ lệ 16:9, mỗi slide sử dụng 1 ảnh chất lượng cao phủ kín 100% diện tích làm hình nền. Dùng khi người dùng yêu cầu tạo file PowerPoint hoặc xuất slide trình chiếu.
---

# E-Learning Stage 3: Đóng Gói Slide Bài Giảng PowerPoint (.pptx) & PDF 16:9

## 1. Vai trò & Mục tiêu
Chuyển đổi bài giảng thành tệp trình chiếu PowerPoint (`.pptx`) và tài liệu học tập PDF (`.pdf`) chuẩn tỷ lệ 16:9 Widescreen ($1920\times 1080$), hỗ trợ các nguồn sinh slide linh hoạt:
1. **Nguồn 1: HyperFrames Engine (HTML/SVG & JSON Spec v2):** Dựng trạng thái hoàn thiện từ cảnh HTML5/CSS3/SVG hoặc JSON Spec v2, bảo toàn 100% Visual Anchor SVG, hiệu ứng đổ bóng, code studio và font Be Vietnam Pro ExtraBold.
2. **Nguồn 2: Manim / 3Dmol / Matter.js / VexFlow / Cesium / Molstar / Virtual Lab:** Chụp trạng thái hoàn thiện từ các engine chuyên biệt.
3. **Nguồn 3: Ảnh Infographic sẵn có (Images Engine):** Đóng gói từ các ảnh trong `output/<ma-mon-hoc>/video-<x>/images/`.

- **Thư mục đầu vào:** `output/<ma-mon-hoc>/video-<x>/`
- **Tệp đầu ra:**
  - `output/<ma-mon-hoc>/video-<x>/slides.pptx` (Trình chiếu PowerPoint 16:9 full-bleed)
  - `output/<ma-mon-hoc>/video-<x>/slides.pdf` (Tài liệu phát tay PDF 16:9 sắc nét)

---

## 2. Quy Chuẩn Kỹ Thuật Bắt Buộc

1. **Tỷ lệ Khung hình 16:9 Widescreen Chuẩn Quốc Tế:**
   - Chiều rộng: `13.333 inches` (33.867 cm).
   - Chiều cao: `7.5 inches` (19.05 cm).
2. **Nguyên tắc Phủ kín 100% (Full Background):**
   - Mỗi slide sử dụng bố cục trắng tinh (Blank Layout - layout index 6).
   - Đặt ảnh từ tọa độ gốc `left = 0, top = 0`, kích thước trải rộng toàn bộ `width = slide_width, height = slide_height`.
   - Tuyệt đối không để viền đen hoặc dải trắng thừa ở các cạnh.
3. **Bảo toàn Thẩm mỹ Cao & Độc lập Thiết bị:**
   - Sử dụng ảnh snapshot trạng thái hoàn thiện ở độ phân giải gốc $1920\times 1080$.
   - Giữ nguyên 100% gradient, vector SVG, bóng đổ mờ và font chữ tiếng Việt, không bao giờ bị nhảy dòng hay lỗi font khi mở trên bất kỳ máy tính nào.

---

## 3. Cách Thức Thực Thi Theo Từng Engine

### Tùy chọn A: Xuất từ HyperFrames Engine
```bash
python core/hf_engine.py "output/<ma-mon-hoc>/video-<x>" --mode slides
```
- Tự động xuất cả file `slides_hyperframes.pptx` và `slides_hyperframes.pdf`.

### Tùy chọn B: Đóng gói từ Ảnh Infographic Sẵn Có
```bash
python core/pptx_engine.py "output/<ma-mon-hoc>/video-<x>/images" --format all --name slides
```

Sau khi hoàn thành, Agent báo cáo dung lượng tệp, tổng số slide và cung cấp link mở tệp trực tiếp cho người dùng.

