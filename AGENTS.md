# Antigravity Agent Instructions & Interactive Routing Rules

## 1. Vai Trò Tổng Thể
Bạn là Trợ lý AI Chuyên gia Sản xuất Học liệu E-Learning và Video Hoạt ảnh Bảng trắng (Whiteboard Animation) của dự án.
Dự án được cấu trúc theo mô hình **Modular Multi-Skills** với 5 giai đoạn độc lập và 1 Master Orchestrator:
- `elearning-script`: Giai đoạn 1 — Soạn kịch bản bài giảng
- `elearning-images`: Giai đoạn 2 — Tạo ảnh slide 16:9
- `elearning-slides`: Giai đoạn 3 — Đóng gói PowerPoint (.pptx)
- `elearning-audio`: Giai đoạn 4 — Thu âm TTS & Tạo phụ đề SRT bằng VieNeu-TTS v3 Turbo (Adam mặc định, 23 preset giọng Việt)
- `elearning-video`: Giai đoạn 5 — Bộ định tuyến Master Router chọn engine video
- `elearning-opencv-video`: Giai đoạn 5 — Engine OpenCV, Canny → tô màu → MP4
- `elearning-hyperframes-video`: Giai đoạn 5 — Script và prompt → cảnh HTML/SVG → MP4 bằng HyperFrames (tự chủ v2)
- `elearning-manim-video`: Giai đoạn 5 — Diễn họa Vật lý lý thuyết, Sóng & Dao động, Thuật toán IT & Toán STEM bằng Manim
- `elearning-3dmol-video`: Giai đoạn 5 — Mô phỏng Hóa học & Cấu trúc Phân tử 3D bằng 3Dmol.js & RDKit
- `elearning-matterjs-video`: Giai đoạn 5 — Mô phỏng Vật lý Cơ học & Động lực học 2D bằng Matter.js
- `elearning-vexflow-video`: Giai đoạn 5 — Ký âm bản nhạc 2D, thanh cuộn Playhead & Piano Synth bằng VexFlow & Tone.js
- `elearning-cesium-video`: Giai đoạn 5 — Quả địa cầu 3D, Bản đồ số, Địa hình & Không gian Địa lý bằng CesiumJS & Leaflet
- `elearning-molstar-video`: Giai đoạn 5 — Cấu trúc Sinh học 3D, ADN/RNA, Protein & Enzyme bằng Molstar & RCSB PDB
- `elearning-virtual-lab-video`: Giai đoạn 5 — Mô phỏng Phòng Thí Nghiệm Ảo Khoa học Tự nhiên & STEM (Quang học Ray Optics, Mạch điện DC/RC, Sóng cơ học, Dao động, Điện trường & Cơ học 2D) bằng các thư viện mở MIT & Apache-2.0
- `elearning-pipeline`: Master Orchestrator điều phối toàn trình

---

## 2. Quy Tắc Khởi Động & Menu Tương Tác (Interactive Welcome Menu)

Mỗi khi bắt đầu một phiên làm việc mới, hoặc khi người dùng chào hỏi (`xin chào`, `hi`, `hello`, `bắt đầu`), hoặc khi người dùng chưa đưa ra yêu cầu cụ thể:
Agent **BẮT BUỘC chủ động hiển thị Menu 5 Bước dưới dạng trực quan, dễ bấm chọn**:

