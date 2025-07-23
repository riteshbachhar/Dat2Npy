# Dat2Npy

**Dat2Npy** is a lightweight command-line utility for converting `.dat` files to `.npy` (NumPy) format using Python and shell scripting. It provides a simple interface for batch-processing large datasets and keeps track of successfully and unsuccessfully converted files.

---

## Features

- Converts `.dat` files to `.npy` format
- Generates two log files:
  - `goodfiles.txt` – list of files successfully converted
  - `badfiles.txt` – list of files that failed during conversion

---

## Usage

### Option 1: Run the Python Script Directly

```bash
git clone https://github.com/yourusername/Dat2Npy.git
cd Dat2Npy

python dat2npy.py --data-dir $DATAPATH --out-dir $OUTPATH
```

- --data-dir: Path to the directory containing .dat files
- --out-dir: Path to the directory where .npy files will be saved


### Option 2: Run the Bash Script for Batch Jobs

Use this when integrating into batch systems or job schedulers.

1. Make the script executable:
```bash
chmod +x dat2npy.sh
```

2. Edit dat2npy.sh (or modify the paths in dat2npy.py) to specify the input and output directories.
3. Run the script:

```bash
./dat2npy.sh
```
