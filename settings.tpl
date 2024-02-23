ptf @
# -*- coding: utf-8 -*-
##define common setting and paths to data bases
 
##xarray
 
#https://github.com/pydata/xarray/releases/tag/v0.17.0
 
# Import packages:
 
#from scipy import stats
#from scipy import interpolate
import os
import sys
##import django
import sys
##from django.db.models import Func, F, Min, Max
#from pathlib import Path
import json
import math
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import pcraster as pcr
from matplotlib import pyplot as plt
 
 
 
# =============================================================================
# from Simulator_updated import sociohydmodel
#
# =============================================================================
#sys.path.append('D:/Faiz/Code/sh_model')
 
## date range of precipitation dataset. data doesn't have date stamps so this
##date range is used in dataa_time function to give data stamps in datasets
startdate = "1983-01-01"
enddate = "2017-12-31"
 
##date range is used in dataa_time function to give data stamps in datasets
##for rain aguge
startdate_g = "1990-01-01"
enddate_g = "2010-12-31"
 
## date range of temperature dataset. data doesn't have date stamps so this
##date range is used in dataa_time function to give data stamps in datasets
startdate_t = "1980-01-01"
enddate_t = "2017-12-31"
 
##simulation period
##this date range for filtering simulation period
sim_start = "1990-06-15"
sim_end = "2010-06-14"
 
##simulation
start_year = 1990
end_year = 2010
Tsimul = end_year-start_year
 
#number of simulation days, year*366
days=Tsimul *366
 
 
##mask shapefile
mask_sh = "D:/PhD_work/Code/input_data/mask/kamadhiya1.shp"
 
##slope
slope='D:/PhD_work/Code/input_data/dem/slope_rsp.nc'
 
##pcr raster
clone = 'D:/PhD_work/Code/input_data/dem/dem2.map'
 
## resolution to work on##later when we write a module
#resol = 0.01 ## 1 degree  ~ 110 km grid
 
##use 1 if rainfall input is excel else 0
excel_flag=0
##excel_Rainfall
rainfall_e='D:/PhD_work/Code/input_data/climate/jasdan_imputed.csv'
 
##space-time variable
rain = 'D:/PhD_work/Code/input_data/climate/rstack.nc'
rain_g = "D:/PhD_work/Code/input_data/climate/rain_gauge_idw_f2.nc"
#rain_g = "D:/PhD_work/Code/input_data/climate/rain_gauge.nc"
meanT = 'D:/PhD_work/Code/input_data/climate/meant_stack.nc'
#need to repalce eith mint data
minT = 'D:/PhD_work/Code/input_data/climate/meant_stack.nc'
maxT = 'D:/PhD_work/Code/input_data/climate/maxt_stack.nc'
 
##soil parameters
##top layer
FC_top = 'D:/PhD_work/Code/input_data/soil/FC_top.nc'
WP_top = 'D:/PhD_work/Code/input_data/soil/WP_top.nc'
SAT_top = 'D:/PhD_work/Code/input_data/soil/SAT_top.nc'
Ksat_top = 'D:/PhD_work/Code/input_data/soil/Ksat_top.nc'
 
##bottom layer
FC_bottom = 'D:/PhD_work/Code/input_data/soil/FC_bottom.nc'
WP_bottom = 'D:/PhD_work/Code/input_data/soil/WP_bottom.nc'
SAT_bottom = 'D:/PhD_work/Code/input_data/soil/SAT_bottom.nc'
Ksat_bottom = 'D:/PhD_work/Code/input_data/soil/Ksat_bottom.nc'
 
##farmers_data
farmers_data = "D:/PhD_work/Code/input_data/farmer_data/lulc/farmer_data_n.csv"
farmer_irr = "D:/PhD_work/Code/input_data/farmer_data/lulc/farmer_irr_data.csv"
far_training = "D:/PhD_work/Code/input_data/farmer_data/lulc/training.csv"
##wheat_area = "D:/PhD_work/Code/input_data/crop/wheatarea.csv"



 
#A 5% depreciation rate of capital is assumed. (Pande and Savenije, 2016)
delt = 0.05
 
##initial captial of each farmer
##provided 0, else provide in farmers data
capital = 25000
 
#interest on debt
debt_interest = 0.1
 
##how much farmer sells of each crop, eiother constant or provide farmer list
selling_factor=1
##farmer code_grid
##gives farmer id agains grid id and lat and lon
farmers_code_grid = "D:/PhD_work/Code/input_data/farmer_data/lulc/farmer_code_n.csv"
 
