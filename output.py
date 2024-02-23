# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 12:28:11 2023

@author: faiza
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 
from settings import *
import variables
from cal_loop import *


def output_csv(f1):
    ##runoff
    f= f1
    # runoff = pd.DataFrame(variables.routed_runoff[1542,:])
    # date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
    # data=pd.concat([runoff], axis = 1)
    # data.columns = ["runoff"]
    # data['year'] = date.year
    # data['month']=date.month
    # data['day']=date.day
    # data['runoff'] = data['runoff'].astype(np.float64)
    # data["mcm"] = (data.runoff*24*3600)/1000000
    # run_monthly = data.groupby(["year","month"]).sum().reset_index()
    
    # filename = f"D:/PhD_work/Code/output/Run1_2/Runoff/runoff_{f}.xlsx"
    # run_monthly.to_excel(filename)
    
    # run_monthly = run_monthly[run_monthly["year"] >=1993]
    # run_monthly = run_monthly[run_monthly["year"] <=2009]
    # data = pd.concat([run_monthly.year , run_monthly.month, run_monthly.mcm], axis = 1) 
    # data.to_csv("D:/PhD_work/Code/output/output_q.csv")
    
    
    # # ##groundwater
    # include = np.array(grid_code.include)[:, np.newaxis]
    # include_f = np.array(farmer_profile.include)[:, np.newaxis]
    
    # #w_cd = np.array(cd_loc.check_dams)
    
    # GWL = pd.DataFrame(variables.GWL[:,:]*include)
    # GWL = GWL.T
    # date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
    # GWL['year'] = date.year
    # GWL['month']=date.month
    # GWL['day']=date.day
    # GWL = GWL.groupby(["year","month"]).mean().reset_index()
    # del GWL['year']
    # del GWL['month']
    # del GWL['day']
    # GWL= GWL.T
    # filename = f"D:/PhD_work/Code/output/Run1_2/GWL/GWL_c_{f}.xlsx"
    # GWL.to_excel(filename)
    
    # GWL = pd.DataFrame(np.average(variables.GWL[:,:]*include, axis=0))
    
    
    
    # date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
    
    # data1=pd.concat([GWL], axis = 1)
    # data1.columns = ["GWL"]
    # data1['year'] = date.year
    # data1['month']=date.month
    # data1['day']=date.day
    # data1['GWL'] = data1['GWL'].astype(np.float64)
    
    # data1["GWL_bottom"] = aq_depth- (data1.GWL)
    # GWL_monthly = data1.groupby(["year","month"]).mean().reset_index()
    
    # filename = f"D:/PhD_work/Code/output/Run1_2/GWL/gwl_{f}.xlsx"
    # GWL_monthly.to_excel(filename)
    
    # GWL_monthly = GWL_monthly[GWL_monthly["year"] >=1993]
    # GWL_monthly = GWL_monthly[GWL_monthly["year"] <=2009]
    
    
    
    # # ##output csv
    # data = pd.concat([run_monthly.year , run_monthly.month, GWL_monthly.GWL_bottom], axis = 1) 
    # data.to_csv("D:/PhD_work/Code/output/output_gwl.csv")
    
    # # ##capital
    # cap = pd.DataFrame(variables.Capital[:,:])
    # filename = f"D:/PhD_work/Code/output/Run1_2/Capital/capital_{f}.xlsx"
    # cap.to_excel(filename)
    
    # # income = pd.DataFrame(variables.income[:,:])
    # # filename = f"D:/PhD_work/Code/output/Run_1/Capital/income_{f}.xlsx"
    # # income.to_excel(filename)
    
    # # expenditure = pd.DataFrame(variables.expenditure[:,:])
    # # filename = f"D:/PhD_work/Code/output/Run_1/Capital/expenditure_{f}.xlsx"
    # # expenditure.to_excel(filename)
    
    # Profit = pd.DataFrame(variables.Profit[:,:])
    # filename = f"D:/PhD_work/Code/output/Run1_2/Capital/Profit_{f}.xlsx"
    # Profit.to_excel(filename)
    
    # # # ##drip
    # drip_adopt = pd.DataFrame(variables.drip_adopt_f[:,:])
    # filename = f"D:/PhD_work/Code/output/Run1_2/Drip/drip_{f}.xlsx"
    # drip_adopt.to_excel(filename)
    
    # # ##bw
    # bw_adopt = pd.DataFrame(variables.bw_adopt_f[:,:])
    # filename = f"D:/PhD_work/Code/output/Run1_2/BW/bw_{f}.xlsx"
    # bw_adopt.to_excel(filename)
    
    # bw_value = pd.DataFrame(variables.value_b[:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/BW/bw_value_{f}.xlsx"
    # bw_value.to_excel(filename)
    
    # # ##cn area
    # cn_area = pd.DataFrame(variables.crop_area[0,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/Cotton_area/cotton_area_{f}.xlsx"
    # cn_area.to_excel(filename)
    
    # ##wheat area
    # wheat_area = pd.DataFrame(variables.crop_area[2,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/Wheat_area/wheat_area_{f}.xlsx"
    # wheat_area.to_excel(filename)
    
    # ##gn area
    # gn_area = pd.DataFrame(variables.crop_area[1,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/GN_area/gn_area_{f}.xlsx"
    # gn_area.to_excel(filename)

    # ##wheat area_f
    # wheat_area_f = pd.DataFrame(variables.crop_area_f[2,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_2/Wheat_area_f/wheat_area_f_{f}.xlsx"
    # wheat_area_f.to_excel(filename)
    
    # ##cotton area f
    # cn_area_f = pd.DataFrame(variables.crop_area_f[0,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/Cotton_area_f/cotton_area_f_{f}.xlsx"
    # cn_area_f.to_excel(filename)
    
    # include_f = np.array(farmer_profile.include)[:, np.newaxis]
    # cotton_area = pd.DataFrame(np.sum(variables.crop_area[0,:,:], axis=0))
    # cotton_area_irr = pd.DataFrame(np.sum(variables.irr_area[0,:,:], axis=0))
    
    # GN_area = pd.DataFrame(np.sum(variables.crop_area[1,:,:], axis=0))
    # GN_area_irr = pd.DataFrame(np.sum(variables.irr_area[1,:,:], axis=0))
    
    # Wheat_area = pd.DataFrame(np.sum(variables.crop_area[2,:,:], axis=0))
    # Wheat_area_irr = pd.DataFrame(np.sum(variables.irr_area[2,:,:], axis=0))
    
    # irr_yield_0 = pd.DataFrame(variables.Yield_irr[0,:,:]*include_f)
    # rain_yield_0 = pd.DataFrame(variables.Yield_rain[0,:,:]*include_f)
    # cotton_irr_yield=irr_yield_0.replace(0, np.nan).mean()
    # cotton_rain_yield = rain_yield_0.replace(0, np.nan).mean()
    
    
    # irr_yield_1 = pd.DataFrame(variables.Yield_irr[1,:,:]*include_f)
    # rain_yield_1 = pd.DataFrame(variables.Yield_rain[1,:,:]*include_f)
    # GN_irr_yield=irr_yield_1.replace(0, np.nan).mean()
    # GN_rain_yield = rain_yield_1.replace(0, np.nan).mean()
    
    
    # irr_yield_2 = pd.DataFrame(variables.Yield_irr[2,:,:]*include_f)
    # rain_yield_2 = pd.DataFrame(variables.Yield_rain[2,:,:]*include_f)
    # wheat_irr_yield=irr_yield_2.replace(0, np.nan).mean()
    # wheat_rain_yield = rain_yield_2.replace(0, np.nan).mean()
    
    # yield_c=pd.DataFrame(np.average(variables.Yield[0,:,:]*include_f, axis=0))
    # yield_gn=pd.DataFrame(np.average(variables.Yield[1,:,:]*include_f, axis=0))
    # yield_w=pd.DataFrame(np.average(variables.Yield[2,:,:]*include_f, axis=0))
    
    
    # data=pd.concat([cotton_area,cotton_area_irr, GN_area, GN_area_irr, Wheat_area, Wheat_area_irr, yield_c, cotton_irr_yield, cotton_rain_yield, yield_gn, GN_irr_yield, GN_rain_yield,yield_w, wheat_irr_yield,wheat_rain_yield], axis = 1)
    # data.columns = ["Cotton_a","Cotton_irra", "GN_a","GN_irra", "Wh_a", "Wh_irra","Yieldc", "Cotton_iy","Cotton_ry", "Yieldgn","GN_iY","GN_rY","Yieldw", "Wh_iY", "Wh_rY"]
    # filename = f"D:/PhD_work/Code/output/Run_1/Crop_yields/Crop_yields_{f}.xlsx"
    # data.to_excel(filename)
    
    # ##saveAET+IWRIWR_T_g_mm_year
    Y1=pd.DataFrame((variables.AET_year[:,:]))
    Y2=pd.DataFrame((variables.IWR_met_g_mm_year[:,:]))
    AET=Y1 + Y2
    filename = f"D:/PhD_work/Code/output/Calibrated_values/Run1/AET_sm_n_{f}.xlsx"
    AET.to_excel(filename)
    
    Y1=pd.DataFrame((variables.AET_year[:,:]))
    AET=Y1
    filename = f"D:/PhD_work/Code/output/Calibrated_values/Run1/AET_1.xlsx"
    AET.to_excel(filename)
    
    
    
    Y2=pd.DataFrame((variables.IWR_met_g_mm_year[:,:]))
    AET= Y2
    filename = f"D:/PhD_work/Code/output/Calibrated_values/Run1/IWR_1_{f}.xlsx"
    AET.to_excel(filename)
    # # #check dam results
    # #multipley with include where we don't want cells with 0 farmers excluded
    # include = np.array(cd_loc.check_dams)[:, np.newaxis]
    # capture = pd.DataFrame(np.sum(variables.check_dam_c[:,:]*include, axis=0))
    # recharge = pd.DataFrame(np.sum(variables.check_dam_r[:,:]*include , axis=0))
    # storage= pd.DataFrame(np.sum(variables.check_dam_s[:,:]*include   , axis=0) )
    # infil = pd.DataFrame(np.average(variables.infil[:,:]*include, axis=0))
    # Hcd = pd.DataFrame(np.average(variables.Hcd[:,:]*include , axis=0))
    # rainfall = pd.DataFrame(np.average(variables.rainfall[:,:]*include   , axis=0))
    
    # ##do average for all grids
    
    # date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
    # data=pd.concat([capture, recharge , storage, infil, Hcd, rainfall], axis = 1)
    # data.columns = ["capture", "recharge", "storage","infil" , "Hcd" ,"rainfall"]
    # data['year'] = date.year
    # data['month']=date.month
    # data['day']=date.day
    
    # ##summarise runoff, anda ll by year
    # ##
    # waterbalance = data.groupby("year").sum()
    # rain = pd.DataFrame(np.average(variables.rainfall_year[:,:], axis=0))
    # waterbalance= pd.concat([waterbalance, rain])
    # filename = f"D:/PhD_work/Code/output/Run_1/cd_results_{f}.xlsx"
    # waterbalance.to_excel(filename)
    
    # # ##all yields
    # yield_c=pd.DataFrame(variables.Yield[0,:,:]*include_f)
    # filename = f"D:/PhD_work/Code/output/Run_1/yield_tot_cotton_{f}.xlsx"
    # yield_c.to_excel(filename)
    # yield_gn=pd.DataFrame(variables.Yield[1,:,:]*include_f)
    # filename = f"D:/PhD_work/Code/output/Run_1/yield_tot_gn_{f}.xlsx"
    # yield_gn.to_excel(filename)
    # yield_w=pd.DataFrame(variables.Yield[2,:,:]*include_f)
    # filename = f"D:/PhD_work/Code/output/Run_1/yield_tot_wheat_{f}.xlsx"
    # yield_w.to_excel(filename)
        
    #  #   irrigation
    # w_cd = np.array(farmer_profile.cd)
    # Irr_m3 = pd.DataFrame(variables.IWRmet_T_f_m3[:,:]*include_f).mul(w_cd, axis = 0)
    # Irr_m3 = np.sum(Irr_m3, axis = 0)
    # df = pd.DataFrame({'Irr_m3': Irr_m3})
    # df.to_excel("D:/PhD_work/Code/output/Run1_2/Irrigation/Irr_m3.xlsx")
    # # #GWL = pd.DataFrame(np.average(variables.GWL[:,:]*include, axis=0))
    # # filename = f"D:/PhD_work/Code/output/Run_1/GW_irr_{f}.xlsx"
    # # Irr_m3.to_excel(filename)
    
    # Irr_m3_2 = pd.DataFrame(variables.IWRmet_T_f_m3_2[:,:]*include_f).mul(w_cd, axis = 0)
    # Irr_m3_2 = np.sum(Irr_m3_2, axis = 0)
    # df = pd.DataFrame({'Irr_m3_2': Irr_m3_2})
    # df.to_excel("D:/PhD_work/Code/output/Run1_2/Irrigation_2/Irr_m3_2.xlsx")
    
