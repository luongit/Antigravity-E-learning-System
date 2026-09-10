"""
core/broll_manager.py
Hệ thống quản lý Thư viện Video Trám Cảnh (B-roll Video Library) cho E-Learning HyperFrames.
Hỗ trợ:
1. Quét và phân loại video minh họa theo chủ đề từ inputs/video-libraries/
2. Tự động kiểm tra thông số kỹ thuật (độ phân giải, fps, thời lượng thực tế)
3. Tính toán thời điểm trám cảnh (B-roll Cues) cho các đoạn thuyết minh dài (>15s)
4. Hỗ trợ 3 chế độ hiển thị: PiP Card (Khung thẻ bo góc), Split-Screen, Full Cutaway
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

try:
    import av
except ImportError:
    av = None


class BRollManager:
    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent
        else:
            self.workspace_root = workspace_root
        self.library_dir = self.workspace_root / "inputs" / "video-libraries"

    def scan_libraries(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Quét toàn bộ thư mục inputs/video-libraries/ và trả về cây danh mục video:
        {
          "ai-robotics": [
             {"filename": "robot_arm.mp4", "path": "...", "duration": 12.5, "width": 1920, "height": 1080}
          ],
          ...
        }
        """
        if not self.library_dir.exists():
            return {}

        results: Dict[str, List[Dict[str, Any]]] = {}
        supported_exts = (".mp4", ".webm", ".mov", ".m4v")

        for cat_dir in self.library_dir.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith((".", "_")):
                cat_name = cat_dir.name
                videos = []
                for vfile in sorted(cat_dir.iterdir()):
                    if vfile.is_file() and vfile.suffix.lower() in supported_exts:
                        info = self._get_video_info(vfile)
                        if info:
                            videos.append(info)
                if videos:
                    results[cat_name] = videos
        return results

    def _get_video_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Lấy thông số kỹ thuật video thực tế bằng PyAV."""
        rel_path = file_path.relative_to(self.workspace_root).as_posix()
        meta = {
            "name": file_path.stem,
            "filename": file_path.name,
            "path": rel_path,
            "abs_path": str(file_path),
            "duration": 10.0,
            "width": 1920,
            "height": 1080,
            "fps": 30.0
        }

        if av is not None:
            try:
                container = av.open(str(file_path))
                if container.duration is not None:
                    meta["duration"] = round(float(container.duration) / av.time_base, 2)
                video_stream = next((s for s in container.streams if s.type == "video"), None)
                if video_stream:
                    meta["width"] = video_stream.width
                    meta["height"] = video_stream.height
                    if video_stream.average_rate:
                        meta["fps"] = round(float(video_stream.average_rate), 2)
                container.close()
            except Exception:
                pass

        return meta

    def match_broll_for_slide(
        self,
        slide_title: str,
        voice_text: str,
        library_index: Optional[Dict[str, List[Dict[str, Any]]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Tìm kiếm video B-roll phù hợp nhất dựa trên từ khóa trong tiêu đề và lời thuyết minh:
        - ai-robotics: từ khóa AI, Robot, Trí tuệ nhân tạo, Công nghệ cao, Máy tính
        - business-corporate: từ khóa Doanh nghiệp, Kinh doanh, Quản trị, Hợp tác, Lãnh đạo
        - student-campus: từ khóa Sinh viên, Học sinh, Trường học, Đại học, Lớp học
        - general-tech: từ khóa Code, Lập trình, Phần mềm, Mạng, Dữ liệu
        """
        if library_index is None:
            library_index = self.scan_libraries()

        if not library_index:
            return None

        combined_text = f"{slide_title} {voice_text}".lower()

        topic_mapping = {
            "ai-robotics": ["trí tuệ nhân tạo", "ai", "robot", "robotics", "machine learning", "tự động hóa", "neural", "agent", "tác tử", "mô hình"],
            "công nghệ ảo lòi": ["ảo", "tương lai", "neon", "chip", "siêu máy tính", "hologram", "data center", "cloud"],
            "Lập trình": ["lập trình", "code", "phần mềm", "công nghệ thông tin", "mạng", "hệ thống", "database", "api", "java", "react", "spring boot", "backend", "frontend", "flutter"],
            "minh họa phần mềm": ["giao diện", "phần mềm", "dashboard", "biểu đồ", "phân tích", "hệ thống quản lý", "app"],
            "sử dụng máy tính": ["máy tính", "laptop", "thao tác", "gõ phím", "tra cứu", "làm việc số", "thiết bị"],
            "video chủ đề văn phòng": ["doanh nghiệp", "kinh doanh", "đối tác", "hợp tác", "thị trường", "quản trị", "chiến lược", "hội đồng", "văn phòng", "tuyển dụng", "nhân sự", "thực tế"],
            "pháp luật": ["luật", "pháp lý", "hợp đồng", "quy định", "chính sách", "điều khoản"]
        }

        best_category = None
        best_score = 0

        for cat, keywords in topic_mapping.items():
            if cat in library_index:
                score = sum(len(re.findall(rf"\b{re.escape(kw)}\b", combined_text)) for kw in keywords)
                if score > best_score:
                    best_score = score
                    best_category = cat

        if best_category and best_score > 0 and library_index.get(best_category):
            return library_index[best_category][0]

        # Fallback to any first available category
        for cat in ["Lập trình", "ai-robotics", "video chủ đề văn phòng", "sử dụng máy tính"]:
            if library_index.get(cat):
                return library_index[cat][0]

        return None

    def match_clips_for_semantic_cutaway(
        self,
        semantic_text: str,
        target_duration: float,
        library_index: Optional[Dict[str, List[Dict[str, Any]]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Ghép nối chuỗi video (Multi-Clip Chaining) cho một khoảng thời lượng trám cảnh:
        - Nếu target_duration <= 6s: dùng 1 clip phù hợp.
        - Nếu target_duration > 6s (ví dụ 10s-16s): ghép nối 2-3 clip liên tiếp để tạo nhịp phim tài liệu,
          tránh góc nhìn tĩnh đơn điệu.
        """
        if library_index is None:
            library_index = self.scan_libraries()

        if not library_index:
            return []

        # Xác định category phù hợp
        primary_clip = self.match_broll_for_slide("", semantic_text, library_index)
        if not primary_clip:
            return []

        # Tìm các clip thuộc cùng category hoặc category bổ trợ
        category_name = None
        for cat, clips in library_index.items():
            if any(c["filename"] == primary_clip["filename"] for c in clips):
                category_name = cat
                break

        available_clips = list(library_index.get(category_name, []))
        if len(available_clips) < 2:
            # Thêm clip từ category liên quan
            for cat, clips in library_index.items():
                if cat != category_name and clips:
                    available_clips.extend(clips)

        # Tính toán phân bổ thời gian cho từng clip
        result_sequence = []
        rem_dur = round(target_duration, 2)
        clip_idx = 0
        current_offset = 0.0

        while rem_dur > 0.5 and available_clips:
            clip_meta = available_clips[clip_idx % len(available_clips)]
            # Thời lượng mỗi phân đoạn clip: lý tưởng từ 4.5s đến 7.0s
            if rem_dur <= 7.0:
                seg_dur = rem_dur
            else:
                seg_dur = round(min(rem_dur / 2.0, 6.0), 2)
                if seg_dur < 4.0:
                    seg_dur = rem_dur

            result_sequence.append({
                "clip": clip_meta,
                "offset": current_offset,
                "duration": seg_dur,
                "video_src": clip_meta["path"]
            })

            current_offset = round(current_offset + seg_dur, 2)
            rem_dur = round(rem_dur - seg_dur, 2)
            clip_idx += 1

        return result_sequence

    def generate_semantic_cutaway_html(
        self,
        cutaway_plan: Dict[str, Any],
        scene_id: str
    ) -> str:
        """
        Sinh đoạn mã HTML/CSS cho phân đoạn trám cảnh ngữ nghĩa (hỗ trợ cả Single-clip và Multi-clip Chaining):
        - cutaway_plan: {
            "start_time": 10.5,
            "duration": 12.0,
            "badge_text": "BỐI CẢNH THỰC TẾ DOANH NGHIỆP",
            "clips": [ {"video_src": "...", "offset": 0.0, "duration": 6.0}, ... ]
          }
        """
        start = cutaway_plan.get("start_time", 0.0)
        dur = cutaway_plan.get("duration", 6.0)
        badge = cutaway_plan.get("badge_text", "MINH HỌA THỰC TIỄN")
        clips = cutaway_plan.get("clips", [])

        if not clips:
            return ""

        videos_html = []
        for i, c in enumerate(clips):
            c_offset = c.get("offset", 0.0)
            c_dur = c.get("duration", dur)
            v_src = c.get("video_src", "")
            # Clip đầu tiên hiển thị ngay, các clip sau xuất hiện tại offset tương ứng
            videos_html.append(f"""
            <div class="broll-chain-item" style="position: absolute; inset: 0; opacity: {'1' if i == 0 else '0'};" data-chain-start="{round(start + c_offset, 2)}" data-chain-dur="{c_dur}">
              <video src="{v_src}" muted playsinline loop style="width: 100%; height: 100%; object-fit: cover;"></video>
            </div>""")

        return f"""
        <!-- Semantic Full-Screen Cutaway (Start: {start}s, Dur: {dur}s, Clips: {len(clips)}) -->
        <div class="semantic-cutaway-overlay" style="position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; z-index: 500; opacity: 0; pointer-events: none;" data-cutaway-start="{start}" data-cutaway-dur="{dur}">
          {''.join(videos_html)}
          <div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(15,23,42,0.4) 0%, rgba(15,23,42,0.15) 50%, rgba(15,23,42,0.85) 100%);"></div>
          <div style="position: absolute; top: 96px; left: 80px; z-index: 600; display: inline-flex; align-items: center; gap: 8px; background: rgba(15,23,42,0.75); border: 1px solid rgba(56,189,248,0.4); backdrop-filter: blur(12px); color: #38BDF8; font-size: 13px; font-weight: 700; padding: 6px 14px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #38BDF8; display: inline-block;"></span>
            {badge}
          </div>
        </div>
"""


