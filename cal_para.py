# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 22:35:44 2023

@author: faiza
"""

from settings import *
from spatial_data import *

def cal_par_f(f):
    f = caliberation.iloc[f,0]
    return f

def cal_par(f):
    D=10
    top = caliberation.iloc[f,1]
    bottom = caliberation.iloc[f,2]
    #f_soil_top=caliberation.iloc[f,1]
    #f_soil_bottom=caliberation.iloc[f,2]
    cap_ris_max=caliberation.iloc[f,3]
    aq_depth=caliberation.iloc[f,4]
    YieldGw=caliberation.iloc[f,5]
    aq_conduct=caliberation.iloc[f,6]
    deltaGw=caliberation.iloc[f,7]
    alphaGw=caliberation.iloc[f,8]
    BaseThresh=caliberation.iloc[f,9]
    kx=caliberation.iloc[f,10]
    RF=caliberation.iloc[f,11]
    f_soil_top1=caliberation.iloc[f,12]
    f_soil_top2=caliberation.iloc[f,13]
    f_soil_top3=caliberation.iloc[f,14]
    f_soil_top4=caliberation.iloc[f,15]
    f_soil_bottom1=caliberation.iloc[f,16]
    f_soil_bottom2=caliberation.iloc[f,17]
    f_soil_bottom3=caliberation.iloc[f,18]
    f_soil_bottom4=caliberation.iloc[f,19]
    #print(BaseThresh)
    #print("cal_para", top,bottom,cap_ris_max,aq_depth,YieldGw, aq_conduct,deltaGw,alphaGw,BaseThresh,kx,RF,f_soil_top1,f_soil_top2,f_soil_top3,f_soil_top4,f_soil_bottom1,f_soil_bottom2,f_soil_bottom3,f_soil_bottom4)

    ##retunf flow factor
    #RF=0.15

##adding slope  

    spatial['Slope'] = slope1['var'].values.ravel()
    delta=np.arctan(spatial['Slope']) ###slope of the area [radians]
 
    spatial['RootField'] = FC_top1['var'].values.ravel()*top*f_soil_top1
   
    spatial['RootWilt'] = WP_top1['var'].values.ravel()*top*f_soil_top2
  
    spatial['RootSat'] = SAT_top1['var'].values.ravel()*top*f_soil_top3

    ##in mm/day
    ##multiply by 24 as map in mm / hour
    spatial['RootKsat'] = Ksat_top1['var'].values.ravel() *24*f_soil_top4
    
    ##derived parameters
    spatial['RootDrainVel']= spatial['RootKsat']*spatial['Slope']
        
    spatial['RootTT']= np.maximum((spatial['RootSat']- spatial['RootField'])/spatial['RootKsat'], 0.0001)
    
    ##bottom layer paramters

    spatial['SubField'] = FC_bottom1['var'].values.ravel()*bottom*f_soil_bottom1

    
    spatial['SubWilt'] = WP_bottom1['var'].values.ravel()*bottom*f_soil_bottom2


    spatial['SubSat'] = SAT_bottom1['var'].values.ravel()*bottom*f_soil_bottom3

    spatial['SubKsat'] = Ksat_bottom1['var'].values.ravel()*24*f_soil_bottom4

    ##dervied paramters      
    spatial['SubTT']= np.maximum((spatial['SubSat']- spatial['SubField'])/spatial['SubKsat'], 0.0001)
        
    spatial['CapRiseMax']  = cap_ris_max
        
    # GROUNDWATER DEPTH (thickness of groundwater layer (mm)). Can be a map or single value.
    spatial['aqdepth']  = aq_depth
        
    # SPECIFIC AQUIFER YIELD (m/m). This is the specific yield of the groundwater storage and is used for
    # the groundwater table height calculation.
    spatial['YieldGw'] = YieldGw
    
    # SATURATED WATER CONTENT GROUNDWATER (saturated water content in groundwater zone (mm)). Can be
    # map or single value.
    spatial['GwSat'] = aq_depth*YieldGw*1000
    # GROUNDWATER RECHARGE DELAY TIME (delay in groundwater recharge (days)). Can be map or single value.
    spatial['deltaGw'] = deltaGw
        
    # BASEFLOW THRESHOLD (minimum value for baseflow to occur (mm)). Can be map or single value.
    spatial['BaseThresh'] = BaseThresh
    # BASEFLOW DAYS (parameter of baseflow days: alfaGw = 2.3/X (X = nr. of baseflow days). 
    # AlfaGw ranges between 0.1-1.0). Can be map or single value.
    spatial['alphaGw'] = alphaGw
    
    # RECESSION ROUTING COEF (recession coefficient of routing (-)). Can be map or single value.
    spatial['kx']	= kx
    
    return  delta, spatial['RootField'],spatial['RootWilt'], spatial['RootSat'],spatial['RootKsat'],spatial['RootDrainVel'],spatial['RootTT'],spatial['SubField'],spatial['SubWilt'],spatial['SubSat'],spatial['SubKsat'],spatial['SubTT'], spatial['CapRiseMax'] ,RF,spatial['aqdepth'],spatial['YieldGw'],spatial['GwSat'],spatial['deltaGw'] ,spatial['BaseThresh'],spatial['alphaGw']
            

        
def cal_par2(f):
    top = caliberation.iloc[f,1]
    bottom = caliberation.iloc[f,2]
    #f_soil_top=caliberation.iloc[f,1]
    f_soil_top1=caliberation.iloc[f,12]
    f_soil_top2=caliberation.iloc[f,13]
    #f_crop_k=caliberation.iloc[f,19]
    #f_crop_r=caliberation.iloc[f,20]
    #Ze=caliberation.iloc[f,21]
    #p_Ze=caliberation.iloc[f,22]
    RWP = caliberation.iloc[f,20]
    Irr = caliberation.iloc[f,21]
    

    ##retunf flow factor
    RF=caliberation.iloc[f,11]
##adding slope  

    spatial['RootField'] = FC_top1['var'].values.ravel()*top*f_soil_top1
   
    spatial['RootWilt'] = WP_top1['var'].values.ravel()*top*f_soil_top2
    
    GN_irr = caliberation.iloc[f,22]
    #print("cal_para2", f_soil_top1,f_soil_top2,RWP, Irr, RF, GN_irr)

  
   

    return spatial['RootField'],spatial['RootWilt'], RF, RWP, Irr, GN_irr

def cal_par3(f):
        # GROUNDWATER DEPTH (thickness of groundwater layer (mm)). Can be a map or single value.
    spatial['aqdepth']  = aq_depth
   

    return spatial['RootField'],spatial['RootWilt'], RF
    
def cal_par4(f):
        # GROUNDWATER DEPTH (thickness of groundwater layer (mm)). Can be a map or single value.
    
    risk_drip  = caliberation.iloc[f,23]
    impact_drip  = caliberation.iloc[f,24]
    ability_drip  = caliberation.iloc[f,25]
    attitude_drip  = caliberation.iloc[f,26]
    norm_drip  = caliberation.iloc[f,27]
    intercept_drip = caliberation.iloc[f,28]
    
    ###bw
 
    ability_bw  = caliberation.iloc[f,29]
    attitude_bw  = caliberation.iloc[f,30]
    norm_bw  = caliberation.iloc[f,31]
    water_bw  = caliberation.iloc[f,32]
    area_bw  = caliberation.iloc[f,33]
    intercept_bw = caliberation.iloc[f,34]
    
    ##wheat
    intercept_wheat =caliberation.iloc[f,35]
    GWL_wheat = caliberation.iloc[f,36]
    
    ##cotton
      
    intercept_cotton =caliberation.iloc[f,37]
    year_cotton_b = caliberation.iloc[f,38]
    year_cotton_a =caliberation.iloc[f,39]
    training_per = caliberation.iloc[f,40]
    income_per = caliberation.iloc[f,41]
    threshold_drip = caliberation.iloc[f,42]
    threshold_bw = caliberation.iloc[f,43]
    livestock_bw=caliberation.iloc[f,45]
    plan_bw=caliberation.iloc[f,46]
    #print(livestock_bw)

    return risk_drip, impact_drip,ability_drip,attitude_drip, norm_drip,intercept_drip,ability_bw,attitude_bw,norm_bw,water_bw,area_bw,intercept_bw,intercept_wheat,GWL_wheat,intercept_cotton,year_cotton_b,year_cotton_a,training_per,income_per, threshold_drip, threshold_bw,livestock_bw,plan_bw

def cal_par5(f):
        # GROUNDWATER DEPTH (thickness of groundwater layer (mm)). Can be a map or single value.
    
    drip_turn  = caliberation.iloc[f,44]
    return drip_turn  