# =============================================================================
#     Irr_m3_g = pd.DataFrame(variables.IWR_c_f_m3[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/Irr_m3_g_{f}.xlsx"
#     Irr_m3_g.to_excel(filename)
#     
#     Irr_mm_f = pd.DataFrame(variables.IWR_c_f_mm[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/Irr_mm_f_{f}.xlsx"
#     Irr_mm_f.to_excel(filename)
#     
#     Irr_m3_met_g = pd.DataFrame(variables.IWRmet_c_f_m3[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/Irr_met_m3_{f}.xlsx"
#     Irr_m3_met_g.to_excel(filename)
#     
#     Irr_mm_met_f = pd.DataFrame(variables.IWRmet_c_f_mm[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/Irr_mm_met_f_{f}.xlsx"
#     Irr_mm_met_f.to_excel(filename)
#     
#     bw_m3_f = pd.DataFrame(variables.bw_abstraction[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/bw_m3_f_{f}.xlsx"
#     Irr_m3_g.to_excel(filename)
#     
#     frac_f = pd.DataFrame(variables.frac_f[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/frac_f_{f}.xlsx"
#     frac_f.to_excel(filename)
#     
#     Irr_mm_g = pd.DataFrame(variables.frac_f[0,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/frac_f_{f}.xlsx"
#     frac_f.to_excel(filename)
#     
# =============================================================================
    ##GN
    # Irr_mm_g = pd.DataFrame(variables.IWR_c_g_mm[1,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/Irr_mm_g_{f}.xlsx"
    # Irr_mm_g.to_excel(filename)
    
    # Irr_m3_met_g = pd.DataFrame(variables.IWRmet_T_f_m3_2[:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/Irr_met_m3_{f}.xlsx"
    # Irr_m3_met_g.to_excel(filename)
