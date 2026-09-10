"""
core/preflight.py
Module kiểm tra điều kiện tiên quyết (Pre-flight Check) & Tự động định tuyến (Dynamic Routing).
Giúp Agent và người dùng biết chính xác:
- Hiện tại đang có những tài nguyên gì?
- Thiếu điều kiện gì để render video hoặc tạo audio?
- Đề xuất kế hoạch hành động tối ưu tiếp theo.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from core.voice_parser import parse_voice_script
except ImportError:
    from voice_parser import parse_voice_script

try:
    from core.theme_manager import get_theme, detect_recommended_theme, list_themes
    from core.broll_manager import BRollManager
except ImportError:
    from theme_manager import get_theme, detect_recommended_theme, list_themes
    from broll_manager import BRollManager


class PreflightChecker:
    def __init__(self, target_dir: Optional[str] = None):
        self.workspace_root = Path(__file__).resolve().parent.parent
        if target_dir:
            p = Path(target_dir)
            self.target_dir = p if p.is_absolute() else (self.workspace_root / p).resolve()
        else:
            self.target_dir = None

    def find_voice_script(self, search_dir: Optional[Path] = None) -> Optional[Path]:
        """Tìm file voice script theo các vị trí ưu tiên."""
        # 1. Ưu tiên cao nhất: voice-script.* ngay trong search_dir
        if search_dir and search_dir.exists():
            for f in search_dir.iterdir():
                if f.is_file() and ("voice-script" in f.name.lower() or "voice_script" in f.name.lower()):
                    return f

        # 2. Ưu tiên thứ 2: trong inputs/voice_scripts/
        input_vs = self.workspace_root / "inputs" / "voice_scripts"
        if input_vs.exists():
            for f in input_vs.iterdir():
                if f.is_file() and f.suffix.lower() in (".txt", ".md"):
                    return f

        # 3. Ưu tiên thứ 3: script.md trong search_dir
        if search_dir and (search_dir / "script.md").exists():
            return search_dir / "script.md"

        # 4. Ưu tiên thứ 4: script.md ở thư mục cha (môn học)
        if search_dir and search_dir.parent.exists() and (search_dir.parent / "script.md").exists():
            return search_dir.parent / "script.md"

        # 5. Fallback các file .txt/.md khác
        if search_dir and search_dir.exists():
            for f in search_dir.iterdir():
                if f.is_file() and f.suffix.lower() in (".txt", ".md") and "plan" not in f.name.lower():
                    return f
        return None

    def find_images(self, search_dir: Optional[Path] = None) -> List[Path]:
        """Tìm danh sách ảnh slide theo thứ tự."""
        img_dirs = []
        if search_dir:
            if (search_dir / "images").exists():
                img_dirs.append(search_dir / "images")
            if search_dir.name == "images":
                img_dirs.append(search_dir)
            img_dirs.append(search_dir)

        # Fallback vào inputs/images
        input_img = self.workspace_root / "inputs" / "images"
        if input_img.exists():
            img_dirs.append(input_img)

        exts = (".png", ".jpeg", ".jpg", ".webp")
        found = []
        for d in img_dirs:
            if d.exists():
                imgs = [p for p in d.iterdir() if p.suffix.lower() in exts and not p.name.startswith(".")]
                if imgs:
                    # Nếu có các file đặt tên theo mẫu slide-X thì ưu tiên lấy nhóm này
                    slide_imgs = [p for p in imgs if re.search(r"slide[-_]?\d+", p.stem, re.IGNORECASE)]
                    if slide_imgs:
                        imgs = slide_imgs

                    # Sắp xếp theo số thứ tự slide
                    def sort_key(p):
                        m = re.search(r"(\d+)", p.stem)
                        return int(m.group(1)) if m else 999
                    found = sorted(imgs, key=sort_key)
                    break
        return found

    def find_audio_and_srt(self, search_dir: Optional[Path] = None) -> Dict[str, List[Path]]:
        """Tìm các file mp3 và srt đã có."""
        mp3_dir = None
        if search_dir:
            if (search_dir / "mp3").exists():
                mp3_dir = search_dir / "mp3"
            elif search_dir.name == "mp3":
                mp3_dir = search_dir

        mp3s, srts = [], []
        if mp3_dir and mp3_dir.exists():
            mp3s = sorted([p for p in mp3_dir.glob("*.mp3")])
            srts = sorted([p for p in mp3_dir.glob("*.srt")])
        return {"mp3": mp3s, "srt": srts}

    def check(self, target_dir: Optional[str] = None, engine: Optional[str] = None, for_video: bool = False, theme: Optional[str] = None) -> Dict[str, Any]:
        """Thực hiện kiểm tra toàn diện và trả về báo cáo phân tích."""
        if target_dir:
            p = Path(target_dir)
            t_dir = p if p.is_absolute() else (self.workspace_root / p).resolve()
        elif self.target_dir:
            t_dir = self.target_dir
        else:
            t_dir = self.workspace_root

        # Quét thư viện video B-roll
        broll_mgr = BRollManager(self.workspace_root)
        broll_libs = broll_mgr.scan_libraries()
        broll_info = {
            "total_categories": len(broll_libs),
            "categories": list(broll_libs.keys()),
            "total_videos": sum(len(v) for v in broll_libs.values())
        }

        SUPPORTED_ENGINES = ("opencv", "hyperframes", "manim", "3dmol", "matterjs", "vexflow", "cesium", "molstar", "virtuallab")
        if engine is not None:
            engine = engine.lower().replace("-", "").replace("_", "")
            if engine in ("virtuallab", "lab", "virtual"):
                engine = "virtuallab"
            if engine not in SUPPORTED_ENGINES:
                raise ValueError(f"Engine phải là một trong: {', '.join(SUPPORTED_ENGINES)}")
        # Engine choice precedes engine-specific prerequisites. HTML scenes do
        # not require flattened slide images. Never infer consent from assets.
        if (for_video and engine is None) or engine in ("hyperframes", "manim", "3dmol", "matterjs", "vexflow", "cesium", "molstar", "virtuallab"):
            script = t_dir / "script.md"
            images = sorted((t_dir / "images").glob("*")) if (t_dir / "images").is_dir() else []
            images = [p for p in images if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
            audio = self.find_audio_and_srt(t_dir)
            has_script = script.is_file() and bool(script.read_text(encoding="utf-8-sig").strip())
            selecting = engine is None

            sample_text = script.read_text(encoding="utf-8-sig") if has_script else ""
            rec_theme = detect_recommended_theme(sample_text)
            chosen_theme = theme if theme else rec_theme
            theme_meta = get_theme(chosen_theme)

            target_skill = f"elearning-virtual-lab-video" if engine == "virtuallab" else (f"elearning-{engine}-video" if engine in ("manim", "3dmol", "matterjs", "vexflow", "cesium", "molstar") else "elearning-hyperframes-video")

            return {
                "status": "STATUS_NEED_VIDEO_ENGINE" if selecting else (
                    "STATUS_NEED_SCENE_PREPARATION" if has_script else "STATUS_NEED_VIDEO_SCRIPT"),
                "target_dir": str(t_dir), "engine": engine,
                "next_skill": "elearning-video" if selecting else target_skill,
                "question": "OpenCV, HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar hay Virtual Lab" if selecting else None,
                "theme": chosen_theme,
                "theme_name": theme_meta["name"],
                "recommended_theme": rec_theme,
                "broll_libraries": broll_info,
                "num_images": len(images), "images": [p.name for p in images],
                "script_file": str(script) if has_script else None,
                # A four-column Markdown table is not a plain voice script.
                "voice_script_file": None, "num_voice_sections": None,
                "num_mp3": len(audio["mp3"]), "num_srt": len(audio["srt"]),
                "missing": [] if selecting or has_script else [f"Thiếu script.md riêng của video: {script}"],
                "action_plan": ["Chọn engine: OpenCV, HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar hay Virtual Lab"] if selecting else ([
                    f"Đọc script.md của video và áp dụng Theme phong cách: {theme_meta['name']}.",
                    "Đối chiếu từng slide với MP3/SRT; bổ sung audio còn thiếu qua elearning-audio.",
                    f"Tận dụng {broll_info['total_videos']} video B-roll từ inputs/video-libraries/ cho các đoạn voice dài (>15s)." if broll_info['total_videos'] > 0 else "Có thể bổ sung video minh họa vào inputs/video-libraries/ để tự động trám cảnh.",
                    f"Dùng {target_skill} để dựng, kiểm tra, xem trước và render."
                ] if has_script else ["Cần kịch bản riêng của video; không lấy nhầm kịch bản môn học hoặc video khác."])
            }

        # 1. Tìm ảnh
        images = self.find_images(t_dir)
        num_images = len(images)

        # 2. Tìm voice script
        vs_path = self.find_voice_script(t_dir)
        voice_sections = []
        if vs_path:
            voice_sections = parse_voice_script(str(vs_path))
        num_voice = len(voice_sections)

        # 3. Tìm audio & srt
        audio_info = self.find_audio_and_srt(t_dir)
        num_mp3 = len(audio_info["mp3"])
        num_srt = len(audio_info["srt"])

        # 4. Đánh giá điều kiện
        has_images = num_images > 0
        has_voice = num_voice > 0
        has_audio = num_mp3 > 0 and num_mp3 == num_images
        has_srt = num_srt > 0 and num_srt == num_images

        status = "UNKNOWN"
        action_plan = []
        missing = []

        if has_images and has_audio and has_srt:
            status = "STATUS_READY_FOR_VIDEO"
            action_plan.append("Đã có đủ ảnh, audio MP3 và phụ đề SRT.")
            action_plan.append("Kích hoạt elearning-opencv-video." if engine == "opencv" else
                               "Chuyển elearning-video để chọn engine: OpenCV hay hyperframes")
        elif has_images and has_voice:
            if not has_audio or not has_srt:
                status = "STATUS_NEED_AUDIO_GENERATION"
                action_plan.append(f"Đã nhận diện {num_images} ảnh slide và {num_voice} đoạn voice script.")
                if num_images != num_voice:
                    action_plan.append(f"CẢNH BÁO: Số lượng ảnh ({num_images}) chưa khớp số đoạn voice ({num_voice})!")
                action_plan.append("Tạo Audio TTS & SRT qua elearning-audio; đến giai đoạn 5 chuyển qua elearning-video, không tự chọn engine.")
        elif not has_images and has_voice:
            status = "STATUS_NEED_IMAGES"
            missing.append("Thiếu thư mục ảnh slide (images/). Cần cung cấp các file slide-1.png, slide-2.png... hoặc sinh ảnh từ kịch bản.")
        elif has_images and not has_voice:
            status = "STATUS_NEED_VOICE_SCRIPT"
            missing.append("Thiếu file Voice Script. Cần cung cấp file voice_script.txt với các đoạn cách nhau bởi dòng trống.")
        else:
            # Kiểm tra xem có tài liệu thô ở inputs/documents không
            doc_dir = self.workspace_root / "inputs" / "documents"
            raw_docs = list(doc_dir.glob("*.*")) if doc_dir.exists() else []
            if raw_docs:
                status = "STATUS_START_FROM_DOCUMENTS"
                action_plan.append(f"Phát hiện tài liệu thô trong inputs/documents/ ({len(raw_docs)} tệp).")
                action_plan.append("Kích hoạt quy trình toàn trình từ Giai đoạn 1: Soạn kịch bản & đề cương bài giảng.")
            else:
                status = "STATUS_EMPTY_WORKSPACE"
                missing.append("Chưa có tài liệu nguồn, voice script hoặc ảnh slide nào trong hệ thống.")

        # Nhận diện Theme cho inventory check
        sample_vs_text = vs_path.read_text(encoding="utf-8-sig") if (vs_path and vs_path.is_file()) else ""
        rec_theme = detect_recommended_theme(sample_vs_text)
        chosen_theme = theme if theme else rec_theme
        theme_meta = get_theme(chosen_theme)

        report = {
            "status": status,
            "engine": engine,
            "next_skill": "elearning-opencv-video" if engine == "opencv" else "elearning-video",
            "target_dir": str(t_dir),
            "theme": chosen_theme,
            "theme_name": theme_meta["name"],
            "recommended_theme": rec_theme,
            "broll_libraries": broll_info,
            "num_images": num_images,
            "images": [p.name for p in images],
            "voice_script_file": vs_path.name if vs_path else None,
            "num_voice_sections": num_voice,
            "num_mp3": num_mp3,
            "num_srt": num_srt,
            "missing": missing,
            "action_plan": action_plan
        }
        return report

    def print_report(self, report: Dict[str, Any]):
        """In báo cáo định dạng console tiếng Việt rõ ràng."""
        sys.stdout.reconfigure(encoding='utf-8')
        print("=" * 60)
        print(" BÁO CÁO PRE-FLIGHT CHECK (KIỂM TRA ĐIỀU KIỆN SẢN XUẤT)")
        print("=" * 60)
        print(f"- Thư mục kiểm tra : {report['target_dir']}")
        print(f"- Trạng thái       : {report['status']}")
        print("-" * 60)
        print(f"[1] Ảnh Slide      : {report['num_images']} tệp")
        if report['images']:
            print(f"    Mẫu            : {', '.join(report['images'][:4])}...")
        print(f"[2] Voice Script   : {report['voice_script_file'] or 'Chưa có'}")
        print(f"    Số đoạn lời    : {report['num_voice_sections'] if report['num_voice_sections'] is not None else 'Cần đọc bảng script.md'}")
        if report.get("script_file"):
            print(f"    Kịch bản cảnh  : {report['script_file']}")
        print(f"[3] Âm thanh & Phụ đề:")
        print(f"    File MP3       : {report['num_mp3']} tệp")
        print(f"    File SRT       : {report['num_srt']} tệp")
        if report.get("theme_name"):
            print(f"[4] Theme Phong cách: {report['theme_name']} ({report.get('theme')})")
        if report.get("broll_libraries"):
            b_info = report["broll_libraries"]
            cats = ", ".join(b_info["categories"]) if b_info["categories"] else "Chưa có chủ đề"
            print(f"[5] Video B-roll   : {b_info['total_videos']} tệp trong {b_info['total_categories']} chủ đề ({cats})")
        print("-" * 60)
        if report['missing']:
            print("CẦN BỔ SUNG:")
            for m in report['missing']:
                print(f"  [X] {m}")
        if report['action_plan']:
            print("KẾ HOẠCH HÀNH ĐỘNG ĐỀ XUẤT:")
            for a in report['action_plan']:
                print(f"  -> {a}")
        print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kiểm tra tài nguyên; --stage video yêu cầu chọn engine trước khi dựng.")
    parser.add_argument("target", nargs="?", default="output/KNM01/video-1")
    parser.add_argument("--engine", type=str.lower, choices=("opencv", "hyperframes", "manim", "3dmol", "matterjs", "vexflow", "cesium", "molstar", "virtuallab"))
    parser.add_argument("--theme", type=str.lower, choices=("light-whiteboard", "dark-modern", "ai-tech-neon", "flat-editorial"))
    parser.add_argument("--stage", choices=("inventory", "video"), default="inventory")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checker = PreflightChecker()
    rep = checker.check(args.target, engine=args.engine, for_video=args.stage == "video", theme=args.theme)
    if args.json:
        sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        checker.print_report(rep)
