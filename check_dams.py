# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 11:59:11 2022

@author: faiza
"""

##process for check dams storage and infiltration
import pandas as pd
import numpy as np
from settings import *
#from spatial_data2 import *
import variables
from cal_para import *
from spatial_data import *

# =============================================================================
# def check_dams(cd_loc, runoff, check_dam_s,check_dam_c,check_dam_r, i, evap1, max_store,cd_s_avail ):
#     #max_store[:,i]=((cd_loc.storage)*1000)/(100*10000) 
#     max_store[:,i]=cd_loc.storage
#     ##divide by grid area to get m3 in mm
#     cd_s_avail[:,i]=max_store[:,i] - check_dam_s[:, i-1]
#     ##runoff in m3, mm to m3
#     runoff=(runoff[:,i]/1000)*100*10000
#     #update capture
#     check_dam_c[:,i]=np.where(max_store[:,i]>0, np.where(runoff >= 0, np.minimum(runoff,cd_s_avail[:,i]) , 0),0)
#     ##evaporation loss
#     evap_loss=(evap1/1000)*cd_loc.area
#     #update storage
#     check_dam_s[:,i] = check_dam_c[:,i]   + check_dam_s[:,i-1] - evap_loss
#     ##max reccharge, inf*Area
#     #infiltation = 5 mm/day
#     max_recharge= (5/1000)*cd_loc.area
#     ##get recharge
#     check_dam_r[:,i]=np.where(check_dam_s[:,i]>0, np.minimum(max_recharge,check_dam_s[:,i]) ,0)
#     #update storage
#     check_dam_s[:,i] = check_dam_s[:,i]  - check_dam_r[:,i]
#     
#     return check_dam_s,check_dam_c,check_dam_r
# =============================================================================

def check_dams(cd_loc, runoff,check_dam_s,check_dam_c,check_dam_r, i, evap1, max_store,cd_s_avail, infil, Hcd, delta,f):
    delta,spatial['RootField'],spatial['RootWilt'], spatial['RootSat'],spatial['RootKsat'],spatial['RootDrainVel'],spatial['RootTT'],spatial['SubField'],spatial['SubWilt'],spatial['SubSat'],spatial['SubKsat'],spatial['SubTT'], spatial['CapRiseMax'] ,RF,spatial['aqdepth'],spatial['YieldGw'],spatial['GwSat'],spatial['deltaGw'] ,spatial['BaseThresh'],spatial['alphaGw'] =cal_par(f)
    aq_depth = spatial['aqdepth']
    #max_store[:,i]=((cd_loc.storage)*1000)/(100*10000) 
    max_store[:,i]=cd_loc.storage
    ##divide by grid area to get m3 in mm
    cd_s_avail[:,i]=max_store[:,i] - check_dam_s[:, i-1]
    ##runoff in mM, mm to m3
    runoff=(runoff[:,i]/1000)*100*10000
    
    #update capture
    #update capture
    check_dam_c[:,i]=np.where(max_store[:,i]>0, np.where(runoff >= 0, np.minimum(runoff,cd_s_avail[:,i]) , 0),0)
    
    check_dam_s[:,i] = check_dam_c[:,i]   + check_dam_s[:,i-1]


    ##updated width and height based on the day
    Wcd = cd_loc.width ##with of the check dam
    Hcd[:,i] = np.where(cd_loc.check_dams == 1,np.sqrt((check_dam_s[:,i]*2*np.tan(delta))/(Wcd)),0) ##water level in cd
    Asurf = (Wcd*Hcd[:,i])/np.tan(delta)
    
   
    #update storage
    
    ##evaporation loss
    evap_loss=(evap1/1000)*Asurf
    ##storage
    check_dam_s[:,i] = np.where(check_dam_s[:,i] - evap_loss <= 0,0,check_dam_s[:,i] - evap_loss)

    if cond == 1:
         ##condition A
    #areas where the lower layer has a higher permeability than the upper one (KI ≪ KII),
    #assuming for analytical purposes an underlying layer of infinite permeability.   
        infil[:,i] = np.where(aq_depth - variables.GWL[:,i-1]<=1, 0, aq_conduct*np.pi*variables.GWL[:,i-1]/(Wcd*max(log(a*(aq_depth+Hcd[:,i])/(Wcd+2*Hcd[:,i]),1))))
        
    elif cond == 2:
            ##condition B
    #assumes an underlying impermeable layer and can be used to approximate an area 
    #where the lower layer has much lower permeability than the upper one (KI ≫KII).

            Ls = (Wcd+Hcd[:,i] + aq_depth)/2
       
            infil[:,i] =  np.where(aq_depth - variables.GWL[:,i-1]<=1, 0,(aq_conduct*2*variables.GWL[:,i-1]/Wcd)*((Hcd[:,i] + aq_depth - 0.5*variables.GWL[:,i-1])/(Ls - 0.25*(2*Wcd))))
    else: 
       ##condition C with silt
    #hannels with a thin soil cover of much lower hydraulic conductivity 
    #than the original soil (often referred to as a clogging laye

            infil[:,i] =  np.where(aq_depth - variables.GWL[:,i-1]<=1, 0,((Hcd[:,i]-P_cr)*Wcd+(Hcd[:,i]-2*P_cr)*(Hcd[:,i])/(Wcd*R_a)))
       
    
    check_dam_r[:,i]=np.where(check_dam_s[:,i]>0, np.minimum(check_dam_s[:,i], Asurf*infil[:,i]),0)
   
    #update storage
    check_dam_s[:,i] = check_dam_s[:,i]  - check_dam_r[:,i]
    
    return check_dam_s,check_dam_c,check_dam_r, infil