# =============================================================================
#     Irr_m3_g = pd.DataFrame(variables.IWR_c_f_m3[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/Irr_m3_g_{f}.xlsx"
#     Irr_m3_g.to_excel(filename)
#     
#     Irr_mm_f = pd.DataFrame(variables.IWR_c_f_mm[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/Irr_mm_f_{f}.xlsx"
#     Irr_mm_f.to_excel(filename)
#     
#     Irr_m3_met_g = pd.DataFrame(variables.IWRmet_c_f_m3[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/Irr_met_m3_{f}.xlsx"
#     Irr_m3_met_g.to_excel(filename)
#     
#     Irr_mm_met_f = pd.DataFrame(variables.IWRmet_c_f_mm[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/Irr_mm_met_f_{f}.xlsx"
#     Irr_mm_met_f.to_excel(filename)
#     
#     bw_m3_f = pd.DataFrame(variables.bw_abstraction[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/bw_m3_f_{f}.xlsx"
#     Irr_m3_g.to_excel(filename)
#     
#     frac_f = pd.DataFrame(variables.frac_f[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/frac_f_{f}.xlsx"
#     frac_f.to_excel(filename)
#     
#     Irr_mm_g = pd.DataFrame(variables.frac_f[1,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/GN_irrigation/frac_f_{f}.xlsx"
#     frac_f.to_excel(filename)
# =============================================================================
    
    ##wheat
    # Irr_mm_g = pd.DataFrame(variables.IWR_c_g_mm[2,:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/Irr_mm_g_{f}.xlsx"
    # Irr_mm_g.to_excel(filename)
    
    # Irr_m3_met_g = pd.DataFrame(variables.IWRmet_T_f_m3_2[:,:])
    # filename = f"D:/PhD_work/Code/output/Run_1/Cotton_irrigation/Irr_met_m3_{f}.xlsx"
    # Irr_m3_met_g.to_excel(filename)
    
