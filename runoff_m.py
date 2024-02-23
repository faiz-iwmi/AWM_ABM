# -*- coding: utf-8 -*-


## sautration excess runoff
import numpy as np
import xarray as xr
from osgeo import ogr
from osgeo import gdal
#import ogr, gdal
import rioxarray as rio
import pcraster as pcr
from space_time_fn import *
##calcualte runoff from rain happening due to sataruation excess runoff
def RootRunoff(rain,RootSat,RootWater):
    #-Saturation excess surface runoff
    #-Assume infiltration capacity to be equal to saturated hydraulic conductivity
    #Infil_cap = RootKsat
    #Infil = np.maximum(0, np.minimum(rain, Infil_cap, RootWater-RootSat))
    #-Infiltration
    rootrunoff = np.where(rain>0, np.maximum(RootWater-RootSat,0),0)
    
    return rootrunoff


#-Function to calculate surface runoff
#def RootRunoff(self, pcr, rainfrac, rain):
#    #-Infiltration excess surface runoff
#    if self.InfilFLAG == 1:
 #       #-Infiltration capacity, scaled based on rootwater content and ksat and corrected for paved surface
#        Infil_cap = self.K_eff * self.RootKsat / 24 * (1 + ((self.RootSat - self.RootWater) / self.RootSat))**self.Labda_Infil

        #-Infiltration
#        Infil_excess = pcr.ifthenelse((self.Alpha * rain) > Infil_cap, rain - ((self.Alpha * rain - Infil_cap)**2) / (self.Alpha**2 * rain), rain)
#       Saturated_excess = self.RootSat - self.RootWater
#       Infil = pcr.max(0, pcr.min(Infil_excess, Saturated_excess)) * (1-self.pavedFrac)

        #-Surface runoff
#        rootrunoff = rain - Infil

    #-Saturation excess surface runoff
#    else:
        #-Assume infiltration capacity to be equal to saturated hydraulic conductivity
#       Infil_cap = self.RootKsat

#        #-Infiltration
 #       Infil = pcr.max(0, pcr.min(rain, Infil_cap, self.RootSat - self.RootWater))
        #-Runoff
#      rootrunoff = pcr.ifthenelse(rainfrac > 0, rain - Infil, 0)

#    return rootrunoff, Infil


##calcualte laterflow from first layer
def RootDrainage(RootWater, rootdrain, rootfield, rootsat, drainvel, rootTT):
    rootexcess = np.maximum(RootWater - rootfield, 0)
    rootexcessfrac = rootexcess / (rootsat - rootfield)
    rootlat = rootexcessfrac * drainvel
    rootdrainage = np.maximum(np.minimum(rootexcess, rootlat  * (1-np.exp(-1/rootTT)) + rootdrain * (np.exp(-1/rootTT))), 0)
    return rootdrainage

##calcualte percolation down from layer 1
def RootPercolation(RootWater, subwater, rootfield, rootTT, subsat):
    rootexcess1 = np.maximum(RootWater - rootfield, 0) ##water in layer is above fc
    rootexcess2 = np.maximum(subsat - subwater, 0) ##there is space in layer 2 to get water
    rootexcess=np.where((rootexcess1<=0) | (rootexcess2>=0), np.where (rootexcess1>=rootexcess2,rootexcess2,rootexcess1),0)
    
    rootperc = rootexcess * (1 - np.exp(-1 / rootTT))
    #rootperc = np.where(subwater >= subsat, 0, np.minimum(subsat - subwater, rootperc))
    rootperc = np.maximum(np.minimum(rootperc, rootexcess), 0)
    return rootperc


#-Function to calculate rootzone drainage
#def RootDrainage(pcr, rootwater, rootdrain, rootfield, rootsat, drainvel, rootTT):
#    rootexcess = pcr.max(rootwater - rootfield, 0)
#    rootexcessfrac = rootexcess / (rootsat - rootfield)
#    rootlat = rootexcessfrac * drainvel
#    rootdrainage = pcr.max(pcr.min(rootexcess, rootlat * (1-pcr.exp(-1/rootTT)) + rootdrain * pcr.exp(-1/rootTT)), 0)
#    return rootdrainage

#-Function to calculate rootzone percolation
#def RootPercolation(pcr, rootwater, subwater, rootfield, rootTT, subsat):
#    rootexcess = pcr.max(rootwater - rootfield, 0)
#    rootperc = rootexcess * (1 - pcr.exp(-1 / rootTT))
#    rootperc = pcr.ifthenelse(subwater >= subsat, 0, pcr.min(subsat - subwater, rootperc))
#   rootperc = pcr.max(pcr.min(rootperc, rootexcess), 0)
#    return rootperc

