# HyperFrames TTS — Kokoro cục bộ

## Phạm vi miễn phí và ngôn ngữ

Đã đối chiếu tài liệu chính thức ngày 2026-09-07:

- HyperFrames có giấy phép Apache 2.0. Lệnh `hyperframes tts` tổng hợp cục bộ bằng Kokoro; không cần khóa API và không mất phí theo lượt đọc. Cần tài nguyên máy và tải model lần đầu; offline sau khi đã có đủ model/phụ thuộc.
- Kokoro-82M có trọng số theo Apache 2.0. Dịch vụ cloud dùng Kokoro hoặc HeyGen có chính sách riêng; không suy ra miễn phí từ giấy phép model.
- Ngôn ngữ CLI đang liệt kê: `en-us`, `en-gb`, `es`, `fr-fr`, `hi`, `it`, `pt-br`, `ja`, `zh`. **Chưa có tiếng Việt**, không có Nam Minh/Hoài My.
- HeyGen OAuth có đường dùng theo hạn mức miễn phí; API key có thể tính phí. Nhánh này chỉ dùng Kokoro local, không đăng nhập hoặc gọi cloud thay thế.

Nguồn: [HyperFrames LICENSE](https://github.com/heygen-com/hyperframes/blob/main/LICENSE), [TTS CLI và ngôn ngữ](https://github.com/heygen-com/hyperframes/blob/main/skills/media-use/audio/references/tts.md), [Kokoro model card](https://huggingface.co/hexgrad/Kokoro-82M), [providers](https://github.com/heygen-com/hyperframes/blob/main/skills/media-use/references/setup-providers.md).

## Quy trình thực hiện

1. Đọc lời thoại đã chốt của từng slide, xác định ngôn ngữ. Tách cột Voice Script nếu đầu vào là bảng `script.md`; không đọc nội dung slide/prompt như lời thoại. Giữ nguyên kịch bản, không dùng từ điển phiên âm IT tiếng Việt cho lời ngoại ngữ.
2. Đọc skill HyperFrames CLI đang có, xác định phiên bản phù hợp và ghim phiên bản khi thực thi. Kiểm tra `tts --help` và `tts --list` của chính phiên bản đó. Node.js ≥22; nhánh Kokoro cần Python với `kokoro-onnx`, `soundfile` và model/voices. Ngôn ngữ ngoài tiếng Anh có thể cần `espeak-ng`. Kiểm tra thực tế trước cài đặt, giữ thư viện/model cục bộ; không mặc định cài model khi chỉ cập nhật skill.
3. Chọn voice từ danh sách thực tế, khớp ngôn ngữ. Ví dụ tiếng Anh `af_heart`, `am_michael`, `bf_emma`. Tham số tốc độ Kokoro là hệ số (`--speed`, nếu phiên bản hỗ trợ), không dùng `rate="-8%"` của Edge-TTS. Có thể bắt đầu ở 0.9 cho bài giảng và nghe kiểm tra.
4. Lưu từng lời thoại vào TXT UTF-8 trong thư mục tạm riêng của video, gọi CLI bằng đường dẫn tệp để tránh lỗi shell. Sinh WAV rồi chuyển thành `mp3/mp3-X.mp3` qua FFmpeg để tương thích hai engine video. Không đổi đuôi WAV thành MP3.
5. Kokoro CLI không tự cung cấp word timestamps. Tạo transcript từ audio bằng công cụ transcription tương thích của phiên bản HyperFrames đã chọn, đúng ngôn ngữ và model đa ngôn ngữ khi cần. Đối chiếu văn bản nhận dạng với lời thoại gốc, đặc biệt tên riêng/thuật ngữ. Chia SRT thành cụm ngắn 6–8 từ khi phù hợp, giữ nội dung lời thoại gốc và dùng mốc thời gian đã căn chỉnh. Không tuyên bố SRT chính xác theo từ nếu chỉ chia đều thời lượng.
6. Nếu chưa có công cụ căn chỉnh, báo rõ phần SRT chưa hoàn tất; có thể lưu phụ đề ước lượng kèm nhãn `timing_quality: estimated` cho bản nháp. Không đánh dấu sẵn sàng video đồng bộ chính xác trước khi kiểm tra.
7. Kiểm tra MP3 nghe được, thời lượng >0, SRT tăng dần với start < end, không vượt thời lượng audio, không thiếu slide. Lưu `mp3/tts-metadata.json` với engine, phiên bản CLI, voice, ngôn ngữ, speed, file và chất lượng thời gian từng slide. Giữ audio cũ khi tạo bản thử, không ghi đè ngoài phạm vi yêu cầu.

## Lệnh tham khảo

Thay `<VERSION>` bằng phiên bản đã kiểm tra và `<X>` bằng số slide. Chạy từ thư mục video. Đối chiếu cờ với `--help` trước dùng; không chạy nguyên placeholder.

```powershell
npx hyperframes@<VERSION> tts --help
npx hyperframes@<VERSION> tts --list
npx hyperframes@<VERSION> tts "tts-work/voice-<X>.txt" --voice af_heart --speed 0.9 --output "tts-work/voice-<X>.wav"
ffmpeg -n -i "tts-work/voice-<X>.wav" -codec:a libmp3lame -q:a 2 "mp3/mp3-<X>.mp3"
npx hyperframes@<VERSION> transcribe --help
```

Tệp transcript không mặc nhiên là SRT; đọc schema output thực tế và xuất SRT chuẩn sau khi đối chiếu. Việc thêm nhánh skill chưa chứng minh CLI/model đã được cài hoặc đã sinh audio thành công.
