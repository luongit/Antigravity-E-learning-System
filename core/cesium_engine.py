#!/usr/bin/env python3
"""
core/cesium_engine.py
Thư viện lõi điều phối CesiumJS & 3D Digital Globe Engine cho Hệ thống E-Learning Antigravity.
- Chuyên dụng cho các bài giảng Địa lý tự nhiên, Quả địa cầu 3D, Bản đồ số, Địa hình & Dữ liệu GeoJSON.
- Sinh cấu hình JSON tọa độ địa lý (Waypoints, Latitude, Longitude, Altitude, Heading, Pitch).
- Dựng cảnh WebGL 3D Digital Globe với khí quyển phát sáng, lưới kinh vĩ tuyến, địa danh và quỹ đạo Fly-to.
- Ghi hình video Full HD 1080p30 mượt mà qua Puppeteer frame-pipe đến FFmpeg.
- Đóng gói Slide PowerPoint (.pptx) và tài liệu PDF 16:9 qua core.pptx_engine.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))


class CesiumEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        self.video_dir = Path(video_dir).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "cesium"
        self.output_dir = self.video_dir

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.node_bin = shutil.which("node") or "node"

    def create_geo_config(self, camera_waypoints: list, output_json_path: Path, meta_extra: Optional[dict] = None) -> Path:
        """Lưu danh sách tọa độ các điểm dừng camera (Waypoints) và thông số bài giảng."""
        output_json_path = Path(output_json_path).resolve()
        output_json_path.parent.mkdir(parents=True, exist_ok=True)

        data = {"waypoints": camera_waypoints}
        if meta_extra:
            data.update(meta_extra)

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"📄 [Cesium] Đã lưu file cấu hình địa lý: {output_json_path.name}")
        return output_json_path

    def build_landmark_config(
        self,
        landmark_name: str = "Đỉnh Everest — Dãy Himalaya",
        latitude: float = 27.9881,
        longitude: float = 86.9250,
        altitude: float = 20000,
        heading: float = 45.0,
        pitch: float = -30.0,
        title: str = "CẤU TẠO ĐỊA HÌNH DÃY NÚI HIMALAYA & ĐỈNH EVEREST",
        subtitle: str = "Mô phỏng Quả địa cầu 3D • Tọa độ 27.9881°B, 86.9250°Đ • Quỹ đạo Camera Fly-to",
        elevation_m: float = 8848.86,
    ) -> dict:
        """Tạo cấu trúc config tiêu chuẩn cho bài giảng địa lý."""
        return {
            "title": title,
            "subtitle": subtitle,
            "landmark": landmark_name,
            "elevation_m": elevation_m,
            "waypoints": [
                {
                    "name": landmark_name,
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude": altitude,
                    "heading": heading,
                    "pitch": pitch,
                }
            ],
        }

    def generate_html_page(
        self,
        geo_config: dict,
        output_html_path: Path,
        template_path: Optional[Path] = None,
    ) -> Path:
        """Điền cấu hình địa lý vào HTML template Cesium/Globe."""
        if not template_path:
            template_path = WORKSPACE_ROOT / "assets" / "templates" / "cesium_globe.html"

        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        three_rel = os.path.relpath(WORKSPACE_ROOT / "assets" / "libs" / "three.min.js", output_html_path.parent).replace("\\", "/")
        html = html.replace("__LIB_THREE_PATH__", three_rel)

        config_json = json.dumps(geo_config, ensure_ascii=False)
        html = html.replace("__GEO_CONFIG_PLACEHOLDER__", config_json)

        output_html_path = Path(output_html_path).resolve()
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"🌐 [Cesium View] Đã xuất bản trang mô phỏng quả địa cầu 3D: {output_html_path.name}")
        return output_html_path

    def render_still(self, html_path: Path, output_image_path: Path, progress_ratio: float = 0.5) -> Path:
        """Chụp snapshot trạng thái quả địa cầu 3D bằng Puppeteer."""
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
    if (window.renderGlobeStep) window.renderGlobeStep(ratio * 5000, 5000);
  }}, {progress_ratio});

  await page.screenshot({{ path: '{img_out}', type: 'png' }});
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_globe_snap.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_code)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_image_path.exists():
            raise RuntimeError(f"Lỗi khi chụp still frame Cesium từ {html_path.name}")

        print(f"📸 [Cesium Still] Đã chụp ảnh slide 16:9: {output_image_path.name}")
        return output_image_path

    def render_video(
        self,
        html_path: Path,
        output_mp4_path: Path,
        duration_sec: float = 6.0,
        fps: int = 30,
    ) -> Path:
        """
        Ghi hình chuyển động quả địa cầu 3D và quỹ đạo camera Fly-to qua Puppeteer và pipe FFmpeg.
        """
        html_path = Path(html_path).resolve()
        output_mp4_path = Path(output_mp4_path).resolve()
        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

        total_frames = int(round(duration_sec * fps))
        print(f"🎬 [Cesium Video] Đang ghi hình Quả địa cầu 3D ({duration_sec}s, {total_frames} frames @ {fps}fps)...")

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
      if (window.renderGlobeStep) window.renderGlobeStep(curMs, durMs);
    }}, currentMs, durationMs);

    const buffer = await page.screenshot({{ type: 'png' }});
    ffmpeg.stdin.write(buffer);
  }}

  ffmpeg.stdin.end();
  await new Promise((resolve) => ffmpeg.on('close', resolve));
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_globe_record.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(recorder_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_mp4_path.exists():
            raise RuntimeError(f"Lỗi khi render video Cesium từ {html_path.name}")

        print(f"   [OK] Đã xuất video raw: {output_mp4_path.name}")
        return output_mp4_path

    def merge_audio_and_subtitles(
        self,
        raw_video: Path,
        audio_path: Optional[Path],
        srt_path: Optional[Path],
        output_video: Path,
        bgm_path: Optional[Path] = None,
        bgm_volume: float = 0.12,
    ) -> Path:
        """
        Dùng FFmpeg ghép nối Video Quả địa cầu 3D + Giọng đọc VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT.
        """
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [Cesium Audio/SRT Integration] Đang đóng gói hoàn thiện video bài giảng Địa lý...")

        cmd = ["ffmpeg", "-y", "-i", str(raw_video)]

        has_vocal = audio_path and Path(audio_path).exists()
        has_bgm = bgm_path and Path(bgm_path).exists()
        has_srt = srt_path and Path(srt_path).exists()

        if has_vocal:
            cmd.extend(["-i", str(Path(audio_path).resolve())])
        if has_bgm:
            cmd.extend(["-stream_loop", "-1", "-i", str(Path(bgm_path).resolve())])

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

        if has_vocal and has_bgm:
            cmd.extend([
                "-filter_complex",
                f"[1:a]volume=1.0[vocal];[2:a]volume={bgm_volume}[bgm];[vocal][bgm]amix=inputs=2:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]"
            ])
        elif has_vocal:
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        elif has_bgm:
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
            raise RuntimeError(f"FFmpeg thất bại khi đóng gói video Cesium {output_video.name}")

        print(f"🎉 [XUẤT SẮC] Video Cesium hoàn thiện: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scenes_data: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_cesium",
    ) -> dict[str, Path]:
        """
        Đóng gói slide PowerPoint (.pptx) và tài liệu PDF 16:9 từ các cảnh Quả địa cầu 3D.
        """
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        captured_slides = []
        for i, sc in enumerate(scenes_data, 1):
            html_path = sc.get("html_path")
            out_img = self.runtime_dir / "temp_slide_frames" / f"cesium_slide_{i}.png"
            ratio = sc.get("ratio", 0.5)
            img_path = self.render_still(Path(html_path), out_img, progress_ratio=ratio)
            captured_slides.append(img_path)

        results = package_slides(captured_slides, output_dir, base_name, format_type)
        return results
