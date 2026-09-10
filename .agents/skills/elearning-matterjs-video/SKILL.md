---
name: elearning-matterjs-video
description: Giai đoạn 5 - Render video E-Learning và mô phỏng trực quan Vật lý Cơ học, Động lực học 2D bằng Matter.js.
---

# Kỹ Năng: elearning-matterjs-video (Giai Đoạn 5 — Matter.js 2D Physics Engine)

## 1. Giới Thiệu & Bản Chất Kỹ Thuật

`elearning-matterjs-video` là engine sản xuất video học liệu và bài giảng chuyên sâu cho các môn **Vật lý đại cương, Cơ học lý thuyết, Động lực học chất điểm & vật rắn 2D**, dựa trên **Matter.js** — thư viện mô phỏng vật lý 2D chuẩn xác hàng đầu hiện nay.

### 🌟 Điểm Vượt Trội Của Matter.js:
1. **Mô Phỏng Động Lực Học Vật Rắn (Rigid Body Dynamics):**
   - Trọng trường $g$, lực cản không khí, véc-tơ vận tốc $\vec{v}$, véc-tơ gia tốc $\vec{a}$.
   - Chuyển động ném ngang, ném xiên với quỹ đạo Parabol trực quan.
2. **Va Chạm & Bảo Toàn Cơ Năng (Collisions & Conservation):**
   - Va chạm hoàn toàn đàn hồi ($e = 1.0$), va chạm mềm ($e = 0$), bảo toàn động lượng và động năng.
3. **Cơ Cấu Liên Kết & Ràng Buộc (Constraints & Springs):**
   - Hệ con lắc đơn, con lắc kép hỗn loạn (double pendulum), hệ con lắc lò xo dao động điều hòa, ròng rọc cơ học.
4. **Vẽ Quỹ Đạo Chuyển Động Sống Động (Trajectory Tracing):**
   - Tự động lưu vết chuyển động $(x, y)$ tạo đường quỹ đạo phát sáng neon và mũi tên véc-tơ vận tốc tức thời theo thời gian thực.
5. **Đóng Gói Slide 2 Trong 1 (PowerPoint & PDF 16:9):**
   - Chụp snapshot quỹ đạo cơ học ở trạng thái trực quan nhất để đóng gói thành slide PowerPoint (`.pptx`) và tài liệu PDF 16:9 (`.pdf`) qua `core/pptx_engine.py`.

---

## 2. Quy Chuẩn Kỹ Thuật & Thư Mục Sạch (Clean Output Policy)

- **Engine lõi trung tâm:** `core/matterjs_engine.py`.
- **Thư viện cục bộ:** `assets/libs/matter.min.js`.
- **Template giao diện:** `assets/templates/matterjs_physics.html`.
- **Thư mục xuất slide:** `engines/matterjs/export_slides.py`.
- **Thư mục học liệu sạch:** Toàn bộ thành phẩm xuất trực tiếp vào `output/<ma-mon-hoc>/video-<x>/`:
  - `video_matterjs.mp4`: Video Full HD 1080p 30fps mượt mà.
  - `slides_matterjs.pptx`: Slide trình chiếu PowerPoint 16:9.
  - `slides_matterjs.pdf`: Tài liệu PDF 16:9.

---

## 3. Quy Trình Thực Thi 4 Bước (Execution Workflow)

```
[1. Script & Params] ──> [2. Calc & Config JSON] ──> [3. Matter.js WebGL] ──> [4. Audio & Subtitles]
   script.md, v0, α          physics_config.json          Puppeteer 30fps MP4        FFmpeg amix & sub
```

### Bước 1: Pre-flight Check (Kiểm Tra Môi Trường)
- Kiểm tra `assets/libs/matter.min.js`.
- Kiểm tra Node.js Puppeteer và FFmpeg.
- Đọc file kịch bản `output/<ma-mon-hoc>/video-<x>/script.md` để trích xuất bài toán cơ học:
  - Vận tốc đầu $v_0$ (m/s)
  - Góc ném $\alpha$ (độ)
  - Gia tốc trọng trường $g$ ($9.8\text{ m/s}^2$ hoặc $10\text{ m/s}^2$)
  - Hệ số đàn hồi $e$, ma sát $\mu$.

### Bước 2: Tính Toán Cơ Học & Xuất Config JSON
- Gọi `MatterJSEngine.build_projectile_config()` hoặc `build_collision_config()` để tự động tính toán:
  - $v_x = v_0 \cos\alpha$, $v_y = -v_0 \sin\alpha$
  - Tầm cao cực đại $H_{max} = \frac{v_0^2 \sin^2\alpha}{2g}$
  - Tầm xa cực đại $L_{max} = \frac{v_0^2 \sin(2\alpha)}{g}$
  - Thời gian bay $t_{flight} = \frac{2 v_0 \sin\alpha}{g}$
- Ghi dữ liệu ra `physics_config.json`.

### Bước 3: Đóng Gói HTML & Ghi Hình Video
- Gọi `MatterJSEngine.generate_html_page(...)` để tạo trang mô phỏng HTML 16:9.
- Chụp ảnh slide tĩnh qua `MatterJSEngine.render_still(...)`.
- Ghi hình video chuyển động vật lý mượt mà qua `MatterJSEngine.render_video(...)`.

### Bước 4: Hoàn Thiện Video Bài Giảng
- Gọi `MatterJSEngine.merge_audio_and_subtitles()` để ghép nối:
  - Video mô phỏng vật lý
  - Giọng đọc Edge-TTS Nam Minh
  - Nhạc nền Lo-Fi nhẹ
  - Phụ đề SRT viền mờ đáy không stroke lem luốc.
- Đóng gói slide PPTX & PDF qua `engines/matterjs/export_slides.py`.

---

## 4. Ví Dụ Mã Lệnh Python Điều Phối

```python
from pathlib import Path
from core.matterjs_engine import MatterJSEngine

video_dir = Path("output/vat-ly-10/video-1")
engine = MatterJSEngine(video_dir)

# 1. Sinh cấu hình ném xiên góc 45 độ, v0 = 22 m/s
config_data = engine.build_projectile_config(v0=22.0, angle_deg=45.0, restitution=0.75)
config_path = engine.create_simulation_config(config_data, video_dir / "physics_config.json")

# 2. Sinh trang HTML mô phỏng
html_path = engine.generate_html_page(config_data, video_dir / "view_projectile.html")

# 3. Ghi hình video 6s @ 30fps
raw_video = engine.render_video(html_path, video_dir / "raw_projectile.mp4", duration_sec=6.0, fps=30)

# 4. Ghép giọng đọc và phụ đề SRT
final_video = engine.merge_audio_and_subtitles(
    raw_video=raw_video,
    audio_path=video_dir / "mp3" / "mp3-1.mp3",
    srt_path=video_dir / "mp3" / "mp3-1.srt",
    output_video=video_dir / "video_matterjs.mp4",
    bgm_path=Path("assets/audio/bg-lofi-tech.mp3")
)
```
