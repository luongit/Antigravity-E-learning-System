#!/usr/bin/env python3
"""
engines/hyperframes/runtime/hf_scene_builder.py
Agent-friendly HyperFrames Scene Spec v2 Builder & Validator

API:
    builder = HFSceneBuilder()
    builder.set_meta(title="Bài Giảng", fps=30, theme="dark-modern")
    builder.add_narration("mp3/mp3-1.mp3", "mp3/mp3-1.srt")
    builder.add_bgm("assets/audio/bg-lofi.mp3", volume=0.12)
    scene = builder.add_scene("sc1", duration=55.0, layout="split-left")
    builder.add_card(scene, tag="NỘI DUNG", title="Tiêu đề", desc="Mô tả", accent="#3B82F6", appear_sec=12.5)
    builder.add_cutaway(scene, start_sec=0, end_sec=8.5, clips=["van-phong/clip1.mp4"], label="BỐI CẢNH")
    spec = builder.build()
    errors = HFSceneBuilder.validate(spec)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class HFSceneBuilder:
    """Xây dựng HF Scene Spec v2 JSON — Agent-friendly API."""

    SCHEMA = "hyperframes-scene-v2"
    SUPPORTED_THEMES = ("dark-modern", "light-whiteboard", "ai-tech-neon", "flat-editorial")
    SUPPORTED_LAYOUTS = ("split-left", "split-right", "center-anchor", "cards-grid")
    SUPPORTED_ANCHOR_TYPES = (
        "buni-student", "ai-robotics", "tech-orbit", "enterprise-network",
        "four-stages", "career-passport", "buni-ecosystem", "custom-image",
    )
    SUPPORTED_ANIMATION_PRESETS = (
        "fadeIn", "fadeInDown", "fadeInUp", "fadeInLeft", "fadeInRight",
        "slideInLeft", "slideInRight", "slideInUp",
        "zoomIn", "scaleUp",
        "springUp", "springLeft",
        "highlight", "blurIn",
        "typewriter", "kinetic", "drawSVG", "countUp",
    )

    def __init__(self):
        self._spec: dict[str, Any] = {
            "schema": self.SCHEMA,
            "meta": {
                "title": "HyperFrames Video",
                "fps": 30,
                "width": 1920,
                "height": 1080,
                "theme": "dark-modern",
            },
            "settings": {
                "bgColor": "#0F172A",
                "accentColor": "#38BDF8",
            },
            "globalAudio": [],
            "scenes": [],
        }
        self._scene_counter = 0
        self._element_counter = 0

    # ─── Meta ──────────────────────────────────────────────────────
    def set_meta(
        self,
        title: str = None,
        fps: int = None,
        theme: str = None,
        bg_color: str = None,
        accent_color: str = None,
        width: int = None,
        height: int = None,
    ) -> "HFSceneBuilder":
        if title:       self._spec["meta"]["title"] = title
        if fps:         self._spec["meta"]["fps"] = fps
        if width:       self._spec["meta"]["width"] = width
        if height:      self._spec["meta"]["height"] = height
        if theme and theme in self.SUPPORTED_THEMES:
            self._spec["meta"]["theme"] = theme
            # Tự động thiết lập màu theo theme
            theme_colors = {
                "dark-modern":      ("#0F172A", "#38BDF8"),
                "light-whiteboard": ("#FFFFFF", "#1E40AF"),
                "ai-tech-neon":     ("#0B0F19", "#00FFF0"),
                "flat-editorial":   ("#F8FAFC", "#4F46E5"),
            }
            bg, accent = theme_colors.get(theme, ("#0F172A", "#38BDF8"))
            self._spec["settings"]["bgColor"] = bg
            self._spec["settings"]["accentColor"] = accent
        if bg_color:    self._spec["settings"]["bgColor"] = bg_color
        if accent_color: self._spec["settings"]["accentColor"] = accent_color
        return self

    # ─── Audio ─────────────────────────────────────────────────────
    def add_narration(
        self,
        mp3_path: str,
        srt_path: str = None,
        volume: float = 1.0,
        scene_offset: float = 0.0,
    ) -> "HFSceneBuilder":
        """Thêm track narration (lời giảng TTS)."""
        track = {
            "id": "narration",
            "type": "narration",
            "src": str(mp3_path),
            "volume": volume,
        }
        if srt_path: track["srt"] = str(srt_path)
        if scene_offset: track["sceneOffset"] = scene_offset
        # Xóa narration cũ nếu có
        self._spec["globalAudio"] = [a for a in self._spec["globalAudio"] if a.get("id") != "narration"]
        self._spec["globalAudio"].insert(0, track)
        return self

    def add_bgm(
        self,
        src: str,
        volume: float = 0.12,
        loop: bool = True,
        fade_in: float = 1.5,
    ) -> "HFSceneBuilder":
        """Thêm track nhạc nền BGM Lo-Fi."""
        self._spec["globalAudio"] = [a for a in self._spec["globalAudio"] if a.get("id") != "bgm"]
        self._spec["globalAudio"].append({
            "id": "bgm",
            "type": "music",
            "src": str(src),
            "volume": volume,
            "loop": loop,
            "fadeIn": fade_in,
        })
        return self

    # ─── Scene ─────────────────────────────────────────────────────
    def add_scene(
        self,
        scene_id: str = None,
        duration: float = 40.0,
        layout: str = "cards-grid",
        title: str = "",
        badge: str = "",
        slide_number: str = "",
        bg_type: str = "tech-grid",
        bg_opacity: float = 0.3,
    ) -> dict:
        """
        Thêm scene mới vào spec.
        Trả về dict scene để tiếp tục thêm elements.
        """
        self._scene_counter += 1
        sid = scene_id or f"sc{self._scene_counter}"
        scene = {
            "id": sid,
            "duration": duration,
            "layout": layout if layout in self.SUPPORTED_LAYOUTS else "cards-grid",
            "title": title,
            "badge": badge,
            "slideNumber": slide_number,
            "background": {"type": bg_type, "opacity": bg_opacity},
            "elements": [],
            "cutaways": [],
        }
        self._spec["scenes"].append(scene)
        return scene

    # ─── Elements ──────────────────────────────────────────────────
    def add_card(
        self,
        scene: dict,
        tag: str = "",
        title: str = "",
        desc: str = "",
        icon: str = "📌",
        accent_color: str = None,
        bg_gradient: str = None,
        appear_sec: float = None,
        animation_preset: str = "springUp",
        element_id: str = None,
    ) -> "HFSceneBuilder":
        """Thêm thẻ card nội dung vào scene."""
        self._element_counter += 1
        eid = element_id or f"card-{self._element_counter}"
        card = {
            "id": eid,
            "type": "card",
            "content": {"tag": tag, "title": title, "desc": desc, "icon": icon},
            "style": {},
            "animation": {
                "preset": animation_preset if animation_preset in self.SUPPORTED_ANIMATION_PRESETS else "springUp",
            },
        }
        if accent_color:
            card["style"]["accentColor"] = accent_color
        if bg_gradient:
            card["style"]["bgGradient"] = bg_gradient
        if appear_sec is not None:
            card["animation"]["appearSec"] = appear_sec
        else:
            # Mặc định: xuất hiện sau thẻ trước
            existing_cards = [e for e in scene["elements"] if e.get("type") == "card"]
            card["animation"]["appearSec"] = 0.5 + len(existing_cards) * 0.3
        scene["elements"].append(card)
        return self

    def add_text(
        self,
        scene: dict,
        content: str,
        font_size: int = 40,
        font_weight: int = 800,
        color: str = "#F8FAFC",
        animation_preset: str = "fadeInDown",
        delay: float = 0.2,
        duration: float = 0.5,
        element_id: str = None,
    ) -> "HFSceneBuilder":
        """Thêm text element vào scene."""
        self._element_counter += 1
        eid = element_id or f"text-{self._element_counter}"
        scene["elements"].append({
            "id": eid,
            "type": "text",
            "content": content,
            "style": {"fontSize": font_size, "fontWeight": font_weight, "color": color},
            "animation": {"preset": animation_preset, "delay": delay, "duration": duration},
        })
        return self

    def add_code(
        self,
        scene: dict,
        language: str = "python",
        filename: str = "main.py",
        code: str = "",
        delay: float = 0.6,
        char_duration: float = 3.0,
        element_id: str = None,
    ) -> "HFSceneBuilder":
        """Thêm Code Studio Typewriter vào scene."""
        self._element_counter += 1
        eid = element_id or f"code-{self._element_counter}"
        scene["elements"].append({
            "id": eid,
            "type": "code",
            "language": language,
            "filename": filename,
            "content": code,
            "animation": {
                "preset": "typewriter",
                "delay": delay,
                "charDuration": char_duration,
            },
        })
        return self

    def set_visual_anchor(
        self,
        scene: dict,
        anchor_type: str = "buni-ecosystem",
        accent_color: str = None,
        label: str = None,
        image_src: str = None,
        size: int = 500,
    ) -> "HFSceneBuilder":
        """Gán Visual Anchor (SVG preset hoặc custom image) cho scene."""
        anchor = {
            "type": anchor_type if anchor_type in self.SUPPORTED_ANCHOR_TYPES else "buni-ecosystem",
            "size": size,
        }
        if accent_color: anchor["accentColor"] = accent_color
        if label:        anchor["label"] = label
        if image_src:    anchor["imageSrc"] = image_src
        scene["visualAnchor"] = anchor
        return self

    # ─── Cutaways ──────────────────────────────────────────────────
    def add_cutaway(
        self,
        scene: dict,
        start_sec: float,
        end_sec: float,
        clips: list[str | dict],
        label: str = "",
        default_clip_duration: float = 8.0,
    ) -> "HFSceneBuilder":
        """
        Thêm B-roll cutaway segment.
        clips: list đường dẫn video hoặc [{"src": "...", "duration": 5.0}]
        """
        resolved_clips = []
        for clip in clips:
            if isinstance(clip, str):
                resolved_clips.append({"src": clip, "duration": default_clip_duration})
            else:
                resolved_clips.append(clip)

        scene["cutaways"].append({
            "startSec": start_sec,
            "endSec": end_sec,
            "label": label,
            "clips": resolved_clips,
        })
        return self

    # ─── Build & Validate ──────────────────────────────────────────
    def build(self) -> dict:
        """Trả về HF Scene Spec JSON dict đầy đủ."""
        return self._spec

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self._spec, ensure_ascii=False, indent=indent)

    def save(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_json(), encoding="utf-8")
        return out

    @staticmethod
    def validate(spec: dict) -> list[str]:
        """
        Kiểm tra tính hợp lệ của spec.
        Trả về list lỗi (rỗng = hợp lệ).
        """
        errors = []
        if spec.get("schema") != "hyperframes-scene-v2":
            errors.append(f"schema phải là 'hyperframes-scene-v2', hiện tại: {spec.get('schema')}")

        meta = spec.get("meta", {})
        if meta.get("fps", 30) not in (24, 25, 30, 60):
            errors.append(f"fps không hợp lệ: {meta.get('fps')}")
        if meta.get("width", 1920) != 1920 or meta.get("height", 1080) != 1080:
            errors.append("width/height phải là 1920×1080")

        for i, scene in enumerate(spec.get("scenes", [])):
            prefix = f"scenes[{i}]"
            if not scene.get("id"):
                errors.append(f"{prefix}: thiếu 'id'")
            if not scene.get("duration") or scene["duration"] <= 0:
                errors.append(f"{prefix}: 'duration' phải > 0")
            if scene.get("layout") and scene["layout"] not in HFSceneBuilder.SUPPORTED_LAYOUTS:
                errors.append(f"{prefix}: layout '{scene['layout']}' không hợp lệ")
            for j, el in enumerate(scene.get("elements", [])):
                eprefix = f"{prefix}.elements[{j}]"
                if not el.get("id"):
                    errors.append(f"{eprefix}: thiếu 'id'")
                if el.get("type") not in ("text", "card", "text_card", "code", "image", "shape"):
                    errors.append(f"{eprefix}: type '{el.get('type')}' không hợp lệ")
            for j, cut in enumerate(scene.get("cutaways", [])):
                cprefix = f"{prefix}.cutaways[{j}]"
                if cut.get("startSec", 0) >= cut.get("endSec", 0):
                    errors.append(f"{cprefix}: startSec >= endSec")
                if not cut.get("clips"):
                    errors.append(f"{cprefix}: thiếu 'clips'")

        return errors

    # ─── Input Variable Binding ────────────────────────────────────
    @staticmethod
    def bind_variables(spec: dict, variables: dict) -> dict:
        """
        Thay thế biến template trong spec.
        variables: {"video_title": "Bài Giảng 1", "scene_num": "2", "slide_total": "8"}
        """
        spec_str = json.dumps(spec, ensure_ascii=False)
        for key, value in variables.items():
            spec_str = spec_str.replace("{" + key + "}", str(value))
        return json.loads(spec_str)

    @staticmethod
    def from_file(path: str | Path) -> dict:
        """Load spec từ file JSON."""
        return json.loads(Path(path).read_text(encoding="utf-8"))
