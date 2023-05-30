
#-------------------------------------------------
#                LIBRERIES
#-------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from changeable_field import *
#------------------------------------------------------------------------------------------------
#                           SETTING PARAMETERS BY THE USER
#-----------------------------------------------------------------------------------------------

N_ex1 = 100000                      # Number of Spins
option = 0                          # 1: Experimental temperatures; 0: other temperature
T = [25]                            # Temperature, K. If only option = 0
decay = 0                           # 1: yes; 0 = no
save = 1                            # 1: for saving results; 0: no
sweep_rate = 0.0035                 # (T/s)

#-------------------------------------------------
# DO NOT CHANGE THIS PART OF THE CODE
#-------------------------------------------------

if option == 1:
    T = [1.9, 2, 3, 3.5, 4, 4.5,  5, 7, 9, 11,
         13, 15, 17, 19, 21, 23, 25, 27, 29, 
         31, 33, 35, 37, 39, 41, 44]                  # Vector containing all temperatures, 
    
if decay == 0:
    configurations = 248                              # Numerical Integration for 248 crystal orientations
    starting_mode = 0.5                               # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy)
else:
    configurations = 1
    starting_mode = 0                                 # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy)

N_ex = int(N_ex1/configurations)+1                    # Spins for each configuration
B_max = 5                                             # Maximun value for Magnetic Field 
batch = 5                                             # Number of cycles
time_per_batch = B_max/sweep_rate                     # s
total_time = time_per_batch * batch                   # Timeline, s
step = (total_time/batch)/(B_max/0.01)                # Time step
time_steps = (int(total_time/step))                   # Total time steps

#-----------------------------------------------------------------------------------------------
#                           READING THE DATA
#-----------------------------------------------------------------------------------------------

VALOR = int(time_steps/batch)
VALOR1 = int(time_steps - VALOR)
number_1 = int(time_steps -(time_steps/batch))

#------------------------------------------------

B = pd.read_csv('B.csv')                        # Magnetic Field
B = B.astype('float32')
B = B.values.tolist()
B_cos = B[VALOR+1:]

B_cos = B[VALOR+1:]
size = int(time_steps -(time_steps/batch))

#------------------------------------------------

peso = pd.read_csv('peso.txt', sep='=')         # Numerical Integration for 248 crystal orientations
peso = peso.iloc[:, 1]
peso = peso.astype('float32')

#------------------------------------------------

total_gap = pd.read_csv('total_gap.txt')        # Numerical Integration for 248 crystal orientations
total_gap = total_gap.astype('float32')
total_gap = total_gap.values.tolist()

#-----------------------------------------------------------------------------------------------
#                           GRAPH CONFIGURATIONS 
#-----------------------------------------------------------------------------------------------

font = {'family' : "Times New Roman",
       'weight' : 'normal',
       'size'   : 30  }

plt.rc('font', **font)
plt.rc('legend',fontsize=30) # using a size in points
plt.rcParams['lines.linewidth'] = 4
plt.rcParams['lines.linestyle'] = '-'
plt.rcParams["figure.figsize"] = [24, 16]
plt.rcParams["figure.autolayout"] = True

#-----------------------------------------------------------------------------------------------
#                           FUNCTIONS
#-----------------------------------------------------------------------------------------------

def main_program (T, N_ex, total_gap, B, starting_mode, total_time, time_steps, VALOR, size, configurations, save, decay):
    
    #-----------------------------------------------------------------------------------------------
    #                                   MATRIX
    #-----------------------------------------------------------------------------------------------

    y_Matrix = np.zeros ((size, configurations))                            # Matrix containing all spin states
    temp = np.zeros ((size, configurations))                    
    y_hys = np.zeros ((size))                                               # Vector containing hysteresis data
    t = np.arange (start = 0, stop = (time_steps * step), step = step)      # Time vector 
   
    for i in range (0, configurations):
        
        print ('Part:', i)        
        Matrix, y, B_total  = changeable_field (N_ex, time_steps, step,  t, B, starting_mode, T, VALOR, total_gap[i], decay)       # Stochastic proccess
        
        if decay == 0:
            for a in range (0, len(y)):
                y_Matrix [a, i] = y_Matrix [a, i] + y[a]
                temp [a, i] =  (y_Matrix [a, i]) * (peso[i])
    
    if decay == 0:          
        for a in range (0, number_1):     
            y_hys [a] = sum (temp[a, :])
                   
    else:
        
        y_relaxation = y

    #   **********************************************************************
    #                       SAVING FILES
    #   ********************************************************************** 
    
    if save == 1 & decay == 0:
        
        name = '_' + str(T) + '.csv'    
    
        B_copy = pd.DataFrame(B_cos)
        B_copy.to_csv('Bsim' + name, index=False)
          
        y_copy = pd.DataFrame(y_hys)
        y_copy.to_csv('ysim' + name, index=False)

    
    elif save == 1 & decay == 1:
        
        name = '_' + str(T) + '.csv'  
        
        y_relaxation_total = pd.DataFrame(y_relaxation)
        y_relaxation_total.to_csv('y_relaxation' + name, index=False)
        
        t_total = pd.DataFrame(t[0:len(y_relaxation)])
        t_total.to_csv('t_relaxation' + name, index=False)
                
    
    #   **********************************************************************
    #                       GRAPHS
    #   ********************************************************************** 
        
    if decay == 0:
    
        name = 'Mag_'+str(T)+'K.png'
        plt.plot(B_cos, y_hys, color = "red", marker = "o", markersize = 5, label='sim')
        plt.xlabel('Field (Tesla)')
    else:
        name = 'Rel_'+str(T)+'K.png' 
        plt.plot(t[0:len(y_relaxation)], y_relaxation, color = "red", marker = "o", markersize = 5, label='sim')
        plt.xlabel('Time (s)')
    
    plt.ylabel('Magnetic Moment (emu)')
    plt.title('@ %.2f K with %d spins' %( T, N_ex1))
    plt.legend(loc='lower right', prop={'size': 30})
    plt.grid()
    plt.savefig(name)
    plt.show() 

for i in range (0, len(T)):
    print('Temperature: ', T[i], 'K')
    main_program (T[i], N_ex, total_gap, B, starting_mode, total_time, time_steps, VALOR, size, configurations, save, decay)
