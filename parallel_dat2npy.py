import argparse
import glob
import numpy as np
from tqdm import tqdm
import os
import os.path
from concurrent.futures import ProcessPoolExecutor, as_completed

# ------------------ Argument Parser ------------------
parser = argparse.ArgumentParser(description="Convert .dat files to .npy format.")
parser.add_argument('--data-dir', type=str, default='.',
                    help='Directory containing .dat files (default: current directory)')
parser.add_argument('--out-dir', type=str, default='.',
                    help='Directory to save .npy files (default: current directory)')
parser.add_argument('--num-workers', type=int, default=None,
                    help='Number of parallel workers to use (default: number of CPU cores)')
args = parser.parse_args()

data_dir = os.path.abspath(args.data_dir)
out_dir = os.path.abspath(args.out_dir)
log_dir = os.getcwd()  # Current working directory

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# ------------------ Conversion Function ------------------
def convert_file(filepath):
    base_name = os.path.basename(filepath)
    output_path = os.path.join(out_dir, base_name.replace('.dat', '.npy'))

    if os.path.isfile(output_path):
        return (base_name, True, "skipped")

    try:
        x = np.genfromtxt(filepath, delimiter=' ')
        np.save(output_path, x)
        return (base_name, True, None)
    except Exception as e:
        return (base_name, False, str(e))

# ------------------ Parallel Execution ------------------
files = glob.glob(os.path.join(data_dir, '*.dat'))
good_files = []
bad_files = []

num_workers = args.num_workers or os.cpu_count()
with ProcessPoolExecutor(max_workers=num_workers) as executor:
    futures = [executor.submit(convert_file, f) for f in files]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Converting .dat to .npy"):
        base_name, success, msg = future.result()
        if success and msg != "skipped":
            good_files.append(base_name)
        elif not success:
            bad_files.append(base_name)

# ------------------ Save Logs ------------------
bad_log_path = os.path.join(log_dir, 'badfiles.txt')
good_log_path = os.path.join(log_dir, 'goodfiles.txt')

with open(bad_log_path, 'w') as f:
    for file in bad_files:
        f.write(file + '\n')

with open(good_log_path, 'w') as f:
    for file in good_files:
        f.write(file + '\n')

print(f"\nSaved {len(good_files)} good files to {good_log_path}")
print(f"Saved {len(bad_files)} bad files to {bad_log_path}")
