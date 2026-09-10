"""
core/voice_parser.py
Parser phân tích tệp Voice Script do người dùng cung cấp.
Hỗ trợ:
- Phân đoạn theo dòng trống (\n\n)
- Phân đoạn theo nhãn: [Đoạn X], Đoạn X:, Slide X:, Scene X:
- Bỏ qua dòng tiêu đề bài học nếu có (ví dụ: 'Voice script video 1 - ...')
"""

import re
from pathlib import Path
from typing import List, Dict, Any

def parse_voice_script(file_path_or_text: str) -> List[Dict[str, Any]]:
    """
    Phân tích file hoặc chuỗi văn bản Voice Script thành danh sách các đoạn.
    Trả về:
    [
        {"index": 1, "label": "Slide 1", "text": "...", "word_count": 120},
        ...
    ]
    """
    p = Path(file_path_or_text)
    if p.exists() and p.is_file():
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="utf-8-sig")
    else:
        content = file_path_or_text

    content = content.strip()
    if not content:
        return []

    lines = content.splitlines()
    
    # 1. Kiểm tra nếu có dòng tiêu đề tổng quát ở đầu
    start_idx = 0
    first_line = lines[0].strip()
    if re.match(r"^(voice\s*script|kịch\s*bản\s*lời\s*thoại|video\s*\d+|bài\s*\d+)", first_line, re.IGNORECASE):
        start_idx = 1

    remaining_text = "\n".join(lines[start_idx:]).strip()

    # 2. Thử tách theo nhãn [Đoạn X], Đoạn X, Slide X
    section_pattern = re.compile(
        r"(?:^|\n)\s*(?:\[|\b)(?:Đoạn|Slide|Scene|Phần|Mục)\s*(\d+)(?:\]|:|\s*[-–—]|\.|\))\s*",
        re.IGNORECASE
    )

    matches = list(section_pattern.finditer(remaining_text))
    sections = []

    if matches:
        for i, m in enumerate(matches):
            sec_num = int(m.group(1))
            sec_start = m.end()
            sec_end = matches[i + 1].start() if i + 1 < len(matches) else len(remaining_text)
            body = remaining_text[sec_start:sec_end].strip()
            
            body_lines = [l.strip() for l in body.splitlines() if l.strip()]
            clean_text = " ".join(body_lines)
            
            words = clean_text.split()
            sections.append({
                "index": sec_num,
                "label": f"Slide {sec_num}",
                "text": clean_text,
                "word_count": len(words)
            })
    else:
        # 3. Nếu không có nhãn đánh số, tách theo 1 hoặc nhiều dòng trống (\n\s*\n)
        raw_blocks = re.split(r"\n\s*\n+", remaining_text)
        block_idx = 1
        for block in raw_blocks:
            clean_block = " ".join([l.strip() for l in block.splitlines() if l.strip()])
            if clean_block:
                words = clean_block.split()
                sections.append({
                    "index": block_idx,
                    "label": f"Slide {block_idx}",
                    "text": clean_block,
                    "word_count": len(words)
                })
                block_idx += 1

    return sections

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sample = """
    Voice script video 1 - Kỹ thuật Phân tích Nguyên nhân Gốc rễ

    Đoạn 1:
    Chào mừng các bạn đã quay trở lại. Hôm nay chúng ta sẽ tìm hiểu về mô hình 5 Whys và Ishikawa.

    Đoạn 2:
    Mục tiêu bài học giúp các bạn phân biệt rõ ràng giữa triệu chứng bề mặt và nguyên nhân cốt lõi.

    Đoạn 3:
    Mô hình tảng băng minh họa rõ điều này. 10% phần nổi là lỗi nhìn thấy được, 90% phần chìm là nợ kỹ thuật.
    """
    res = parse_voice_script(sample)
    print(f"Parsed {len(res)} sections:")
    for s in res:
        print(f"- {s['label']}: ({s['word_count']} words) {s['text'][:60]}...")
