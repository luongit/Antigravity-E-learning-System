# 📋 Kiểm Kê Bản Quyền Toàn Bộ Engine & Thư Viện
> **ASK 01 – License Audit Report**
> Ngày kiểm tra: 2026-09-09  
> Phạm vi: Toàn bộ engine, framework, thư viện bên thứ ba trong hệ thống E-Learning Antigravity
> Mục tiêu thương mại: **Sản xuất học liệu E-Learning thương mại (BUNI / PTIT – Bachkhoa Aptech)**

---

## 🏆 Phân Loại Tổng Quan

| Màu | Ý nghĩa |
|-----|---------|
| ✅ **GIỮ LẠI** | License hoàn toàn phù hợp mục tiêu thương mại |
| ⚠️ **CẦN XEM XÉT** | Phù hợp nhưng có điều kiện hoặc rủi ro cần lưu ý |
| ❌ **LOẠI BỎ / THAY THẾ** | Vi phạm hoặc rủi ro pháp lý cao cho mục đích thương mại |

---

## 📦 PHẦN I — Thư Viện JavaScript (assets/libs/)

| # | Thư viện | File | License | Phân loại | Ghi chú |
|---|----------|------|---------|-----------|---------|
| 1 | **3Dmol.js** | `3Dmol-min.js` | BSD 3-Clause | ✅ GIỮ LẠI | Dùng thương mại tự do; chỉ cần giữ copyright notice |
| 2 | **Leaflet.js** | `leaflet.js` / `leaflet.css` | BSD 2-Clause | ✅ GIỮ LẠI | Hoàn toàn tự do thương mại |
| 3 | **Matter.js** | `matter.min.js` | MIT | ✅ GIỮ LẠI | Tự do thương mại không điều kiện |
| 4 | **Three.js** | `three.min.js` | MIT | ✅ GIỮ LẠI | Tự do thương mại không điều kiện |
| 5 | **Tone.js** | `tone.min.js` | MIT | ✅ GIỮ LẠI | Tự do thương mại không điều kiện |
| 6 | **VexFlow** | `vexflow.min.js` | MIT | ✅ GIỮ LẠI | Tự do thương mại không điều kiện |

> **Kết quả Phần I:** Tất cả 6 thư viện JS đều có license MIT hoặc BSD — **An toàn thương mại 100%**.

---

## 🐍 PHẦN II — Thư Viện Python (core/ & .venv/)

| # | Thư viện | pip package | License | Phân loại | Ghi chú |
|---|----------|-------------|---------|-----------|---------|
| 1 | **python-pptx** | `python-pptx` | MIT | ✅ GIỮ LẠI | Tự do thương mại |
| 2 | **python-docx** | `python-docx` | MIT | ✅ GIỮ LẠI | Tự do thương mại |
| 3 | **pypdf** | `pypdf` | BSD | ✅ GIỮ LẠI | Tự do thương mại |
| 4 | **OpenCV** | `opencv-python` | Apache 2.0 | ✅ GIỮ LẠI | Hoàn toàn tự do thương mại |
| 5 | **NumPy** | `numpy` | BSD 3-Clause | ✅ GIỮ LẠI | Tự do thương mại |
| 6 | **PyAV (av)** | `av` | BSD | ✅ GIỮ LẠI | Wrapper FFmpeg; xem lưu ý FFmpeg bên dưới |
| 7 | **Pillow** | `Pillow` | HPND (MIT-like) | ✅ GIỮ LẠI | Tự do thương mại |
| 8 | **RDKit** | `rdkit` | BSD 3-Clause | ✅ GIỮ LẠI | Cheminformatics; tự do thương mại |
| 9 | **Manim CE** | `manim` | MIT | ✅ GIỮ LẠI | Tự do thương mại; không dùng "Pi creature" 3B1B |
| 10 | **edge-tts** | `edge-tts>=7.2` | GPL-3.0 | ❌ **ĐÃ LOẠI Bỏ HOÀN TOÀN** | Thay bằng VieNeu-TTS v3 Turbo (xem bên dưới) |
| 11 | **vieneu** | `vieneu` | MIT | ✅ GIỮ LẠI | VieNeu-TTS v3 Turbo; ONNX · CPU · offline · 23 giọng Việt |

### ✅ edge-tts: ĐÃ THAY THẾ HOÀN TOÀN BẰỚC VieNeu-TTS v3 Turbo

> [!IMPORTANT]
> **Trạng thái:** ✅ **ĐÃ THAY THẾ HOÀN TOÀN**
> - `edge-tts` (GPL-3.0 + Vi phạm ToS Microsoft) đã được gỡ bỏ triệt để khỏi toàn bộ hệ thống.
> - Thay thế bằng **VieNeu-TTS v3 Turbo** (MIT license): `vieneu==3.6.4`, ONNX backend, chạy hoàn toàn trên CPU, offline.
> - 23 preset giọng Việt cố định; không phụ thuộc mạng hay API của bên thứ ba.
> - Điểm cần chú ý: Model `pnnbao-ump/VieNeu-TTS-v3-Turbo` download tự động khi khởi động lần đầu.

