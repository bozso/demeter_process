# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:52:03 2017

@author: Bozsó István
"""

#%%
import fun.process_data as pd
from os import listdir

#%%

data_dir = r'C:\Users\Bozsó István\Documents\demeter\IAP_data\\'
input_paths = [data_dir + path for path in listdir(data_dir)]

#%%

req = ['cnesjd', 'h', 'mlat', 'mlon', 'alt']
day, _ = pd.read_data(input_paths, required=req)

#%%