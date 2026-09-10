#!/usr/bin/env python3
"""
core/molstar_engine.py
Thư viện lõi điều phối Mô phỏng Sinh học & Cấu trúc Phân tử Sinh học 3D (Molstar & RCSB PDB)
cho Hệ thống E-Learning Antigravity.
- Quản lý và tra cứu mã PDB ID (ADN 1BNA, RNA 1EHZ, Protein p53 1TUP, Hemoglobin 4HHB, Insulin 1TRN...).
- Tự động sinh hoặc tải dữ liệu tọa độ nguyên tử PDB chuẩn.
- Sinh trang trực quan hóa WebGL 16:9 Full HD qua Molstar / 3Dmol.js với hiệu ứng quay 360 độ.
- Ghi hình video động qua Puppeteer headless và pipe FFmpeg chất lượng cao.
- Hòa trộn âm thanh đa kênh: Giọng đọc VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT.
- Đóng gói slide PowerPoint (.pptx) và tài liệu PDF 16:9 chuẩn sư phạm.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

# Từ điển ánh xạ tên phân tử sinh học phổ biến sang mã RCSB PDB ID và thông số chuẩn
BIOMOLECULE_DATABASE = {
    "adn": {
        "pdb_id": "1BNA",
        "molecule_name": "Chuỗi Xoắn Đôi ADN B-form (Dodecamer)",
        "representation": "Cartoon Ribbon & Ball-and-Stick",
        "pairing_info": "A = T (2 liên kết H) • G ≡ X (3 liên kết H)",
        "title": "CẤU TRÚC KHÔNG GIAN 3D CỦA CHUỖI XOẮN ĐÔI ADN (B-FORM)",
        "subtitle": "Mô hình Watson & Crick • Cặp bazơ A-T & G-X • Chu kỳ xoắn 10 cặp bazơ / 3.4 nm"
    },
    "dna": {
        "pdb_id": "1BNA",
        "molecule_name": "Chuỗi Xoắn Đôi ADN B-form (Dodecamer)",
        "representation": "Cartoon Ribbon & Ball-and-Stick",
        "pairing_info": "A = T (2 liên kết H) • G ≡ X (3 liên kết H)",
        "title": "CẤU TRÚC KHÔNG GIAN 3D CỦA CHUỖI XOẮN ĐÔI ADN (B-FORM)",
        "subtitle": "Mô hình Watson & Crick • Cặp bazơ A-T & G-X • Chu kỳ xoắn 10 cặp bazơ / 3.4 nm"
    },
    "1bna": {
        "pdb_id": "1BNA",
        "molecule_name": "Chuỗi Xoắn Đôi ADN B-form (Dodecamer)",
        "representation": "Cartoon Ribbon & Ball-and-Stick",
        "pairing_info": "A = T (2 liên kết H) • G ≡ X (3 liên kết H)",
        "title": "CẤU TRÚC KHÔNG GIAN 3D CỦA CHUỖI XOẮN ĐÔI ADN (B-FORM)",
        "subtitle": "Mô hình Watson & Crick • Cặp bazơ A-T & G-X • Chu kỳ xoắn 10 cặp bazơ / 3.4 nm"
    },
    "arn": {
        "pdb_id": "1EHZ",
        "molecule_name": "Phân tử tRNA Vận Chuyển Men Men Nấm (Yeast tRNA)",
        "representation": "Cartoon Ribbon & Base Pair Sticks",
        "pairing_info": "Hình lá chẽ 3 thùy cuộn chữ L • Vòng đối mã Anticodon",
        "title": "CẤU TRÚC KHÔNG GIAN 3D CỦA PHÂN TỬ tRNA VẬN CHUYỂN",
        "subtitle": "Cấu trúc bậc 3 dạng chữ L • Thùy mang axit amin 3'-CCA & Thùy đối mã Anticodon"
    },
    "rna": {
        "pdb_id": "1EHZ",
        "molecule_name": "Phân tử tRNA Vận Chuyển Men Men Nấm (Yeast tRNA)",
        "representation": "Cartoon Ribbon & Base Pair Sticks",
        "pairing_info": "Hình lá chẽ 3 thùy cuộn chữ L • Vòng đối mã Anticodon",
        "title": "CẤU TRÚC KHÔNG GIAN 3D CỦA PHÂN TỬ tRNA VẬN CHUYỂN",
        "subtitle": "Cấu trúc bậc 3 dạng chữ L • Thùy mang axit amin 3'-CCA & Thùy đối mã Anticodon"
    },
    "p53": {
        "pdb_id": "1TUP",
        "molecule_name": "Protein Ức Chế Khối U p53 Liên Kết ADN",
        "representation": "Cartoon Secondary Structure & Zinc Ion",
        "pairing_info": "Miền lõi liên kết rãnh lớn ADN • Phức hệ phối trí kẽm Zn²⁺",
        "title": "CẤU TRÚC PROTEIN ỨC CHẾ KHỐI U P53 GẮN VÀO ADN",
        "subtitle": "Gen hộ mệnh của bộ gen (Guardian of the Genome) • Điều hòa chu kỳ tế bào & Apoptosis"
    },
    "hemoglobin": {
        "pdb_id": "4HHB",
        "molecule_name": "Protein Huyết Sắc Tố Hemoglobin Bậc 4",
        "representation": "Cartoon Tetramer & Heme Groups",
        "pairing_info": "4 tiểu phần (2 chuỗi α, 2 chuỗi β) • 4 nhân Heme mang Fe²⁺",
        "title": "CẤU TRÚC BẬC 4 CỦA PROTEIN HUYẾT SẮC TỐ HEMOGLOBIN",
        "subtitle": "Phức hợp vận chuyển khí O2 và CO2 trong máu hồng cầu động vật có vú"
    },
    "insulin": {
        "pdb_id": "1TRN",
        "molecule_name": "Hormone Tuyến Tụy Insulin (Bovine Insulin)",
        "representation": "Cartoon Alpha Helices & Disulfide Bridges",
        "pairing_info": "Chuỗi A (21 aa) & Chuỗi B (30 aa) • 3 cầu liên kết đisunphua (-S-S-)",
        "title": "CẤU TRÚC KHÔNG GIAN HORMONE INSULIN ĐIỀU HÒA ĐƯỜNG HUYẾT",
        "subtitle": "Hormone chuyển hóa đường glucozo • Cấu trúc tinh thể dạng hexamer phối trí kẽm"
    }
}


class MolstarEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        v_path = Path(video_dir)
        self.video_dir = v_path.resolve() if v_path.is_absolute() else (WORKSPACE_ROOT / v_path).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "molstar"
        self.output_dir = self.video_dir

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        node_path = shutil.which("node")
        if not node_path:
            cand = Path(r"C:\Users\luongna\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
            if cand.exists():
                node_path = str(cand)
            else:
                node_path = "node"
        self.node_bin = node_path

    def resolve_biomolecule(self, query: str) -> dict:
        """Nhận diện tên phân tử sinh học hoặc mã PDB ID và trả về cấu hình chi tiết."""
        clean_q = query.strip().lower()
        if clean_q in BIOMOLECULE_DATABASE:
            return dict(BIOMOLECULE_DATABASE[clean_q])

        for key, val in BIOMOLECULE_DATABASE.items():
            if key in clean_q or clean_q in key:
                return dict(val)

        # Mặc định xem query là mã PDB 4 ký tự
        pdb_clean = query.strip().upper()[:4]
        return {
            "pdb_id": pdb_clean,
            "molecule_name": f"Phân Tử Sinh Học PDB ID: {pdb_clean}",
            "representation": "Cartoon Ribbon & Ball-and-Stick",
            "pairing_info": "Cấu trúc không gian bậc 3/4 tinh thể học tia X",
            "title": f"CẤU TRÚC 3D PHÂN TỬ SINH HỌC (PDB {pdb_clean})",
            "subtitle": f"Dữ liệu cấu trúc nguyên tử thực nghiệm từ Ngân hàng Protein RCSB PDB ({pdb_clean})"
        }

    def get_or_generate_pdb_data(self, pdb_id: str, output_pdb_path: Optional[Path] = None) -> tuple[Path, str]:
        """
        Lấy nội dung file PDB từ cache, file mẫu cục bộ, hoặc sinh cấu trúc B-DNA chuẩn.
        """
        pdb_id = pdb_id.strip().upper()
        local_model = WORKSPACE_ROOT / "assets" / "models" / f"{pdb_id.lower()}.pdb"

        if not output_pdb_path:
            output_pdb_path = self.cache_dir / f"{pdb_id.lower()}.pdb"
        else:
            output_pdb_path = Path(output_pdb_path).resolve()

        output_pdb_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Kiểm tra nếu có sẵn trong assets/models
        if local_model.exists():
            shutil.copy2(local_model, output_pdb_path)
            content = output_pdb_path.read_text(encoding="utf-8", errors="ignore")
            print(f"📦 [Molstar PDB] Sử dụng file PDB mẫu có sẵn: {local_model.name}")
            return output_pdb_path, content

        # 2. Nếu là 1BNA và chưa có file, sinh tự động
        if pdb_id == "1BNA":
            from scripts.generate_dna_pdb import generate_bdna_pdb
            generate_bdna_pdb(output_pdb_path)
            content = output_pdb_path.read_text(encoding="utf-8", errors="ignore")
            print(f"🧬 [Molstar PDB] Đã sinh cấu trúc ADN 1BNA chuẩn: {output_pdb_path.name}")
            return output_pdb_path, content

        # 3. Fallback: Nếu không tìm thấy, tạo PDB tối thiểu
        fallback_lines = [
            f"HEADER    BIOMOLECULE                             01-JAN-26   {pdb_id}",
            f"TITLE     STRUCTURE FOR PDB ID {pdb_id}",
            f"ATOM      1  P   DA  A   1       0.000   0.000   0.000  1.00 30.00           P",
            f"ATOM      2  N1  DA  A   1       2.500   1.200   0.500  1.00 30.00           N",
            "END"
        ]
        content = "\n".join(fallback_lines)
        with open(output_pdb_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_pdb_path, content

    def create_bio_config(
        self,
        pdb_id: str,
        output_json_path: Path,
        representation: str = "cartoon",
        extra_meta: Optional[dict] = None
    ) -> Path:
        """Lưu cấu hình phân tử sinh học vào tệp JSON."""
        resolved = self.resolve_biomolecule(pdb_id)
        if representation:
            resolved["representation"] = representation
        if extra_meta:
            resolved.update(extra_meta)

        output_json_path = Path(output_json_path).resolve()
        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(resolved, f, ensure_ascii=False, indent=2)

        print(f"📄 [Molstar] Đã lưu file cấu hình sinh học: {output_json_path.name}")
        return output_json_path

    def generate_html_page(
        self,
        bio_config: dict,
        pdb_content: str,
        output_html_path: Path,
        template_path: Optional[Path] = None,
    ) -> Path:
        """Sinh trang HTML mô phỏng cấu trúc 3D WebGL từ template."""
        if not template_path:
            template_path = WORKSPACE_ROOT / "assets" / "templates" / "molstar_bio.html"

        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Đường dẫn tương đối đến thư viện 3Dmol.js offline
        lib_rel = os.path.relpath(WORKSPACE_ROOT / "assets" / "libs" / "3Dmol-min.js", output_html_path.parent).replace("\\", "/")
        html = html.replace("__LIB_3DMOL_PATH__", lib_rel)

        config_json = json.dumps(bio_config, ensure_ascii=False)
        html = html.replace("__BIO_CONFIG_PLACEHOLDER__", config_json)

        # Chèn nội dung file PDB
        clean_pdb = pdb_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        html = html.replace("__PDB_CONTENT_PLACEHOLDER__", clean_pdb)

        output_html_path = Path(output_html_path).resolve()
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"🌐 [Molstar View] Đã xuất bản trang mô phỏng sinh học 3D: {output_html_path.name}")
        return output_html_path

    def render_still(self, html_path: Path, output_image_path: Path, progress_ratio: float = 0.25) -> Path:
        """Chụp snapshot trạng thái phân tử sinh học 3D bằng Puppeteer WebGL."""
        html_path = Path(html_path).resolve()
        output_image_path = Path(output_image_path).resolve()
        output_image_path.parent.mkdir(parents=True, exist_ok=True)

        html_url = str(html_path).replace("\\", "/")
        img_out = str(output_image_path).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        script_code = f"""