**Khuyến nghị:** Tiếp tục dùng **VieNeu-TTS v3 Turbo**.

---

## ⚙️ PHẦN III — Công Cụ Hệ Thống (System Tools)

| # | Công cụ | License | Phân loại | Ghi chú |
|---|---------|---------|-----------|---------|
| 1 | **FFmpeg** (binary) | LGPL 2.1+ | ⚠️ **CẦN XEM XÉT** | Xem phân tích chi tiết bên dưới |
| 2 | **Node.js** | MIT | ✅ GIỮ LẠI | Tự do thương mại |
| 3 | **npm** | Artistic License 2.0 | ✅ GIỮ LẠI | Tự do thương mại |

### 🟡 Phân Tích Chi Tiết: FFmpeg (Cần Tuân Thủ)

| Điều kiện | Yêu cầu |
|-----------|---------|
| Không dùng `--enable-gpl` | Nếu dùng libx264, libx265 → FFmpeg trở thành GPL |
| Dynamic linking | Nên dùng liên kết động (DLL) thay static |
| Attribution | Bắt buộc ghi nhận FFmpeg trong tài liệu sản phẩm |

Đối với dự án này (sản xuất học liệu, không phân phối binary): Hệ thống chỉ dùng FFmpeg như công cụ runtime nội bộ. Video đầu ra (MP4) chỉ là tác phẩm được tạo ra — không phải sản phẩm phái sinh của FFmpeg. **Rủi ro thực tế: Thấp.** Tuân thủ bằng cách ghi attribution trong tài liệu dự án.

---

## 🌐 PHẦN IV — Remotion (ĐÃ LOẠI BỎ HOÀN TOÀN)

> [!IMPORTANT]
> **Trạng thái:** ❌ **ĐÃ LOẠI BỎ HOÀN TOÀN KHỎI HỆ THỐNG**
> - Toàn bộ thư mục `engines/remotion/`, skill `elearning-remotion-video`, package `remotion`, `@remotion/cli` và các cấu hình đã được gỡ bỏ triệt để.
> - Toàn bộ tính năng diễn hoạt Spring physics, Timeline frame-accurate, Kinetic typography đã được chuyển giao sang **HyperFrames v2** tự chủ (`core/hf_engine.py`, `assets/templates/hf_components/`).

---

## 🌐 PHẦN V — Rendervid (ĐÃ LOẠI BỎ HOÀN TOÀN)

> [!IMPORTANT]
> **Trạng thái:** ❌ **ĐÃ LOẠI BỎ HOÀN TOÀN KHỎI HỆ THỐNG**
> - Toàn bộ thư mục `engines/rendervid/`, skill `elearning-rendervid-video`, các dependency `@rendervid/*` và runtime liên quan đã được gỡ bỏ triệt để.
> - Toàn bộ ý tưởng thiết kế hữu ích (JSON Scene Specification, Code Studio typewriter, multi-track Lo-Fi audio, smart-skip capture) đã được tích hợp đầy đủ vào **HyperFrames v2** tự chủ và sử dụng Puppeteer (Apache 2.0).


---

## 🧠 PHẦN VI — Dữ Liệu Bên Thứ Ba & Thí Nghiệm Ảo

| # | Nguồn dữ liệu / Thí nghiệm | License | Phân loại | Ghi chú |
|---|---------------------------|---------|-----------|---------|
| 1 | **RCSB PDB** (dữ liệu phân tử) | CC0 1.0 Public Domain | ✅ GIỮ LẠI | Hoàn toàn tự do thương mại |
| 2 | **Virtual Lab (Thí nghiệm Ảo)** | MIT & Apache 2.0 | ✅ GIỮ LẠI | Ray Optics (Apache-2.0), Matter.js (MIT), Three.js (MIT) — 100% tự do thương mại |
| 3 | **Font: Be Vietnam Pro** | SIL Open Font License 1.1 | ✅ GIỮ LẠI | Tự do thương mại |
| 4 | **PhET Simulations** | CC BY-NC 4.0 & GPLv3 | ❌ **ĐÃ LOẠI BỎ HOÀN TOÀN** | Đã loại bỏ triệt để toàn bộ source, asset, demo & skill; thay bằng Virtual Lab |

---

## 🔬 PHẦN VII — PhET Simulations (ĐÃ LOẠI BỎ HOÀN TOÀN)

> [!IMPORTANT]
> **Trạng thái:** ❌ **ĐÃ LOẠI BỎ HOÀN TOÀN KHỎI HỆ THỐNG**
> - PhET Interactive Simulations áp dụng giấy phép phi thương mại **CC BY-NC 4.0** cho các file mô phỏng HTML và yêu cầu trả phí Commercial License khi tích hợp vào sản phẩm thương mại / thuê bao.
> - Toàn bộ mã nguồn `core/phet_engine.py`, `engines/phet/`, `.agents/skills/elearning-phet-video/`, `assets/templates/phet_runner.html`, cache runtime và các file demo PhET đã được **gỡ bỏ triệt để 100%**.
> - Không dùng lại bất kỳ source code, asset hay screenshot nào của PhET.
> - Toàn bộ chức năng thí nghiệm ảo đã được chuyển sang **Virtual Lab Engine** (`core/virtual_lab_engine.py`) sử dụng các thư viện mã nguồn mở cấp phép mở tự do thương mại:
>   - **Quang học:** Ray Optics Simulation (Apache 2.0)
>   - **Cơ học:** Matter.js (MIT) với 9 dạng bài thí nghiệm
>   - **Mạch điện:** Pure Canvas Circuit Runner (MIT)
>   - **Sóng & Dao động:** Wave Runner (MIT)
>   - **Điện trường:** Coulomb Field Runner (MIT)

