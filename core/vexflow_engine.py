#!/usr/bin/env python3
"""
core/vexflow_engine.py
Thư viện lõi điều phối VexFlow (Music Notation) & Tone.js Web Audio Engine cho Antigravity.
- Chuyên dụng cho các bài giảng Âm nhạc, Ký âm, Lý thuyết bản nhạc, Khóa Sol/Pha, Xướng âm & Piano.
- Sinh cấu hình JSON bản nhạc và trang HTML mô phỏng tương tác 16:9.
- Mô phỏng thanh cuộn Playhead chuyển động mượt mà và bàn phím Piano sáng đèn tương ứng cao độ nốt.
- Tự động tổng hợp âm thanh nhạc cụ Piano Synth chất lượng cao qua bộ dao động sóng âm PCM.
- Ghi hình video Full HD 1080p30 qua Puppeteer frame-pipe đến FFmpeg.
- Đóng gói Slide bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 qua core.pptx_engine.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path
from typing import Optional, Union

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))


class VexFlowEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        self.video_dir = Path(video_dir).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "vexflow"
        self.output_dir = self.video_dir

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.node_bin = shutil.which("node") or "node"

    # Tần số chuẩn các nốt nhạc (Hz)
    PITCH_FREQUENCIES = {
        "C4": 261.63, "C#4": 277.18, "Db4": 277.18,
        "D4": 293.66, "D#4": 311.13, "Eb4": 311.13,
        "E4": 329.63,
        "F4": 349.23, "F#4": 369.99, "Gb4": 369.99,
        "G4": 392.00, "G#4": 415.30, "Ab4": 415.30,
        "A4": 440.00, "A#4": 466.16, "Bb4": 466.16,
        "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25
    }

    def create_score_config(self, notes_data: dict, output_json_path: Path) -> Path:
        """Lưu file cấu hình nốt nhạc và nhịp điệu (BPM)."""
        output_json_path = Path(output_json_path).resolve()
        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(notes_data, f, ensure_ascii=False, indent=2)
        print(f"📄 [VexFlow] Đã lưu file cấu hình bản nhạc: {output_json_path.name}")
        return output_json_path

    def build_melody_config(
        self,
        notes_str: str = "C4/q, D4/q, E4/q, F4/q, G4/h, C5/h",
        clef: str = "treble",
        time_signature: str = "4/4",
        tempo: int = 100,
        title: str = "BÀI HỌC: GAM TRƯỞNG & GIAI ĐIỆU CĂN BẢN",
        subtitle: str = "Khóa Sol • Nhịp 4/4 • Tempo 100 BPM • Ký âm VexFlow & Diễn hoạt Piano Synth",
        key: str = "Đô Trưởng (C Major)",
    ) -> dict:
        """Tạo cấu trúc config tiêu chuẩn cho bài giảng âm nhạc."""
        # Trích xuất danh sách pitch (C4, D4, ...) từ chuỗi nốt
        note_tokens = [tok.strip() for tok in notes_str.split(",") if tok.strip()]
        pitches = []
        durations = []
        for tok in note_tokens:
            parts = tok.split("/")
            p = parts[0].strip().upper()
            d = parts[1].strip() if len(parts) > 1 else "q"
            pitches.append(p)
            durations.append(d)

        return {
            "title": title,
            "subtitle": subtitle,
            "clef": clef,
            "time_signature": time_signature,
            "tempo": tempo,
            "key": key,
            "notes_str": notes_str,
            "note_list": pitches,
            "durations": durations,
        }

    def generate_html_page(
        self,
        music_config: dict,
        output_html_path: Path,
        template_path: Optional[Path] = None,
    ) -> Path:
        """Điền cấu hình âm nhạc vào HTML template VexFlow."""
        if not template_path:
            template_path = WORKSPACE_ROOT / "assets" / "templates" / "vexflow_music.html"

        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        vex_rel = os.path.relpath(WORKSPACE_ROOT / "assets" / "libs" / "vexflow.min.js", output_html_path.parent).replace("\\", "/")
        tone_rel = os.path.relpath(WORKSPACE_ROOT / "assets" / "libs" / "tone.min.js", output_html_path.parent).replace("\\", "/")

        html = html.replace("__LIB_VEXFLOW_PATH__", vex_rel)
        html = html.replace("__LIB_TONE_PATH__", tone_rel)

        config_json = json.dumps(music_config, ensure_ascii=False)
        html = html.replace("__MUSIC_DATA_PLACEHOLDER__", config_json)

        output_html_path = Path(output_html_path).resolve()
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"🌐 [VexFlow View] Đã xuất bản trang mô phỏng âm nhạc: {output_html_path.name}")
        return output_html_path

    def generate_piano_synth_audio(
        self,
        music_config: dict,
        output_wav_path: Path,
        sample_rate: int = 44100,
    ) -> Path:
        """
        Tổng hợp âm thanh Piano Synth studio-grade (WAV 16-bit PCM) theo chuỗi nốt nhạc.
        Sử dụng tổng hợp âm sắc giàu họa âm (Harmonic additive synthesis) và đường bao ADSR.
        """
        output_wav_path = Path(output_wav_path).resolve()
        output_wav_path.parent.mkdir(parents=True, exist_ok=True)

        tempo = music_config.get("tempo", 100)
        beat_duration = 60.0 / tempo  # Thời lượng 1 phách (nốt đen q)
        durations_map = {
            "w": beat_duration * 4,  # Tròn
            "h": beat_duration * 2,  # Trắng
            "q": beat_duration * 1,  # Đen
            "8": beat_duration * 0.5, # Móc đơn
            "16": beat_duration * 0.25 # Móc kép
        }

        note_list = music_config.get("note_list", ["C4", "D4", "E4", "F4", "G4", "C5"])
        duration_tokens = music_config.get("durations", ["q"] * len(note_list))

        audio_samples = []

        for pitch, dur_code in zip(note_list, duration_tokens):
            freq = self.PITCH_FREQUENCIES.get(pitch, 261.63)
            dur_sec = durations_map.get(dur_code, beat_duration)
            total_samples = int(sample_rate * dur_sec)

            for i in range(total_samples):
                t = i / sample_rate
                # Họa âm phong phú như tiếng đàn Piano
                tone = (
                    0.60 * math.sin(2 * math.pi * freq * t) +
                    0.25 * math.sin(2 * math.pi * 2 * freq * t) +
                    0.10 * math.sin(2 * math.pi * 3 * freq * t) +
                    0.05 * math.sin(2 * math.pi * 4 * freq * t)
                )

                # Đường bao âm lượng ADSR (Attack - Decay - Sustain - Release)
                decay_envelope = math.exp(-3.5 * (t / dur_sec))
                sample_val = int(tone * decay_envelope * 24000)
                # Giới hạn 16-bit
                sample_val = max(-32767, min(32767, sample_val))
                audio_samples.append(sample_val)

        # Ghi file WAV PCM
        with wave.open(str(output_wav_path), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            raw_data = struct.pack(f"<{len(audio_samples)}h", *audio_samples)
            wav_file.writeframes(raw_data)

        print(f"🎵 [Piano Synth] Đã tổng hợp file âm thanh nhạc cụ: {output_wav_path.name}")
        return output_wav_path

    def render_still(self, html_path: Path, output_image_path: Path, progress_ratio: float = 0.5) -> Path:
        """Chụp snapshot trạng thái bản nhạc và phím Piano đang sáng ở khung hình giữa bằng Puppeteer."""
        html_path = Path(html_path).resolve()
        output_image_path = Path(output_image_path).resolve()
        output_image_path.parent.mkdir(parents=True, exist_ok=True)

        html_url = str(html_path).replace("\\", "/")
        img_out = str(output_image_path).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        script_code = f"""
