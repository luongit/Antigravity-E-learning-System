---
name: elearning-manim-video
description: Giai đoạn 5 - Render video E-Learning và diễn họa trực quan Vật lý Lý thuyết, Sóng, Dao động, Thuật toán IT, Cấu trúc dữ liệu và Toán học STEM bằng Manim Community Edition.
---

# Kỹ Năng: elearning-manim-video (Giai Đoạn 5 — Manim Community Engine)

## 1. Giới Thiệu & Bản Chất Kỹ Thuật

`elearning-manim-video` là engine diễn họa chuyên sâu dựa trên **Manim Community Edition** (kế thừa từ công cụ diễn họa toán học kinh điển của 3Blue1Brown).
Đây là giải pháp số một cho các bài giảng **Toán học cao cấp, Vật lý lý thuyết, Sóng & Dao động, Công nghệ thông tin, Cấu trúc dữ liệu và Trí tuệ nhân tạo (AI/ML)**.

### 📌 Liên Kết Tham Khảo Chính Thức
- **Manim Community Edition:**
  - GitHub: [github.com/ManimCommunity/manim](https://github.com/ManimCommunity/manim)
  - Documentation: [docs.manim.community](https://docs.manim.community)
  - Examples & Gallery: [docs.manim.community/en/stable/examples.html](https://docs.manim.community/en/stable/examples.html)
- **Manim Sideview (VS Code Extension hỗ trợ Preview thời gian thực):**
  - GitHub: [github.com/EulerSim/Manim-Sideview](https://github.com/EulerSim/Manim-Sideview)

---

## 2. Các Tính Năng Nổi Trội Phục Vụ Bài Giảng Vật Lý & Toán Học

### 2.1. Diễn Họa Công Thức Toán Học ($\text{\LaTeX}$ & Unicode Pango) & Đồ Thị Động
- **Công thức chuẩn hóa:** Hiển thị sắc nét phương trình động lực học, tích phân xác định, đạo hàm/vi phân, ma trận chuyển vị, hệ phương trình vi phân phi tuyến.
- **Cơ chế Dual-Renderer thông minh:**
  - Tự động dùng `MathTex` nếu hệ thống có MiKTeX / TeXLive.
  - Tự động chuyển đổi sang `Text` Unicode chất lượng cao (font **Be Vietnam Pro**) nếu máy tính chưa cài sẵn LaTeX, bảo đảm 100% không bị lỗi gián đoạn biên dịch.
- **Đồ thị hàm số biến thiên ($y = f(x)$):** Vẽ mượt mà các hàm số đại số, lượng giác, hàm mũ, đường cong phân phối chuẩn Gauss kết hợp minh họa diện tích tích phân qua hình chữ nhật Riemann (`get_riemann_rectangles`).
- **Hình học & Véc-tơ không gian:** Biểu diễn véc-tơ vận tốc, gia tốc, lực, phép biến đổi ma trận (`LinearTransformationScene`) và phép quay không gian.

### 2.2. Mô Phỏng Hiện Tượng Vật Lý & Sóng Cơ / Sóng Điện Từ
- **Dao động & Sóng:** Biểu diễn trực quan sóng cơ học lan truyền $u(x, t) = A \cos(\omega t - kx + \varphi)$, hiện tượng giao thoa sóng 2 nguồn, sóng dừng và đồ thị dao động điều hòa.
- **Cơ cấu Dao động Cơ học:** Diễn họa con lắc đơn, con lắc kép, hệ lò xo - vật nặng dưới dạng phương trình vi phân giải tích.
- **Điện từ học & Trường:** Mô hình đường sức điện trường xung quanh điện tích điểm, từ trường của dòng điện tròn/ống dây solenoid và trường hấp dẫn.

### 2.3. Hoạt Ảnh Biến Đổi Hình Học (Morphing & Transformation)
- Biến đổi mượt mà từ một công thức toán học trừu tượng sang mô hình hình học trực quan tương ứng (ví dụ: biến đổi từ phương trình đường tròn $x^2 + y^2 = r^2$ thành hình tròn thực tế bằng `Transform` hoặc `ReplacementTransform`).

### 2.4. Diễn Họa Thuật Toán IT & Cấu Trúc Dữ Liệu
- Diễn họa từng bước Mảng (`Array`), Danh sách liên kết (`LinkedList`), Cây nhị phân (`BinaryTree`), Đồ thị (`Graph`) và các thuật toán kinh điển (Dijkstra, BFS/DFS, QuickSort).

---

## 3. Kiến Trúc Tích Hợp & Thư Mục Sạch (Clean Output Policy)

```text
Hyperframes E-learning/
├── assets/
│   └── templates/
│       └── manim_physics_math.py    # Template chuẩn Vật lý (Gauss, Sóng, Euler)
├── core/
│   ├── manim_engine.py              # Thư viện lõi Python điều phối render & đóng gói
│   └── pptx_engine.py               # Engine đóng gói Slide PowerPoint & PDF
├── engines/
│   └── manim/
│       └── export_slides.py         # Script xuất bản PPTX & PDF 16:9
├── runtime/
│   ├── tasks/                       # Script kịch bản sinh động (manim_scene_<x>.py)
│   └── cache/manim/                 # Cache video và media thô
└── output/<ma-mon-hoc>/video-<x>/   # Thư mục học liệu sạch chứa kết quả hoàn thiện
```

---

## 4. Quy Trình Thực Thi 4 Bước (Execution Workflow)

```
[1. Script & Voice] ──> [2. Sinh Mã Python] ──> [3. Render Scene] ──> [4. Audio & Subtitles]
  script.md, mp3, srt    manim_scene_<x>.py     Manim CLI (1080p30)     FFmpeg amix & SRT
```

### Bước 1: Pre-flight Check (Kiểm Tra Môi Trường)
- Kiểm tra Python & Manim: `python -m manim --version`.
- Kiểm tra FFmpeg: `ffmpeg -version`.
- Kiểm tra LaTeX (nếu có): `latex --version`.
- Kiểm tra file âm thanh `mp3/mp3-1.mp3` và phụ đề `mp3/mp3-1.srt`.

### Bước 2: Sinh Mã Nguồn Python Manim
- Kế thừa class `Scene` từ `manim`.
- Áp dụng bảng màu E-Learning chuẩn:
  - Nền tối: `self.camera.background_color = "#0F172A"`
  - Màu chủ đạo: `#38BDF8` (Cyan), `#F59E0B` (Amber), `#10B981` (Emerald), `#EF4444` (Rose Red).
  - Font chữ typography: `font="Be Vietnam Pro"`.
- Căn chỉnh thời lượng các animation (`run_time`, `wait`) khớp với nhịp điệu của file SRT.

### Bước 3: Render Video Raw & Trích Xuất Ảnh Slide Tĩnh
- Render video raw: `engine.render_scene(script_path, "SceneName", quality="1080p30")`.
- Trích xuất ảnh tĩnh hoàn thiện: `engine.render_still(script_path, "SceneName", output_image)`.

### Bước 4: Đóng Gói Hoàn Thiện (Audio + SRT + BGM) & Slide PPTX/PDF
- Ghép giọng đọc Edge-TTS + Nhạc nền Lo-Fi nhẹ (`volume=0.12`) + Phụ đề SRT viền mờ đáy không stroke qua `engine.merge_audio_and_subtitles()`.
- Đóng gói Slide PowerPoint (`.pptx`) và tài liệu PDF (`.pdf`) qua `engine.export_slides()`.

---

## 5. Các Mẫu Code Manim Chuẩn Cho Vật Lý & Toán Học

### Mẫu 1: Tích Phân Gauss & Tổng Riemann (`PhysicsMathScene`)
```python
import numpy as np
from manim import *

class PhysicsMathScene(Scene):
    def construct(self):
        self.camera.background_color = "#0F172A"

        # Tiêu đề công thức
        title = Text("f(x) = ∫₀^∞ e^(-x²) dx = √π / 2", font="Be Vietnam Pro", font_size=32, color="#38BDF8")
        title.to_edge(UP, buff=0.8)

        # Trục tọa độ 2D
        axes = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 1.4, 0.5], x_length=9, y_length=4.5, axis_config={"color": "#64748B"}).shift(DOWN * 0.6)
        
        # Đồ thị Gauss & Diện tích Riemann
        graph = axes.plot(lambda x: np.exp(-x**2), color="#F59E0B", stroke_width=4)
        area = axes.get_riemann_rectangles(graph, x_range=[-2.2, 2.2], dx=0.15, color="#EF4444", fill_opacity=0.45)

        self.play(Write(title))
        self.play(Create(axes), Create(graph))
        self.play(FadeIn(area))
        self.wait(2)
```

### Mẫu 2: Dao Động & Truyền Sóng Điều Hòa (`WaveSimulationScene`)
```python
import numpy as np
from manim import *

class WaveSimulationScene(Scene):
    def construct(self):
        self.camera.background_color = "#0F172A"

        formula = Text("u(x, t) = A · cos(ωt - kx + φ)", font="Be Vietnam Pro", font_size=32, color="#38BDF8").to_edge(UP, buff=0.8)
        axes = Axes(x_range=[0, 4 * np.pi, np.pi], y_range=[-1.5, 1.5, 0.5], x_length=10, y_length=4.5, axis_config={"color": "#475569"}).shift(DOWN * 0.5)
        sine_wave = axes.plot(lambda x: np.sin(x), color="#38BDF8", stroke_width=4)

        self.play(Write(formula))
        self.play(Create(axes), Create(sine_wave), run_time=1.5)
        self.wait(2)
```

### Mẫu 3: Đẳng Thức Euler Trong Mặt Phẳng Phức (`EulerIdentityScene`)
```python
from manim import *

class EulerIdentityScene(Scene):
    def construct(self):
        self.camera.background_color = "#0F172A"

        euler_eq = Text("e^(iπ) + 1 = 0", font="Be Vietnam Pro", font_size=40, color="#EF4444").to_edge(UP, buff=1.0)
        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-1.5, 1.5, 1], axis_config={"color": "#64748B"}).shift(DOWN * 0.5)
        unit_circle = Circle(radius=plane.get_x_unit_size(), color="#38BDF8", stroke_width=2.5).move_to(plane.c2p(0, 0))
        dot = Dot(plane.c2p(1, 0), color="#F59E0B", radius=0.1)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color="#F59E0B")

        self.play(Write(euler_eq))
        self.play(Create(plane), Create(unit_circle))
        self.play(GrowArrow(vector), FadeIn(dot))
        self.wait(2)
```

---

## 6. Lệnh Thực Thi Bằng Python

```python
from pathlib import Path
from core.manim_engine import ManimEngine

v_dir = Path("output/buni-overview/video-1")
engine = ManimEngine(v_dir)

# 1. Sinh script hoặc dùng template có sẵn
template_path = Path("assets/templates/manim_physics_math.py")

# 2. Render ảnh slide tĩnh
engine.render_still(template_path, "PhysicsMathScene", v_dir / "slide_physics_math.png")

# 3. Render video raw
raw_mp4 = engine.render_scene(template_path, "PhysicsMathScene", quality="1080p30")

# 4. Đóng gói audio Edge-TTS, BGM Lo-Fi và phụ đề SRT
engine.merge_audio_and_subtitles(
    raw_video=raw_mp4,
    audio_path=v_dir / "mp3" / "mp3-1.mp3",
    srt_path=v_dir / "mp3" / "mp3-1.srt",
    output_video=v_dir / "video_physics_math.mp4",
    bgm_path=Path("assets/audio/bg-lofi-tech.mp3")
)

# 5. Đóng gói slide PowerPoint PPTX & tài liệu PDF 16:9
engine.export_slides(
    [{"script_path": template_path, "scene_class": "PhysicsMathScene"}],
    output_dir=v_dir,
    format_type="all",
    base_name="slides_physics_math"
)
```
