"""Module hỗ trợ Subtitle Be Vietnam Pro chữ đen không viền và hiệu ứng Hand-Drawing & Paper Cut-out."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT_DIR / "assets" / "fonts" / "BeVietnamPro-SemiBold.ttf"
HAND_PATH = ROOT_DIR / "assets" / "drawing-hand.png"

OUT_W, OUT_H = 1920, 1080

# Nạp font và ảnh bàn tay sẵn
_FONT_CACHE = {}
def get_font(size: int = 30):
    if size not in _FONT_CACHE:
        _FONT_CACHE[size] = ImageFont.truetype(str(FONT_PATH), size)
    return _FONT_CACHE[size]

_HAND_IMG = None
def get_hand_image(scale: float = 0.70) -> Image.Image:
    global _HAND_IMG
    if _HAND_IMG is None:
        raw = Image.open(HAND_PATH).convert("RGBA")
        hw, hh = int(raw.width * scale), int(raw.height * scale)
        _HAND_IMG = raw.resize((hw, hh), Image.Resampling.LANCZOS)
    return _HAND_IMG


def draw_subtitle_on_frame(frame: Image.Image, text: str, font_size: int = 48):
    """Vẽ phụ đề không nền, chữ màu đen (#1A202C) sắc nét, không viền, căn giữa ở đáy màn hình."""
    if not text or not text.strip():
        return
    draw = ImageDraw.Draw(frame)
    font = get_font(font_size)

    # Wrap text nếu quá dài (> 1550px)
    words = text.strip().split()
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bbox = font.getbbox(test)
        if (bbox[2] - bbox[0]) > 1550 and curr:
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
        # Chữ màu đen, không viền stroke
        draw.text((x, y), line, font=font, fill=(26, 32, 44))


def ease_out_cubic(x: float) -> float:
    return 1.0 - math.pow(1.0 - max(0.0, min(1.0, x)), 3)


def ease_out_back(x: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * math.pow(x - 1.0, 3) + c1 * math.pow(x - 1.0, 2)


def render_paper_cutout(crop: Image.Image, border_width: int = 3, shadow_blur: int = 5) -> tuple[Image.Image, int, int]:
    """Tạo hiệu ứng cắt dán từng mảnh: viền sticker mảnh và bóng đổ mềm."""
    w, h = crop.size
    pad = shadow_blur * 2 + border_width + 4
    canvas_w, canvas_h = w + pad * 2, h + pad * 2

    # Drop shadow
    shadow_mask = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_mask)
    s_draw.rectangle([pad + 2, pad + 5, pad + w - 2, pad + h + 2], fill=(0, 0, 0, 70))
    shadow = shadow_mask.filter(ImageFilter.GaussianBlur(shadow_blur))

    # Viền sticker trắng mảnh
    sticker = shadow.copy()
    st_draw = ImageDraw.Draw(sticker)
    st_draw.rectangle([pad - border_width, pad - border_width, pad + w + border_width, pad + h + border_width], 
                      fill=(255, 255, 255, 255), outline=(225, 225, 225, 255), width=1)
    sticker.paste(crop, (pad, pad))
    return sticker, pad, pad


def apply_hand_drawing_to_crop(frame: Image.Image, crop: Image.Image, box: tuple, progress: float):
    """Tiết lộ nét vẽ kết hợp bàn tay vẽ theo tiến trình progress [0..1].
    Sau khi progress >= 1.0, bàn tay lướt ra ngoài."""
    x0, y0, x1, y1 = box
    w, h = crop.size

    prog_clamped = max(0.0, min(1.0, progress))
    # Tiết lộ theo đường quét chéo từ góc trên trái xuống dưới phải
    # Tạo alpha mask dựa trên khoảng cách (x + y)
    diag = w + h
    curr_diag = diag * ease_out_cubic(prog_clamped)

    # Cắt phần hiển thị bằng mặt nạ
    if prog_clamped >= 1.0:
        frame.paste(crop, (x0, y0))
        # Bàn tay trượt ra ngoài
        exit_prog = min(1.0, (progress - 1.0) / 0.3)
        if exit_prog < 1.0:
            hand = get_hand_image()
            hx = int(round(x1 + exit_prog * 400))
            hy = int(round(y1 + exit_prog * 400))
            frame.paste(hand, (hx, hy), hand)
        return

    # Tạo mask tiết lộ
    # Đơn giản hoá: tiết lộ theo chiều dọc (wipe_y)
    vis_h = max(1, int(round(h * prog_clamped)))
    part = crop.crop((0, 0, w, vis_h))
    frame.paste(part, (x0, y0))

    # Đặt ngòi bút tại vị trí đang vẽ
    hand = get_hand_image()
    tip_x, tip_y = 1, 1
    # Bút vẽ lượn sóng zic-zac theo chiều ngang khi quét xuống
    sweep_x = int(w * (0.5 + 0.4 * math.sin(progress * math.pi * 6)))
    hx = x0 + sweep_x - tip_x
    hy = y0 + vis_h - tip_y
    frame.paste(hand, (hx, hy), hand)
