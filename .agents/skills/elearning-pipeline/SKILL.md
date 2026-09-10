---
name: elearning-pipeline
description: Điều phối 5 giai đoạn sản xuất E-Learning từ tài liệu, kịch bản, ảnh hoặc audio sẵn có. Kiểm kê tài nguyên và đến giai đoạn 5 định tuyến OpenCV hoặc HyperFrames theo lựa chọn người dùng.
---

# Điều phối toàn trình E-Learning

## Các skill

| Bước | Skill | Đầu ra |
|---|---|---|
| 1 | [elearning-script](../elearning-script/SKILL.md) | Đề cương, kịch bản 4 cột, lời thoại từng video |
| 2 | [elearning-images](../elearning-images/SKILL.md) | Prompt và ảnh infographic 16:9 |
| 3 | [elearning-slides](../elearning-slides/SKILL.md) | PowerPoint phủ kín ảnh |
| 4 | [elearning-audio](../elearning-audio/SKILL.md) | MP3 Nam Minh/Hoài My và SRT |
| 5 | [elearning-video](../elearning-video/SKILL.md) | Chọn engine và điều phối xuất video |
| 5 | [elearning-opencv-video](../elearning-opencv-video/SKILL.md) | Quy trình Canny/ảnh/bàn tay hiện tại |
| 5 | [elearning-hyperframes-video](../elearning-hyperframes-video/SKILL.md) | Script + prompt → cảnh HTML/SVG → MP4 |

## Pre-flight và lựa chọn engine

Xác định đúng thư mục video trước khi chạy từ gốc dự án:

```powershell
python core/preflight.py "output/<ma-mon-hoc>/video-<x>" --json
```

Đây là kiểm kê tài nguyên, không tự cấp quyền chọn engine. Khi đến giai đoạn 5, luôn vào `elearning-video`:

```powershell
python core/preflight.py "output/<ma-mon-hoc>/video-<x>" --stage video --json
```

Nếu người dùng chưa chỉ rõ engine, hỏi đúng **"Bạn muốn xuất video bằng OpenCV, HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar hay Virtual Lab?"** và đợi câu trả lời. Không chọn mặc định theo ảnh, audio, tên thư mục hoặc chế độ tự động. Lựa chọn đã xác nhận cho tác vụ hiện tại được giữ khi tiếp tục; không hỏi lại. Sau lựa chọn, kiểm tra điều kiện nhánh tương ứng.


## Định tuyến theo đầu vào

- **Tài liệu thô:** `elearning-script` phân tích Biết–Hiểu–Làm được, đề cương Blended Learning, video chung–riêng. Giữ checkpoint duyệt bước 4 của skill này trước kịch bản chi tiết. Sau khi chốt, sản xuất các đầu ra được giao. Toàn trình có thể chạy bước 2–4 rồi đến router bước 5; nếu đã chọn HyperFrames và chỉ cần video, ảnh slide phẳng/PPTX không phải điều kiện dựng cảnh.
- **Ảnh + voice script:** có thể tạo audio qua bước 4; đến bước 5 hỏi engine nếu chưa rõ. OpenCV dùng ảnh/audio như cũ. HyperFrames cần `script.md` riêng của video có nội dung và prompt; nếu thiếu, nêu thiếu nguồn thay vì giả vờ ảnh và voice script đã đủ.
- **Ảnh + MP3/SRT:** đến router bước 5. OpenCV kiểm tra các cặp slide/audio và render như hiện tại. Nếu chọn HyperFrames, đọc script/prompt theo nhánh mới; không mặc định OpenCV vì đã có ảnh.
- **Script riêng của video + prompt:** khi chọn HyperFrames, đi thẳng vào skill tương ứng; dựng cảnh từ script, dùng bước 4 để bổ sung audio còn thiếu. Không yêu cầu người dùng tạo ảnh trước.
- **Chỉ yêu cầu audio/PPTX/ảnh:** thực hiện đúng skill được yêu cầu; không hỏi engine video khi chưa đến giai đoạn 5.
- **Thiếu hoặc lệch dữ liệu:** báo đúng phần thiếu của engine đã chọn. Không lấy kịch bản/MP3 từ video khác và không bỏ qua slide lệch. Pre-flight đếm tệp không thay thế kiểm tra nội dung/media.

## Cấu trúc và sản phẩm

`core/` giữ thư viện dùng chung; `.agents/skills/` chứa 8 skill; `inputs/` chứa nguyên liệu; `runtime/` chứa script tạm, cache và log. Không thay đổi engine OpenCV trong tác vụ dựng video thông thường.

```text
output/<ma-mon-hoc>/
├── plan.md, plan.json
├── script.md, script.xls
├── labguide.md
└── video-<x>/
    ├── script.md
    ├── voice-script.md
    ├── prompts/
    ├── images/
    ├── mp3/
    ├── hyperframes/                 # chỉ khi dùng HyperFrames, giữ nguồn dựng
    ├── Bài <X> - <Tên>.pptx
    └── Video <X> - <Tên>.mp4
```

Voice script riêng chứa lời đọc từng slide, có thể dùng nhãn `Đoạn 1:`/`Slide 1:` hoặc tách bằng dòng trống. Bảng script 4 cột cần trích riêng cột lời đọc trước TTS.

Tự động tiếp tục các giai đoạn đã được giao, sửa lỗi có thể xử lý và kiểm tra sản phẩm thực tế. Chế độ tự động hoặc `/goal` không bỏ qua lựa chọn engine còn thiếu và checkpoint nội dung. Không tuyên bố hoàn tất khi chưa có sản phẩm đã kiểm tra.
