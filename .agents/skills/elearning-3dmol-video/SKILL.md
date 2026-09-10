---
name: elearning-3dmol-video
description: Giai đoạn 5 - Render video E-Learning và mô phỏng trực quan Hóa học, Cấu trúc Phân tử 3D bằng 3Dmol.js và RDKit.
---

# Kỹ Năng: elearning-3dmol-video (Giai Đoạn 5 — 3D Molecular Chemistry Engine)

## 1. Giới Thiệu & Bản Chất Kỹ Thuật

`elearning-3dmol-video` là engine sản xuất video học liệu và bài giảng chuyên sâu cho các môn **Hóa học đại cương, Hóa hữu cơ, Hóa sinh, Khoa học vật liệu và Dược phẩm**, dựa trên sự kết hợp hoàn hảo giữa:
- **RDKit (Open-Source Cheminformatics):** Thư viện tính toán hóa tin học hàng đầu thế giới, tự động chuyển đổi tên hợp chất tiếng Việt hoặc chuỗi SMILES sang tọa độ không gian 3D và tối ưu hóa năng lượng hình học (Force Field MMFF94).
- **3Dmol.js (WebGL Molecular Visualization):** Nền tảng diễn họa phân tử 3D siêu nhẹ chạy trên WebGL Canvas, hỗ trợ camera 360 độ, xoay phân tử mượt mà và đa dạng kiểu biểu diễn (`ball-and-stick`, `sphere/spacefill`, `stick`, `cartoon`).

---

## 2. Các Tính Năng Nổi Trội

1. **Nhận Diện Thông Minh Tên Hóa Học Tiếng Việt:**
   - Tự động nhận diện các hợp chất quen thuộc: Ethanol (Cồn etylic `CCO`), Axit Axetic (`CC(=O)O`), Etyl Axetat (`CCOC(C)=O`), Cafein (`CN1C=NC2=C1C(=O)N(C(=O)N2C)C`), Aspirin (`CC(=O)Oc1ccccc1C(=O)O`), Glucozơ, Benzen, Nước, Metan...
2. **Tối Ưu Hóa Năng Lượng Không Gian 3D Chuẩn Xác:**
   - RDKit tự động thêm nguyên tử Hydro ($H$), tính toán góc liên kết chuẩn (ví dụ góc liên kết $sp^3 \approx 109.5^\circ$, $sp^2 \approx 120^\circ$) và cân bằng lực trường trước khi xuất file `.sdf`.
3. **Bố Cục Slide Sư Phạm Đỉnh Cao 16:9:**
   - Bố cục 2 cột cân bằng đối xứng toán học:
     - **Cột trái:** Thẻ thông số phân tử (Công thức, Khối lượng mol, Chuỗi SMILES, Thống kê nguyên tử) và Thẻ phân tích nhóm chức/đặc trưng liên kết hóa học.
     - **Cột phải:** Viewport WebGL Canvas 3D sắc nét $1920\times 1080$, phân tử tự động quay 360 độ nhịp nhàng.
4. **Hòa Trộn Đa Âm Thanh & Phụ Đề Chuẩn:**
   - Ghép giọng đọc Edge-TTS Nam Minh, nhạc nền Lo-Fi thư thái và phụ đề SRT Be Vietnam Pro không viền đen stroke.
5. **Đóng Gói Slide 2 Trong 1:**
   - Chụp snapshot hoàn thiện của cấu trúc phân tử 3D để xuất ra slide PowerPoint (`.pptx`) và tài liệu PDF 16:9 (`.pdf`) qua `core/pptx_engine.py`.

---

## 3. Quy Trình Thực Thi 4 Bước (Execution Workflow)

```
[1. Script & SMILES] ──> [2. RDKit 3D SDF] ──> [3. 3Dmol WebGL] ──> [4. Audio & Subtitles]
   script.md, tên chất     runtime/tasks/*.sdf     Puppeteer 30fps MP4     FFmpeg amix & sub
```

### Bước 1: Pre-flight Check (Kiểm Tra Môi Trường)
- Kiểm tra RDKit: `python -c "import rdkit"`
- Kiểm tra 3Dmol.js: `assets/libs/3Dmol-min.js`
- Kiểm tra Puppeteer & FFmpeg.
- Đọc file kịch bản `output/<ma-mon-hoc>/video-<x>/script.md` để lấy tên chất, phản ứng hóa học hoặc mã SMILES.

### Bước 2: Sinh Cấu Trúc 3D Bằng RDKit
- Gọi `Mol3DEngine.resolve_smiles(query)` để lấy mã SMILES.
- Gọi `Mol3DEngine.smiles_to_sdf3d(smiles)` để tạo file tọa độ 3D `.sdf` và lấy `mol_block`.
- Lấy thông số phân tử bằng `Mol3DEngine.get_molecule_properties(smiles)`.

### Bước 3: Đóng Gói Trang WebGL & Render Video
- Tạo file HTML bài giảng bằng `Mol3DEngine.generate_html_page(...)`.
- Chụp ảnh slide tĩnh bằng `Mol3DEngine.render_still(...)`.
- Render video chuyển động phân tử 3D quay 360 độ mượt mà bằng `Mol3DEngine.render_video(...)`.

### Bước 4: Hoàn Thiện Video Bài Giảng
- Gọi `Mol3DEngine.merge_audio_and_subtitles()` để lồng ghép giọng đọc TTS, nhạc nền và phụ đề SRT ngắn.
- Xuất slide PowerPoint `.pptx` và `.pdf` qua `engines/3dmol/export_slides.py`.

---

## 4. Ví Dụ Mã Lệnh Python Điều Phối

```python
from pathlib import Path
from core.mol3d_engine import Mol3DEngine

video_dir = Path("output/hoa-hoc-10/video-1")
engine = Mol3DEngine(video_dir)

# 1. Nhận diện và sinh tọa độ 3D Ethanol
smiles = engine.resolve_smiles("Ethanol")  # 'CCO'
sdf_path, mol_block = engine.smiles_to_sdf3d(smiles)
mol_info = engine.get_molecule_properties(smiles, custom_name="Ethanol (Cồn Etylic)")

# 2. Sinh trang HTML 3Dmol
html_path = engine.generate_html_page(
    molecule_info=mol_info,
    mol_block=mol_block,
    output_html_path=video_dir / "view_ethanol.html",
    feature_title="Nhóm Chức Hydroxyl (-OH) Phân Cực",
    feature_desc="Tạo liên kết Hydro liên phân tử, nhiệt độ sôi 78.3°C, tan vô hạn trong nước."
)

# 3. Ghi hình video phân tử 3D 10s @ 30fps
raw_video = engine.render_video(html_path, video_dir / "raw_ethanol.mp4", duration_sec=10.0)

# 4. Ghép nối giọng đọc Nam Minh, nhạc nền và phụ đề SRT
final_video = engine.merge_audio_and_subtitles(
    raw_video=raw_video,
    audio_path=video_dir / "mp3" / "mp3-1.mp3",
    srt_path=video_dir / "mp3" / "mp3-1.srt",
    output_video=video_dir / "video_3dmol_ethanol.mp4",
    bgm_path=Path("assets/audio/bg-lofi-tech.mp3")
)
```
