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
image_files = 0

save_images = []
count_images = []
count_files = 0


for file in files:
    if os.path.isfile(f"{file}/{egn_modes}"):
        if not os.path.exists(f"{file}/{saving_file}"):
            os.makedirs(f"{file}/{saving_file}")

        print(f"{file}:")
        egn_df(f"{file}/{egn_modes}",file,saving_file)

        #List excel files created for plotting
        saved_files = os.listdir(f"{file}/{saving_file}")
        excel_files = sorted(list(filter(lambda saved_files: ".xlsx" in saved_files, saved_files)))

        if len(saved_files) > len(excel_files):
            image_files = 1 

        count = 0
        values_df = pd.read_fwf(f"{file}/{egn_values}",header=None,names=["Growth_rate","f(kHz)"])
        
        if image_files == 0:
            for e_file in excel_files: 
                df = pd.read_excel(f"{file}/{saving_file}/{e_file}")    
                gf = values_df.values[count]
                gam, freq = gf[0], gf[1]
                f, energy, beta = plasma_parameters(file,profile,freq)
                f, energy, gam = round(abs(f),2), round(energy,0), round(gam,2)
                plot_func_eigensolver(df,gam,f,file,saving_file,count,energy,beta)
                if count < 6:
                    count += 1 

        #Counts the number of images files 
        images_in_files = os.listdir(f"{file}/{saving_file}/")
        images_in_files = [filename for filename in images_in_files if not filename.endswith('.xlsx')]
        images_in_files = [f"{file}/{saving_file}/" + filename for filename in images_in_files]

        save_images.append(images_in_files)
        count_images.append(len(images_in_files))
        count_files += 1        

eigenfunctions_map(save_images, count_images, count_files)

