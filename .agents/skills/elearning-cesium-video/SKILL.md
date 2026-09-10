---
name: elearning-cesium-video
description: Giai đoạn 5 - Render video E-Learning và diễn họa Quả địa cầu 3D, Bản đồ số, Địa hình & Không gian Địa lý bằng CesiumJS và Leaflet.
---

# Kỹ Năng: elearning-cesium-video (Giai Đoạn 5 — Cesium & 3D Globe Engine)

## 1. Giới Thiệu & Bản Chất Kỹ Thuật

`elearning-cesium-video` là engine sản xuất video bài giảng chuyên sâu cho lĩnh vực **Địa lý Tự nhiên, Địa lý Kinh tế, Thiên văn học, Bản đồ số (GIS), Địa hình 3D (Terrain / DEM) và Không gian Toàn cầu** dựa trên **CesiumJS** kết hợp **Leaflet** và WebGL 3D Globe.

### 📌 Liên Kết Tham Khảo Chính Thức
- **CesiumJS (3D Globe & Map Visualization Engine):**
  - GitHub: [github.com/CesiumGS/cesium](https://github.com/CesiumGS/cesium)
  - Documentation: [cesium.com/learn/cesiumjs/ref-doc/](https://cesium.com/learn/cesiumjs/ref-doc/)
  - Cesium Sandcastle (Interactive Demos): [sandcastle.cesium.com](https://sandcastle.cesium.com/)
- **Leaflet (2D Open-source Interactive Maps):**
  - GitHub: [github.com/Leaflet/Leaflet](https://github.com/Leaflet/Leaflet)
  - Documentation: [leafletjs.com/reference.html](https://leafletjs.com/reference.html)

---

## 2. Tính Năng Nổi Trội Phục Vụ Bài Giảng Địa Lý

### 2.1. Diễn Họa Quả Địa Cầu 3D (3D Digital Globe)
- Phóng to/thu nhỏ (Zoom), xoay quanh trục 360 độ, điều khiển góc nhìn camera (Heading, Pitch, Roll) đến bất kỳ tọa độ nào trên Trái Đất với độ phân giải cao.
- Hiệu ứng bầu khí quyển phát sáng (Atmospheric corona glow) và ánh sáng mặt trời tự nhiên.

### 2.2. Mô Phỏng Địa Hình & Độ Cao 3D (3D Terrain & DEM)
- Trực quan hóa độ cao các rặng núi hùng vĩ, thung lũng, cao nguyên (ví dụ: Dãy Himalaya, Đỉnh Everest $8,848.86\text{m}$, Hẻm vực Grand Canyon).
- Thước đo cao độ và bảng thông số tọa độ HUD hiển thị thời gian thực.

### 2.3. Biểu Diễn Dữ Liệu Địa Lý & Lớp Thông Tin (GeoJSON & Layers)
- Vẽ ranh giới quốc gia, các dòng hải lưu nóng/lạnh, hướng gió mùa, vành đai lửa Thái Bình Dương, phân bố dân cư và đới khí hậu toàn cầu.

### 2.4. Quỹ Đạo & Đường Đi (Fly-to Camera Animations)
- Hiệu ứng camera "bay" mượt mà giữa các địa danh (ví dụ: Tuyến bay thương mại Hà Nội $\to$ Paris, hoặc Con đường tơ lụa hàng hải cổ đại).
- Điểm đánh dấu (Waypoint Pin Marker) với sóng xung radar phát sáng (`pulse-ring`).

### 2.5. Đóng Gói Slide 2 Trong 1 (PowerPoint PPTX & PDF 16:9)
- Tự động chụp khung hình hoàn thiện của quả địa cầu và đóng gói thành slide thuyết trình PowerPoint `.pptx` và tài liệu PDF `.pdf` 16:9 sắc nét.

---

## 3. Kiến Trúc Tích Hợp & Thư Mục Sạch (Clean Output Policy)

```text
Hyperframes E-learning/
├── assets/
│   ├── libs/
│   │   ├── three.min.js            # Thư viện 3D WebGL Globe 100% offline (603 KB)
│   │   ├── leaflet.js              # Thư viện bản đồ 2D Leaflet (147 KB)
│   │   └── leaflet.css             # Style giao diện Leaflet
│   └── templates/
│       └── cesium_globe.html       # Template 16:9 Full HD, HUD Card & 3D Digital Globe
├── core/
│   └── cesium_engine.py            # Wrapper Python: Quản lý Waypoints, render WebGL & xuất video
├── engines/
│   └── cesium/
│       └── export_slides.py        # Đóng gói PowerPoint PPTX & PDF 16:9
└── output/<ma-mon-hoc>/video-<x>/  # Thư mục học liệu sạch chứa kết quả hoàn thiện
```

---

## 4. Quy Trình Thực Thi 4 Bước (Execution Workflow)

```
[1. Script & Voice] ──> [2. Sinh Geo JSON] ──> [3. Render WebGL] ──> [4. Audio & Slide]
  script.md, mp3, srt     waypoints, Lon/Lat     Puppeteer 1080p30       Vocal + Lo-Fi + PPTX
```

### Bước 1: Pre-flight Check (Kiểm Tra Môi Trường)
- Kiểm tra Node.js và Puppeteer.
- Kiểm tra file `script.md`, `mp3-1.mp3`, `mp3-1.srt`.

### Bước 2: Trích Xuất Tọa Độ & Sinh Cấu Hình JSON
- Đọc `script.md` trích xuất danh sách địa điểm cần khảo sát (Ví dụ: Dãy Himalaya $86.9250^\circ\text{E}, 27.9881^\circ\text{N}$, độ cao $20,000\text{m}$).
- Lưu cấu hình vào `geo_config.json`.

### Bước 3: Dựng Cảnh HTML & Ghi Hình Video WebGL
- Inject JSON vào `assets/templates/cesium_globe.html`.
- Ghi hình video chuyển động xoay quả địa cầu và camera Fly-to qua Puppeteer và pipe FFmpeg thành `raw_globe.mp4`.

### Bước 4: Đóng Gói Thành Phẩm Hoàn Chỉnh
- Hòa trộn giọng đọc Edge-TTS + Nhạc nền Lo-Fi + Phụ đề SRT viền mờ đáy thành file MP4 hoàn thiện.
- Xuất PowerPoint PPTX và PDF 16:9.

---

## 5. Mẫu Cấu Hình & Code Thực Thi Python

```python
from pathlib import Path
from core.cesium_engine import CesiumEngine

v_dir = Path("output/buni-overview/video-1")
engine = CesiumEngine(v_dir)

# 1. Cấu hình địa lý
geo_config = engine.build_landmark_config(
    landmark_name="Đỉnh Everest (Chomolungma) — Dãy Himalaya",
    latitude=27.9881,
    longitude=86.9250,
    altitude=20000,
    heading=45.0,
    pitch=-30.0,
    title="CẤU TẠO ĐỊA HÌNH DÃY NÚI HIMALAYA & ĐỈNH EVEREST",
    subtitle="Mô phỏng Quả địa cầu 3D • Tọa độ 27.9881°B, 86.9250°Đ • Quỹ đạo Camera Fly-to",
    elevation_m=8848.86
)
engine.create_geo_config(geo_config["waypoints"], v_dir / "geo_config.json", meta_extra=geo_config)

# 2. Sinh trang HTML & Chụp ảnh Slide tĩnh
html_path = v_dir / "view_globe.html"
engine.generate_html_page(geo_config, html_path)
engine.render_still(html_path, v_dir / "slide_cesium_demo.png", progress_ratio=0.5)

# 3. Ghi hình video chuyển động Quả địa cầu 3D (5s @ 30fps)
raw_vid = v_dir / "raw_globe.mp4"
engine.render_video(html_path, raw_vid, duration_sec=5.0, fps=30)

# 4. Ghép nối Giọng đọc Edge-TTS + Nhạc nền Lo-Fi + Phụ đề SRT
final_vid = v_dir / "video_cesium_demo.mp4"
engine.merge_audio_and_subtitles(
    raw_video=raw_vid,
    audio_path=v_dir / "mp3" / "mp3-1.mp3",
    srt_path=v_dir / "mp3" / "mp3-1.srt",
    output_video=final_vid,
    bgm_path=Path("assets/audio/bg-lofi-tech.mp3")
)

# 5. Đóng gói PowerPoint PPTX & PDF 16:9
engine.export_slides(
    [{"html_path": html_path, "ratio": 0.5}],
    output_dir=v_dir,
    format_type="all",
    base_name="slides_cesium"
)
```
