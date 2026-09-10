#!/usr/bin/env python3
"""
engines/virtual_lab/runtime/mechanics_lab.py
Module Mô Phỏng Vật Lý Cơ Học 2D Mở Rộng (Matter.js Mechanics Lab):
- Cấp phép theo MIT (Matter.js).
- Mở rộng 9 dạng bài thí nghiệm cơ học:
  1. Rơi tự do (Free Fall)
  2. Ném ngang (Horizontal Throw)
  3. Ném xiên (Projectile Motion)
  4. Va chạm đàn hồi & Va chạm mềm (Collisions & Momentum Conservation)
  5. Ma sát & Mặt phẳng nghiêng (Friction & Inclined Plane)
  6. Con lắc lò xo (Spring Oscillator)
  7. Con lắc đơn (Simple Pendulum)
  8. Hệ nhiều vật liên kết (Multi-body system / Pulley)
  9. Chuyển động có lực tác dụng biến thiên (Driven motion)
"""

import math
from typing import Any, Dict, List, Optional


def build_projectile_config(
    v0: float = 24.0,
    angle_deg: float = 45.0,
    restitution: float = 0.75,
    air_friction: float = 0.0,
) -> Dict[str, Any]:
    """Khảo sát chuyển động ném xiên trong trọng trường."""
    rad = math.radians(angle_deg)
    g = 9.8
    h_max = (v0**2 * (math.sin(rad)**2)) / (2 * g)
    l_max = (v0**2 * math.sin(2 * rad)) / g
    t_flight = (2 * v0 * math.sin(rad)) / g

    return {
        "domain": "mechanics",
        "sub_type": "projectile",
        "title": "MÔ PHỎNG CƠ HỌC: CHUYỂN ĐỘNG NÉM XIÊN TRONG TRỌNG TRƯỜNG",
        "subtitle": f"Góc ném α = {angle_deg:.1f}° • Vận tốc đầu v₀ = {v0:.1f} m/s • Khảo sát quỹ đạo Parabol",
        "params": {
            "v0": v0,
            "angle_deg": angle_deg,
            "restitution": restitution,
            "gravity": 1.0,
            "air_friction": air_friction,
            "startX": 220,
            "startY": 880,
            "floorY": 940,
        },
        "telemetry": {
            "law_name": "CHUYỂN ĐỘNG TRONG TRỌNG TRƯỜNG ĐỀU",
            "formula": "y = x·tan(α) - (g·x²)/(2·v₀²·cos²(α))",
            "v0": f"{v0:.1f} m/s",
            "angle": f"{angle_deg:.1f}°",
            "h_max": f"{h_max:.2f} m",
            "l_max": f"{l_max:.2f} m",
            "t_flight": f"{t_flight:.2f} s",
        },
    }


def build_free_fall_config(
    height_m: float = 45.0,
    mass_kg: float = 2.0,
    air_resistance: bool = False,
) -> Dict[str, Any]:
    """Khảo sát sự rơi tự do của vật thể trong trọng trường."""
    g = 9.8
    t_fall = math.sqrt(2 * height_m / g)
    v_impact = g * t_fall

    return {
        "domain": "mechanics",
        "sub_type": "free_fall",
        "title": "MÔ PHỎNG CƠ HỌC: SỰ RƠI TỰ DO CỦA VẬT THỂ",
        "subtitle": f"Độ cao ban đầu h = {height_m:.1f}m • Khối lượng m = {mass_kg:.1f}kg • Gia tốc g = 9.8 m/s²",
        "params": {
            "height_m": height_m,
            "mass_kg": mass_kg,
            "air_resistance": air_resistance,
            "gravity": 1.0,
            "startX": 960,
            "startY": 200,
            "floorY": 920,
        },
        "telemetry": {
            "law_name": "ĐỊNH LUẬT RƠI TỰ DO (GALILEO)",
            "formula": "h = ½·g·t² | v = g·t = √(2·g·h)",
            "height": f"{height_m:.1f} m",
            "t_fall": f"{t_fall:.2f} s",
            "v_impact": f"{v_impact:.2f} m/s",
            "mass": f"{mass_kg:.1f} kg",
        },
    }


def build_collision_config(
    m1: float = 2.0,
    v1: float = 12.0,
    m2: float = 1.0,
    v2: float = -4.0,
    elastic: bool = True,
) -> Dict[str, Any]:
    """Khảo sát va chạm đàn hồi và va chạm mềm giữa 2 vật."""
    # Vận tốc sau va chạm đàn hồi 1D
    if elastic:
        v1_after = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        v2_after = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
        law = "ĐỊNH LUẬT BẢO TOÀN ĐỘNG LƯỢNG & ĐỘNG NĂNG (VA CHẠM ĐÀN HỒI)"
    else:
        v_common = (m1 * v1 + m2 * v2) / (m1 + m2)
        v1_after = v2_after = v_common
        law = "ĐỊNH LUẬT BẢO TOÀN ĐỘNG LƯỢNG (VA CHẠM MỀM)"

    p_total = m1 * v1 + m2 * v2
    return {
        "domain": "mechanics",
        "sub_type": "collision",
        "title": f"MÔ PHỎNG CƠ HỌC: VA CHẠM {'ĐÀN HỒI' if elastic else 'MỀM'} 1D",
        "subtitle": f"m₁={m1}kg (v₁={v1}m/s) va chạm với m₂={m2}kg (v₂={v2}m/s)",
        "params": {
            "m1": m1, "v1": v1,
            "m2": m2, "v2": v2,
            "elastic": elastic,
            "v1_after": v1_after,
            "v2_after": v2_after,
            "p_total": p_total,
        },
        "telemetry": {
            "law_name": law,
            "formula": "m₁·v₁ + m₂·v₂ = m₁·v₁' + m₂·v₂'",
            "p_initial": f"{p_total:.2f} kg·m/s",
            "v1_prime": f"{v1_after:.2f} m/s",
            "v2_prime": f"{v2_after:.2f} m/s",
        },
    }


def build_pendulum_config(
    length_m: float = 2.5,
    angle_deg: float = 30.0,
    bob_mass: float = 1.0,
) -> Dict[str, Any]:
    """Khảo sát dao động của con lắc đơn."""
    g = 9.8
    period_T = 2 * math.pi * math.sqrt(length_m / g)
    freq_f = 1.0 / period_T

    return {
        "domain": "mechanics",
        "sub_type": "pendulum",
        "title": "MÔ PHỎNG CƠ HỌC: DAO ĐỘNG CON LẮC ĐƠN",
        "subtitle": f"Chiều dài dây l = {length_m:.2f}m • Góc lệch cực đại α₀ = {angle_deg:.1f}°",
        "params": {
            "length_m": length_m,
            "angle_deg": angle_deg,
            "bob_mass": bob_mass,
            "pivotX": 960,
            "pivotY": 240,
        },
        "telemetry": {
            "law_name": "DAO ĐỘNG ĐIỀU HÒA CỦA CON LẮC ĐƠN",
            "formula": "T = 2π·√(l/g) | ω = √(g/l)",
            "period": f"{period_T:.2f} s",
            "frequency": f"{freq_f:.2f} Hz",
            "length": f"{length_m:.2f} m",
            "max_angle": f"{angle_deg:.1f}°",
        },
    }
