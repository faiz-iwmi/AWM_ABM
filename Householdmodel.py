
# -*- coding: utf-8 -*-


# Import modules 
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import pandas as pd
from settings import *
from space_time_fn import *

from climate_data import *
from crop_farmer_data import *
# Import local modules
from Net_household_income import *
from Expenditure import *
#from crop_cost_balance import *
#from crop_cost_compute import *
from WB_yield_space_runoff import *
from crop_yield import *
from adoption import *
#importlib.reload(sys.modules['settings'])
#import time
#from spatial_data2 import *
from cal_para import *
from spatial_data import *
from output import*
#from memory_profiler import profile

'''
This is the householdmodel version #1 in python based, this function simulates 
five states defining the socio-hydrological situation of a smallholder. If you 
want to reference to this model reference to Pande and Savenije (2016) and Den 
Besten et al (2016), doi will follow'
'''
##no ETO. This will be calculated for each year.
#@profile
#def sociohydmodel(top,bottom,cap_ris_max,aq_depth,YieldGw,deltaGw,alphaGw,BaseThresh,kx,f):

def sociohydmodel(f):              
    import variables
    f1=cal_par_f(f)
    print(f1)

    #days=len(p.time)

    yr1 = np.arange(start_year,end_year+1)
    if wheat_s == 1:
        wheatarea=1
    else:
        filename = f"D:/PhD_work/Code/output/Run_2/Wheat_area_f/wheat_area_f_{f1}.xlsx"
        # Read the file into a DataFrame
        wheatarea = pd.read_excel(filename)
        wheatarea=wheatarea.iloc[:, 1:27]
         # Define the new column names as strings representing years from 1990 to 2009
        new_columns = yr1[0:26]
        # Rename the columns
        wheatarea.columns = new_columns
    day=0
    #for t in range(constants['Tsimul']): #tsimul is just a number
    for t in range(0,Tsimul):    
        yearstart = str(yr1[t]) + '-06-15'
        yearend = str(yr1[t+1]) + '-06-14'
        
        if excel_flag==1:
            rainfall_ex = pd.read_csv(rainfall_e) 
            rainfall_ex['date'] = pd.to_datetime(rainfall_ex['date'])
            rainfall_ex=rainfall_ex[rainfall_ex['date'].ge(sim_start) & rainfall_ex['date'].le(sim_end)]
            precip1=rainfall_ex[rainfall_ex['date'].ge(yearstart) & rainfall_ex['date'].le(yearend)]
            day_end=len(precip1)
        else:
            precip1 = data_year_filter(p, yearstart, yearend)
            day_end=len(precip1.time)
            rainfall_ex=0
        

        t_mean1= data_year_filter(t_mean, yearstart, yearend)
        
        
        if t == 0:
##intitalise hydrology paramters by a number or by a initial map
            variables.Capital[:,0]=capital
            variables.rootdrain[:, day:day+day_end] = 0
            variables.percloation[:, day:day+day_end] = 0
            variables.RootWater[:, day:day+day_end] = 80
            variables.caprise[:, day:day+day_end]=0
            variables.SubWater[:, day:day+day_end] =50
            variables.subpercolation[:, day:day+day_end] = 0
            variables.baseflow[:, day:day+day_end] = 0
            variables.GWS[:, day:day+day_end]=100
            #random_numbers = np.random.rand(variables.training_f[:,t].size) 
    # Select the elements where the random number is less than 0.02
            #mask = random_numbers < 0.01
    # Replace the selected elements with the value 1
            #variables.drip_adopt_f[:,t][mask] = 1
            #variables.bw_adopt_f[:,t][mask] = 1
            #variables.GWL[:, day:day+day_end] = 0
            if excel_flag==1:
                aa=np.sum(precip1["rainfall(mm)"])
                variables.rainfall_year[:,t]=aa
            else:
                aa=precip1.sum(dim="time")
                variables.rainfall_year[:,t]= aa.rain.values.ravel()
            
            
            #print(day)
            #print(day+day_end)
            day=day+day_end
            #print("year", yr1[t])
            
            #print(day)
            
        else:
            #print(RF1)
            variables.runoff,variables.ETp, variables.ETa,variables.routed_runoff= WB_Yield(precip1, t_mean1,p,t_mean,day,day_end,t, excel_flag, yr1,f,wheatarea)
            
            
            #variables.Yield_irr, variables.Yield_rain = crop_yield(day,precip1,t,day_end)  
            variables.Yield = crop_yield_ag(day,precip1,t, crop, day_end,yr1)
            ##result stored yearly, crop wise
           
            #variables.crop_Income_rain, variables.crop_Income_irr= Net_household_income(constants, lenght,t) 
            variables.income,  variables.Production,variables.sales = Net_household_income_ag(t, crop,f) 
            # crop costs which is what is calculated in crop_crop_compute.
            
            
            #variables.Crop_cost_rain,variables.Crop_cost_irr,variables.Total_cost_rain, variables.Total_cost_irr,variables.expenditure_irr, variables.expenditure_rain = Expenditure(constants, investment,t)
            variables.crop_cost, variables.total_cost,variables.expenditure = Expenditure_ag(t, crop)
         