const puppeteer = require('{puppeteer_mod}');
(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 400));

  await page.evaluate((ratio) => {{
    window.renderMusicStep(ratio * 5000, 5000);
  }}, {progress_ratio});

  await page.screenshot({{ path: '{img_out}', type: 'png' }});
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_music_snap.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_code)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_image_path.exists():
            raise RuntimeError(f"Lỗi khi chụp still frame VexFlow từ {html_path.name}")

        print(f"📸 [VexFlow Still] Đã chụp ảnh slide 16:9: {output_image_path.name}")
        return output_image_path

    def render_video(
        self,
        html_path: Path,
        output_mp4_path: Path,
        duration_sec: float = 6.0,
        fps: int = 30,
    ) -> Path:
        """
        Ghi hình chuyển động Playhead cuộn qua bản nhạc và phím Piano sáng nhấp nháy
        chuẩn xác từng frame qua Puppeteer và pipe FFmpeg.
        """
        html_path = Path(html_path).resolve()
        output_mp4_path = Path(output_mp4_path).resolve()
        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

        total_frames = int(round(duration_sec * fps))
        print(f"🎬 [VexFlow Video] Đang ghi hình bản nhạc ({duration_sec}s, {total_frames} frames @ {fps}fps)...")

        html_url = str(html_path).replace("\\", "/")
        vid_out = str(output_mp4_path).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        recorder_script = f"""
const puppeteer = require('{puppeteer_mod}');
const {{ spawn }} = require('child_process');

(async () => {{
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', '{fps}',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '22',
    '{vid_out}'
  ]);

  ffmpeg.stderr.on('data', (d) => {{}});

  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});

  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 400));

  const totalFrames = {total_frames};
  const durationMs = {duration_sec * 1000};
  const dtMs = 1000 / {fps};

  for (let frame = 0; frame < totalFrames; frame++) {{
    const currentMs = frame * dtMs;
    await page.evaluate((curMs, durMs) => {{
      window.renderMusicStep(curMs, durMs);
    }}, currentMs, durationMs);

    const buffer = await page.screenshot({{ type: 'png' }});
    ffmpeg.stdin.write(buffer);
  }}

  ffmpeg.stdin.end();
  await new Promise((resolve) => ffmpeg.on('close', resolve));
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_music_record.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(recorder_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_mp4_path.exists():
            raise RuntimeError(f"Lỗi khi render video VexFlow từ {html_path.name}")

        print(f"   [OK] Đã xuất video raw: {output_mp4_path.name}")
        return output_mp4_path

    def merge_audio_and_subtitles(
        self,
        raw_video: Path,
        audio_path: Optional[Path],
        srt_path: Optional[Path],
        output_video: Path,
        synth_audio_path: Optional[Path] = None,
        bgm_path: Optional[Path] = None,
        synth_volume: float = 0.65,
        bgm_volume: float = 0.10,
    ) -> Path:
        """
        Dùng FFmpeg hòa trộn Video + Giọng đọc VieNeu-TTS v3 Turbo + Âm thanh Piano Synth + Nhạc nền Lo-Fi + Phụ đề SRT.
        """
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [VexFlow Multi-track Integration] Đang đóng gói video hoàn thiện...")

        cmd = ["ffmpeg", "-y", "-i", str(raw_video)]

        inputs = []
        has_vocal = audio_path and Path(audio_path).exists()
        has_synth = synth_audio_path and Path(synth_audio_path).exists()
        has_bgm = bgm_path and Path(bgm_path).exists()
        has_srt = srt_path and Path(srt_path).exists()

        if has_vocal:
            cmd.extend(["-i", str(Path(audio_path).resolve())])
            inputs.append("vocal")
        if has_synth:
            cmd.extend(["-i", str(Path(synth_audio_path).resolve())])
            inputs.append("synth")
        if has_bgm:
            cmd.extend(["-stream_loop", "-1", "-i", str(Path(bgm_path).resolve())])
            inputs.append("bgm")

        filters = []
        if has_srt:
            escaped_srt = str(Path(srt_path).resolve()).replace("\\", "/").replace(":", "\\:")
            sub_filter = (
                f"subtitles='{escaped_srt}':force_style="
                "'Fontname=Be Vietnam Pro,FontSize=24,Bold=1,PrimaryColour=&H00FFFFFF,"
                "BackColour=&H900F172A,BorderStyle=4,Shadow=0,MarginV=35'"
            )
            filters.append(sub_filter)

        if filters:
            cmd.extend(["-vf", ",".join(filters)])

        # Audio mixing logic
        if len(inputs) == 3:  # vocal + synth + bgm
            cmd.extend([
                "-filter_complex",
                f"[1:a]volume=1.0[vocal];[2:a]volume={synth_volume}[synth];[3:a]volume={bgm_volume}[bgm];[vocal][synth][bgm]amix=inputs=3:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]"
            ])
        elif len(inputs) == 2:
            cmd.extend([
                "-filter_complex",
                f"[1:a]volume=1.0[a1];[2:a]volume=0.5[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]"
            ])
        elif len(inputs) == 1:
            cmd.extend(["-map", "0:v", "-map", "1:a"])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video)
        ])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("FFmpeg error:", proc.stderr)
            raise RuntimeError(f"FFmpeg thất bại khi đóng gói video VexFlow {output_video.name}")

        print(f"🎉 [XUẤT SẮC] Video VexFlow hoàn thiện: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scores_data: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_vexflow",
    ) -> dict[str, Path]:
        """
        Đóng gói slide PowerPoint (.pptx) và tài liệu PDF 16:9 từ các bản nhạc VexFlow.
        """
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        captured_slides = []
        for i, sc in enumerate(scores_data, 1):
            html_path = sc.get("html_path")
            out_img = self.runtime_dir / "temp_slide_frames" / f"vexflow_slide_{i}.png"
            ratio = sc.get("ratio", 0.5)
            img_path = self.render_still(Path(html_path), out_img, progress_ratio=ratio)
            captured_slides.append(img_path)

        results = package_slides(captured_slides, output_dir, base_name, format_type)
        return results
