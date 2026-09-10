#!/usr/bin/env python3
"""
core/matterjs_engine.py
Thư viện lõi điều phối Mô phỏng Vật lý Cơ học & Động lực học 2D cho Hệ thống E-Learning Antigravity.
- Mô phỏng động lực học vật rắn (Rigid Body Dynamics) qua Matter.js: Trọng lực, Ném xiên, Va chạm đàn hồi, Ma sát, Con lắc & Lò xo.
- Tự động tính toán véc-tơ lực, vận tốc ban đầu và phương trình quỹ đạo cơ học chính xác.
- Render video chuyển động vật lý 1080p 30fps/60fps mượt mà qua Puppeteer headless và FFmpeg pipe.
- Đóng gói slide bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 chuẩn sư phạm.
- Lồng ghép giọng đọc VieNeu-TTS v3 Turbo Nam Minh, nhạc nền Lo-Fi và phụ đề SRT ngắn.
"""

from __future__ import annotations

import json
import math
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


class MatterJSEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        self.video_dir = Path(video_dir).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "matterjs"
        self.output_dir = self.video_dir

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.node_bin = "node"

    def build_projectile_config(
        self,
        v0: float = 22.0,
        angle_deg: float = 45.0,
        restitution: float = 0.75,
        start_x: float = 200.0,
        start_y: float = 880.0,
        color: str = "#38BDF8",
    ) -> dict:
        """
        Tính toán thông số vật lý của chuyển động ném xiên và sinh config Matter.js.
        g = 9.8 m/s^2 (tương ứng scale trọng lực của canvas)
        """
        rad = math.radians(angle_deg)
        # Trong hệ tọa độ Canvas 1920x1080, trục Y hướng xuống nên vận tốc ban đầu Vy hướng lên mang dấu âm
        scale_factor = 1.0
        vx = v0 * math.cos(rad) * scale_factor
        vy = -v0 * math.sin(rad) * scale_factor

        g = 9.8
        h_max = (v0**2 * (math.sin(rad)**2)) / (2 * g)
        l_max = (v0**2 * math.sin(2 * rad)) / g
        t_flight = (2 * v0 * math.sin(rad)) / g

        return {
            "title": "MÔ PHỎNG CHUYỂN ĐỘNG NÉM XIÊN TRONG TRỌNG TRƯỜNG",
            "subtitle": f"Góc ném α = {angle_deg:.1f}° • Vận tốc đầu v₀ = {v0:.1f} m/s • Khảo sát quỹ đạo Parabol",
            "telemetry": {
                "v0": f"{v0:.1f} m/s",
                "angle": f"{angle_deg:.1f}°",
                "h_max": f"{h_max:.2f} m",
                "l_max": f"{l_max:.2f} m",
                "t_flight": f"{t_flight:.2f} s",
                "restitution": f"{restitution:.2f}",
                "formula": "y = x·tan(α) - (g·x²)/(2·v₀²·cos²(α))<br/>Hmax = (v₀²·sin²(α))/(2·g) | Lmax = (v₀²·sin(2α))/g",
            },
            "gravity": 1.0,
            "floorY": 940,
            "bodies": [
                {
                    "type": "circle",
                    "x": start_x,
                    "y": start_y,
                    "radius": 24,
                    "color": color,
                    "strokeColor": "#FFFFFF",
                    "lineWidth": 2.5,
                    "restitution": restitution,
                    "friction": 0.05,
                    "frictionAir": 0.001,
                    "initialVelocity": {"x": round(vx, 2), "y": round(vy, 2)},
                }
            ],
        }

    def build_collision_config(
        self,
        v1: float = 12.0,
        v2: float = -8.0,
        m1: float = 1.0,
        m2: float = 2.0,
        restitution: float = 0.9,
    ) -> dict:
        """Cấu hình va chạm đàn hồi 2 vật thể."""
        return {
            "title": "MÔ PHỎNG VA CHẠM ĐÀN HỒI TRONG KHÔNG GIAN 2D",
            "subtitle": f"Vật 1 (v₁ = {v1} m/s, m₁ = {m1} kg) chạm Vật 2 (v₂ = {v2} m/s, m₂ = {m2} kg) • e = {restitution}",
            "telemetry": {
                "v0": f"v₁ = {v1} m/s, v₂ = {v2} m/s",
                "angle": "Đồng trục 0°",
                "h_max": "N/A",
                "l_max": f"m₁={m1}kg, m₂={m2}kg",
                "t_flight": "N/A",
                "restitution": f"{restitution:.2f}",
                "formula": "m₁v₁ + m₂v₂ = m₁v'₁ + m₂v'₂<br/>Định luật bảo toàn động lượng & động năng",
            },
            "gravity": 0.0,  # Không gian không trọng lực cho va chạm thuần túy
            "floorY": 940,
            "bodies": [
                {
                    "type": "circle",
                    "x": 400,
                    "y": 600,
                    "radius": 35,
                    "color": "#38BDF8",
                    "restitution": restitution,
                    "initialVelocity": {"x": v1, "y": 0},
                },
                {
                    "type": "circle",
                    "x": 1400,
                    "y": 600,
                    "radius": 50,
                    "color": "#F59E0B",
                    "restitution": restitution,
                    "initialVelocity": {"x": v2, "y": 0},
                },
            ],
        }

    def create_simulation_config(self, config_data: dict, output_json_path: Path) -> Path:
        """Lưu file JSON khai báo môi trường và các vật thể vật lý."""
        output_json_path = Path(output_json_path).resolve()
        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        print(f"📄 [Matter.js] Đã lưu file cấu hình mô phỏng: {output_json_path.name}")
        return output_json_path

    def generate_html_page(
        self,
        physics_config: dict,
        output_html_path: Path,
        template_path: Optional[Path] = None,
    ) -> Path:
        """Điền cấu hình vật lý vào HTML template Matter.js."""
        if not template_path:
            template_path = WORKSPACE_ROOT / "assets" / "templates" / "matterjs_physics.html"

        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        lib_rel = os.path.relpath(WORKSPACE_ROOT / "assets" / "libs" / "matter.min.js", output_html_path.parent).replace("\\", "/")
        html = html.replace("__LIB_MATTER_PATH__", lib_rel)

        # Inject JSON config
        config_json = json.dumps(physics_config, ensure_ascii=False)
        html = html.replace("__PHYSICS_CONFIG_PLACEHOLDER__", config_json)

        # Cập nhật tiêu đề và thẻ thông số nếu có
        if "title" in physics_config:
            html = html.replace('id="slide-title">MÔ PHỎNG CHUYỂN ĐỘNG NÉM XIÊN TRONG TRỌNG TRƯỜNG', f'id="slide-title">{physics_config["title"]}')
        if "subtitle" in physics_config:
            html = html.replace('id="slide-subtitle">Khảo sát quỹ đạo Parabol • Định luật bảo toàn cơ năng • Va chạm đàn hồi với mặt sàn', f'id="slide-subtitle">{physics_config["subtitle"]}')

        telem = physics_config.get("telemetry", {})
        if telem:
            if "v0" in telem:
                html = html.replace('id="prop-v0">20.0 m/s', f'id="prop-v0">{telem["v0"]}')
            if "angle" in telem:
                html = html.replace('id="prop-angle">45.0°', f'id="prop-angle">{telem["angle"]}')
            if "h_max" in telem:
                html = html.replace('id="prop-hmax">10.20 m', f'id="prop-hmax">{telem["h_max"]}')
            if "l_max" in telem:
                html = html.replace('id="prop-lmax">40.82 m', f'id="prop-lmax">{telem["l_max"]}')
            if "restitution" in telem:
                html = html.replace('id="prop-restitution">0.75', f'id="prop-restitution">{telem["restitution"]}')
            if "formula" in telem:
                html = html.replace('y = x·tan(α) - (g·x²) / (2·v₀²·cos²(α))<br/>\n      Hmax = (v₀²·sin²(α)) / (2·g)', telem["formula"])

        output_html_path = Path(output_html_path).resolve()
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"🌐 [Matter.js View] Đã xuất bản trang mô phỏng: {output_html_path.name}")
        return output_html_path

    def render_still(self, html_path: Path, output_image_path: Path, step_count: int = 50) -> Path:
        """Chụp snapshot trạng thái quỹ đạo vật lý ở thời điểm đẹp nhất bằng Puppeteer."""
        html_path = Path(html_path).resolve()
        output_image_path = Path(output_image_path).resolve()
        output_image_path.parent.mkdir(parents=True, exist_ok=True)

        html_url = str(html_path.resolve()).replace("\\", "/")
        img_out = str(output_image_path.resolve()).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        puppeteer_script = f"""
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

  await page.evaluate((steps) => {{
    window.manualStepMode = true;
    for (let i = 0; i < steps; i++) {{
      if (window.renderPhysicsStep) window.renderPhysicsStep(16.67);
    }}
  }}, {step_count});

  await page.screenshot({{ path: '{img_out}', type: 'png' }});
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_physics_snap.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(puppeteer_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_image_path.exists():
            raise RuntimeError(f"Lỗi khi chụp still frame Matter.js từ {html_path.name}")

        print(f"📸 [Matter.js Still] Đã chụp ảnh slide 16:9: {output_image_path.name}")
        return output_image_path

    def render_video(
        self,
        html_path: Path,
        output_mp4_path: Path,
        duration_sec: float = 6.0,
        fps: int = 30,
    ) -> Path:
        """
        Ghi hình chuyển động vật lý 2D mượt mà bằng Puppeteer và FFmpeg streaming.
        """
        html_path = Path(html_path).resolve()
        output_mp4_path = Path(output_mp4_path).resolve()
        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

        total_frames = int(round(duration_sec * fps))
        print(f"🎬 [Matter.js Video] Đang ghi hình mô phỏng vật lý ({duration_sec}s, {total_frames} frames @ {fps}fps)...")

        html_url = str(html_path).replace("\\", "/")
        vid_out = str(output_mp4_path).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        recorder_script = f"""
