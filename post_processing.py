# -*- coding: utf-8 -*-
##process the results from the code
import variables
from matplotlib import pyplot as plt 
import numpy as np
import panda as pd

###output for excel

wheat_area = pd.DataFrame(variables.crop_area[2,:,:])
wheat_area.to_excel("D:/PhD_work/Code/output/wheat_area_3.xlsx")

cn_area = pd.DataFrame(variables.crop_area[0,:,:])
cn_area.to_excel("D:/PhD_work/Code/output/cotton_area_3.xlsx")

cn_areaf = pd.DataFrame(variables.crop_area_f[0,:,:])
cn_areaf.to_excel("D:/PhD_work/Code/output/cotton_area_0_f.xlsx")

gn_area = pd.DataFrame(variables.crop_area[1,:,:])
gn_area.to_excel("D:/PhD_work/Code/output/gn_area_3.xlsx")

wheat_area = pd.DataFrame(variables.crop_area_f[2,:,:])
wheat_area.to_excel("D:/PhD_work/Code/output/wheat_area_3_f.xlsx")

Production=pd.DataFrame(variables.Production[2,:,:])
Production.to_excel("D:/PhD_work/Code/output/Production_3.xlsx")

Sales=pd.DataFrame(variables.sales[2,:,:])
Sales.to_excel("D:/PhD_work/Code/output/sales_3.xlsx")

crop_cost=pd.DataFrame(variables.crop_cost[2,:,:])
crop_cost.to_excel("D:/PhD_work/Code/output/crop_cost_3.xlsx")

yield_c = pd.DataFrame(variables.Yield[0,:,:])
yield_c .to_excel("D:/PhD_work/Code/output/yield_c_3.xlsx")

yield_gn = pd.DataFrame(variables.Yield[1,:,:])
yield_gn .to_excel("D:/PhD_work/Code/output/yield_gn_3.xlsx")

yield_w = pd.DataFrame(variables.Yield[2,:,:])
yield_w .to_excel("D:/PhD_work/Code/output/yield_w_3.xlsx")

cap = pd.DataFrame(variables.Capital[:,:])
cap.to_excel("D:/PhD_work/Code/output/capital_0.xlsx")

drip_adopt = pd.DataFrame(variables.drip_adopt_f[:,:])
drip_adopt.to_excel("D:/PhD_work/Code/output/drip_ad_f_0.xlsx")

bw_adopt = pd.DataFrame(variables.bw_adopt_f[:,:])
bw_adopt.to_excel("D:/PhD_work/Code/output/bw_ad_f_0.xlsx")

##to excel

w_cd = np.array(farmer_profile.cd)
wo_cd = 1- np.array(farmer_profile.cd)
include_f = np.array(farmer_profile.include)[:, np.newaxis]
GWL = pd.DataFrame(variables.IWRmet_T_f_m3[:,:]*include_f).mul(w_cd, axis = 0)
GWL = np.sum(GWL, axis = 0)
df = pd.DataFrame({'GWL': GWL})
df.to_excel("D:/PhD_work/Code/output/Calibrated_values/Run3/GW_irr.xlsx")


##gw_2
GWL = pd.DataFrame(variables.IWRmet_c_f_m3[1,:,:]*include_f).mul(w_cd, axis = 0)
GWL = np.sum(GWL, axis = 0)
df = pd.DataFrame({'GWL': GWL})
GWL.to_excel("D:/PhD_work/Code/output/Calibrated_values/Run3/IWR_met_GN.xlsx")
GWL = GWL.T
date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
GWL['year'] = date.year
GWL['month']=date.month
GWL['day']=date.day
GWL = GWL.groupby(["year","month"]).mean().reset_index()
del GWL['year']
del GWL['month']
del GWL['day']
GWL= GWL.T
GWL.to_excel("D:/PhD_work/Code/output/Calibrated_values/Run3/GW_irr_2.xlsx")

###
w_cd = np.array(cd_loc.check_dams)
GWL = pd.DataFrame(variables.IWR_T_g_mm[:,:]*include).mul(w_cd, axis = 0)
GWL = np.sum(GWL, axis = 0)
df = pd.DataFrame({'GWL': GWL})
GWL.to_excel("D:/PhD_work/Code/output/Calibrated_values/Run1/IWR_g3.xlsx")
GWL = GWL.T
date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
GWL['year'] = date.year
GWL['month']=date.month
GWL['day']=date.day
GWL = GWL.groupby(["year","month"]).mean().reset_index()
del GWL['year']
del GWL['month']
del GWL['day']
GWL= GWL.T
GWL.to_excel("D:/PhD_work/Code/output/Calibrated_values/Run1/IWR_g.xlsx")

##check water balance components first to assess if model is leaking
##water balance
##rainfall = total_runoff + storage change (soil1, soil,2, GWS) + AET (sm, irrigaiton counted in GWS)
##multipley with include where we don't want cells with 0 farmers excluded
include = np.array(grid_code.include)[:, np.newaxis]
include_f = np.array(farmer_profile.include)[:, np.newaxis]
rainfall = pd.DataFrame(np.average(variables.rainfall[:,:]*include, axis=0))
rainfall.to_excel("D:/PhD_work/Code/output/Calibrated_values/rainfall_n.xlsx")

runoff = pd.DataFrame(np.average(variables.total_runoff[:,:]*include , axis=0))
AET= pd.DataFrame(np.average(variables.AET_SM[:,:]*include   , axis=0) )
storage1 = pd.DataFrame(np.average(variables.dGWS[:,:]*include   , axis=0))
storage2 = pd.DataFrame(np.average(variables.dSubWater[:,:]*include   , axis=0))
storage3 = pd.DataFrame(np.average(variables.dRootWater[:,:]*include   , axis=0))

##do average for all grids

date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)

data=pd.concat([rainfall, runoff, AET, storage1, storage2, storage3], axis = 1)
data.columns = ["rainfall", "runoff", "AET", "storage1", "storage2", "storage3"]
data['year'] = date.year
data['month']=date.month
data['day']=date.day
data.to_excel("D:/PhD_work/Code/output/waterbalance2.xlsx")
##summarise runoff, anda ll by year
##
waterbalance = data.groupby("year").sum()
waterbalance.to_excel("D:/PhD_work/Code/output/waterbalance.xlsx")

results=pd.DataFrame(results)
results.to_excel("D:/PhD_work/Code/output/gnarewa.xlsx")

##crop area and yield
include_f = np.array(farmer_profile.include)[:, np.newaxis]
cotton_area = pd.DataFrame(np.sum(variables.crop_area[0,:,:], axis=0))
cotton_area_irr = pd.DataFrame(np.sum(variables.irr_area[0,:,:], axis=0))

GN_area = pd.DataFrame(np.sum(variables.crop_area[1,:,:], axis=0))
GN_area_irr = pd.DataFrame(np.sum(variables.irr_area[1,:,:], axis=0))

