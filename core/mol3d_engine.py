#!/usr/bin/env python3
"""
core/mol3d_engine.py
Thư viện lõi điều phối Mô phỏng Hóa học & Cấu trúc Phân tử 3D cho Hệ thống E-Learning Antigravity.
- Chuyển đổi mã SMILES sang tọa độ không gian 3D tối ưu hóa năng lượng MMFF94 bằng RDKit.
- Sinh trang trực quan hóa WebGL phân tử chuẩn 16:9 Full HD bằng 3Dmol.js.
- Ghi hình chuyển động quay phân tử 360 độ siêu nét qua Puppeteer headless và FFmpeg.
- Đóng gói slide bài giảng PowerPoint (.pptx) và tài liệu PDF 16:9 chuẩn sư phạm.
- Ghép nối giọng đọc thuyết minh VieNeu-TTS v3 Turbo Nam Minh, nhạc nền Lo-Fi và phụ đề SRT ngắn.
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

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

# Từ điển ánh xạ tên hóa học tiếng Việt phổ biến sang mã SMILES
VIETNAMESE_COMPOUNDS = {
    "ethanol": "CCO",
    "cồn": "CCO",
    "cồn etylic": "CCO",
    "rượu etylic": "CCO",
    "axit axetic": "CC(=O)O",
    "giấm": "CC(=O)O",
    "etyl axetat": "CCOC(C)=O",
    "ethyl acetate": "CCOC(C)=O",
    "caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "cafein": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "axit axetylsalixylic": "CC(=O)Oc1ccccc1C(=O)O",
    "benzen": "c1ccccc1",
    "benzene": "c1ccccc1",
    "metan": "C",
    "methane": "C",
    "etilen": "C=C",
    "ethylene": "C=C",
    "axetilen": "C#C",
    "acetylene": "C#C",
    "nước": "O",
    "water": "O",
    "glucozo": "OCC1OC(O)C(O)C(O)C1O",
    "glucose": "OCC1OC(O)C(O)C(O)C1O",
    "fructozo": "OCC1(O)OC(CO)C(O)C1O",
    "saccarozo": "OCC1OC(OC2(CO)OC(CO)C(O)C2O)C(O)C(O)C1O",
}


class Mol3DEngine:
    def __init__(self, video_dir: Union[str, Path], runtime_dir: Optional[Union[str, Path]] = None):
        self.video_dir = Path(video_dir).resolve()
        self.runtime_dir = Path(runtime_dir).resolve() if runtime_dir else WORKSPACE_ROOT / "runtime"
        self.tasks_dir = self.runtime_dir / "tasks"
        self.cache_dir = self.runtime_dir / "cache" / "3dmol"
        self.output_dir = self.video_dir

        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.node_bin = "node"

    def resolve_smiles(self, query: str) -> str:
        """Nhận diện tên hợp chất hóa học hoặc trả về chuỗi SMILES tương ứng."""
        clean_query = query.strip().lower()
        if clean_query in VIETNAMESE_COMPOUNDS:
            return VIETNAMESE_COMPOUNDS[clean_query]
        # Nếu đã là chuỗi SMILES hợp lệ
        mol = Chem.MolFromSmiles(query)
        if mol:
            return query
        # Thử tìm kiếm mờ trong từ điển
        for name, smi in VIETNAMESE_COMPOUNDS.items():
            if name in clean_query or clean_query in name:
                return smi
        return query

    def smiles_to_sdf3d(self, smiles: str, output_sdf_path: Optional[Path] = None) -> tuple[Path, str]:
        """
        Chuyển mã SMILES thành file cấu trúc 3D (.sdf) bằng RDKit.
        - Thêm nguyên tử Hydro (Chem.AddHs)
        - Tính toán tọa độ không gian 3D (AllChem.EmbedMolecule ETKDG)
        - Tối ưu hóa năng lượng hình học (AllChem.MMFFOptimizeMolecule)
        """
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Không thể phân tích chuỗi SMILES: '{smiles}'")

        mol = Chem.AddHs(mol)
        params = AllChem.ETKDGv3()
        params.randomSeed = 42
        embed_status = AllChem.EmbedMolecule(mol, params)
        if embed_status != 0:
            # Fallback nếu ETKDGv3 không hội tụ
            AllChem.EmbedMolecule(mol, AllChem.ETKDG())

        try:
            AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
        except Exception:
            pass  # Vẫn giữ cấu trúc 3D ban đầu nếu lực trường MMFF không hỗ trợ nguyên tố đặc thù

        mol_block = Chem.MolToMolBlock(mol)

        if not output_sdf_path:
            output_sdf_path = self.tasks_dir / f"mol_{abs(hash(smiles)) % 100000}.sdf"

        output_sdf_path = Path(output_sdf_path).resolve()
        output_sdf_path.parent.mkdir(parents=True, exist_ok=True)

        writer = Chem.SDWriter(str(output_sdf_path))
        writer.write(mol)
        writer.close()

        print(f"🧪 [RDKit 3D] Đã sinh tọa độ 3D: {output_sdf_path.name}")
        return output_sdf_path, mol_block

    def get_molecule_properties(self, smiles: str, custom_name: str = "") -> dict:
        """Trích xuất công thức phân tử, khối lượng mol và phân bố nguyên tử."""
        mol = Chem.MolFromSmiles(smiles)
        mol_with_h = Chem.AddHs(mol)

        formula = rdMolDescriptors.CalcMolFormula(mol_with_h)
        weight = rdMolDescriptors.CalcExactMolWt(mol_with_h)
        num_atoms = mol_with_h.GetNumAtoms()
        num_bonds = mol_with_h.GetNumBonds()

        # Đếm chi tiết từng nguyên tố
        atom_counts = {}
        for atom in mol_with_h.GetAtoms():
            sym = atom.GetSymbol()
            atom_counts[sym] = atom_counts.get(sym, 0) + 1

        atoms_summary = ", ".join([f"{count}{sym}" for sym, count in atom_counts.items()])

        return {
            "name": custom_name or "Hợp Chất Hóa Học 3D",
            "smiles": smiles,
            "formula": formula,
            "molar_mass": f"{weight:.2f} g/mol",
            "num_atoms": num_atoms,
            "num_bonds": num_bonds,
            "atoms_summary": f"{num_atoms} nguyên tử ({atoms_summary})",
        }

    def generate_html_page(
        self,
        molecule_info: dict,
        mol_block: str,
        output_html_path: Path,
        template_path: Optional[Path] = None,
        feature_title: str = "Đặc Trưng Cấu Trúc & Liên Kết",
        feature_desc: str = "Phân tử thể hiện mô hình liên kết không gian 3D trực quan, tối ưu hóa năng lượng cấu hình.",
    ) -> Path:
        """Điền thông số và mã SDF vào HTML Template 3Dmol."""
        if not template_path:
            template_path = WORKSPACE_ROOT / "assets" / "templates" / "3dmol_view.html"

        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        lib_rel = os.path.relpath(WORKSPACE_ROOT / "assets" / "libs" / "3Dmol-min.js", output_html_path.parent).replace("\\", "/")
        html = html.replace("__LIB_3DMOL_PATH__", lib_rel)

        # Thay thế placeholder SDF và thông tin phân tử
        html = html.replace("__SDF_DATA_PLACEHOLDER__", mol_block)
        html = html.replace('id="slide-title">MÔ HÌNH KHÔNG GIAN 3D: ETHANOL (C₂H₆O)', f'id="slide-title">{molecule_info["name"].upper()} — {molecule_info["formula"]}')
        html = html.replace('id="prop-formula">C2H6O', f'id="prop-formula">{molecule_info["formula"]}')
        html = html.replace('id="prop-weight">46.07 g/mol', f'id="prop-weight">{molecule_info["molar_mass"]}')
        html = html.replace('id="prop-smiles">CCO', f'id="prop-smiles">{molecule_info["smiles"]}')
        html = html.replace('id="prop-atoms">9 nguyên tử (2C, 6H, 1O)', f'id="prop-atoms">{molecule_info["atoms_summary"]}')
        html = html.replace('id="feature-title">Nhóm Chức Hydroxyl (-OH) Phân Cực', f'id="feature-title">{feature_title}')
        html = html.replace('Liên kết O-H phân cực mạnh tạo liên kết Hydro liên phân tử, dẫn đến nhiệt độ sôi cao bất thường (78.3°C) và khả năng hòa tan vô hạn trong nước.', feature_desc)

        output_html_path = Path(output_html_path).resolve()
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"🌐 [3Dmol View] Đã xuất bản trang trực quan hóa: {output_html_path.name}")
        return output_html_path

    def render_still(self, html_path: Path, output_image_path: Path) -> Path:
        """Chụp snapshot WebGL tĩnh Full HD (1920x1080) bằng Puppeteer."""
        html_path = Path(html_path).resolve()
        output_image_path = Path(output_image_path).resolve()
        html_url = str(html_path.resolve()).replace("\\", "/")
        img_out = str(output_image_path.resolve()).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        puppeteer_script = f"""
