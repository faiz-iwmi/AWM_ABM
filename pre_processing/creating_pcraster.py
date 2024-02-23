# -*- coding: utf-8 -*-

##creating pc raster clone file

import os
import rioxarray as rio
import xarray as xr
from osgeo import gdal
import matplotlib.pyplot as plt

##read dem file
## crop it based on shapefile extent

data='D:/PhD_work/Code/input_data/dem/dem_rsp.nc'
dem21=space(data,min_lon,max_lon,min_lat,max_lat)

# =============================================================================
# lat1=rain1.lat.values
# lon1=rain1.lon.values
# dem2=dem2.assign_coords(lon=lon1)
# dem2=dem2.assign_coords(lat=lat1)
# =============================================================================

##rio fcuntin requred naming lat and lon as y and x
thisdict = {
  "lat": "y",
  "lon": "x",
}

dem21=dem21.rename(thisdict)

plot = dem21.dem
plot.plot()


#dem2 = dem2.sortby('y', ascending=False)
##save to tif
dem21.dem.rio.to_raster("D:/PhD_work/Code/input_data/dem/dem2.tif")

##upload tif and convert to map as required by pcraster
ds = gdal.Open("D:/PhD_work/Code/input_data/dem/dem2.tif")
format = "PCraster"
driver = gdal.GetDriverByName(format)
ds = gdal.Translate('D:/PhD_work/Code/input_data/dem/dem2.map', ds, outputType = gdal.GDT_Float32)
ds = None

##use pc raster
import pcraster as pcr

dem3=pcr.readmap('D://PhD_work/Code/input_data/dem/dem2.map') 
pcr.matplotlib.plot(dem3, labels=None, title=None, filename=None)

##get flowdir
flow_dir = pcr.lddcreate(dem3, 9999999,9999999,9999999,9999999)
pcr.report(flow_dir, 'D:/PhD_work/Code/input_data/dem/flow_dir.map')




