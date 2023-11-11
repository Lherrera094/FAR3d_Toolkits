#!/usr/bin/env python
# coding: utf-8
# Developer: Luis Carlos Herrera Quesada
# Date: 10/04/2023
# Universidad Carlos III de Madrid

import sys 
sys.path.append('FAR3_libraries/')
from launch_eigensolver_TK import *

launch_num = 5 #number of simulations to launch

sh_name = "TJII_eigen.sh"

act_dir = os.listdir()
files = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))

done = launch_sims(files,launch_num, sh_name)




