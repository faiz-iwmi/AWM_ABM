# -*- coding: utf-8 -*-

#create all varibles on which data will be stored

import numpy as np
from crop_farmer_data import *
from settings import *

# =============================================================================
# global ETp,ETa,IWR,Ks, Kr, AET,runoff,total_runoff,rootdrain,percloation,RootWater,caprise,SubWater,subpercolation,recharge,baseflow,GWS,GWL
#     
# global crop_area,Yield,Yield_f,Production,crop_income,Total_income,crop_cost,Total_cost,expenditure,Total_expense,Capital,Profit
#    
# global rainfall_year,recharge_year,runoff_year,total_runoff_year ,rootdrain_year, percloation_year,baseflow_year,AET_year
#    
# =============================================================================

##water balance parameters
##stored daaily
rainfall = np.zeros((grid_len,days), dtype="float16")
runoff= np.zeros((grid_len,days), dtype="float32")
total_runoff=np.zeros((grid_len,days), dtype="float32")
routed_runoff=np.zeros((grid_len,days), dtype="float16")
rootdrain = np.zeros((grid_len,days), dtype="float16")
percloation = np.zeros((grid_len,days), dtype="float16")
RootWater = np.zeros((grid_len,days), dtype="float16")
# =============================================================================
# delta_RootWater = np.zeros((grid_len,Tsimul))
# =============================================================================
dRootWater = np.zeros((grid_len,days), dtype="float16")

caprise=np.zeros((grid_len,days), dtype="float16")

SubWater = np.zeros((grid_len,days), dtype="float16")
# =============================================================================
# delta_SubWater=np.zeros((grid_len,Tsimul))
# =============================================================================
dSubWater=np.zeros((grid_len,days), dtype="float16")

subpercolation = np.zeros((grid_len,days), dtype="float16")
recharge = np.zeros((grid_len,days), dtype="float16")
infil = np.zeros((grid_len,days), dtype="float16")
baseflow = np.zeros((grid_len,days), dtype="float16")
GWS=np.zeros((grid_len,days), dtype="float16")
# =============================================================================
# delta_GWS=np.zeros((grid_len,Tsimul))
# =============================================================================
dGWS=np.zeros((grid_len,days), dtype="float16")
GWL = np.zeros((grid_len,days), dtype="float16")

##soil stress paramtners
Ks = np.zeros((grid_len,days), dtype="float16")         #Soil moisture stress
Kr = np.zeros((grid_len,days), dtype="float32") 

##sumthings yearly

# =============================================================================
rainfall_year=np.zeros((grid_len,Tsimul))
# recharge_year = np.zeros((grid_len,Tsimul))
# runoff_year = np.zeros((grid_len,Tsimul))
# baseflow_year = np.zeros((grid_len,Tsimul))
# rootdrainage_year = np.zeros((grid_len,Tsimul))
# total_runoff_year = np.zeros((grid_len,Tsimul))
# rootdrain_year = np.zeros((grid_len,Tsimul))
# subpercolation_year = np.zeros((grid_len,Tsimul))
# percloation_year = np.zeros((grid_len,Tsimul))
# baseflow_year = np.zeros((grid_len,Tsimul))
# 
# =============================================================================

##crop parameters
#crop specific variables
ETp = np.zeros((crop,grid_len,days),dtype="float16")
ETa = np.zeros((crop,grid_len,days), dtype="float16")


##IWR
##IWR need of each crop for each grid
IWR_c_g_mm = np.zeros((crop,grid_len,days), dtype="float16")
##sum of each farmer for all crops for each grid
IWR_T_g_m3=np.zeros((grid_len,days), dtype="float32")

##IWR sum of all crops that is met for each grid that is met and is fed to water balance
IWR_T_g_mm=  np.zeros((grid_len,days), dtype="float16")
IWR_met_c_mm=  np.zeros((3,grid_len,days), dtype="float16")
IWR_met_g_mm=  np.zeros((grid_len,days), dtype="float16")
##sum at annual
# =============================================================================
IWR_T_g_mm_year=np.zeros((grid_len,Tsimul))
IWR_met_g_mm_year=np.zeros((grid_len,Tsimul))
# =============================================================================

