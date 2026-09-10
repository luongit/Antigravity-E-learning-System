#!/usr/bin/env python3
"""
engines/opencv/render.py
Bộ điều phối trung tâm của Engine OpenCV Whiteboard Animation.
- Đọc ảnh slide từ output/<ma-mon-hoc>/video-<x>/images/slide-<x>.png
- Đọc audio và SRT từ output/<ma-mon-hoc>/video-<x>/mp3/mp3-<x>.*
- Render video Whiteboard 2 pha: Nét vẽ chì phác thảo (Canny) + bàn tay vẽ -> Tô màu dần (Color Reveal)
- Đồng bộ phụ đề Subtitle 48px Be Vietnam Pro Bold không viền đen
- Mux âm thanh xuất thẳng tệp MP4 vào thư mục học liệu đích
"""

import argparse
import math
import subprocess
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.whiteboard_engine import (
    create_sketch_image,
    apply_sketch_to_color_reveal,
    draw_subtitle,
    get_hand_image,
    OUT_W,
    OUT_H,
)
from core.hf_engine import parse_srt, get_audio_duration


def render_opencv_scene(video_dir: Path, scene_num: int, output_file: Path = None):
    video_dir = video_dir.resolve()
    print(f"\n============================================================")
    print(f"✏️ [OpenCV Whiteboard Engine] Render Cảnh {scene_num}")
    print(f"   Thư mục nguồn: {video_dir}")
    print(f"============================================================")

    img_dir = video_dir / "images"
    audio_dir = video_dir / "mp3"

    # Tìm file ảnh slide
    img_candidates = [
        img_dir / f"slide-{scene_num}.png",
        img_dir / f"slide-{scene_num}.jpg",
        img_dir / f"slide_{scene_num}.png",
        img_dir / f"slide_{scene_num}.jpg",
    ]
    img_path = next((p for p in img_candidates if p.exists()), None)
    if not img_path:
        print(f"❌ Không tìm thấy ảnh slide cho cảnh {scene_num} trong {img_dir}")
        sys.exit(1)

    mp3_path = audio_dir / f"mp3-{scene_num}.mp3"
    srt_path = audio_dir / f"mp3-{scene_num}.srt"

    if not mp3_path.exists():
        print(f"❌ Không tìm thấy file âm thanh: {mp3_path}")
        sys.exit(1)

    duration_sec = get_audio_duration(mp3_path)
    fps = 30
    total_frames = int(round(duration_sec * fps))
    print(f"🖼️ Ảnh slide: {img_path.name}")
    print(f"⏱️ Thời lượng audio: {duration_sec:.2f}s ({total_frames} frames @ {fps}fps)")

    # 1. Đọc và chuẩn hóa ảnh gốc về 1920x1080
    raw_img = Image.open(img_path).convert("RGB")
    if raw_img.size != (OUT_W, OUT_H):
        raw_img = raw_img.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)

    # 2. Tạo ảnh nét vẽ chì Canny Edge
    print("🎨 Đang sinh nét vẽ chì phác thảo (Canny Edge)...")
    sketch_img = create_sketch_image(raw_img)

    # 3. Phân tích SRT
    subtitles = parse_srt(srt_path)
    print(f"📝 Đã nạp {len(subtitles)} đoạn phụ đề SRT")

    # 3.1. Thiết lập danh sách Cutaways ngữ nghĩa theo quy chuẩn chung
    cutaways = []
    if scene_num == 1:
        cutaways = [
            {
                "videoFile": "office_intro.mp4",
                "startSec": 16.581,
                "endSec": 30.447,
                "label": "BỐI CẢNH KINH TẾ SỐ & NHU CẦU NHÂN LỰC THỰC CHIẾN",
            }
        ]
    elif scene_num == 2:
        cutaways = [
            {
                "videoFile": "office_intro.mp4",
                "startSec": 0.0,
                "endSec": 7.46,
                "label": "BỐI CẢNH & ĐỊNH HƯỚNG NGHỀ NGHIỆP",
            }
        ]

    # Mở sẵn VideoCapture cho các video B-roll cutaways
    cutaway_caps = {}
    for c in cutaways:
        v_name = c["videoFile"]
        v_path = WORKSPACE_ROOT / "inputs" / "video-libraries" / v_name
        if not v_path.exists():
            v_path = (
                WORKSPACE_ROOT
                / "inputs"
                / "video-libraries"
                / "video chủ đề văn phòng"
                / "7154210-hd_1920_1080_25fps.mp4"
            )
        if v_path.exists():
            cap = cv2.VideoCapture(str(v_path))
            cutaway_caps[v_name] = {
                "cap": cap,
                "total_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "fps": cap.get(cv2.CAP_PROP_FPS) or 30.0,
            }
            print(f"🎥 Đã nạp video B-roll cutaway: {v_path.name}")

    if not output_file:
        output_file = video_dir / f"test_opencv_scene{scene_num}.mp4"
    output_file = output_file.resolve()

    temp_video = video_dir / f"temp_opencv_{scene_num}.mp4"

    # 4. Render từng frame bằng OpenCV VideoWriter
    print(f"🚀 Đang render {total_frames} frames hoạt họa Whiteboard & B-roll Cutaway...")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(temp_video), fourcc, fps, (OUT_W, OUT_H))

    # Bố cục diễn hoạt 2 vùng:
    # Vùng 1: Ảnh minh họa mỏ neo bên trái (x: 0 -> 900)
    # Vùng 2: Khối tiêu đề và nội dung bên phải (x: 900 -> 1920)
    box_left = (40, 100, 880, 980)
    box_right = (880, 80, 1880, 980)

    for i in range(total_frames):
        t_curr = i / fps

        # A. Kiểm tra nếu đang trong khoảng Cutaway B-roll toàn màn hình
        active_cutaway = next(
            (c for c in cutaways if c["startSec"] <= t_curr <= c["endSec"]), None
        )
        if active_cutaway and active_cutaway["videoFile"] in cutaway_caps:
            c_info = cutaway_caps[active_cutaway["videoFile"]]
            cap = c_info["cap"]
            dt = t_curr - active_cutaway["startSec"]
            broll_fps = c_info["fps"]
            total_broll_frames = max(1, c_info["total_frames"])
            frame_idx = int(dt * broll_fps) % total_broll_frames

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, b_frame = cap.read()
            if ret:
                # Resize về 1920x1080 cover
                b_frame = cv2.resize(b_frame, (OUT_W, OUT_H), interpolation=cv2.INTER_LINEAR)
                frame = Image.fromarray(cv2.cvtColor(b_frame, cv2.COLOR_BGR2RGB))

                # Lớp scrim gradient tối mờ ở đỉnh và đáy
                draw = ImageDraw.Draw(frame)
                # Dải gradient mờ đỉnh & đáy
                draw.rectangle([(0, 0), (OUT_W, 140)], fill=(15, 23, 42))
                draw.rectangle([(0, OUT_H - 180), (OUT_W, OUT_H)], fill=(15, 23, 42))
                # Phủ bán trong suốt bằng blend
                dim_overlay = Image.new("RGB", (OUT_W, OUT_H), (15, 23, 42))
                frame = Image.blend(frame, dim_overlay, 0.25)

                # Vẽ Status Badge góc trên bên trái
                badge_text = active_cutaway.get("label", "BỐI CẢNH THỰC TẾ")
                from core.whiteboard_engine import get_bold_font
                font_badge = get_bold_font(15)
                draw = ImageDraw.Draw(frame)
                bx, by = 60, 48
                draw.rounded_rectangle(
                    [(bx, by), (bx + 540, by + 42)],
                    radius=20,
                    fill=(15, 23, 42),
                    outline=(56, 189, 248),
                    width=2,
                )
                draw.ellipse([(bx + 16, by + 16), (bx + 26, by + 26)], fill=(56, 189, 248))
                draw.text((bx + 36, by + 11), badge_text, font=font_badge, fill=(56, 189, 248))

                # Phụ đề chữ trắng sáng (#F8FAFC) trên nền video B-roll tối
                active_sub = next(
                    (s["text"] for s in subtitles if s["startSec"] <= t_curr <= s["endSec"]), None
                )
                if active_sub:
                    draw_subtitle(frame, active_sub, font_size=46, text_color=(248, 250, 252))

                arr_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                writer.write(arr_bgr)

                if i % 150 == 0 or i == total_frames - 1:
                    prog = int((i + 1) / total_frames * 100)
                    print(f"   Tiến độ: {prog}% ({i+1}/{total_frames} frames)")
                continue

        # B. Ngoài Cutaway: Hoạt họa Whiteboard nét vẽ bảng trắng trên nền sáng
        frame = Image.new("RGB", (OUT_W, OUT_H), (255, 255, 255))

        # Pha 1: Vẽ mỏ neo bên trái (0.0s -> 2.5s)
        apply_sketch_to_color_reveal(
            frame, raw_img, sketch_img, box_left, t_curr, t_start=0.0, sketch_dur=1.8, color_dur=0.6
        )

        # Pha 2: Vẽ nội dung chữ và khối bên phải (1.5s -> 4.2s)
        apply_sketch_to_color_reveal(
            frame, raw_img, sketch_img, box_right, t_curr, t_start=1.5, sketch_dur=2.0, color_dur=0.7
        )

        # Nếu sau 4.2s: Giữ nguyên ảnh slide hoàn chỉnh
        if t_curr >= 4.2:
            frame.paste(raw_img, (0, 0))

        # Phụ đề đáy theo SRT: Chữ đen (#1A202C) trên nền slide sáng
        active_sub = next(
            (s["text"] for s in subtitles if s["startSec"] <= t_curr <= s["endSec"]), None
        )
        if active_sub:
            draw_subtitle(frame, active_sub, font_size=46, text_color=(26, 32, 44))

        # Chuyển sang mảng OpenCV BGR để ghi frame
        arr_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        writer.write(arr_bgr)

        if i % 150 == 0 or i == total_frames - 1:
            prog = int((i + 1) / total_frames * 100)
            print(f"   Tiến độ: {prog}% ({i+1}/{total_frames} frames)")

    # Giải phóng VideoCapture
    for c_info in cutaway_caps.values():
        c_info["cap"].release()

    writer.release()
    print("🎬 Render khung hình hoàn tất. Đang ghép âm thanh...")

    # 5. Ghép âm thanh AAC bằng FFmpeg
    mux_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(temp_video),
        "-i",
        str(mp3_path),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(output_file),
    ]
    mux_res = subprocess.run(mux_cmd, capture_output=True, text=True)

    if temp_video.exists():
        temp_video.unlink()

    if mux_res.returncode == 0 and output_file.exists():
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"\n✅ OPENCV RENDER THÀNH CÔNG!")
        print(f"   Tệp sản phẩm: {output_file} ({size_mb:.1f} MB)")
    else:
        print(f"❌ Mux FFmpeg thất bại:\n{mux_res.stderr}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="OpenCV Whiteboard Video Renderer")
    parser.add_argument("video_dir", nargs="?", default="output/buni-overview/video-1")
    parser.add_argument("--scene", type=int, default=1, help="Số thứ tự cảnh cần render")
    parser.add_argument("--output", type=str, default=None, help="Đường dẫn file MP4 đầu ra")
    args = parser.parse_args()

    v_dir = Path(args.video_dir)
    if not v_dir.is_absolute():
        v_dir = WORKSPACE_ROOT / v_dir

    out_p = Path(args.output) if args.output else None
    render_opencv_scene(v_dir, args.scene, out_p)


if __name__ == "__main__":
    main()
