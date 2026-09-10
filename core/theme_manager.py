"""
core/theme_manager.py
Hệ thống quản lý Bộ sưu tập Theme Presets (Background, Color Palettes & Subtitle Styles)
cho video E-Learning HyperFrames & Whiteboard Animation.
Hỗ trợ 4 phong cách chuẩn:
1. light-whiteboard: Nền trắng tinh khiết, chữ tối, chuyên nghiệp, thoáng đãng (Mặc định).
2. dark-modern: Nền than chì / Slate tối, chữ sáng, sang trọng, chiều sâu.
3. ai-tech-neon: Nền gradient Xanh tím không gian, hiệu ứng Glassmorphism, chữ sáng Neon.
4. flat-editorial: Nền kem giấy mềm mại, chữ đen mực, phong cách tạp chí học thuật.
"""

import re
from typing import Dict, Any, List, Optional

THEMES: Dict[str, Dict[str, Any]] = {
    "light-whiteboard": {
        "id": "light-whiteboard",
        "name": "Light Whiteboard (Mặc định)",
        "description": "Nền trắng tinh khiết (#FFFFFF), chữ đen thanh lịch, phù hợp mọi nội dung đại cương, tổng quan và tư duy.",
        "bg_color": "#FFFFFF",
        "bg_gradient": "linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)",
        "surface_card_bg": "#FFFFFF",
        "surface_card_border": "1.5px solid #E2E8F0",
        "surface_card_shadow": "0 10px 25px rgba(22, 50, 79, 0.06)",
        "text_primary": "#1A202C",
        "text_secondary": "#4A5568",
        "text_muted": "#718096",
        "brand_badge_bg": "#16324F",
        "brand_badge_text": "#FFFFFF",
        "brand_tagline_bg": "#E6FFFA",
        "brand_tagline_text": "#007F82",
        "brand_tagline_border": "1px solid #B2F5EA",
        "accent_primary": "#16324F",
        "accent_secondary": "#007F82",
        "highlight_pill_bg": "linear-gradient(135deg, #FF7043, #F4511E)",
        "highlight_pill_text": "#FFFFFF",
        "subtitle_color": "#1A202C",
        "subtitle_font_size": "48px",
        "subtitle_font_weight": "800",
        "subtitle_text_shadow": "0 1px 3px rgba(255, 255, 255, 0.95), 0 0 15px rgba(255, 255, 255, 0.85)",
        "glassmorphism": False,
    },
    "dark-modern": {
        "id": "dark-modern",
        "name": "Dark Modern (Tối Sang trọng)",
        "description": "Nền than chì / Slate tối (#0F172A), chữ sáng, phù hợp kỹ thuật lập trình, hệ thống, DevOps, phân tích dữ liệu.",
        "bg_color": "#0F172A",
        "bg_gradient": "linear-gradient(180deg, #0F172A 0%, #1E293B 100%)",
        "surface_card_bg": "#1E293B",
        "surface_card_border": "1.5px solid #334155",
        "surface_card_shadow": "0 10px 30px rgba(0, 0, 0, 0.35)",
        "text_primary": "#F8FAFC",
        "text_secondary": "#CBD5E1",
        "text_muted": "#94A3B8",
        "brand_badge_bg": "#38BDF8",
        "brand_badge_text": "#0F172A",
        "brand_tagline_bg": "rgba(56, 189, 248, 0.15)",
        "brand_tagline_text": "#38BDF8",
        "brand_tagline_border": "1px solid rgba(56, 189, 248, 0.3)",
        "accent_primary": "#38BDF8",
        "accent_secondary": "#F59E0B",
        "highlight_pill_bg": "linear-gradient(135deg, #F59E0B, #D97706)",
        "highlight_pill_text": "#0F172A",
        "subtitle_color": "#F8FAFC",
        "subtitle_font_size": "48px",
        "subtitle_font_weight": "800",
        "subtitle_text_shadow": "0 2px 6px rgba(0, 0, 0, 0.9), 0 0 20px rgba(0, 0, 0, 0.8)",
        "glassmorphism": False,
    },
    "ai-tech-neon": {
        "id": "ai-tech-neon",
        "name": "AI Tech Neon (Cyber / Không gian số)",
        "description": "Nền gradient Xanh tím huyền ảo, hiệu ứng kính mờ Glassmorphism, điểm nhấn Neon Cyan & Violet. Phù hợp chuyên ngành AI, Robotics, Data Science.",
        "bg_color": "#0B0F19",
        "bg_gradient": "radial-gradient(ellipse at 80% 20%, rgba(168, 85, 247, 0.15) 0%, transparent 50%), radial-gradient(ellipse at 20% 80%, rgba(0, 245, 255, 0.12) 0%, transparent 50%), linear-gradient(135deg, #0B0F19 0%, #131B2E 50%, #1E1B4B 100%)",
        "surface_card_bg": "rgba(19, 27, 46, 0.75)",
        "surface_card_border": "1px solid rgba(0, 245, 255, 0.25)",
        "surface_card_shadow": "0 12px 35px rgba(0, 0, 0, 0.4), 0 0 15px rgba(0, 245, 255, 0.1)",
        "text_primary": "#FFFFFF",
        "text_secondary": "#E2E8F0",
        "text_muted": "#94A3B8",
        "brand_badge_bg": "linear-gradient(135deg, #00F5FF, #3B82F6)",
        "brand_badge_text": "#0B0F19",
        "brand_tagline_bg": "rgba(168, 85, 247, 0.2)",
        "brand_tagline_text": "#C084FC",
        "brand_tagline_border": "1px solid rgba(168, 85, 247, 0.4)",
        "accent_primary": "#00F5FF",
        "accent_secondary": "#A855F7",
        "highlight_pill_bg": "linear-gradient(135deg, #00F5FF, #0284C7)",
        "highlight_pill_text": "#0B0F19",
        "subtitle_color": "#F0FDF4",
        "subtitle_font_size": "48px",
        "subtitle_font_weight": "800",
        "subtitle_text_shadow": "0 2px 8px rgba(0, 0, 0, 0.95), 0 0 25px rgba(0, 245, 255, 0.35)",
        "glassmorphism": True,
    },
    "flat-editorial": {
        "id": "flat-editorial",
        "name": "Flat Editorial (Ấm áp / Học thuật)",
        "description": "Nền kem giấy mềm mại (#FAF8F5), chữ đen than dứt khoát, phong cách tạp chí tri thức. Phù hợp kinh doanh, khởi nghiệp, marketing, kỹ năng mềm.",
        "bg_color": "#FAF8F5",
        "bg_gradient": "linear-gradient(180deg, #FAF8F5 0%, #F5F1EB 100%)",
        "surface_card_bg": "#FFFFFF",
        "surface_card_border": "1.5px solid #E7E0D8",
        "surface_card_shadow": "0 8px 24px rgba(69, 26, 3, 0.05)",
        "text_primary": "#1C1917",
        "text_secondary": "#44403C",
        "text_muted": "#78716C",
        "brand_badge_bg": "#BE123C",
        "brand_badge_text": "#FFFFFF",
        "brand_tagline_bg": "#F0FDF4",
        "brand_tagline_text": "#15803D",
        "brand_tagline_border": "1px solid #BBF7D0",
        "accent_primary": "#BE123C",
        "accent_secondary": "#15803D",
        "highlight_pill_bg": "linear-gradient(135deg, #BE123C, #9F1239)",
        "highlight_pill_text": "#FFFFFF",
        "subtitle_color": "#1C1917",
        "subtitle_font_size": "48px",
        "subtitle_font_weight": "800",
        "subtitle_text_shadow": "0 1px 3px rgba(250, 248, 245, 0.95), 0 0 15px rgba(250, 248, 245, 0.85)",
        "glassmorphism": False,
    }
}

