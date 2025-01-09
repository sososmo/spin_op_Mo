# Multi-Objective Adaptive Surrogate Modelling-based Optimization
from __future__ import division, print_function, absolute_import
import sampling
import gp
import NSGA2
import numpy as np
from uq import http_model


def optimization(nInput, nOutput, xlb, xub, niter, pct, pf,
                 Xinit=None, Yinit=None, pop=100, gen=1000,
                 crossover_rate=0.9, mu=20, mum=20):
    """ 
    Multi-Objective Adaptive Surrogate Modelling-based Optimization
    model: the evaluated model function
    nInput: number of model input
    nOutput: number of output objectives
    xlb: lower bound of input
    xub: upper bound of input
    niter: number of iterations
    pct: percentage of resampled points in each iteration
    Xinit and Yinit: initial samplers for surrogate model construction
    ### options for the embedded NSGA-II of MO-ASMO
        pop: number of population
        gen: number of generation
        crossover_rate: ratio of crossover in each generation
        mu: distribution index for crossover
        mum: distribution index for mutation
    """
    N_resample = int(pop * pct)
    if (Xinit is None and Yinit is None):
        print(nInput,'nInput')
        Ninit = nInput * 10
        Xinit = sampling.glp(Ninit, nInput)[:Ninit]
        print(Xinit, 'Xinit')
        for i in range(Ninit):
            Xinit[i, :] = Xinit[i, :] * (xub - xlb) + xlb
        np.savetxt('initial_Input_s.txt', Xinit, delimiter=' ')

        # Yinit = np.zeros((Xinit, nOutput))
        Yinit = np.zeros((len(Xinit), nOutput))
        #
        #     '''
        #     loops:SPIN-UP TIMES
        #     '''
        # ht = http_model.Http_CS_Conect({
        #     'loops': 10
        # })
        ht = http_model.Http_CS_Conect({
            'loops': 1
        })
        for i in range(Ninit):
            print(i)
            ev = ht.evaluate(Xinit[i, :], pf['names'])
            Yinit[i, :] = ev['modelout']
            print(Yinit[i, :], 'Yinit[i, :]')
            # Yinit[i,:] = model.evaluate(Xinit[i,:])
    else:
        Ninit = Xinit.shape[0]
    np.savetxt('initial_Output_s.txt', Yinit, delimiter=' ')
    icall = Ninit

    x = Xinit.copy()
    y = Yinit.copy()

    print('initial:', x, y)
    for i in range(niter):
        print('Surrogate Opt loop: %d' % i)
        sm = gp.GPR_Matern(x, y, nInput, nOutput, x.shape[0], xlb, xub)
        bestx_sm, besty_sm, x_sm, y_sm = \
            NSGA2.optimization(sm, nInput, nOutput, xlb, xub, \
                               pop, gen, crossover_rate, mu, mum)
        D = NSGA2.crowding_distance(besty_sm)
        idxr = D.argsort()[::-1][:N_resample]
        x_resample = bestx_sm[idxr, :]
        print(x_resample, 'x_resample')
        y_resample = np.zeros((N_resample, nOutput))
        for j in range(N_resample):
            y_resample[j, :] = ht.evaluate(x_resample[j, :], pf['names'])['modelout']
            print(y_resample, 'y_resample')
        icall += N_resample
        x = np.vstack((x, x_resample))
        y = np.vstack((y, y_resample))

    xtmp = x.copy()
    ytmp = y.copy()
    np.savetxt('tem_Input_S.txt', xtmp, delimiter=' ')
    np.savetxt('tem_Output_S.txt', ytmp, delimiter=' ')

    xtmp, ytmp, rank, crowd = NSGA2.sortMO(xtmp, ytmp, nInput, nOutput)
    idxp = (rank == 0)
    bestx = xtmp[idxp, :]
    besty = ytmp[idxp, :]
    # Deduplication
    bestx = np.unique(bestx, axis=0)
    besty = np.unique(besty, axis=0)

    np.savetxt('bestx_MOASMO_OUT_x.txt', bestx, delimiter=' ')
    np.savetxt('bestx_MOASMO_OUT_y.txt', besty, delimiter=' ')

    print(bestx, besty)
    return bestx, besty, x, y