#Function to calculate the right fraction between the two fluxes
def CalcFrac(rootwater, rootfield, rootdrain, rootperc):
    rootexcess = np.maximum(rootwater - rootfield, 0)
    est = np.where(rootdrain + rootperc<= 0,0,rootdrain + rootperc)
    frac=np.where(est<= rootexcess,0,(est - rootexcess) / est)
    #frac = ((rootdrain + rootperc) - rootexcess) / (rootdrain + rootperc)
    rootdrain = rootdrain - (rootdrain * frac)
    rootperc = rootperc - (rootperc * frac)
    return rootdrain, rootperc


#-Function to calculate capillary rise for layer 2 to layer 1
def CapilRise(subfield, subwater, capmax, rootwater, rootsat, rootfield):
    subrelwat = np.maximum(np.minimum((subwater / subfield), 1), 0)
    rootrelwat = np.maximum(np.minimum((rootwater / rootfield), 1), 0)
    caprise = np.minimum(subwater, capmax * (1 - rootrelwat) * subrelwat) ##subwater cannot reduce below wp
    caprise = np.maximum(np.minimum(caprise, np.maximum(rootsat - rootwater,0)),0)  # adding caprise can not exceed saturated rootwater content
    return caprise


#-Function to calculate capillary rise
#def CapilRise(pcr, subfield, subwater, capmax, rootwater, rootsat, rootfield):
#    subrelwat = pcr.max(pcr.min((subwater / subfield), 1), 0)
#    rootrelwat = pcr.max(pcr.min((rootwater / rootfield), 1), 0)
 #   caprise = pcr.min(subwater, capmax * (1 - rootrelwat) * subrelwat)
 #   caprise = pcr.min(caprise, rootsat - rootwater)  # adding caprise can not exceed saturated rootwater content
#    return caprise


#-Function to calculate percolation from subsoil (only if groundwater module is used)
def SubPercolation(subwater, subfield, subTT, gw, gwsat):
    #subperc =  np.where((gw < gwsat) & ((subwater - subfield) > 0), (subwater - subfield) * (1 - np.exp(-1 / subTT)), 0)
    rootexcess1 = np.maximum(subwater - subfield, 0) ##water in layer is above fc
    rootexcess2 = np.maximum(gwsat - gw, 0) ##there is space in layer 2 to get water
    rootexcess=np.where((rootexcess1<=0) | (rootexcess2>=0), np.where (rootexcess1>=rootexcess2,rootexcess2,rootexcess1),0)
    subperc = rootexcess * (1 - np.exp(-1 / subTT))
    #rootperc = np.where(subwater >= subsat, 0, np.minimum(subsat - subwater, rootperc))
    subTT = np.maximum(np.minimum(subTT, rootexcess), 0)
    return subperc

#-Function to calculate percolation from subsoil (only if groundwater module is used)
#def SubPercolation(pcr, subwater, subfield, subTT, gw, gwsat):
#    subperc =  pcr.ifthenelse((gw < gwsat) & ((subwater - subfield) > 0), (subwater - subfield) * (1 - pcr.exp(-1 / subTT)), 0)
#    return subperc

#-Function to calculate drainage from subsoil (only if groundwater module is NOT used)
#def SubDrainage(pcr, subwater, subfield, subsat, drainvel, subdrainage, subTT):
#    subexcess = pcr.max(subwater - subfield, 0)
#    subexcessfrac = subexcess / (subsat - subfield)
#    sublateral = subexcessfrac * drainvel
 #   subdrainage = (sublateral + subdrainage) * (1 - pcr.exp(-1 / subTT))
 #   subdrainage = pcr.max(pcr.min(subdrainage, subwater), 0)
 #   return subdrainage



## groundwater flows
#-Function to calculate groundwater recharge
def GroundWaterRecharge(deltagw, gwrecharge, subperc):
    gwseep = (1 - np.exp(-1 / deltagw)) * (subperc)
    gwrecharge = (np.exp(-1 / deltagw) * gwrecharge) + gwseep
    return gwrecharge

#-Function to calculate baseflow
def BaseFlow(gw, baser, gwrecharge, basethresh, alphagw):
    baser = np.where(gw <= basethresh, 0, (baser * np.exp(-alphagw) + gwrecharge * (1 - np.exp(-alphagw))))
    return baser

#-Function to calculate the groundwater height, taken from the bottom of the gw layer (zero reference)
def HLevel(Hgw, alphagw, gwrecharge, yield_gw):
    Hgw = (Hgw * np.exp(-alphagw)) + ((gwrecharge * (1 - np.exp(-alphagw))) / (800 * yield_gw * alphagw))
    return Hgw

