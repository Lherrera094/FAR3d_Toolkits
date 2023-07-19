#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 19/07/2023
# Universidad Carlos III de Madrid
# %%

import os 
import subprocess
import pandas as pd

def run_files(entry,sim):
    print(f"{sim}:")
    #subprocess.call(f"chmod +xrw {entry}", shell = True, cwd=f"{sim}/")
    #subprocess.call("chmod +xrw "+entry, shell = True,cwd=f"{sim}/")
    subprocess.call("qsub "+entry, shell = True,cwd=sim+"/")          

	

def launch_sims(files,launch_num,sh_name): 
    count = 0
    
    for i in range(len(files)):
        file = os.listdir(files[i])
        bash = f"{sh_name}"
    
        if f"egn_values.dat" not in file and count < launch_num:
            run_files(bash,files[i])
            count += 1