return_flow_total_g=np.zeros((grid_len,days),dtype="float16")

##crop area
crop_area=np.zeros((crop,grid_len,Tsimul), dtype="float32")
irr_area=np.zeros((crop,grid_len,Tsimul), dtype="float32")
crop_area_d=np.zeros((crop,grid_len,days), dtype="float32")
crop_area_total=np.zeros((grid_len,days), dtype="float16")
crop_area_total_year=np.zeros((grid_len,Tsimul), dtype="float16")
fallow_area= np.zeros((grid_len,days),dtype="float16")

##AET crops
AET_SM = np.zeros((grid_len,days), dtype="float32")

##summed yearly
# =============================================================================
AET_year = np.zeros((grid_len,Tsimul))
# =============================================================================

##waterbalance

waterbalance=np.zeros((grid_len,days), dtype="float16")
waterbalanceTot=np.zeros((grid_len,days), dtype="float16")
ds=np.zeros((grid_len,days), dtype="float16")
# =============================================================================
# waterbalance_catch=np.zeros((grid_len,days), dtype="float16")
# waterbalanceTot_catch=np.zeros((grid_len,days), dtype="float16")
# =============================================================================


###variables for new code where agents are individuals
##farmers_data



crop_area_f=np.zeros((crop,far_len,Tsimul))
crop_irr_f=np.zeros((crop,far_len,Tsimul))
crop_rain_f=np.zeros((crop,far_len,Tsimul))
crop_area_f_d=np.zeros((3,far_len,days), dtype="float16")


##iwr need of each farmer for each crop
#in mm
IWR_c_f_mm=np.zeros((3,far_len,days), dtype="float16")
#in m3 for each farmer
IWR_c_f_m3=np.zeros((3,far_len,days), dtype="float32")

##met in m3
IWRmet_c_f_m3=np.zeros((3,far_len,days), dtype="float32")
##bw abstraction
bw_abstraction=np.zeros((3,far_len,days), dtype="float16")
##updated water met with bw asbtraction added
IWRmet_c_f_m3_2=np.zeros((3,far_len,days), dtype="float32")

##in m3 as sum of all crops
IWRmet_T_f_m3=np.zeros((far_len,days), dtype="float32")
IWRmet_T_f_m3_2=np.zeros((far_len,days), dtype="float32")

## in m3 that is met for all crops


##fraction
store_f=np.zeros((far_len,days), dtype="float32")
frac_f = np.zeros((3,far_len,days), dtype="float16")




##iwr that is met for each crop for each farmers
IWRmet_c_f_mm=np.zeros((3,far_len,days), dtype="float16")
IWRmet_c_f_mm_year=np.zeros((3,far_len,Tsimul), dtype="float16")

#return_flow=np.zeros((crop,far_len,days), dtype="float16")
store=np.zeros((grid_len,days), dtype="float32")
frac=np.zeros((grid_len,days), dtype="float16")
return_flow_total_f=np.zeros((far_len,days), dtype="float16")
GWS_f=np.zeros((far_len,days), dtype="float16")
GWL_f=np.zeros((far_len,days), dtype="float16")



##aggregating for season
ETp_f=np.zeros((3,far_len,Tsimul ), dtype="float16")
ETa_f=np.zeros((3,far_len, Tsimul), dtype="float16")

ETp_f_1=np.zeros((3,far_len,Tsimul ), dtype="float16")
ETa_f_1=np.zeros((3,far_len, Tsimul), dtype="float16")

ETp_f_2=np.zeros((3,far_len,Tsimul ), dtype="float16")
ETa_f_2=np.zeros((3,far_len, Tsimul), dtype="float16")

ETp_f_3=np.zeros((3,far_len,Tsimul ), dtype="float16")
ETa_f_3=np.zeros((3,far_len, Tsimul), dtype="float16")

ETp_f_4=np.zeros((3,far_len,Tsimul ), dtype="float16")
ETa_f_4=np.zeros((3,far_len, Tsimul), dtype="float16")