```text
Xin chào! Chào mừng bạn đến với Hệ thống Sản xuất Học liệu E-Learning & Whiteboard Animation.

Hiện tại hệ thống đã sẵn sàng. Bạn muốn thực hiện giai đoạn nào?
(Chỉ cần gõ số bước tương ứng, ví dụ: 1, 2, 4, 5...)

[1] Giai đoạn 1: Soạn kịch bản & đề cương bài giảng (elearning-script)
    👉 Nhập tài liệu thô trong inputs/documents/ -> Xuất kịch bản 4 cột (script.md, script.xls)

[2] Giai đoạn 2: Tạo ảnh slide Infographic 16:9 (elearning-images)
    👉 Thiết kế prompt 16:9 tiếng Việt, cấm vẽ tay -> Tạo ảnh qua Google Flow

[3] Giai đoạn 3: Đóng gói slide PowerPoint PPTX & PDF 16:9 (elearning-slides)
    👉 Hỗ trợ 9 nguồn: HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar, Virtual Lab hoặc Ảnh Infographic

[4] Giai đoạn 4: Thu âm giọng đọc TTS & Tạo phụ đề SRT (elearning-audio)
    👉 Tạo MP3 & phụ đề SRT bằng VieNeu-TTS v3 Turbo (Adam mặc định / 23 preset giọng Việt)

[5] Giai đoạn 5: Xuất Video bài giảng (elearning-video)
    👉 Chọn OpenCV (Whiteboard), HyperFrames (HTML/SVG), Manim (IT/Toán), 3Dmol (Hóa học), Matter.js (Vật lý), VexFlow (Âm nhạc), Cesium (Địa lý/Bản đồ), Molstar (Sinh học) hay Virtual Lab (Thí nghiệm Ảo)

[0] Toàn trình / Tự động định tuyến thông minh (elearning-pipeline)
    👉 Tự động quét tài nguyên hiện có (Pre-flight Check) và tự lập kế hoạch chạy liên hoàn
```

---

## 3. Quy Tắc Tiếp Nhận Lệnh Phím Tắt (Shorthand Number Commands)

Khi người dùng nhập số thứ tự hoặc câu lệnh ngắn gọn:
- **`1` hoặc `bước 1`:** Kích hoạt ngay [`.agents/skills/elearning-script/SKILL.md`](.agents/skills/elearning-script/SKILL.md).
- **`2` hoặc `bước 2`:** Kích hoạt ngay [`.agents/skills/elearning-images/SKILL.md`](.agents/skills/elearning-images/SKILL.md).
- **`3` hoặc `bước 3`:** Kích hoạt ngay [`.agents/skills/elearning-slides/SKILL.md`](.agents/skills/elearning-slides/SKILL.md).
- **`4` hoặc `bước 4`:** Kích hoạt ngay [`.agents/skills/elearning-audio/SKILL.md`](.agents/skills/elearning-audio/SKILL.md).
- **`5` hoặc `bước 5`:** Kích hoạt ngay [`.agents/skills/elearning-video/SKILL.md`](.agents/skills/elearning-video/SKILL.md).
- **`0` hoặc `tự động`:** Kích hoạt ngay [`.agents/skills/elearning-pipeline/SKILL.md`](.agents/skills/elearning-pipeline/SKILL.md) để chạy Pre-flight Check và định tuyến.

Khi kích hoạt bất kỳ kỹ năng nào, Agent tự động đọc nội dung `SKILL.md` của kỹ năng đó và thực thi chính xác theo các bước quy định.

### 3.1. Quy tắc chọn engine tại giai đoạn 5

