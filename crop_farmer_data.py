# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 15:10:24 2022

@author: faiza
"""
import pandas as pd
from settings import *

##lets creat farmers and crpp data

##crop data
crop_kc = pd.read_csv(kc)
#root depth
root_depth = pd.read_csv(depth)
#crop variations
crop_var = pd.read_csv(cropvar)
##crop cultivated ratio
crop_ratio = pd.read_csv(crop_area_ratio)

##wheat
#wheatarea= pd.read_csv(wheat_area)

##farmer data
##csv file with farmer data and variables
farmer_profile = pd.read_csv(farmers_data) 
far_len = len(farmer_profile)
farm_irr = pd.read_csv(farmer_irr)

##grid and farmer code
##grid_Code
##give grid id against lat and lon
grid_code= pd.read_csv(grid) 
grid_len = len(grid_code)

##farmer code_grid
##gives farmer id agains grid id and lat and lon
farmer_code = pd.read_csv(farmers_code_grid) 

##training
training = pd.read_csv(far_training)