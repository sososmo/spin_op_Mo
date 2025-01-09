from sys import exit
import argparse, shutil
import numpy as np
from uq.uqofrun.UQ.util import read_param_file, scale_samples

pasrer = argparse.ArgumentParser(description='Perform parameter optimization on model')

pasrer.add_argument('-m', '--method', type=str, choices=['sce', 'dds', 'ASMO', 'MOASMO', 'mcmc', 'PSO', 'GA', 'SA'],
                    required=True)
pasrer.add_argument('-p', '--paramfile', type=str, required=True)
# pasrer.add_argument('-f', '--modelfile', type=str, required=True)
args = pasrer.parse_args()

bl = np.empty(0)
bu = np.empty(0)
pf = read_param_file(args.paramfile)
for i, b in enumerate(pf['bounds']):
    bl = np.append(bl, b[0])
    bu = np.append(bu, b[1])

# 复制模型文件到functn.p
# dir = './UQ/test_functions/'
# shutil.copy(args.modelfile, dir+'functn.py')

# import SCE, PSO, ASMO, DDS
import ASMO_S as ASMO
import MOASMO as MOASMO
# import MOASMO_20241115_initial as MOASMO
# import MOASMO_gen as MOASMO_gen

# if args.method == 'sce':
#     SCE.sceua(bl, bu, pf, ngs=2)
# elif args.method == 'dds':
#     DDS.optimization(bl, bu, pf, max_sample = 100)
if args.method == 'ASMO':
    ASMO.optimization(bl, bu, pf, max_sample=6)
elif args.method == 'MOASMO':
    nInput = pf['num_vars']
    niter = 20
    # pct:样本比例*100
    pct = 0.05

    MOASMO.optimization(nInput, 2, bl, bu, niter, pct, pf)
    # MOASMO_gen.optimization(nInput, 2, bl, bu, niter, pct, pf)

# elif args.method == 'mcmc':
# MCMC.optimization(bl, bu, pf)
# elif args.method == 'PSO':
#     PSO.optimization(bl, bu, pf)
# elif args.method == 'GA':
# GA.method(bl, bu)
# elif args.method == 'SA':
# SA.method(bl, bu)