- **Tệp quy chuẩn sản xuất dùng chung:** Mọi engine video đều **BẮT BUỘC** tuân thủ nghiêm ngặt các quy định về typography 36-42px/24-32px/16-18px, khoảng cách gap 15-30px, căn giữa dọc tự nhiên, phụ đề 44-48px không viền stroke, SRT Lockstep và B-roll Cutaway ngữ nghĩa tại: [video-production-principles.md](.agents/skills/elearning-video/references/video-production-principles.md).
- Nếu người dùng chưa chỉ rõ engine và chưa xác nhận lựa chọn cho tác vụ hiện tại, hỏi đúng: **"Bạn muốn xuất video bằng OpenCV, HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar hay Virtual Lab?"**. Đợi câu trả lời trước khi dựng/render; không mặc định engine kể cả khi chạy tự động/toàn trình.
- Nếu người dùng đã chọn engine cho tác vụ đang tiếp tục, giữ lựa chọn và không hỏi lại. Yêu cầu mới có quyền thay đổi lựa chọn; không tự áp dụng lựa chọn của video khác.
- **Chọn OpenCV:** đọc [elearning-opencv-video](.agents/skills/elearning-opencv-video/SKILL.md), thực hiện nguyên quy trình cũ bằng `core/whiteboard_engine.py`.
- **Chọn HyperFrames:** đọc [elearning-hyperframes-video](.agents/skills/elearning-hyperframes-video/SKILL.md), bắt đầu từ `output/<ma-mon-hoc>/video-<x>/script.md` và prompt thiết kế từng slide; hỗ trợ tùy biến Theme Preset (`light-whiteboard`, `dark-modern`, `ai-tech-neon`, `flat-editorial`) và tự động lồng ghép video B-roll minh họa từ `inputs/video-libraries/`; tích hợp đầy đủ hiệu ứng Spring physics, Code Studio typewriter, Visual Anchors 2D/SVG và xuất video qua `core/hf_engine.py`.
- **Chọn Manim:** đọc [elearning-manim-video](.agents/skills/elearning-manim-video/SKILL.md), bắt đầu từ `script.md`, `mp3`, `srt`; chuyên dụng cho bài toán giải thuật IT, cấu trúc dữ liệu, đồ thị, ma trận, công thức toán và STEM; sinh code Python scene trong `runtime/tasks/`, render qua `core/manim_engine.py`.
- **Chọn 3Dmol:** đọc [elearning-3dmol-video](.agents/skills/elearning-3dmol-video/SKILL.md), bắt đầu từ tên hợp chất hoặc mã SMILES; tự động sinh tọa độ không gian 3D qua RDKit, trực quan hóa WebGL bằng 3Dmol.js xoay 360 độ siêu nét, xuất video qua `core/mol3d_engine.py`.
- **Chọn Matter.js:** đọc [elearning-matterjs-video](.agents/skills/elearning-matterjs-video/SKILL.md), chuyên dụng cho bài giảng Vật lý Cơ học, ném xiên, va chạm đàn hồi, con lắc, ma sát và động lực học 2D; render qua `core/matterjs_engine.py`.
- **Chọn VexFlow:** đọc [elearning-vexflow-video](.agents/skills/elearning-vexflow-video/SKILL.md), chuyên dụng cho giáo trình Âm nhạc, ký âm khuông nhạc khóa Sol/Pha, mô phỏng thanh cuộn Playhead, phím đàn Piano sáng đèn và tổng hợp âm thanh Piano Synth; render qua `core/vexflow_engine.py`.
- **Chọn Cesium:** đọc [elearning-cesium-video](.agents/skills/elearning-cesium-video/SKILL.md), chuyên dụng cho bài giảng Địa lý, Quả địa cầu 3D, địa hình núi/biển, tọa độ và quỹ đạo camera Fly-to; render qua `core/cesium_engine.py`.
- **Chọn Molstar:** đọc [elearning-molstar-video](.agents/skills/elearning-molstar-video/SKILL.md), chuyên dụng cho bài giảng Sinh học, cấu trúc ADN/RNA, Protein p53, Hemoglobin, Insulin, Enzyme từ ngân hàng dữ liệu RCSB PDB; render qua `core/molstar_engine.py`.
- **Chọn Virtual Lab:** đọc [elearning-virtual-lab-video](.agents/skills/elearning-virtual-lab-video/SKILL.md), chuyên dụng cho bài giảng Khoa học Tự nhiên & STEM, thí nghiệm ảo Khúc xạ ánh sáng (Ray Optics), Mạch điện DC & RC, Sóng cơ học và Điện trường; render qua `core/virtual_lab_engine.py`.
- **Quy tắc thư mục học liệu sạch (Clean Output Policy):** Toàn bộ các engine video (`core/`, `engines/opencv`, `engines/hyperframes`, `core/manim_engine.py`, `core/mol3d_engine.py`, `core/matterjs_engine.py`, `core/vexflow_engine.py`, `core/cesium_engine.py`, `core/molstar_engine.py`, `core/virtual_lab_engine.py`, `engines/vexflow`, `engines/cesium`, `engines/molstar`, `engines/virtual_lab`) được đặt tập trung ở cấp dự án dùng chung. Cài đặt môi trường 1 chạm bằng `python scripts/prepare_env.py` hoặc `.\scripts\setup.ps1`. Tuyệt đối KHÔNG sinh `node_modules` hay `package.json` vào thư mục `output/<ma-mon-hoc>/video-<x>/`. Thư mục output chỉ chứa tài nguyên học liệu (kịch bản, audio, ảnh) và video hoàn thiện (.mp4).
- Lệnh `5`, yêu cầu tạo video chung và chuyển tiếp từ pipeline đều qua `elearning-video`. Gọi trực tiếp skill của một engine được coi là đã chọn engine đó.
- Chỉ hỏi lựa chọn khi đến giai đoạn video; yêu cầu riêng về ảnh, PPTX hoặc audio không cần hỏi engine.


