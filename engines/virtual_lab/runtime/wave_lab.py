#!/usr/bin/env python3
"""
engines/virtual_lab/runtime/wave_lab.py
Module Mô Phỏng Sóng Cơ Học & Dao Động Điều Hòa (Wave & Oscillator Lab):
- Cấp phép theo MIT.
- Các bài thí nghiệm chuẩn:
  1. Sóng truyền trên sợi dây đàn hồi (Wave on a string): y = A·sin(ωt - kx)
  2. Khảo sát biên độ A, bước sóng λ, tần số f, vận tốc truyền sóng v = λ·f
  3. Hiện tượng sóng dừng (Standing Wave): Nút sóng (Nodes) và Bụng sóng (Antinodes)
  4. Phản xạ sóng tại đầu cố định (ngược pha) và đầu tự do (cùng pha)
  5. Giao thoa sóng cơ giữa 2 nguồn kết hợp
"""

import math
from typing import Any, Dict, Optional


def build_wave_on_string_config(
    amplitude_cm: float = 4.0,
    frequency_hz: float = 1.5,
    tension_level: str = "medium",  # "low", "medium", "high"
    damping: float = 0.05,
    end_type: str = "fixed",        # "fixed" (cố định), "free" (tự do), "infinite" (vô hạn)
) -> Dict[str, Any]:
    """
    Tính toán thông số sóng cơ truyền trên sợi dây đàn hồi.
    """
    tension_speed_map = {
        "low": 180.0,      # px/s
        "medium": 320.0,   # px/s
        "high": 480.0,     # px/s
    }
    wave_speed_v = tension_speed_map.get(tension_level, 320.0)
    wavelength_px = wave_speed_v / frequency_hz
    omega = 2 * math.pi * frequency_hz
    k = 2 * math.pi / wavelength_px

    return {
        "domain": "wave",
        "sub_type": "string_wave",
        "title": "MÔ PHỎNG SÓNG CƠ HỌC TRÊN SỢI DÂY ĐÀN HỒI",
        "subtitle": f"Biên độ A = {amplitude_cm:.1f}cm • Tần số f = {frequency_hz:.2f}Hz • Đầu phản xạ: {end_type.upper()}",
        "params": {
            "amplitude_cm": amplitude_cm,
            "amplitude_px": amplitude_cm * 10.0,
            "frequency_hz": frequency_hz,
            "omega": omega,
            "wave_speed": wave_speed_v,
            "wavelength_px": wavelength_px,
            "damping": damping,
            "end_type": end_type,
            "string_length_px": 1200,
            "num_points": 120,
        },
        "telemetry": {
            "law_name": "PHƯƠNG TRÌNH TRUYỀN SÓNG CƠ HÌNH SIN",
            "formula": "u(x,t) = A·sin(2πft - 2πx/λ) | v = λ · f",
            "amplitude": f"{amplitude_cm:.1f} cm",
            "frequency": f"{frequency_hz:.2f} Hz",
            "period": f"{1.0 / frequency_hz:.2f} s",
            "wavelength": f"{wavelength_px / 10.0:.1f} cm (tương ứng scale)",
            "speed": f"{wave_speed_v / 10.0:.1f} cm/s",
            "end_condition": "Đầu cố định (Đảo pha π)" if end_type == "fixed" else "Đầu tự do (Cùng pha)",
        },
    }


def build_interference_config(
    freq_hz: float = 2.0,
    distance_sources_cm: float = 20.0,
) -> Dict[str, Any]:
    """Mô phỏng giao thoa sóng cơ giữa 2 nguồn kết hợp cùng pha."""
    wavelength = 8.0  # cm
    return {
        "domain": "wave",
        "sub_type": "interference",
        "title": "MÔ PHỎNG GIAO THOA SÓNG CƠ HỌC (2 NGUỒN CÙNG PHA)",
        "subtitle": f"Khoảng cách 2 nguồn d = {distance_sources_cm:.1f}cm • Bước sóng λ = {wavelength:.1f}cm",
        "params": {
            "frequency_hz": freq_hz,
            "distance_sources_cm": distance_sources_cm,
            "wavelength": wavelength,
        },
        "telemetry": {
            "law_name": "ĐIỀU KIỆN GIAO THOA SÓNG KẾT HỢP",
            "formula": "Cực đại: d₂ - d₁ = k·λ | Cực tiểu: d₂ - d₁ = (k + ½)·λ",
            "distance": f"{distance_sources_cm:.1f} cm",
            "wavelength": f"{wavelength:.1f} cm",
            "f": f"{freq_hz:.1f} Hz",
        },
    }
