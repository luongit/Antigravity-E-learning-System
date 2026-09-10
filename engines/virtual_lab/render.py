#!/usr/bin/env python3
"""
engines/virtual_lab/render.py
CLI Renderer cho Virtual Lab Engine (elearning-virtual-lab-video)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.virtual_lab_engine import VirtualLabEngine


def main():
    parser = argparse.ArgumentParser(description="Virtual Lab Engine CLI Renderer")
    parser.add_argument("video_dir", help="Đường dẫn thư mục video học liệu")
    parser.add_argument("--query", "-q", default="khúc xạ ánh sáng", help="Mô tả thí nghiệm bằng ngôn ngữ tự nhiên")
    parser.add_argument("--mode", "-m", choices=["video", "still", "html"], default="video", help="Chế độ render")
    parser.add_argument("--output", "-o", help="Tên file xuất ra")
    parser.add_argument("--duration", "-d", type=float, default=10.0, help="Thời lượng video (giây)")
    parser.add_argument("--fps", type=int, default=30, help="Khung hình/giây")
    args = parser.parse_args()

    video_dir = Path(args.video_dir).resolve()
    lab = VirtualLabEngine(video_dir)

    print(f"🔬 [Virtual Lab CLI] Xử lý yêu cầu: '{args.query}'")
    config = lab.dispatch_experiment(args.query)
    html_file = lab.generate_html(config)

    domain = config.get("domain", "lab")
    if args.mode == "html":
        print(f"🌐 Đã xuất bản trang tương tác: {html_file}")
        return

    if args.mode == "still":
        out_img = Path(args.output).resolve() if args.output else video_dir / f"slide_virtuallab_{domain}.png"
        lab.capture_still(html_file, out_img)
        print(f"📸 Đã xuất ảnh slide: {out_img}")
        return

    out_mp4 = Path(args.output).resolve() if args.output else video_dir / f"video_virtuallab_{domain}.mp4"
    lab.render_video(html_file, out_mp4, duration_sec=args.duration, fps=args.fps)
    print(f"🎬 Đã xuất video hoàn chỉnh: {out_mp4}")


if __name__ == "__main__":
    main()