DEFAULT_THEME_ID = "light-whiteboard"


def get_theme(theme_id: Optional[str] = None) -> Dict[str, Any]:
    """Lấy thông tin cấu hình của một theme theo ID, fallback về default nếu không khớp."""
    if not theme_id:
        return THEMES[DEFAULT_THEME_ID]
    tid = theme_id.strip().lower()
    return THEMES.get(tid, THEMES[DEFAULT_THEME_ID])


def list_themes() -> List[Dict[str, str]]:
    """Liệt kê danh sách các theme có sẵn kèm mô tả ngắn."""
    return [
        {
            "id": t["id"],
            "name": t["name"],
            "description": t["description"],
            "bg_color": t["bg_color"],
            "subtitle_color": t["subtitle_color"]
        }
        for t in THEMES.values()
    ]


def detect_recommended_theme(script_text: str) -> str:
    """
    Tự động phân tích nội dung kịch bản để gợi ý Theme phù hợp:
    - Nếu nhiều từ khóa AI, Robot, Neural, Machine Learning -> ai-tech-neon
    - Nếu nhiều từ khóa Code, Lập trình, SQL, Docker, Database, System -> dark-modern
    - Nếu nhiều từ khóa Kinh doanh, Khởi nghiệp, Marketing, Quản trị, Kỹ năng -> flat-editorial
    - Mặc định: light-whiteboard
    """
    if not script_text:
        return DEFAULT_THEME_ID

    text = script_text.lower()

    ai_keywords = [
        "trí tuệ nhân tạo", "ai", "machine learning", "deep learning", "llm",
        "robot", "robotics", "neural network", "agent", "prompt", "rag",
        "generative", "vision", "tự động hóa thông minh"
    ]
    code_keywords = [
        "lập trình", "source code", "backend", "frontend", "api", "database",
        "sql", "docker", "kubernetes", "debug", "compiler", "git", "framework",
        "cloud", "server", "kiến trúc phần mềm"
    ]
    business_keywords = [
        "kinh doanh", "doanh nghiệp", "khởi nghiệp", "marketing", "quản trị",
        "kpi", "doanh thu", "lợi nhuận", "chiến lược", "kỹ năng mềm",
        "tư duy", "lãnh đạo", "giao tiếp"
    ]

    ai_score = sum(len(re.findall(rf"\b{re.escape(kw)}\b", text)) for kw in ai_keywords)
    code_score = sum(len(re.findall(rf"\b{re.escape(kw)}\b", text)) for kw in code_keywords)
    biz_score = sum(len(re.findall(rf"\b{re.escape(kw)}\b", text)) for kw in business_keywords)

    if ai_score >= 4 and ai_score >= code_score:
        return "ai-tech-neon"
    if code_score >= 4 and code_score > biz_score:
        return "dark-modern"
    if biz_score >= 4:
        return "flat-editorial"

    return DEFAULT_THEME_ID