Wheat_area = pd.DataFrame(np.sum(variables.crop_area[2,:,:], axis=0))
Wheat_area_irr = pd.DataFrame(np.sum(variables.irr_area[2,:,:], axis=0))

irr_yield_0 = pd.DataFrame(variables.Yield_irr[0,:,:]*include_f)
rain_yield_0 = pd.DataFrame(variables.Yield_rain[0,:,:]*include_f)
cotton_irr_yield=irr_yield_0.replace(0, np.nan).mean()
cotton_rain_yield = rain_yield_0.replace(0, np.nan).mean()


irr_yield_1 = pd.DataFrame(variables.Yield_irr[1,:,:]*include_f)
rain_yield_1 = pd.DataFrame(variables.Yield_rain[1,:,:]*include_f)
GN_irr_yield=irr_yield_1.replace(0, np.nan).mean()
GN_rain_yield = rain_yield_1.replace(0, np.nan).mean()


irr_yield_2 = pd.DataFrame(variables.Yield_irr[2,:,:]*include_f)
rain_yield_2 = pd.DataFrame(variables.Yield_rain[2,:,:]*include_f)
wheat_irr_yield=irr_yield_2.replace(0, np.nan).mean()
wheat_rain_yield = rain_yield_2.replace(0, np.nan).mean()

yield_c=pd.DataFrame(np.average(variables.Yield[0,:,:]*include_f, axis=0))
yield_gn=pd.DataFrame(np.average(variables.Yield[1,:,:]*include_f, axis=0))
yield_w=pd.DataFrame(np.average(variables.Yield[2,:,:]*include_f, axis=0))


data=pd.concat([cotton_area,cotton_area_irr, GN_area, GN_area_irr, Wheat_area, Wheat_area_irr, yield_c, cotton_irr_yield, cotton_rain_yield, yield_gn, GN_irr_yield, GN_rain_yield,yield_w, wheat_irr_yield,wheat_rain_yield], axis = 1)
data.columns = ["Cotton_a","Cotton_irra", "GN_a","GN_irra", "Wh_a", "Wh_irra","Yieldc", "Cotton_iy","Cotton_ry", "Yieldgn","GN_iY","GN_rY","Yieldw", "Wh_iY", "Wh_rY"]
data.to_excel("D:/PhD_work/Code/output/crop.xlsx")


include = np.array(grid_code.include)[:, np.newaxis]
rainfall = pd.DataFrame(variables.rainfall_year[:,:]*include)
rainfall = rainfall.replace(0, np.nan).mean()


ETp_f_1=pd.DataFrame(np.average(variables.ETp_f_1[1,:,:], axis=0))
ETp_f_2=pd.DataFrame(np.average(variables.ETp_f_2[1,:,:], axis=0))
ETp_f_3=pd.DataFrame(np.average(variables.ETp_f_3[1,:,:], axis=0))
ETp_f_4=pd.DataFrame(np.average(variables.ETp_f_4[1,:,:], axis=0))

ETa_f_1=pd.DataFrame(np.average(variables.ETa_f_1[1,:,:], axis=0))
ETa_f_2=pd.DataFrame(np.average(variables.ETa_f_2[1,:,:], axis=0))
ETa_f_3=pd.DataFrame(np.average(variables.ETa_f_3[1,:,:], axis=0))
ETa_f_4=pd.DataFrame(np.average(variables.ETa_f_4[1,:,:], axis=0))

yield_c=pd.DataFrame(np.average(variables.Yield[0,:,:]*include_f, axis=0))
yield_gn=pd.DataFrame(np.average(variables.Yield[1,:,:]*include_f, axis=0))
yield_w=pd.DataFrame(np.average(variables.Yield[2,:,:]*include_f, axis=0))

data=pd.concat([cotton_area,cotton_area_irr, GN_area, GN_area_irr, Wheat_area, Wheat_area_irr, yield_c, cotton_irr_yield, cotton_rain_yield, yield_gn, GN_irr_yield, GN_rain_yield,yield_w, wheat_irr_yield,wheat_rain_yield, rainfall, ETp_f_1, ETp_f_2, ETp_f_3, ETp_f_4, ETa_f_1, ETa_f_2, ETa_f_3, ETa_f_4], axis = 1)
data.columns = ["Cotton_a","Cotton_irra", "GN_a","GN_irra", "Wh_a", "Wh_irra","Yieldc", "Cotton_iy","Cotton_ry", "Yieldgn","GN_iY","GN_rY","Yieldw", "Wh_Y", "Wh_iY", "rainfall", "et1", "et2","et3","et4","ea1","ea1","ea3","ea4"]
data.to_excel("D:/PhD_work/Code/output/crop.xlsx")

##check why rainfed yield is zero
rainfall = pd.DataFrame(np.average(variables.rainfall[:,:]*include, axis=0))
rainfall.to_excel("D:/PhD_work/Code/output/rainfall.xlsx")

ETp_f_1=pd.DataFrame(variables.ETp_f_1[0,:,12:18])
ETp_f_1.to_excel("D:/PhD_work/Code/output/ETp_f_1.xlsx")

ETa_f_1=pd.DataFrame(variables.ETa_f_1[0,:,12:18])
ETa_f_1.to_excel("D:/PhD_work/Code/output/ETa_f_1.xlsx")

IWR=pd.DataFrame(variables.IWRmet_c_f_mm[0,:,:])
IWR.to_excel("D:/PhD_work/Code/output/IWR.xlsx")

yield_c=pd.DataFrame(variables.Yield[0,:,12:18])
yield_c.to_excel("D:/PhD_work/Code/output/yield_c.xlsx")


##ET, ETA, IWR and IWRmet
include = np.array(grid_code.include)[:, np.newaxis]
rainfall = pd.DataFrame(np.average(variables.rainfall[:,:]*include, axis=0))
AET= pd.DataFrame(np.average(variables.AET_SM[:,:]*include   , axis=0) )

ETP1 = pd.DataFrame(np.average(variables.ETp[0,:,:], axis=0))
ETP2 = pd.DataFrame(np.average(variables.ETp [1,:,:], axis=0))
ETP3= pd.DataFrame(np.average(variables.ETp[2,:,:], axis=0))


ETA1 = pd.DataFrame(np.average(variables.ETa[0,:,:], axis=0))
ETA2 = pd.DataFrame(np.average(variables.ETa[1,:,:], axis=0))
ETA3= pd.DataFrame(np.average(variables.ETa[2,:,:], axis=0))

IWR1 = pd.DataFrame(np.average(variables.IWR_c_f_mm[0,:,:], axis=0))
IWR2 = pd.DataFrame(np.average(variables.IWR_c_f_mm[1,:,:], axis=0))
IWR3= pd.DataFrame(np.average(variables.IWR_c_f_mm[2,:,:], axis=0))


