#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 10/04/2023
# Universidad Carlos III de Madrid
# %%

import os 
import subprocess
import pandas as pd

def get_values_df():
    act_dir = os.listdir()

    for file in act_dir:
        if file.endswith(".xlsx"):
            df = file

    dataframe = pd.read_excel(df)
    om_0 = dataframe["Frequency"]
    gamma = dataframe["Growth Rate"]
    rad = dataframe["radial_pos_maximum"]

    return om_0, gamma, rad

def substitute_values(om_0, gamma, rad, files,sh_name):
    
    #print(rad.values[0])
    for i in range(len(files)):
        if rad.values[i] >= 0.85:
            os.remove(f"{files[i]}/{sh_name}")

    ## Change executable
        if rad.values[i] < 0.85:
            freq, gr = om_0.values[i], gamma.values[i]            

            with open(f"{files[i]}/{sh_name}", 'r') as tfile:
                ndata    = tfile.readlines()
        
            ## Change frequency
            tline        = [idx for idx,line in enumerate(ndata) if 'xEigen' in line][0]
            ndata[tline] = f"        ./../../../../../../Addon/Eigensolver/xEigen {freq} {gr}\n"

            with open(f"{files[i]}/{sh_name}", 'w') as nfile:
                nfile.writelines(ndata)

    return 0
        

