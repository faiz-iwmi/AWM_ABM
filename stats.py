# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 11:29:05 2023

@author: faiza
"""

##check simulated vs observed

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 
from settings import *
import variables
from cal_loop import *


##for runoff
def cal_runoff(f):
    
    runoff = pd.DataFrame(variables.routed_runoff[1542,:])
    
    date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
    
    data=pd.concat([runoff], axis = 1)
    data.columns = ["runoff"]
    data['year'] = date.year
    data['month']=date.month
    data['day']=date.day
    data['runoff'] = data['runoff'].astype(np.float64)
    
    data["mcm"] = (data.runoff*24*3600)/1000000
    #data["mcm"] = np.where(data["mcm"]<2,0, data["mcm"]- 2)
    
    #data.to_excel("D:/PhD_work/Code/output/runoff_d.xlsx")
    
    run_monthly = data.groupby(["year","month"]).sum().reset_index()
    
    #run_monthly.to_excel("D:/PhD_work/Code/output/runoff_m.xlsx")
    
    run_monthly = run_monthly[run_monthly["month"].isin([6,7,8,9,10])]
    run_monthly.drop(run_monthly.tail(1).index,inplace=True)
    
    run_monthly = run_monthly[run_monthly["year"] >=1991]
    run_monthly = run_monthly[run_monthly["year"] <=2015]
    
    observed_runoff = pd.read_csv('D:/PhD_work/Code/output/monthly_runoff.csv')
    
    observed_runoff = observed_runoff[observed_runoff["Year"] >=1991]
    observed_runoff = observed_runoff[observed_runoff["Year"] <=2015]
    
    simulated = run_monthly["mcm"]
    simulated= np.float64(simulated)
    observed = observed_runoff["runoff(mcm)"]
    observed = np.float64(observed)
    
    
    fig, ax1 = plt.subplots()
    #color = 'tab:red'
    ax1.set_xlabel('time (months)')
    ax1.set_ylabel('MCM/month', color="black")
    ax1.plot(observed, color="black", label ="Observed monthly flow (MCM)")
    ax1.plot(simulated, color="green", label ="Simulated monthly flow (MCM)")
    ax1.tick_params(axis='y', labelcolor="black")
    ax1.legend(loc = "upper right")
    plt.show()
 

    #https://pypi.org/project/hydroeval/
    import hydroeval as he



    nse = he.evaluator(he.nse, simulated, observed)
    pbias=he.evaluator(he.pbias, simulated, observed)
    
    def nse(observed,simulated):
        return 1-(np.sum((observed-simulated)**2)/np.sum((observed-np.mean(simulated))**2))
    nse = nse(observed,simulated)
    print("nse-runoff",nse)
    # calculate manually
    #variables.cal[f,1]=nse
    d = observed - simulated
    mse_f = np.mean(d**2)
    mae_f = np.mean(abs(d))
    rmse_f = np.sqrt(mse_f)
    r2_f = 1-(sum(d**2)/sum((observed-np.mean(observed))**2))
    
    #print("Results by manual calculation:")
    #print("MAE:",mae_f)
    #print("MSE:", mse_f)
    #print("RMSE:", rmse_f)
    print("R-Squared:runoff", r2_f)
    #variables.cal[f,2]=r2_f
    print(pbias)


##for GWL
def GWL_cal(f):
    #aq_depth=caliberation.iloc[f,4]
    include = np.array(grid_code.include)[:, np.newaxis]
    GWL = pd.DataFrame(np.average(variables.GWL[:,:]*include, axis=0))
    
    date = pd.date_range(start ='15-06-1990', periods = Tsimul *366)
    
    data1=pd.concat([GWL], axis = 1)
    data1.columns = ["GWL"]
    data1['year'] = date.year
    data1['month']=date.month
    data1['day']=date.day
    data1['GWL'] = data1['GWL'].astype(np.float64)
    
    data1["GWL_bottom"] = aq_depth- (data1.GWL)
    
    #data.to_excel("D:/PhD_work/Code/output/runoff_d.xlsx")
    
    ##select pre and post months
    data1 = data1[data1["month"].isin([5,11])]
    
    GWL_monthly = data1.groupby(["year","month"]).mean().reset_index()
    GWL_monthly.drop(GWL_monthly.head(1).index,inplace=True)
    GWL_monthly.drop(GWL_monthly.tail(1).index,inplace=True)
    
    GWL_monthly = GWL_monthly[GWL_monthly["year"] >=1992]
    GWL_monthly = GWL_monthly[GWL_monthly["year"] <=2015]
    
    
    #run_monthly.drop(run_monthly.tail(1).index,inplace=True)
    
    observed_GWL = pd.read_csv('D:/PhD_work/Code/output/GWL_observed.csv')
    
    observed_GWL = observed_GWL[observed_GWL["Year"] >=1992]
    observed_GWL = observed_GWL[observed_GWL["Year"] <=2015]
    
    simulated1 = GWL_monthly["GWL_bottom"]
    simulated1= np.float64(simulated1)
    observed1 = observed_GWL["GW level"]
    observed1 = np.float64(observed1)
    
    plt.plot(observed1,color='green')
    plt.plot(simulated1, color='black')
    
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('time (months)')
    ax1.set_ylabel('GWL (mbgl)', color="black")
    ax1.plot(observed1, color="black", label ="Observed GWL (mbgl)")
    ax1.plot(simulated1, color="red", label ="Simulated GWL (mbgl)")
    ax1.tick_params(axis='y', labelcolor="black")
    ax1.legend(loc = "upper right")
    plt.show()
 
    
    def nse(observed,simulated):
        return 1-(np.sum((observed-simulated)**2)/np.sum((observed-np.mean(simulated))**2))
    nse= nse(observed1,simulated1)
    # calculate manually
    print("nse-GWL",nse)
    #variables.cal[f,3]=nse
    d = observed1 - simulated1
    mse_f = np.mean(d**2)
    mae_f = np.mean(abs(d))
    rmse_f = np.sqrt(mse_f)
    r2_f = 1-(sum(d**2)/sum((observed1-np.mean(observed1))**2))
    
    #print("Results by manual calculation:")
    #print("MAE:",mae_f)
    #print("MSE:", mse_f)
    #print("RMSE:", rmse_f)
    print("R-Squared:GWL", r2_f)
    #variables.cal[f,4]=r2_f

##for yield
def Yield(f):
    
    cotton = pd.DataFrame(np.average(variables.Yield[0,:,:] , axis=0))
    gn = pd.DataFrame(np.average(variables.Yield[0,:,:],  axis=0))
    wheat = pd.DataFrame(np.average(variables.Yield[0,:,:], axis=0))
    
    date = np.arange(1990, 2010, 1)
    
    data1=pd.concat([cotton], axis = 1)
    data1.columns = ["cotton"]
    
    data1['gn'] = gn
    data1['wheat'] = wheat
    data1['year'] = date

  
    #data1 = data1[data1["year"] >=1993]
    #data1 = data1[data1["year"] <=2009]
    
    cotton_sim = data1["cotton"]
    gn_sim = data1["gn"]
    wheat_sim = data1["wheat"]
    
    
    observed_yield = pd.read_csv('D:/PhD_work/Code/input_data/crop/Crop_caliberation_data.csv')
    
    observed_yield = observed_yield[observed_yield["Year"] >=1990]
    observed_yield = observed_yield[observed_yield["Year"] <=2009]
    
    cotton_obs = np.float64(observed_yield["cotton"])
    gn_obs = np.float64(observed_yield["groundnut"])
    wheat_obs = np.float64(observed_yield["wheat"])
    
    #plt.plot(observed1,color='green')
    #plt.plot(simulated1, color='black')
    
    
    
    def nse(observed,simulated):
        return 1-(np.sum((observed-simulated)**2)/np.sum((observed-np.mean(simulated))**2))
    nse_cotton= nse(cotton_obs,cotton_sim)
    nse_gn= nse(gn_obs,gn_sim)
    nse_wheat= nse(wheat_obs,wheat_sim)
    
    # calculate manually
    print("nse-cotton",nse_cotton)
    print("nse_gn",nse_gn)
    print("nse_wheat",nse_wheat)
    
    d_cotton = cotton_obs - cotton_sim
    d_gn = gn_obs - gn_sim
    d_wheat = wheat_obs - wheat_sim
   
    r2_f_cotton = 1-(sum(d_cotton**2)/sum((cotton_obs-np.mean(cotton_obs))**2))
    r2_f_gn = 1-(sum(d_cotton**2)/sum((gn_obs-np.mean(gn_obs))**2))
    r2_f_wheat = 1-(sum(d_cotton**2)/sum((wheat_obs-np.mean(wheat_obs))**2))
    
 
    print("R-Squared:cotton", r2_f_cotton)
    print("R-Squared:gn", r2_f_gn)
    print("R-Squared:wheat", r2_f_wheat)