IWRm1 = pd.DataFrame(np.average(variables.IWRmet_c_f_mm[0,:,:], axis=0))
IWRm2 = pd.DataFrame(np.average(variables.IWRmet_c_f_mm[1,:,:], axis=0))
IWRm3= pd.DataFrame(np.average(variables.IWRmet_c_f_mm[2,:,:], axis=0))

# =============================================================================
# IWR1_m = pd.DataFrame(np.average(variables.IWR_c_g_mm[0,:,:], axis=0))
# IWR2_m = pd.DataFrame(np.average(variables.IWR_c_g_mm[1,:,:], axis=0))
# IWR3_m = pd.DataFrame(np.average(variables.IWR_c_g_mm[2,:,:], axis=0))
# 
# =============================================================================

##do average for all grids

date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)

data=pd.concat([rainfall, AET, ETP1, ETP2, ETP3, ETA1, ETA2, ETA3, IWR1, IWR2,IWR3, IWRm1, IWRm2,IWRm3, Yield1, Yield2, Yield3], axis = 1)
data.columns = ["rainfall", "AET", "ETP1", "ETP2", "ETP3", "ETA1","ETA2","ETA3","IWR1","IWR2","IWR3", "IWRm1","IWRm2","IWRm3", "Yield1", "Yield2", "Yield3"]
data['year'] = date.year
data['month']=date.month
data['day']=date.day

data = data.groupby("year").sum()
data.to_excel("D:/PhD_work/Code/output/crop_water.xlsx")

##
Y=pd.DataFrame((variables.Yield[1,:,:]))
##aggregate for grids
#Y=farmer_code.groupby('grid_id').mean()*include
Y.to_excel("D:/PhD_work/Code/output/gn_yield.xlsx")

##get ks and all
rainfall = pd.DataFrame(np.average(variables.rainfall[:,:]*include, axis=0))
ks = pd.DataFrame(np.average(variables.Ks[:,:]*include, axis=0))
RW = pd.DataFrame(np.average(variables.RootWater[:,:]*include, axis=0))
#De = pd.DataFrame(np.average(spatial['RootField']*include)-RW)
ETP1 = pd.DataFrame(np.average(variables.ETp[0,:,:], axis=0))
ETP2 = pd.DataFrame(np.average(variables.ETp[1,:,:], axis=0))
ETP3= pd.DataFrame(np.average(variables.ETp[2,:,:], axis=0))


ETA1 = pd.DataFrame(np.average(variables.ETa[0,:,:], axis=0))
ETA2 = pd.DataFrame(np.average(variables.ETa[1,:,:], axis=0))
ETA3= pd.DataFrame(np.average(variables.ETa[2,:,:], axis=0))

IWR1 = pd.DataFrame(np.average(variables.IWR_c_g_mm[0,:,:], axis=0))
IWR2 = pd.DataFrame(np.average(variables.IWR_c_g_mm[1,:,:], axis=0))
IWR3= pd.DataFrame(np.average(variables.IWR_c_g_mm[2,:,:], axis=0))


date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)

data=pd.concat([rainfall, ks, RW,  ETP1, ETP2, ETP3, ETA1, ETA2, ETA3, IWR1, IWR2,IWR3], axis = 1)
data.columns = ["rainfall", "ks", "RW", "ETP1", "ETP2", "ETP3", "ETA1","ETA2","ETA3","IWR1","IWR2","IWR3"]
data['year'] = date.year
data['month']=date.month
data['day']=date.day

#data = data.groupby("year").sum()
data.to_excel("D:/PhD_work/Code/output/Soil_water.xlsx")

##for one grid
rainfall = pd.DataFrame(variables.rainfall[500,:])
runoff = pd.DataFrame(variables.runoff[500,:])
ks = pd.DataFrame(variables.Ks[500,:])
RW = pd.DataFrame(variables.RootWater[500,:])
#De = pd.DataFrame(spatial['RootField'][500]-RW)
ETP1 = pd.DataFrame(variables.ETp[0,500,:])
ETP2 = pd.DataFrame(variables.ETp [1,500,:])
ETP3= pd.DataFrame(variables.ETp [2,500,:])


ETA1 = pd.DataFrame(variables.ETa[0,500,:])
ETA2 = pd.DataFrame(variables.ETa[1,500,:])
ETA3= pd.DataFrame(variables.ETa[2,500,:])
ETA4= pd.DataFrame(variables.ETa[3,500,:])

crop1_area = pd.DataFrame(variables.crop_area_d[0,500,:])
crop2_area = pd.DataFrame(variables.crop_area_d[1,500,:])
crop3_area = pd.DataFrame(variables.crop_area_d[2,500,:])


rain = pd.DataFrame(variables.rainfall[500,:] )
caprise = pd.DataFrame(variables.caprise[500,:] )
runoff = pd.DataFrame(variables.runoff[500,:] )
percolation = pd.DataFrame(variables.percloation[500,:] )
AET = pd.DataFrame(variables.AET_SM[500,:] )
rootdrain = pd.DataFrame(variables.rootdrain[500,:] )
baseflow = pd.DataFrame(variables.baseflow[500,:] )
subwater = pd.DataFrame(variables.SubWater[500,:] )

IWR1 = pd.DataFrame(variables.IWR_c_g_mm[0,500,:])
IWR2 = pd.DataFrame(variables.IWR_c_g_mm[1,500,:])
IWR3= pd.DataFrame(variables.IWR_c_g_mm[2,500,:])

date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)

data=pd.concat([rainfall, ks, RW,  ETP1, ETP2, ETP3, ETA1, ETA2, ETA3,ETA4, crop1_area, crop2_area, crop3_area, rain, caprise, runoff, percolation, AET, rootdrain, baseflow, subwater, IWR1, IWR2,IWR3], axis = 1)
data.columns = ["rainfall", "ks", "RW",  "ETP1", "ETP2", "ETP3", "ETA1","ETA2","ETA3", "ETA4", "crop1_area", "crop2_area", "crop3_area", "rain", "caprise", "runoff", "percolation", "AET", "rootdrain", "baseflow", "subwater", "IWR1","IWR2","IWR3"]
data['year'] = date.year
data['month']=date.month
data['day']=date.day

#data = data.groupby("year").sum()
data.to_excel("D:/PhD_work/Code/output/Soil_water_500.xlsx")
##summarise runoff, anda ll by year
##

ETp_f = pd.DataFrame(non_adopters)
ETp_f.to_excel("D:/PhD_work/Code/output/non_adopters.xlsx")

##Other plots

plt.plot(np.average(variables.waterbalance[:,:], axis=0))
plt.plot(np.average(variables.waterbalanceTot[:,:], axis=0))

