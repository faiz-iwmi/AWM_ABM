# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 16:01:13 2022

@author: faiza
"""

from osgeo import ogr
from osgeo import gdal
#import ogr, gdal
import xarray as xr
import pandas as pd
##using shapefile
##get extent of shapefile
def shapefile_extent(mask_sh):
    basin = ogr.Open(mask_sh)
    shp_layer = basin.GetLayer()
    xmin, xmax, ymin, ymax = shp_layer.GetExtent()
    min_lon = xmin
    min_lat = ymin
    max_lon = xmax
    max_lat = ymax
    return min_lon, min_lat, max_lon, max_lat

## Read met data as NC file with correct time and date
## Doesn't matter it is one year data or multi year data
## It needs to be read as YYYY-MM-DD
## This will be used to filtering date and all
##Assign time to data if it is not already assigned
##crop it against given mask shapefile
# data = xr.open_dataset(rain_g)
# startdate = "1990-01-01"
# enddate = "2010-12-31"
# date = pd.date_range(startdate, enddate)
# data["time"]= date
# data= data.sel(time=slice("1990-01-01", "2010-05-31"))

# data2 = xr.open_dataset(rain_g_3)
# startdate = "2010-06-01"
# enddate = "2010-12-31"
# date = pd.date_range(startdate, enddate)
# data2["time"]= date
# #data= data.sel(time=slice("1990-01-01", "2010-05-31"))

# data3 = xr.open_dataset(rain_g_2)
# startdate = "2010-06-01"
# enddate = "2020-12-31"
# date = pd.date_range(startdate, enddate)
# data3["time"]= date
# data3= data3.sel(time=slice("2011-01-01", "2020-12-31"))
# # Concatenate the two datasets along the time dimension
# data4 = xr.concat([data, data2, data3], dim="time")

# # Save the concatenated dataset to a NetCDF file
# data4.to_netcdf("D:/PhD_work/Code/input_data/climate/rain_gauge_idw_com.nc")
def space_time(data,min_lon,max_lon,min_lat,max_lat,startdate, enddate, sim_start, sim_end):
  #read data
  data = xr.open_dataset(data)
  date = pd.date_range(startdate, enddate)
  data["time"]= date
  data= data.sel(time=slice(sim_start, sim_end))
  mask_lon = (data.lon >= min_lon) & (data.lon <= max_lon)
  mask_lat = (data.lat >= min_lat) & (data.lat <= max_lat)
  data = data.where(mask_lon & mask_lat, drop=True)
  return data

def space_time1(data,min_lon,max_lon,min_lat,max_lat,startdate, enddate, sim_start, sim_end):
  #read data
  data = xr.open_dataset(data)
  date = pd.date_range(startdate, enddate)
  data["time"]= date
  data= data.sel(time=slice(sim_start, sim_end))
  mask_lon = (data.longitude >= min_lon) & (data.longitude <= max_lon)
  mask_lat = (data.latitude >= min_lat) & (data.latitude <= max_lat)
  data = data.where(mask_lon & mask_lat, drop=True)
  mask_lon = (data.longitude < 71.315)
  data = data.where(mask_lon, drop=True)
  data = data.rename({'longitude': 'lon','latitude': 'lat'})
  
  return data

##code for masking data spatial data
##mask against shapefile
def space(data,min_lon,max_lon,min_lat,max_lat):
    data = xr.open_dataset(data)
    mask_lon = (data.lon >= min_lon) & (data.lon <= max_lon)
    mask_lat = (data.lat >= min_lat) & (data.lat <= max_lat)
    data = data.where(mask_lon & mask_lat, drop=True)
    return data

def space1(data,min_lon,max_lon,min_lat,max_lat):
    data = xr.open_dataset(data)
    mask_lon = (data.lon >= min_lon) & (data.lon <= max_lon)
    mask_lat = (data.lat >= min_lat) & (data.lat <= max_lat)
    data = data.where(mask_lon & mask_lat, drop=True)
    mask_lon = (data.lon < 71.315)
    data = data.where(mask_lon, drop=True)
    return data
###this for seleiton data as year
def data_year_filter(data,yearstart, yearend):
  #read data
  data= data.sel(time=slice(yearstart, yearend))
  return data
