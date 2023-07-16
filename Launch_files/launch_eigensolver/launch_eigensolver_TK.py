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
	

def launch_sims(files,launch_num): 
    count = 0
    
    for i in range(len(files)):
        file = os.listdir(files[i])
        bash = list(filter(lambda file: ".sh" in file, file))[0]
        if "farprt" not in file and count < launch_num:
            run_files(bash,files[i])
            count += 1

def get_values_df(files):

    for file in files:
        if "Output_" and ".xlsx" in file:
            df = file

    dataframe = pd.read_csv(df)
    om_0 = dataframe["Frequency"]
    gamma = dataframe["Growth Rate"]

    return om_0, gamma

