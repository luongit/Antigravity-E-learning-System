#!/usr/bin/env python3
"""
engines/virtual_lab/runtime/optics_lab.py
Module Mô Phỏng Quang Học & Truyền Tia Sáng (Ray Optics Simulation):
- Cấp phép theo giấy phép mở Apache-2.0 / MIT.
- 100% độc lập, không phụ thuộc bên thứ ba bị hạn chế bản quyền thương mại.
- Chuyên biệt hóa cho bài giảng:
  + Định luật Khúc xạ ánh sáng (Định luật Snell: n1*sin(θ1) = n2*sin(θ2))
  + Định luật Phản xạ ánh sáng (θr = θ1) & Phản xạ toàn phần (Góc tới hạn θc)
  + Thấu kính mỏng (Hội tụ / Phân kỳ, tiêu cự f, ảnh thật / ảnh ảo)
  + Lăng kính & Tán sắc ánh sáng
  + Thước đo góc tròn Protractor 360 độ đo trực tiếp góc tới và góc khúc xạ
"""

import math
from typing import Any, Dict, List, Optional

# Thư viện chiết suất của các môi trường truyền sáng chuẩn
REFRACTIVE_INDICES = {
    "air": {"name": "Không khí", "n": 1.0003, "color": "rgba(255, 255, 255, 0.05)"},
    "water": {"name": "Nước", "n": 1.3330, "color": "rgba(56, 189, 248, 0.22)"},
    "glass": {"name": "Thủy tinh Crown", "n": 1.5200, "color": "rgba(99, 102, 241, 0.25)"},
    "flint_glass": {"name": "Thủy tinh Flint", "n": 1.6600, "color": "rgba(139, 92, 246, 0.28)"},
    "diamond": {"name": "Kim cương", "n": 2.4170, "color": "rgba(236, 72, 153, 0.30)"},
    "oil": {"name": "Dầu ăn thực vật", "n": 1.4700, "color": "rgba(245, 158, 11, 0.22)"},
}


def build_refraction_config(
    theta1_deg: float = 45.0,
    n1_key: str = "air",
    n2_key: str = "water",
    ray_color: str = "#EF4444",
    laser_power: float = 1.0,
    show_protractor: bool = True,
    show_normal: bool = True,
    show_intensity: bool = True,
    show_angles: bool = True,
) -> Dict[str, Any]:
    """
    Tính toán thông số hình học và quang học cho thí nghiệm khúc xạ ánh sáng (Định luật Snell).
    """
    mat1 = REFRACTIVE_INDICES.get(n1_key, REFRACTIVE_INDICES["air"])
    mat2 = REFRACTIVE_INDICES.get(n2_key, REFRACTIVE_INDICES["water"])
    n1 = mat1["n"]
    n2 = mat2["n"]

    theta1_rad = math.radians(theta1_deg)
    sin_theta1 = math.sin(theta1_rad)
    sin_theta2 = (n1 / n2) * sin_theta1

    is_total_internal_reflection = sin_theta2 > 1.0
    critical_angle_deg = None
    if n1 > n2:
        critical_angle_deg = math.degrees(math.asin(n2 / n1))

    if is_total_internal_reflection:
        theta2_deg = None
        refl_power = laser_power
        refr_power = 0.0
    else:
        theta2_rad = math.asin(sin_theta2)
        theta2_deg = math.degrees(theta2_rad)
        # Tính cường độ phản xạ & khúc xạ theo công thức gần đúng Fresnel
        r0 = ((n1 - n2) / (n1 + n2)) ** 2
        refl_power = r0 + (1 - r0) * ((1 - math.cos(theta1_rad)) ** 5)
        refr_power = max(0.0, laser_power - refl_power)

    # Dữ liệu phục vụ HUD viễn trắc (Telemetry)
    telemetry = {
        "law_name": "ĐỊNH LUẬT KHÚC XẠ ÁNH SÁNG (ĐỊNH LUẬT SNELL)",
        "formula": "n₁ · sin(θ₁) = n₂ · sin(θ₂)",
        "env1_name": f"{mat1['name']} (n₁ = {n1:.3f})",
        "env2_name": f"{mat2['name']} (n₂ = {n2:.3f})",
        "theta1": f"{theta1_deg:.1f}°",
        "theta_r": f"{theta1_deg:.1f}°",
        "theta2": f"{theta2_deg:.1f}°" if theta2_deg is not None else "Phản xạ toàn phần",
        "critical_angle": f"{critical_angle_deg:.2f}°" if critical_angle_deg else "Không có (n₁ < n₂)",
        "status": "PHẢN XẠ TOÀN PHẦN" if is_total_internal_reflection else "KHÚC XẠ & PHẢN XẠ MỘT PHẦN",
    }

    return {
        "domain": "optics",
        "sub_type": "refraction",
        "title": "MÔ PHỎNG QUANG HỌC: ĐỊNH LUẬT KHÚC XẠ VÀ PHẢN XẠ ÁNH SÁNG",
        "subtitle": f"Khảo sát tia sáng từ {mat1['name']} (n={n1:.2f}) sang {mat2['name']} (n={n2:.2f})",
        "params": {
            "theta1_deg": theta1_deg,
            "n1": n1,
            "n2": n2,
            "mat1_name": mat1["name"],
            "mat2_name": mat2["name"],
            "mat1_color": mat1["color"],
            "mat2_color": mat2["color"],
            "ray_color": ray_color,
            "laser_power": laser_power,
            "theta2_deg": theta2_deg,
            "is_tir": is_total_internal_reflection,
            "critical_angle_deg": critical_angle_deg,
            "refl_power": refl_power,
            "refr_power": refr_power,
            "show_protractor": show_protractor,
            "show_normal": show_normal,
            "show_intensity": show_intensity,
            "show_angles": show_angles,
        },
        "telemetry": telemetry,
    }


