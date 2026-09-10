---
name: elearning-molstar-video
description: Giai đoạn 5 - Render video E-Learning và diễn họa trực quan Cấu trúc Sinh học 3D, Chuỗi xoắn đôi ADN/RNA, Protein & Enzyme bằng Molstar và dữ liệu RCSB PDB.
---

# Kỹ Năng: elearning-molstar-video (Giai Đoạn 5 — Molstar & Biomolecular 3D Engine)

## 1. Giới Thiệu & Bản Chất Kỹ Thuật

`elearning-molstar-video` là engine sản xuất video bài giảng chuyên sâu cho lĩnh vực **Sinh học Phân tử, Di truyền học, Hóa sinh học, Dược học, Cấu trúc ADN/RNA, Protein, Enzyme và Phân tử Sinh học 3D** dựa trên nền tảng **Molstar (Mol\*)** kết hợp ngân hàng dữ liệu cấu trúc nguyên tử toàn cầu **RCSB Protein Data Bank (PDB)** và WebGL 3Dmol.

### 📌 Liên Kết Tham Khảo Chính Thức
- **Mol\* (Molstar - 3D Biomolecular Visualization Engine):**
  - GitHub: [github.com/molstar/molstar](https://github.com/molstar/molstar)
  - Documentation: [molstar.org/viewer-docs/](https://molstar.org/viewer-docs/)
  - Live Viewer: [molstar.org/viewer/](https://molstar.org/viewer/)
- **PDB (RCSB Protein Data Bank - Nguồn dữ liệu ADN, RNA, Protein):**
  - Website: [rcsb.org](https://www.rcsb.org/)

---

## 2. Tính Năng Nổi Trội Phục Vụ Bài Giảng Sinh Học

### 2.1. Mô Phỏng 3D Chuỗi ADN, RNA & Protein
- Tải trực tiếp các cấu trúc phân tử sinh học từ thư viện RCSB PDB (thông qua mã PDB ID như `1BNA` cho ADN B-form, `1EHZ` cho tRNA, `1TUP` cho Protein p53, `4HHB` cho Hemoglobin, `1TRN` cho Insulin).
- Tự động sinh cấu trúc B-DNA nguyên tử chuẩn xác ngay cả trong môi trường offline hoàn toàn.

### 2.2. Đa Dạng Chế Độ Hiển Thị Cấu Trúc Sinh Học
- **`cartoon`**: Dạng băng dây xoắn $\alpha$ (Alpha helix) và phiến $\beta$ (Beta sheet) cho chuỗi polypeptide của Protein.
- **`ball-and-stick`**: Dạng quả cầu - que cho các nucleotide ADN/RNA, hiển thị rõ khung đường - photphat và các vòng thơm bazơ nitơ.
- **`spacefill / sphere`**: Hiển thị mô hình bán kính van der Waals, mật độ điện tích và bề mặt tiếp xúc phân tử.

### 2.3. Bảng Màu Nhận Diện Bazơ Nitơ & Liên Kết Hydrogen
- Phân biệt màu sắc trực quan:
  - 🔵 **Adenin (A)**: Xanh Cyan `#38BDF8`
  - 🔴 **Thymin (T)**: Đỏ Rose `#FB7185`
  - 🟢 **Guanin (G)**: Xanh ngọc Emerald `#34D399`
  - 🟡 **Xitôzin (C/X)**: Vàng hổ phách `#FBBF24`
  - 🟣 **Khung Phốtphat-Đường**: Tím chàm Indigo `#818CF8`
- Thể hiện nguyên tắc bổ sung: $A = T$ (2 liên kết H) và $G \equiv X$ (3 liên kết H).

### 2.4. Hoạt Ảnh Quay 360° & Đóng Gói Slide 2 Trong 1
- Xoay 360 độ mượt mà quanh trục Y để quan sát toàn diện rãnh lớn (Major groove), rãnh nhỏ (Minor groove) và chu kỳ xoắn $3.4\text{ nm}$ ($10\text{ cặp bazơ / vòng}$).
- Tự động đóng gói thành slide PowerPoint `.pptx` và tài liệu PDF `.pdf` 16:9 sắc nét.

---

## 3. Kiến Trúc Tích Hợp & Thư Mục Sạch (Clean Output Policy)

```text
Hyperframes E-learning/
├── assets/
│   ├── libs/
│   │   ├── 3Dmol-min.js            # Thư viện 3D WebGL Biomolecular 100% offline (541 KB)
│   │   └── three.min.js            # Thư viện Three.js WebGL (603 KB)
│   ├── models/
│   │   └── 1bna.pdb                # Cấu trúc nguyên tử ADN B-form Dodecamer chuẩn
│   └── templates/
│       └── molstar_bio.html        # Template 16:9 Full HD, HUD Card & 3D Biomolecule
├── core/
│   └── molstar_engine.py           # Wrapper Python: Tra cứu PDB, render WebGL & xuất video
├── engines/
│   └── molstar/
│       └── export_slides.py        # Đóng gói PowerPoint PPTX & PDF 16:9
└── output/<ma-mon-hoc>/video-<x>/  # Thư mục học liệu sạch chứa kết quả hoàn thiện
```

---

## 4. Quy Trình Thực Thi 4 Bước (Execution Workflow)

```
[1. Script & Voice] ──> [2. Tra Cứu PDB] ──> [3. Render WebGL] ──> [4. Audio & Slide]
  script.md, mp3, srt     1BNA, Cartoon/Stick    Puppeteer 1080p30       Vocal + Lo-Fi + PPTX
```

### Bước 1: Pre-flight Check
- Kiểm tra Node.js và Puppeteer.
- Kiểm tra file `script.md`, `mp3-1.mp3`, `mp3-1.srt`.

### Bước 2: Trích Xuất & Sinh Cấu Hình Sinh Học
- Đọc `script.md` trích xuất tên phân tử hoặc mã PDB ID (Ví dụ: ADN B-form $\to$ `1BNA`).
- Lưu cấu hình vào `bio_config.json`.

### Bước 3: Dựng Cảnh HTML & Ghi Hình Video WebGL
- Inject cấu hình JSON và dữ liệu PDB vào `assets/templates/molstar_bio.html`.
- Ghi hình video chuyển động xoay 360 độ qua Puppeteer và pipe FFmpeg thành `raw_bio.mp4`.

### Bước 4: Đóng Gói Thành Phẩm Hoàn Chỉnh
- Hòa trộn giọng đọc Edge-TTS + Nhạc nền Lo-Fi + Phụ đề SRT viền mờ đáy thành file MP4 hoàn thiện.
- Xuất PowerPoint PPTX và PDF 16:9.

---

## 5. Mẫu Cấu Hình & Code Thực Thi Python

```python
from pathlib import Path
from core.molstar_engine import MolstarEngine

v_dir = Path("output/buni-overview/video-1")
engine = MolstarEngine(v_dir)

# 1. Tra cứu phân tử sinh học và lấy dữ liệu PDB
bio_config = engine.resolve_biomolecule("adn")
pdb_path, pdb_text = engine.get_or_generate_pdb_data(bio_config["pdb_id"], v_dir / "molecule.pdb")
engine.create_bio_config(bio_config["pdb_id"], v_dir / "bio_config.json", extra_meta=bio_config)

# 2. Sinh trang HTML & Chụp ảnh Slide tĩnh
html_path = v_dir / "view_dna.html"
engine.generate_html_page(bio_config, pdb_text, html_path)
engine.render_still(html_path, v_dir / "slide_molstar_demo.png", progress_ratio=0.25)

# 3. Ghi hình video chuyển động xoay 360 độ (5s @ 30fps)
raw_vid = v_dir / "raw_bio.mp4"
engine.render_video(html_path, raw_vid, duration_sec=5.0, fps=30)

# 4. Ghép nối Giọng đọc Edge-TTS + Nhạc nền Lo-Fi + Phụ đề SRT
final_vid = v_dir / "video_molstar_demo.mp4"
engine.merge_audio_and_subtitles(
    raw_video=raw_vid,
    audio_path=v_dir / "mp3" / "mp3-1.mp3",
    srt_path=v_dir / "mp3" / "mp3-1.srt",
    output_video=final_vid,
    bgm_path=Path("assets/audio/bg-lofi-tech.mp3")
)

# 5. Đóng gói PowerPoint PPTX & PDF 16:9
engine.export_slides(
    [{"html_path": html_path, "ratio": 0.25}],
    output_dir=v_dir,
    format_type="all",
    base_name="slides_molstar"
)
```