###routing
def ROUT(pcr, total_runoff, routed_runoff, flow_dir, kx,i, cellArea,p):
    q = flow_input(total_runoff[:,i], p)
    rr = (q * 0.001 * cellArea) / (24*3600)
    ra = pcr.accuflux(flow_dir, rr)
    ra_np=pcr.numpy_operations.pcr2numpy(ra, -9999)
    ra_np=ra_np.ravel()
    routed_runoff= (1 - kx) * ra_np + kx * routed_runoff[:,i-1]
    return routed_runoff


##function to create flow input to rout function
def flow_input(array, p):
    ##this is equal to length of lat and lon
    a=np.reshape(array, (len(p.lat),len(p.lon)))
    a = xr.DataArray(a, coords=[("y", p.lat.data), ("x", p.lon.data)])
    #a = a.sortby('y', ascending=False)
    #a.to_netcdf("C:/Users/dell/Desktop/PhD_work/Code/Git/shmodel_citg_tudelft/input_data/dem/rout.nc")
    #os.remove("D:/PhD_work/Code/input_data/dem/rout2.tif")
    path="D:/PhD_work/Code/input_data/dem/rout2.tif"
    #shutil.rmtree(path) 
    #os.remove(path)
    a.rio.to_raster(path)
    ds = gdal.Open("D:/PhD_work/Code/input_data/dem/rout2.tif", gdal.GA_ReadOnly)
    #Open output format driver, see gdal_translate --formats for list
    format = "PCraster"
    driver = gdal.GetDriverByName(format)
    ds1 = gdal.Translate('D:/PhD_work/Code/input_data/dem/rout2.map', ds, xRes=.01, yRes=.01, outputType = gdal.GDT_Float32)
    ##
    #ds.close()
    ds = None
    # close the rasterio dataset
    rout=pcr.readmap('D:/PhD_work/Code/input_data/dem/rout2.map')
    return rout

#-dynamic groundwater processes
def dynamic(self, pcr, ActSubPerc, GlacPerc):
    # GwOld = self.Gw
    #-Groundwater recharge
    self.GwRecharge = self.groundwater.GroundWaterRecharge(pcr,	self.deltaGw, self.GwRecharge, ActSubPerc, GlacPerc)
    #-Report groundwater recharge
    self.reporting.reporting(self, pcr, 'TotGwRechargeF', self.GwRecharge)
    #-Update groundwater storage
    self.Gw = self.Gw + self.GwRecharge
    #-Baseflow
    self.BaseR = self.groundwater.BaseFlow(pcr, self.Gw, self.BaseR, self.GwRecharge, self.BaseThresh, self.alphaGw)
    #-Update groundwater storage
    self.Gw = self.Gw - self.BaseR
    #-Report groundwater storage
    self.reporting.reporting(self, pcr, 'StorGroundW', self.Gw * (1-self.openWaterFrac))
    #-Correct for open-water fraction
    self.BaseR = self.BaseR * (1-self.openWaterFrac)
    #-Report Baseflow
    self.reporting.reporting(self, pcr, 'TotBaseRF', self.BaseR)
    #-Calculate groundwater level
    self.H_gw = self.groundwater.HLevel(pcr, self.H_gw, self.alphaGw, self.GwRecharge, self.YieldGw)
    #-Report groundwater level
    self.reporting.reporting(self, pcr, 'GWL', ((self.SubDepthFlat + self.RootDepthFlat + self.GwDepth)/1000 - self.H_gw)*-1)



#def RootRunoff(self, pcr, rainfrac, rain):
#    #-Infiltration excess surface runoff
#    if self.InfilFLAG == 1:
#        #-Infiltration capacity, scaled based on rootwater content and ksat and corrected for paved surface
#        Infil_cap = self.K_eff * self.RootKsat / 24 * (1 + ((self.RootSat - self.RootWater) / self.RootSat))**self.Labda_Infil
#
#        #-Infiltration
#        Infil_excess = pcr.ifthenelse((self.Alpha * rain) > Infil_cap, rain - ((self.Alpha * rain - Infil_cap)**2) / (self.Alpha**2 * rain), rain)
#        Saturated_excess = self.RootSat - self.RootWater
 #       Infil = pcr.max(0, pcr.min(Infil_excess, Saturated_excess)) * (1-self.pavedFrac)

 #       #-Surface runoff
 #       rootrunoff = rain - Infil

    #-Saturation excess surface runoff
 #   else:
        #-Assume infiltration capacity to be equal to saturated hydraulic conductivity
 #       Infil_cap = self.RootKsat

 #       #-Infiltration
 #       Infil = pcr.max(0, pcr.min(rain, Infil_cap, self.RootSat - self.RootWater))
        #-Runoff
 #       rootrunoff = pcr.ifthenelse(rainfrac > 0, rain - Infil, 0)

 #   return rootrunoff, Infil


## percolation


## lateral flows







