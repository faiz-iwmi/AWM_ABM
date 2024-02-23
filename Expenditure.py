#Expenditure is the sum of expenses that a smallholder faces during a year and reduces her capital.

##import other functions
import numpy as np
from settings import *
from crop_farmer_data import *
import variables


##thsi function is calculatin bith cost and expenditure

##function when agent

def Expenditure_ag(t, crop):     
    #'this is the expenditure function blablabla'
    
    for c in range(0,crop-2):
        variables.Production[c,:,t] = variables.Yield[c,:,t]*variables.crop_area_f[c,:,t]
        #cost as cost/ton
        variables.crop_cost[c,:,t]=variables.crop_var.iloc[18,c+1]*variables.Production[c,:,t]
        variables.total_cost[:,t] = variables.total_cost[:,t] + variables.crop_cost[c,:,t]
    

    variables.expenditure[:,t]=variables.total_cost[:,t]
    
    return variables.crop_cost, variables.total_cost,variables.expenditure
    #return (E, crop_cost,labour_balance)   

