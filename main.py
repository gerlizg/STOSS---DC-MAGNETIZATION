# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:05:39 2023

@author: Principal
"""



#	Main Code

#-------------------------------------------------
#                   FUNCTIONS
#-------------------------------------------------

from read_data import *
from Bolztman_distribution import *
from changeable_field import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#--------------------------------------------------------------------
#                   CONFIGURATIONS
#--------------------------------------------------------------------

N_ex1 = 100000                                   # Number of Spins
T = [1.9, 2, 3, 3.5, 4, 4.5,  5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 44]   



def main1 (T, N_ex, N_ex1,total_gap, B_cos, B, number_1, VALOR, VALOR1, starting_mode, total_time, time_steps ):
    
    
    save = 1                                        # 1: for saving results; 0: for not saving results
    xx = 0.1
    yy = 2E-05
    searchval = 0.3
    
    data = pd.read_excel('old-hys.xlsx')            # Reading the file
    temperature = str(T) + ' K'                     # Getting the temperature in a string format
    y_hys = data.loc[:, temperature]                # Getting the column 

    x_hys = data.iloc[:, 0]                         # Getting the magnetic field 
    
    
    x_hys = x_hys.astype('float32')
    y_hys  = y_hys .astype('float32')
    x_hys = [ (j/10000) for j in x_hys]                 # Magnetic Field to Tesla
    #x_hys = np.array([round (i,round_decimals) for i in x_hys])
    
    #   **********************************************************************
    #                       GENERAL CONFIGURATIONS
    #   **********************************************************************
    
    
    #   **********************************************************************
    #       NUMBER OF SPINS CONSIDERING THE AMOUNT OF CONFIGURATIONS
    #   **********************************************************************

    
    
    #   **********************************************************************
    #                             MATRIX
    #   **********************************************************************
    number_1 = int(time_steps- (time_steps/batch) )
    y_Matrix = np.zeros ((number_1, configurations)) 
    y_Relax = np.zeros ((number_1, configurations)) 
    
    temp = np.zeros ((number_1, configurations)) 
    temp2 = np.zeros ((number_1, configurations)) 
    y_total = np.zeros ((number_1)) 
    y_total_rel = np.zeros ((number_1)) 
    
    t = np.arange(start = 0, stop = (time_steps*step), step = step) 
    
    

    #   **********************************************************************
    #                       ITERATIVE PROCCESS
    #   **********************************************************************
    
    up = np.zeros ((time_steps)) 
    down = np.zeros ((time_steps))
    B_total = np.zeros ((time_steps))
    
    for i in range (0, configurations):
        
        print (i)  
        
        #t, P_ij, x, y, E[:,i],  tau_mag, tau_exp, probability, tau_QTM, A, B2 = Bolztman_distribution (compound_constants, total_gap [i], g_Dy[i], T, time_steps, step, number_1, B_total, option, batch)
    
        Matrix, y, B_total  = changeable_field (N_ex, time_steps, step,  t, B, starting_mode, T, VALOR, total_gap[i])
        

        for a in range (0, len(y)):
            y_Matrix [a, i] = y_Matrix [a, i] + y[a]
            temp [a, i] =  (y_Matrix [a, i]) * (peso[i])
            '''
            y_Relax [a, i] = y_Relax [a, i] + y_relaxation[a]
            temp2 [a, i] =  (y_Relax [a, i]) * (peso[i])
           '''
    
    for a in range (0, number_1):     
        y_total [a] = sum (temp[a, :])
        #y_total_rel [a] = sum (temp2[a, :])
        
    #   **********************************************************************
    #                       NORMALIZATION
    #   **********************************************************************    
    
    
    
    rmin = min(y_total)             # value
    rmax = max(y_total)
    tmax = max(y_hys)               # target
    tmin = min(y_hys)
    y_norm = [(((i-rmin)/(rmax-rmin))*(tmax-tmin))+tmin for i in y_total] 
    
    '''
    rmin = min(y_total_rel)             # value
    rmax = max(y_total_rel)
    tmax = max(y_decay)               # target
    tmin = min(y_decay)
    y_norm2 = [(((i-rmin)/(rmax-rmin))*(tmax-tmin))+tmin for i in y_total_rel] 
    '''
    #   **********************************************************************
    #                       SAVING FILES
    #   ********************************************************************** 
    
    
        
    name = '_' + str(T) + '.csv'    

    B_copy = pd.DataFrame(B_cos)
    B_copy.to_csv('Bsim' + name, index=False)
      
    y_copy = pd.DataFrame(y_norm)
    y_copy.to_csv('ysim' + name, index=False)
    
    B_copy1 = pd.DataFrame(x_hys)
    B_copy1.to_csv('Bexp' + name, index=False)
      
    Matrix_final = pd.DataFrame(y_total)
    Matrix_final.to_csv('Matrix' + name, index=False)
    
    B_final = pd.DataFrame(B_total)
    B_final.to_csv('B' + name, index=False)
    
    y_copy1 = pd.DataFrame(y_hys)
    y_copy1.to_csv('yexp' + name, index=False)
    
    #   **********************************************************************
    #                       GRAPHS
    #   ********************************************************************** 
    
    name1 = 'Mag_'+str(T)+'K.png'
    
    A = 0.02/100      #0.02
    B2 = 500
      
                                         # Temperature, Kelvin

    tau_QTM = 75 
    
    #   **********************************************************************
    #                       GRAPH CONFIGURATIONS 
    #   **********************************************************************
    font = {'family' : "Times New Roman",
           'weight' : 'normal',
           'size'   : 30  }
    
    plt.rc('font', **font)
    plt.rc('legend',fontsize=30) # using a size in points
    plt.rcParams['lines.linewidth'] = 4
    plt.rcParams['lines.linestyle'] = '-'
    plt.rcParams["figure.figsize"] = [24, 16]
    plt.rcParams["figure.autolayout"] = True
    
    plt.plot(x_hys, y_hys, color = 'blue', marker = "o", markersize = 5, label='exp')
    plt.plot(B_cos, y_norm, color = "red", marker = "o", markersize = 5, label='sim')
    #plt.plot(B_cos2, y_norm2, color = "red")
    #plt.ylim(-yy, yy)
    #plt.xlim(-xx, xx)
    plt.xlabel('Field (Tesla)')
    plt.ylabel('Magnetic Moment')
    plt.title('@ %.2f K with Tau QTM= %.3f, B2= %.3f (%d spins), A = %.5f ' %( T, tau_QTM, B2, N_ex1, A))
    #plt.legend(['Experimental', 'Raman + QTM + Direct'])
    plt.legend(loc='lower right', prop={'size': 30})
    plt.grid()
    plt.savefig('Relax_'+str(T)+'.png')
    plt.show() 
    
    '''
    plt.plot(x_decay, y_decay, color = 'blue', marker = "o", markersize = 5, label='exp')
    plt.plot(t[0:len(y_norm2)], y_norm2, color = "red", marker = "o", markersize = 5, label='sim')
    #plt.plot(B_cos2, y_norm2, color = "red")
    #plt.ylim(-yy, yy)
    #plt.xlim(-xx, xx)
    plt.xlabel('Field (Tesla)')
    plt.ylabel('Magnetic Moment')
    plt.title('@ %.2f K with Tau QTM= %.3f, B2= %.3f (%d spins), A = %.5f ' %( T, tau_QTM, B2, N_ex1, A))
    #plt.legend(['Experimental', 'Raman + QTM + Direct'])
    plt.legend(loc='lower right', prop={'size': 30})
    plt.grid()
    plt.savefig(name1)
    plt.show() 
    '''

flag = 24                            # System index in the data set
B_max = 5                            # Max Magnetic Field Value
starting_mode = 0.5                  # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy)
batch = 5                            # Number of cosine cycles
total_time = 1429 * batch 
step = 2.8579
time_steps = (int(total_time/step))              #(int(total_time/step))

VALOR = int(time_steps/batch)

VALOR1 = int(time_steps - VALOR)

y0 = np.zeros(VALOR)+5
STEP = B_max/VALOR
yy = np.arange(start = 0, stop = 5+(STEP), step = (STEP))
y1 = -np.sort(-yy)
y2 = -yy[1:]
y3 = np.sort(-yy)
B = [yt for x in [y0, y1, y2, y3[1:-1], yy] for yt in x] 

B_cos = B[VALOR+1:]
number_1 = int(time_steps -(time_steps/batch))

configurations = 248
N_ex = int(N_ex1/configurations)+1

peso = pd.read_csv('peso.txt', sep='=')     # Reading the file
peso = peso.iloc[:, 1]
peso = peso.astype('float32')

total_gap = pd.read_csv('total_gap.txt')   # Reading the file
total_gap = total_gap.astype('float32')
total_gap = total_gap.values.tolist()
    


for i in range (0, len(T)):
    main1(T[i], N_ex, N_ex1, total_gap, B_cos, B, number_1, VALOR, VALOR1, starting_mode, total_time, time_steps)