def generate_theme_css(theme_id: Optional[str] = None) -> str:
    """Sinh khối CSS định nghĩa biến toàn cục (:root) và các class style của theme."""
    t = get_theme(theme_id)

    glass_css = ""
    if t.get("glassmorphism", False):
        glass_css = """
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
"""

    css = f"""
    /* Theme Variables: {t['name']} */
    :root {{
      --bg-color: {t['bg_color']};
      --bg-gradient: {t['bg_gradient']};
      --surface-card-bg: {t['surface_card_bg']};
      --surface-card-border: {t['surface_card_border']};
      --surface-card-shadow: {t['surface_card_shadow']};
      --text-primary: {t['text_primary']};
      --text-secondary: {t['text_secondary']};
      --text-muted: {t['text_muted']};
      --brand-badge-bg: {t['brand_badge_bg']};
      --brand-badge-text: {t['brand_badge_text']};
      --brand-tagline-bg: {t['brand_tagline_bg']};
      --brand-tagline-text: {t['brand_tagline_text']};
      --brand-tagline-border: {t['brand_tagline_border']};
      --accent-primary: {t['accent_primary']};
      --accent-secondary: {t['accent_secondary']};
      --highlight-pill-bg: {t['highlight_pill_bg']};
      --highlight-pill-text: {t['highlight_pill_text']};
      --subtitle-color: {t['subtitle_color']};
      --subtitle-font-size: {t['subtitle_font_size']};
      --subtitle-font-weight: {t['subtitle_font_weight']};
      --subtitle-text-shadow: {t['subtitle_text_shadow']};
    }}

    body {{
      background: var(--bg-gradient);
      color: var(--text-primary);
    }}

    .card {{
      background: var(--surface-card-bg);
      border: var(--surface-card-border);
      box-shadow: var(--surface-card-shadow);
      border-radius: 16px;{glass_css}
    }}

    .brand-badge {{
      background: var(--brand-badge-bg);
      color: var(--brand-badge-text);
      font-weight: 800;
      font-size: 18px;
      padding: 6px 14px;
      border-radius: 6px;
    }}

    .brand-collab {{
      color: var(--text-secondary);
      font-weight: 600;
      font-size: 16px;
    }}

    .brand-tagline {{
      background: var(--brand-tagline-bg);
      color: var(--brand-tagline-text);
      border: var(--brand-tagline-border);
      font-size: 15px;
      font-weight: 700;
      padding: 6px 16px;
      border-radius: 20px;
    }}

    .highlight-pill {{
      background: var(--highlight-pill-bg);
      color: var(--highlight-pill-text);
      font-weight: 700;
      border-radius: 8px;
      padding: 8px 16px;
      display: inline-block;
    }}

    #subtitle-text {{
      font-size: var(--subtitle-font-size);
      font-weight: var(--subtitle-font-weight);
      color: var(--subtitle-color);
      text-shadow: var(--subtitle-text-shadow);
      line-height: 1.3;
      max-width: 1700px;
      letter-spacing: -0.3px;
    }}
"""
    return css
