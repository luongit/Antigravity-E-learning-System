---
name: elearning-vexflow-video
description: Giai đoạn 5 - Render video E-Learning và ký âm bản nhạc 2D, mô phỏng thanh cuộn Playhead và tổng hợp Piano Synth bằng VexFlow và Tone.js.
---

# Kỹ Năng: elearning-vexflow-video (Giai Đoạn 5 — VexFlow Music Engine)

## 1. Giới Thiệu & Bản Chất Kỹ Thuật

`elearning-vexflow-video` là engine sản xuất video bài giảng chuyên sâu cho lĩnh vực **Giáo dục Âm nhạc, Nhạc lý Căn bản, Đọc & Ký âm Bản nhạc (Music Notation), Xướng âm (Solfège) và Bàn phím Piano** dựa trên **VexFlow v4.2.2** kết hợp **Tone.js Web Audio**.

### 📌 Liên Kết Tham Khảo Chính Thức
- **VexFlow (HTML5 Music Notation Rendering):**
  - GitHub: [github.com/0xfe/vexflow](https://github.com/0xfe/vexflow)
  - Documentation: [vexflow.com](https://www.vexflow.com/)
  - Tutorials: [github.com/0xfe/vexflow/wiki/Tutorial](https://github.com/0xfe/vexflow/wiki/Tutorial)
- **Tone.js (Web Audio Framework cho Âm thanh & Nhạc cụ):**
  - GitHub: [github.com/Tonejs/Tone.js](https://github.com/Tonejs/Tone.js)
  - Documentation: [tonejs.github.io](https://tonejs.github.io/)

---

## 2. Tính Năng Nổi Trội Phục Vụ Bài Giảng Âm Nhạc

### 2.1. Tự Động Ký Âm & Vẽ Khuông Nhạc (Music Notation) Chuẩn Quốc Tế
- Hỗ trợ đầy đủ các khóa nhạc: **Khóa Sol (Treble Clef)** và **Khóa Pha (Bass Clef)**.
- Các loại hình nốt chuẩn: Nốt tròn (`w`), nốt trắng (`h`), nốt đen (`q`), nốt móc đơn (`8`), nốt móc kép (`16`).
- Chỉ số nhịp (Time Signature): 4/4, 3/4, 2/4, 6/8.
- Vạch nhịp (Barlines), dấu hóa (Thăng `#`, Giáng `b`, Bình), dấu lặng (Rests) và nối chùm nốt (Beaming).

### 2.2. Thanh Cuộn Phát Nhạc (Scrolling / Animated Playhead Cursor)
- Con trỏ laser thời gian thực (`#playhead`) lướt mượt mà qua từng vạch nhịp và từng nốt nhạc đúng theo Tempo (BPM) của giáo trình.
- Nốt nhạc đang phát sáng đèn rực rỡ với hiệu ứng hào quang (`box-shadow` / `drop-shadow`).

### 2.3. Bàn Phím Piano Minh Họa Trực Quan (Interactive Piano Keyboard)
- Dải bàn phím Piano 14 phím trắng/đen hiển thị trực tiếp ngay dưới khuông nhạc.
- Nốt nhạc vang lên đến đâu, phím đàn tương ứng sẽ tự động nhấn xuống và phát sáng màu xanh Cyan / vàng Amber rực rỡ, giúp người học vừa nhìn nốt trên khuông vừa định vị được phím đàn.

### 2.4. Tổng Hợp Âm Thanh Nhạc Cụ Piano Synth Chuẩn Phòng Thu
- Bộ dao động âm sắc phong phú (Harmonic Additive Synthesis) và đường bao ADSR, mô phỏng chân thực tiếng đàn Piano cho từng nốt nhạc.
- Hòa trộn đa kênh: Giọng đọc giáo viên (Edge-TTS) + Tiếng đàn Piano (Synth) + Nhạc nền Lo-Fi + Phụ đề SRT.

### 2.5. Đóng Gói Slide 2 Trong 1 (PowerPoint PPTX & PDF 16:9)
- Tự động chụp khung hình bản nhạc ở trạng thái hiển thị đẹp nhất và đóng gói thành slide thuyết trình PowerPoint `.pptx` và tài liệu PDF `.pdf` 16:9.

---

## 3. Kiến Trúc Tích Hợp & Thư Mục Sạch (Clean Output Policy)

```text
Hyperframes E-learning/
├── assets/
│   ├── libs/
│   │   ├── vexflow.min.js          # Thư viện VexFlow v4.2.2 offline 100%
│   │   └── tone.min.js             # Thư viện Tone.js Web Audio offline 100%
│   └── templates/
│       └── vexflow_music.html      # Template 16:9 Full HD, Dark Studio Theme & Piano Keyboard
├── core/
│   └── vexflow_engine.py           # Wrapper Python: Ký âm, tổng hợp âm thanh & render
├── engines/
│   └── vexflow/
│       └── export_slides.py        # Đóng gói PowerPoint PPTX & PDF 16:9
└── output/<ma-mon-hoc>/video-<x>/  # Thư mục học liệu sạch chứa kết quả hoàn thiện
```

---

## 4. Quy Trình Thực Thi 4 Bước (Execution Workflow)

```
[1. Script & Voice] ──> [2. Sinh Score JSON] ──> [3. Render Canvas] ──> [4. Audio & Slide]
  script.md, mp3, srt     notes_str, clef, BPM    Puppeteer 1080p30       Piano + Vocal + PPTX
```

### Bước 1: Pre-flight Check (Kiểm Tra Môi Trường)
- Kiểm tra Node.js và Puppeteer.
- Kiểm tra file `script.md`, `mp3-1.mp3`, `mp3-1.srt`.

### Bước 2: Phân Tích Kịch Bản & Xuất Cấu Hình JSON
- Đọc `script.md` trích xuất chuỗi ký âm (Ví dụ: Gam Đô Trưởng `C4/q, D4/q, E4/q, F4/q, G4/h, C5/h`).
- Lưu cấu hình vào `score_config.json`.

### Bước 3: Render Video & Tổng Hợp Tiếng Đàn
- Gọi `engine.generate_piano_synth_audio()` để tạo file âm thanh tiếng đàn `synth_piano.wav`.
- Gọi `engine.render_video()` qua Puppeteer ghi lại chuyển động của Playhead và phím đàn thành `raw_music.mp4`.

### Bước 4: Đóng Gói Thành Phẩm Hoàn Chỉnh
- Hòa trộn 3 luồng âm thanh (Vocal + Piano Synth + Lo-Fi) cùng phụ đề SRT chuẩn sư phạm thành file video MP4 hoàn thiện.
- Xuất PowerPoint PPTX và PDF 16:9.

---

## 5. Mẫu Cấu Hình & Code Thực Thi Python

```python
from pathlib import Path
from core.vexflow_engine import VexFlowEngine

v_dir = Path("output/buni-overview/video-1")
engine = VexFlowEngine(v_dir)

# 1. Cấu hình bản nhạc
score_config = engine.build_melody_config(
    notes_str="C4/q, D4/q, E4/q, F4/q, G4/h, C5/h",
    clef="treble",
    time_signature="4/4",
    tempo=100,
    title="BÀI HỌC: GAM TRƯỞNG & GIAI ĐIỆU CĂN BẢN",
    subtitle="Khóa Sol • Nhịp 4/4 • Tempo 100 BPM • Ký âm VexFlow & Diễn hoạt Piano Synth",
    key="Đô Trưởng (C Major)"
)
engine.create_score_config(score_config, v_dir / "score_config.json")

# 2. Sinh trang HTML & Chụp ảnh Slide tĩnh
html_path = v_dir / "view_music.html"
engine.generate_html_page(score_config, html_path)
engine.render_still(html_path, v_dir / "slide_vexflow_demo.png", progress_ratio=0.5)

# 3. Tạo âm thanh tiếng đàn Piano Synth
synth_wav = v_dir / "piano_melody.wav"
engine.generate_piano_synth_audio(score_config, synth_wav)

# 4. Ghi hình video chuyển động Playhead & Phím đàn (6s @ 30fps)
raw_vid = v_dir / "raw_music.mp4"
engine.render_video(html_path, raw_vid, duration_sec=6.0, fps=30)

# 5. Ghép nối Giọng đọc + Tiếng đàn Piano + Nhạc nền Lo-Fi + Phụ đề SRT
final_vid = v_dir / "video_vexflow_demo.mp4"
engine.merge_audio_and_subtitles(
    raw_video=raw_vid,
    audio_path=v_dir / "mp3" / "mp3-1.mp3",
    srt_path=v_dir / "mp3" / "mp3-1.srt",
    output_video=final_vid,
    synth_audio_path=synth_wav,
    bgm_path=Path("assets/audio/bg-lofi-tech.mp3")
)

# 6. Đóng gói PowerPoint PPTX & PDF 16:9
engine.export_slides(
    [{"html_path": html_path, "ratio": 0.5}],
    output_dir=v_dir,
    format_type="all",
    base_name="slides_vexflow"
)
```
