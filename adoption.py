# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 20:08:34 2022

@author: faiza
"""

##RANAS adoption of technologies

##drip adoption
##at the start of new year
from Agg_Disagg import *
import numpy as np
from settings import * 
import variables
import math
import random
from crop_farmer_data import *
from cal_para import *
##memory decay rate
d = 0.20
##damage by wens and PMT = 1 - exp(-harvestloss)
##See for last 10 year drought question

# =============================================================================
# def indices(far_len):
#         # Randomly assign each farmer to either group 1 (drip-first) or group 0 (BW-first)
#     group_assignment = np.random.choice([0, 1], size=far_len)
#                 
#     # Apply the adoption functions based on the group assignment
#     # Assuming drip_adoption and bw_adoption functions can take an array of farmer indices
#     drip_first_indices = np.where(group_assignment == 1)[0]
#     bw_first_indices = np.where(group_assignment == 0)[0]
#                   # Apply adoption functions for each group
#     variables.drip_adopt_f[drip_first_indices, :] = drip_adoption(yr1, t, drip_first_indices)
#     drip_adopt =variables.drip_adopt_f[:, t] - variables.drip_adopt_f[:, t-1] 
#     drip_co = np.where(drip_adopt ==1, drip_cost1, 0)
#     variables.Capital[:,t]=variables.Capital[:,t]-drip_co
#                 
#     variables.bw_adopt_f[drip_first_indices, :] = bw_adoption(yr1, t, drip_first_indices)
#     bw_adopt =variables.bw_adopt_f[:, t] - variables.bw_adopt_f[:, t-1] 
#     bw_co = np.where(bw_adopt ==1, bw_cost1, 0)
#     variables.Capital[:,t]=variables.Capital[:,t]-bw_co
#                 
#     variables.bw_adopt_f[bw_first_indices, :] = bw_adoption(yr1, t, bw_first_indices)
#     bw_adopt =variables.bw_adopt_f[:, t] - variables.bw_adopt_f[:, t-1] 
#     bw_co = np.where(bw_adopt ==1, bw_cost1, 0)
#     variables.Capital[:,t]=variables.Capital[:,t]-bw_co
#                 
#                 
#     variables.drip_adopt_f[bw_first_indices, :] = drip_adoption(yr1, t, bw_first_indices)
#     drip_adopt =variables.drip_adopt_f[:, t] - variables.drip_adopt_f[:, t-1] 
#     drip_co = np.where(drip_adopt ==1, drip_cost1, 0)
#     variables.Capital[:,t]=variables.Capital[:,t]-drip_co
#                 
#     return drip_first_indices, bw_first_indices
# =============================================================================

def risk(t):
    variables.drought[:,t] = np.where(variables.rainfall_year[:,t]<= 400, 1,0)
    variables.drought_f = disagg_n(variables.drought, variables.drought_f,grid_code,farmer_code,t)

    #risk = variables.drought_f[:,t]
    #risk_n = (risk- np.min(data)) / (np.max(data) - np.min(data))
    ##normalise between 0 to 4
    #risk = ((risk- min(risk)) / (max(risk) - min(risk)))*4
    variables.risk[:,t]= variables.drought_f[:,t] + variables.risk[:,t-1] - d*variables.risk[:,t-1]
    return variables.risk
    
def impact(t):
    variables.drought[:,t] = np.where(variables.rainfall_year[:,t]<= 400, 1,0)
    variables.drought_f = disagg_n(variables.drought, variables.drought_f,grid_code,farmer_code,t)

    ##count impact on yields
    impact = variables.drought_f[:,t]*(1-variables.avg_yield[:,t]) # 1 minus gives the reduction in drought year.##avg yield is ratio.
    
    ##normalise betwee on to 4
    #impact =  ((impact- min(impact)) / (max(impact) - min(impact)))*4
    variables.impact[:,t]= impact - d*variables.impact[:,t-1] +  variables.impact[:,t-1] 
    return variables.impact
    
def norm(t):
    c= t-1
    variables.drip_adopt_g=agg_n(variables.drip_adopt_g, variables.drip_adopt_f,grid_code,farmer_code,c)
    variables.percent_g[:,t] = np.where(grid_code.num_farmers>0, (variables.drip_adopt_g[:,c]/grid_code.num_farmers)*100,0)
    variables.percent_g[:,t] = ((variables.percent_g[:,t]- 0) / (100 - 0))*4
    variables.percent_f=disagg_n(variables.percent_g, variables.percent_f,grid_code,farmer_code,t)
    return variables.percent_f
   
def norm_b(t):
    c= t-1
    variables.bw_adopt_g=agg_n(variables.bw_adopt_g, variables.bw_adopt_f,grid_code,farmer_code,c)
    variables.percent_b_g[:,t] = np.where(grid_code.num_farmers>0, (variables.bw_adopt_g[:,c]/grid_code.num_farmers)*100,0)
    
    ##whole watershed
    #whole = np.sum(variables.bw_adopt_g[:,c],0)
    #whole_per = (whole/far_len)*100
    #whole_per = ((whole_per- 0) / (100 - 0))*4
    
    variables.percent_b_g[:,t] = (variables.percent_b_g[:,t]- 0) / (100 - 0)*4 # 0.25*whole_per + 0.75*((variables.percent_b_g[:,t]- 0) / (100 - 0))*4
    variables.percent_b_f=disagg_n(variables.percent_b_g, variables.percent_b_f,grid_code,farmer_code,t)
    
    return variables.percent_b_f
   
def attitude(t, yr1,f):
    risk_drip, impact_drip,ability_drip,attitude_drip, norm_drip,intercept_drip,ability_bw,attitude_bw,norm_bw,water_bw,area_bw,intercept_bw,intercept_wheat,GWL_wheat,intercept_cotton,year_cotton_b,year_cotton_a,training_per,income_per,threshold_drip, threshold_bw,livestock_bw, plan_bw = cal_par4(f)
    
   
    #yield of other
    ##yield aggregated to grid level
    adopters= np.where(variables.drip_adopt_f[:,t-1]==1, variables.avg_yield[:,t],0)
    variables.avg_yield_g_ad=agg_mean(variables.avg_yield_g_ad, adopters,grid_code,farmer_code,t)
    
    non_adopters = np.where(variables.drip_adopt_f[:,t-1]==0, variables.avg_yield[:,t],0)
    variables.avg_yield_g_nad=agg_mean(variables.avg_yield_g_nad, non_adopters,grid_code,farmer_code,t)
    ##when there is no adopters who else they will copu
    variables.benefit_g[:,t] = np.where(variables.avg_yield_g_ad[:,t]>0,(variables.avg_yield_g_ad[:, t] - variables.avg_yield_g_nad[:,t])*100,0)
    variables.benefit_g[:,t] = np.where(variables.benefit_g[:,t]>0,((variables.benefit_g[:,t]- min(variables.benefit_g[:,t])) / (max(variables.benefit_g[:,t]) - min(variables.benefit_g[:,t])))*4,0)
    
    variables.benefit_f = disagg_n(variables.benefit_g, variables.benefit_f,grid_code,farmer_code,t)
    #training
     ##
    column_index = training.columns.get_loc(str(yr1[t]))
    train=training.iloc[:,column_index]
    #random_numbers = np.random.rand(variables.training_f[:,t].size) 
    # Select the elements where the random number is less than 0.05
    #mask = random_numbers < 0.05
    # Replace the selected elements with the value 1=4
    if (yr1[t]< 2005):
        variables.training_f[:,t] = 0
        training_per1 = 0
    else:
        variables.training_f[:,t] = np.where(train==1,4,0)
        training_per1 = training_per
    #variables.training_f[:,t] = np.where(train==1,4,0)
    #variables.training_f[:,t]= training[:,t]
    #final attiude
    
    variables.attitude[:,t] = (1-training_per1)*variables.benefit_f[:,t] + training_per1*variables.training_f[:,t]
    return variables.attitude

def attitude_b(t,yr1):
    #yield of other
    ##yield aggregated to grid level
    adopters= np.where(variables.bw_adopt_f[:,t-1]==1, variables.avg_yield[:,t],0)
    
    variables.avg_yield_g_ad_b=agg_mean(variables.avg_yield_g_ad_b, adopters,grid_code,farmer_code,t)
    
    
    non_adopters = np.where(variables.bw_adopt_f[:,t-1]==0, variables.avg_yield[:,t],0)
    variables.avg_yield_g_nad_b=agg_mean(variables.avg_yield_g_nad_b, non_adopters,grid_code,farmer_code,t)
    ##when there is no adopters who else they will copu
    variables.benefit_g_b[:,t] = np.where(variables.avg_yield_g_ad_b[:,t]>0,(variables.avg_yield_g_ad_b[:, t] - variables.avg_yield_g_nad_b[:,t])*100,0)
    variables.benefit_g_b[:,t] = np.where(variables.benefit_g_b[:,t]>0,((variables.benefit_g_b[:,t]- min(variables.benefit_g_b[:,t])) / (max(variables.benefit_g_b[:,t]) - min(variables.benefit_g_b[:,t])))*4,0)
    
    variables.benefit_f_b = disagg_n(variables.benefit_g_b, variables.benefit_f_b,grid_code,farmer_code,t)
    #training
    #random_numbers = np.random.rand(variables.training_f[:,t].size) 
    # Select the elements where the random number is less than 0.05
    #mask = random_numbers < 0.05
    # Replace the selected elements with the value 1=4
    #variables.training_f_b[:,t][mask] = 4
    #variables.training_f[:,t]= training[:,t]
    #column_index = training.columns.get_loc(str(yr1[t]))
    #train=training.iloc[:,column_index]
    #random_numbers = np.random.rand(variables.training_f[:,t].size) 
    # Select the elements where the random number is less than 0.05
    #mask = random_numbers < 0.05
    # Replace the selected elements with the value 1=4
    #if (yr1[t]< 2005):
    #    variables.training_f[:,t] = 0
    #else:
    #    variables.training_f[:,t] = np.where(train==1,4,0)
    #final attiude
    variables.attitude_b[:,t] = variables.benefit_f_b[:,t] #+ 0.50*variables.training_f_b[:,t]
    return variables.attitude_b


def ability(t,yr1):
    #variables.exp[:,t] = farmer_profile.exp + t
    ## may be with capital?

    ability_n = np.where(variables.Capital[:,t]<0,0,variables.Capital[:,t])
    aa = max(variables.Capital[:,t])
    if min(variables.Capital[:,t])<0:
        min_c = 0
    else:
        min_c = min(variables.Capital[:,t])
    
    if aa <= 0:
        variables.ability[:,t]=0
    else:
        variables.ability[:,t] = ((ability_n - min_c) / (max(variables.Capital[:,t]) - min_c))*4
        
    #if (yr1[t]< 2005):
    #    accessibility = 0.25
    #else:
    #    accessibility = 0.75
    #variables.training_f[:,t] = np.where(train==1,4,0)
    #variables.training_f[:,t]= training[:,t]
    #final attiude
    
    variables.ability[:,t]=variables.ability[:,t]
    
    return variables.ability

def drip_adoption(yr1,t,f):
    
    risk_drip, impact_drip,ability_drip,attitude_drip, norm_drip,intercept_drip,ability_bw,attitude_bw,norm_bw,water_bw,area_bw,intercept_bw,intercept_wheat,GWL_wheat,intercept_cotton,year_cotton_b,year_cotton_a,training_per,income_per,threshold_drip, threshold_bw,livestock_bw, plan_bw = cal_par4(f)
       # Find the column index that matches the value
    column_index = farm_irr.columns.get_loc(str(yr1[t]))
    ##irrigation varaible is 0 or 1
    irrigation = farm_irr.iloc[:,column_index]
    
    variables.risk = risk(t)
    risk_n = ((variables.risk[:,t]- min(variables.risk[:,t])) / (max(variables.risk[:,t]) - min(variables.risk[:,t])))*4
    #print(risk_n)
    
    variables.impact = impact(t)
    impact_n = ((variables.impact[:,t]- min(variables.impact[:,t])) / (max(variables.impact[:,t]) - min(variables.impact[:,t])))*4
    
    variables.ability = ability(t,yr1)
    
    
    variables.percent_f= norm(t)
    variables.attitude = attitude(t, yr1,f)
    variables.value[:,t] = intercept_drip + ability_drip*variables.ability[:,t]+risk_drip*risk_n +impact_drip*impact_n+  attitude_drip*variables.attitude[:,t] + norm_drip*variables.percent_f[:,t]
    variables.prob[:,t] = np.exp(variables.value[:,t])/(1+ np.exp(variables.value[:,t]))
    
    if (yr1[t]< 2005):
        drip_cost1 = 1.5*drip_cost*farmer_profile.area
    else:
        drip_cost1 = 0.5*drip_cost*farmer_profile.area
    
    variables.drip_adopt_f[:, t] = np.where(variables.drip_adopt_f[:, t-1] == 1,1, np.where(irrigation == 0, 0, np.where(variables.Capital[:,t]<= drip_cost1, 0, np.where(variables.prob[:,t]<=threshold_drip,0, 1))))
    return variables.drip_adopt_f,drip_cost1
    

##borewell

def bw_adoption(yr1,t,f):
    risk_drip, impact_drip,ability_drip,attitude_drip, norm_drip,intercept_drip,ability_bw,attitude_bw,norm_bw,water_bw,area_bw,intercept_bw,intercept_wheat,GWL_wheat,intercept_cotton,year_cotton_b,year_cotton_a,training_per,income_per, threshold_drip, threshold_bw, livestock_bw, plan_bw = cal_par4(f)
       # Find the column index that matches the value
    column_index = farm_irr.columns.get_loc(str(yr1[t]))
    ##irrigation varaible is 0 or 1
    irrigation = farm_irr.iloc[:,column_index]
    
    ##cd distance
    if (yr1[t]< 2002):
        bw_cost1 = 2*bw_cost
        access = 0.25
     
    else:
        bw_cost1 = bw_cost
        access = 0.5

    
    variables.percent_b_f= norm_b(t)
    variables.attitude_b = attitude_b(t, yr1)
    variables.ability = ability(t,yr1)
    variables.value_b[:,t] = intercept_bw + attitude_bw*variables.attitude_b[:,t] + norm_bw*variables.percent_b_f[:,t] + water_bw*farmer_profile.water + area_bw*(farmer_profile.area*6.18) + livestock_bw*farmer_profile.livestock + plan_bw*variables.ability[:,t]*access
    
    variables.prob_b[:,t] = np.exp(variables.value_b[:,t])/(1+ np.exp(variables.value_b[:,t]))

    numbers = [1, 0]  # 1 represents the desired number, 0 represents other numbers
    weights = [0.33, 0.67]  # 33% weight for 1, 67% weight for 0
    # Generate a random number for each farmer

    # Generate a random number for each farmer
    random_number = [random.choices(numbers, weights=weights)[0] if bw_adopt_value != 1 else 0 for bw_adopt_value in variables.bw_adopt_f[:, t-1]]

    #random_number =random.choices(numbers, weights=weights)[0]
 
    variables.bw_adopt_f[:, t] = np.where(variables.bw_adopt_f[:, t-1] == 1,1, np.where(irrigation == 0, 0, np.where(variables.Capital[:,t]<= bw_cost1, 0, np.where(variables.prob_b[:,t]<=threshold_bw,0,1))))
    bw_adopt =variables.bw_adopt_f[:, t] - variables.bw_adopt_f[:, t-1] 
    bw_co = np.where(bw_adopt ==1, bw_cost1, 0)
    ##final actual based on failure of well
    variables.bw_adopt_f[:, t] = np.where(variables.bw_adopt_f[:, t-1] == 1,1, np.where(variables.bw_adopt_f[:, t] == 1, variables.bw_adopt_f[:, t]*random_number,0))
    
    return variables.bw_adopt_f,bw_co,variables.value_b,variables.prob_b
    

    