plt.plot(np.average(variables.rainfall[:,:], axis=0))
plt.plot(np.average(variables.runoff[:,:], axis=0))
plt.plot(np.average(variables.rootdrain[:,:], axis=0))
plt.plot(np.average(variables.baseflow[:,:], axis=0))
plt.plot(np.average(variables.baseflow[:,:]*include, axis=0))
plt.plot(np.average(variables.GWS[:,:], axis=0))
plt.plot(np.average(variables.GWS[:,:]*include, axis=0))
plt.plot(np.average(variables.IWR_c_g_mm[0,:,:], axis=0))
plt.plot(np.average(variables.IWR_c_f_mm[0,:,:], axis=0))


plt.plot(np.average(variables.RootWater[:,:], axis=0))
plt.plot(np.average(variables.SubWater[:,:], axis=0))
plt.plot(np.average(variables.percloation[:,:], axis=0))
plt.plot(np.average(variables.rootdrain[:,:], axis=0))
plt.plot(np.average(variables.caprise[:,:], axis=0))
plt.plot(np.average(variables.subpercolation[:,:], axis=0))
plt.plot(np.average(variables.recharge[:,:], axis=0))
plt.plot(np.average(variables.GWS[:,:], axis=0))
plt.plot(np.average(variables.GWL_f[:,:], axis=0))
plt.plot(np.average(variables.AET_SM[:,:], axis=0))
plt.plot(np.sum(variables.crop_area[2,:,:], axis=0))
plt.plot(np.average(variables.IWR_T_g_mm[:,:], axis=0))
plt.plot(np.average(variables.return_flow_total_g[:,:], axis=0))
##water blance check for a grid
plt.plot((variables.GWL[525,:]))
plt.plot((variables.GWL_f[12960,:]))

plt.plot((variables.baseflow[508,:]))

rainfall=pd.DataFrame(variables.rainfall[500,:])
runoff=pd.DataFrame(variables.runoff[500,:])
AET=pd.DataFrame(variables.AET_SM[500,:])
rootdrain=pd.DataFrame(variables.rootdrain[500,:])
percloation=pd.DataFrame(variables.percloation[500,:])
caprise=pd.DataFrame(variables.caprise[500,:])
RootWater=pd.DataFrame(variables.RootWater[500,:])
subpercolation=pd.DataFrame(variables.subpercolation[500,:])
recharge=pd.DataFrame(variables.recharge[500,:])
SubWater=pd.DataFrame(variables.SubWater[500,:])
GWS=pd.DataFrame(variables.GWS[500,:])
IWR_T_g_mm=pd.DataFrame(variables.IWR_T_g_mm[500,:])
return_flow_total_g=pd.DataFrame(variables.return_flow_total_g[500,:])
baseflow=pd.DataFrame(variables.baseflow[500,:])

date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
data=pd.concat([rainfall, runoff, AET, rootdrain, percloation, caprise,RootWater,subpercolation,recharge,SubWater,GWS,IWR_T_g_mm,return_flow_total_g,baseflow], axis = 1)
data.columns = ["rainfall", "runoff", "AET", "rootdrain", "percloation", "caprise","Rootwater" , "subpercolation", "recharge"
                ,"SubWater", "GWS", "IWR_T_g_mm", "return_flow_total_g", "baseflow"]

data.to_excel("D:/PhD_work/Code/output/waterbalance_500.xlsx")


##plot area taken by eafch farmers farmer on grid

plt.plot(np.average(variables.fallow_area[:,:], axis=0))
##crop area
plt.plot(np.sum(variables.crop_area[0,:,:], axis=0))
##irrigated area
plt.plot(np.sum(variables.irr_area[0,:,:], axis=0))

plt.plot(np.sum(variables.crop_area[1,:,:], axis=0))
##irrigated area
plt.plot(np.sum(variables.irr_area[1,:,:], axis=0))

plt.plot(np.sum(variables.crop_area_f[2,:,:], axis=0))
##irrigated area
plt.plot(np.sum(variables.irr_area[2,:,:], axis=0))


##average yield
plt.plot(np.average(variables.Yield[0,:,:], axis=0))
plt.plot(np.average(variables.Yield[1,:,:], axis=0))
plt.plot(np.average(variables.Yield[2,:,:], axis=0))

##irrigated yield ##multiply by farm_irr matrix
irr_matrix = farm_irr.iloc[:,8:28]
rain_matrix = 1 - irr_matrix 

##cd matrix

w_cd = np.array(farmer_profile.cd)
wo_cd = 1- np.array(farmer_profile.cd)
variable = variables.crop_area[2,:,:]
cd = pd.DataFrame(variable[:,:]*include).mul(w_cd, axis = 0)


w_cd = np.array(cd_loc.check_dams)
wo_cd = 1- np.array(cd_loc.check_dams)
#plt.plot(GWL_cd.replace(0, np.nan).mean(), color='blue')
#plt.plot(capital_wocd.replace(0, np.nan).sum(), color='green')

GWL_cd = pd.DataFrame(variables.GWL[:,:]*include).mul(w_cd, axis = 0)
GWL_cd = GWL_cd.replace(0, np.nan).mean()

date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
data1=pd.concat([GWL_cd], axis = 1)
data1.columns = ["GWL"]
data1['year'] = date.year
data1['month']=date.month
data1['day']=date.day
data1['GWL'] = data1['GWL'].astype(np.float64)
data1["GWL_bottom"] = data1.GWL
data1 = data1[data1["month"].isin([5,11])]
GWL_cd = data1.groupby(["year","month"]).mean().reset_index()
GWL_cd  = GWL_cd ["GWL_bottom"]
#GWL_cd.to_excel("D:/PhD_work/Code/output/GWL_cd_2.xlsx")



GWL_wocd = pd.DataFrame(variables.GWL[:,:]*include).mul(wo_cd, axis = 0)
GWL_wocd = GWL_wocd.replace(0, np.nan).mean()
date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
data2=pd.concat([GWL_wocd], axis = 1)
data2.columns = ["GWL"]
data2['year'] = date.year
data2['month']=date.month
data2['day']=date.day
data2['GWL'] = data2['GWL'].astype(np.float64)
data2["GWL_bottom"] = data2.GWL
data2 = data2[data2["month"].isin([5,11])]
GWL_wocd = data2.groupby(["year","month"]).mean().reset_index()
GWL_wocd = GWL_wocd ["GWL_bottom"]
#GWL_wocd.to_excel("D:/PhD_work/Code/output/GWL_wocd_2.xlsx")

fig, ax1 = plt.subplots()
ax1.set_xlabel('time (months)')
ax1.set_ylabel('GWL (mbgl)', color="black")
ax1.plot(GWL_cd, color="black", label ="GWL with CD (mbgl)")
ax1.plot(GWL_wocd, color="red", label ="GWL without CD (mbgl)")
ax1.tick_params(axis='y', labelcolor="black")
ax1.legend(loc = "upper right")
plt.show()



