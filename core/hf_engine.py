#!/usr/bin/env python3
"""
core/hf_engine.py
Trình điều phối trung tâm của Engine HyperFrames Thế Hệ 2 (v2):
- Hoàn toàn tự chủ, hỗ trợ đầy đủ 25 tính năng diễn hoạt đồ họa & trình chiếu bài giảng.
- Không phụ thuộc vào bất kỳ framework video bên thứ ba nào.
- Hỗ trợ JSON Scene Spec v2 Agent-friendly.
- Đầy đủ 25 tính năng: Spring physics, Timeline frame-accurate, Kinetic Typography,
  Code Studio typewriter, Visual Anchors (7 SVG + custom image), Multi-clip B-roll Cutaway,
  SRT Lockstep subtitles, Multi-track audio (TTS + Lo-Fi BGM), Smart-skip Puppeteer render,
  Batch rendering & Slide export (PNG/PPTX).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path
from typing import Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
HYPERFRAMES_ROOT = WORKSPACE_ROOT / "engines" / "hyperframes"
RENDERER_MJS = HYPERFRAMES_ROOT / "renderer" / "renderer.mjs"

# Import runtime builders
sys.path.insert(0, str(WORKSPACE_ROOT))
from engines.hyperframes.runtime.hf_scene_builder import HFSceneBuilder
from engines.hyperframes.runtime.hf_html_builder import build_html, save_html


def get_audio_duration(audio_path: Path) -> float:
    """Lấy thời lượng file audio chính xác bằng ffprobe."""
    if not audio_path.exists():
        return 40.0
    cmd = [
        "ffprobe",
        "-i",
        str(audio_path),
        "-show_entries",
        "format=duration",
        "-v",
        "quiet",
        "-of",
        "csv=p=0",
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0 and res.stdout.strip():
            return float(res.stdout.strip())
    except Exception:
        pass
    return 40.0


def parse_srt(srt_path: Path) -> list[dict]:
    """Phân tích file SRT thành danh sách timestamp phụ đề."""
    if not srt_path.exists():
        return []
    content = srt_path.read_text(encoding="utf-8-sig")
    pattern = re.compile(
        r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\d+\s*\n|\Z)",
        re.DOTALL,
    )
    items = []
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        t1 = m.group(2)
        t2 = m.group(3)
        txt = " ".join(m.group(4).strip().split())

        def to_sec(t: str) -> float:
            h, mi, s = t.replace(",", ".").split(":")
            return round(int(h) * 3600 + int(mi) * 60 + float(s), 3)

        items.append({"id": idx, "startSec": to_sec(t1), "endSec": to_sec(t2), "text": txt})
    return items


class HFEngine:
    """HyperFrames v2 Core Engine điều phối JSON Spec, Puppeteer Renderer & Slides."""

    def __init__(self, video_dir: Path | str):
        self.video_dir = Path(video_dir).resolve()
        self.audio_dir = self.video_dir / "mp3"
        self.broll_dir = WORKSPACE_ROOT / "inputs" / "video-libraries"

        # BGM options
        self.bgm_path = WORKSPACE_ROOT / "assets" / "audio" / "bg-lofi-tech.mp3"
        if not self.bgm_path.exists():
            alt_bgm = WORKSPACE_ROOT / "assets" / "audio" / "bg-lofi.mp3"
            if alt_bgm.exists():
                self.bgm_path = alt_bgm

    def parse_script_scenes(self) -> dict[int, dict]:
        """Đọc và trích xuất thông tin cảnh từ file script.md nếu có."""
        script_path = self.video_dir / "script.md"
        if not script_path.exists():
            return {}

        scenes: dict[int, dict] = {}
        content = script_path.read_text(encoding="utf-8")

        # Tìm các khối cảnh theo định dạng: ### Cảnh X: ... hoặc ## Slide X: ...
        scene_blocks = re.split(r"(?:###|##)\s*(?:Cảnh|Slide|Phân cảnh)\s*(\d+)", content, flags=re.IGNORECASE)
        if len(scene_blocks) > 1:
            for i in range(1, len(scene_blocks), 2):
                s_num = int(scene_blocks[i])
                block_text = scene_blocks[i + 1]

                title_m = re.search(r"Tiêu đề\s*:\s*(.+)", block_text, re.IGNORECASE)
                title = title_m.group(1).strip() if title_m else f"CẢNH {s_num}"

                cards = []
                card_matches = re.findall(r"-\s*\*\*([^*]+)\*\*:\s*(.+)", block_text)
                colors = ["#38BDF8", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"]
                for c_idx, (c_title, c_desc) in enumerate(card_matches):
                    cards.append({
                        "step": f"0{c_idx+1}",
                        "tag": "TRỌNG TÂM",
                        "title": c_title.strip(),
                        "desc": c_desc.strip(),
                        "color": colors[c_idx % len(colors)],
                    })

                scenes[s_num] = {
                    "title": title,
                    "subtitle": "",
                    "cards": cards,
                    "code_snippet": None,
                }
        return scenes

    def build_scene_spec(
        self,
        scene_num: int,
        duration_sec: float | None = None,
        theme: str = "dark-modern",
        layout: str = "cards-grid",
        spec_override: dict | None = None,
    ) -> dict:
        """Xây dựng HF Scene Spec v2 hoàn chỉnh cho 1 cảnh."""
        if spec_override:
            return spec_override

        # Tìm narration audio & srt
        mp3_path = self.audio_dir / f"mp3-{scene_num}.mp3"
        srt_path = self.audio_dir / f"mp3-{scene_num}.srt"
        if not mp3_path.exists():
            fallback_mp3 = self.audio_dir / f"scene_{scene_num}.mp3"
            if fallback_mp3.exists():
                mp3_path = fallback_mp3
                srt_path = self.audio_dir / f"scene_{scene_num}.srt"

        if duration_sec is None:
            if mp3_path.exists():
                duration_sec = get_audio_duration(mp3_path)
            else:
                duration_sec = 40.0

        builder = HFSceneBuilder()
        builder.set_meta(
            title=f"Bài Giảng E-Learning - Cảnh {scene_num}",
            fps=30,
            theme=theme,
        )

        if mp3_path.exists():
            rel_mp3 = os.path.relpath(mp3_path, self.video_dir).replace("\\", "/")
            rel_srt = os.path.relpath(srt_path, self.video_dir).replace("\\", "/") if srt_path.exists() else None
            builder.add_narration(rel_mp3, rel_srt)

        if self.bgm_path.exists():
            rel_bgm = os.path.relpath(self.bgm_path, self.video_dir).replace("\\", "/")
            builder.add_bgm(rel_bgm, volume=0.12)

        # Trích xuất dữ liệu nội dung từ script.md
        script_scenes = self.parse_script_scenes()
        info = script_scenes.get(scene_num)

        # Fallback dữ liệu mặc định chuẩn kiến trúc BUNI nếu không có trong script.md
        if not info:
            default_map = {
                1: {
                    "title": "CHƯƠNG TRÌNH ĐẠI HỌC ỨNG DỤNG BUNI",
                    "subtitle": "Hệ Sinh Thái Đại Học Ứng Dụng Liên Kết Doanh Nghiệp PTIT & Bachkhoa Aptech",
                    "cards": [
                        {"tag": "BẢN QUYỀN ĐÀO TẠO", "title": "Mô Hình Bản Quyền: 'Làm Trước Học Sau'", "desc": "Kế thừa mô hình bản quyền số 7190/2021/QTG của Bachkhoa.", "color": "#FF7043"},
                        {"tag": "PHƯƠNG CHÂM HÀNH ĐỘNG", "title": "Môi Trường Thực Chiến Đỉnh Cao", "desc": "Làm quen nhịp điệu doanh nghiệp ngay từ năm nhất.", "color": "#38BDF8"},
                        {"tag": "LỢI THẾ CẠNH TRANH", "title": "Làm Chủ Tương Lai Nghề Nghiệp", "desc": "Tự tin vững vàng sự nghiệp trong kỷ nguyên số.", "color": "#10B981"},
                    ],
                    "code_snippet": None,
                    "anchor": "buni-ecosystem",
                },
                2: {
                    "title": "MỤC TIÊU BÀI HỌC",
                    "subtitle": "Ba Giá Trị Trọng Tâm Nâng Tầm Năng Lực Sinh Viên",
                    "cards": [
                        {"tag": "TẦM NHÌN CHIẾN LƯỢC", "title": "Hệ Sinh Thái BUNI Toàn Diện", "desc": "Thấu hiểu tầm nhìn liên kết và lợi thế cạnh tranh.", "color": "#3B82F6"},
                        {"tag": "TRIẾT LÝ BẢN QUYỀN", "title": "Mô Hình 'Làm Trước Học Sau'", "desc": "Tiếp cận bài toán thực tế trước, đào sâu nguyên lý sau.", "color": "#F59E0B"},
                        {"tag": "THANG NĂNG LỰC", "title": "Bản Đồ Ngành Đào Tạo Mũi Nhọn", "desc": "Khám phá lộ trình 4 cấp độ dự án và chuyên ngành AI.", "color": "#10B981"},
                    ],
                    "code_snippet": None,
                    "anchor": "tech-orbit",
                },
                3: {
                    "title": "TRIẾT LÝ ĐỘC QUYỀN 'LÀM TRƯỚC HỌC SAU'",
                    "subtitle": "Chu Trình Học Tập Thực Chiến 3 Bước Bản Quyền Số 7190/2021/QTG",
                    "cards": [
                        {"tag": "BƯỚC 1: TIẾP CẬN", "title": "Bài Toán Thực Tế Doanh Nghiệp", "desc": "Bước thẳng vào tình huống công việc sống động.", "color": "#3B82F6"},
                        {"tag": "BƯỚC 2: XÂY DỰNG", "title": "Thử Nghiệm & Hình Thành Giải Pháp", "desc": "Tự tay tìm tòi, ghép nối và trực tiếp tạo ra sản phẩm.", "color": "#F59E0B"},
                        {"tag": "BƯỚC 3: TỐI ƯU", "title": "Đào Sâu Nguyên Lý Nền Tảng", "desc": "Tiếp nhận lý thuyết khoa học để tối ưu hóa sản phẩm.", "color": "#10B981"},
                    ],
                    "code_snippet": None,
                    "anchor": "four-stages",
                },
                4: {
                    "title": "LẤY SẢN PHẨM LÀM TRUNG TÂM & MÃ NGUỒN CHUẨN",
                    "subtitle": "Kiến Trúc Tự Động Hóa Thực Thi Pipeline E-Learning",
                    "cards": [
                        {"tag": "VÒNG ĐỜI SẢN PHẨM", "title": "Tư Duy Trọn Vẹn Từ Đề Bài Đến Triển Khai", "desc": "Phân tích yêu cầu -> Thiết kế -> Xây dựng mã nguồn -> Kiểm thử.", "color": "#38BDF8"},
                        {"tag": "THƯỚC ĐO NĂNG LỰC", "title": "Sản Phẩm Chạy Thực Tế", "desc": "Tích lũy hồ sơ năng lực số (Portfolio) qua từng dự án.", "color": "#10B981"},
                    ],
                    "code_snippet": {
                        "language": "python",
                        "title": "core/hf_engine.py",
                        "code": "def build_hyperframes_pipeline(video_dir: str):\n    \"\"\"HyperFrames v2 Autonomous Pipeline\"\"\"\n    engine = HFEngine(video_dir)\n    spec = engine.build_scene_spec(scene_num=1)\n    return engine.render(spec, output_path='scene_1.mp4')",
                    },
                    "anchor": "ai-robotics",
                },
            }
            info = default_map.get(scene_num, {
                "title": f"BÀI HỌC E-LEARNING - PHẦN {scene_num}",
                "subtitle": "Nội Dung Bài Giảng Chuyên Đề Ứng Dụng",
                "cards": [
                    {"tag": "MỤC TIÊU", "title": "Nắm vững kiến thức trọng tâm", "desc": "Hiểu rõ cơ chế và phương pháp thực hiện.", "color": "#38BDF8"},
                    {"tag": "THỰC HÀNH", "title": "Triển khai bài tập ứng dụng", "desc": "Áp dụng trực tiếp vào quy trình làm việc chuẩn.", "color": "#10B981"},
                ],
                "code_snippet": None,
                "anchor": "buni-student",
            })

        # Xác định layout phù hợp
        chosen_layout = layout
        if info.get("code_snippet"):
            chosen_layout = "split-right"
        elif info.get("anchor"):
            chosen_layout = "cards-grid"

        scene = builder.add_scene(
            scene_id=f"sc{scene_num}",
            duration=duration_sec,
            layout=chosen_layout,
            title=info["title"],
            badge=info.get("subtitle", ""),
            slide_number=scene_num,
        )

        # Gán Visual Anchor
        anchor_name = info.get("anchor", "buni-ecosystem")
        builder.set_visual_anchor(scene, anchor_type=anchor_name, size=460)

        # Tính toán thời điểm xuất hiện thẻ theo SRT Lockstep
        srt_items = parse_srt(srt_path) if srt_path.exists() else []
        cards = info.get("cards", [])
        for c_idx, card in enumerate(cards):
            card_title_lower = card["title"].lower()
            appear_time = None
            if srt_items:
                # Tìm cue có chứa từ khóa của card title
                first_words = [w for w in re.findall(r"\w+", card_title_lower) if len(w) > 2]
                for cue in srt_items:
                    cue_txt = cue["text"].lower()
                    if any(w in cue_txt for w in first_words):
                        appear_time = cue["startSec"]
                        break
            if appear_time is None:
                appear_time = 0.8 + c_idx * 1.8

            builder.add_card(
                scene=scene,
                tag=card.get("tag", "NỘI DUNG"),
                title=card["title"],
                desc=card["desc"],
                accent_color=card.get("color", "#38BDF8"),
                appear_sec=round(appear_time, 2),
                animation_preset="springUp",
            )

        # Code Studio Snippet
        code_info = info.get("code_snippet")
        if code_info:
            builder.add_code(
                scene=scene,
                language=code_info.get("language", "python"),
                filename=code_info.get("title", "pipeline.py"),
                code=code_info.get("code", ""),
                delay=1.5,
                char_duration=4.0,
            )

        # B-roll Cutaways
        cutaways = self.resolve_broll_cutaways(scene_num, srt_items)
        for cut in cutaways:
            builder.add_cutaway(
                scene=scene,
                start_sec=cut["startSec"],
                end_sec=cut["endSec"],
                clips=cut["clips"],
                label=cut.get("label", "BỐI CẢNH MINH HỌA"),
            )

        spec = builder.build()
        errors = HFSceneBuilder.validate(spec)
        if errors:
            print(f"[HFEngine] Cảnh báo kiểm tra Spec (Cảnh {scene_num}):", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)

        return spec

    def resolve_broll_cutaways(self, scene_num: int, srt_items: list[dict]) -> list[dict]:
        """Tự động khớp video B-roll minh họa ngữ nghĩa từ thư viện video."""
        cutaways = []
        if not srt_items or not self.broll_dir.exists():
            return cutaways

        # Danh sách video có sẵn theo chuyên đề
        broll_clips = list(self.broll_dir.glob("**/*.mp4"))
        if not broll_clips:
            return cutaways

        # Tìm các đoạn dẫn dắt mở bài hoặc liên hệ thực tế
        for cue in srt_items:
            cue_txt = cue["text"].lower()
            if any(k in cue_txt for k in ["thực tế", "doanh nghiệp", "kỷ nguyên số", "thị trường", "môi trường"]):
                duration = cue["endSec"] - cue["startSec"]
                if duration >= 3.5:
                    chosen_clip = broll_clips[scene_num % len(broll_clips)]
                    rel_clip = os.path.relpath(chosen_clip, self.video_dir).replace("\\", "/")
                    cutaways.append({
                        "startSec": cue["startSec"],
                        "endSec": cue["endSec"],
                        "label": "LIÊN HỆ THỰC TIỄN DOANH NGHIỆP",
                        "clips": [rel_clip],
                    })
                    break  # Mỗi cảnh tối đa 1 cutaway tự động nếu không cấu hình thêm
        return cutaways

    def render_scene(
        self,
        scene_num: int,
        output_path: Path | str | None = None,
        mode: str = "video",
        spec_override: dict | None = None,
    ) -> Path:
        """
        Render một cảnh ra MP4 (video) hoặc PNG (slide) hoặc xem trước (preview).
        """
        output_dir = self.video_dir
        if output_path:
            out_file = Path(output_path).resolve()
        else:
            if mode == "slides":
                out_file = output_dir / f"slide_{scene_num}.png"
            else:
                out_file = output_dir / f"scene_{scene_num}_hf.mp4"

        out_file.parent.mkdir(parents=True, exist_ok=True)

        # 1. Tạo Spec
        spec = self.build_scene_spec(scene_num, spec_override=spec_override)

        # 2. Lưu Spec JSON & Sinh Master HTML
        spec_json_path = output_dir / f"hf_spec_scene_{scene_num}.json"
        spec_json_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")

        html_path = output_dir / f"hf_scene_{scene_num}.html"
        save_html(spec, self.video_dir, html_path, silent_mode=(mode != "preview"))

        # 3. Chế độ Preview
        if mode == "preview":
            print(f"[HFEngine] Mở xem trước cảnh {scene_num} trên trình duyệt...")
            webbrowser.open(html_path.as_uri())
            return html_path

        # 4. Chạy Renderer (Puppeteer + FFmpeg)
        node_cmd = shutil.which("node") or "node"
        renderer_script = RENDERER_MJS

        cmd = [
            node_cmd,
            str(renderer_script),
            f"--spec={spec_json_path}",
            f"--html={html_path}",
            f"--output={out_file}",
        ]

        if mode == "slides":
            cmd.append("--slides")
            cmd.append(f"--slides-dir={output_dir}")

        print(f"[HFEngine] Bắt đầu render Cảnh {scene_num} ({mode}) -> {out_file.name}...")
        res = subprocess.run(cmd, cwd=str(HYPERFRAMES_ROOT), check=False)
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi render HyperFrames cảnh {scene_num} (mã thoát: {res.returncode})")

        print(f"[HFEngine] Render thành công: {out_file}")
        return out_file

    def export_slides(self, scene_num: int | None = None, output_dir: Path | str | None = None) -> list[Path]:
        """Xuất ảnh tĩnh 1920x1080 của slide để đóng gói PowerPoint/PDF."""
        out_dir = Path(output_dir).resolve() if output_dir else self.video_dir / "slides_hf"
        out_dir.mkdir(parents=True, exist_ok=True)

        scenes_to_export = [scene_num] if scene_num else [1, 2, 3, 4]
        results = []
        for s in scenes_to_export:
            slide_out = out_dir / f"slide_{s}.png"
            self.render_scene(scene_num=s, output_path=slide_out, mode="slides")
            if slide_out.exists():
                results.append(slide_out)
        return results

    def batch_render(self, scenes: list[int] | None = None, mode: str = "video") -> list[Path]:
        """Render hàng loạt danh sách các cảnh."""
        scenes_list = scenes or [1, 2, 3, 4]
        outputs = []
        print(f"[HFEngine] Bắt đầu batch render {len(scenes_list)} cảnh: {scenes_list}")
        for s in scenes_list:
            out = self.render_scene(scene_num=s, mode=mode)
            outputs.append(out)
        print(f"[HFEngine] Hoàn thành batch render {len(outputs)} cảnh.")
        return outputs


def main():
    parser = argparse.ArgumentParser(description="HyperFrames v2 Autonomous CLI Orchestrator")
    parser.add_argument("video_dir", type=str, help="Đường dẫn thư mục video học liệu (chứa script.md, mp3/)")
    parser.add_argument("--scene", "-s", type=int, default=1, help="Số thứ tự cảnh cần render (mặc định: 1)")
    parser.add_argument("--output", "-o", type=str, default=None, help="Đường dẫn file xuất kết quả")
    parser.add_argument("--mode", "-m", choices=["video", "slides", "preview"], default="video", help="Chế độ render")
    parser.add_argument("--batch", "-b", type=str, default=None, help="Danh sách cảnh cần render gộp (vd: 1,2,3)")
    parser.add_argument("--theme", type=str, default="dark-modern", help="Theme màu sắc bài giảng")

    args = parser.parse_args()
    engine = HFEngine(args.video_dir)

    if args.batch:
        scenes = [int(x.strip()) for x in args.batch.split(",") if x.strip().isdigit()]
        engine.batch_render(scenes=scenes, mode=args.mode)
    else:
        engine.render_scene(scene_num=args.scene, output_path=args.output, mode=args.mode)


if __name__ == "__main__":
    main()
