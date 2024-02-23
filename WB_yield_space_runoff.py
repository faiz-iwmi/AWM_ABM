
## -*- coding: utf-8 -*-

##function withtout aquacrop
"""
Created on Mon Nov 16 21:21:18 2015

@author: Nadezhda
"""

from datetime import datetime
from space_time_fn import *
from runoff_m import *
#import importlib
#importlib.reload(sys.modules['settings'])
from settings import *
from numpy import nan
from crop_selection import *
from runoff_m import *
#from crop_module import *
from crop_module_agent import *
from Agg_Disagg import *
from check_dams import *
#import time
from cal_para import *
from spatial_data import *
#from spatial_data2 import *
#from memory_profiler import profile
import variables

#@profile
def WB_Yield(precip1, t_mean1,p,t_mean,day,day_end,t, excel_flag, yr1,f,wheatarea):
    
    delta,spatial['RootField'],spatial['RootWilt'], spatial['RootSat'],spatial['RootKsat'],spatial['RootDrainVel'],spatial['RootTT'],spatial['SubField'],spatial['SubWilt'],spatial['SubSat'],spatial['SubKsat'],spatial['SubTT'], spatial['CapRiseMax'] ,RF,spatial['aqdepth'],spatial['YieldGw'],spatial['GwSat'],spatial['deltaGw'] ,spatial['BaseThresh'],spatial['alphaGw'] =cal_par(f)
    spatial['RootField'],spatial['RootWilt'], RF, RWP, Irr, GN_irr =cal_par2(f)
    j=0 ##setting yearly day counter
    aq_depth=spatial['aqdepth']
    #print(spatial['kx'])
    #irrigation = irr_cal(Irr, t, yr1,f)
    column_index = farm_irr.columns.get_loc(str(yr1[t]))
    irrigation = farm_irr.iloc[:,column_index]

    for i in range(day,day+day_end): 
        #t0 = time.time() 
        ##provide gwl to rabi
        ##plan date 150 to 160
        
        variables.crop_area_f,variables.crop_irr_f,variables.crop_rain_f, variables.ratio_cotton_wocd, variables.ratio_cotton_cd =crop_area(farmer_profile,variables.crop_area_f,variables.crop_irr_f, variables.crop_rain_f,t, crop, crop_var,j, i, variables.GWL_f,crop_ratio, yr1,aq_depth, irrigation,f,variables.ratio_cotton_wocd, variables.ratio_cotton_cd,wheatarea)
        if ((j == crop_var.iloc[10,0+1]) or (j == crop_var.iloc[10,1+1]) or (j == crop_var.iloc[10,2+1])): 
            variables.crop_area=crop_agg(variables.crop_area, variables.crop_area_f,grid_code,farmer_code,t,j, crop, crop_var)
            variables.irr_area=crop_agg(variables.irr_area, variables.crop_irr_f,grid_code,farmer_code,t,j, crop, crop_var)
            #print(np.average(variables.GWL_f[:,i-1]))
    #for i in range(day,day+len(precip1)):     
        #below line if input is excel
        if excel_flag == 1:
            precip = precip1.iloc[j,1]
        else:
            precip = p.isel(time=i)
            precip = precip['rain'].values.ravel()
            precip[np.isnan(precip)] = 0
            precip[precip == -99.9] = 0
         
        variables.rainfall[:,i]=precip
        #t_mean0 = t_mean1.isel(time=i)
        t_mean0 = t_mean.isel(time=i)
        t_mean2 = t_mean0["meant"]
        T=t_mean2.values.ravel()
        
        evap1=t_mean0["ET0"]
        evap1 = evap1.values.ravel()
        ##INTERCEPTION
        D=10.
        I = np.minimum(precip,D)
    
        ##(IN)FILTRATION 
        ##add runoff function here
        
        variables.RootWater[:,i]= variables.RootWater[:,i-1] + variables.rainfall[:,i] + variables.caprise[:,i-1]
        
        run = RootRunoff(precip,spatial['RootSat'],variables.RootWater[:,i])
        variables.runoff[:,i]=run
        
        ##capture runoff by storage interventions
        if inte==1:
            if yr1[t] >= 2002:
                variables.check_dam_s,variables.check_dam_c,variables.check_dam_r, variables.infil=check_dams(cd_loc, variables.runoff, variables.check_dam_s,variables.check_dam_c,variables.check_dam_r, i, evap1, variables.max_store,variables.cd_s_avail, variables.infil, variables.Hcd, delta,f)
     
        
        variables.runoff[:,i]=variables.runoff[:,i]-((variables.check_dam_c[:,i]*1000)/(100*10000))
        variables.RootWater[:,i]= variables.RootWater[:,i]-variables.runoff[:,i]
        
        variables.AET_SM,variables.return_flow_total_g = AET_fun(variables.RootWater,variables.Ks, variables.Kr,i,j, evap1,t, crop,f, yr1)
        ##may be here use of self comes into play
       
        variables.RootWater[:,i] = variables.RootWater[:,i] - variables.AET_SM[:,i]
        #lateran flow
        variables.rootdrain[:,i]= RootDrainage(variables.RootWater[:,i], variables.rootdrain[:,i-1], spatial['RootField'], spatial['RootSat'], spatial['RootDrainVel'], spatial['RootTT'])
        #variables.RootWater[:,i]=variables.RootWater[:,i]-variables.rootdrain[:,i]
        ##percolation
        variables.percloation[:,i]= RootPercolation(variables.RootWater[:,i], variables.SubWater[:,i-1], spatial['RootField'], spatial['RootTT'], spatial['SubSat'])
        
        #RootOut = variables.rootdrain[:,i] + variables.percloation[:,i]
        #-Calculate new values for drainage and percolation (to be used when RootOut > RootExcess)
        newdrain, newperc = CalcFrac(variables.RootWater[:,i], spatial['RootField'], variables.rootdrain[:,i], variables.percloation[:,i])
        #rootexcess = np.maximum(variables.RootWater[:,i] - b_constants['RootField'], 0)
        variables.rootdrain[:,i] =  newdrain
        variables.percloation[:,i] = newperc
        #-Update the RootWater content
        # Roottemp = self.RootWater
        
        ##update SM
        variables.RootWater[:,i] = variables.RootWater[:,i] -  variables.percloation[:,i] -variables.rootdrain[:,i]
        
        variables.SubWater[:,i] = variables.SubWater[:,i-1] + variables.percloation[:,i]
        #Capillary rise
        variables.caprise[:,i] = CapilRise(spatial['SubField'], variables.SubWater[:,i], spatial['CapRiseMax'], variables.RootWater[:,i], spatial['RootSat'], spatial['RootField'])
        ##SM2 layer
        #-Update sub soil water content
        variables.SubWater[:,i] = variables.SubWater[:,i] - variables.caprise[:,i]
        ##calculate sub-percolation
        variables.subpercolation[:,i] = SubPercolation(variables.SubWater[:,i], spatial['SubField'], spatial['SubTT'], variables.GWS[:,i-1], spatial['GwSat'])
        variables.SubWater[:,i] = variables.SubWater[:,i] - variables.subpercolation[:,i]
        variables.recharge[:,i]=GroundWaterRecharge(spatial['deltaGw'], variables.recharge[:,i-1], variables.subpercolation[:,i])
        
        variables.GWS[:,i] = variables.GWS[:,i-1] + variables.recharge[:,i]+((variables.check_dam_r[:,i]*1000)/(100*10000))
        
     
        
        variables.GWS[:,i] = variables.GWS[:,i] - variables.IWR_T_g_mm[:,i]  + variables.return_flow_total_g[:,i]
        #print(np.average(variables.GWS[:,i]), axis = 0)
        
        variables.baseflow[:,i]=BaseFlow(variables.GWS[:,i], variables.baseflow[:,i-1], variables.recharge[:,i], spatial['BaseThresh'], spatial['alphaGw'])
        #print(np.average(variables.baseflow[:,i]), axis = 0)
        
        variables.GWS[:,i] = variables.GWS[:,i] - variables.baseflow[:,i]
        ##giving to each agent
        #variables.GWS_f=disagg_n(variables.GWS,variables.GWS_f,grid_code,farmer_code,i)
        #variables.GWL[:,i]=HLevel(variables.GWL[:,i-1], b_constants['alphaGw'], variables.recharge[:,i], b_constants['YieldGw'])
        variables.GWL[:,i]=variables.GWS[:,i]/(1000*spatial['YieldGw'])

        if ((j >= 150) and (j <= 160)): ##any duration when rabi is sown
            variables.GWL_f=disagg_n(variables.GWL,variables.GWL_f,grid_code,farmer_code,i)
