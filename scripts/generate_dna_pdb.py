#!/usr/bin/env python3
"""
scripts/generate_dna_pdb.py
Tạo tệp PDB chuẩn cho Chuỗi xoắn đôi ADN B-form (1BNA Dodecamer)
Chuỗi: CGCGAATTCGCG (12 cặp bazơ, 24 nucleotide, 2 chuỗi xoắn đối song song 5'->3' và 3'->5')
"""

import math
from pathlib import Path

def generate_bdna_pdb(output_path: Path):
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    seq_strand_a = "CGCGAATTCGCG"
    comp_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    seq_strand_b = "".join([comp_map[b] for b in reversed(seq_strand_a)])

    lines = []
    lines.append("HEADER    DNA (DEOXYRIBONUCLEIC ACID)             28-JAN-26   1BNA")
    lines.append("TITLE     CRYSTAL STRUCTURE OF AN ALTERNATING B-DNA DODECAMER")
    lines.append("COMPND    MOL_ID: 1; MOLECULE: B-DNA (5'-D(*CP*GP*CP*GP*AP*AP*TP*TP*CP*GP*CP*G)-3');")

    atom_id = 1
    # B-DNA geometry parameters
    # 10.5 bp / turn -> twist = 34.3 deg (0.598 rad)
    # rise = 3.38 A
    twist_rad = math.radians(34.28)
    rise_a = 3.38
    r_phos = 9.4
    r_sugar = 6.8
    r_base_center = 2.8

    # Strand A: 5' to 3'
    for i, base_char in enumerate(seq_strand_a, 1):
        res_name = f"D{base_char}"
        theta = (i - 1) * twist_rad
        z = (i - 1) * rise_a

        # Phosphate (skip for 5' terminal i=1 or include)
        px = r_phos * math.cos(theta)
        py = r_phos * math.sin(theta)
        lines.append(f"ATOM  {atom_id:5d}  P   {res_name:3s} A{i:4d}    {px:8.3f}{py:8.3f}{z:8.3f}  1.00 45.00           P")
        atom_id += 1

        op1x = (r_phos + 1.2) * math.cos(theta + 0.1)
        op1y = (r_phos + 1.2) * math.sin(theta + 0.1)
        lines.append(f"ATOM  {atom_id:5d}  OP1 {res_name:3s} A{i:4d}    {op1x:8.3f}{op1y:8.3f}{z+0.8:8.3f}  1.00 45.00           O")
        atom_id += 1

        # Sugar ring (C4', O4', C1', C2', C3')
        sx = r_sugar * math.cos(theta + 0.18)
        sy = r_sugar * math.sin(theta + 0.18)
        lines.append(f"ATOM  {atom_id:5d}  C4' {res_name:3s} A{i:4d}    {sx:8.3f}{sy:8.3f}{z+0.5:8.3f}  1.00 40.00           C")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  O4' {res_name:3s} A{i:4d}    {sx-0.8*math.cos(theta):8.3f}{sy-0.8*math.sin(theta):8.3f}{z+0.6:8.3f}  1.00 40.00           O")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  C1' {res_name:3s} A{i:4d}    {sx-1.3*math.cos(theta):8.3f}{sy-1.3*math.sin(theta):8.3f}{z+0.3:8.3f}  1.00 40.00           C")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  C3' {res_name:3s} A{i:4d}    {sx+0.3*math.cos(theta):8.3f}{sy+0.3*math.sin(theta):8.3f}{z+1.5:8.3f}  1.00 40.00           C")
        atom_id += 1

        # Base atoms extending towards central axis
        bx = r_base_center * math.cos(theta + 0.45)
        by = r_base_center * math.sin(theta + 0.45)
        n_name = "N9" if base_char in ['A', 'G'] else "N1"
        lines.append(f"ATOM  {atom_id:5d}  {n_name:3s} {res_name:3s} A{i:4d}    {bx+1.2*math.cos(theta+0.45):8.3f}{by+1.2*math.sin(theta+0.45):8.3f}{z+0.2:8.3f}  1.00 35.00           N")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  C6  {res_name:3s} A{i:4d}    {bx:8.3f}{by:8.3f}{z:8.3f}  1.00 35.00           C")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  N1  {res_name:3s} A{i:4d}    {bx-0.8*math.cos(theta+0.45):8.3f}{by-0.8*math.sin(theta+0.45):8.3f}{z:8.3f}  1.00 35.00           N")
        atom_id += 1

    # Strand B: 3' to 5' (antiparallel, offset by ~144 deg / 2.5 rad across major/minor groove)
    delta_strand = math.pi + math.radians(36.0)
    for i, base_char in enumerate(seq_strand_b, 1):
        res_name = f"D{base_char}"
        idx_pair = 13 - i
        theta = (idx_pair - 1) * twist_rad + delta_strand
        z = (idx_pair - 1) * rise_a

        px = r_phos * math.cos(theta)
        py = r_phos * math.sin(theta)
        lines.append(f"ATOM  {atom_id:5d}  P   {res_name:3s} B{i:4d}    {px:8.3f}{py:8.3f}{z:8.3f}  1.00 45.00           P")
        atom_id += 1

        op1x = (r_phos + 1.2) * math.cos(theta - 0.1)
        op1y = (r_phos + 1.2) * math.sin(theta - 0.1)
        lines.append(f"ATOM  {atom_id:5d}  OP1 {res_name:3s} B{i:4d}    {op1x:8.3f}{op1y:8.3f}{z-0.8:8.3f}  1.00 45.00           O")
        atom_id += 1

        sx = r_sugar * math.cos(theta - 0.18)
        sy = r_sugar * math.sin(theta - 0.18)
        lines.append(f"ATOM  {atom_id:5d}  C4' {res_name:3s} B{i:4d}    {sx:8.3f}{sy:8.3f}{z-0.5:8.3f}  1.00 40.00           C")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  O4' {res_name:3s} B{i:4d}    {sx-0.8*math.cos(theta):8.3f}{sy-0.8*math.sin(theta):8.3f}{z-0.6:8.3f}  1.00 40.00           O")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  C1' {res_name:3s} B{i:4d}    {sx-1.3*math.cos(theta):8.3f}{sy-1.3*math.sin(theta):8.3f}{z-0.3:8.3f}  1.00 40.00           C")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  C3' {res_name:3s} B{i:4d}    {sx+0.3*math.cos(theta):8.3f}{sy+0.3*math.sin(theta):8.3f}{z-1.5:8.3f}  1.00 40.00           C")
        atom_id += 1

        bx = r_base_center * math.cos(theta - 0.45)
        by = r_base_center * math.sin(theta - 0.45)
        n_name = "N9" if base_char in ['A', 'G'] else "N1"
        lines.append(f"ATOM  {atom_id:5d}  {n_name:3s} {res_name:3s} B{i:4d}    {bx+1.2*math.cos(theta-0.45):8.3f}{by+1.2*math.sin(theta-0.45):8.3f}{z-0.2:8.3f}  1.00 35.00           N")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  C6  {res_name:3s} B{i:4d}    {bx:8.3f}{by:8.3f}{z:8.3f}  1.00 35.00           C")
        atom_id += 1
        lines.append(f"ATOM  {atom_id:5d}  N1  {res_name:3s} B{i:4d}    {bx-0.8*math.cos(theta-0.45):8.3f}{by-0.8*math.sin(theta-0.45):8.3f}{z:8.3f}  1.00 35.00           N")
        atom_id += 1

    lines.append("END")

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated B-DNA PDB: {output_path} ({len(lines)} lines)")
    return output_path

if __name__ == "__main__":
    out = Path("E:/Soft/E-Learning/Hyperframes E-learning/assets/models/1bna.pdb")
    generate_bdna_pdb(out)
