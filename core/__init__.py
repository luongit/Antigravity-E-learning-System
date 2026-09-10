"""
core module
Chứa các động cơ cốt lõi (Core Engines) của hệ thống E-Learning Whiteboard Animation:
- preflight: Kiểm tra điều kiện tiên quyết & định tuyến
- voice_parser: Phân tích file Voice Script từ người dùng
- whiteboard_engine: Động cơ vẽ phác thảo Whiteboard Canny Edge & Hand Overlay
- audio_tts_engine: Động cơ sinh giọng đọc TTS (Edge/Piper) & tạo SRT phân đoạn ngắn
- pptx_engine: Đóng gói bài giảng PowerPoint 16:9
"""

from core.voice_parser import parse_voice_script
from core.preflight import PreflightChecker
