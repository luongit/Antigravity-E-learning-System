#!/usr/bin/env python3
"""
engines/hyperframes/render.py
HyperFrames v2 Entry Point CLI:
Cung cấp lệnh thực thi trực tiếp từ thư mục engine:
python engines/hyperframes/render.py <video_dir> [--scene N] [--output OUT] [--mode video|slides|preview] [--batch 1,2,3]
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from core.hf_engine import main

if __name__ == "__main__":
    main()
