# -*- coding: utf-8 -*-
##this code at the start of year and season
import numpy as np
import pandas as pd
from Agg_Disagg import *
from settings import *
from cal_loop import *
from cal_para import *
from settings import *
##select which crop and how much area of that crop farmer takes

## logic below which one can change later

## for monsoon crop

#1. Farmer check last year rainfall
##2. Faamrer check how much irrigation storage and how much area it can prvodie irrigation
##3. farmer see relative profit of each crop and do some optimisation here
##3. later we can have capital, yield, memory and all
##4. farmer check how much cotton and groundnit to take

##this function is applied at the start of year which starts with monsoon season

##outputs to a matrix
##2 d array of each crop
## with length of farmers
## for each year area, goes there
def crop_area(farmer_profile,crop_area_f,crop_irr_f, crop_rain_f, t, crop, crop_var,j, i, GWL_f, crop_ratio, yr1,aq_depth, irrigation,f,ratio_cotton_wocd, ratio_cotton_cd, wheatarea):
    spatial['RootField'],spatial['RootWilt'], RF , RWP, Irr, GN_irr = cal_par2(f)
    risk_drip, impact_drip,ability_drip,attitude_drip, norm_drip,intercept_drip,ability_bw,attitude_bw,norm_bw,water_bw,area_bw,intercept_bw,intercept_wheat,GWL_wheat,intercept_cotton,year_cotton_b,year_cotton_a,training_per,income_per,threshold_drip, threshold_bw,livestock_bw, plan_bw = cal_par4(f)
   
    
    for c in range(0,crop-2):
        # Find the column index that matches the value
        #column_index = farm_irr.columns.get_loc(str(yr1[t]))
        
        
