"""
core/audio_tts_engine.py
Động cơ tổng hợp giọng đọc (TTS Engine) và tạo phụ đề SRT phân đoạn ngắn.
Hỗ trợ:
- VieNeu-TTS v3 Turbo (ONNX + CPU, offline, 23 preset voices):
  * Mặc định: Adam (Nam · Nam · Giọng đọc tự nhiên)
  * Xem VIENEU_VOICES để biết danh sách đầy đủ.
- Từ điển chuẩn hóa phát âm thuật ngữ kỹ thuật, viết tắt, danh từ riêng
- Phân chia phụ đề thành các phân đoạn ngắn 6-8 từ/cụm để hiển thị subtitle 48px
"""

import os
import re
import sys
import wave
import struct
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# DANH SÁCH GIỌNG ĐỌC VIENEU V3 TURBO (23 preset voices)
# Key = tên ngắn dùng trong code/SKILL
# Value = preset key trong VieNeu (exact string từ list_preset_voices())
# ─────────────────────────────────────────────────────────────────────────────
VIENEU_VOICES: Dict[str, str] = {
    # ─── Giọng Nam ───────────────────────────────────────────────────────────
    "Adam":         "Adam",          # Nam · Nam · Giọng đọc tự nhiên (MẶC ĐỊNH)
    "Minh Đức":     "Minh Đức",      # Nam · Bắc · Phong cách tin tức
    "Phạm Tuyên":   "Phạm Tuyên",    # Nam · Bắc · Phong cách tự nhiên
    "Thái Sơn":     "Thái Sơn",      # Nam · Nam · Phong cách kể chuyện
    "Xuân Vĩnh":    "Xuân Vĩnh",     # Nam · Bắc · Phong cách tự nhiên
    "Thanh Bình":   "Thanh Bình",    # Nam · Bắc · Phong cách kể chuyện
    "Minh Triết":   "Minh Triết",    # Nam · Nam · Phong cách tin tức
    "Quang Sơn":    "Quang Sơn",     # Nam · Trung · Phong cách tự nhiên
    "Đức Trí":      "Đức Trí",       # Nam · Nam · Phong cách đọc truyện
    "Mạnh Dũng":    "Mạnh Dũng",     # Nam · Bắc · Phong cách tự nhiên
    "Minh Quân":    "Minh Quân",     # Nam · Bắc · Phong cách tự nhiên
    "Anh Khôi":     "Anh Khôi",      # Nam · Bắc · Phong cách kể chuyện
    # ─── Giọng Nữ ───────────────────────────────────────────────────────────
    "Trúc Ly":      "Trúc Ly",       # Nữ · Bắc · Phong cách tự nhiên
    "Ngọc Linh":    "Ngọc Linh",     # Nữ · Bắc · Phong cách kể chuyện
    "Đoan Trang":   "Đoan Trang",    # Nữ · Bắc · Phong cách tự nhiên
    "Mai Anh":      "Mai Anh",       # Nữ · Bắc · Phong cách tin tức
    "Thục Đoan":    "Thục Đoan",     # Nữ · Nam · Phong cách kể chuyện
    "Thùy Dung":    "Thùy Dung",     # Nữ · Nam · Phong cách tin tức
    "Ngọc Trân":    "Ngọc Trân",     # Nữ · Trung · Phong cách tự nhiên
    "Mỹ Duyên":     "Mỹ Duyên",      # Nữ · Nam · Phong cách đọc truyện
    "Quỳnh Anh":    "Quỳnh Anh",     # Nữ · Bắc · Phong cách đọc truyện
    "Kim Thanh":    "Kim Thanh",     # Nữ · Nam · Phong cách đọc truyện
    "Ngọc Huyền":   "Ngọc Huyền",    # Nữ · Bắc · Giọng đọc tự nhiên
}

# Giọng mặc định khi không chỉ định
DEFAULT_VOICE = "Adam"

# Sample rate của VieNeu v3 Turbo
VIENEU_SAMPLE_RATE = 48000

# Singleton engine (lazy-load để tránh khởi động chậm khi import)
_vieneu_engine = None


def _get_engine():
    """Lazy-load VieNeu v3 Turbo engine (singleton per process)."""
    global _vieneu_engine
    if _vieneu_engine is None:
        from vieneu import Vieneu
        _vieneu_engine = Vieneu(mode="v3turbo")
    return _vieneu_engine