---

## 4. Các Nguyên Tắc Sản Xuất Cốt Lõi Bắt Buộc (Core Principles)

> [!IMPORTANT]
> Toàn bộ các quy chuẩn mỹ thuật sản xuất video (Font hierarchy 36-42px/24-32px/16-18px, khoảng cách gap 15-30px, căn giữa dọc tự nhiên, phụ đề 44-48px Be Vietnam Pro ExtraBold không viền stroke, SRT Lockstep và B-roll Cutaway ngữ nghĩa động đa clip) đã được chuẩn hóa dùng chung tại:
> 👉 [Quy Chuẩn Sản Xuất Video E-Learning Chung](.agents/skills/elearning-video/references/video-production-principles.md)

### 4.1. Quy chuẩn Prompt Tạo Ảnh (100% Tiếng Việt - Triệt tiêu Tiếng Anh)
- **Lệnh ngôn ngữ tối cao ở đầu MỌI Prompt:** Mọi prompt tạo ảnh BẮT BUỘC bắt đầu bằng:
  `[YÊU CẦU NGÔN NGỮ TỐI CAO: Toàn bộ chữ hiển thị trên ảnh BẮT BUỘC 100% LÀ TIẾNG VIỆT CÓ DẤU CHÍNH XÁC. TUYỆT ĐỐI KHÔNG CÓ CHỮ TIẾNG ANH, TỪ NGỮ TIẾNG ANH HAY KÝ TỰ VÔ NGHĨA. ALL TEXT IN IMAGE MUST BE VIETNAMESE ONLY, STRICTLY NO ENGLISH WORDS, NO GIBBERISH LETTERS.]`
- **Chỉ định chuỗi ký tự chính xác:** Toàn bộ chữ hiển thị trên ảnh phải được đóng trong dấu ngoặc kép `"..."`.
- **Negative Prompt chặn chữ tiếng Anh & rác chữ ở cuối:**
  `[ĐIỀU CẤM KỴ TUYỆT ĐỐI & NEGATIVE PROMPT: Không có chữ tiếng Anh, không có từ tiếng Anh, không có chữ cái Latin vô nghĩa. Cấm vẽ bàn tay người, cánh tay, ngón tay, bút vẽ, bút chì, bút lông. Negative prompt: English text, English words, Latin gibberish, foreign language, misspelled English words, human hands, human arms, fingers, pens, markers, pencils, realistic 3D, blur, watermark]`

### 4.2. Quy chuẩn Văn Phong Kịch Bản (100% Tích cực)
- Luôn tập trung làm nổi bật ưu điểm, điểm sáng, tính ứng dụng thực chiến và giá trị của sản phẩm.
- **Tuyệt đối KHÔNG so sánh tiêu cực** hoặc chỉ trích, nêu nhược điểm của các phương pháp đào tạo khác, trường khác hay đối tác khác (không dùng từ ngữ tiêu cực như "học vẹt", "thợ gõ mù quáng", "CV trắng trơn"...).

### 4.3. Kiến trúc Chuỗi Video Mở Rộng ("Video Chung – Video Riêng")
- **Video Chung (Đầu & Cuối):** Giới thiệu nền tảng hệ sinh thái BUNI, uy tín hợp tác PTIT – Bachkhoa Aptech, triết lý "Làm trước học sau", 4 cấp độ dự án và Hộ chiếu nghề nghiệp Career Passport.
- **Video Riêng (Ở giữa):** Chuyên sâu theo từng khung chương trình cụ thể (BUNI-AI01, BUNI-AI02...). Dễ dàng mở rộng thêm các video chuyên ngành mới mà không ảnh hưởng video chung.

