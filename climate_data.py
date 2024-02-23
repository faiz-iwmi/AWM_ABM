# -*- coding: utf-8 -*-


##spatial data 

from settings import *
from space_time_fn import *


min_lon, min_lat, max_lon, max_lat = shapefile_extent(mask_sh)

#rain1 = space_time(rain,min_lon,max_lon,min_lat,max_lat,startdate, enddate, sim_start, sim_end)
#rainplot = rain1.Rain
#Rain1d = rainplot.isel(time=200)
##function to get one slice
#Rain1d = Rain1d.where(Rain1d > -50, 0) #seeting negative values 0
#Rain1d.attrs
#Rain1d.plot()

##for raingauge data
rain1 = space_time1(rain_g_3,min_lon,max_lon,min_lat,max_lat,startdate_g, enddate_g, sim_start, sim_end)

    
p = rain1  ##start_year and end year are in settings already.
#days=len(p.time)
del rain1

meanT1 = space_time(meanT,min_lon,max_lon,min_lat,max_lat,startdate_t, enddate_t, sim_start, sim_end)
t_mean= meanT1
del meanT1
  
minT1 = space_time(minT,min_lon,max_lon,min_lat,max_lat,startdate_t, enddate_t, sim_start, sim_end)
temp_min_data=minT1
del minT1
   
maxT1 = space_time(maxT,min_lon,max_lon,min_lat,max_lat,startdate_t, enddate_t, sim_start, sim_end)
temp_max_data= maxT1
del maxT1
 
# ET0
#t_mean["ET0"] = 0.0023*15*(t_mean.meanT+17.8)*(temp_max_data.maxT-temp_min_data.minT)**0.5
t_mean["ET0"] = 0.0023*15*(t_mean.meant+17.8)*(temp_max_data.maxt-temp_min_data.meant)**0.5
