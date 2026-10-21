import os
import shutil
from pathlib import Path

variants = ['10', '12', '14', '16', '18', '20']
original_name = 'cordiccart2pol_10.h'

script_dir = Path(__file__).resolve().parent
target_dir = script_dir.parent / 'project2' / 'cordic' / 'HLS' / 'cordic' / 'questions' / 'q1'
src_path = target_dir / original_name

if src_path.exists():
    with open(src_path, 'r') as f:
        template = f.read()

    for variant in variants:
        dest_path = target_dir / f"cordiccart2pol_{variant}.h"
        content = re.sub(r'#define\s+NO_ITER\s+\d+', f'#define NO_ITER {variant}', template)
        with open(dest_path, 'w') as f:
            f.write(content)