# =============================================================================
#             print('ok')
#             print(variables.GWL_f[12960,i])
# =============================================================================

        #GWL disaggregation 
        #variables.GWL_f=disagg_n(variables.GWL,variables.GWL_f,grid_code,farmer_code,i)
        ##multiply GWS and baser with (1-openwaterfract)

        ##total runoff
         
        variables.total_runoff[:,i] = variables.runoff[:,i] + variables.rootdrain[:,i] + variables.baseflow[:,i]
         
        ###
        cellArea=1000000
        flow_dir = pcr.lddcreate(dem3, 9999999,9999999,9999999,9999999)
       
        variables.routed_runoff[:,i]=ROUT(pcr, variables.total_runoff, variables.routed_runoff, flow_dir, spatial['kx'],i, cellArea,p)
                
        #water balance ##change is storage
        variables.dGWS[:,i]=variables.GWS[:,i]-variables.GWS[:,i-1]
        variables.dSubWater[:,i]=variables.SubWater[:,i]-variables.SubWater[:,i-1]
        variables.dRootWater[:,i]=variables.RootWater[:,i]-variables.RootWater[:,i-1]
        variables.ds[:,i]=variables.dGWS[:,i]+variables.dSubWater[:,i]+variables.dRootWater[:,i]
        
        variables.waterbalance[:,i]=variables.rainfall[:,i]-variables.AET_SM[:,i]- variables.IWR_T_g_mm[:,i] -variables.total_runoff[:,i] -variables.ds[:,i]
        variables.waterbalanceTot[:,i]=variables.waterbalanceTot[:,i-1]+variables.waterbalance[:,i]
    
        ##pcr raster operations
# =============================================================================
#         wb = flow_input(variables.waterbalance[:,i], p)
#         #locations = pcr.readmap(self.inpath + config.get('GENERAL','locations'))
#         wbalTSS= pcr.catchmenttotal(wb, flow_dir)/pcr.catchmenttotal(1., flow_dir)
#         store1=pcr.numpy_operations.pcr2numpy(wbalTSS, -9999)
#         store_np=store1.ravel()
#         variables.waterbalance_catch[:,i]=store_np
#         wb2 = flow_input(variables.waterbalanceTot[:,i], p)
#         wbalTotTSS = pcr.catchmenttotal(wb2, flow_dir)/pcr.catchmenttotal(1., flow_dir)
#         store1=pcr.numpy_operations.pcr2numpy(wbalTotTSS, -9999)
#         store_np=store1.ravel()
#         variables.waterbalanceTot_catch[:,i]=store_np
# =============================================================================
        #t1 = time.time()
        #print("time1",  t1-t0)      
        j=j+1 
        #print(j)
    return variables.runoff,variables.ETp, variables.ETa,variables.routed_runoff