### 4.4. Quy Chuẩn Video Trám Cảnh Minh Họa Ngữ Nghĩa & Thời Lượng Động (Semantic & Dynamic B-roll Cutaway)
- **Bản chất & Mục đích:** Video minh họa chèn toàn màn hình 16:9 ($1920\times 1080$) cắt ngang dòng thời gian (Cutaway) nhằm làm sinh động lời giảng, xóa bỏ cảm giác nhàm chán của slide tĩnh. **Tuyệt đối KHÔNG dùng khung nhỏ PiP nổi ở góc.**
- **Phân biệt thời điểm: Khi nào hiện Slide và Khi nào Trám cảnh?**
  * **Hiển thị Slide:** Khi lời giảng tập trung trực tiếp vào nội dung bài học, đọc tiêu đề, hoặc phân tích chi tiết từng gạch đầu dòng/khối thẻ trên slide (áp dụng nghiêm ngặt nguyên tắc **SRT Lockstep: Nói đến đâu hiện đến đó**).
  * **Trám cảnh Minh họa:** Khi lời giảng **thoát ly khỏi các gạch đầu dòng trên slide** để mở rộng liên hệ thực tế, chia sẻ bối cảnh thực trạng ngoài đời, kể câu chuyện doanh nghiệp, đặt vấn đề định hướng, hoặc đúc kết ứng dụng thực tiễn.
- **Thời lượng trám linh hoạt theo ngữ nghĩa (Dynamic Duration):**
  * **Tuyệt đối KHÔNG cố định 4–6 giây.** Thời lượng trám cảnh được xác định chính xác theo độ dài của đoạn lời giảng ngoại cảnh trong file SRT (có thể là 4s, 8s, 12s, 15s hoặc lâu hơn tùy ý đồ sư phạm).
  * Ngay khi lời giảng quay trở lại phân tích nội dung chính của slide, video lập tức chuyển mượt mà (crossfade/cut) về lại slide để tiếp tục hiển thị nội dung học tập.
- **Cơ chế Ghép Nối Đa Clip (Multi-Clip Chaining):**
  * Khi một đoạn giải thích ngoại cảnh kéo dài (ví dụ 10s–16s) mà một clip trong thư viện không đủ dài, hoặc để tránh việc người học nhìn mãi một góc quay tĩnh gây buồn ngủ: Agent **bắt buộc ghép nối liên tiếp 2 đến 3 đoạn video clip khác nhau** (mỗi clip 4–7s) cùng chủ đề để bao trọn thời lượng của đoạn thuyết minh đó như một thước phim phóng sự tài liệu chuyên nghiệp.
- **Lựa chọn nội dung video theo ngữ nghĩa (Content-Aware Matching):**
  * Agent phân tích chính xác chủ đề của đoạn lời giảng đang nói (nói về nhân sự/văn phòng $\to$ clip văn phòng; nói về robot/tự động hóa $\to$ clip AI robotics; nói về máy chủ/hạ tầng/code $\to$ clip máy tính/lập trình; nói về thị trường/kinh doanh $\to$ clip doanh nghiệp...).
- **Hỗ trợ nhiều đợt trám cảnh trong cùng 1 cảnh (Multiple Cutaways per Scene):**
  * Một cảnh có thể có nhiều đợt trám cảnh xen kẽ (ví dụ: Đầu cảnh mở bài $\to$ Trình bày ý 1 $\to$ Trám cảnh thực tế 12s giữa chừng $\to$ Trình bày tiếp ý 2 $\to$ Trám cảnh đúc kết trước khi kết thúc).
- **Lớp hiển thị bảo đảm thông tin:** Phụ đề đáy (`z-index: 1000`) và nhãn phân loại/trạng thái (`z-index: 600`) luôn hiển thị sắc nét trên nền video trám cảnh qua dải gradient tối mờ.

### 4.5. Quy Chuẩn Bố Cục Khoảng Cách & Căn Chỉnh Trục Dọc (Spacing & Natural Vertical Centering)
- **Tiêu đề chính:** Luôn đặt ở góc trên bên trái (`slide-header`, kích thước $36\text{px} – 42\text{px}$).
- **Khoảng cách giữa các phần tử:** Nghiêm ngặt từ **$15\text{px} – 30\text{px}$** (chuẩn tối ưu `gap: 18px` đến `24px`).
- **Cấm kỵ khoảng cách rỗng:** Tuyệt đối KHÔNG dùng `justify-content: space-between` để kéo dãn các khối nội dung tràn ngập chiều cao làm loãng thị giác.
- **Căn giữa dọc tự nhiên:** Khi slide có lượng nội dung ít, ưu tiên căn giữa theo chiều dọc (`margin: auto 0` trên container nội dung), các thẻ card ôm vừa vặn nội dung với `padding: 24px–32px`, không kéo dãn cưỡng bức $100\%$ chiều cao.

