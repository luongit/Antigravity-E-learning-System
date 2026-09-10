# Hợp đồng cảnh E-Learning → HyperFrames

Đọc trước khi lập storyboard/manifest. Manifest là dữ liệu do agent trích và kiểm tra từ script, không phải bộ parser bảng Markdown tự động.

## Tệp đầu ra

```text
video-<x>/
├── script.md
├── prompts/
├── images/                     # tùy chọn
├── mp3/
├── hyperframes/
│   ├── DESIGN.md
│   ├── storyboard.md
│   ├── scene-manifest.json
│   ├── index.html
│   ├── compositions/
│   ├── assets/                 # media và font cục bộ
│   └── qa.md
└── Video <X> - <Tên Video>.mp4
```

CLI có thể tạo thêm package.json, lockfile, hyperframes.json và thư mục làm việc. Giữ chúng khi cần tái lập render. Không đặt source composition chỉ trong runtime/cache.

## Trường dữ liệu

Manifest có `schema_version`, `engine: "hyperframes"`, `cli_version`, `source_script`, `width: 1920`, `height: 1080`, `fps: 30`, `duration_seconds`, `scenes`.

Mỗi cảnh ghi:

| Trường | Ý nghĩa |
|---|---|
| `id`, `source_row`, `order` | ID duy nhất, STT gốc và thứ tự cảnh |
| `slide_content`, `design_prompt`, `prompt_source` | Nội dung và mô tả thiết kế lấy từ nguồn nào |
| `voice_text` | Lời thoại nguyên bản, không gồm cột prompt |
| `audio`, `srt` | Đường dẫn tương đối tính từ thư mục manifest, đúng số cảnh |
| `start_seconds`, `audio_duration_seconds`, `duration_seconds` | Thời gian thật và khoảng giữ/chuyển cảnh |
| `timing_quality` | `estimated`, `aligned` hoặc `reviewed`; ghi căn cứ trong QA |
| `elements` | Vai trò, nội dung, vùng bố cục và tài nguyên từng phần tử |
| `cutaways` | Danh sách các đợt trám cảnh toàn màn hình theo ngữ nghĩa (start, duration, chained clips, badge_text) khi lời giảng thoát ly slide |
| `cues` | ID phần tử, thời gian cục bộ, kiểu chuyển động và mốc lời giảng theo nguyên tắc SRT Lockstep |
| `transition` | Kiểu, thời lượng, vùng overlap hình nếu có |

`storyboard.md` mô tả theo từng cảnh: ý chính → bố cục → chuyển động → lời đọc và tài nguyên. Prompt phải được diễn giải thành hình cụ thể; không chỉ chép prompt vào manifest rồi tuyên bố đã dựng.

## Điều kiện trước render

- Mỗi dòng slide có đúng một cảnh; ID/STT ánh xạ rõ, không mất dòng hoặc nhầm video.
- Voice text đối chiếu script đã chốt; MP3 cũ chỉ tái sử dụng khi đúng lời hiện tại.
- Audio/SRT tồn tại và đọc được; SRT có start < end, thứ tự hợp lệ, không vượt audio. Thiếu media thì bổ sung trước render.
- Các phần tử được xuất hiện trong khoảng cảnh; camera cố định; toàn bộ nội dung cần đọc hiện đủ lâu.
- Tổng thời gian tính theo audio + hold + transition, trừ phần overlap hình đúng một lần. Không overlap lời đọc.
- Tài nguyên/font được đóng gói cục bộ để render không phụ thuộc URL tạm.
- Lưu thời điểm chụp QA, kết quả kiểm tra, lệnh và phiên bản thực chạy. Không ghi `aligned`/`reviewed` nếu chưa căn chỉnh/nghe kiểm tra.

## Cập nhật nguồn

Khi script/prompt thay đổi, cập nhật cảnh tương ứng và các offset phía sau nếu thời lượng đổi. Khi lời đọc đổi, tạo lại MP3/SRT liên quan. Giữ các cảnh không liên quan và tài nguyên gốc. Khi nhiều engine cùng xuất sản phẩm, không ghi đè sản phẩm khác ngoài yêu cầu.