def resolve_voice_key(voice_name: str) -> str:
    """
    Giải quyết tên giọng đọc thành preset key của VieNeu.
    - Nếu khớp chính xác với key trong VIENEU_VOICES → trả về preset key
    - Nếu không tìm thấy → cảnh báo và dùng Adam mặc định
    """
    if voice_name in VIENEU_VOICES:
        return VIENEU_VOICES[voice_name]
    # Tìm kiếm không phân biệt hoa thường
    for k, v in VIENEU_VOICES.items():
        if k.lower() == voice_name.lower():
            return v
    # Fallback
    print(f"[TTS CẢNH BÁO] Không tìm thấy giọng '{voice_name}', dùng mặc định '{DEFAULT_VOICE}'.")
    return VIENEU_VOICES[DEFAULT_VOICE]


# ─────────────────────────────────────────────────────────────────────────────
# PRONUNCIATION DICT (Inline — dự phòng)
# ─────────────────────────────────────────────────────────────────────────────
PRONUNCIATION_DICT = {
    r"\bFlowchart\b": "phờ lâu chác",
    r"\bFlowcharts\b": "phờ lâu chác",
    r"\bPseudocode\b": "mã giả su đô cốt",
    r"\bSyntax\b": "xin tắc",
    r"\bBug\b": "bấc",
    r"\bBugs\b": "bấc",
    r"\bDebug\b": "đi bấc",
    r"\bDebugging\b": "đi bấc ghinh",
    r"\bFile log\b": "phai lốc",
    r"\bLog\b": "lốc",
    r"\bLogs\b": "lốc",
    r"\bBrute-force\b": "bơ rút-phoóc",
    r"\bCase study\b": "kết xì ta-đi",
    r"\bTest-case\b": "tét kây-sơ",
    r"\bIshikawa\b": "Í-si-ka-oa",
    r"\b5 Whys\b": "5 Lần Tại Sao",
    r"\bRoot Cause\b": "nguyên nhân gốc rễ",
    r"\bSymptom\b": "triệu chứng bề mặt",
    r"\bDivide & Conquer\b": "Chia để trị",
    r"\bDivide and Conquer\b": "Chia để trị",
    r"\bMemory Leak\b": "tràn bộ nhớ Me mo ry lích",
    r"\bIndex SQL\b": "chỉ mục ét quy eo",
    r"\bSQL\b": "ét quy eo",
    r"\bCPU\b": "xê-pê-u",
    r"\bRAM\b": "ram",
    r"\bFlash Sale\b": "Phơ lát xeo",
    r"\bFull Table Scan\b": "Phun thây bồ xờ ken",
    r"\bCode dump\b": "cốt đăm",
    r"\bApp\b": "áp",
    r"\bAI\b": "ây-ai",
    r"\bAction Challenge\b": "Thách thức hành động",
    r"\bChecklist\b": "chếch-lít",
}

from core.pronunciation_dict import normalize_pronunciation, MASTER_PRONUNCIATION_LIST


def clean_and_phoneticize_text(text: str) -> str:
    """Chuẩn hóa văn bản đọc: loại bỏ dấu markdown, chuẩn hóa phát âm toàn diện theo từ điển."""
    if not text:
        return ""
    # Loại bỏ ký tự markdown thô
    t = re.sub(r"[\*\_#`]", "", text)
    # Áp dụng từ điển phát âm & chuẩn hóa ngữ âm toàn diện
    t = normalize_pronunciation(t)
    return t


def format_srt_time(seconds: float) -> str:
    """Chuyển số giây float thành định dạng SRT HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int(round((seconds - int(seconds)) * 1000))
    if msecs >= 1000:
        msecs = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"


def split_text_into_chunks(text: str, chunk_size: int = 7) -> List[str]:
    """Chia văn bản thành các cụm từ súc tích 6-8 từ."""
    words = text.split()
    chunks = []
    curr = []
    for w in words:
        curr.append(w)
        if len(curr) >= chunk_size or w.endswith((".", ",", ";", ":", "!", "?", "—", "-")):
            chunks.append(" ".join(curr))
            curr = []
    if curr:
        chunks.append(" ".join(curr))
    return chunks


def _numpy_to_wav_bytes(audio_np, sample_rate: int = VIENEU_SAMPLE_RATE) -> bytes:
    """Chuyển numpy array (float32) thành WAV bytes."""
    import numpy as np
    import io
    # Chuyển float32 [-1, 1] sang int16
    audio_int16 = (audio_np * 32767).clip(-32768, 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    return buf.getvalue()


def _split_long_text(text: str, max_chars: int = 200) -> List[str]:
    """
    Chia văn bản dài thành các đoạn nhỏ hơn max_chars ký tự,
    ưu tiên cắt tại dấu câu (. , ; : ! ?) hoặc khoảng trắng.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    remaining = text.strip()

    while len(remaining) > max_chars:
        # Tìm điểm cắt tại dấu câu trong khoảng max_chars ký tự
        cut_pos = -1
        for punct in [".", "?", "!", ";", ",", ":"]:
            pos = remaining.rfind(punct, 0, max_chars)
            if pos > cut_pos:
                cut_pos = pos

        # Nếu không có dấu câu, cắt tại khoảng trắng cuối cùng
        if cut_pos <= 0:
            cut_pos = remaining.rfind(" ", 0, max_chars)

        # Nếu vẫn không có, cắt cứng tại max_chars
        if cut_pos <= 0:
            cut_pos = max_chars

        chunk = remaining[:cut_pos + 1].strip()
        if chunk:
            chunks.append(chunk)
        remaining = remaining[cut_pos + 1:].strip()

    if remaining:
        chunks.append(remaining)

    return chunks


