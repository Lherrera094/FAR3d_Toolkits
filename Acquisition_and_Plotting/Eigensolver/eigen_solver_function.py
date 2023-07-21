#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


saving_file = "eigensolver_results"
if not os.path.exists(saving_file):
        os.makedirs(saving_file)


# In[3]:


def egn_df(egn_modes_files):
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
        modes.to_excel(f"{saving_file}/egn_functions_{k}.xlsx", index=False)


# In[4]:


egn_modes = "egn_mode_asci.dat"
egn_df(egn_modes)


# In[10]:


get_ipython().run_line_magic('matplotlib', 'notebook')
#for col in modes.columns:
plt.plot(modes["r/a"],modes["-5/3"])
plt.plot(modes["r/a"],modes["-5/2"])
plt.plot(modes["r/a"],modes["-9/7"])
plt.plot(modes["r/a"],modes["-9/6"])
plt.plot(modes["r/a"],modes["-9/5"])
plt.plot(modes["r/a"],modes["-13/9"])
plt.plot(modes["r/a"],modes["-13/8"])
plt.plot(modes["r/a"],modes["-13/7"])
plt.plot(modes["r/a"],modes["-17/12"])
plt.plot(modes["r/a"],modes["-17/11"])
plt.plot(modes["r/a"],modes["-17/10"])

plt.plot(modes["r/a"],modes["5/-3"],"--")
plt.plot(modes["r/a"],modes["5/-2"],"--")
plt.plot(modes["r/a"],modes["9/-7"],"--")
plt.plot(modes["r/a"],modes["9/-6"],"--")
plt.plot(modes["r/a"],modes["9/-5"],"--")
plt.plot(modes["r/a"],modes["13/-9"],"--")
plt.plot(modes["r/a"],modes["13/-8"],"--")
plt.plot(modes["r/a"],modes["13/-7"],"--")
plt.plot(modes["r/a"],modes["17/-12"],"--")
plt.plot(modes["r/a"],modes["17/-11"],"--")
plt.plot(modes["r/a"],modes["17/-10"],"--")


# In[ ]:




