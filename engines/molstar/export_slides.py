#!/usr/bin/env python3
"""
engines/molstar/export_slides.py
Bộ xuất bản bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 từ Molstar Biomolecular Engine.
- Chụp ảnh snapshot cấu trúc 3D ADN, RNA, Protein với bảng màu bazơ nitơ và thông số sinh học.
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

from core.molstar_engine import MolstarEngine
from core.pptx_engine import package_slides


def export_molstar_slides(
    video_dir: Path,
    scenes_meta: list[dict],
    output_dir: Path = None,
    format_type: str = "all",
    base_name: str = "slides_molstar",
) -> dict[str, Path]:
    video_dir = video_dir.resolve()
    print("============================================================")
    print("🧬 [Molstar Slide Exporter] Xuất PowerPoint & PDF 16:9")
    print(f"   Thư mục học liệu: {video_dir}")
    print("============================================================")

    engine = MolstarEngine(video_dir)
    results = engine.export_slides(scenes_meta, output_dir, format_type, base_name)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xuất PowerPoint và PDF 16:9 từ Molstar Engine")
    parser.add_argument("video_dir", nargs="?", default="output/buni-overview/video-1")
    parser.add_argument("--format", choices=["pptx", "pdf", "all"], default="all")
    parser.add_argument("--name", default="slides_molstar")
    args = parser.parse_args()

    v_dir = Path(args.video_dir)
    if not v_dir.is_absolute():
        v_dir = WORKSPACE_ROOT / v_dir

    print("Molstar Slide Exporter sẵn sàng nhận metadata scenes.")