w_cd = np.array(farmer_profile.cd)
wo_cd = 1- np.array(farmer_profile.cd)
#irr_yield_0 = pd.DataFrame(variables.Yield[0,:,:]*irr_matrix)
irr_yield_0 = pd.DataFrame(variables.Yield[0,:,:]).mul(w_cd, axis = 0)
#rain_yield_0 = pd.DataFrame(variables.Yield[0,:,:]*rain_matrix)
rain_yield_0 = pd.DataFrame(variables.Yield[0,:,:]).mul(wo_cd, axis = 0)
plt.plot(irr_yield_0.replace(0, np.nan).mean(), color='blue')
plt.plot(rain_yield_0.replace(0, np.nan).mean(), color='green')

irr_yield_1 = pd.DataFrame(variables.Yield[1,:,:]*irr_matrix)
rain_yield_1 = pd.DataFrame(variables.Yield[1,:,:]*rain_matrix)
plt.plot(irr_yield_1.replace(0, np.nan).mean(), color='blue')
plt.plot(rain_yield_1.replace(0, np.nan).mean(), color='green')

irr_yield_2 = pd.DataFrame(variables.Yield[2,:,:]*irr_matrix)
rain_yield_2= pd.DataFrame(variables.Yield[2,:,:]*rain_matrix)
plt.plot(irr_yield_2.replace(0, np.nan).mean(), color='blue')
plt.plot(rain_yield_2.replace(0, np.nan).mean(), color='green')


capital_cd = pd.DataFrame(variables.Capital[:,:]).mul(w_cd, axis = 0)
capital_cd =capital_cd.replace(0, np.nan).sum()
capital_wocd = pd.DataFrame(variables.Capital[:,:]).mul(wo_cd, axis = 0)
capital_wocd=capital_wocd.replace(0, np.nan).sum()

plt.plot(capital_cd, color='blue')
plt.plot(capital_wocd, color='green')

drip_cd = pd.DataFrame(variables.drip_adopt_f[:,:]).mul(w_cd, axis = 0)
drip_cd =drip_cd.replace(0, np.nan).sum()
drip_wocd = pd.DataFrame(variables.drip_adopt_f[:,:]).mul(wo_cd, axis = 0)
drip_wocd=drip_wocd.replace(0, np.nan).sum()

fig, ax1 = plt.subplots()
ax1.set_xlabel('time (months)')
ax1.set_ylabel('Adopters', color="black")
ax1.plot(drip_cd, color="black", label ="drip_Adopt_with_Cd")
ax1.plot(drip_wocd, color="blue", label ="drip_Adopt_without_Cd")
ax1.tick_params(axis='y', labelcolor="black")
ax1.legend(loc = "upper right")
plt.show()

bw_cd = pd.DataFrame(variables.bw_adopt_f[:,:]).mul(w_cd, axis = 0)
bw_cd =bw_cd.replace(0, np.nan).sum()
bw_wocd = pd.DataFrame(variables.bw_adopt_f[:,:]).mul(wo_cd, axis = 0)
bw_wocd=bw_wocd.replace(0, np.nan).sum()

fig, ax1 = plt.subplots()
ax1.set_xlabel('time (months)')
ax1.set_ylabel('Adopters', color="black")
ax1.plot(bw_cd, color="black", label ="BW_Adopt_with_Cd")
ax1.plot(bw_wocd, color="blue", label ="BW_Adopt_without_Cd")
ax1.tick_params(axis='y', labelcolor="black")
ax1.legend(loc = "upper right")
plt.show()

##cd matrix
w_cd = np.array(cd_loc.check_dams)
wo_cd = 1- np.array(cd_loc.check_dams)
variable = variables.crop_area[2,:,:]
variable = variables.GWL[:,:]
include = np.array(grid_code.include)[:, np.newaxis]
GWL_cd = pd.DataFrame(variable*include).mul(w_cd, axis = 0)
GWL_cd = GWL_cd.replace(0, np.nan).mean()


#plt.plot(GWL_cd.replace(0, np.nan).mean(), color='blue')
#plt.plot(capital_wocd.replace(0, np.nan).sum(), color='green')


date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
data1=pd.concat([GWL_cd], axis = 1)
data1.columns = ["GWL"]
data1['year'] = date.year
data1['month']=date.month
data1['day']=date.day
data1['GWL'] = data1['GWL'].astype(np.float64)
data1["GWL_bottom"] = data1.GWL
data1 = data1[data1["month"].isin([5,11])]
GWL_cd = data1.groupby(["year","month"]).mean().reset_index()
GWL_cd  = GWL_cd ["GWL_bottom"]



GWL_wocd = pd.DataFrame(variable[:,:]*include).mul(wo_cd, axis = 0)
GWL_wocd = GWL_wocd.replace(0, np.nan).mean()
date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
data2=pd.concat([GWL_wocd], axis = 1)
data2.columns = ["GWL"]
data2['year'] = date.year
data2['month']=date.month
data2['day']=date.day
data2['GWL'] = data2['GWL'].astype(np.float64)
data2["GWL_bottom"] = data2.GWL
data2 = data2[data2["month"].isin([5,11])]
GWL_wocd = data2.groupby(["year","month"]).mean().reset_index()
GWL_wocd = GWL_wocd ["GWL_bottom"]


fig, ax1 = plt.subplots()
ax1.set_xlabel('time (years)')
ax1.set_ylabel('GWL (m)))', color="black")
ax1.plot(GWL_cd, color="blue", label ="With CD")
ax1.plot(GWL_wocd, color="red", label ="Without CD")
ax1.tick_params(axis='y', labelcolor="black")
ax1.legend(loc = "upper right")
plt.show()

##wheat

wheat_cd = pd.DataFrame(variables.crop_area[2,:,:]).mul(w_cd, axis = 0)
wheat_cd=wheat_cd.replace(0, np.nan).mean()
wheat_cd.to_excel("D:/PhD_work/Code/output/wheat_cd_bl_2.xlsx")


wheat_wocd = pd.DataFrame(variables.crop_area[2,:,:]).mul(wo_cd, axis = 0)
wheat_wocd=wheat_wocd.replace(0, np.nan).mean()
wheat_wocd.to_excel("D:/PhD_work/Code/output/wheat_wocd_bl_2.xlsx")




plt.plot(wheat_cd.replace(0, np.nan).mean(), color='blue')
plt.plot(wheat_wocd.replace(0, np.nan).mean(), color='green')


##crop cost, investment and expenditure
c_cost= np.average(variables.crop_cost[0,:,:], axis=0)
plt.plot(c_cost)
c_cost= np.average(variables.crop_cost[1,:,:], axis=0)
plt.plot(c_cost)
c_cost= np.average(variables.crop_cost[2,:,:], axis=0)
plt.plot(c_cost)

