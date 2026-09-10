# Antigravity Modular E-Learning & Whiteboard Animation

> **Giải pháp Tự động hóa Toàn diện Sản xuất Học liệu E-Learning & Video Hoạt ảnh Bảng trắng (Whiteboard Animation) theo Kiến trúc Modular Multi-Skills & Pre-flight Check Thông minh.**

---

## 👨‍💻 Thông tin Tác giả & Kênh Cộng đồng

- **Tác giả:** `luongna`
- **Website:** [lungcode.com](https://lungcode.com)
- **Kênh Youtube:** [Lửng Code - AI Agent & Automation](https://www.youtube.com/channel/UCaUOOdtyRzaZ0zbrPgWRVZg?sub_confirmation=1)

---

## 🌟 Giới thiệu Kiến Trúc Modular Multi-Skills

Hệ thống gồm **8 skill** trong `.agents/skills/`: 4 skill sản xuất đầu vào, 1 router video, 2 engine video và 1 điều phối toàn trình. Bạn có thể bắt đầu ở bất kỳ giai đoạn nào.

```
                                  ┌─────────────────────────────┐
                                  │      elearning-pipeline     │
                                  │    (Master Orchestrator)    │
                                  └──────────────┬──────────────┘
                                                 │
        ┌───────────────────┬────────────────────┼───────────────────┬───────────────────┐
        ▼                   ▼                    ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐    ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│elearning-     │   │elearning-     │    │elearning-     │   │elearning-     │   │elearning-     │
│script         │   │images         │    │slides         │   │audio          │   │video          │
│(Kịch bản)     │   │(Tạo ảnh)      │    │(Slide PPTX)   │   │(TTS MP3 & SRT)│   │(Video WB)     │
└───────────────┘   └───────────────┘    └───────────────┘   └───────────────┘   └───────────────┘
```

1. **`elearning-pipeline` (Master Orchestrator):** Điều phối toàn trình và tự động kiểm tra điều kiện (Pre-flight Check) để tự lập kế hoạch hành động.
2. **`elearning-script` (Giai đoạn 1 - Kịch bản riêng):** Đánh giá tài liệu gốc (PDF, DOCX, TXT), xác định mục tiêu Biết - Hiểu - Làm được, cấu trúc Blended Learning và xuất bản kịch bản 4 cột (`script.md`, `script.xls`). *(Dừng duyệt bắt buộc tại Bước 4)*. Xuất bản 2 bản độc lập cho từng video: `script.md` (kịch bản full) và `voice-script.md` (chỉ có lời thoại).
3. **`elearning-images` (Giai đoạn 2 - Tạo ảnh riêng):** Thiết kế Prompt Infographic 16:9 chuẩn Tiếng Việt 100%, font Be Vietnam Pro, cấm vẽ tay người; tự động hóa sinh ảnh hàng loạt qua Browser Subagent (Google Flow).
4. **`elearning-slides` (Giai đoạn 3 - Slide PPT riêng):** Đóng gói bộ ảnh slide thành bài giảng PowerPoint (`.pptx`) 16:9 chất lượng cao làm hình nền full-bleed.
5. **`elearning-audio` (Giai đoạn 4 - Audio riêng):** Thu âm giọng đọc **VieNeu-TTS v3 Turbo** (ONNX · CPU · offline) với 23 preset giọng Việt, chuẩn hóa phát âm thuật ngữ IT và tạo phụ đề SRT phân đoạn ngắn 6–8 từ.
6. **`elearning-video` (Giai đoạn 5 - Router):** Nếu chưa có lựa chọn engine, hỏi đúng **OpenCV hay hyperframes** và đợi câu trả lời. Lựa chọn đã chốt cho tác vụ đang tiếp tục được giữ lại.
7. **`elearning-opencv-video` (Giai đoạn 5 - OpenCV):** Quy trình cũ với ảnh slide, Canny, tô màu, bàn tay, MP3/SRT và MP4 1080p. Mã `core/whiteboard_engine.py` được giữ nguyên.
8. **`elearning-hyperframes-video` (Giai đoạn 5 - HyperFrames):** Đọc `script.md` riêng từng video và prompt thiết kế slide, dựng cảnh HTML/CSS/SVG, đồng bộ MP3/SRT, kiểm tra và xuất video. Ảnh slide phẳng không bắt buộc.

---

## 📁 Cấu trúc Thư mục Chuẩn (Phân định Rõ ràng)

Hệ thống phân định rạch ròi giữa **Mã lõi bất biến**, **Vùng người dùng cung cấp**, **Vùng tạm thời khi Agent chạy** và **Sản phẩm bàn giao**:

```text
srt-whiteboard-animation/
├── .agents/skills/                             # [CORE SKILLS] 8 skill
│   ├── elearning-pipeline/                     # Master Orchestrator
│   ├── elearning-script/                       # GĐ 1: Kịch bản riêng
│   ├── elearning-images/                       # GĐ 2: Tạo ảnh riêng
│   ├── elearning-slides/                       # GĐ 3: Slide PPT riêng
│   ├── elearning-audio/                        # GĐ 4: Audio MP3 & SRT riêng
│   ├── elearning-video/                        # GĐ 5: Router chọn engine
│   ├── elearning-opencv-video/                 # GĐ 5: Engine OpenCV hiện tại
│   └── elearning-hyperframes-video/            # GĐ 5: Cảnh HTML/SVG bằng HyperFrames
│
├── core/                                       # [CORE ENGINES] Thư viện động cơ lõi dùng chung (Bất biến)
│   ├── preflight.py                            # Module kiểm tra điều kiện & định tuyến động
│   ├── voice_parser.py                         # Parser đọc file voice_script.txt linh hoạt
│   ├── pronunciation_dict.py                   # Từ điển chuẩn hóa phát âm 13 danh mục & ngữ âm TTS
│   ├── audio_tts_engine.py                     # VieNeu-TTS v3 Turbo (23 giọng · ONNX · CPU) + Chuẩn hóa + SRT ngắn
│   ├── whiteboard_engine.py                    # Canny Outline + Hand Drawing + Subtitle 48px chữ đen
│   ├── pptx_engine.py                          # Tạo slide PowerPoint 16:9
│   ├── doc_reader.py                           # Đọc tài liệu PDF, DOCX, TXT
│   └── video_effects.py                        # Các hiệu ứng chuyển động video
│
├── inputs/                                     # [USER INPUTS] Vùng người dùng đưa tài liệu & nguyên liệu
│   ├── documents/                              # Tài liệu thô: PDF, DOCX, TXT, đề cương...
│   ├── voice_scripts/                          # File voice_script.txt người dùng tự viết
│   └── images/                                 # Ảnh slide người dùng tự chuẩn bị sẵn
│
├── runtime/                                    # [RUNTIME / SCRATCH] Khu vực tạm của Agent (CÓ THỂ XÓA SẠCH)
│   ├── tasks/                                  # Script code sinh thêm theo từng video khi chạy
│   ├── cache/                                  # Cache ảnh nháp, canny edges, frames tạm
│   ├── logs/                                   # File log chạy tác vụ
│   └── archive/                                # Lưu trữ lịch sử các script cũ
│
├── output/                                     # [OUTPUTS] Sản phẩm đầu ra phân cấp rõ ràng
│   └── <Khoa-hoc_Mon-hoc>/                     # Ví dụ: KNM01/
│       ├── plan.md, plan.json                  # Kế hoạch tổng thể môn học (nếu chạy từ GĐ 1)
│       ├── script.md, script.xls               # Kịch bản tổng hợp môn học
│       ├── labguide.md                         # Hướng dẫn thực hành Lab
│       └── video-<x>/                          # Thư mục độc lập của từng video
│           ├── script.md                       # Bản 1: Kịch bản full của video
│           ├── voice-script.md                 # Bản 2: Chỉ có voice script của video
│           ├── images/                         # slide-1.jpeg, slide-2.jpeg...
│           ├── prompts/                        # prompt-1.txt, prompt-2.txt...
│           ├── mp3/                            # mp3-1.mp3, mp3-1.srt...
│           ├── hyperframes/                    # Nguồn HTML, storyboard, manifest và QA nếu chọn HyperFrames
│           ├── Bài <X> - [Tên].pptx            # File thuyết trình PPTX
│           └── Video <X> - [Tên].mp4           # Video thành phẩm Master
│
├── scripts/                                    # [SETUP] Tiện ích cài đặt môi trường ban đầu
│   └── prepare_env.py                          # Script cấu hình thư viện phụ thuộc
│
└── assets/                                     # Tài nguyên tĩnh: fonts (BeVietnamPro-Bold.ttf), drawing-hand.png
```

---

## 🎯 Các Kịch Bản Sử Dụng Linh Hoạt (Flexible Entry Points)

### Kịch bản 1: Người dùng chỉ có File Voice Script TXT + Thư mục Ảnh (Phổ biến nhất)
- **Tình huống:** Bạn không có tài liệu thô, không cần qua bước viết kịch bản; bạn chỉ có 1 file text chứa các đoạn lời thoại và 1 thư mục ảnh slide.
- **Cách chuẩn bị:**
  1. Thả ảnh vào thư mục `output/<mon-hoc>/video-<x>/images/` (hoặc `inputs/images/`): `slide-1.png`, `slide-2.png`...
  2. Tạo file `voice_script.txt` trong `inputs/voice_scripts/` với cấu trúc rất đơn giản:
     ```text
     Voice script video 1 - Kỹ thuật Phân tích Nguyên nhân Gốc rễ

     Đoạn 1:
     Chào mừng các bạn đã quay trở lại với bài học hôm nay...

     Đoạn 2:
     Mục tiêu bài học giúp các bạn phân biệt giữa triệu chứng và nguyên nhân...

     Đoạn 3:
     Mô hình tảng băng minh họa rõ điều này...
     ```
     *(Hoặc chỉ cần tách nhau bằng 1 dòng trống `\n\n`, hệ thống sẽ tự động nhận diện).*
  3. Nhắn lệnh cho AI Agent:
     > *"Tạo video animation cho Video 1"*
  4. **Cơ chế Pre-flight Check tự động kích hoạt:**
     - AI nhận diện: Có ảnh + Voice Script nhưng chưa có MP3/SRT.
     - AI tạo MP3/SRT qua `elearning-audio`, sau đó vào `elearning-video` để hỏi engine nếu chưa chỉ rõ. OpenCV dùng ảnh/audio như hiện tại; HyperFrames đọc thêm `script.md` riêng và prompt thiết kế trước khi dựng cảnh.

---

### Kịch bản 2: Toàn trình từ Tài liệu Gốc (End-to-End)
- **Cách làm:**
  1. Thả file tài liệu (`.pdf`, `.docx`, `.txt`) vào `inputs/documents/`.
  2. Nhắn lệnh: *"Bắt đầu phân tích tài liệu để làm học liệu môn học."*
  3. AI kích hoạt `elearning-script`: Phân tích Biết - Hiểu - Làm được $\to$ Đề xuất đề cương Blended Learning $\to$ **Dừng duyệt ở Bước 4**.
  4. Bạn nhắn: **"Tiếp tục"**.
  5. AI tự động: Tạo kịch bản 4 cột (xuất `script.md` và `voice-script.md`) $\to$ Sinh prompt & ảnh (`elearning-images`) $\to$ Sinh audio MP3/SRT (`elearning-audio`) $\to$ Tạo PowerPoint (`elearning-slides`) $\to$ Xuất bản Video hoàn chỉnh (`elearning-video`).

---

### Kịch bản 3: Chỉ sử dụng đơn lẻ một giai đoạn
- **Chỉ tạo Kịch bản:** Sử dụng skill `elearning-script`.
- **Chỉ tạo Ảnh:** Sử dụng skill `elearning-images`.
- **Chỉ tạo Slide PPTX:** Sử dụng skill `elearning-slides`.
- **Chỉ tạo Audio & SRT:** Sử dụng skill `elearning-audio` (mặc định giọng Nam Minh).
- **Chỉ tạo Video khi đã có sẵn MP3:** Sử dụng skill `elearning-video`.

### Giai đoạn 5: lựa chọn engine

Lệnh `5`, yêu cầu tạo video hoặc chuyển tiếp từ toàn trình đều đi qua router. Chỉ yêu cầu audio/ảnh/PPTX thì không hỏi engine video. Gọi trực tiếp skill OpenCV hoặc HyperFrames được coi là đã chọn engine đó.

```powershell
# Chưa chọn engine: kết quả yêu cầu hỏi "OpenCV hay hyperframes"
python core/preflight.py "output/KNM01/video-1" --stage video --json
# Đã chọn OpenCV: giữ điều kiện ảnh + MP3/SRT hiện tại
python core/preflight.py "output/KNM01/video-1" --stage video --engine opencv --json
# Đã chọn HyperFrames: kiểm tra script riêng, không bắt buộc ảnh phẳng
python core/preflight.py "output/KNM01/video-1" --stage video --engine hyperframes --json
```

Nhánh HyperFrames bắt đầu từ `output/<mon-hoc>/video-<x>/script.md`: đọc nội dung, cột prompt và lời thoại; đối chiếu `prompts/prompt-X.txt` nếu có; lập storyboard/manifest rồi dựng cảnh theo thiết kế. MP3/SRT dùng lại nếu đúng lời đã chốt, thiếu thì tạo qua `elearning-audio`. `STATUS_NEED_SCENE_PREPARATION` chỉ là có script để đọc, không phải đã sẵn sàng render.

Nguồn dựng và kết quả kiểm tra được giữ trong `video-<x>/hyperframes/`. Chi tiết: [skill HyperFrames](.agents/skills/elearning-hyperframes-video/SKILL.md). Engine cần Node.js ≥22, FFmpeg và Chrome phục vụ render; ghim CLI theo phiên bản đã kiểm tra. Các thay đổi skill/định tuyến không đồng nghĩa môi trường render đã được cài hoặc kiểm chứng.

---

## 🎨 Hệ Thống Theme Presets (Bộ Sưu Tập Màu Nền & Màu Chữ)

Hệ thống cho phép tùy biến phong cách thị giác của bài giảng phù hợp với từng lĩnh vực và chủ đề đào tạo thông qua module [`core/theme_manager.py`](core/theme_manager.py):

| Theme Preset ID | Tên Phong Cách | Màu Nền Chủ Đạo | Màu Chữ & Subtitle | Điểm Nhấn & Phù Hợp Cho |
|---|---|---|---|---|
| `light-whiteboard` *(Mặc định)* | Trắng Tinh Khiết / Bản tin | `#FFFFFF` / `#F8FAFC` | `#1A202C` (Đen đậm sắc nét) | Navy `#16324F`, Teal `#007F82`. Bài giảng sư phạm, phổ thông, kinh tế. |
| `dark-modern` | Tối Hiện Đại / Dark Mode | Slate `#0F172A` | `#F8FAFC` (Trắng sáng dịu mắt) | Sky Blue `#38BDF8`, Amber `#F59E0B`. Lập trình, phần mềm, công nghệ cao. |
| `ai-tech-neon` | AI Cyber Neon / Tương Lai | Gradient `#0B0F19` $\to$ `#1E1B4B` | `#F0FDF4` (Sáng dạ quang) | Cyan `#00F5FF`, Violet `#A855F7`. Trí tuệ nhân tạo, Robotics, IoT, Data Science. |
| `flat-editorial` | Flat Tạp Chí / Báo Cáo | Giấy kem `#FAF8F5` | `#1C1917` (Mực đen cổ điển) | Crimson `#E11D48`, Emerald `#059669`. Quản trị kinh doanh, tài chính, khởi nghiệp. |

- **Cơ chế hoạt động:**
  1. **Tự động nhận diện (Auto-detect):** Quét từ khóa trong kịch bản (AI, Robotics, Lập trình, Kinh doanh...) để tự động gợi ý Theme phù hợp nhất trong Pre-flight Check.
  2. **Tùy chọn ghi đè bằng cờ lệnh:** `--theme dark-modern` hoặc `--theme ai-tech-neon`.
  3. **Chuẩn hóa Phụ đề theo Theme:** Nền sáng chữ màu đen (`#1A202C`), nền tối/cyber chữ màu trắng sáng (`#F8FAFC`), font size 48px Be Vietnam Pro Bold, không viền stroke, đảm bảo độ tương phản WCAG AA.

---

## 🎬 Thư Viện Video Trám Cảnh (B-Roll Video Library & Inlay)

Giải pháp khắc phục nhược điểm "màn hình tĩnh" khi giảng viên thuyết minh các đoạn dài (trên 14–15s). Hệ thống tích hợp module [`core/broll_manager.py`](core/broll_manager.py) tự động phân tích và lồng ghép video thực tế:

- **Cấu trúc thư mục quản lý:**
  ```text
  inputs/video-libraries/
  ├── ai-robotics/          # Clip về AI, robot, tự động hóa, mạch điện tử
  ├── business-corporate/   # Clip về văn phòng, họp hành, đàm phán doanh nghiệp
  ├── student-campus/       # Clip về sinh viên, học nhóm, giảng đường, thực hành
  └── general-tech/         # Clip về viết mã lập trình, máy chủ, dữ liệu
  ```
- **Quy tắc lồng ghép thông minh:**
  1. **Thời điểm kích hoạt:** Chỉ chèn vào các slide có voice dài ($> 14$s).
  2. **Trễ hiển thị (Delay Hold):** Xuất hiện từ giây thứ 5.0s (sau khi người học đã nắm rõ tiêu đề bài học và cấu trúc chính).
  3. **Chế độ trình chiếu PiP Card:** Hiển thị dạng thẻ video bo góc nổi bật (16:9, viền sang trọng, shadow mềm mại, huy hiệu *"MINH HỌA THỰC CHIẾN"*), kích thước 500x281px tại góc phải trên, tuyệt đối không che khuất mỏ neo thị giác và phụ đề ở đáy màn hình.
  4. **Âm thanh:** Toàn bộ video trám cảnh được đặt chế độ `muted` để giọng đọc giảng viên luôn là tâm điểm duy nhất.

---

## 🎙️ Hệ Thống Giọng Đọc & Chuẩn Hóa Phát Âm

- **Giọng đọc mặc định:** `vi-VN-NamMinhNeural` (Nam miền Nam, truyền cảm, chững chạc).
- **Giọng đọc tùy chọn:** `vi-VN-HoaiMyNeural` (Nữ miền Nam, trong trẻo, nhẹ nhàng).
- **Động cơ thực thi:** Toàn bộ từ điển bên dưới được chuẩn hóa tự động qua module [`core/pronunciation_dict.py`](core/pronunciation_dict.py) và tích hợp trực tiếp vào [`core/audio_tts_engine.py`](core/audio_tts_engine.py).
- **Cơ chế xử lý thông minh:**
  1. Tự động ưu tiên cụm từ dài trước (tránh xung đột từ khóa con).
  2. Phân biệt chữ hoa viết tắt pháp quy/chức danh và từ mượn thông dụng.
  3. Tự động quy đổi định dạng ngày tháng, giờ giấc, phần trăm, ký hiệu toán học và đơn vị đo lường.

### 1. Cơ quan - Danh từ riêng & Chức danh
* `BUNI` → `bu ni`
* `TGĐ` → `Tổng Giám đốc`
* `PTGĐ` → `Phó Tổng Giám đốc`
* `GĐ` → `Giám đốc`
* `PGĐ` → `Phó Giám đốc`

* `CTHĐQT` → `Chủ tịch Hội đồng Quản trị`
* `HĐQT` → `Hội đồng Quản trị`
* `HĐTV` → `Hội đồng Thành viên`
* `BKS` → `Ban Kiểm soát`

* `TNHH` → `trách nhiệm hữu hạn`
* `CTCP` → `công ty cổ phần`
* `CP` → `cổ phần`  # cần xử lý theo ngữ cảnh

* `CP` → `Chính phủ`
* `TTg` → `Thủ tướng Chính phủ`
* `TW` → `Trung ương`

* `BGDĐT` → `Bộ Giáo dục và Đào tạo`
* `GDĐT` → `Giáo dục và Đào tạo`
* `SGDĐT` → `Sở Giáo dục và Đào tạo`
* `PGDĐT` → `Phòng Giáo dục và Đào tạo`

* `Bộ GD&ĐT` → `Bộ Giáo dục và Đào tạo`
* `Sở GD&ĐT` → `Sở Giáo dục và Đào tạo`
* `Phòng GD&ĐT` → `Phòng Giáo dục và Đào tạo`

* `BTTTT` → `Bộ Thông tin và Truyền thông`
* `BKHCN` → `Bộ Khoa học và Công nghệ`
* `BTC` → `Bộ Tài chính`
* `BCA` → `Bộ Công an`
* `BNV` → `Bộ Nội vụ`
* `BYT` → `Bộ Y tế`
* `BTP` → `Bộ Tư pháp`
* `BLĐTBXH` → `Bộ Lao động, Thương binh và Xã hội`

* `UBND` → `Ủy ban nhân dân`
* `HĐND` → `Hội đồng nhân dân`
* `UBTVQH` → `Ủy ban Thường vụ Quốc hội`
* `QH` → `Quốc hội`

### 2. Thuật ngữ Công nghệ Thông tin & Lập trình

* `IT` → `ai ti`
* `ICT` → `ai xi ti`
* `AI` → `ây ai`
* `A.I.` → `ây ai`
* `ML` → `em eo`
* `Machine Learning` → `mờ shin lơ ning`
* `Deep Learning` → `đíp lơ ning`
* `Generative AI` → `jen nơ rây tiv ây ai`
* `GenAI` → `jen ây ai`
* `LLM` → `eo eo em`
* `NLP` → `en eo pi`
* `Computer Vision` → `cơm piu tờ vi dần`

* `API` → `ây pi ai`
* `REST API` → `rést ây pi ai`
* `RESTful API` → `rést phồ ây pi ai`
* `SDK` → `ét đi cây`
* `IDE` → `ai đi i`
* `CLI` → `xi eo ai`
* `GUI` → `gu-i`
* `UI` → `iu ai`
* `UX` → `iu éc`
* `UI/UX` → `iu ai, iu éc`

* `CPU` → `xi pi iu`
* `GPU` → `gi pi iu`
* `RAM` → `ram`
* `ROM` → `rom`
* `SSD` → `ét ét đi`
* `HDD` → `hát đi đi`
* `USB` → `iu ét bi`
* `IoT` → `ai ô ti`

* `HTML` → `hát ti em eo`
* `CSS` → `xi ét ét`
* `JavaScript` → `gia va sờ cờ-ríp`
* `TypeScript` → `tai-p sờ cờ-ríp`
* `Python` → `pai thần`
* `Java` → `gia va`
* `C` → `xi`
* `C++` → `xi cộng cộng`
* `C#` → `xi-sharp`
* `.NET` → `đót nét`
* `ASP.NET` → `ây ét pi đót nét`
* `PHP` → `pi hát pi`
* `Node.js` → `nốt chấm giây ét`
* `React` → `ri ác`
* `Angular` → `eng giu lờ`
* `Vue.js` → `viu chấm giây ét`

* `SQL` → `ét quy eo`
* `MySQL` → `mai ét quy eo`
* `SQL Server` → `ét quy eo sơ-vờ`
* `PostgreSQL` → `pốt gờ-rét ét quy eo`
* `NoSQL` → `nô ét quy eo`
* `MongoDB` → `mon gô đi bi`
* `Database` → `đây tờ bây-s`
* `DBMS` → `đi bi em ét`

* `JSON` → `giây sần`
* `XML` → `éc em eo`
* `CSV` → `xi ét vi`
* `YAML` → `ya-mồ`
* `URL` → `iu a eo`
* `URI` → `iu a ai`
* `HTTP` → `hát ti ti pi`
* `HTTPS` → `hát ti ti pi ét`
* `DNS` → `đi en ét`
* `IP` → `ai pi`
* `TCP/IP` → `ti xi pi, ai pi`
* `SSH` → `ét ét hát`
* `SSL` → `ét ét eo`
* `TLS` → `ti eo ét`
* `VPN` → `vi pi en`

* `Git` → `gít`
* `GitHub` → `gít hắp`
* `GitLab` → `gít láp`
* `Commit` → `cờ mít`
* `Push` → `pút`
* `Pull` → `pun`
* `Pull Request` → `pun ri-quest`
* `Branch` → `branh-ch`
* `Merge` → `mơ-j`
* `Repository` → `ri pô zi to ri`
* `Repo` → `ri pô`

* `Docker` → `đóc-cờ`
* `Kubernetes` → `ku bơ nét ti-s`
* `Cloud` → `cờ-lao-đ`
* `Server` → `sơ-vờ`
* `Client` → `cờ-lai-ần`
* `Backend` → `bách en`
* `Frontend` → `phờ-rân en`
* `Full-stack` → `phun sờ-téc`

* `Framework` → `phờ-rêm-uớc`
* `Library` → `lai bờ re ri`
* `Module` → `mo đun`
* `Package` → `péc-kịt`
* `Plugin` → `plấc-in`
* `Extension` → `éc-sten-sần`

* `Algorithm` → `an gờ-rít-thầm`
* `Flowchart` → `phờ-lâu chát`
* `Pseudocode` → `su đô cốt`
* `Syntax` → `xin-tắc`
* `Variable` → `ve ri ờ bồ`
* `Function` → `phâng-sần`
* `Parameter` → `pờ-ra-mơ-tờ`
* `Argument` → `a-giu-mần`
* `Array` → `ờ-rây`
* `Object` → `óp-jẹct`
* `Class` → `cờ-lát`
* `Interface` → `in-tờ-phâys`
* `Loop` → `lúp`
* `Boolean` → `bu-li-ần`
* `String` → `sờ-trinh`
* `Integer` → `in-ti-jờ`
* `Float` → `phờ-lốt`
* `Null` → `nân`

* `Bug` → `bấc`
* `Debug` → `đi-bấc`
* `Debugger` → `đi-bấc-gờ`
* `Debugging` → `đi-bấc-ghinh`
* `Error` → `e-rờ`
* `Exception` → `éc-sep-sần`
* `Runtime` → `ran-tai-m`
* `Compile` → `cơm-pai-l`
* `Compiler` → `cơm-pai-lờ`

* `Log` → `lốc`
* `File log` → `phai lốc`
* `Log file` → `lốc phai`
* `Cache` → `két-sh`
* `Cookie` → `cu-ki`
* `Session` → `se-sần`
* `Token` → `tô-kần`

* `Test` → `tét`
* `Testing` → `tét-ting`
* `Test case` → `tét kây-s`
* `Unit Test` → `iu-nịt tét`
* `Integration Test` → `in-tờ-grây-sần tét`
* `QA` → `kiu ây`
* `QC` → `kiu xi`

* `Brute-force` → `bờ-rút phoóc`
* `Root Cause` → `nguyên nhân gốc rễ`
* `Root Cause Analysis` → `phân tích nguyên nhân gốc rễ`
* `Symptom` → `triệu chứng`
* `Ishikawa` → `I-si-ka-oa`
* `5 Whys` → `năm lần tại sao`

* `Memory Leak` → `rò rỉ bộ nhớ`
* `Memory Overflow` → `tràn bộ nhớ`
* `Out of Memory` → `hết bộ nhớ`
* `Index` → `chỉ mục`
* `SQL Index` → `chỉ mục ét quy eo`
* `Full Table Scan` → `quét toàn bộ bảng`
* `Query` → `truy vấn`
* `SQL Query` → `truy vấn ét quy eo`

## 🎙️ Hệ Thống Giọng Đọc & Chuẩn Hóa Phát Âm AI – Data Science – Robotics
* `Data` → `đây tờ`
* `Dataset` → `đây tờ sét`
* `Big Data` → `bích đây tờ`
* `Data Science` → `đây tờ sai-ần-s`
* `Data Scientist` → `đây tờ sai-ần-tịt`
* `Data Analytics` → `đây tờ a-na-li-tích`
* `Data Mining` → `khai phá dữ liệu`

* `Model` → `mô đồ`
* `AI Model` → `mô hình ây ai`
* `Training` → `huấn luyện`
* `Train Model` → `huấn luyện mô hình`
* `Inference` → `suy luận`
* `Prediction` → `dự đoán`
* `Classification` → `phân loại`
* `Regression` → `hồi quy`
* `Clustering` → `phân cụm`

* `Neural Network` → `mạng nơ ron`
* `CNN` → `xi en en`
* `RNN` → `a en en`
* `Transformer` → `tran-s-phoóc-mờ`
* `Tensor` → `ten-sờ`
* `TensorFlow` → `ten-sờ phờ-lâu`
* `PyTorch` → `pai toóc`
* `OpenCV` → `ô-pần xi vi`

* `Prompt` → `prôm`
* `Prompt Engineering` → `kỹ thuật thiết kế prôm`
* `Chatbot` → `chát-bót`
* `Agent` → `ây-jần`
* `AI Agent` → `ây ai ây-jần`
* `RAG` → `rác`
* `Embedding` → `em-be-đinh`
* `Vector` → `véc-tơ`
* `Vector Database` → `cơ sở dữ liệu véc-tơ`

* `Accuracy` → `độ chính xác`
* `Precision` → `độ chính xác dự đoán dương`
* `Recall` → `độ bao phủ`
* `F1-score` → `điểm ép một`
* `Confusion Matrix` → `ma trận nhầm lẫn`

* `Robot` → `rô-bốt`
* `Robotics` → `rô-bó-tích`
* `Sensor` → `cảm biến`
* `Actuator` → `cơ cấu chấp hành`
* `Arduino` → `a-đu-i-nô`
* `Raspberry Pi` → `ráp-bờ-ri pai`
* `Microcontroller` → `vi điều khiển`

## 🎙️ Hệ Thống Giọng Đọc & Chuẩn Hóa Phát Âm Giáo dục – Đào tạo – E-Learning
* `E-Learning` → `i lơ ning`
* `eLearning` → `i lơ ning`
* `LMS` → `eo em ét`
* `LCMS` → `eo xi em ét`
* `MOOC` → `múc`
* `SCORM` → `sờ-coóc-m`
* `xAPI` → `éc ây pi ai`

* `STEM` → `stem`
* `STEAM` → `sti-m`
* `EdTech` → `ét-téc`
* `Education Technology` → `công nghệ giáo dục`

* `Online` → `on-lai-n`
* `Offline` → `óp-lai-n`
* `Blended Learning` → `học tập kết hợp`
* `Hybrid Learning` → `học tập kết hợp trực tiếp và trực tuyến`
* `Self-learning` → `tự học`
* `Microlearning` → `học tập vi mô`

* `Learning Outcome` → `chuẩn đầu ra`
* `Learning Objectives` → `mục tiêu học tập`
* `Outcome` → `kết quả đầu ra`
* `Competency` → `năng lực`
* `Skill` → `kỹ năng`
* `Knowledge` → `kiến thức`
* `Assessment` → `đánh giá`
* `Evaluation` → `đánh giá`
* `Rubric` → `bảng tiêu chí đánh giá`

* `Quiz` → `bài kiểm tra`
* `Multiple Choice` → `trắc nghiệm nhiều lựa chọn`
* `Assignment` → `bài tập`
* `Feedback` → `phản hồi`
* `Grade` → `điểm`
* `Gradebook` → `sổ điểm`

* `Course` → `khóa học`
* `Module` → `mô đun`
* `Lesson` → `bài học`
* `Curriculum` → `chương trình đào tạo`
* `Syllabus` → `đề cương môn học`

* `Instructor` → `giảng viên`
* `Teacher` → `giáo viên`
* `Learner` → `người học`
* `Student` → `học sinh` hoặc `sinh viên`
* `Mentor` → `người hướng dẫn`
* `Tutor` → `gia sư`

### 4. Kinh doanh – Quản trị – Khởi nghiệp
* `CEO` → `xi i ô`
* `CFO` → `xi ép ô`
* `CTO` → `xi ti ô`
* `COO` → `xi ô ô`
* `CMO` → `xi em ô`
* `CIO` → `xi ai ô`
* `CHRO` → `xi hát a ô`

* `KPI` → `cây pi ai`
* `KPI's` → `các cây pi ai`
* `OKR` → `ô cây a`
* `ROI` → `a ô ai`
* `ROE` → `a ô i`
* `ROA` → `a ô ây`

* `B2B` → `bi tu bi`
* `B2C` → `bi tu xi`
* `C2C` → `xi tu xi`
* `B2G` → `bi tu gi`
* `D2C` → `đi tu xi`

* `CRM` → `xi a em`
* `ERP` → `i a pi`
* `HRM` → `hát a em`
* `HR` → `hát a`

* `SaaS` → `sát`
* `PaaS` → `pát`
* `IaaS` → `ai át`

* `Startup` → `khởi nghiệp`
* `Founder` → `nhà sáng lập`
* `Co-founder` → `đồng sáng lập`
* `Investor` → `nhà đầu tư`
* `Stakeholder` → `bên liên quan`
* `Shareholder` → `cổ đông`

* `Business Model` → `mô hình kinh doanh`
* `Business Plan` → `kế hoạch kinh doanh`
* `Business Model Canvas` → `mô hình kinh doanh canvas`
* `BMC` → `bi em xi`

* `SWOT` → `sờ-uốt`
* `PEST` → `pét`
* `PESTEL` → `pét-tồ`

* `Revenue` → `doanh thu`
* `Profit` → `lợi nhuận`
* `Cost` → `chi phí`
* `Cash Flow` → `dòng tiền`
* `Break-even Point` → `điểm hòa vốn`
* `Gross Profit` → `lợi nhuận gộp`
* `Net Profit` → `lợi nhuận ròng`

* `Market` → `thị trường`
* `Market Share` → `thị phần`
* `Target Market` → `thị trường mục tiêu`
* `Target Customer` → `khách hàng mục tiêu`
* `Customer Segment` → `phân khúc khách hàng`

* `Case Study` → `tình huống nghiên cứu`
* `Benchmark` → `đối chuẩn`
* `Best Practice` → `thực tiễn tốt`
* `Roadmap` → `lộ trình`
* `Milestone` → `cột mốc`
### 5. Marketing – Digital Marketing
* `Marketing` → `ma-kờ-ting`
* `Digital Marketing` → `đi-gi-tồ ma-kờ-ting`
* `Content Marketing` → `con-ten ma-kờ-ting`

* `SEO` → `ét i ô`
* `SEM` → `ét i em`
* `SMM` → `ét em em`
* `PPC` → `pi pi xi`
* `CPC` → `xi pi xi`
* `CPM` → `xi pi em`
* `CPA` → `xi pi ây`
* `CTR` → `xi ti a`
* `CTA` → `xi ti ây`
* `CPL` → `xi pi eo`

* `Lead` → `khách hàng tiềm năng`
* `Conversion` → `chuyển đổi`
* `Conversion Rate` → `tỷ lệ chuyển đổi`
* `Landing Page` → `trang đích`
* `Traffic` → `lưu lượng truy cập`
* `Organic Traffic` → `lưu lượng truy cập tự nhiên`

* `Brand` → `thương hiệu`
* `Branding` → `xây dựng thương hiệu`
* `Brand Awareness` → `nhận biết thương hiệu`

* `Flash Sale` → `phờ-lét xeo`
* `Sale` → `xeo`
* `Voucher` → `vao-chờ`
* `Coupon` → `cu-pon`
* `Affiliate` → `a-phi-li-ợt`
* `Affiliate Marketing` → `tiếp thị liên kết`

* `Livestream` → `lai-v sờ-trim`
* `Influencer` → `in-phờ-lu-en-sờ`
* `KOL` → `cây ô eo`
* `KOC` → `cây ô xi`

### 6. Truyền thông đa phương tiện – Thiết kế – Video
* `Multimedia` → `mân-ti-mi-đi-a`
* `Media` → `mi-đi-a`
* `Digital Media` → `đi-gi-tồ mi-đi-a`

* `Graphic Design` → `thiết kế đồ họa`
* `Motion Graphic` → `đồ họa chuyển động`
* `Animation` → `hoạt hình`
* `3D` → `ba đi`
* `2D` → `hai đi`

* `Adobe` → `ờ-đô-bi`
* `Photoshop` → `phô-tô-sóp`
* `Illustrator` → `i-lớt-trây-tờ`
* `Premiere` → `pờ-ri-mia`
* `After Effects` → `áp-tờ i-phéc`
* `InDesign` → `in-đi-zai-n`
* `Lightroom` → `lai-t rum`

* `Canva` → `can-va`
* `Figma` → `phích-ma`
* `CapCut` → `cáp-cắt`

* `Frame` → `khung hình`
* `Frame Rate` → `tốc độ khung hình`
* `FPS` → `ép pi ét`
* `Resolution` → `độ phân giải`
* `Pixel` → `pích-xeo`
* `Megapixel` → `mê-ga-pích-xeo`

* `Full HD` → `phun hát đi`
* `HD` → `hát đi`
* `4K` → `bốn cây`
* `8K` → `tám cây`

* `RGB` → `a gi bi`
* `CMYK` → `xi em oai cây`
* `DPI` → `đi pi ai`

* `Render` → `ren-đờ`
* `Rendering` → `ren-đờ-rinh`
* `Timeline` → `tai-m-lai-n`
* `Keyframe` → `ki-phờ-rêm`
* `Transition` → `chuyển cảnh`
* `Effect` → `hiệu ứng`
* `Voice-over` → `lời thuyết minh`
* `Subtitle` → `phụ đề`
* `Caption` → `chú thích`
### 7. Tên loại văn bản
* `NĐ` → `Nghị định`
* `NĐ-CP` → `Nghị định của Chính phủ`
* `QĐ` → `Quyết định`
* `QĐ-TTg` → `Quyết định của Thủ tướng Chính phủ`
* `QĐ-BGDĐT` → `Quyết định của Bộ Giáo dục và Đào tạo`

* `TT` → `Thông tư`
* `TT-BGDĐT` → `Thông tư của Bộ Giáo dục và Đào tạo`
* `TT-BTC` → `Thông tư của Bộ Tài chính`
* `TT-BLĐTBXH` → `Thông tư của Bộ Lao động, Thương binh và Xã hội`
* `TT-BTTTT` → `Thông tư của Bộ Thông tin và Truyền thông`
* `TT-BKHCN` → `Thông tư của Bộ Khoa học và Công nghệ`
* `TT-BNV` → `Thông tư của Bộ Nội vụ`

* `NQ` → `Nghị quyết`
* `NQ-CP` → `Nghị quyết của Chính phủ`
* `NQ/TW` → `Nghị quyết Trung ương`

* `CT` → `Chỉ thị`
* `CT-TTg` → `Chỉ thị của Thủ tướng Chính phủ`

* `CV` → `Công văn`
* `HD` → `Hướng dẫn`
* `KH` → `Kế hoạch`
* `TB` → `Thông báo`
* `BC` → `Báo cáo`

### 8. Các cấp học, bằng cấp và thuật ngữ giáo dục Việt Nam
* `MN` → `mầm non`
* `TH` → `tiểu học`
* `THCS` → `trung học cơ sở`
* `THPT` → `trung học phổ thông`
* `GDTX` → `giáo dục thường xuyên`
* `GDNN` → `giáo dục nghề nghiệp`

* `ĐH` → `đại học`
* `CĐ` → `cao đẳng`
* `TC` → `trung cấp`

* `GV` → `giáo viên`
* `GVBM` → `giáo viên bộ môn`
* `GVCN` → `giáo viên chủ nhiệm`
* `HS` → `học sinh`
* `SV` → `sinh viên`
* `HV` → `học viên`
* `CBGV` → `cán bộ giáo viên`
* `CBQL` → `cán bộ quản lý`
* `CBQLGD` → `cán bộ quản lý giáo dục`

* `CTGDPT` → `Chương trình Giáo dục phổ thông`
* `GDPT` → `giáo dục phổ thông`
* `CTGDPT 2018` → `Chương trình Giáo dục phổ thông năm 2018`

* `PPDH` → `phương pháp dạy học`
* `KTĐG` → `kiểm tra đánh giá`
* `KT-ĐG` → `kiểm tra, đánh giá`

* `CNTT` → `công nghệ thông tin`
* `CĐS` → `chuyển đổi số`
* `NLS` → `năng lực số`

### 9. Ký hiệu toán học thường gặp
* `+` → `cộng`
* `-` → `trừ`
* `×` → `nhân`
* `x` → `nhân` # chỉ trong biểu thức toán
* `÷` → `chia`
* `/` → `chia`
* `=` → `bằng`

* `>` → `lớn hơn`
* `<` → `nhỏ hơn`
* `>=` → `lớn hơn hoặc bằng`
* `<=` → `nhỏ hơn hoặc bằng`
* `≥` → `lớn hơn hoặc bằng`
* `≤` → `nhỏ hơn hoặc bằng`
* `≠` → `khác`

* `%` → `phần trăm`
* `‰` → `phần nghìn`

* `≈` → `xấp xỉ`
* `±` → `cộng hoặc trừ`
* `∞` → `vô cực`

* `√` → `căn bậc hai`
* `π` → `pi`
* `Δ` → `đen ta`
* `Σ` → `xích ma`

* `°` → `độ`
* `°C` → `độ C`
* `°F` → `độ F`

### 10. Ký hiệu lập trình
* `==` → `bằng bằng`
* `===` → `bằng bằng bằng`
* `!=` → `khác bằng`
* `!==` → `khác bằng bằng`
* `&&` → `và`
* `||` → `hoặc`
* `!` → `phủ định`
* `++` → `cộng cộng`
* `--` → `trừ trừ`
* `+=` → `cộng bằng`
* `-=` → `trừ bằng`
* `=>` → `mũi tên`

### 11. Đơn vị đo
* `mm` → `mi li mét`
* `cm` → `xen ti mét`
* `m` → `mét`
* `km` → `ki lô mét`

* `mm²` → `mi li mét vuông`
* `cm²` → `xen ti mét vuông`
* `m²` → `mét vuông`
* `km²` → `ki lô mét vuông`

* `cm³` → `xen ti mét khối`
* `m³` → `mét khối`

* `mg` → `mi li gam`
* `g` → `gam`
* `kg` → `ki lô gam`

* `ml` → `mi li lít`
* `mL` → `mi li lít`
* `l` → `lít`
* `L` → `lít`

* `Hz` → `héc`
* `kHz` → `ki lô héc`
* `MHz` → `mê ga héc`
* `GHz` → `gi ga héc`

* `V` → `vôn`
* `mV` → `mi li vôn`
* `A` → `ampe`
* `mA` → `mi li ampe`
* `W` → `oát`
* `kW` → `ki lô oát`
* `kWh` → `ki lô oát giờ`
* `Wh` → `oát giờ`

* `KB` → `ki lô bai`
* `MB` → `mê ga bai`
* `GB` → `gi ga bai`
* `TB` → `tê ra bai`
* `Mbps` → `mê ga bít trên giây`
* `Gbps` → `gi ga bít trên giây`

### 12. Ngày tháng và thời gian
* `07/09/2026` → ngày 7 tháng 9 năm 2026
* `7/9` → `ngày 7 tháng 9`
* `08:30` → `8 giờ 30 phút`
* `8h30` → `8 giờ 30 phút`
* `14h` → `14 giờ`
* `24/7` → `hai mươi bốn trên bảy`

### 13. Một số tên nền tảng/công nghệ thường xuất hiện trong bài giảng
* `Google` → `gu-gồ`
* `Google Classroom` → `gu-gồ cờ-lát-rum`
* `Google Drive` → `gu-gồ đờ-rai-v`
* `Google Docs` → `gu-gồ đốc`
* `Google Sheets` → `gu-gồ sít`
* `Google Meet` → `gu-gồ mít`

* `Microsoft` → `mai-cờ-rô-sóp`
* `Microsoft Teams` → `mai-cờ-rô-sóp tim`
* `Word` → `uớt`
* `Excel` → `éc-xeo`
* `PowerPoint` → `pao-ờ-poi-n-t`

* `YouTube` → `iu-túp`
* `Facebook` → `phây-s-búc`
* `TikTok` → `tích-tóc`
* `Instagram` → `in-stờ-gram`
* `LinkedIn` → `lin-kờ-đin`

* `ChatGPT` → `chát gi pi ti`
* `GPT` → `gi pi ti`
* `OpenAI` → `ô-pần ây ai`
* `Gemini` → `gem-mi-nai`
* `Claude` → `cờ-lót`
* `Copilot` → `cô-pai-lợt`

---

## 🛠️ Hướng dẫn Cài đặt Môi trường

1. **Python:** Phiên bản 3.10 trở lên.
2. **FFmpeg & ffprobe:** Đã cài đặt và thêm vào biến môi trường `PATH`.
3. **Cài đặt thư viện:**
   ```powershell
   python scripts/prepare_env.py
   ```
4. **Kiểm tra Pre-flight Check trực tiếp:**
   ```powershell
   python core/preflight.py output/KNM01/video-1
   ```

---

## 📜 Bản quyền & Giấy phép
Project developed by **Nguyễn Anh Lương (LuongNA)** - [lungcode.com](https://lungcode.com).

* 🟢 **Personal & Educational Use:** Free to use, modify, and learn.
* 🔴 **Commercial Use:** Requires explicit written permission from the author.