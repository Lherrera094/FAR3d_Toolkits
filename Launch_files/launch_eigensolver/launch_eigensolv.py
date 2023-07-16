#!/usr/bin/env python
# coding: utf-8


import sys 
sys.path.append('FAR3_libraries/')
from launch_eigenfunctions_TK import *

launch_num = 16 #number of simulations to launch

act_dir = os.listdir()
files = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))

om_0, gamma = get_values_df(files)

print(om_0, gamma)

#done = launch_sims(files,launch_num)




