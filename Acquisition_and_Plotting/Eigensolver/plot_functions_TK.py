#!/usr/bin/env python
# coding: utf-8
# +
# Developer: Luis Carlos Herrera Quesada
# Date: 02/06/2023
# Universidad Carlos III de Madrid
# -

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import os
from ipywidgets import interact, interactive, fixed
from IPython.display import clear_output
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from PIL import Image

from search_and_evaluate_TK import *

def get_colors_dict(n):
    n = int(n)
    
    d =  {
	1: {
            'colfam': "black",
            'colors': ['black','silver'] 
        },
	2: {
            'colfam': 'navy',
            'colors': ["navy","royalblue"]             
        },
    3: {
            'colfam': "darkslategrey",
            'colors': ["darkslategrey","darkturquoise"]             
        },
	4: {
            'colfam': "brown",
            'colors': ["saddlebrown","sandybrown"] 
        },
        
    5: {
            'colfam': 'blue',
            'colors': ['navy','lightskyblue']
        },
    6: {
            'colfam': 'darkturquoise',
            'colors': ['darkcyan','cyan']
        },
        
    7: {
            'colfam': 'limegreen',
            'colors': ['darkgreen','lime']
        },
    8: {
            'colfam': 'springgreen',
            'colors': ["green","springgreen"]
        },
    9: {
            'colfam': "red",
            'colors': ["darkred","red"] 
        },
    10: {
            'colfam': "orange",
            'colors': ["darkgoldenrod","yellow"] 
        },
    11: {
            'colfam': "darkmagenta",
            'colors': ["darkmagenta","magenta"] 
        },
    12: {
            'colfam': "olive",
            'colors': ["olive","darkkhaki"]
        },
    13: {
            'colfam': 'k',
            'colors': ["black","silver"]
        },
    14: {
            'colfam': "red",
            'colors': ['darkred','salmon']
 
        },
    15: {
            'colfam': "dodgerblue",
            'colors': ["steelblue","lightskyblue"] 
        },
    16: {
            'colfam': 'mediumvioletred',
            'colors': ["mediumvioletred","palevioletred"]
        },
    17: {
            'colfam': 'green',
            'colors': ["forestgreen","lawngreen"] 
        },
    }
    
    return d[n]

def plot_eigenfunctions(dm,dm2,dm3,alfm,rp,rp2,rp3,df,r,energy,beta,f,sav_file,tor_coupl, num_pol):
    im = plt.figure(figsize=(9,8))
    i,j,k=0,0,0

    dm = change_modes_order(dm)
    dm2 = change_modes_order(dm2)
    
    #Information about the dominant modes
    plt.annotate(f"Dominant Mode (n/m): {dm}", xy=(0.55, 0.08), xycoords='axes fraction', fontsize = 15)    
    plt.annotate(f"Coupled (n/m): {dm2}", xy=(0.55, 0.05), xycoords='axes fraction', fontsize = 15)             
    #plt.annotate(f"Alfvén Mode: {alfm}", xy=(0.55, 0.17), xycoords='axes fraction', fontsize = 15)
    
    #Marking lines and annotations    
    if 6 in tor_coupl:
        plt.axvline(rp/1000,color="blue",linewidth=1)
            
    else:
        plt.axvline(rp/1000,color="red",linewidth=1)
            
    if rp3 != "--":
        dm3 = change_modes_order(dm3)
        plt.axvline(rp3/1000,color="k",linestyle="--",linewidth=1)
        plt.annotate(f"2nd Coupled (n/m): {dm3}", xy=(0.55, 0.02), xycoords='axes fraction', fontsize = 15)                 
    
    for n in tor_coupl:
        d = get_colors_dict(n)
        plt.axhline(0,xmin = 0.05, xmax = 0.06,color=d["colfam"],linewidth=2,label=f"n= {n}")                   
        k += 1
                
    plt.axvline(rp2/1000,color="k",linewidth=1)
    
    #plot Eigenfunctions
    for m in tor_coupl:
        i,j=0,0
        d = get_colors_dict(m)
        cmap = mc.LinearSegmentedColormap.from_list("", d["colors"])
        
        for col in df.columns:
            if f"/ {m}" in col or f"/{m}" in col:
                if "I" in col:
                    plt.plot(r,df[col],"--",color=cmap(i/num_pol),linewidth=2)
                    i += 1
                if "R" in col:
                    plt.plot(r,df[col],color=cmap(i/num_pol),linewidth=2)
                    j += 1 
    
    plt.title(r"$T_{f}:$" + f"{round(energy)} keV/ "+ r"$\beta_{f}$:"+f"{beta}/ $f$: {round(f)} kHz", fontsize=24)               
    plt.xlabel("r/a")
    plt.ylabel(r"$\delta \Phi$")
    plt.rcParams['axes.labelsize'] = 22
    plt.grid(True)
    plt.legend(loc="upper right",prop={'size':18})
    plt.savefig(f"{sav_file}{round(energy)}_{beta}.png",dpi=350)


#Creates an array of sorted plots for panoramic visualization
def eigenfunction_maps(directory):
    images = []
    
    #Arrange list in descending order for energy and ascending for beta
    act_dir = sorted(os.listdir(directory)) #makes a list of the images names 
    act_dir = sorted(act_dir, key=sort_key,reverse=True)
         
    #Gets the number of energy plots for the array of images
    my_list = [f.split("_")[0] for f in act_dir]
    unique_elements = sorted(set(my_list),reverse=True)
    columns = []
    for element in unique_elements:
        count = my_list.count(element)
        columns.append(count)
        
    column_num = max(columns)
    row_num = len(columns)
    
    # Loop through the directory and add the images to a list
    for filename in act_dir:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            images.append(Image.open(os.path.join(directory, filename)))
            
    # Calculate the width and height of the output image
    output_width = int(column_num*(images[0].size[0]/2))
    output_height = int(row_num*(images[0].size[1]/2))

    #Create a new image
    output_image = Image.new('RGB', (output_width, output_height))
    
    # Loop through the images and paste them onto the output image
    row_count,column_count = 0,0
    num_col = 0
    x,i = 0,0 #x:image position for each column,i:image position for each column
    
    for image in images:
        if column_count == columns[num_col]:
            num_col += 1
            column_count = 0
            x = 0
            i += int(output_height/row_num) 
        
        output_image.paste(image.resize((int(image.size[0]/2), 
                                         int(image.size[1]/2))), (x, i))
        x += int(image.size[0]/2)  #Position in x for the image
        column_count += 1    
        
    output_image.save("Eigenfunctions_full.jpg")


