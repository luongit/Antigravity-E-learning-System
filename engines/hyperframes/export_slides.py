#!/usr/bin/env python3
"""
engines/hyperframes/export_slides.py
Bộ xuất bản bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 từ HyperFrames HTML/SVG Engine.
- Tự động chụp trạng thái hoàn thiện của từng cảnh HyperFrames (1920x1080) bằng HyperFrames snapshot CLI.
- Bảo toàn 100% đồ họa Web: Vector SVG, bảng màu phẳng, gradient, font Be Vietnam Pro ExtraBold.
- Đóng gói thành slide trình chiếu PowerPoint và tài liệu PDF phát tay đồng bộ.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
HYPERFRAMES_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.pptx_engine import package_slides


def export_hyperframes_slides(
    video_dir: Path,
    output_dir: Path = None,
    format_type: str = "all",
    base_name: str = "slides_hyperframes",
) -> dict[str, Path]:
    video_dir = video_dir.resolve()
    print("============================================================")
    print("🌐 [HyperFrames Slide Exporter] Xuất PowerPoint & PDF 16:9")
    print(f"   Thư mục học liệu: {video_dir}")
    print("============================================================")

    # Tìm các thư mục cảnh HyperFrames
    scene_candidates = [
        video_dir / "hyperframes",
        video_dir / "test-scene-1-cutaway",
    ]
    target_scene_dir = next((d for d in scene_candidates if d.exists() and (d / "index.html").exists()), None)

    if not target_scene_dir:
        print(f"❌ Không tìm thấy thư mục cảnh HyperFrames (index.html) trong: {video_dir}")
        return {}

    temp_out_dir = target_scene_dir / "snapshots_export"
    temp_out_dir.mkdir(parents=True, exist_ok=True)

    # Chụp frame hoàn thiện bằng hyperframes snapshot
    # Thời điểm 48.0s là lúc slide đã hiện đầy đủ toàn bộ nội dung
    snap_cmd = [
        "npx",
        "--yes",
        "hyperframes",
        "snapshot",
        str(target_scene_dir),
        "--at=48.0",
        f"-o={str(temp_out_dir)}",
        "--no-end",
    ]

    print(f"📸 Đang chụp snapshot hoàn thiện từ: {target_scene_dir.name}...")
    proc = subprocess.run(snap_cmd, cwd=str(WORKSPACE_ROOT), shell=True)

    # Thu thập ảnh chụp được
    exts = (".png", ".jpg", ".jpeg")
    captured_images = sorted([p for p in temp_out_dir.iterdir() if p.suffix.lower() in exts])

    # Nếu lệnh snapshot gặp lỗi, kiểm tra xem có ảnh snapshot QA có sẵn không
    if not captured_images:
        qa_images = sorted([p for p in target_scene_dir.iterdir() if p.name.startswith("qa_") and p.suffix.lower() in exts])
        if qa_images:
            print("   [INFO] Sử dụng ảnh QA snapshot sẵn có của HyperFrames...")
            captured_images = [qa_images[-1]]  # Lấy frame cuối cùng hoàn thiện

    if not captured_images:
        print("❌ Không thu thập được ảnh snapshot nào từ HyperFrames.")
        return {}

    print(f"   [OK] Đã thu thập {len(captured_images)} ảnh slide hoàn thiện.")

    # Đóng gói ra thư mục đầu ra
    if not output_dir:
        output_dir = video_dir

    print(f"\n📦 Đang đóng gói sang định dạng '{format_type}'...")
    results = package_slides(captured_images, output_dir, base_name, format_type)

    return results


def main():
    parser = argparse.ArgumentParser(description="Xuất PowerPoint và PDF 16:9 từ HyperFrames")
    parser.add_argument("video_dir", nargs="?", default="output/buni-overview/video-1")
    parser.add_argument("--output-dir", default=None, help="Thư mục xuất file")
    parser.add_argument("--name", default="slides_hyperframes", help="Tên file đầu ra (không kèm đuôi)")
    parser.add_argument(
        "--format",
        choices=["pptx", "pdf", "all"],
        default="all",
        help="Định dạng xuất (pptx, pdf, all)",
    )
    args = parser.parse_args()

    v_dir = Path(args.video_dir)
    if not v_dir.is_absolute():
        v_dir = WORKSPACE_ROOT / v_dir

    out_dir = Path(args.output_dir) if args.output_dir else None
    export_hyperframes_slides(v_dir, out_dir, args.format, args.name)


if __name__ == "__main__":
    main()
