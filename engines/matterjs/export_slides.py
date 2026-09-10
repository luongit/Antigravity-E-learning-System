#!/usr/bin/env python3
"""
engines/matterjs/export_slides.py
Bộ xuất bản bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 từ Matter.js Physics Engine.
- Chụp trạng thái quỹ đạo chuyển động cơ học 2D từ Matter.js Canvas.
- Đóng gói slide PowerPoint (.pptx) và tài liệu PDF 16:9 sắc nét qua core.pptx_engine.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.matterjs_engine import MatterJSEngine
from core.pptx_engine import package_slides


def export_matterjs_slides(
    video_dir: Path,
    scenes_meta: list[dict],
    output_dir: Path = None,
    format_type: str = "all",
    base_name: str = "slides_matterjs",
) -> dict[str, Path]:
    video_dir = video_dir.resolve()
    print("============================================================")
    print("🎨 [Matter.js Slide Exporter] Xuất PowerPoint & PDF 16:9")
    print(f"   Thư mục học liệu: {video_dir}")
    print("============================================================")

    engine = MatterJSEngine(video_dir)
    results = engine.export_slides(scenes_meta, output_dir, format_type, base_name)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xuất PowerPoint và PDF 16:9 từ Matter.js Engine")
    parser.add_argument("video_dir", nargs="?", default="output/buni-overview/video-1")
    parser.add_argument("--format", choices=["pptx", "pdf", "all"], default="all")
    parser.add_argument("--name", default="slides_matterjs")
    args = parser.parse_args()

    print("Matter.js Slide Exporter sẵn sàng.")