def generate_tts_audio_and_srt(
    display_text: str,
    spoken_text: str,
    out_mp3: Path,
    out_srt: Path,
    voice: str = DEFAULT_VOICE,
    speed: float = 0.92,
) -> float:
    """
    Tạo file MP3 (thông qua WAV → FFmpeg) và file SRT phân đoạn ngắn
    bằng VieNeu-TTS v3 Turbo.

    Args:
        display_text: Văn bản gốc hiển thị trên phụ đề (giữ từ tiếng Anh chuẩn hoa mỹ)
        spoken_text:  Văn bản đã chuẩn hóa phát âm để TTS đọc
        out_mp3:      Đường dẫn file MP3 xuất ra
        out_srt:      Đường dẫn file SRT xuất ra
        voice:        Tên giọng đọc (key trong VIENEU_VOICES hoặc preset key trực tiếp)
        speed:        Tốc độ đọc (0.85-1.0, mặc định 0.92 = chậm nhẹ ~8%)

    Returns:
        Thời lượng âm thanh (giây)
    """
    import numpy as np
    import subprocess
    import shutil

    out_mp3 = Path(out_mp3)
    out_srt = Path(out_srt)
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    out_srt.parent.mkdir(parents=True, exist_ok=True)

    # Giải quyết preset key
    preset_key = resolve_voice_key(voice)

    # Chuẩn bị text để đọc
    if not spoken_text:
        spoken_text = display_text
    spoken_text = spoken_text.strip()

    # Khởi động engine
    engine = _get_engine()

    # Chia text dài thành các đoạn nhỏ (VieNeu tối ưu max ~200 ký tự/lần)
    text_chunks = _split_long_text(spoken_text, max_chars=200)

    # Synthesize từng đoạn và ghép lại
    audio_segments = []
    for chunk in text_chunks:
        if not chunk.strip():
            continue
        try:
            audio_np = engine.infer(
                text=chunk,
                voice=preset_key,
                temperature=0.75,
                top_k=20,
                top_p=0.9,
                repetition_penalty=1.15,
                apply_watermark=False,
            )
            if audio_np is not None and len(audio_np) > 0:
                audio_segments.append(audio_np)
        except Exception as e:
            print(f"[TTS LỖI] Lỗi synthesize chunk: {e}")
            continue

    if not audio_segments:
        raise RuntimeError(f"[TTS] Không tổng hợp được âm thanh cho văn bản: {spoken_text[:80]}...")

    # Ghép các đoạn audio với khoảng dừng ngắn (0.3s silence) giữa các câu
    silence_samples = int(0.3 * VIENEU_SAMPLE_RATE)
    silence = np.zeros(silence_samples, dtype=np.float32)

    combined_parts = []
    for i, seg in enumerate(audio_segments):
        combined_parts.append(seg)
        if i < len(audio_segments) - 1:
            combined_parts.append(silence)

    audio_combined = np.concatenate(combined_parts, axis=0)

    # Áp dụng speed bằng cách resample (giảm sample rate → phát chậm hơn)
    if abs(speed - 1.0) > 0.02:
        import scipy.signal
        target_samples = int(len(audio_combined) / speed)
        audio_combined = scipy.signal.resample(audio_combined, target_samples)

    # Lưu WAV tạm thời (dùng cùng thư mục với MP3 để tránh permission issues)
    wav_tmp = out_mp3.with_suffix(".tmp.wav")
    wav_bytes = _numpy_to_wav_bytes(audio_combined, VIENEU_SAMPLE_RATE)
    wav_tmp.write_bytes(wav_bytes)

    # Chuyển đổi WAV → MP3 bằng FFmpeg (nếu có), ngược lại copy WAV
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass

    if not ffmpeg_path:
        _FFMPEG_CANDIDATES = [
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
        ]
        for candidate in _FFMPEG_CANDIDATES:
            candidate_path = Path(candidate)
            if candidate_path.exists():
                ffmpeg_path = str(candidate_path)
                break

    converted_ok = False
    try:
        if ffmpeg_path:
            try:
                result = subprocess.run(
                    [
                        ffmpeg_path, "-y",
                        "-i", str(wav_tmp),
                        "-codec:a", "libmp3lame",
                        "-qscale:a", "2",
                        "-ar", "44100",
                        str(out_mp3),
                    ],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    converted_ok = True
                else:
                    print(f"[TTS WARNING] FFmpeg WAV→MP3 trả về mã {result.returncode}: {result.stderr[-200:]}")
            except Exception as run_err:
                print(f"[TTS WARNING] Không thể thực thi FFmpeg ({run_err})")

        if not converted_ok:
            # Fallback: copy WAV bytes vào file MP3
            # (PyAV và các engine video pipeline vẫn đọc được audio binary)
            import shutil as _shutil
            _shutil.copy2(str(wav_tmp), str(out_mp3))
            print(f"[TTS INFO] Đã xuất WAV trực tiếp cho {out_mp3.name}")
    finally:
        wav_tmp.unlink(missing_ok=True)

    # Đo thời lượng chính xác từ số sample
    duration = len(audio_combined) / VIENEU_SAMPLE_RATE


    # Tạo file SRT phân đoạn ngắn từ display_text gốc
    chunks = split_text_into_chunks(display_text, chunk_size=7)
    if not chunks:
        chunks = [display_text]

    total_words = sum(len(c.split()) for c in chunks)
    srt_lines = []
    curr_time = 0.0

    for i, c in enumerate(chunks, 1):
        c_words = len(c.split())
        c_dur = max(1.2, duration * (c_words / max(1, total_words)))
        t_start = curr_time
        t_end = min(duration, curr_time + c_dur)
        if i == len(chunks):
            t_end = duration

        srt_lines.append(f"{i}")
        srt_lines.append(f"{format_srt_time(t_start)} --> {format_srt_time(t_end)}")
        srt_lines.append(c)
        srt_lines.append("")
        curr_time = t_end

    out_srt.write_text("\n".join(srt_lines), encoding="utf-8")
    return duration


# ─────────────────────────────────────────────────────────────────────────────
# BACKWARD COMPATIBILITY ALIAS
# Các engine cũ gọi generate_edge_tts_audio_and_srt → redirect sang hàm mới
# ─────────────────────────────────────────────────────────────────────────────
async def generate_edge_tts_audio_and_srt(
    display_text: str,
    spoken_text: str,
    out_mp3: Path,
    out_srt: Path,
    voice: str = "vi-VN-NamMinhNeural",
    rate: str = "-8%",
) -> float:
    """
    [DEPRECATED] Alias backward-compat cho code cũ dùng Edge-TTS API.
    Tự động chuyển hướng sang VieNeu-TTS v3 Turbo.
    - voice 'vi-VN-NamMinhNeural' → Adam
    - voice 'vi-VN-HoaiMyNeural'  → Mai Anh
    - rate '-8%' → speed=0.92
    """
    # Map voice cũ → giọng VieNeu
    voice_map = {
        "vi-VN-NamMinhNeural": "Adam",
        "vi-VN-HoaiMyNeural":  "Mai Anh",
    }
    mapped_voice = voice_map.get(voice, "Adam")

    # Map rate → speed (rate -8% ≈ speed 0.92)
    speed = 0.92
    if rate:
        rate_str = rate.replace("%", "").replace("+", "").strip()
        try:
            rate_val = float(rate_str)
            # Chuyển đổi: rate -8% → speed 0.92 (1.0 + rate/100)
            speed = max(0.7, min(1.2, 1.0 + rate_val / 100))
        except ValueError:
            speed = 0.92

    return generate_tts_audio_and_srt(
        display_text=display_text,
        spoken_text=spoken_text,
        out_mp3=Path(out_mp3),
        out_srt=Path(out_srt),
        voice=mapped_voice,
        speed=speed,
    )
