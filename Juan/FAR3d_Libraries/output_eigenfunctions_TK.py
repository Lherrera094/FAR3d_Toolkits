#!/usr/bin/env python
# coding: utf-8
# +
# Developer: Luis Carlos Herrera Quesada
# Date: 02/06/2023
# Universidad Carlos III de Madrid
# -

import pandas as pd
import matplotlib.pyplot as plt
import os 
import numpy as np
from ipywidgets import interact, interactive, fixed
from IPython.display import clear_output
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from PIL import Image
import matplotlib.colors as mc

from search_and_evaluate_TK import *

#Read all folders and create the folder to save the plots
def create_files():
    
    act_dir = os.listdir()
    folders = find_farprt(act_dir)
    file = sorted(folders)
    
    #creates a dataframe to savel results
    results = pd.DataFrame(columns=['beta', 'efast', 'dominant_mode', 'radial_pos_maximum','width_i','width_f',
                                    'width','coupling','radial_pos_2','Possible_EAE',
                                    'radial_pos_3','Alfvén_mode','Growth Rate',
                                    'Frequency','f(kHz)'])
    
    saving_file = "Eigenfunction_plots/" #Folder to save the eigenfunctions
    if not os.path.exists(saving_file):
        os.makedirs(saving_file)
        
    main_file = list(filter(lambda act_dir: "00_main" in act_dir, act_dir))
    main_file = os.listdir(main_file[0])
    txt = list(filter(lambda main_file: ".txt" in main_file, main_file))[0]
    
    return results, file, txt, saving_file


#From farprt and profiles.dat obtains the relevant plasma characteristics
def plasma_parameters(directory,profile,frec):
    #Read farprt
    farprt_data = open(directory + '/farprt')
    nfarprt_data = farprt_data.readlines()
    
    #profile, exist = find_profiles(directory)
    
    #read external profiles
    data = open(directory + '/' + profile)
    ndata = data.readlines()
    
    #constants
    mi = 1.67e-27
    mu_0 = 1.25664e-06
    e = 1.602e-19
    
    #EP energy
    tline = [idx for idx,line in enumerate(nfarprt_data) if 'cvfp:' in line][0] + 1
    cvfp = nfarprt_data[tline].split(",")
    cvfp = float(cvfp[0])
    
    #EP beta
    tline = [idx for idx,line in enumerate(nfarprt_data) if 'bet0_f' in line][0] + 1
    beta = nfarprt_data[tline].split("\t")
    beta = float(beta[0])
    
    #Magnetic Field
    tline = [idx for idx,line in enumerate(ndata) if 'Vacuum' in line][0] + 1
    B = ndata[tline]
    B = get_number_line(B)
    
    #Major Radius
    tline = [idx for idx,line in enumerate(ndata) if 'Geometric Center' in line][0] + 1
    R = ndata[tline]
    R = get_number_line(R)
    
    #Main Ion species mass/proton
    tline = [idx for idx,line in enumerate(ndata) if 'Main Ion' in line][0] + 1
    M = ndata[tline]
    M = get_number_line(M)
    
    #Density and safety factor
    tline = [idx for idx,line in enumerate(ndata) if 'Rho' in line][0] + 1
    full_line = ndata[tline].split("\t")
    full_line = full_line[0].split(" ")
    q = float(full_line[1])
    ni = float(full_line[3])
    ni = ni*10**(20)
    
    #Alfvén speed
    Va = (B)/np.sqrt(M*mu_0*mi*ni)

    #Frecuency
    f = (frec*Va)/(2*np.pi*R*1000*q)
    #Energy
    energy = mi*(cvfp*Va)**2/(e*1000)
    
    return f, energy, beta, cvfp


#From farprt obtains frequency and growth rate, and checks convergence of the simulation
def get_main_data(f):
    data = open(f+'/farprt')
    ndata = data.readlines()
    line_diference = 4
    toroidal_couplings = []
    gamma = []

    tline = [idx for idx,line in enumerate(ndata) if 'n       Avg. gam:         Avg. om_r:' in line][0] + 1
    n, grwth, omega = ndata[tline].split()
    toroidal_couplings.append(n)

    if grwth == "NaN":
        grwth, omega = 0,-1000
    else: 
        grwth, omega = float(grwth), float(omega)

    gamma.append(grwth)
    
    try:
        for i in range(1,10):
            tline = [idx for idx,line in enumerate(ndata) if 'n       Avg. gam:         Avg. om_r:' in line][0] + 1 + (line_diference*i)
            n, grwth1, omega1 = ndata[tline].split()
            toroidal_couplings.append(n)
        
            if grwth1 == "NaN" or grwth1 == "nan":
                grwth1, omega1 = 0,-1000
            else:
                grwth1, omega1 = float(grwth1), float(omega1)

            gamma.append(grwth1)
                
            if grwth1 >= grwth:
                grwth = grwth1
                omega = omega1

    except Exception as e:
        x = 0

    chek = check_convergence(gamma)      

    if chek:
        print("Acceptable Convergence")
    else:
        print("Non-convergence Simulation")

    return grwth, omega, toroidal_couplings


