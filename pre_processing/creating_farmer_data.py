# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import xarray
import numpy

from settings import *
from data_module import *

##this code is to get grid id and lat and lon

##take rain data, read it

rain1 = space_time(rain,min_lon,max_lon,min_lat,max_lat,startdate, enddate, sim_start, sim_end)
p = rain1  ##start_year and end year are in settings already.
  
##this function makes lat and lon list with grid for a spatial data
def grid_lat_lon(data):
    variable = data.rain
    variable1d = variable.isel(time=1)
    da_stacked=variable1d.stack(dim=['lat', 'lon'])
    nona_coords = da_stacked.dim
    clt1=numpy.array(nona_coords)
    clt1 = pd.DataFrame(clt1)                                                                                                                                                      
    lat_lon_list = pd.DataFrame(clt1[0].tolist(), index=clt1.index)                                                                                                                                    
    return lat_lon_list

##apply function
lat_lon_list=grid_lat_lon(p)

##output to a csv file
##used as grid code file
lat_lon_list.to_csv("D:/PhD_work/Code/input_data/farmer_data/lat_lon_grid.csv")

##this grid file is used to assign farmer data
##check r code

##downlading in CSV the holdings under each grid
Mr_hold='D:/PhD_work/Code/input_data/farmer_data/census/Mr_hold_2011.nc'
Sm_hold='D:/PhD_work/Code/input_data/farmer_data/census/Sm_hold_2011.nc'
SMe_hold='D:/PhD_work/Code/input_data/farmer_data/census/SMe_hold_2011.nc'
Me_hold='D:/PhD_work/Code/input_data/farmer_data/census/Me_hold_2011.nc'
L_hold='D:/PhD_work/Code/input_data/farmer_data/census/L_hold_2011.nc'

##
water = 'D:/PhD_work/Code/input_data/lulc/lulc_resam2019_r.nc'
#water = 'D:/PhD_work/Code/input_data/interventions/checkdam_v3.nc'
data= space(water,min_lon,max_lon,min_lat,max_lat)
##for 1d data ##for farmer data
#variable = data['var']
variable = data['var']
da_stacked=variable.stack(dim=['lat', 'lon'])
nona_coords = da_stacked.dim
clt1=np.array(nona_coords)
clt1 = pd.DataFrame(clt1)                                                                                                                                                      
lat_lon_list = pd.DataFrame(clt1[0].tolist(), index=clt1.index)
values = pd.DataFrame(da_stacked.values.ravel())
df_c = pd.concat([lat_lon_list.reset_index(drop=True), values], axis=1)                                                                                                                                     
df_c.to_csv("D:/PhD_work/Code/input_data/lulc/cultivated2019_r.csv")