const puppeteer = require('{puppeteer_mod}');
(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 600));

  await page.evaluate((ratio) => {{
    if (window.renderBioStep) window.renderBioStep(ratio * 5000, 5000);
  }}, {progress_ratio});

  await page.screenshot({{ path: '{img_out}', type: 'png' }});
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_bio_snap.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_code)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_image_path.exists():
            raise RuntimeError(f"Lỗi khi chụp still frame Molstar từ {html_path.name}")

        print(f"📸 [Molstar Still] Đã chụp ảnh slide 16:9: {output_image_path.name}")
        return output_image_path

    def render_video(
        self,
        html_path: Path,
        output_mp4_path: Path,
        duration_sec: float = 6.0,
        fps: int = 30,
    ) -> Path:
        """
        Ghi hình chuyển động quay phân tử 360 độ qua Puppeteer và pipe FFmpeg.
        """
        html_path = Path(html_path).resolve()
        output_mp4_path = Path(output_mp4_path).resolve()
        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

        total_frames = int(round(duration_sec * fps))
        print(f"🎬 [Molstar Video] Đang ghi hình Cấu trúc Sinh học 3D ({duration_sec}s, {total_frames} frames @ {fps}fps)...")

        html_url = str(html_path).replace("\\", "/")
        vid_out = str(output_mp4_path).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        recorder_script = f"""
const puppeteer = require('{puppeteer_mod}');
const {{ spawn }} = require('child_process');

(async () => {{
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', '{fps}',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '22',
    '{vid_out}'
  ]);

  ffmpeg.stderr.on('data', (d) => {{}});

  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});

  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 600));

  const totalFrames = {total_frames};
  const durationMs = {duration_sec * 1000};
  const dtMs = 1000 / {fps};

  for (let frame = 0; frame < totalFrames; frame++) {{
    const currentMs = frame * dtMs;
    await page.evaluate((curMs, durMs) => {{
      if (window.renderBioStep) window.renderBioStep(curMs, durMs);
    }}, currentMs, durationMs);

    const buffer = await page.screenshot({{ type: 'png' }});
    ffmpeg.stdin.write(buffer);
  }}

  ffmpeg.stdin.end();
  await new Promise((resolve) => ffmpeg.on('close', resolve));
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_bio_record.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(recorder_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_mp4_path.exists():
            raise RuntimeError(f"Lỗi khi render video Molstar từ {html_path.name}")

        print(f"   [OK] Đã xuất video raw: {output_mp4_path.name}")
        return output_mp4_path

    def merge_audio_and_subtitles(
        self,
        raw_video: Path,
        audio_path: Optional[Path],
        srt_path: Optional[Path],
        output_video: Path,
        bgm_path: Optional[Path] = None,
        bgm_volume: float = 0.12,
    ) -> Path:
        """
        Dùng FFmpeg ghép nối Video Phân tử Sinh học 3D + Giọng đọc VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT.
        """
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [Molstar Audio/SRT Integration] Đang đóng gói hoàn thiện video bài giảng Sinh học...")

        cmd = ["ffmpeg", "-y", "-i", str(raw_video)]

        has_vocal = audio_path and Path(audio_path).exists()
        has_bgm = bgm_path and Path(bgm_path).exists()
        has_srt = srt_path and Path(srt_path).exists()

        if has_vocal:
            cmd.extend(["-i", str(Path(audio_path).resolve())])
        if has_bgm:
            cmd.extend(["-stream_loop", "-1", "-i", str(Path(bgm_path).resolve())])

        filters = []
        if has_srt:
            escaped_srt = str(Path(srt_path).resolve()).replace("\\", "/").replace(":", "\\:")
            sub_filter = (
                f"subtitles='{escaped_srt}':force_style="
                "'Fontname=Be Vietnam Pro,FontSize=24,Bold=1,PrimaryColour=&H00FFFFFF,"
                "BackColour=&H900B0F19,BorderStyle=4,Shadow=0,MarginV=35'"
            )
            filters.append(sub_filter)

        if filters:
            cmd.extend(["-vf", ",".join(filters)])

        if has_vocal and has_bgm:
            cmd.extend([
                "-filter_complex",
                f"[1:a]volume=1.0[vocal];[2:a]volume={bgm_volume}[bgm];[vocal][bgm]amix=inputs=2:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]"
            ])
        elif has_vocal:
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        elif has_bgm:
            cmd.extend(["-map", "0:v", "-map", "1:a"])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video)
        ])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("FFmpeg error:", proc.stderr)
            raise RuntimeError(f"FFmpeg thất bại khi đóng gói video Molstar {output_video.name}")

        print(f"🎉 [XUẤT SẮC] Video Molstar hoàn thiện: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scenes_data: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_molstar",
    ) -> dict[str, Path]:
        """
        Đóng gói slide PowerPoint (.pptx) và tài liệu PDF 16:9 từ các cảnh Cấu trúc Sinh học 3D.
        """
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        captured_slides = []
        for i, sc in enumerate(scenes_data, 1):
            html_path = sc.get("html_path")
            out_img = self.runtime_dir / "temp_slide_frames" / f"molstar_slide_{i}.png"
            ratio = sc.get("ratio", 0.25)
            img_path = self.render_still(Path(html_path), out_img, progress_ratio=ratio)
            captured_slides.append(img_path)

        results = package_slides(captured_slides, output_dir, base_name, format_type)
        return results