# =============================================================================
#     Irr_m3_g = pd.DataFrame(variables.IWR_c_f_m3[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/Irr_m3_g_{f}.xlsx"
#     Irr_m3_g.to_excel(filename)
#     
#     Irr_mm_f = pd.DataFrame(variables.IWR_c_f_mm[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/Irr_mm_f_{f}.xlsx"
#     Irr_mm_f.to_excel(filename)
#     
#     Irr_m3_met_g = pd.DataFrame(variables.IWRmet_c_f_m3[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/Irr_met_m3_{f}.xlsx"
#     Irr_m3_met_g.to_excel(filename)
#     
#     Irr_mm_met_f = pd.DataFrame(variables.IWRmet_c_f_mm[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/Irr_mm_met_f_{f}.xlsx"
#     Irr_mm_met_f.to_excel(filename)
#     
#     bw_m3_f = pd.DataFrame(variables.bw_abstraction[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/bw_m3_f_{f}.xlsx"
#     Irr_m3_g.to_excel(filename)
#     
#     frac_f = pd.DataFrame(variables.frac_f[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/frac_f_{f}.xlsx"
#     frac_f.to_excel(filename)
#     
#     Irr_mm_g = pd.DataFrame(variables.frac_f[2,:,:])
#     filename = f"D:/PhD_work/Code/output/Run_1/Wheat_irrigation/frac_f_{f}.xlsx"
#     frac_f.to_excel(filename)
# =============================================================================

    
    
    
    
