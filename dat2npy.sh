#!/bin/bash -
#SBATCH -J Coverting                       # Job Name
#SBATCH -o converting.stdout                # Output file name
#SBATCH -e converting.stderr                # Error file name
#SBATCH -N 1                       # Total number of nodes
#SBATCH -t 24:00:00                  # Run time
#SBATCH --cpus-per-task=16                    # Adjust based on expected parallelism
#SBATCH --mem 0
#SBATCH -p cpu,cpu-preempt,uri-cpu
#SBATCH --mail-user riteshbachhar@uri.edu
#SBATCH --mail-type END

umask 0022
set -x


source /modules/opt/linux-ubuntu24.04-x86_64/miniforge3/24.7.1/etc/profile.d/conda.sh
conda deactivate
conda activate SurModel

python parallel_dat2npy.py --data-dir ../Teukolsky_Code_Data/Waveform_Data_Long_Full/ \
                           --out-dir ../Teukolsky_Code_Data/Waveform_Data_Long_npy \
                           --num-workers 16

