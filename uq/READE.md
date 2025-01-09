MO-ASMO -- uq/MOASMO.py -- optimization()
This is a standalone version of MO-ASMO, a surrogate based multi-objective optimization algorithm.

Quick start: please run ZDT1/ZDT1\_MOASMO.py to start your first run. For more information about MO-ASMO, please read the paper. And please cite it if you use the code in your own research.   
Gong, W., Q. Duan, J. Li, C. Wang, Z. Di, A. Ye, C. Miao, and Y. Dai (2016), Multiobjective adaptive surrogate modeling-based optimization for parameter estimation of large, complex geophysical models, Water Resour. Res., 52(3), 1984-2008. doi:10.1002/2015WR018230.

Many test cases with the test function uq.
1. uq\NSGA2.py: Optimize with NSGA2 algorithm, a traditional multi-objective optimization algorithm.
2. uq\MOASMO.py: Optimize with MO-ASMO.
3. uq\WNSGA2.py: Optimize with WNSGA2, NSGA2 with weighted crowding distance, which can constrain the search region better than your default parameters.
4. uq\WMOASMO.py: Optimize with WMO-ASMO, MO-ASMO with weighted crowding distance.
5. uq\http_model.py: Modify Parameters, Run the Model, and Compute Results
6. uq\compute: Code for calculating SCDF based on parameter optimization simulation results