##from crop ration sheet find ration for the given year
        a=crop_ratio.index[crop_ratio['Year'] == yr1[t]]
        
        ##first version where irrigaton holdin gbase don admin data
        #irr=crop_ratio.columns.get_loc("ratio[irr]")
        #ratio_irr = crop_ratio.iloc[a,irr]
        #rainf=crop_ratio.columns.get_loc("ratio[rain]")
        #ratio_rain= crop_ratio.iloc[a,rainf]
        #NSA=crop_ratio.columns.get_loc("ration[NCA]")
        #ratio_NSA = crop_ratio.iloc[a,NSA]
        
        ###from crop ration version 2 where % cotton irrigated is taken as % irrigation holdings
        ##ration of model area to be multiplied to match observed NSA
        NSA=crop_ratio.columns.get_loc("ration[NCA]")
        ratio_NSA = crop_ratio.iloc[a,NSA]
        
        ##ration of cotton area in that
        #cotton=crop_ratio.columns.get_loc("Cotton_r_NSA")
        #ratio_cotton = crop_ratio.iloc[a,cotton]
        if yr1[t] <= 2002:
            ratio_cotton_wocd[t] = intercept_cotton + year_cotton_b*yr1[t]
            ratio_cotton_cd[t]= ratio_cotton_wocd[t]
        else:
            ratio_cotton_wocd[t] = intercept_cotton + year_cotton_b*yr1[t]
            ratio_cotton_cd[t]= ratio_cotton_cd[t-1] + year_cotton_a
        
        if cotton_s != 1:
            ratio_cotton_cd[t]=ratio_cotton_wocd[t]
             
        ##rations for cd and wocd farmers
        
        #cotton_wocd=crop_ratio.columns.get_loc("Cotton/NSA_wocd")
        #ratio_cotton_wocd = crop_ratio.iloc[a,cotton_wocd]
        
        #cotton_cd=crop_ratio.columns.get_loc("Cotton/NSA_cd")
        #ratio_cotton_cd = crop_ratio.iloc[a,cotton_cd]
        
        #ratio_cotton_cd[t]=ratio_cotton_wocd[t]
        #if inte ==0:
        #    ratio_cotton_cd=ratio_cotton_wocd
            
        ##ration of cotton irrigated
        irr_c=crop_ratio.columns.get_loc("Cotton_IR")
        ratio_irr_c = crop_ratio.iloc[a,irr_c]
        
        
        #irr_cal = Irr ##caliberating parameter
        if c==0: #for cotton
            if j == crop_var.iloc[10,c+1]:
             
                #crop_area_f[c,:,t]= np.where(irrigation == 1, (ratio_irr.iloc[0]*farmer_profile.area*ratio_NSA.iloc[0]), (ratio_rain.iloc[0]*farmer_profile.area*ratio_NSA.iloc[0]))
                #crop_irr_f[c,:,t]= np.where(irrigation == 1, (ratio_irr.iloc[0]*farmer_profile.area*ratio_NSA.iloc[0]), 0)
                #crop_rain_f[c,:,t]= np.where(irrigation == 0, (ratio_rain.iloc[0]*farmer_profile.area*ratio_NSA.iloc[0]), 0)
                ##2nd version
                #crop_area_f[c,:,t]= farmer_profile.area*ratio_NSA.iloc[0]*ratio_cotton.iloc[0]
                ##3rd version where ratio is different for cd and wocd farmers
                #crop_area_f[c,:,t]= np.where(farmer_profile.cd == 1, farmer_profile.area*ratio_NSA.iloc[0]*ratio_cotton_cd[t], farmer_profile.area*ratio_NSA.iloc[0]*ratio_cotton_wocd[t])
                crop_irr_f[c,:,t]=np.where(irrigation == 1, np.where(farmer_profile.cd == 1, farmer_profile.area*ratio_NSA.iloc[0]*ratio_cotton_cd[t], farmer_profile.area*ratio_NSA.iloc[0]*ratio_cotton_wocd[t]),0)
                crop_rain_f[c,:,t]=np.where(irrigation ==0, farmer_profile.area*ratio_NSA.iloc[0]*ratio_cotton_wocd[t],0)
                crop_area_f[c,:,t]=  crop_irr_f[c,:,t] + crop_rain_f[c,:,t]
               
                #crop_irr_f[c,:,t]= crop_area_f[c,:,t]*ratio_irr_c.iloc[0]
                #crop_rain_f[c,:,t]= crop_area_f[c,:,t]-crop_irr_f[c,:,t]
                #farm_irr.iloc[:,column_index] == 1
        elif c==1: #for groundnut
            if j == crop_var.iloc[10,c+1]:
                
                #crop_area_f[c,:,t]= np.where(irrigation == 1, ((1-ratio_irr.iloc[0])*farmer_profile.area*ratio_NSA.iloc[0]), ((1-ratio_rain.iloc[0])*farmer_profile.area*ratio_NSA.iloc[0]))
                #crop_irr_f[c,:,t]= np.where(irrigation == 1, ((1-ratio_irr.iloc[0])*farmer_profile.area*ratio_NSA.iloc[0]), 0)
                #crop_rain_f[c,:,t]= np.where(irrigation == 0, ((1-ratio_rain.iloc[0])*farmer_profile.area*ratio_NSA.iloc[0]), 0)
                
                ##2nd version
                #crop_area_f[c,:,t]= farmer_profile.area*ratio_NSA.iloc[0]*(1-ratio_cotton.iloc[0])
                
                ##3rd version where ratio is different for cd and wocd farmers
                #crop_area_f[c,:,t]= np.where(farmer_profile.cd == 1, farmer_profile.area*ratio_NSA.iloc[0]*(1-ratio_cotton_cd[t]), farmer_profile.area*ratio_NSA.iloc[0]*(1-ratio_cotton_wocd[t]))
                
                #crop_irr_f[c,:,t]=  crop_area_f[c,:,t]*ratio_irr_c.iloc[0]*GN_irr
                #crop_rain_f[c,:,t]= crop_area_f[c,:,t]-crop_irr_f[c,:,t]
                
                crop_irr_f[c,:,t]=np.where(irrigation == 1, np.where(farmer_profile.cd == 1, farmer_profile.area*ratio_NSA.iloc[0]*(1-ratio_cotton_cd[t]), farmer_profile.area*ratio_NSA.iloc[0]*(1-ratio_cotton_wocd[t])),0)
                crop_rain_f[c,:,t]=np.where(irrigation ==0, farmer_profile.area*ratio_NSA.iloc[0]*(1-ratio_cotton_wocd[t]),0)
                crop_area_f[c,:,t]=  crop_irr_f[c,:,t] + crop_rain_f[c,:,t]
               
                
        elif c==2: #for wheat with c==2
        ##for wheat area, control is defined as alternative where checkdams wer not there
        ##in that case, they kept on doing the same wheat area as in case of without checkdams
        
            if j == crop_var.iloc[10,c+1]:
                #crop_area_f[c,:,t]= crop_area_f[c-1,:,t]
                b= aq_depth-GWL_f[:,i-1]
                crop_area_f[c,:,t]=np.where(irrigation == 1, ((GWL_wheat*b + intercept_wheat)*farmer_profile.area*ratio_NSA.iloc[0]), 0)
                if wheat_s == 1:
                    crop_area_f[c,:,t]=np.where(irrigation == 1, ((GWL_wheat*b + intercept_wheat)*farmer_profile.area*ratio_NSA.iloc[0]), 0)
                #crop_area_f[c,:,t]=((-0.0212*b + 0.28)*farmer_profile.area*ratio_NSA.iloc[0])
                else:
                    column_index1 = wheatarea.columns.get_loc(yr1[t])
                    crop_area_f[c,:,t]=wheatarea.iloc[:,column_index1]
                    
                
                crop_area_f[c,:,t]= np.where(crop_area_f[c,:,t]<0,0,crop_area_f[c,:,t])
                crop_irr_f[c,:,t]= crop_area_f[c,:,t]
                crop_rain_f[c,:,t]= 0
                
                
    return crop_area_f, crop_irr_f,crop_rain_f,ratio_cotton_wocd,ratio_cotton_cd

##function irrigation

def irrigation(ETp_ag, ETa_ag,IWR_ag,IWR_ag_acc,i,GWS_ag):
    for c in range(0,crop-2):
        IWR_ag[c][:][:,i]=ETp_ag[c][:][:,i]-ETa_ag[c][:][:,i]
        ##sum of ID across all crops
    #global ETp_year, ETa_year, IWR_year
    IWR_ag_acc[:,i] = np.transpose(np.sum(IWR_ag[:,:,i],axis = 0))
    IWR_ag_acc[:,i]=np.where((IWR_ag_acc[:,i] <= GWS_ag[:,i-1]), IWR_ag_acc[:,i], IWR_ag_acc[:,i])
    IWR_ag_acc[:,i]=np.where(GWS_ag[:,i-1]>0, np.where((IWR_ag_acc[:,i] <= GWS_ag[:,i-1]), IWR_ag_acc[:,i], GWS_ag[:,i-1]),0)
    return IWR_ag, IWR_ag_acc