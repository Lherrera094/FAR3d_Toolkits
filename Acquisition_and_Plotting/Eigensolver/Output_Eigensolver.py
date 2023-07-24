#!/usr/bin/env python
# coding: utf-8

# Developer: Luis Carlos Herrera Quesada
# Date: 27/04/2023
# Universidad Carlos III de Madrid

import sys, os 
sys.path.append('FAR3_libraries/')
from eigensolver_function_TK import *

act_dir = os.listdir()
files = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))

egn_modes = "egn_mode_asci.dat"
egn_values = "egn_values.dat"
saving_file = "eigensolver_results"
profile = "TJII_NBI.txt"

for file in files:
    if os.path.isfile(f"{file}/{egn_modes}"):
        if not os.path.exists(f"{file}/{saving_file}"):
            os.makedirs(f"{file}/{saving_file}")

        print(f"{file}:")
        egn_df(f"{file}/{egn_modes}",file,saving_file)

        #List excel files created for plotting
        excel_files = os.listdir(f"{file}/{saving_file}")
        excel_files = sorted(list(filter(lambda excel_files: ".xlsx" in excel_files, excel_files)))

        count = 0
        values_df = pd.read_fwf(f"{file}/{egn_values}",header=None,names=["Growth_rate","f(kHz)"])

        for e_file in excel_files: 
            df = pd.read_excel(f"{file}/{saving_file}/{e_file}")    
            gf = values_df.values[count]
            gam, freq = gf[0], gf[1]
            f, energy, beta = plasma_parameters(file,profile,freq)
            f, energy, gam = round(abs(f),2), round(energy,0), round(gam,2)
            print(f,energy,beta)
            plot_func_eigensolver(df,gam,f,file,saving_file,count,energy,beta)
            if count < 6:
                count += 1 