##capital
cap = pd.DataFrame(variables.Capital[:,:])
cap.to_excel("D:/PhD_work/Code/output/capital_1_1.xlsx")

cap = np.average(variables.Capital[:,:]*include_f, axis=0)
plt.plot(cap)

inc = np.average(variables.income[:,:]*include_f, axis=0)
plt.plot(inc)

exp= np.average(variables.total_cost[:,:]*include_f, axis=0)
plt.plot(exp)

inv= np.average(variables.investment[:,:]*include_f, axis=0)
plt.plot(inv)

plt.plot(np.average(variables.Capital[:,:], axis=0))
plt.plot(np.average(variables.income[:,:], axis=0))
plt.plot(np.average(variables.expenditure[:,:], axis=0))
plt.plot(np.average(variables.Profit[:,:], axis=0))
plt.plot(np.average(variables.sales[0,:,:], axis=0))
##adoption

plt.plot(np.average(variables.avg_yield[:,:], axis=0))
plt.plot(np.average(variables.rainfall_year[:,:], axis=0))
plt.plot(np.average(variables.risk[:,:], axis=0))
plt.plot(np.average(variables.impact[:,:], axis=0))

plt.plot(np.average(variables.percent_g[:,:], axis=0))
plt.plot(np.average(variables.percent_f[:,:], axis=0))


variables.avg_yield_g_ad[variables.avg_yield_g_ad == 0] = np.nan
plt.plot(np.nanmean(variables.avg_yield_g_ad[:,:], axis=0), color='green')

variables.avg_yield_g_nad[variables.avg_yield_g_nad == 0] = np.nan
plt.plot(np.nanmean(variables.avg_yield_g_nad[:,:], axis=0), color='black')

plt.plot(np.average(variables.benefit_g[:,:], axis=0))
plt.plot(np.average(variables.benefit_f[:,:], axis=0))
plt.plot(np.average(variables.training_f[:,:], axis=0))

plt.plot(np.average(variables.attitude[:,:], axis=0))
plt.plot(np.average(variables.Capital[:,:], axis=0))
plt.plot(np.average(variables.ability[:,:], axis=0))
plt.plot(np.average(variables.percent_b_f[:,:], axis=0))

plt.plot(np.average(variables.value[:,:], axis=0))
plt.plot(np.average(variables.prob[:,:], axis=0))
plt.plot(variables.prob[:,19])
plt.plot((np.average(variables.drip_adopt_f[:,:], axis=0)*47000))
plt.plot(np.sum(variables.drip_adopt_g[:,:], axis=0))

variables.avg_yield_g_ad_b[variables.avg_yield_g_ad_b == 0] = np.nan
plt.plot(np.nanmean(variables.avg_yield_g_ad_b[:,:], axis=0), color='green')

variables.avg_yield_g_nad_b[variables.avg_yield_g_nad_b == 0] = np.nan
plt.plot(np.nanmean(variables.avg_yield_g_nad_b[:,:], axis=0), color='black')

plt.plot(np.average(variables.ability[:,:], axis=0))
plt.plot(np.average(variables.benefit_g_b[:,:], axis=0))
plt.plot(np.average(variables.benefit_f_b[:,:], axis=0))
plt.plot(np.average(variables.training_f_b[:,:], axis=0))
plt.plot(np.average(variables.percent_b_f[:,:], axis=0))

plt.plot(np.average(variables.attitude_b[:,:], axis=0))
plt.plot(np.average(variables.value_b[:,:], axis=0))
plt.plot(np.average(variables.prob_b[:,:], axis=0))
plt.plot(variables.prob_b[:,19])
plt.plot((np.average(variables.bw_adopt_f[:,:], axis=0)*47000))
plt.plot(np.sum(variables.bw_abstraction[:,:], axis=0))

capture = pd.DataFrame(variables.drip_adopt_f[:,:])
capture.to_excel("D:/PhD_work/Code/output/drip_ad_f.xlsx")


###results stored daily, crop wise
#for all agents, in year t

##check dam results
##multipley with include where we don't want cells with 0 farmers excluded
include = np.array(cd_loc.check_dams)[:, np.newaxis]
capture = pd.DataFrame(np.sum(variables.check_dam_c[:,:]*include, axis=0))
recharge = pd.DataFrame(np.sum(variables.check_dam_r[:,:]*include , axis=0))
storage= pd.DataFrame(np.sum(variables.check_dam_s[:,:]*include   , axis=0) )
infil = pd.DataFrame(np.average(variables.infil[:,:]*include, axis=0))
Hcd = pd.DataFrame(np.average(variables.Hcd[:,:]*include , axis=0))
rainfall = pd.DataFrame(np.average(variables.rainfall[:,:]*include   , axis=0))

##do average for all grids

date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
data=pd.concat([capture, recharge , storage, infil, Hcd, rainfall], axis = 1)
data.columns = ["capture", "recharge", "storage","infil" , "Hcd" ,"rainfall"]
data['year'] = date.year
data['month']=date.month
data['day']=date.day

##summarise runoff, anda ll by year
##
waterbalance = data.groupby("year").sum()
rain = pd.DataFrame(np.average(variables.rainfall_year[:,:], axis=0))
waterbalance= pd.concat([waterbalance, rain])
waterbalance.to_excel("D:/PhD_work/Code/output/cd_results.xlsx")

#### Create 2 axis plots 
## For farmers
## Different farmers stratified by type
## Capital
## Capital=np.zeros((far_len,Tsimul))

capital = pd.DataFrame(variables.Capital[:,1:20])
result_ex = pd.DataFrame(capital)
result_ex.to_csv("D:/PhD_work/Code/output/capital_wcd.csv")

#now bind this with famers data/indicator you want
capital_cd = pd.DataFrame(variables.Capital[:,:]*irr_matrix).mul(w_cd, axis = 0)
#capital_cd =capital_cd.replace(0, np.nan).sum()
capital_wocd = pd.DataFrame(variables.Capital[:,:]*rain_matrix).mul(w_cd, axis = 0)
#capital_wocd=capital_wocd.replace(0, np.nan).sum()

#irr_yield_1 = pd.DataFrame(variables.Yield[1,:,:]*irr_matrix)
#rain_yield_1 = pd.DataFrame(variables.Yield[1,:,:]*rain_matrix)

capital= capital_cd.join(farmer_profile.type)
result = capital.groupby("type").sum()

result_wocd=capital_wocd.join(farmer_profile.type)
result_wocd=result_wocd.groupby("type").sum()

##
years =   np.arange(1990, 2010, 1)
marginal = result.loc['Mr']
small = result.loc['Sm']
large = result.loc['Me']
marginal_wocd = result_wocd.loc['Mr']
small_wocd = result_wocd.loc['Sm']
large_wocd = result_wocd.loc['Me']
fig, ax1 = plt.subplots()
t = np.arange(1990, 2010, 1)

