# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 09:59:02 2023

@author: faiza
"""

from Householdmodel import *
from stats import *
from settings import *
import importlib
import variables
def main_loop():
    for f in range (0,1):
        print(f)
       

        sociohydmodel(f)
        
        
        
        
        cal_runoff(f)
        GWL_cal(f)
        #Yield(f)
        
        my_module = importlib.import_module('variables')
        module = {'variables': my_module}
        importlib.reload(module['variables'])
        