const puppeteer = require('{puppeteer_mod}');
(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 600)); // Đợi WebGL render xong
  await page.evaluate(() => {{
    if (window.renderFrameAtTime) window.renderFrameAtTime(1.5);
  }});
  await page.screenshot({{ path: '{img_out}', type: 'png' }});
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_snap.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(puppeteer_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_image_path.exists():
            raise RuntimeError(f"Lỗi khi chụp still frame 3Dmol từ {html_path.name}")

        print(f"📸 [3Dmol Still] Đã chụp ảnh slide 16:9: {output_image_path.name}")
        return output_image_path

    def render_video(
        self,
        html_path: Path,
        output_mp4_path: Path,
        duration_sec: float = 10.0,
        fps: int = 30,
    ) -> Path:
        """
        Ghi hình chuyển động quay phân tử 3D mượt mà bằng Puppeteer và FFmpeg streaming.
        """
        html_path = Path(html_path).resolve()
        output_mp4_path = Path(output_mp4_path).resolve()
        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

        total_frames = int(round(duration_sec * fps))
        print(f"🎬 [3Dmol Video] Đang ghi hình phân tử 3D ({duration_sec}s, {total_frames} frames @ {fps}fps)...")

        html_url = str(html_path).replace("\\", "/")
        vid_out = str(output_mp4_path).replace("\\", "/")
        puppeteer_mod = str((WORKSPACE_ROOT / "engines" / "hyperframes" / "renderer" / "node_modules" / "puppeteer").resolve()).replace("\\", "/")

        # Kịch bản Node.js streaming frames vào stdout của process
        recorder_script = f"""
const puppeteer = require('{puppeteer_mod}');
const {{ spawn }} = require('child_process');

(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-webgl', '--use-gl=angle']
  }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1920, height: 1080 }});
  await page.goto('file://{html_url}', {{ waitUntil: 'networkidle0' }});
  await new Promise(r => setTimeout(r, 600));

  await page.evaluate(() => {{
    window.manualFrameControl = true;
  }});

  // Khởi chạy FFmpeg nhận stdin image2pipe
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', '{fps}',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-r', '{fps}',
    '{vid_out}'
  ], {{ stdio: ['pipe', 'inherit', 'inherit'] }});

  const totalFrames = {total_frames};
  const fps = {fps};

  for (let f = 0; f < totalFrames; f++) {{
    const t = f / fps;
    await page.evaluate((timeSec) => {{
      if (window.renderFrameAtTime) window.renderFrameAtTime(timeSec);
    }}, t);

    const buf = await page.screenshot({{ type: 'png' }});
    const canWrite = ffmpeg.stdin.write(buf);
    if (!canWrite) {{
      await new Promise(r => ffmpeg.stdin.once('drain', r));
    }}
  }}

  ffmpeg.stdin.end();
  await new Promise(resolve => ffmpeg.on('close', resolve));
  await browser.close();
}})();
"""
        script_file = self.tasks_dir / "temp_record.js"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(recorder_script)

        proc = subprocess.run([self.node_bin, str(script_file)], cwd=str(WORKSPACE_ROOT))
        if script_file.exists():
            script_file.unlink()

        if proc.returncode != 0 or not output_mp4_path.exists():
            raise RuntimeError(f"Lỗi khi render video 3Dmol từ {html_path.name}")

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
        """Ghép nối Video 3Dmol + Giọng đọc VieNeu-TTS v3 Turbo + Nhạc nền Lo-Fi + Phụ đề SRT."""
        raw_video = Path(raw_video).resolve()
        output_video = Path(output_video).resolve()
        output_video.parent.mkdir(parents=True, exist_ok=True)

        print(f"🎙️ [3Dmol Audio/SRT Integration] Đang đóng gói hoàn thiện video bài giảng Hóa học...")

        cmd = ["ffmpeg", "-y", "-i", str(raw_video)]

        has_narration = audio_path and Path(audio_path).exists()
        has_bgm = bgm_path and Path(bgm_path).exists()
        has_srt = srt_path and Path(srt_path).exists()

        if has_narration:
            cmd.extend(["-i", str(Path(audio_path).resolve())])
        if has_bgm:
            cmd.extend(["-stream_loop", "-1", "-i", str(Path(bgm_path).resolve())])

        filters = []
        if has_srt:
            escaped_srt = str(Path(srt_path).resolve()).replace("\\", "/").replace(":", "\\:")
            sub_filter = (
                f"subtitles='{escaped_srt}':force_style="
                "'Fontname=Be Vietnam Pro,FontSize=24,Bold=1,PrimaryColour=&H00FFFFFF,"
                "BackColour=&H900F172A,BorderStyle=4,Shadow=0,MarginV=35'"
            )
            filters.append(sub_filter)

        if filters:
            cmd.extend(["-vf", ",".join(filters)])

        if has_narration and has_bgm:
            cmd.extend([
                "-filter_complex",
                f"[1:a]volume=1.0[vocal];[2:a]volume={bgm_volume}[bgm];[vocal][bgm]amix=inputs=2:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]",
            ])
        elif has_narration:
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        elif has_bgm:
            cmd.extend(["-map", "0:v", "-map", "1:a"])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video),
        ])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("FFmpeg stderr:", proc.stderr)
            raise RuntimeError(f"FFmpeg thất bại khi ghép audio/subtitles cho {output_video.name}")

        print(f"🎉 [XUẤT SẮC] Video 3Dmol hoàn thiện: {output_video.name}")
        return output_video

    def export_slides(
        self,
        scenes_meta: list[dict],
        output_dir: Optional[Path] = None,
        format_type: str = "all",
        base_name: str = "slides_3dmol",
    ) -> dict[str, Path]:
        """Đóng gói các slide phân tử 3D tĩnh sang PowerPoint (.pptx) và PDF (.pdf)."""
        from core.pptx_engine import package_slides

        if not output_dir:
            output_dir = self.video_dir

        temp_slides_dir = self.runtime_dir / "temp_3dmol_slides"
        temp_slides_dir.mkdir(parents=True, exist_ok=True)

        captured_slides = []
        for i, sc in enumerate(scenes_meta, 1):
            html_p = sc.get("html_path")
            out_img = temp_slides_dir / f"slide_mol_{i}.png"
            img_p = self.render_still(Path(html_p), out_img)
            captured_slides.append(img_p)

        results = package_slides(captured_slides, output_dir, base_name, format_type)
        return results
