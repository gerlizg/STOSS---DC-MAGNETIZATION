# **********************************************************************
#                       	STOSS
# ********************************************************************** 

#----------------------
Necessary files:
#----------------------

1) B.csv (Magnetic Field applied)
2) peso.txt and total_gap.txt (Numerical integration for the crystal configuration)
3) Changeable_field.py (Part of the code for the iterative proccess)
4) Main.py (Part of the code where the user specifies the parameters)

#----------------------
Modules from python:
#----------------------

1) Numpy
2) Matplotlib
3) Pandas 
4) Scipy.optimize
5) Collections
6) Random
7) Math
8) Mpmath
9) Sympy 

#----------------------
Options for the user:
#----------------------
N_ex1 = 100000          # Number of Spins
option = 0              # 1: Experimental temperatures; 0: other temperature
T = [25]                # Temperature, K. If only option = 0
decay = 0               # 1: yes; 0 = no
save = 1                # 1: for saving results; 0: no
sweep_rate = 0.0035     # (T/s)

If you want to try different temperature from the experimental data (T = [1.9, 2, 3, 3.5, 4, 4.5,  5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 44])
option must be different from 1, and you need to put them inside the vector called T. 

If you want to simulate decay curves, set the variable decay equal to 1, otherwise the simulator will work on hysteresis curves.

If you want to save results, set the variable save equal to 1. 

#------------------------------------
Relaxation Mechanisms STOSS uses: 
#------------------------------------

1) Raman: C*(T^n)
2) Quantum Tunnelling of Magnetization (*): (QTM^-1)/{1+[B2*(Magnetic Field^2)]}
3) Direct(**): (Zeeman^2)*[A*coth(Zeeman/Temperature)]

(*) Valentin V. Novikov, Alexander A. Pavlov, Yulia V. Nelyubina, Marie-Emmanuelle Boulon, Oleg A. Varzatskii, Yan Z. Voloshin, and Richard E.P. Winpenny Journal of the American Chemical Society 2015 137 (31), 9792-9795
(**) Francielli S. Santana, Mauro Perfetti, Matteo Briganti, Francesca Sacco, Giordano Poneti, Enrico Ravera, Jaísa F. Soares and Roberta Sessoli. Chem. Sci., 2022, 13, 5860-5871

#------------------------------------
Previous work:
#------------------------------------

This is a new version of the STOSS from the paper: Lanthanide molecular nanomagnets as probabilistic bits [arXiv:2301.08182].
STOSS is a Markov Chain Monte Carlo model employed to simulate, with the same parameters, magnetization decay at all temperatures and hysteresis at all temperatures, given the physical parameters of the system.

#------------------------------------
To cite this work:
#------------------------------------

High-temperature Magnetic Blocking in a Monometallic Dysprosium Azafullerene Single-molecule Magnet
Ziqi Hu1,(3†), Yuanyuan Wang(2†), Aman Ullah(1), Gerliz M. Gutiérrez-Finol(1), Amilcar Bedoya-Pinto1, Dier Shi(4), 
Shangfeng Yang(3), Zujin Shi(2), Alejandro Gaita-Ariño(1) and Eugenio Coronado(1)


1 Instituto de Ciencia Molecular, Universidad de Valencia, C/Catedrático José Beltrán 2, 46980 Paterna, Spain.
2 National Laboratory for Molecular Sciences, State Key Laboratory of Rare Earth Materials Chemistry and Applications, College of Chemistry and Molecular Engineering, Peking University, Beijing 100871, People’s Republic of China.
3 Department of Materials Science and Engineering, CAS Key Laboratory of Materials for Energy Conversion, Anhui Laboratory of Advanced Photon Science and Technology, University of Science and Technology of China, Hefei 230026, China
4 Department of Chemistry, Zhejiang University, Hangzhou 310027, People’s Republic of China.
† These authors contributed equally to this work.

*Correspondence: zjshi@pku.edu.cn; alejandro.gaita@uv.es; eugenio.coronado@uv.es; 
#-------------------------------------------------------------------------
Any kind of question from this code, please contac: gerliz.gutierrez@uv.es
#-------------------------------------------------------------------------
