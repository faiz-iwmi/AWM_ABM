##this moeule calcualte AET for each grid and feedback to hydrologu module
from datetime import datetime
from spatial_data import *
from crop_farmer_data import *
#from data_module import *
from runoff_m import *
from settings import * 
from crop_selection import *
from Agg_Disagg import *
import variables
from cal_para import *
from spatial_data import *
#from spatial_data2 import *

def AET_fun(RootWater, Ks, Kr,i,j,evap1,t, crop,f, yr1):
    #disaggregate De to each user
    #deficit
    spatial['RootField'],spatial['RootWilt'], RF , RWP, Irr, GN_irr = cal_par2(f)
    #De = spatial['RootField'] - variables.RootWater[:,i]
   ##ttoal available water ##this already multiplied with soil depth/not root depth
    #TAW=spatial['RootField']-spatial['RootWilt']
   
    for c in range(0,crop):
        if c < crop-2:
            # Crop Specific
            
            plant_day=crop_var.iloc[10,c+1]
            t_grow=crop_var.iloc[11,c+1]
           
            #load kc here
            Kc=crop_kc[crop_kc.columns[c+1]]
            #if plant_day<=  i <= plant_day+int(t_grow):
            if Kc[j]>0:
            # Calculate water stress factor (Ks)
                #variables.Ks[:,i]=np.where(De <= Dr_lower,1,np.where(De >= Dr_upper,0,(Dr_upper - De)/(Dr_upper-Dr_lower)))
                ks = np.where(variables.RootWater[:,i] >= RWP*spatial['RootField'], 1, (variables.RootWater[:,i] - spatial['RootWilt'])/(RWP*spatial['RootField']-spatial['RootWilt']))
                variables.Ks[:,i]=np.where(ks <= 0,0,ks)
                variables.ETp[c][:][:,i] = Kc[j]*evap1
                variables.ETa[c][:][:,i] = variables.Ks[:,i]*Kc[j]*evap1
                variables.IWR_c_g_mm[c][:][:,i]=variables.ETp[c,:,i]-variables.ETa[c,:,i]
                
                ##srtting to irrigated area as this is used to calcilated IWR in m3
                variables.crop_area_f_d[c][:][:,i]=variables.crop_area_f[c,:,t]
                variables.crop_area_d[c][:][:,i]=variables.crop_area[c,:,t]
                ##calculated irrigated requiremnet here
            ####################STEP 6########################
            else:
                variables.ETp[c][:][:,i] = 0
                variables.ETa[c][:][:,i] = 0
                variables.IWR_c_g_mm[c][:][:,i]=0
                variables.crop_area_f_d[c][:][:,i]=0
                variables.crop_area_d[c][:][:,i]=0
        if c==crop-2: #non-crop land
                
                ks = np.where(variables.RootWater[:,i] >= RWP*spatial['RootField'], 1, (variables.RootWater[:,i] - spatial['RootWilt'])/(RWP*spatial['RootField']-spatial['RootWilt']))
                variables.Ks[:,i]=np.where(ks <= 0,0,ks)
                
                Ke = 1.2
                variables.ETp[c][:][:,i] = Ke*evap1
                variables.ETa[c][:][:,i] =  variables.Ks[:,i]*Ke*evap1
        if c==crop-1:
            variables.ETp[c][:][:,i] = evap1
            variables.ETa[c][:][:,i] = evap1
    
    

    #disaggrgateing irrigation need to each farmers
    variables.IWR_c_f_mm=disagg(variables.IWR_c_g_mm,variables.IWR_c_f_mm,grid_code,farmer_code,i, crop)
    
    # Find the column index that matches the value
    column_index = farm_irr.columns.get_loc(str(yr1[t]))
    ##irrigation varaible is 0 or 1
    irrigation = farm_irr.iloc[:,column_index]
    
    ##get efficiency and multiply  area to get IWR in  m3.   
    for c in range(0,crop-2):
        if c ==0:
            efficiency = np.where (variables.drip_adopt_f[:,t-1]==1, 0.9, 0.6)
            variables.IWR_c_f_m3[c,:,i]=((variables.IWR_c_f_mm[c][:][:,i]*irrigation)/efficiency)*variables.crop_area_f_d[c,:,i]*10*farmer_profile.include
        elif c == 1:
            efficiency = 0.6
            variables.IWR_c_f_m3[c,:,i]=((variables.IWR_c_f_mm[c][:][:,i]*irrigation)/efficiency)*variables.crop_area_f_d[c,:,i]*10*farmer_profile.include
        else:
            efficiency = 0.6
            variables.IWR_c_f_m3[c,:,i]=((variables.IWR_c_f_mm[c][:][:,i]*irrigation)/efficiency)*variables.crop_area_f_d[c,:,i]*10*farmer_profile.include
            

    ##sum up to get total irrigation requirement after efficiency
    # for c in range(0,crop-2):
    #     aa=variables.IWR_c_f_m3[c][:][:,i]
    #     variables.IWR_T_f_m3[:,i]=aa + variables.IWR_T_f_m3[:,i]
   
    ##aggregate in each grid how many farmers have irrigation
    irr_farmers = agg_sum(irrigation,grid_code,farmer_code)
   

