---
name: elearning-audio
description: Giai đoạn 4 - Tạo MP3 và SRT bằng VieNeu-TTS v3 Turbo (offline, ONNX, CPU) với 23 preset giọng Việt. Mặc định giọng Adam. Dùng khi người dùng yêu cầu thu âm, TTS hoặc phụ đề.
---

# E-Learning Stage 4: Thu Âm Giọng Đọc TTS & Tạo Phụ Đề SRT Phân Đoạn Ngắn

## 1. Vai trò & Mục tiêu
Chuyển đổi văn bản lời giảng (Voice Script) thành các tệp âm thanh giọng đọc chuẩn sư phạm (`.mp3`), đồng thời tự động xuất tệp phụ đề (`.srt`) phân đoạn ngắn để làm căn cứ thời gian (Timestamp) kích hoạt các chuyển động xuất hiện trên màn hình.

- **Thư mục đầu vào:**
  - File kịch bản `output/<ma-mon-hoc>/script.md` HOẶC
  - File người dùng tự cung cấp: `inputs/voice_scripts/voice_script.txt` (được phân tích qua `core/voice_parser.py`).
- **Thư mục đầu ra:**
  - `output/<ma-mon-hoc>/video-<x>/mp3/mp3-X.mp3` (File âm thanh từng slide)
  - `output/<ma-mon-hoc>/video-<x>/mp3/mp3-X.srt` (File phụ đề phân đoạn ngắn từng slide)

---

## 2. Hệ Thống Giọng Đọc VieNeu-TTS v3 Turbo (23 Preset)

**Engine:** VieNeu-TTS v3 Turbo | ONNX · CPU · Offline | MIT License

### 2.1. Giọng Nam (12 giọng)

| Tên giọng | Vùng | Phong cách |
|-----------|------|-----------|
| **Adam** *(MẶC ĐỊNH)* | Nam | Giọng đọc tự nhiên |
| Minh Đức | Bắc | Tin tức |
| Phạm Tuyên | Bắc | Tự nhiên |
| Thái Sơn | Nam | Kể chuyện |
| Xuân Vĩnh | Bắc | Tự nhiên |
| Thanh Bình | Bắc | Kể chuyện |
| Minh Triết | Nam | Tin tức |
| Quang Sơn | Trung | Tự nhiên |
| Đức Trí | Nam | Đọc truyện |
| Mạnh Dũng | Bắc | Tự nhiên |
| Minh Quân | Bắc | Tự nhiên |
| Anh Khôi | Bắc | Kể chuyện |

### 2.2. Giọng Nữ (11 giọng)

| Tên giọng | Vùng | Phong cách |
|-----------|------|-----------|
| Trúc Ly | Bắc | Tự nhiên |
| Ngọc Linh | Bắc | Kể chuyện |
| Đoan Trang | Bắc | Tự nhiên |
| Mai Anh | Bắc | Tin tức |
| Thục Đoan | Nam | Kể chuyện |
| Thùy Dung | Nam | Tin tức |
| Ngọc Trân | Trung | Tự nhiên |
| Mỹ Duyên | Nam | Đọc truyện |
| Quỳnh Anh | Bắc | Đọc truyện |
| Kim Thanh | Nam | Đọc truyện |
| Ngọc Huyền | Bắc | Giọng đọc tự nhiên |

> **Tốc độ đọc khuyến nghị:** `speed=0.92` (tương đương `-8%`) để giọng nói từ tốn, ấm áp, đúng phong thái giảng bài và khớp nhịp vẽ whiteboard.

---

## 3. Chuẩn Hóa Phát Âm Thuật Ngữ IT (Pronunciation Dictionary)

Bắt buộc áp dụng từ điển phiên âm âm tiết tiếng Việt trong `core/audio_tts_engine.py` / `core/pronunciation_dict.py` để máy đọc tròn vành rõ chữ, không bị ngắc ngứ hay nuốt âm:
- `Flowchart` → `phờ lâu chác`
- `Pseudocode` → `mã giả su đô cốt`
- `Syntax` → `xin tắc`
- `Bug` → `bấc`, `Debug` → `đi bấc`, `Debugging` → `đi bấc ghinh`
- `File log` → `phai lốc`, `Log` → `lốc`
- `Brute-force` → `bơ rút-phoóc`
- `Case study` → `kết xì ta-đi`, `Test-case` → `tét kây-sơ`
- `Ishikawa` → `Í-si-ka-oa`, `5 Whys` → `5 Lần Tại Sao`
- `Root Cause` → `nguyên nhân gốc rễ`, `Symptom` → `triệu chứng bề mặt`
- `Memory Leak` → `tràn bộ nhớ Me mo ry lích`, `Index SQL` → `chỉ mục ét quy eo`
- `Flash Sale` → `Phơ lát xeo`, `Full Table Scan` → `Phun thây bồ xờ ken`

*(Nguyên tắc bất biến: Khi xuất file phụ đề SRT hiển thị lên màn hình, tự động giữ nguyên từ viết chuẩn tiếng Anh hoa mỹ, không để lộ từ phiên âm thô).*

---

## 4. Quy Chuẩn Phụ Đề SRT Phân Đoạn Ngắn (Short Chunking)

- **Chia nhỏ câu thoại:** Mỗi phân đoạn SRT chỉ dài **6–8 từ** (thay vì để nguyên câu dài 25–30 từ).
- **Lợi ích:**
  1. Phụ đề hiển thị to rõ 42px ở đáy màn hình mà không bị tràn viền hay che khuất hình vẽ.
  2. Timestamp phân đoạn ngắn cung cấp mốc thời gian chính xác từng giây để kích hoạt các khối nội dung xuất hiện theo nguyên tắc: *"Nói đến đâu – Xuất hiện đến đó"*.

---

## 5. Cách Thức Triển Khai (Mẫu Code)

```python
from pathlib import Path
from core.voice_parser import parse_voice_script
from core.audio_tts_engine import generate_tts_audio_and_srt, clean_and_phoneticize_text

def produce_all_audio(voice_script_path: Path, output_mp3_dir: Path, voice: str = "Adam"):
    sections = parse_voice_script(str(voice_script_path))
    output_mp3_dir.mkdir(parents=True, exist_ok=True)

    for s in sections:
        idx = s["index"]
        raw_text = s["text"]
        phonetic_text = clean_and_phoneticize_text(raw_text)

        mp3_file = output_mp3_dir / f"mp3-{idx}.mp3"
        srt_file = output_mp3_dir / f"mp3-{idx}.srt"

        dur = generate_tts_audio_and_srt(
            display_text=raw_text,
            spoken_text=phonetic_text,
            out_mp3=mp3_file,
            out_srt=srt_file,
            voice=voice,
            speed=0.92       # ~-8%, từ tốn chuẩn sư phạm
        )
        print(f"Slide {idx}: {dur:.1f}s -> {mp3_file.name}")

if __name__ == "__main__":
    produce_all_audio(
        Path("inputs/voice_scripts/voice_script.txt"),
        Path("output/KNM01/video-1/mp3")
    )
```

> **Ghi chú:** Hàm `generate_tts_audio_and_srt` là hàm chính. Alias cũ `generate_edge_tts_audio_and_srt` (async) vẫn được giữ lại để backward-compat với script cũ — nó tự động chuyển hướng sang VieNeu.
