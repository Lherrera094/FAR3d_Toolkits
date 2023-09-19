#!/usr/bin/env python
# coding: utf-8

# Developer: Luis Carlos Herrera Quesada
# Date: 23/07/2023
# Universidad Carlos III de Madrid


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from plot_functions_TK import *
from output_eigenfunctions_TK import *
from search_and_evaluate_TK import *


def plot_func_eigensolver(df,gam,freq,file,sav_file,l,energy,beta):

    df.rename(columns={"r/a":"Radius"}, inplace=True) 

    dm, dm_r, dm2, dm_r2, dm3, dm_r3, alfmode, x_1, x_2, width = get_values(df)
        
    df.rename(columns={"Radius":"r/a"}, inplace=True)
    im = plt.figure(figsize=(9,8))   
    new_df = df.drop(columns="r/a")
    k=0
    tor_coupl = [5,9,13,17]
    for n in tor_coupl:
            d = get_colors_dict(n)
            plt.axhline(0,xmin = 0.05, xmax = 0.06,color=d["colfam"],linewidth=2,label=f"n= {n}")                   
            k += 1

    for i in new_df.columns:
        j=0
        m = i.split("/")[0]

        d = get_colors_dict(abs(int(m)))
        cmap = mc.LinearSegmentedColormap.from_list("", d["colors"])

        if int(m) >= 0:
            plt.plot(df["r/a"],new_df[i],color=cmap(j/3))

        elif int(m) < 0:
            plt.plot(df["r/a"],new_df[i],"--",color=cmap(j/3))

    plt.axvline(dm_r/1000,color="red",linewidth=1)
    plt.annotate(f"Dominant Mode (n/m): {dm}", xy=(0.55, 0.02), xycoords='axes fraction', fontsize = 15)

    plt.title(f"$T_f:{int(energy)}$keV/"+r"$\beta_f$"+f":{beta}/$\gamma$:{gam}/$f$(kHz):{freq}",fontsize=28)
    plt.xlabel("r/a")
    plt.ylabel(r"$\delta \Phi$")
    plt.rcParams['axes.labelsize'] = 25
    #plt.ticklabel_format("both","sci")
    plt.grid(True)
    plt.legend(loc="upper right",prop={'size':18})
    plt.savefig(f"{file}/{sav_file}/{energy}_{beta}_Eigenfunctions_{l+1}.png",dpi=350)


def egn_df(egn_modes_files,file,saving_file):
    #Reads file egn_mode
    eigen_file = pd.read_fwf(egn_modes_files,col_name="values")
    res_modes = eigen_file.columns.values
    res_modes = int(res_modes[0])
    eigen_file.columns = ["values"]
    
    #Number of poloidal modes
    pol_modes = int(eigen_file["values"].values[0])
    new_eigen_file = eigen_file.drop(index=0)

    #Number of radial points
    num_rad = int(eigen_file["values"].values[1])
    new_eigen_file = new_eigen_file.drop(index=1).reset_index(drop=True)
    
    #Saves n and m modes
    m_modes, n_modes = [], []
    for i in range(pol_modes*2):
        if i%2 == 0:
            m_modes.append(int(new_eigen_file["values"].values[0]))
        if i%2 != 0:
            n_modes.append(int(new_eigen_file["values"].values[0]))

        new_eigen_file = new_eigen_file.drop(index=0).reset_index(drop=True)
    
    #Delets next values which correpond to the frequencies for the resonant modes
    eigen_func = new_eigen_file.iloc[res_modes:].reset_index(drop=True)
    
    #Obtaines radial values column
    radius = eigen_func.loc[:num_rad-1]
    radius.columns = ["r/a"]

    #creates new datasets
    new_eigen_func = eigen_func.iloc[num_rad:].reset_index(drop=True)
    df_val = eigen_func.iloc[num_rad:].reset_index(drop=True)
    
    for k in range(res_modes):
        modes = pd.DataFrame(columns = [f"{n_modes[i]}/{m_modes[i]}" for i in range(len(m_modes))])
        row = 0
        for i in range(num_rad):
            values = df_val.loc[:pol_modes-1]["values"].to_numpy()
            df_val = df_val.iloc[pol_modes:].reset_index(drop=True)
            modes.loc[row] = values
            row += 1

        modes.insert(0,"r/a",radius)
        modes.to_excel(f"{file}/{saving_file}/egn_functions_{k+1}.xlsx", index=False)

#From farprt and egn_values.dat obtains the relevant simulations characteristics
def plasma_parameters(directory,profiles,frec):
    #Read farprt
    farprt_data = open(directory + '/farprt')
    nfarprt_data = farprt_data.readlines()
    
    #profile, exist = find_profiles(directory)
    
    #read external profiles
    data = open(directory + '/' + profiles)
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
    
    return f, energy, beta

def eigenfunctions_map(directory, col_num, row_num):
    images = []

    for filename in directory:
        for image_file in filename:
            images.append(Image.open(image_file))

    #Calculate the width and height of the output image
    output_width = int(max(col_num)*(images[0].size[0]/2))
    output_height = int(row_num*(images[0].size[1]/2))

    #Create a new image
    output_image = Image.new('RGB', (output_width, output_height))

    # Loop through the images and paste them onto the output image
    row_count,column_count = 0,0
    x,i,j = 0,0,0   #x:image position for each column,i:image position for each column

    for image in images:
        if column_count == col_num[j]:
            j += 1
            column_count = 0
            x = 0
            i += int(output_height/row_num)

        output_image.paste(image.resize((int(image.size[0]/2), 
                                         int(image.size[1]/2))), (x, i))
        x += int(image.size[0]/2)  #Position in x for the image
        column_count += 1
    
    output_image.save("Eigenfunctions_Eigensolver.jpg")