const puppeteer = require('{puppeteer_mod}');
const {{ spawn }} = require('child_process');

(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 400));

  await page.evaluate(() => {{
    window.manualStepMode = true;
  }});

  // Khởi chạy FFmpeg nhận stdin image2pipe
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', '{fps}',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-r', '{fps}',
    '{vid_out}'
  ], {{ stdio: ['pipe', 'inherit', 'inherit'] }});

  const totalFrames = {total_frames};
  const dtMs = 1000.0 / {fps};

  for (let f = 0; f < totalFrames; f++) {{
    await page.evaluate((dt) => {{
      if (window.renderPhysicsStep) window.renderPhysicsStep(dt);
    }}, dtMs);

    const buf = await page.screenshot({{ type: 'png' }});
    const canWrite = ffmpeg.stdin.write(buf);
    if (!canWrite) {{
      await new Promise(r => ffmpeg.stdin.once('drain', r));
    }}
  }}

  ffmpeg.stdin.end();
  await new Promise(resolve => ffmpeg.on('close', resolve));
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_physics_record.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(recorder_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_mp4_path.exists():
            raise RuntimeError(f"Lỗi khi render video Matter.js từ {html_path.name}")

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
        """Ghép nối Video Matter.js + Giọng đọc VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT."""
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [Matter.js Audio/SRT Integration] Đang đóng gói hoàn thiện video bài giảng Vật lý...")

        cmd = ["ffmpeg", "-y", "-i", str(raw_video)]

        has_narration = audio_path and Path(audio_path).exists()
        has_bgm = bgm_path and Path(bgm_path).exists()
        has_srt = srt_path and Path(srt_path).exists()

        if has_narration:
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

        if has_narration and has_bgm:
            cmd.extend([
                "-filter_complex",
                f"[1:a]volume=1.0[vocal];[2:a]volume={bgm_volume}[bgm];[vocal][bgm]amix=inputs=2:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]",
            ])
        elif has_narration:
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        elif has_bgm:
            cmd.extend(["-map", "0:v", "-map", "1:a"])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video),
        ])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("FFmpeg stderr:", proc.stderr)
            raise RuntimeError(f"FFmpeg thất bại khi ghép audio/subtitles cho {output_video.name}")

        print(f"🎉 [XUẤT SẮC] Video Matter.js hoàn thiện: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scenes_meta: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_matterjs",
    ) -> dict[str, Path]:
        """Đóng gói slide mô phỏng vật lý sang PowerPoint (.pptx) và PDF (.pdf)."""
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        temp_slides_dir = self.runtime_dir / "temp_matterjs_slides"
        temp_slides_dir.mkdir(parents=True, exist_ok=True)

        captured_slides = []
        for i, sc in enumerate(scenes_meta, 1):
            html_p = sc.get("html_path")
            steps = sc.get("steps", 50)
            out_img = temp_slides_dir / f"slide_physics_{i}.png"
            img_p = self.render_still(Path(html_p), out_img, step_count=steps)
            captured_slides.append(img_p)

        results = package_slides(captured_slides, output_dir, base_name, format_type)
        return results
