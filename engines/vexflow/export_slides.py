#!/usr/bin/env python3
"""
engines/vexflow/export_slides.py
Bộ xuất bản bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 từ VexFlow Music Engine.
- Chụp ảnh snapshot bản nhạc ký âm chuẩn quốc tế và bàn phím Piano trực quan.
- Đóng gói slide PowerPoint (.pptx) và tài liệu học tập PDF (.pdf) chuẩn 16:9 qua core.pptx_engine.
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

from core.vexflow_engine import VexFlowEngine
from core.pptx_engine import package_slides


def export_vexflow_slides(
    video_dir: Path,
    scores_meta: list[dict],
    output_dir: Path = None,
    format_type: str = "all",
    base_name: str = "slides_vexflow",
) -> dict[str, Path]:
    video_dir = video_dir.resolve()
    print("============================================================")
    print("🎹 [VexFlow Slide Exporter] Xuất PowerPoint & PDF 16:9")
    print(f"   Thư mục học liệu: {video_dir}")
    print("============================================================")

    engine = VexFlowEngine(video_dir)
    results = engine.export_slides(scores_meta, output_dir, format_type, base_name)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xuất PowerPoint và PDF 16:9 từ VexFlow Music Engine")
    parser.add_argument("video_dir", nargs="?", default="output/buni-overview/video-1")
    parser.add_argument("--format", choices=["pptx", "pdf", "all"], default="all")
    parser.add_argument("--name", default="slides_vexflow")
    args = parser.parse_args()

    v_dir = Path(args.video_dir)
    if not v_dir.is_absolute():
        v_dir = WORKSPACE_ROOT / v_dir

    print("VexFlow Slide Exporter sẵn sàng nhận metadata bản nhạc.")