ax1.set_xlabel('time (years)')
ax1.set_ylabel('Capital (INR)', color="black")
ax1.plot(t, marginal, color="black", marker='o', label ="Marginal_wcd")
#ax1.plot(t, small, color="blue", marker='o', label ="Small")
ax1.plot(t, large, color="green", marker='o', label ="Medium_wcd")

ax1.plot(t, marginal_wocd, color="blue", marker='o', label ="Marginal_wocd")
#ax1.plot(t, small_wocd, color="blue", marker='o', label ="Small")
ax1.plot(t, large_wocd, color="red", marker='o', label ="Medium_wocd")

ax1.tick_params(axis='y', labelcolor="black")
ax1.legend(loc = "upper left")
plt.show()





##Yeild of crops
crop = 0 #0,1,2,3
#Yield=np.zeros((crop,far_len,Tsimul))
Y=pd.DataFrame(variables.Yield[crop,:,:])
#Y.to_csv("D:/PhD_work/Code/output/wheat_yield_wocd.csv")

#now bind this with famers data/indicator you want
Y= Y.join(farmer_profile.type)
result = Y.groupby("type").mean()

years =   np.arange(1990, 2010, 1)
small = result.loc['Sm']
large = result.loc['L']
plt.plot(years, small, 'b-', label='Small')
plt.plot(years, large, 'g-', label='Large')
plt.show()


##two axis plot of
## rainfed and irrigated crops
crop=1

irr_matrix = farm_irr.iloc[:,8:28]
rain_matrix = 1 - irr_matrix 

irr_yield_0 = pd.DataFrame(variables.Yield[crop,:,:]*irr_matrix)
rain_yield_0 = pd.DataFrame(variables.Yield[crop,:,:]*rain_matrix)

irr_avg = irr_yield_0.replace(0, np.nan).mean()
rain_avg = rain_yield_0.replace(0, np.nan).mean()



years =   np.arange(1990, 2009, 1)

rain = np.average(variables.rainfall_year[:,:], axis=0)


