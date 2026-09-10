#!/usr/bin/env python3
"""
scripts/prepare_env.py
Bộ thiết lập và kiểm tra môi trường toàn diện cho toàn bộ dự án E-Learning:
1. Python Virtual Environment (.venv): pptx, vieneu (VieNeu-TTS v3 Turbo), opencv, numpy, av, Pillow, scipy
2. Node.js & HyperFrames Renderer (engines/hyperframes/renderer/node_modules)
3. FFmpeg & công cụ hệ thống

Cách dùng:
  python scripts/prepare_env.py          # Kiểm tra và tự động cài đặt toàn bộ
  python scripts/prepare_env.py --check  # Chỉ kiểm tra trạng thái
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
VENV_ROOT = WORKSPACE_ROOT / ".venv"
HYPERFRAMES_RENDERER = WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer"

# Thư viện Python cần thiết
DEPS: dict[str, str] = {
    "pptx": "python-pptx",
    "vieneu": "vieneu",            # VieNeu-TTS v3 Turbo (thay thế edge-tts)
    "docx": "python-docx",
    "pypdf": "pypdf",
    "cv2": "opencv-python",
    "numpy": "numpy",
    "scipy": "scipy",              # Dùng cho speed control trong VieNeu audio
    "av": "av",
    "PIL": "Pillow",
}


def interpreter_path() -> Path:
    """Đường dẫn python trong venv (Windows / Linux / macOS)."""
    if sys.platform.startswith("win"):
        return VENV_ROOT / "Scripts" / "python.exe"
    return VENV_ROOT / "bin" / "python"


def can_import(py: Path, import_name: str) -> bool:
    probe = subprocess.run(
        [str(py), "-c", f"import {import_name}"],
        capture_output=True,
    )
    return probe.returncode == 0


def ensure_venv(check_only: bool) -> Path:
    current_py = Path(sys.executable)
    py = interpreter_path()
    if py.exists():
        print(f"[OK] Virtual Environment đã tồn tại: {VENV_ROOT}")
        return py

    if check_only:
        print(f"[CẢNH BÁO] Chưa tìm thấy virtualenv tại: {VENV_ROOT}")
        return current_py

    print(f"[...] Đang khởi tạo virtualenv tại: {VENV_ROOT}...")
    venv.create(VENV_ROOT, with_pip=True)
    print(f"[OK] Đã tạo virtualenv thành công.")
    return py


def install_python_deps(py: Path, packages: list[str]) -> bool:
    print(f"\n[...] Đang cài đặt các thư viện Python: {', '.join(packages)}...")
    res = subprocess.run([str(py), "-m", "pip", "install", "--upgrade", "pip"])
    res = subprocess.run([str(py), "-m", "pip", "install"] + packages)
    if res.returncode == 0:
        print("[OK] Cài đặt thư viện Python thành công!")
        return True
    else:
        print(f"[LỖI] pip install thất bại với mã lỗi: {res.returncode}")
        return False


def check_ffmpeg() -> bool:
    cmd = shutil.which("ffmpeg")
    if cmd:
        print(f"  [OK] FFmpeg đã sẵn sàng: {cmd}")
        return True
    else:
        print("  [CẢNH BÁO] Chưa tìm thấy FFmpeg trong PATH hệ thống!")
        return False


def setup_hyperframes_engine(check_only: bool) -> bool:
    """Kiểm tra và cài đặt Node.js dependencies cho engines/hyperframes/renderer 1 lần duy nhất."""
    print("\n------------------------------------------------------------")
    print("📦 KIỂM TRA HYPERFRAMES V2 RENDERER (engines/hyperframes/renderer)")
    print("------------------------------------------------------------")

    # 1. Kiểm tra Node.js
    try:
        node_res = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if node_res.returncode == 0:
            print(f"[OK] Node.js đã sẵn sàng: {node_res.stdout.strip()}")
        else:
            print("[LỖI] Node.js chưa được cài đặt.")
            return False
    except FileNotFoundError:
        print("[LỖI] Không tìm thấy lệnh 'node'. Cần cài đặt Node.js >= 18.")
        return False

    # 2. Kiểm tra node_modules trong engines/hyperframes/renderer
    node_modules = HYPERFRAMES_RENDERER / "node_modules"
    package_json = HYPERFRAMES_RENDERER / "package.json"

    if not package_json.exists():
        print(f"[LỖI] Không tìm thấy {package_json}")
        return False

    if node_modules.exists() and (node_modules / "puppeteer").exists():
        print(f"[OK] Thư viện Puppeteer đã được cài đặt tập trung tại: {node_modules}")
        return True

    if check_only:
        print(f"[CẢNH BÁO] Chưa cài đặt dependencies cho HyperFrames tại: {HYPERFRAMES_RENDERER}")
        return False

    print(f"[...] Đang cài đặt npm packages cho engines/hyperframes/renderer (1 lần duy nhất)...")
    npm_res = subprocess.run(["npm", "install"], cwd=str(HYPERFRAMES_RENDERER), shell=True)
    if npm_res.returncode == 0:
        print("[OK] Cài đặt HyperFrames Renderer thành công!")
        return True
    else:
        print(f"[LỖI] npm install thất bại với mã lỗi: {npm_res.returncode}")
        return False


def main() -> None:
    check_only = "--check" in sys.argv

    print("============================================================")
    print("🚀 BỘ KIỂM TRA & THIẾT LẬP MÔI TRƯỜNG DỰ ÁN E-LEARNING")
    print("============================================================")

    # 1. Python Environment
    py = ensure_venv(check_only)
    missing: list[str] = []
    for import_name, pip_name in DEPS.items():
        if can_import(py, import_name):
            print(f"  [OK] {pip_name}")
        else:
            print(f"  [MISSING] {pip_name}")
            missing.append(pip_name)

    if missing:
        if check_only:
            print(f"\n[LỖI] Thiếu {len(missing)} thư viện Python: {', '.join(missing)}")
            sys.exit(1)
        if not install_python_deps(py, missing):
            sys.exit(1)

    # 2. FFmpeg Check
    print("\n------------------------------------------------------------")
    print("🎥 KIỂM TRA CÔNG CỤ XỬ LÝ VIDEO (FFmpeg)")
    print("------------------------------------------------------------")
    check_ffmpeg()

    # 3. HyperFrames Engine Setup
    setup_hyperframes_engine(check_only)

    print("\n============================================================")
    print("🎉 HỆ THỐNG ĐÃ SẴN SÀNG SẢN XUẤT CHO CÁC ENGINE:")
    print("   1. Whiteboard Animation với OpenCV (core/whiteboard_engine.py)")
    print("   2. Animation Tự Chủ với HyperFrames v2 (core/hf_engine.py)")
    print("   3. Diễn họa Toán/IT với Manim (core/manim_engine.py)")
    print("   4. Mô phỏng Hóa học 3D với 3Dmol.js (core/mol3d_engine.py)")
    print("   5. Vật lý Cơ học với Matter.js (core/matterjs_engine.py)")
    print("   6. Ký âm Âm nhạc với VexFlow (core/vexflow_engine.py)")
    print("   7. Bản đồ & Địa hình với CesiumJS (core/cesium_engine.py)")
    print("   8. Sinh học Phân tử với Molstar (core/molstar_engine.py)")
    print("   9. Thí nghiệm Ảo Khoa học Tự nhiên với Virtual Lab (core/virtual_lab_engine.py)")
    print(f"   Python Interpreter: {py}")
    print("============================================================\n")


if __name__ == "__main__":
    main()
