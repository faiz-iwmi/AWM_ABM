import numpy as np
from settings import * 
from crop_farmer_data import *
import variables
from cal_para import *

##function when agent
def Net_household_income_ag(t, crop, f):
    #'this function describes the net household income' # This is actually gross income, not net.
    for c in range(0,crop-2):
        
        variables.Yield[c,:,t] = fertilizer_factor*variables.Yield[c,:,t]
        #considering all is being sold for now
        #crop_for_home_consumption = np.minimum((Yield_nh*constants['crop_area']), constants['crop_for_home_consumption']) 
        #Quantity_of_crop_sold = np.maximum((Yield_nh*constants['crop_area']) - crop_for_home_consumption,0.)
        variables.Production[c,:,t] = variables.Yield[c,:,t]*variables.crop_area_f[c,:,t]
        variables.sales[c,:,t] = crop_var.iloc[19,c+1]*variables.Production[c,:,t]*selling_factor
    
    for c in range(0,crop-2):
        aa=variables.sales[c,:,t]
        variables.income[:,t]=aa + variables.income[:,t]
    ##assuming  income is also spent on outside farm actiivites. x % is spent on agruclture
    risk_drip, impact_drip,ability_drip,attitude_drip, norm_drip,intercept_drip,ability_bw,attitude_bw,norm_bw,water_bw,area_bw,intercept_bw,intercept_wheat,GWL_wheat,intercept_cotton,year_cotton_b,year_cotton_a,training_per,income_per,threshold_drip, threshold_bw,livestock_bw, plan_bw = cal_par4(f)
    variables.income[:,t] = income_per*variables.income[:,t] 
    return variables.income,  variables.Production,variables.sales
