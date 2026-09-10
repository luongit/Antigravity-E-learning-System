#!/usr/bin/env python3
"""
engines/virtual_lab/export_slides.py
Bộ xuất bản bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 từ Virtual Lab Engine:
- Chụp ảnh snapshot thí nghiệm ảo (Quang học Snell, Mạch điện Ohm, Cơ học, Sóng, Điện trường).
- Đóng gói chuẩn sư phạm 16:9 tỉ lệ 1920x1080.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.pptx_engine import PPTXEngine
from core.virtual_lab_engine import VirtualLabEngine


def export_virtual_lab_slides(
    video_dir: Path | str,
    query: str = "Định luật khúc xạ ánh sáng Snell",
    base_name: str = "slides_virtual_lab",
) -> dict:
    video_dir = Path(video_dir).resolve()
    print("🔬 [Virtual Lab Slide Exporter] Xuất PowerPoint & PDF 16:9")

    lab = VirtualLabEngine(video_dir)
    config = lab.dispatch_experiment(query)
    html_file = lab.generate_html(config)

    slide_img = video_dir / f"{base_name}.png"
    lab.capture_still(html_file, slide_img, seek_ratio=0.5)

    pptx = PPTXEngine()
    title = config.get("title", "THÍ NGHIỆM ẢO KHOA HỌC (VIRTUAL LAB)")
    subtitle = config.get("subtitle", "Khảo sát hiện tượng vật lý qua mô phỏng tương tác")
    telemetry = config.get("telemetry", {})

    bullets = [f"Nguyên lý: {telemetry.get('law_name', 'Mô phỏng Khoa học')}"]
    if "formula" in telemetry:
        bullets.append(f"Công thức: {telemetry['formula']}")
    for k, v in list(telemetry.items())[:3]:
        if k not in ("law_name", "formula"):
            bullets.append(f"{k}: {v}")

    pptx.add_slide(title=title, subtitle=subtitle, image_path=slide_img, bullet_points=bullets)

    pptx_path = video_dir / f"{base_name}.pptx"
    pdf_path = video_dir / f"{base_name}.pdf"
    pptx.save_pptx(pptx_path)
    pptx.save_pdf(pdf_path)

    print(f"📦 PPTX: {pptx_path}")
    print(f"📄 PDF:  {pdf_path}")
    return {"pptx": pptx_path, "pdf": pdf_path, "image": slide_img}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xuất PowerPoint và PDF 16:9 từ Virtual Lab Engine")
    parser.add_argument("video_dir", help="Đường dẫn thư mục video học liệu")
    parser.add_argument("--query", default="khúc xạ ánh sáng", help="Nội dung bài thí nghiệm")
    parser.add_argument("--name", default="slides_virtual_lab", help="Tên file xuất ra")
    args = parser.parse_args()

    export_virtual_lab_slides(args.video_dir, query=args.query, base_name=args.name)