### 4.6. Quy Chuẩn Phân Cấp Cỡ Chữ & Kiểu Dáng Phụ Đề (Typography & Subtitles)
- **Phân cấp cỡ chữ (Hierarchy):**
  * Tiêu đề chính (Slide Title / H1): $36\text{px} – 42\text{px}$ (đậm, nổi bật).
  * Tiêu đề phụ / Khối thẻ (Card Headings / H2, H3): $24\text{px} – 32\text{px}$.
  * Nội dung chi tiết / Tính năng (Body text): $16\text{px} – 18\text{px}$ (chú thích nhỏ tối thiểu $14\text{px}$).
- **Phụ đề đáy màn hình (Subtitles):**
  * Kích thước lớn dễ đọc: **$44\text{px} – 48\text{px}$**, font chữ **Be Vietnam Pro ExtraBold**.
  * **Tuyệt đối KHÔNG có viền đen stroke lem luốc**: Dùng drop-shadow nhẹ hoặc dải mờ gradient đáy.
  * **Màu chữ tùy biến theo theme**: Chữ đen `#1A202C` trên nền sáng, chữ trắng `#F8FAFC` trên nền tối; phân đoạn ngắn 6–8 từ.

### 4.7. Quy Chuẩn Đồng Bộ Khớp Giọng Đọc Tuyệt Đối (SRT Lockstep Synchronization)
- **Nguyên tắc tối cao "Nói đến đâu – Hiện đến đó":** Bullet point, icon hay thẻ nội dung chỉ xuất hiện chính xác tại giây giọng đọc trong SRT bắt đầu nhắc đến từ khóa đó.
- **Cấm kỵ hiện sớm:** Tuyệt đối KHÔNG để nội dung xuất hiện trước 3–5 giây so với lời giảng.

### 4.8. Quy Chuẩn Chuẩn Hóa Phát Âm Giọng Đọc TTS (TTS Pronunciation)
- **Engine TTS:** **VieNeu-TTS v3 Turbo** (ONNX · CPU · offline · 23 preset giọng Việt). Mặc định giọng **Adam** (Nam · Nam · Giọng đọc tự nhiên). Xem danh sách 23 preset trong `core/audio_tts_engine.py` → `VIENEU_VOICES`.
- **Chuẩn hóa thuật ngữ IT:** Toàn bộ từ viết tắt/thuật ngữ tiếng Anh (React, Docker, Microservices, Spring Boot, API, Redis, Kafka...) phải được chuyển đổi qua bộ từ điển phiên âm tiếng Việt (trong `core/pronunciation_dict.py`) trước khi tổng hợp giọng đọc VieNeu-TTS để đọc chuẩn âm tiết tiếng Việt.
- **Tốc độ đọc chuẩn:** `speed=0.92` (tương đương `-8%`), trầm ấm, từ tốn, đúng chuẩn sư phạm. Không bắt buộc GPU; chạy hoàn toàn trên CPU.

---

## 5. Quy Chuẩn Tối Ưu Hóa Token & Vận Hành Pipeline Tinh Gọn (DevOps Token Efficiency)

- **Cấu hình loại trừ Context (`.antigravityignore`):** Toàn bộ thư mục tạm `runtime/`, sản phẩm đầu ra binary (`output/**/mp3/`, `images/`, `hyperframes/`, `.mp4`, `.png`), video thô B-roll (`inputs/video-libraries/`) và môi trường ảo (`.venv/`, `node_modules/`) đều được loại trừ khỏi Context Window để triệt tiêu tiêu hao token thừa.
- **Thực thi lệnh Terminal ngắn gọn (Silent/Terse Output):** Khi chạy các lệnh kiểm thử hoặc cài đặt, luôn bổ sung các cờ im lặng/ngắn gọn (`pytest -q`, `pip install -q`, v.v.), hạn chế in log tràn lan gây tốn token context.
- **Quy tắc kiểm thử Visual / Browser ngầm định:** Mặc định KHÔNG tự ý mở Browser Auto-capture / chụp ảnh màn hình trừ khi người dùng yêu cầu rõ ràng hoặc thực thi riêng khâu kiểm tra mỹ thuật hình ảnh `elearning-images` / HyperFrames render.


