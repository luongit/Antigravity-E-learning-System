#!/usr/bin/env python3
"""
core/manim_engine.py
Thư viện lõi điều phối Manim Community Engine cho Hệ thống E-Learning Antigravity.
- Chuyên dụng cho các bài giảng IT, Giải thuật, Cấu trúc dữ liệu, Đồ thị, Ma trận & Toán STEM.
- Sinh mã nguồn Manim Python scene từ kịch bản script.md.
- Biên dịch video qua Manim CLI (-qh 1080p60 hoặc -qm 720p30 / custom 1080p30).
- Trích xuất ảnh tĩnh hoàn thiện (--save_last_frame) để đóng gói PowerPoint (.pptx) và PDF 16:9.
- Ghép nối audio VieNeu-TTS v3 Turbo, hòa trộn BGM Lo-Fi và phụ đề SRT theo Quy chuẩn Sản xuất E-Learning.
"""

from __future__ import annotations

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


class ManimEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        self.video_dir = Path(video_dir).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "manim"
        self.output_dir = self.video_dir

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Định vị Python và Manim trong môi trường
        self.python_bin = self._resolve_python_bin()
        self.manim_bin = self._resolve_manim_bin()

    def _resolve_python_bin(self) -> str:
        venv_py = WORKSPACE_ROOT / ".venv" / "Scripts" / "python.exe"
        if venv_py.exists():
            return str(venv_py)
        venv_py_posix = WORKSPACE_ROOT / ".venv" / "bin" / "python"
        if venv_py_posix.exists():
            return str(venv_py_posix)
        return sys.executable

    def _resolve_manim_bin(self) -> list[str]:
        # Ưu tiên python -m manim từ venv để tránh xung đột path
        return [self.python_bin, "-m", "manim"]

    def check_environment(self) -> dict[str, bool]:
        """Kiểm tra môi trường Manim, FFmpeg và các thư viện cần thiết."""
        status = {
            "python": True,
            "manim": False,
            "ffmpeg": False,
        }

        # Check manim
        try:
            res = subprocess.run(
                self.manim_bin + ["--version"],
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode == 0:
                status["manim"] = True
        except Exception:
            status["manim"] = False

        # Check ffmpeg
        try:
            res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                status["ffmpeg"] = True
        except Exception:
            status["ffmpeg"] = False

        # Check latex
        status["latex"] = shutil.which("latex") is not None

        return status

    def has_latex(self) -> bool:
        """Kiểm tra hệ thống có LaTeX (MiKTeX/TeXLive) hay không."""
        return shutil.which("latex") is not None

    def generate_manim_script(self, code_content: str, script_path: Union[str, Path]) -> Path:
        """Lưu mã nguồn Python Manim vào đường dẫn chỉ định."""
        p = Path(script_path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(code_content.strip() + "\n")
        return p

    def generate_scene_script(self, code_content: str, script_filename: str = "manim_scene.py") -> Path:
        """Lưu mã nguồn Manim Python do Agent sinh vào thư mục runtime/tasks/."""
        script_path = self.tasks_dir / script_filename
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code_content.strip() + "\n")
        print(f"📄 [Manim] Đã tạo kịch bản code Manim: {script_path.name}")
        return script_path

    def render_scene(
        self,
        script_path: Path,
        scene_class_name: str,
        quality: str = "1080p30",
        transparent: bool = False,
    ) -> Path:
        """
        Biên dịch Scene Manim ra video MP4 raw (chưa lồng tiếng).
        Quality options:
        - '1080p60': -qh
        - '1080p30': -r 1920,1080 --fps 30
        - '720p30': -qm
        - '480p15': -ql
        """
        script_path = Path(script_path).resolve()
        print(f"🎬 [Manim Render] Đang biên dịch Scene: {scene_class_name} (chất lượng: {quality})...")

        cmd = list(self.manim_bin)

        if quality == "1080p60":
            cmd.append("-qh")
        elif quality == "720p30":
            cmd.append("-qm")
        elif quality == "480p15":
            cmd.append("-ql")
        else:  # Mặc định 1080p30 chuẩn video E-learning
            cmd.extend(["-r", "1920,1080", "--fps", "30"])

        cmd.extend([
            "--format=mp4",
            "--media_dir", str(self.cache_dir),
        ])

        if transparent:
            cmd.append("-t")

        cmd.extend([str(script_path), scene_class_name])

        proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT))
        if proc.returncode != 0:
            raise RuntimeError(f"Lỗi khi biên dịch Manim Scene '{scene_class_name}' từ file '{script_path}'.")

        # Tìm video đầu ra trong cache media dir của Manim
        video_search_pattern = self.cache_dir / "videos" / script_path.stem / "**" / f"{scene_class_name}.mp4"
        found_videos = list(self.cache_dir.glob(f"videos/{script_path.stem}/**/{scene_class_name}.mp4"))

        if not found_videos:
            raise FileNotFoundError(f"Không tìm thấy video output của Manim theo mẫu: {video_search_pattern}")

        # Lấy video mới nhất
        rendered_video = sorted(found_videos, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        print(f"   [OK] Biên dịch thành công: {rendered_video.name}")
        return rendered_video

    def render_still(self, script_path: Path, scene_class_name: str, output_image_path: Path) -> Path:
        """Chụp khung hình cuối cùng của Scene (--save_last_frame) làm ảnh Slide tĩnh 1920x1080."""
        script_path = Path(script_path).resolve()
        output_image_path = Path(output_image_path).resolve()
        output_image_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"📸 [Manim Still] Đang trích xuất ảnh slide tĩnh của {scene_class_name}...")

        cmd = list(self.manim_bin) + [
            "-s",  # save last frame
            "-r", "1920,1080",
            "--media_dir", str(self.cache_dir),
            str(script_path),
            scene_class_name,
        ]

        proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT))
        if proc.returncode != 0:
            raise RuntimeError(f"Lỗi khi chụp still frame Manim Scene '{scene_class_name}'.")

        # Tìm ảnh được sinh ra trong images/ (Manim CE thường gắn hậu tố _ManimCE_v*.png)
        found_images = list(self.cache_dir.glob(f"images/{script_path.stem}/**/{scene_class_name}*.png"))
        if not found_images:
            raise FileNotFoundError(f"Không tìm thấy still image của Manim Scene '{scene_class_name}'.")

        latest_image = sorted(found_images, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        shutil.copy2(latest_image, output_image_path)
        print(f"   [OK] Đã xuất ảnh slide: {output_image_path.name}")
        return output_image_path

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
        Dùng FFmpeg ghép Video Manim + Audio VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT.
        Tuân thủ Quy chuẩn Sản xuất E-Learning:
        - Phụ đề Be Vietnam Pro ExtraBold, 44-48px tương ứng FontSize=26, không stroke lem luốc.
        """
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [Manim Audio/SRT Integration] Đang đóng gói hoàn thiện video...")

        cmd = ["ffmpeg", "-y", "-i", str(raw_video)]

        has_narration = audio_path and Path(audio_path).exists()
        has_bgm = bgm_path and Path(bgm_path).exists()
        has_srt = srt_path and Path(srt_path).exists()

        if has_narration:
            cmd.extend(["-i", str(Path(audio_path).resolve())])
        if has_bgm:
            cmd.extend(["-stream_loop", "-1", "-i", str(Path(bgm_path).resolve())])

        # Filter subtitle & audio mix
        filters = []

        if has_srt:
            # Format subtitle font & style chuẩn
            escaped_srt = str(Path(srt_path).resolve()).replace("\\", "/").replace(":", "\\:")
            # Quy chuẩn: Font Be Vietnam Pro ExtraBold, PrimaryColour White (&H00FFFFFF), No black stroke, Box nền mờ
            sub_filter = (
                f"subtitles='{escaped_srt}':force_style="
                "'Fontname=Be Vietnam Pro,FontSize=24,Bold=1,PrimaryColour=&H00FFFFFF,"
                "BackColour=&H900F172A,BorderStyle=4,Shadow=0,MarginV=35'"
            )
            filters.append(sub_filter)

        if filters:
            cmd.extend(["-vf", ",".join(filters)])

        # Audio mixing
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

        print(f"🎉 [XUẤT SẮC] Video Manim hoàn thiện: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scenes_data: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_manim",
    ) -> dict[str, Path]:
        """
        Chụp still frame của các scene và đóng gói thành slide PowerPoint (.pptx) và PDF 16:9.
        """
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        captured_slides = []
        for i, sc in enumerate(scenes_data, 1):
            script_path = sc.get("script_path")
            scene_class = sc.get("scene_class")
            out_img = self.runtime_dir / "temp_slide_frames" / f"manim_slide_{i}.png"
            img_path = self.render_still(Path(script_path), scene_class, out_img)
            captured_slides.append(img_path)

        results = package_slides(captured_slides, output_dir, base_name, format_type)
        return results
