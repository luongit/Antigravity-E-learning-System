#!/usr/bin/env python3
"""
engines/virtual_lab/runtime/lab_dispatcher.py
Bộ phân loại ngữ nghĩa & Điều phối thí nghiệm ảo (Virtual Lab Dispatcher):
- Phân tích câu lệnh ngôn ngữ tự nhiên từ người dùng.
- Tự động nhận diện domain vật lý / khoa học:
  + OPTICS (Quang học): Khúc xạ, phản xạ, định luật Snell, thấu kính, gương, chiết suất...
  + MECHANICS (Cơ học): Ném xiên, rơi tự do, va chạm, ma sát, lò xo, con lắc, lực...
  + CIRCUIT (Mạch điện): Định luật Ohm, mạch DC, nối tiếp, song song, mạch RC...
  + WAVE (Sóng & Dao động): Sóng trên dây, bước sóng, tần số, giao thoa, dao động điều hòa...
  + FIELD (Điện trường): Điện tích điểm, véc-tơ E, đường sức, tương tác điện tích...
"""

import re
from typing import Any, Dict, Optional

# Bản đồ từ khóa đặc trưng cho từng phân môn thí nghiệm ảo
DOMAIN_KEYWORDS = {
    "optics": [
        "quang", "quang học", "khúc xạ", "phản xạ", "tia sáng", "ánh sáng", "snell",
        "thấu kính", "gương", "lăng kính", "chiết suất", "góc tới", "góc khúc xạ",
        "phản xạ toàn phần", "tiêu cự", "hội tụ", "phân kỳ", "bending light", "ray optics"
    ],
    "mechanics": [
        "cơ học", "ném xiên", "ném ngang", "rơi tự do", "quỹ đạo", "parabol",
        "va chạm", "đàn hồi", "ma sát", "mặt phẳng nghiêng", "con lắc", "lò xo",
        "vận tốc", "gia tốc", "trọng lực", "newton", "động lượng", "ròng rọc"
    ],
    "circuit": [
        "mạch điện", "mạch", "điện trở", "ohm", "định luật ohm", "dòng điện",
        "hiệu điện thế", "vôn", "ampe", "nối tiếp", "song song", "tụ điện",
        "mạch rc", "vôn kế", "ampe kế", "nguồn dc", "pin", "công suất"
    ],
    "wave": [
        "sóng", "sóng cơ", "sóng trên dây", "bước sóng", "tần số", "chu kỳ",
        "biên độ", "sóng dừng", "nút sóng", "bụng sóng", "giao thoa", "dao động",
        "điều hòa", "pha dao động", "vận tốc truyền sóng", "lan truyền"
    ],
    "field": [
        "điện trường", "điện tích", "đường sức", "cường độ điện trường", "coulomb",
        "lực điện", "điện tích điểm", "mặt đẳng thế", "hạt mang điện", "dipole"
    ],
}


def detect_lab_domain(query: str) -> str:
    """
    Nhận diện domain phòng thí nghiệm ảo từ câu lệnh ngôn ngữ tự nhiên.
    Mặc định ưu tiên quang học nếu không khớp rõ ràng.
    """
    q_lower = query.lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}

    for domain, kws in DOMAIN_KEYWORDS.items():
        for kw in kws:
            if kw in q_lower:
                # Trọng số cao hơn nếu từ khóa xuất hiện nguyên vẹn
                scores[domain] += 2 if len(kw) > 4 else 1

    # Tìm domain có điểm cao nhất
    best_domain = max(scores, key=scores.get)
    if scores[best_domain] > 0:
        return best_domain

    # Fallback theo một số mẫu câu thông dụng
    if any(w in q_lower for w in ["sáng", "tia", "kính"]):
        return "optics"
    if any(w in q_lower for w in ["ném", "rơi", "lực", "chuyển động"]):
        return "mechanics"
    if any(w in q_lower for w in ["điện trở", "vôn", "i ="]):
        return "circuit"
    if any(w in q_lower for w in ["dao động", "sóng"]):
        return "wave"
    if any(w in q_lower for w in ["điện tích", "e ="]):
        return "field"

    return "optics"
