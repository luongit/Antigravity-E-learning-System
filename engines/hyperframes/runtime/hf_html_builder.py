#!/usr/bin/env python3
"""
engines/hyperframes/runtime/hf_html_builder.py
Inject HF Scene Spec vào Master HTML Template
- Resolve paths thành absolute (cho Puppeteer offline)
- Inline SRT data vào spec
- Inject __HF_SPEC__ và __HF_SILENT_MODE__ vào HTML
"""

from __future__ import annotations

import json
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATE_PATH = WORKSPACE_ROOT / "assets" / "templates" / "hf_scene_template.html"


def _resolve_asset_path(src: str, video_dir: Path, workspace_root: Path) -> str:
    """
    Resolve đường dẫn tài nguyên thành URL file:// hoặc absolute path.
    Ưu tiên: video_dir → workspace_root → giữ nguyên.
    """
    if not src:
        return src
    if src.startswith(("http://", "https://", "file://", "data:")):
        return src

    candidates = [
        (video_dir / src).resolve(),
        (workspace_root / src).resolve(),
        Path(src).resolve(),
    ]
    for c in candidates:
        if c.exists():
            # Trả về URL file:// tuyệt đối (Windows-safe)
            return c.resolve().as_uri()
    return src  # Giữ nguyên nếu không tìm thấy



def _resolve_spec_paths(spec: dict, video_dir: Path, workspace_root: Path) -> dict:
    """Duyệt spec và resolve tất cả path tài nguyên."""
    spec_str = json.dumps(spec, ensure_ascii=False)

    # Tìm tất cả string có dạng đường dẫn file
    path_pattern = re.compile(r'"((?:[^"]*/)(?:[^"]+\.(?:mp3|mp4|srt|png|jpg|jpeg|svg|webm|ogg|woff2|ttf)))"')

    def replace_path(m):
        raw = m.group(1)
        resolved = _resolve_asset_path(raw, video_dir, workspace_root)
        return f'"{resolved}"'

    spec_str = path_pattern.sub(replace_path, spec_str)
    return json.loads(spec_str)


def _load_srt(srt_path_raw: str, video_dir: Path, workspace_root: Path) -> list[dict]:
    """Load và parse SRT file thành array objects."""
    candidates = [
        video_dir / srt_path_raw,
        workspace_root / srt_path_raw,
    ]
    srt_file = next((c for c in candidates if c.exists()), None)
    if not srt_file:
        return []

    content = srt_file.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(\d+)\s*\n"
        r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n"
        r"([\s\S]*?)(?=\n\d+\s*\n|\n*$)",
        re.MULTILINE,
    )
    items = []
    for m in pattern.finditer(content):
        def to_sec(t: str) -> float:
            h, mn, s = t.replace(",", ".").split(":")
            return float(h) * 3600 + float(mn) * 60 + float(s)

        items.append({
            "id": int(m.group(1)),
            "startSec": to_sec(m.group(2)),
            "endSec": to_sec(m.group(3)),
            "text": m.group(4).replace("\r\n", " ").replace("\n", " ").strip(),
        })
    return items


def _resolve_component_paths(html: str, workspace_root: Path) -> str:
    """
    Thay thế đường dẫn relative của hf_components trong HTML template
    thành đường dẫn file:// tuyệt đối để Puppeteer load được offline.
    """
    components_dir = workspace_root / "assets" / "templates" / "hf_components"
    component_files = [
        "spring_engine.js", "timeline_engine.js", "kinetic_typography.js",
        "subtitle_engine.js", "audio_manager.js", "broll_controller.js",
        "code_studio.js", "visual_anchors.js",
    ]
    for fname in component_files:
        fpath = components_dir / fname
        if fpath.exists():
            html = html.replace(
                f"../../assets/templates/hf_components/{fname}",
                fpath.as_uri(),
            )
    return html


def build_html(
    spec: dict,
    video_dir: Path,
    template_path: Path = None,
    silent_mode: bool = True,
    workspace_root: Path = None,
) -> str:
    """
    Tạo HTML string đầy đủ từ HF Scene Spec và template.

    Args:
        spec: HF Scene Spec v2 dict
        video_dir: Thư mục video (để resolve đường dẫn tương đối)
        template_path: Đường dẫn tới hf_scene_template.html (mặc định WORKSPACE/assets/templates/)
        silent_mode: True khi render bằng Puppeteer (audio không phát)
        workspace_root: Thư mục gốc workspace
    Returns:
        str — HTML đầy đủ sẵn sàng cho Puppeteer
    """
    ws_root = workspace_root or WORKSPACE_ROOT
    tpl_path = template_path or TEMPLATE_PATH
    html = tpl_path.read_text(encoding="utf-8")

    # Resolve component paths thành absolute
    html = _resolve_component_paths(html, ws_root)

    # Load SRT data
    srt_items = []
    for audio_track in spec.get("globalAudio", []):
        if audio_track.get("srt"):
            srt_items.extend(_load_srt(audio_track["srt"], video_dir, ws_root))

    # Sort SRT
    srt_items.sort(key=lambda x: x["startSec"])

    # Resolve asset paths trong spec
    resolved_spec = _resolve_spec_paths(spec, video_dir, ws_root)
    resolved_spec["_srtItems"] = srt_items

    # Inject spec vào HTML trước </body>
    spec_json = json.dumps(resolved_spec, ensure_ascii=False, indent=None)
    injection = f"""
<script>
  window.__HF_SPEC__ = {spec_json};
  window.__HF_SILENT_MODE__ = {'true' if silent_mode else 'false'};
</script>
"""
    html = html.replace("</body>", injection + "\n</body>")
    return html


def save_html(
    spec: dict,
    video_dir: Path,
    output_path: Path,
    silent_mode: bool = True,
    workspace_root: Path = None,
) -> Path:
    """Build HTML và lưu file."""
    html = build_html(spec, video_dir, silent_mode=silent_mode, workspace_root=workspace_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
