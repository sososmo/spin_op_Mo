#!/bin/bash
#SBATCH -p v5_192
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 48
module purge
module load anaconda/3-2023.07-2-hxl
source activate python310
export PYTHONUNBUFFERED=1
python xxx.py
