"""
core/whiteboard_engine.py
Động cơ Whiteboard Sketch Animation Lõi:
1. Tạo ảnh nét chì phác thảo (Pencil Sketch Outline) trên nền trắng tinh khiết bằng Canny edge + Dilation.
2. Diễn hoạt 2 pha: Nét chì phác thảo (Outline) -> Tô màu dần (Color Fade-in).
3. Bàn tay cầm bút hoạt họa (Drawing Hand Overlay) bám sát nét vẽ với gia tốc tự nhiên (ease_out_cubic).
4. Vẽ Subtitle 48px Be Vietnam Pro Bold chữ màu đen (#1A202C) thanh lịch, không viền, không nền che tranh, căn giữa ở đáy màn hình.
"""

import math
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT_DIR / "assets" / "fonts" / "BeVietnamPro-Bold.ttf"
HAND_PATH = ROOT_DIR / "assets" / "drawing-hand.png"

OUT_W, OUT_H = 1920, 1080

_FONT_CACHE = {}
def get_bold_font(size: int = 42) -> ImageFont.FreeTypeFont:
    if size not in _FONT_CACHE:
        if FONT_PATH.exists():
            _FONT_CACHE[size] = ImageFont.truetype(str(FONT_PATH), size)
        else:
            _FONT_CACHE[size] = ImageFont.load_default()
    return _FONT_CACHE[size]

_HAND_IMG = None
def get_hand_image(scale: float = 0.60) -> Image.Image:
    global _HAND_IMG
    if _HAND_IMG is None:
        if HAND_PATH.exists():
            raw = Image.open(HAND_PATH).convert("RGBA")
            hw, hh = int(raw.width * scale), int(raw.height * scale)
            _HAND_IMG = raw.resize((hw, hh), Image.Resampling.LANCZOS)
        else:
            # Fallback nếu thiếu file tay vẽ
            _HAND_IMG = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    return _HAND_IMG

def ease_out_cubic(x: float) -> float:
    return 1.0 - math.pow(1.0 - max(0.0, min(1.0, x)), 3)

def create_sketch_image(img_pil: Image.Image) -> Image.Image:
    """Tạo ảnh nét chì đen trên nền trắng tinh khiết từ ảnh gốc."""
    arr = np.array(img_pil)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 130)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    sketch_arr = np.full_like(gray, 255)
    sketch_arr[dilated > 0] = 35  # Nét chì đen xám
    sketch_rgb = cv2.cvtColor(sketch_arr, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(sketch_rgb)

def draw_subtitle(frame: Image.Image, text: str, font_size: int = 48, text_color: tuple = (26, 32, 44)):
    """Vẽ phụ đề 48px to rõ, font Be Vietnam Pro ExtraBold, không viền lem luốc, căn giữa ở đáy màn hình."""
    if not text or not text.strip():
        return
    draw = ImageDraw.Draw(frame)
    font = get_bold_font(font_size)

    # Wrap nếu dài hơn 1600px
    words = text.strip().split()
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bbox = font.getbbox(test)
        if (bbox[2] - bbox[0]) > 1600 and curr:
            lines.append(" ".join(curr))
            curr = [w]
        else:
            curr.append(w)
    if curr:
        lines.append(" ".join(curr))

    line_h = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] + 12
    total_h = len(lines) * line_h
    y_start = OUT_H - 45 - total_h

    for idx, line in enumerate(lines):
        bbox = font.getbbox(line)
        lw = bbox[2] - bbox[0]
        x = (OUT_W - lw) // 2
        y = y_start + idx * line_h
        
        # Nếu là chữ trắng (trên nền video cutaway), thêm bóng đổ drop shadow mềm
        if text_color[0] > 200 and text_color[1] > 200 and text_color[2] > 200:
            draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, 180))
            draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 100))
        draw.text((x, y), line, font=font, fill=text_color)

draw_subtitle_42px = draw_subtitle

def apply_sketch_to_color_reveal(
    frame: Image.Image,
    img_color: Image.Image,
    img_sketch: Image.Image,
    box: tuple,
    t_curr: float,
    t_start: float,
    sketch_dur: float = 1.0,
    color_dur: float = 0.4
):
    """Diễn hoạt vùng ảnh: Nét chì phác thảo (Outline) -> Tô màu dần (Color Fill)."""
    if t_curr < t_start:
        return

    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    dt = t_curr - t_start

    # Giai đoạn 1: Nét chì phác thảo kèm bàn tay vẽ
    if dt < sketch_dur:
        prog = ease_out_cubic(dt / sketch_dur)
        vis_h = max(1, int(round(bh * prog)))
        sketch_part = img_sketch.crop((x0, y0, x1, y0 + vis_h))
        frame.paste(sketch_part, (x0, y0))

        hand = get_hand_image()
        sweep_x = int(bw * (0.5 + 0.35 * math.sin(prog * math.pi * 8)))
        hx = x0 + sweep_x - 1
        hy = y0 + vis_h - 1
        hx = max(0, min(OUT_W - hand.width, hx))
        hy = max(0, min(OUT_H - hand.height, hy))
        frame.paste(hand, (hx, hy), hand)

    # Giai đoạn 2: Tô màu dần
    elif dt < (sketch_dur + color_dur):
        color_prog = (dt - sketch_dur) / color_dur
        sketch_part = img_sketch.crop((x0, y0, x1, y1))
        color_part = img_color.crop((x0, y0, x1, y1))
        blended = Image.blend(sketch_part, color_part, color_prog)
        frame.paste(blended, (x0, y0))

        exit_prog = color_prog
        hand = get_hand_image()
        hx = int(round(x1 - 50 + exit_prog * 350))
        hy = int(round(y1 - 50 + exit_prog * 350))
        if hx < OUT_W and hy < OUT_H:
            frame.paste(hand, (hx, hy), hand)

    # Giai đoạn 3: Giữ nguyên màu gốc hoàn thiện
    else:
        frame.paste(img_color.crop((x0, y0, x1, y1)), (x0, y0))