fig, ax1 = plt.subplots()
t = np.arange(1990, 2010, 1)
color = 'tab:red'
ax1.set_xlabel('time (years)')
ax1.set_ylabel('Yield', color=color)
ax1.plot(t, irr_avg, color="blue", marker='o', label ="Irrigated")
ax1.plot(t, rain_avg, color="green", marker='o', label ="rainfed")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('rain', color=color)  # we already handled the x-label with ax1
ax2.bar(t, rain, color=color, label ="rain", alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend(loc = "upper left")
ax2.legend(loc = "upper right")
plt.show()

##two axis plot of
##with and without drip
crop=0

ad_matrix = variables.drip_adopt_f[:,:]
nad_matrix = 1 - ad_matrix 

ad_yield_0 = pd.DataFrame(variables.Yield[crop,:,:]*ad_matrix)
nad_yield_0 = pd.DataFrame(variables.Yield[crop,:,:]*nad_matrix)

ad_avg = ad_yield_0.replace(0, np.nan).mean()
nad_avg = nad_yield_0.replace(0, np.nan).mean()

rain = np.average(variables.rainfall_year[:,:], axis=0)

fig, ax1 = plt.subplots()
t = np.arange(1990, 2010, 1)
color = 'tab:red'
ax1.set_xlabel('time (years)')
ax1.set_ylabel('Yield', color=color)
ax1.plot(t, ad_avg, color="blue", marker='o', label ="Drip")
ax1.plot(t, nad_avg , color="green", marker='o', label ="No Drip")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('rain', color=color)  # we already handled the x-label with ax1
ax2.bar(t, rain, color=color, label ="rain", alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend(loc = "upper left")
ax2.legend(loc = "upper right")
plt.show()

####two axis plot of
##with and without bw
crop=1

ad_matrix = variables.bw_adopt_f[:,:]
nad_matrix = 1 - ad_matrix 

ad_yield_0 = pd.DataFrame(variables.Yield[crop,:,:]*ad_matrix)
nad_yield_0 = pd.DataFrame(variables.Yield[crop,:,:]*nad_matrix)

ad_avg = ad_yield_0.replace(0, np.nan).mean()
nad_avg = nad_yield_0.replace(0, np.nan).mean()

rain = np.average(variables.rainfall_year[:,:], axis=0)

fig, ax1 = plt.subplots()
t = np.arange(1990, 2010, 1)
color = 'tab:red'
ax1.set_xlabel('time (years)')
ax1.set_ylabel('Yield', color=color)
ax1.plot(t, ad_avg, color="blue", marker='o', label ="Drip")
ax1.plot(t, nad_avg , color="green", marker='o', label ="No Drip")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('rain', color=color)  # we already handled the x-label with ax1
ax2.bar(t, rain, color=color, label ="rain", alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend(loc = "upper left")
ax2.legend(loc = "upper right")
plt.show()

##two axis plot of
##profit
##income
variable = pd.DataFrame(variables.Capital[:,:])

##yield
#crop=0
#variable = pd.DataFrame(variables.Yield[crop,:,:])
ad_matrix = pd.DataFrame(variables.drip_adopt_f[:,:])
nad_matrix = 1 - ad_matrix 

ad_yield_0 = variable*ad_matrix
ad_yield_0 =  pd.DataFrame(ad_yield_0.replace(0, np.nan))
ad_yield_0=ad_yield_0.join(farmer_profile.type)
ad_result = ad_yield_0.groupby("type").mean()

nad_yield_0 = variable*nad_matrix
nad_yield_0 =  pd.DataFrame(nad_yield_0.replace(0, np.nan))
nad_yield_0=nad_yield_0.join(farmer_profile.type)
nad_result = nad_yield_0.groupby("type").mean()


years =   np.arange(1990, 2010, 1)
small_ad = ad_result.loc['Sm']
small_nad = nad_result.loc['Sm']

large_ad = ad_result.loc['L']
large_nad = nad_result.loc['L']
#plt.plot(years, small_ad, 'b-', label='Small_ad')
#plt.plot(years, small_nad, 'g-', label='Small_nad')
#plt.plot(years, large_ad, 'r-', label='large_ad')
#plt.plot(years, large_nad, 'black', label='large_nad')
#plt.show()


rain = np.average(variables.rainfall_year[:,:], axis=0)

fig, ax1 = plt.subplots()
t = np.arange(1990, 2010, 1)
color = 'tab:red'
ax1.set_xlabel('time (years)')
ax1.set_ylabel('Yield', color=color)
ax1.plot(t, small_ad, color="blue", marker='o', label ="small_ad")
ax1.plot(t, small_nad , color="green", marker='o', label ="small_nad")

#ax1.plot(t, large_ad, color="blue", marker='o', label ="large_ad")
#ax1.plot(t, large_nad , color="green", marker='o', label ="large_nad")

ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('rain', color=color)  # we already handled the x-label with ax1
ax2.bar(t, rain, color=color, label ="rain", alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend(loc = "upper left")
ax2.legend(loc = "upper right")
plt.show()

##lets do spatial plot of maps
##this we do for a partuculare year
AET = pd.read_excel("D:/PhD_work/Code/output/Calibrated_values/Run1/AET_sm_n_1111.xlsx")
AET = AET.iloc[:,1:27]
new_columns = yr1[0:26]
AET.columns = new_columns
#AET = AET*include

for i in range(1, 26):
    Y = pd.DataFrame(AET.iloc[:,i])
    Y= np.asarray(Y)
    t = p
    t = t.isel(time=1)
    data1 = np.reshape(Y, (len(t.lat), len(t.lon)))
    t.rain.values = data1
    t.rain.plot()
    filename = f"D:/PhD_work/Code/output/Calibrated_values/Run1/AET/AET_{i}.tif"
    t = t.rename({'lat': 'y', 'lon': 'x'})
# Export the xarray dataset as a GeoTIFF raster
    t.rio.to_raster(filename)


#Y1=pd.DataFrame((variables.AET_year[:,:]))
#AET
#Y2=pd.DataFrame((variables.IWR_T_g_mm_year[:,:]))
#Y=Y1[12] + Y2[12]
Y= pd.DataFrame((variables.rainfall_year[:,:]))
Y= pd.DataFrame((variables.crop_area[0,:,:]))
Y=Y[5] 
Y= np.asarray(Y)


#area = grid_code.area
#Y = np.asarray(area)

cd_storage = cd_loc.storage
Y = np.asarray(cd_storage)
##aggregate for grids
#farmer_code.data_f=Y[12]
#Y=farmer_code.groupby('grid_id').mean()*include
#Y= np.asarray(Y.data_f)

t = p
plt.plot(Y)
data1 = np.reshape(Y, (len(t.lat), len(t.lon)))
##using exisitng xarary and adding results to that
t = t.isel(time=1)

#data1 = np.reshape(Y, (len(p.lon), len(p.lat)))  ##start_year and end year are in settings already.
##replacing rain values with Yeild value
t.rain.values = data1
t.rain.plot()

# Set the output file path
output_path = 'D:/PhD_work/Code/input_data/ET/cd_storage.tif'
t = t.rename({'lat': 'y', 'lon': 'x'})

# Export the xarray dataset as a GeoTIFF raster
t.rio.to_raster(output_path)

#https://stackoverflow.com/questions/52936720/python-xarray-tick-label-size-issue

##bar olots
from matplotlib import pyplot as plt 
x = np.arange(2000, 2017, 1)
y = np.arange(2000, 2017, 1)

x2 = variables.runoff_year[500,:]
y2 = variables.recharge_year[500,:]
plt.bar(x, x2, align = 'center') 
plt.bar(y, y2, color = 'g', align = 'center') 
plt.title('Bar graph') 
plt.ylabel('Y axis') 
plt.xlabel('X axis')  

plt.show()

##threee together
import matplotlib.pyplot as plt
from matplotlib import colors
fig = plt.figure(figsize=(6, 3.2))
ax = fig.add_subplot(111)
ax.plot(variables.IWR_total_mm[500,:], label='IWR')
ax.plot(variables.GWS[500,:], label='GWS')
ax.plot(variables.GWL[500,:], label='GWL')
ax.legend()

##bar plots
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
langs = [1,2,3,4,5,6,7]
students = variables.rainfall_year[500,:]
ax.bar(langs,students)
plt.show()


from matplotlib import pyplot as plt
import numpy as np

plt.figure()          
N = 17
rehcharge = variables.recharge_year[500,:]
runoff = variables.runoff_year[500,:]
#menStd = (2, 3, 4, 1, 2)
width = 0.35       # the width of the bars
rainfall = variables.rainfall_year[500,:]
#womenStd = (3, 5, 2, 3, 3)    
ind = np.arange(N)
plt.ylim(0.0, 2500)
plt.bar(ind, rainfall, width, color='r', label='rainfal')
#plt.bar(ind+width, runoff , width, color='y', label='runoff')
plt.bar(ind+1.2*width, rehcharge, width, color='b', label='rechagre')
plt.ylabel('Bar plot')      

x = np.linspace(0, N)
y = np.sin(x)
axes2 = plt.twinx()
axes2.plot(x, y, color='k', label='Sine')
axes2.set_ylim(-1, 1)
axes2.set_ylabel('Line plot')

plt.show()

##plot yield of all farmers on a grid
##for grids...

Y = pd.DataFrame((variables.rainfall_year[:,:]))
Y=Y[12]
Y= np.asarray(Y)

t = p
plt.plot(Y)

data1 = np.reshape(Y, (len(p.lat), len(p.lon)))
t = t.isel(time=1)
t.rain.values = data1
t.rain.plot()


##for farmers aggregated to grids
##aggregate for grids

#variables.Yield
Y=pd.DataFrame((variables.drip_adopt_f[:,:]))
farmer_code.data_f=Y[12]
Y=farmer_code.groupby('grid_id').sum()*include
Y= np.asarray(Y.data_f)
Y= np.asarray(cd_loc.storage)
t = p
plt.plot(Y)

data1 = np.reshape(Y, (len(t.lat), len(t.lon)))
t = t.isel(time=1)

#data1 = np.reshape(Y, (len(p.lon), len(p.lat)))  ##start_year and end year are in settings already.
##replacing rain values with Yeild value
t.rain.values = data1
t.rain.plot()

##plot where irrigation is

data = farm_irr.iloc[:,28]


farmer_code.data_f=data
Y=farmer_code.groupby('grid_id').sum()*include
Y= np.asarray(Y.data_f)

t = p
plt.plot(Y)

data1 = np.reshape(Y, (len(p.lat), len(p.lon)))
t = t.isel(time=1)

#data1 = np.reshape(Y, (len(p.lon), len(p.lat)))  ##start_year and end year are in settings already.
##replacing rain values with Yeild value
t.rain.values = data1
t.rain.plot()

import matplotlib.colors as colors
# Define the colormap
cmap = colors.ListedColormap(['blue', 'red'])
bounds = [0, 10, np.inf]

# Create the normalization object with vmin and vmax
norm = colors.BoundaryNorm(bounds, cmap.N, clip=True)

t['rain'].plot(cmap=cmap, norm=norm,cbar_kwargs={'label': 'Rainfall'})
plt.show()
# Get the minimum and maximum values
min_value = t['rain'].min()
max_value = t['rain'].max()

# Customize the legend
legend_text = f'Min: {0:.2f} Max: {30:.2f}'
plt.legend(title='Legend', labels=[legend_text])

# Show the plot
plt.show()







