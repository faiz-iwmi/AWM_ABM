# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:56:07 2022

@author: faiza
"""
from settings import *
from space_time_fn import *
from cal_loop import *


min_lon, min_lat, max_lon, max_lat = shapefile_extent(mask_sh)
##creat a list for storing spatial data in array format
spatial = {}
##adding slope  
slope1= space(slope,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['Slope'] = slope1['var'].values.ravel()
# delta=np.arctan(spatial['Slope']) ###slope of the area [radians]
# del slope1
# =============================================================================

##check dams file
#spatial['Slope']*((math.pi)/180) #slope of the area [degrees]
##check dams file
##location of CD and area, and storage
cd_loc = pd.read_csv(check_dams_file)

##set pcr map optios
pcr.setclone(clone)
#a = pcr.cellarea()
#cellArea = pcr.cellvalue(pcr.cellarea(),1)[0]
cellArea=1000000 ##in m2 ##1 km2
dem3=pcr.readmap('D:/PhD_work/Code/input_data/dem/dem2.map')  
#pcr.matplotlib.plot(dem3, labels=None, title=None, filename=None)
flow_dir = pcr.lddcreate(dem3, 9999999,9999999,9999999,9999999)
##reading and adding soil data
# top layer paramteres

FC_top1= space(FC_top,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['RootField'] = FC_top1['var'].values.ravel()*top*f_soil_top
# print(f_soil_top)
# del FC_top1
# =============================================================================
    
WP_top1= space(WP_top,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['RootWilt'] = WP_top1['var'].values.ravel()*top*f_soil_top
# del WP_top1  
# 
# =============================================================================
SAT_top1= space(SAT_top,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['RootSat'] = SAT_top1['var'].values.ravel()*top*f_soil_top
# del SAT_top1
# =============================================================================

Ksat_top1= space(Ksat_top,min_lon,max_lon,min_lat,max_lat)
##in mm/day
##multiply by 24 as map in mm / hour
# =============================================================================
# spatial['RootKsat'] = Ksat_top1['var'].values.ravel() *24*f_soil_top
# del Ksat_top1
# =============================================================================

##derived parameters
# =============================================================================
# spatial['RootDrainVel']= spatial['RootKsat']*spatial['Slope']
#     
# spatial['RootTT']= np.maximum((spatial['RootSat']- spatial['RootField'])/spatial['RootKsat'], 0.0001)
# 
# =============================================================================

##bottom layer paramters
FC_bottom1= space(FC_bottom,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['SubField'] = FC_bottom1['var'].values.ravel()*f_soil_bottom
# del FC_bottom1
# 
# =============================================================================

WP_bottom1= space(WP_bottom ,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['SubSat'] = WP_bottom1['var'].values.ravel()*f_soil_bottom
# del WP_bottom1
# =============================================================================


SAT_bottom1= space(SAT_bottom,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['SubSat'] = SAT_bottom1['var'].values.ravel()*bottom*f_soil_bottom
# del SAT_bottom1
# 
# =============================================================================
   
Ksat_bottom1= space(Ksat_bottom,min_lon,max_lon,min_lat,max_lat)
# =============================================================================
# spatial['SubKsat'] = Ksat_bottom1['var'].values.ravel()  *24*f_soil_bottom
# del Ksat_bottom1  
# 
# =============================================================================
##dervied paramters      
# =============================================================================
# spatial['SubTT']= np.maximum((spatial['SubSat']- spatial['SubField'])/spatial['SubKsat'], 0.0001)
#     
# spatial['CapRiseMax']  = cap_ris_max
#     
# # GROUNDWATER DEPTH (thickness of groundwater layer (mm)). Can be a map or single value.
# spatial['aqdepth']  = aq_depth
#     
# # SPECIFIC AQUIFER YIELD (m/m). This is the specific yield of the groundwater storage and is used for
# # the groundwater table height calculation.
# spatial['YieldGw'] = YieldGw
# 
# # SATURATED WATER CONTENT GROUNDWATER (saturated water content in groundwater zone (mm)). Can be
# # map or single value.
# spatial['GwSat'] = aq_depth*YieldGw*1000
# # GROUNDWATER RECHARGE DELAY TIME (delay in groundwater recharge (days)). Can be map or single value.
# spatial['deltaGw'] = deltaGw
#     
# # BASEFLOW THRESHOLD (minimum value for baseflow to occur (mm)). Can be map or single value.
# spatial['BaseThresh'] = BaseThresh
# # BASEFLOW DAYS (parameter of baseflow days: alfaGw = 2.3/X (X = nr. of baseflow days). 
# # AlfaGw ranges between 0.1-1.0). Can be map or single value.
# spatial['alphaGw'] = alphaGw
# 
# # RECESSION ROUTING COEF (recession coefficient of routing (-)). Can be map or single value.
# spatial['kx']	= kx
# =============================================================================
