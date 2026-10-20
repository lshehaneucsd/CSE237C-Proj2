import os
import shutil
from pathlib import Path

variants = ['12', '14', '16', '18', '20']
original_name = 'cordiccart2pol_12.h'

script_dir = Path(__file__).resolve().parent
target_dir = script_dir.parent / 'project2' / 'cordic' / 'HLS' / 'cordic' / 'questions' / 'q1'
src_path = target_dir / original_name

prefix, rest = original_name.split('_', 1)
middle, ext = rest.rsplit('.', 1)

for variant in variants:
    dest_path = target_dir / f"{prefix}_{variant}.{ext}"
    if dest_path != src_path:
        shutil.copyfile(src_path, dest_path)