##farmers stop irrigating when GWL are below are certain threshold. water is of no use as such at that point.
##15 mbgl threshold or 5 m layer left

    threshold_gw = 5*1000*spatial['YieldGw']
    variables.store[:,i]=np.where(variables.GWS[:,i-1]<=threshold_gw,0,np.where(irr_farmers==0,0,(variables.GWS[:,i-1])/irr_farmers))
    variables.store[:,i]=(variables.store[:,i]/1000)*100*10000

    ##this gives this value to each farmer in the grid
    variables.store_f = disagg_n(variables.store, variables.store_f,grid_code,farmer_code,i)
    
    ##multiple if the farmer has irrigation or not. this will remove rainfed farnmers
    variables.store_f[:,i]=variables.store_f[:,i]*irrigation
        
    ##put a limit to what each farmer can realistically abstract each data
    ##flow rate is 40m3/hr so for 8 hours 320 m3 . 
    ##lets increase to 3 times assumimg more pumps or irrigaiton on one day can be covered on other days so 960 m3
    ##other way is taking well limit. 25 m well weith 4 m dia is around 350 m3, lets say 1.5 times this  525 m3
    ##use the lower value
    variables.store_f[:,i]=np.where(variables.store_f[:,i]>525, 525,variables.store_f[:,i])
    
    ##meeting IWR crop wise
    ##first cotton, then GN and wheat
    for c in range(0,crop-2):
        if c ==0:
            a=variables.store_f[:,i]
            variables.IWRmet_c_f_m3[c,:,i]=np.where(variables.IWR_c_f_m3[c,:,i]<=0, 0, np.minimum(variables.IWR_c_f_m3[c,:,i],a))
            #for cotton and wheat
    ##if IWM met is less than the required amount and farmer has borewell, they can complete the irrigaiton from that
    ##however put a limit as BW yields are low and can only supplement
    ##rate of 10m3/hr so for 8 hour 80 m3.
            variables.bw_abstraction[c,:,i] = np.where(variables.IWRmet_c_f_m3[c,:,i] >= variables.IWR_c_f_m3[c,:,i], 0, np.where(variables.bw_adopt_f[:,t-1]==1, variables.IWR_c_f_m3[c,:,i]-variables.IWRmet_c_f_m3[c,:,i],0))
            variables.bw_abstraction[c,:,i]=  np.where(variables.bw_abstraction[c,:,i]>80, 80,variables.bw_abstraction[c,:,i])
            ##updated water met
            variables.IWRmet_c_f_m3_2[c,:,i] = variables.IWRmet_c_f_m3[c,:,i] + variables.bw_abstraction[c,:,i]
            ##remain shallow GW stroage
            a= a - variables.IWRmet_c_f_m3[c,:,i]
            ##remain bw capacity
            b = 80 - variables.bw_abstraction[c,:,i]
        elif c == 1:
            variables.IWRmet_c_f_m3[c,:,i]=np.where(variables.IWR_c_f_m3[c,:,i]<=0, 0, np.minimum(variables.IWR_c_f_m3[c,:,i],a))
            ##apply deficit irrigation
            variables.IWRmet_c_f_m3[c,:,i]=variables.IWRmet_c_f_m3[c,:,i]*GN_irr
            a= a - variables.IWRmet_c_f_m3[c,:,i]
            
            ##bw is not used here
            variables.IWRmet_c_f_m3_2[c,:,i] = variables.IWRmet_c_f_m3[c,:,i]
        else:
            variables.IWRmet_c_f_m3[c,:,i]=np.where(variables.IWR_c_f_m3[c,:,i]<=0, 0, np.minimum(variables.IWR_c_f_m3[c,:,i],a))
                 ##if IWM met is less than the required amount and farmer has borewell, they can complete the irrigaiton from that
    ##however put a limit as BW yields are low and can only supplement
    ##rate of 10m3/hr so for 8 hour 80 m3.
            variables.bw_abstraction[c,:,i] = np.where(variables.IWRmet_c_f_m3[c,:,i] >= variables.IWR_c_f_m3[c,:,i], 0, np.where(variables.bw_adopt_f[:,t-1]==1, variables.IWR_c_f_m3[c,:,i]-variables.IWRmet_c_f_m3[c,:,i],0))
            variables.bw_abstraction[c,:,i]=  np.where(variables.bw_abstraction[c,:,i]>b, b,variables.bw_abstraction[c,:,i])
            ##updated water met
            variables.IWRmet_c_f_m3_2[c,:,i] = variables.IWRmet_c_f_m3[c,:,i] + variables.bw_abstraction[c,:,i]
            
    ##sum up to get total irrigation requirement met
    for c in range(0,crop-2):
        aa=variables.IWRmet_c_f_m3[c,:,i]
        bb=variables.IWRmet_c_f_m3_2[c,:,i]
        variables.IWRmet_T_f_m3[:,i]=aa + variables.IWRmet_T_f_m3[:,i]
        variables.IWRmet_T_f_m3_2[:,i]=aa + variables.IWRmet_T_f_m3_2[:,i]
   
    
   
    ##get fraction of IWR met
    ##get overall fraction and apply this in next steps for each crop requirment 
    ##for rained this is already zero
    for c in range(0,crop-2): 
        variables.frac_f[c,:,i] = np.where(variables.IWR_c_f_m3[c,:,i]<=0,0, variables.IWRmet_c_f_m3_2[c,:,i]/variables.IWR_c_f_m3[c,:,i])
    
    
    variables.return_flow_total_f[:,i]=variables.IWRmet_T_f_m3_2[:,i]*((1/efficiency)-1)*RF
    
  
    ##multiply fraction to mm
    
    for c in range(0,crop-2):
        variables.IWRmet_c_f_mm[c,:,i]=variables.frac_f[c,:,i]*variables.IWR_c_f_mm[c,:,i]
        #variables.IWRmet_c_f_m3[c,:,i]=variables.frac_f[:,i]*variables.IWR_c_f_mm[c,:,i]*variables.crop_area_f_d[c,:,i]*10
    
    ##aggrgated 
    variables.IWR_met_c_mm=agg_m(variables.IWR_met_c_mm,  variables.IWRmet_c_f_mm,grid_code,farmer_code,i,crop)
    
    
    for c in range(0,crop-2):
        aa=variables.IWR_met_c_mm[c,:,i]*variables.crop_area_d[c,:,i]*10
        variables.IWR_met_g_mm[:,i]=aa + variables.IWR_met_g_mm[:,i]  
    
    variables.IWR_met_g_mm[:,i]= variables.IWR_met_g_mm[:,i]/(100*10)
    
    ##aggrgate IWRmet_c_f_mm for AET
    
    ##aggregating iwr agent equal for giving input to groundwater storage 
    ##here we keep variables.IWRmet_T_f_m3 which is only from top gw not browell
    variables.IWR_T_g_mm=agg_n(variables.IWR_T_g_mm,  variables.IWRmet_T_f_m3,grid_code,farmer_code,i)
    
    ##dividing bu cell area to get in mm
    variables.IWR_T_g_mm[:,i]=variables.IWR_T_g_mm[:,i]/(100*10)
    
    ##aggregating iwr retunr flow to give to SM
    variables.return_flow_total_g=agg_n(variables.return_flow_total_g,  variables.return_flow_total_f,grid_code,farmer_code,i)
    ##dividing bu cell area to get in mm
    variables.return_flow_total_g[:,i]=variables.return_flow_total_g[:,i]/(100*10)

##sum up ETa that is reducing soil moisture
    for c in range(0,crop-2):
        aa=variables.ETa[c][:][:,i]*variables.crop_area_d[c,:,i]*10
        variables.AET_SM[:,i]=aa + variables.AET_SM[:,i]
     
    ##sum up total crop area and get fallow area
    
    variables.fallow_area[:,i]=100 - np.sum(variables.crop_area_d[:,:,i], axis=0)                                                                 
   
    ##updae SM by removing et from fallow area

    variables.AET_SM[:,i]=variables.AET_SM[:,i]+variables.ETa[3][:][:,i]*variables.fallow_area[:,i]*10

   ## grid level in mm for feeding to water balance
    variables.AET_SM[:,i]=variables.AET_SM[:,i]/(100*10)
    
 
    return variables.AET_SM,variables.return_flow_total_g
                
    