---

## 📊 TỔNG HỢP & ƯU TIÊN HÀNH ĐỘNG

### Hành động ưu tiên cao — Cần xử lý ngay

| # | Thành phần | Vấn đề | Hành động đề xuất |
|---|-----------|--------|---------------------|
| 1 | **edge-tts** | GPL-3.0 + vi phạm ToS Microsoft | ✅ **ĐÃ THAY THẾ bằng VieNeu-TTS v3 Turbo (MIT)** |
| 2 | **Remotion** | Đã loại bỏ hoàn toàn | Đã chuyển giao tính năng sang HyperFrames tự chủ v2 |
| 3 | **PhET** | CC BY-NC 4.0 / GPL | Đã loại bỏ hoàn toàn, thay bằng Virtual Lab (MIT/Apache 2.0) |

### Hành động ưu tiên trung bình — Cần xử lý theo kế hoạch

| # | Thành phần | Vấn đề | Hành động đề xuất |
|---|-----------|--------|---------------------|
| 4 | **FFmpeg** | LGPL — cần attribution | Thêm FFmpeg attribution vào README và tài liệu sản phẩm |
| 5 | **@rendervid** | Đã loại bỏ hoàn toàn | Đã loại bỏ triệt để runtime & dependency |

---

## 🛠️ KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT

### Hành động 1 — Thay thế edge-tts: ĐÃ HOÀN TẤT

```diff
- edge-tts >= 7.2  (GPL-3.0 + Unofficial Microsoft API)
+ vieneu           (VieNeu-TTS v3 Turbo, MIT license, ONNX CPU offline)
```

Trạng thái: **✅ ĐÃ HOÀN TẤT** (Checkpoint 21)
- Đã gỡ bỏ `edge-tts` khỏi toàn bộ hệ thống.
- `core/audio_tts_engine.py` đã được viết lại hoàn toàn với VieNeu-TTS v3 Turbo.
- 23 giọng Việt cố định, không phụ thuộc internet.
- Backward-compat alias `generate_edge_tts_audio_and_srt` đã được cung cấp cho các script cũ.

### Hành động 2 — Remotion (ĐÃ HOÀN TẤT LOẠI BỎ)

- Đã gỡ bỏ toàn bộ `engines/remotion/`, skill `elearning-remotion-video`, package Remotion và router.
- Không còn bất kỳ rủi ro bản quyền thương mại Remotion nào.

### Hành động 3 — FFmpeg Attribution

Thêm vào `README.md`:
```
Hệ thống sử dụng FFmpeg (https://ffmpeg.org) được cấp phép theo GNU LGPL 2.1+.
```

### Hành động 4 — Rendervid (ĐÃ HOÀN TẤT LOẠI BỎ)

- Đã gỡ bỏ toàn bộ runtime, skill và dependency `@rendervid/*`.
- Các ý tưởng tốt (JSON Spec, component hóa) đã được chuẩn hóa vào HyperFrames v2.

---

## 📌 Bảng Tham Chiếu License Nhanh

| License | Dùng thương mại? | Phải open-source? | Attribution bắt buộc? |
|---------|-----------------|------------------|----------------------|
| **MIT** | ✅ Có | ❌ Không | ✅ Giữ copyright notice |
| **BSD 2/3-Clause** | ✅ Có | ❌ Không | ✅ Giữ copyright notice |
| **Apache 2.0** | ✅ Có | ❌ Không | ✅ Ghi nhận trong notice file |
| **SIL OFL 1.1** | ✅ Có | ❌ Không | ✅ Không đổi tên font |
| **CC0 1.0** | ✅ Có | ❌ Không | Khuyến khích (không bắt buộc) |
| **LGPL 2.1** | ✅ Có (với điều kiện) | ⚠️ Chỉ phần thư viện LGPL | ✅ Attribution + dynamic link |
| **GPL-3.0** | ⚠️ Có nhưng bắt buộc open-source | ✅ Bắt buộc toàn bộ | ✅ Attribution |

---

> **Lưu ý:** Tài liệu này phục vụ mục đích thông tin nội bộ, không phải tư vấn pháp lý chính thức.
> Đối với quyết định thương mại quan trọng, vui lòng tham khảo luật sư sở hữu trí tuệ.

*Kiểm kê thực hiện bởi: Antigravity AI Agent | Ngày: 2026-09-09 | Phiên: CHECKPOINT 14*
