import argparse
import glob
import numpy as np
from tqdm import tqdm
import os
import os.path

# ------------------ Argument Parser ------------------
parser = argparse.ArgumentParser(description="Convert .dat files to .npy format.")
parser.add_argument('--data-dir', type=str, default='.',
                    help='Directory containing .dat files (default: current directory)')
parser.add_argument('--out-dir', type=str, default='.',
                    help='Directory to save .npy files (default: current directory)')
args = parser.parse_args()

data_dir = os.path.abspath(args.data_dir)
out_dir = os.path.abspath(args.out_dir)
log_dir = os.getcwd()  # Current working directory

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# ------------------ File Conversion ------------------
files = glob.glob(os.path.join(data_dir, '*.dat'))

bad_files = []
good_files = []

for tmp in tqdm(files, desc="Converting .dat to .npy"):
    base_name = os.path.basename(tmp)
    tmp_np = os.path.join(out_dir, base_name.replace('.dat', '.npy'))

    if os.path.isfile(tmp_np):
        print(f"File {tmp_np} exists... skipping.")
    else:
        try:
            x = np.genfromtxt(tmp, delimiter=' ')
            np.save(tmp_np, x)
            good_files.append(base_name)
        except Exception as e:
            print(f"File {tmp} cannot be exported to npy: {e}")
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