##grid_Code
##give grid id against lat and lon
grid="D:/PhD_work/Code/input_data/farmer_data/grid_code.csv"
 
##interventions
inte =1##one if interventions need to be considered
##check dams file
check_dams_file = "D:/PhD_work/Code/input_data/interventions/check_dams.csv"
cd_loc = pd.read_csv(check_dams_file)
#specify which condition
##1=A, 2= B, 3=C
cond = 2
 
##human behaviour rules on or off
##on if human = 1
human = 1


##cropselection
##if 1 rule is in place, else no crop rule
cotton_s =1
wheat_s =1
##water
water = "D:/PhD_work/Code/input_data/water/water.csv"
water_loc = pd.read_csv(water)
 
# # Bouwer parameters
a=4.3 #confition A parameter
A= 3 #condition A' parameter
P_cr=-0.5 #critic pressure for bouwer[m]
R_a=150#impendence of the clogging layer [day]
 
##cost tecnlogioes
 
drip_cost = 60000 ##per ha
bw_cost = 70000
 
#file containg crop parameters
## number of crops including fallow area
crop = 5
kc='D:/PhD_work/Code/input_data/crop/kc.csv'
depth='D:/PhD_work/Code/input_data/crop/kc.csv'
cropvar='D:/PhD_work/Code/input_data/crop/crop_variables.csv'
#crop_area_ratio = 'D:/PhD_work/Code/input_data/crop/Crop_area_ration.csv'
crop_area_ratio = 'D:/PhD_work/Code/input_data/crop/Crop_area_ration2.csv'
##impact of fertlised on yield
fertilizer_factor=1
 
##caliberating file name
caliberation = 'D:/PhD_work/Code/input_data/caliberation_variables/variables.csv'
caliberation = pd.read_csv(caliberation)
 
 
    # caliberating paratmeters
#=============================================================================
D=10. # threshold for interception # 
# caliberating paratmeters
#depth in mm
top = 650
bottom = 400

##to change soil parameters##remove them may be and go with chnaginbg soil depth
#f_soil_top=1.5
#f_soil_bottom=1
##caprise max
cap_ris_max=@cap_ris @


##gwdepth in m
aq_depth = @aq_depth @
##yield gw (m/m)
YieldGw= @YieldGw @

##aquifer conductivtuy (m/d)
##http://www.aqtesolv.com/aquifer-tests/aquifer_properties.htm
aq_conduct = 0.35

# GROUNDWATER RECHARGE DELAY TIME (delay in groundwater recharge (days)). Can be map or single value.
deltaGw=0.664322

# BASEFLOW DAYS (parameter of baseflow days: alfaGw = 2.3/X (X = nr. of baseflow days). 
# AlfaGw ranges between 0.1-1.0). Can be map or single value.
alphaGw=0.528727

### BASEFLOW THRESHOLD (minimum value for baseflow to occur (mm)). Can be map or single value.
BaseThresh=@BaseThresh @

#RECESSION ROUTING COEF 
kx = @kx @
##claiberation variables
##multipely with crop area
##not being used when external value is given so keep 1
    ##
#f_crop = 1
#f_crop_k=0.8
#f_crop_r=1.5
##retunf flow factor
RF=@RF @

f=1
f_soil_top1=@top1 @
f_soil_top2=@top2 @
f_soil_top3=@top3 @
f_soil_top4=@top4 @
f_soil_bottom1=@bottom1 @
f_soil_bottom2=@bottom2 @
f_soil_bottom3=@bottom3 @
f_soil_bottom4=@bottom4 @

#Ze=0.4
#p_Ze=0.7

RWP = @RWP @
Irr =  1.398
GN_irr = @GN_irr@

risk_drip=-0.62
impact_drip=-0.42

ability_drip	=0.865

attitude_drip=0.56

norm_drip=0.46

intercept_drip=-3.04


ability_bw=0.07

attitude_bw=0.59
norm_bw=0.61
water_bw	=0.86
area_bw=0.02
intercept_bw=-2.19
intercept_wheat=0.276

GWL_wheat=-0.021

intercept_cotton=-26.151

year_cotton_b=0.0132

year_cotton_a=0.0175

training_per=0.5

income_per=0.7

threshold_drip=0.375

threshold_bw	=0.32

drip_turn=1

livestock_bw=0.08
plan_bw = 0.3865

#=============================================================================
