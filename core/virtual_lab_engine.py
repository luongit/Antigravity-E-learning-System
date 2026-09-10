#!/usr/bin/env python3
"""
core/virtual_lab_engine.py
Thư viện lõi điều phối Phòng Thí Nghiệm Ảo E-Learning (Virtual Lab Engine):
- Hoàn toàn độc lập, sạch bản quyền (100% MIT & Apache-2.0).
- Không sử dụng bất kỳ mã nguồn, asset hay branding của PhET.
- Điều phối đa thư viện chuyên ngành theo ngôn ngữ tự nhiên:
  1. QUANG HỌC (Optics): Ray Optics Simulation (Apache-2.0, Snell, khúc xạ, phản xạ, thấu kính)
  2. CƠ HỌC (Mechanics): Matter.js (MIT, rơi tự do, ném xiên, va chạm, lò xo, con lắc)
  3. MẠCH ĐIỆN (Circuit): Circuit POC (MIT, nguồn DC, định luật Ohm, nối tiếp/song song, mạch RC)
  4. SÓNG & DAO ĐỘNG (Waves): Wave on string, bước sóng, tần số, sóng dừng, giao thoa
  5. ĐIỆN TRƯỜNG (Field): Điện tích điểm, họ đường sức và lưới véc-tơ Coulomb
- Render video Full HD 1080p 30fps, chụp ảnh slide snapshot 16:9, đóng gói PowerPoint (.pptx) & PDF.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from engines.virtual_lab.runtime.lab_dispatcher import detect_lab_domain
from engines.virtual_lab.runtime.optics_lab import build_refraction_config, build_lens_config
from engines.virtual_lab.runtime.mechanics_lab import (
    build_projectile_config, build_free_fall_config, build_collision_config, build_pendulum_config
)
from engines.virtual_lab.runtime.circuit_lab import build_dc_circuit_config
from engines.virtual_lab.runtime.wave_lab import build_wave_on_string_config, build_interference_config
from engines.virtual_lab.runtime.field_lab import build_electric_field_config


class VirtualLabEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        self.video_dir = Path(video_dir).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "virtual_lab"
        self.templates_dir = WORKSPACE_ROOT / "engines" / "virtual_lab" / "templates"
        self.node_bin = "node"

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def dispatch_experiment(self, query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Phân tích câu lệnh ngôn ngữ tự nhiên và tự động sinh cấu hình thí nghiệm tương ứng.
        """
        domain = detect_lab_domain(query)
        params = params or {}
        q_lower = query.lower()

        if domain == "optics":
            if any(w in q_lower for w in ["thấu kính", "kính hội tụ", "kính phân kỳ"]):
                lens_type = "diverging" if "phân kỳ" in q_lower else "converging"
                return build_lens_config(
                    lens_type=lens_type,
                    focal_length=float(params.get("focal_length", 180.0)),
                    object_distance=float(params.get("object_distance", 300.0)),
                )
            else:
                return build_refraction_config(
                    theta1_deg=float(params.get("theta1_deg", 45.0)),
                    n1_key=params.get("n1_key", "air"),
                    n2_key=params.get("n2_key", "water"),
                )

        elif domain == "mechanics":
            if any(w in q_lower for w in ["rơi tự do", "rơi"]):
                return build_free_fall_config(
                    height_m=float(params.get("height_m", 45.0)),
                    mass_kg=float(params.get("mass_kg", 2.0)),
                )
            elif any(w in q_lower for w in ["va chạm", "đàn hồi"]):
                return build_collision_config(
                    m1=float(params.get("m1", 2.0)),
                    v1=float(params.get("v1", 12.0)),
                    m2=float(params.get("m2", 1.0)),
                    v2=float(params.get("v2", -4.0)),
                    elastic=("mềm" not in q_lower),
                )
            elif any(w in q_lower for w in ["con lắc", "pendulum"]):
                return build_pendulum_config(
                    length_m=float(params.get("length_m", 2.5)),
                    angle_deg=float(params.get("angle_deg", 30.0)),
                )
            else:
                return build_projectile_config(
                    v0=float(params.get("v0", 24.0)),
                    angle_deg=float(params.get("angle_deg", 45.0)),
                )

        elif domain == "circuit":
            c_type = "series"
            if any(w in q_lower for w in ["song song", "parallel"]):
                c_type = "parallel"
            elif any(w in q_lower for w in ["nạp", "xả", "tụ điện", "rc"]):
                c_type = "rc"
            elif any(w in q_lower for w in ["đơn", "1 điện trở"]):
                c_type = "single"

            return build_dc_circuit_config(
                circuit_type=c_type,
                voltage_u=float(params.get("voltage_u", 12.0)),
                r1=float(params.get("r1", 10.0)),
                r2=float(params.get("r2", 20.0)),
            )

        elif domain == "wave":
            if any(w in q_lower for w in ["giao thoa", "2 nguồn"]):
                return build_interference_config(
                    freq_hz=float(params.get("frequency_hz", 2.0)),
                )
            else:
                return build_wave_on_string_config(
                    amplitude_cm=float(params.get("amplitude_cm", 4.0)),
                    frequency_hz=float(params.get("frequency_hz", 1.5)),
                    end_type=params.get("end_type", "fixed"),
                )

        elif domain == "field":
            return build_electric_field_config(
                charges=params.get("charges", None),
                show_vectors=params.get("show_vectors", True),
                show_field_lines=params.get("show_field_lines", True),
            )

        # Mặc định khúc xạ
        return build_refraction_config()

    def generate_html(self, config: Dict[str, Any], output_html_path: Optional[Path] = None) -> Path:
        """
        Biên dịch cấu hình thí nghiệm thành tệp HTML tự chứa hoàn chỉnh.
        """
        domain = config.get("domain", "optics")
        template_map = {
            "optics": self.templates_dir / "optics_runner.html",
            "circuit": self.templates_dir / "circuit_runner.html",
            "wave": self.templates_dir / "wave_runner.html",
            "field": self.templates_dir / "field_runner.html",
            "mechanics": WORKSPACE_ROOT / "assets" / "templates" / "matterjs_physics.html",
        }
        tpl_path = template_map.get(domain, self.templates_dir / "optics_runner.html")
        html_src = tpl_path.read_text(encoding="utf-8")

        config_json = json.dumps(config, ensure_ascii=False, indent=2)
        if "__CONFIG_JSON_PLACEHOLDER__" in html_src:
            final_html = html_src.replace("__CONFIG_JSON_PLACEHOLDER__", config_json)
        elif "__PHYSICS_CONFIG_PLACEHOLDER__" in html_src:
            final_html = html_src.replace("__PHYSICS_CONFIG_PLACEHOLDER__", config_json)
        else:
            final_html = html_src.replace("</head>", f"<script>const LAB_CONFIG = {config_json};</script></head>")

        if not output_html_path:
            output_html_path = self.video_dir / f"view_{domain}.html"

        output_html_path.write_text(final_html, encoding="utf-8")
        print(f"🌐 [Virtual Lab] Đã xuất bản trang mô phỏng thí nghiệm: {output_html_path.name}")
        return output_html_path

    def capture_still(
        self,
        html_path: Path,
        output_image_path: Path,
        seek_ratio: float = 0.5,
    ) -> Path:
        """
        Chụp ảnh snapshot thí nghiệm 16:9 ($1920\times 1080$) qua Puppeteer.
        """
        puppeteer_pkg = WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer"
        pkg_path_js = puppeteer_pkg.resolve().as_posix()
        file_url = html_path.resolve().as_uri()
        out_img_js = Path(output_image_path).resolve().as_posix()

        script_content = f"""
import {{ createRequire }} from 'module';
const require = createRequire(import.meta.url);
const puppeteer = require('{pkg_path_js}');
(async () => {{
    const browser = await puppeteer.launch({{
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080']
    }});
    const page = await browser.newPage();
    await page.setViewport({{ width: 1920, height: 1080 }});
    await page.goto('{file_url}', {{ waitUntil: 'networkidle0', timeout: 30000 }});
    await page.evaluate((r) => {{
        if (window.renderLabStep) window.renderLabStep(r * 10000, 10000);
    }}, {seek_ratio});
    await new Promise(r => setTimeout(r, 600));
    await page.screenshot({{ path: '{out_img_js}', fullPage: false }});
    await browser.close();
}})();
"""
        task_script = self.tasks_dir / "temp_lab_snap.mjs"
        task_script.write_text(script_content, encoding="utf-8")

        res = subprocess.run([self.node_bin, str(task_script)], capture_output=True, text=True, check=False)
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi chụp snapshot Virtual Lab: {res.stderr}")

        print(f"📸 [Virtual Lab] Đã chụp ảnh slide 16:9: {output_image_path.name}")
        return output_image_path

    def render_video(
        self,
        html_path: Path,
        output_video_path: Path,
        duration_sec: float = 10.0,
        fps: int = 30,
    ) -> Path:
        """
        Ghi hình chuyển động thí nghiệm ảo qua Puppeteer frame-pipe FFmpeg.
        """
        total_frames = int(duration_sec * fps)
        puppeteer_pkg = WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer"
        pkg_path_js = puppeteer_pkg.resolve().as_posix()
        file_url = html_path.resolve().as_uri()
        out_mp4_js = Path(output_video_path).resolve().as_posix()

        print(f"🎬 [Virtual Lab Video] Đang ghi hình ({duration_sec}s, {total_frames} frames @ {fps}fps)...")

        script_content = f"""
import {{ createRequire }} from 'module';
const require = createRequire(import.meta.url);
const puppeteer = require('{pkg_path_js}');
import {{ spawn }} from 'child_process';

(async () => {{
    const browser = await puppeteer.launch({{
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080']
    }});
    const page = await browser.newPage();
    await page.setViewport({{ width: 1920, height: 1080 }});
    await page.goto('{file_url}', {{ waitUntil: 'networkidle0', timeout: 30000 }});

    const ffmpeg = spawn('ffmpeg', [
        '-y', '-f', 'image2pipe', '-vcodec', 'png', '-r', '{fps}',
        '-i', 'pipe:0',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', '-crf', '18',
        '{out_mp4_js}'
    ]);

    const totalFrames = {total_frames};
    const durMs = {duration_sec} * 1000;
    const dt = durMs / totalFrames;

    for (let f = 0; f < totalFrames; f++) {{
        const curMs = f * dt;
        await page.evaluate((t, total) => {{
            if (window.renderLabStep) window.renderLabStep(t, total);
        }}, curMs, durMs);
        const buf = await page.screenshot({{ type: 'png' }});
        ffmpeg.stdin.write(buf);
    }}

    ffmpeg.stdin.end();
    await new Promise((resolve, reject) => {{
        ffmpeg.on('close', resolve);
        ffmpeg.on('error', reject);
    }});
    await browser.close();
}})();
"""
        task_script = self.tasks_dir / "temp_lab_render.mjs"
        task_script.write_text(script_content, encoding="utf-8")

        res = subprocess.run([self.node_bin, str(task_script)], capture_output=True, text=True, check=False)
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi render video Virtual Lab: {res.stderr}")

        print(f"✅ [Virtual Lab] Video hoàn thiện thành công: {output_video_path.name}")
        return output_video_path

    def create_sim_config(
        self,
        user_prompt: str = "khúc xạ ánh sáng",
        domain: Optional[str] = None,
        output_json_path: Optional[Path] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Tạo cấu hình thí nghiệm từ prompt và tham số tùy chọn."""
        query = f"{domain} {user_prompt}" if domain else user_prompt
        cfg = self.dispatch_experiment(query, params=params)
        if output_json_path:
            output_json_path = Path(output_json_path).resolve()
            output_json_path.parent.mkdir(parents=True, exist_ok=True)
            output_json_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        return cfg

    def render_still(self, html_path: Path, output_image_path: Path, progress_ratio: float = 0.5) -> Path:
        """Alias tương thích cho capture_still."""
        return self.capture_still(html_path, output_image_path, seek_ratio=progress_ratio)

    def generate_html_page(self, config: Dict[str, Any], output_html_path: Optional[Path] = None) -> Path:
        """Alias tương thích cho generate_html."""
        return self.generate_html(config, output_html_path)

    def merge_audio_and_subtitles(
        self,
        raw_video: Path,
        audio_path: Optional[Path],
        srt_path: Optional[Path],
        output_video: Path,
        bgm_path: Optional[Path] = None,
        bgm_volume: float = 0.12,
    ) -> Path:
        """Ghép nối Video Thí nghiệm ảo + Giọng đọc VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT."""
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [Virtual Lab Audio/SRT] Đang đóng gói hoàn thiện video bài giảng...")

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

        print(f"🎉 [Virtual Lab] Video hoàn thiện thành công: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scenes_meta: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_virtuallab",
    ) -> dict[str, Path]:
        """Đóng gói slide thí nghiệm ảo sang PowerPoint (.pptx) và PDF (.pdf)."""
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        temp_slides_dir = self.runtime_dir / "temp_virtuallab_slides"
        temp_slides_dir.mkdir(parents=True, exist_ok=True)

        captured_slides = []
        for i, sc in enumerate(scenes_meta, 1):
            h_path = sc.get("html_path")
            r = sc.get("ratio", 0.5)
            s_img = temp_slides_dir / f"slide_{i:02d}.png"
            self.capture_still(Path(h_path), s_img, seek_ratio=r)
            captured_slides.append(s_img)

        res = package_slides(
            image_paths=captured_slides,
            output_dir=output_dir,
            base_name=base_name,
            formats=format_type,
        )
        print(f"📦 [Virtual Lab Slides] Đã đóng gói: {res}")
        return res