#Print file important data
def get_values(data_frame):
    #Obtain Eigenmode with maximum amplitude
    new_df = data_frame
    new_df = new_df.drop(new_df.columns[0], axis=1)
    data = new_df.abs()
    df_desc = data.describe()
    s_max = df_desc.loc["max"]
    
    #Column name for the mode with maximum amplitude
    dominant_mode = s_max[s_max.isin([max(df_desc.loc["max"])])].index[0] 
    radial_pos = np.argmax(data[dominant_mode].values)
    sol = dominant_mode[0]

    #Width of the maximum mode
    max_df = data_frame[dominant_mode]
    y1,x1,y2,x2,width = dominant_mode_width(max_df)
    
    #Delete dominant mode from data_frame
    data = data.drop(dominant_mode,axis=1)
    for col in data.columns:
        if sol not in col:
            data = data.drop(col,axis=1)
       
    #treshold = 1
    #while(treshold <= 0.08):
    df_desc_sec = data.describe()
    s_max = df_desc_sec.loc["max"]
    dominant_mode_2 = s_max[s_max.isin([ max(df_desc_sec.loc["max"])])].index[0]
    radial_pos_2 = np.argmax(data[dominant_mode_2].values)
    treshold = abs(radial_pos - radial_pos_2)/1000
    data = data.drop(dominant_mode_2,axis=1)  
    
    n1 = dominant_mode.split("/")
    n2 = dominant_mode_2.split("/")
    
    try:
        m1 = n1[0].split("-") 
        m2 = n2[0].split("-")
        m_1,m_2 = int(m1[-1]),int(m2[-1])

    except Exception as e: 
        m1 = n1[0].split(" ") 
        m2 = n2[0].split(" ")
        m_1,m_2 = int(m1[-1]),int(m2[-1])

    except Exception as error:
        m1 = n1[0].split("  ") 
        m2 = n2[0].split("  ")
        m_1,m_2 = int(m1[-1]),int(m2[-1])

    n_1,n_2 = int(n1[1]),int(n2[1])
    
    try:
        if(n_1 == n_2):
            df_desc_3 = data.describe()
            s_max = df_desc_3.loc["max"]
            dominant_mode_3 = s_max[s_max.isin([ max(df_desc_3.loc["max"])])].index[0]
            radial_pos_3 = np.argmax(data[dominant_mode_3].values)
            treshold = abs(radial_pos - radial_pos_3)/1000
            data = data.drop(dominant_mode_3,axis=1)
        else:
            dominant_mode_3 = "--"
            radial_pos_3 = "--"
    except Exception as e:
        dominant_mode_3 = "--"
        radial_pos_3 = "--"
    
    if(n_1 != n_2):
        alfmode = "HAE"
    if(n_1 == n_2):
        if(m_1 + 1 == m_2 or m_1 - 1 == m_2):
            alfmode = "TAE/EAE"
    
    return dominant_mode, radial_pos, dominant_mode_2, radial_pos_2,dominant_mode_3, radial_pos_3, alfmode, x1, x2, width


def dominant_mode_width(max_dataframe):
    max_dataframe = pd.DataFrame(max_dataframe)
    #Defines radius column and add it to the dataframe
    radius = np.linspace(0,999,len(max_dataframe))
    max_dataframe['Radius'] = radius
    max_mode = abs(max_dataframe)
    name_column = max_dataframe.columns
    
    max_mode = max_mode.loc[max_mode[name_column[0]] >= max(max_mode[name_column[0]])/2]
    
    #Obtain the points for the width for the max eigenfunction
    x1 = max_mode["Radius"].iloc[0]
    y1 = max_mode[name_column[0]].iloc[0]
    
    x2 = max_mode["Radius"].iloc[-1]
    y2 = max_mode[name_column[0]].iloc[-1]

    width = x2-x1
    
    return y1,x1,y2,x2,width

def module_complex_function(dataframe,r,file):

    new_df = dataframe
    new_df = new_df.drop(new_df.columns[0], axis=1)
    new_df.columns = new_df.columns.str[1:] 

    df_squared = new_df.pow(2)
    df_squared = df_squared.groupby(df_squared.columns, axis=1).sum()
    df_squared = np.sqrt(df_squared)

    new_df_squared = pd.concat([r,df_squared], axis=1)
        
    new_df_squared.to_csv(f"{file}/Squared_Potential.txt",index=None, sep="	")  
      
    return df_squared