Yield=np.zeros((3,far_len,Tsimul))
Yield_irr=np.zeros((3,far_len,Tsimul))
Yield_rain=np.zeros((3,far_len,Tsimul))
avg_yield=np.zeros((far_len,Tsimul))
avg_yield_g_nad=np.zeros((grid_len,Tsimul))
avg_yield_g_ad=np.zeros((grid_len,Tsimul))

avg_yield_g_nad_b=np.zeros((grid_len,Tsimul))
avg_yield_g_ad_b=np.zeros((grid_len,Tsimul))

Production=np.zeros((3,far_len,Tsimul))
sales=np.zeros((3,far_len,Tsimul))
crop_cost= np.zeros((3,far_len,Tsimul))
investment=np.zeros((far_len,Tsimul))
debt=np.zeros((far_len,Tsimul))
expenditure=np.zeros((far_len,Tsimul))
total_cost=np.zeros((far_len,Tsimul))
income=np.zeros((far_len,Tsimul))
Capital=np.zeros((far_len,Tsimul))
Profit=np.zeros((far_len,Tsimul))


##check dam functions
##all in m3
#check dam storage
check_dam_s=np.zeros((grid_len,days), dtype="float32")
#check dam capture
check_dam_c=np.zeros((grid_len,days), dtype="float32")
#check dam recharge
check_dam_r=np.zeros((grid_len,days), dtype="float32")
max_store=np.zeros((grid_len,days), dtype="float32")
#check dam recharge
cd_s_avail=np.zeros((grid_len,days), dtype="float32")
##HcD
Hcd=np.zeros((grid_len,days), dtype="float32")
##infik
infil=np.zeros((grid_len,days), dtype="float32")

##adoption

drip_adopt_g=np.zeros((grid_len,Tsimul), dtype="float16")
drip_adopt_f=np.zeros((far_len,Tsimul), dtype="float16")
drought = np.zeros((grid_len,Tsimul), dtype="float16")
drought_f = np.zeros((far_len,Tsimul), dtype="float16")
exp=np.zeros((far_len,Tsimul), dtype="float16")
risk=np.zeros((far_len,Tsimul), dtype="float16")
impact=np.zeros((far_len,Tsimul), dtype="float16")
ability=np.zeros((far_len,Tsimul), dtype="float16")
norm=np.zeros((far_len,Tsimul), dtype="float16")
attitude=np.zeros((far_len,Tsimul), dtype="float16")
training_f=np.zeros((far_len,Tsimul), dtype="float16")
value=np.zeros((far_len,Tsimul), dtype="float16")
prob=np.zeros((far_len,Tsimul), dtype="float16")
percent_g=np.zeros((grid_len,Tsimul), dtype="float16")
percent_f=np.zeros((far_len,Tsimul), dtype="float16")
benefit_g=np.zeros((grid_len,Tsimul), dtype="float16")
benefit_f=np.zeros((far_len,Tsimul), dtype="float16")


#bw
##adoption

bw_adopt_g=np.zeros((grid_len,Tsimul), dtype="float16")
bw_adopt_f=np.zeros((far_len,Tsimul), dtype="float16")
attitude_b=np.zeros((far_len,Tsimul), dtype="float16")
training_f_b=np.zeros((far_len,Tsimul), dtype="float16")
value_b=np.zeros((far_len,Tsimul), dtype="float16")
prob_b=np.zeros((far_len,Tsimul), dtype="float16")
percent_b_g=np.zeros((grid_len,Tsimul), dtype="float16")
percent_b_f=np.zeros((far_len,Tsimul), dtype="float16")
benefit_g_b=np.zeros((grid_len,Tsimul), dtype="float16")
benefit_f_b=np.zeros((far_len,Tsimul), dtype="float16")

##caliberation
cal=np.zeros((200,5), dtype="float16")

##ctoon
ratio_cotton_wocd = np.zeros(Tsimul, dtype="float16")
ratio_cotton_cd = np.zeros(Tsimul, dtype="float16")