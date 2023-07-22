#!/usr/bin/env python
# coding: utf-8
# +
# Developer: Luis Carlos Herrera Quesada
# Date: 02/06/2023
# Universidad Carlos III de Madrid
# -

import os 
import numpy as np

def find_farprt(root_folders):
    search_file = "farprt"  #looks for farprint file in directories
    folders = []
    
    for root_folder in root_folders:
        for root, dirs, files in os.walk(root_folder):
            if search_file in files:
                folders.append(root)
            
    return folders

def sort_key(item):
    parts = item.split('.png')
    first, last = parts[0].split('_')
    return float(first), -float(last)

#Compares the values of growth rate for the toroidal modes 
def check_convergence(list_modes):
    val_0 = list_modes[0]
    chek = True

    #Compare items in list
    for val in list_modes:
        if val_0 != val:
            chek = False
            break

    return chek

def find_profiles(directory):
    
    #looks for the profiles file
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                profile_txt = file
                exist = True
                           
    return file, exist

#Remove not used files for each folder
def remove_files(direct):
    deleted_list = ["xfar3d","fs00000","fort87","fs00001","fs00002","fs00003","fs00004",
                    "fs00005","fs00006","fs00007","fs00008","fs00009"]
    file = os.listdir(direct)
    for f in file:
        if f in deleted_list:
            os.remove(direct + "/"+f)


#returns the modes in the form n/m
def change_modes_order(mode):
    
    modes = mode.split("/")
    n = modes[1]

    if "-" in modes[0]:
        m = modes[0].split("-") 
        m = m[-1]

    elif "  " in modes[0]: 
        m = modes[0].split("  ") 
        m = m[-1]

    else:
        m = modes[0].split(" ") 
        m = m[-1]

    inverted_mode = f"{n}/{m}"

    return inverted_mode


def get_number_line(line):
    #array to save the number values in array
    value = []
    for char in line:
        if char.isdigit() or char == ".":
            value.append(char)

    new_value = "".join(value)
    new_value = float(new_value)

    return new_value
