#!/usr/bin/env python3
"""
engines/virtual_lab/runtime/field_lab.py
Module Mô Phỏng Điện Trường & Trực Quan Hóa Đường Sức (Electric Field Lab):
- Cấp phép theo MIT (Three.js / HTML5 Canvas).
- Các bài thí nghiệm chuẩn:
  1. Một điện tích điểm đơn lẻ (+q hoặc -q)
  2. Lưỡng cực điện (Dipole: +q và -q)
  3. Hai điện tích cùng dấu (+q và +q)
  4. Hệ 3 hoặc nhiều điện tích phân bố trong không gian
  5. Lưới véc-tơ cường độ điện trường E và họ đường sức điện liên tục
"""

import math
from typing import Any, Dict, List, Optional


def build_electric_field_config(
    charges: Optional[List[Dict[str, Any]]] = None,
    show_vectors: bool = True,
    show_field_lines: bool = True,
    show_potential: bool = False,
) -> Dict[str, Any]:
    """
    Tính toán và trực quan hóa phân bố điện trường theo định luật Coulomb.
    """
    if charges is None:
        # Mặc định tạo hệ lưỡng cực điện (Dipole)
        charges = [
            {"x": 760, "y": 540, "q": 2.0, "color": "#EF4444", "label": "+2µC"},
            {"x": 1160, "y": 540, "q": -2.0, "color": "#3B82F6", "label": "-2µC"},
        ]

    total_q = sum(c["q"] for c in charges)
    num_pos = sum(1 for c in charges if c["q"] > 0)
    num_neg = sum(1 for c in charges if c["q"] < 0)

    return {
        "domain": "field",
        "sub_type": "electrostatics",
        "title": "MÔ PHỎNG ĐIỆN TRƯỜNG TĨNH & ĐƯỜNG SỨC ĐIỆN",
        "subtitle": f"Khảo sát hệ {len(charges)} điện tích điểm ({num_pos} dương, {num_neg} âm) • Tổng điện tích: {total_q:+.1f}µC",
        "params": {
            "charges": charges,
            "k_constant": 8.98755e9,
            "show_vectors": show_vectors,
            "show_field_lines": show_field_lines,
            "show_potential": show_potential,
            "vector_grid_step": 60,
            "num_lines_per_charge": 16,
        },
        "telemetry": {
            "law_name": "NGUYÊN LÝ CHỒNG CHẤT ĐIỆN TRƯỜNG & ĐỊNH LUẬT COULOMB",
            "formula": "E = k · Σ (q_i / r_i²) · r̂_i | V = k · Σ (q_i / r_i)",
            "num_charges": f"{len(charges)} điện tích",
            "total_charge": f"{total_q:+.1f} µC",
            "grid_resolution": "1920 × 1080 Full HD",
            "representation": "Lưới Véc-tơ E + Đường Sức Điện Liên Tục",
        },
    }
