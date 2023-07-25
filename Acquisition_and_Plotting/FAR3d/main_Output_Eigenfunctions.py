#!/usr/bin/env python
# coding: utf-8
# %%


# Developer: Luis Carlos Herrera Quesada
# Date: 27/04/2023
# Universidad Carlos III de Madrid

import sys 
sys.path.append('FAR3_libraries/')
from output_eigenfunctions_TK import *
from plot_functions_TK import *


#Name the Output file as needed 
profile_name = "Profile"

#Give the maximum number of poloidal modes
num_poloidal = 10

l = 0

#Loop to read all files from pathhhh
results, files, txt,saving_file = create_files()
for file in files:
    
    try:
        #read data
        df = pd.read_csv(file + "/phi_0000", sep="\t")
        r = df["r"]
        df = df.drop("r",axis=1)
    
        #Get data analysis
        print(f"Getting data from: {file}")
        gr, freq, toroidal_coupl = get_main_data(file)
        dominant_mode, radial_pos, dominant_mode_2, radial_pos_2,dominant_mode_3,radial_pos_3, alfmode,x1,x2,width = get_values(df)
        frequency, energy, beta, kev = plasma_parameters(file,txt,abs(float(freq)))
        
        #save data in dataframe
        results.loc[l] = [beta, round(energy), dominant_mode, radial_pos/1000, x1/1000, x2/1000, width/1000, dominant_mode_2, 
                          radial_pos_2/1000,dominant_mode_3,radial_pos_3, alfmode, gr, freq,frequency]
        l += 1
        remove_files(file)
        
        #plot phi eigenfunctions
        exist = os.path.isfile(f"{saving_file}/{str(round(energy))}_{str(beta)}.png")
        if exist == False:
            plot_eigenfunctions(dominant_mode,dominant_mode_2,dominant_mode_3,
                                alfmode,radial_pos,radial_pos_2,radial_pos_3,df,r,
                                energy,beta,frequency,saving_file,toroidal_coupl, num_poloidal) 
        
    except Exception as e:
        print(f"Error: {e}")
        
results.to_excel(f"Output_{profile_name}_n{toroidal_coupl[0]}.xlsx")

if len(files) == len(os.listdir(saving_file)):
    eigenfunction_maps(saving_file)


# %%
