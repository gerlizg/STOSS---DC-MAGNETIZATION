#-------------------------------------------------
#                LIBRERIES
#-------------------------------------------------

import numpy as np
import pandas as pd
import scipy.optimize as opt
import collections
import random     
import math
import mpmath
from sympy import *               

#-------------------------------------------------
#                FUNCTIONS
#-------------------------------------------------

def probabi (tau_exp):

    number = tau_exp
    probability = 0

    for i in range (1, 50):
        temp = 1/((number**i) * factorial (i))
        if i %2 == 0:
            probability = probability - temp
        else:
            probability = probability + temp
            
    return probability
#------------------------------------------------

def solve2(vars, vao):
        x, y = vars
        eq1 = (x+y)-(vao [0])
        eq2 = (x/y)-(vao [1])
        return [eq1, eq2]
    
#------------------------------------------------


def changeable_field (N_ex, time_steps, step, t, B, starting_mode, T, VALOR, total_gap, decay):
	
    #-------------------------------------------------
	#   Defining the parameters
    #-------------------------------------------------
    
    swap = {0: 1, 1:0}                  # Function that returns the value                              
    n= 3.3                              # Exponential factor (Raman) 
    C = 2.9E-08                         # Pre-factor factor (Raman)    
    A = 0.02/100                        # Constant factor (direct mechasnim)     
    tau_QTM = 100                       # QTM
    B2 = 500                            # Constant Factor (QTM) 
    miu_B = 0.671713816                 # Bohr's magneton                   
    Mj = 0.5                            # Spin Projection
    B_fit = 0.25                        # 0.25T multiplied for the ratio spins up and down
        
    if decay == 1:
        B = np.zeros ((time_steps))     # Magnetic Field
        g_Dy = 6.63                     # Mean value for gDy
    
    #-------------------------------------------------
    #   Creating the lists
    #-------------------------------------------------   
    
    Matrix = np.zeros ((N_ex, time_steps))         # Contains all the states (0, 1) 
    up = np.zeros ((time_steps))                   # Spins in the excited state 
    down = np.zeros ((time_steps))                 # Spins in the ground state 
    B_total = np.zeros ((time_steps))              # Magnetic Field   
    vao = np.zeros((2))
    
    #------------------------------------------------

    P_ij = np.zeros(time_steps)                    # Bolztman distribution
    P_i = np.zeros(time_steps)                     # Probability for "i" state 
    x = np.zeros(time_steps)                       # Probability of changing to state 1
    y = np.zeros(time_steps)                       # Probability of changing to state 0
    
    #------------------------------------------------

    #-------------------------------------------------                
    #   Iteration over the Matrix
    #-------------------------------------------------
    
    # Initializating the spins in a specific state:
    
    for i in range (0, int (N_ex * starting_mode)):
        Matrix [i, 0] = Matrix [i, 0] + 1
        
    for i in range (int (N_ex * starting_mode), N_ex):
        Matrix [i, 0] = Matrix [i, 0] + 0
    
    # Reading the previous state of each time step:
    
    for j in range (1,time_steps):
            
        random_n = [np.random.uniform(0, 1) for i in range(N_ex)]
        
        up [j-1]= np.sum (Matrix[:,j-1])
        down [j-1] = N_ex - up [j-1]        
        B_total [j] = B[j] - (B_fit * (up [j-1]- down [j-1])/(up [j-1]+ down [j-1]))
        
        if decay == 1:
            E = abs((2 * Mj * g_Dy * miu_B * B_total [j]))
        else:        
            E = abs((total_gap[0] * Mj  * miu_B * B_total [j]))
        
        if E == 0:
            tau_mag = ((((C)*(T**n)))+(((tau_QTM**-1)/(1+(B2*(B_total [j]**2))))))**-1
        else:
            tau_mag = ((((C)*(T**n)))+(((tau_QTM**-1)/(1+(B2*(B_total [j]**2)))))+((E**2)*(A*mpmath.coth(E/T))))**-1
            
        tau_exp = (tau_mag /step)
        probability  = probabi (tau_exp)           
        vao [0] = probability                               
        P_ij  = 1 / (np.exp(E/T))
        vao [1] = P_ij
        
        x, y=  opt.fsolve(solve2, (vao [0]/2, vao [0]/2), vao)

        for i in range(0,N_ex):
            
            if B_total[j]>=0:
                        
                if random_n[i] < x and Matrix[i,j-1]== 1:                
                    Matrix[i,j] = swap[Matrix[i,j-1]]           # Swap the state and direction                
                elif random_n[i] < y and Matrix[i,j-1]== 0:
                    Matrix[i,j] = swap[Matrix[i,j-1]]           # Swap the state and direction
                else:               
                    Matrix[i,j] = Matrix[i,j-1]
                    
            elif  B_total[j]<0:
                
                if random_n[i] < y and Matrix[i,j-1]== 1:                
                    Matrix[i,j] = swap[Matrix[i,j-1]]           # Swap the state and direction                
                elif random_n[i] < x and Matrix[i,j-1]== 0:
                    Matrix[i,j] = swap[Matrix[i,j-1]]           # Swap the state and direction
                else:               
                    Matrix[i,j] = Matrix[i,j-1]
     
    #-------------------------------------------------
    #   Relaxation curve and hysteresis:
    #-------------------------------------------------
    
    column = np.sum(Matrix,axis=0).tolist()
    y_spins = [N_ex - i for i in column]
    
    if decay == 1 :
        y2 = [((2 * x) - N_ex) for x in y_spins]
    else:
        y = y_spins [VALOR:]
        y2 = [(( N_ex-(2 * x))/N_ex) for x in y]

    return  Matrix, y2, B_total
    
    
 
        

  
  
    