def build_lens_config(
    lens_type: str = "converging",  # "converging" (hội tụ) hoặc "diverging" (phân kỳ)
    focal_length: float = 180.0,
    object_distance: float = 300.0,
    object_height: float = 80.0,
) -> Dict[str, Any]:
    """
    Mô phỏng đường đi của chùm tia sáng qua thấu kính mỏng:
    1/f = 1/d + 1/d' => d' = (d * f) / (d - f)
    Độ phóng đại ảnh: k = -d' / d = A'B' / AB
    """
    f = focal_length if lens_type == "converging" else -focal_length
    d = object_distance

    if abs(d - f) < 1e-4:
        d_prime = float("inf")
        height_prime = float("inf")
        is_real = False
    else:
        d_prime = (d * f) / (d - f)
        magnification = -d_prime / d
        height_prime = object_height * magnification
        is_real = d_prime > 0

    return {
        "domain": "optics",
        "sub_type": "lens",
        "title": f"MÔ PHỎNG QUANG HỌC: THẤU KÍNH {'HỘI TỤ' if lens_type == 'converging' else 'PHÂN KỲ'}",
        "subtitle": f"Tiêu cự f = {abs(f):.1f}mm • Khoảng cách vật d = {d:.1f}mm • Khảo sát tạo ảnh",
        "params": {
            "lens_type": lens_type,
            "focal_length": f,
            "object_distance": d,
            "object_height": object_height,
            "image_distance": d_prime if d_prime != float("inf") else 9999,
            "image_height": height_prime if height_prime != float("inf") else 9999,
            "is_real": is_real,
        },
        "telemetry": {
            "law_name": "CÔNG THỨC THẤU KÍNH MỎNG",
            "formula": "1/f = 1/d + 1/d' | k = -d'/d",
            "f": f"{f:.1f} mm",
            "d": f"{d:.1f} mm",
            "d_prime": f"{d_prime:.1f} mm" if d_prime != float("inf") else "Vô cực (ảnh ở ∞)",
            "image_type": "Ảnh thật, ngược chiều" if is_real else "Ảnh ảo, cùng chiều",
            "k": f"{abs(height_prime / object_height):.2f}x" if height_prime != float("inf") else "∞",
        },
    }
