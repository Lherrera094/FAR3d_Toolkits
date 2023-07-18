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

def run_files(entry,sim):
	print(sim+":")
	subprocess.call("qsub "+entry, shell = True,cwd=sim+"/")
	

def launch_sims(files,launch_num,sh_name): 
    count = 0
    
    for i in range(len(files)):
        file = os.listdir(files[i])
        bash = list(filter(lambda file: "eigen.sh" in file, file))[0]
        print(bash)
        if f"{sh_name}" in file and count < launch_num:
            run_files(bash,files[i])
            count += 1