##below when each agent
            variables.Capital[:,t] = (1-delt)*variables.Capital[:,t-1] + variables.income[:,t] - variables.expenditure[:,t]
            variables.Capital[:,t]=variables.Capital[:,t]*farmer_profile.include
            variables.Profit[:,t] = variables.income[:,t]-variables.expenditure[:,t]
            variables.Profit[:,t]=variables.Profit[:,t]*farmer_profile.include
            if excel_flag==1:
                aa=np.sum(precip1["rainfall(mm)"])
                variables.rainfall_year[:,t]=aa
            else:
                aa=precip1.sum(dim="time")
                variables.rainfall_year[:,t]= aa.rain.values.ravel()
                
            ##sum up yearly here
            variables.AET_year[:,t] = np.sum(variables.AET_SM[:,day:day+day_end],axis = 1)
            variables.IWR_met_g_mm_year[:,t] =  np.sum(variables.IWR_met_g_mm[:,day:day+day_end],axis = 1)
            
# =============================================================================
#             variables.recharge_year[:,t] = np.sum(variables.recharge[:,day:day+day_end],axis = 1)
#             variables.baseflow_year[:,t] = np.sum(variables.baseflow[:,day:day+day_end],axis = 1)
#             variables.runoff_year[:,t] = np.sum(variables.runoff[:,day:day+day_end],axis = 1)
#             
#             variables.total_runoff_year[:,t] = np.sum(variables.total_runoff[:,day:day+day_end],axis = 1)
#             variables.rootdrain_year[:,t] = np.sum(variables.rootdrain[:,day:day+day_end],axis = 1)
#             
#             variables.percloation_year[:,t] = np.sum(variables.percloation[:,day:day+day_end],axis = 1)
#             variables.subpercolation_year[:,t] = np.sum(variables.subpercolation[:,day:day+day_end],axis = 1)
# =============================================================================
            
            
# =============================================================================
#             #check dam capture
#             variables.check_dam_c_y[:,t]=np.sum(variables.check_dam_c[:,day:day+day_end],axis = 1)
#             #check dam recharge
#             variables.check_dam_r_y[:,t]=np.sum(variables.check_dam_r[:,day:day+day_end],axis = 1)
#             
# =============================================================================
            
            ##sum crop areas
            #variables.Crop_Area_total_year[:,t]=np.sum(variables.Crop_Area_total[:,day:day+day_end],axis = 1)
            
# =============================================================================
#             variables.IWR_T_g_mm_year[:,t] =  np.sum(variables.IWR_T_g_mm[:,day:day+day_end],axis = 1)
#             
#             
#             variables.delta_GWS[:,t]=variables.GWS[:,day]-variables.GWS[:,day+day_end-1]
#             variables.delta_SubWater[:,t]=variables.SubWater[:,day]-variables.SubWater[:,day+day_end-1]
#             variables.delta_RootWater[:,t]=variables.RootWater[:,day]-variables.RootWater[:,day+day_end-1]
# =============================================================================
            if human==1:
                
             
                variables.drip_adopt_f,drip_cost1 =drip_adoption(yr1, t,f)
                drip_adopt =variables.drip_adopt_f[:, t] - variables.drip_adopt_f[:, t-1] 
                drip_co = np.where(drip_adopt ==1, drip_cost1, 0)
                variables.Capital[:,t]=variables.Capital[:,t]-drip_co
                    
                variables.bw_adopt_f,bw_co,variables.value_b,variables.prob_b = bw_adoption(yr1, t,f)
                    #bw_adopt =variables.bw_adopt_f[:, t] - variables.bw_adopt_f[:, t-1] 
                    #bw_co = np.where(bw_adopt ==1, bw_cost1, 0)
                variables.Capital[:,t]=variables.Capital[:,t]- bw_co
                variables.investment[:,t] = drip_cost + bw_cost
               
    
            #print(day)
            #print(day+day_end)
            print("year next", yr1[t])
            #print(day)
            #print(day+day_end)
           
            day=day+day_end
    output_csv(f1)
    return variables.routed_runoff, variables.GWL
            
            

