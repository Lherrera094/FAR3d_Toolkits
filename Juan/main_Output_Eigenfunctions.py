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
profile_name = "New_Profile"

#Give the maximum number of poloidal modes
num_poloidal = 10

l = 0

#Loop to read all files from pathhhh
results, files, saving_file = create_files()

saving_file_Potential = "Eigenfunction_squaredPotential_plots/" #Folder to save the eigenfunctions
if not os.path.exists(saving_file_Potential):
        os.makedirs(saving_file_Potential)

for file in files:
        
    try:
        #read data
        df = pd.read_csv(file + "/phi_0000", sep="\t")
        main_file = os.listdir(file)
        txt = list(filter(lambda main_file: ".txt" in main_file, main_file))[0]
        r = df["r"]
        df = df.drop("r",axis=1)

        print(txt,l)
    
        #Get data analysis
        print(f"Getting data from: {file}")
        gr, freq, toroidal_coupl = get_main_data(file)
        dominant_mode, radial_pos, dominant_mode_2, radial_pos_2,dominant_mode_3,radial_pos_3, alfmode,x1,x2,width = get_values(df)
        frequency, energy, beta, kev = plasma_parameters(file,txt,abs(float(freq)))

        phi_squared = module_complex_function(df,r,file)
        
        #save data in dataframe
        results.loc[l] = [beta, round(energy), dominant_mode, radial_pos/1000, x1/1000, x2/1000, width/1000, dominant_mode_2, 
                          radial_pos_2/1000,dominant_mode_3,radial_pos_3, alfmode, gr, freq,frequency]
        
        remove_files(file)
        
        #plot phi eigenfunctions
        exist = os.path.isfile(f"{saving_file}/{str(round(energy))}_{str(beta)}_{l}.png")
        if exist == False:
            plot_eigenfunctions(dominant_mode,dominant_mode_2,dominant_mode_3,
                                alfmode,radial_pos,radial_pos_2,radial_pos_3,df,r,
                                energy,beta,frequency,saving_file,toroidal_coupl, num_poloidal,l) 

        exist_squared = os.path.isfile(f"{saving_file_Potential}/{str(round(energy))}_{str(beta)}_{l}.png")
        if exist_squared == False:
            plot_squared_Potential(dominant_mode,dominant_mode_2,alfmode,
                                   radial_pos,radial_pos_2,radial_pos_3,phi_squared,r,
                                   energy,beta,frequency,saving_file_Potential,toroidal_coupl, num_poloidal, l)
        l += 1        

    except Exception as e:
        print(f"Error: {e}")
        
results.to_excel(f"Output_{profile_name}_n{toroidal_coupl[0]}.xlsx")

if len(files) == len(os.listdir(saving_file)):
    eigenfunction_maps(saving_file,"Eigenfunctions_full")

