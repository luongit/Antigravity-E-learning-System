#!/usr/bin/env python3
"""
engines/virtual_lab/runtime/circuit_lab.py
Module Mô Phỏng Mạch Điện Ảo (Circuit Analyzer Lab POC):
- Cấp phép theo MIT.
- Chạy hoàn toàn offline trong browser qua HTML5 Canvas / WebAssembly.
- Các bài thí nghiệm chuẩn:
  1. Mạch DC cơ bản & Khảo sát Định luật Ohm: I = U / R
  2. Hai điện trở mắc nối tiếp: Rtđ = R1 + R2, U = U1 + U2
  3. Hai điện trở mắc song song: 1/Rtđ = 1/R1 + 1/R2, I = I1 + I2
  4. Mạch nạp & xả tụ điện RC: uC(t) = U0·(1 - e^(-t/RC)), hằng số thời gian τ = R·C
  5. Đo lường thời gian thực bằng Vôn kế & Ampe kế ảo
"""

import math
from typing import Any, Dict, Optional


def build_dc_circuit_config(
    circuit_type: str = "series",  # "single", "series", "parallel", "rc"
    voltage_u: float = 12.0,       # Vôn (V)
    r1: float = 10.0,              # Ohm (Ω)
    r2: float = 20.0,              # Ohm (Ω)
    capacitance_c: float = 100.0,  # Microfarad (µF)
) -> Dict[str, Any]:
    """
    Tính toán các đại lượng dòng điện, điện áp và công suất trong mạch điện.
    """
    u = voltage_u
    if circuit_type == "single":
        r_eq = r1
        i_total = u / r_eq
        p_total = u * i_total
        u1, u2 = u, 0.0
        i1, i2 = i_total, 0.0
        law_title = "ĐỊNH LUẬT OHM CHO ĐOẠN MẠCH"
        formula = "I = U / R | P = U · I"

    elif circuit_type == "series":
        r_eq = r1 + r2
        i_total = u / r_eq
        p_total = u * i_total
        u1 = i_total * r1
        u2 = i_total * r2
        i1 = i2 = i_total
        law_title = "ĐOẠN MẠCH NỐI TIẾP & ĐỊNH LUẬT OHM"
        formula = "R_tđ = R₁ + R₂ | I = U / R_tđ | U = U₁ + U₂"

    elif circuit_type == "parallel":
        r_eq = (r1 * r2) / (r1 + r2)
        i1 = u / r1
        i2 = u / r2
        i_total = i1 + i2
        p_total = u * i_total
        u1 = u2 = u
        law_title = "ĐOẠN MẠCH SONG SONG & ĐỊNH LUẬT OHM"
        formula = "1/R_tđ = 1/R₁ + 1/R₂ | I = I₁ + I₂ | U = U₁ = U₂"

    elif circuit_type == "rc":
        r_eq = r1
        i_total = u / r1
        p_total = u * i_total
        tau_ms = r1 * (capacitance_c * 1e-6) * 1000  # Hằng số thời gian τ tính bằng mili-giây
        u1 = u
        u2 = 0.0
        i1, i2 = i_total, 0.0
        law_title = "QUÁ TRÌNH NẠP ĐIỆN CHO TỤ ĐIỆN (MẠCH RC)"
        formula = "u_C(t) = U₀·(1 - e^(-t/RC)) | τ = R · C"
    else:
        r_eq = r1
        i_total = u / r1
        p_total = u * i_total
        u1, u2, i1, i2 = u, 0.0, i_total, 0.0
        law_title = "ĐỊNH LUẬT OHM"
        formula = "I = U / R"

    return {
        "domain": "circuit",
        "sub_type": circuit_type,
        "title": f"MÔ PHỎNG MẠCH ĐIỆN ẢO: {law_title}",
        "subtitle": f"Nguồn điện U = {u:.1f}V • R₁ = {r1:.1f}Ω • R₂ = {r2:.1f}Ω • Đo kiểm dòng điện thời gian thực",
        "params": {
            "circuit_type": circuit_type,
            "voltage_u": u,
            "r1": r1,
            "r2": r2,
            "capacitance_c": capacitance_c,
            "r_equivalent": r_eq,
            "i_total": i_total,
            "i1": i1,
            "i2": i2,
            "u1": u1,
            "u2": u2,
            "p_total": p_total,
        },
        "telemetry": {
            "law_name": law_title,
            "formula": formula,
            "source_u": f"{u:.2f} V",
            "r_equivalent": f"{r_eq:.2f} Ω",
            "current_i": f"{i_total:.3f} A ({i_total * 1000:.1f} mA)",
            "u1": f"{u1:.2f} V",
            "u2": f"{u2:.2f} V",
            "power_p": f"{p_total:.2f} W",
        },
    }
