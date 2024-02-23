# -*- coding: utf-8 -*-

##this function sums up ET and AErt and Irriigation to cauclatate each agent yeild
from settings import * 
from WB_yield_space_runoff import *
import variables 


def crop_yield_ag(day,precip1,t, crop, day_end, yr1):
    #global ETp,ETa
    a=crop_ratio.index[crop_ratio['Year'] == yr1[t]]
    column_index = farm_irr.columns.get_loc(str(yr1[t]))
    column_index1 = farm_irr.columns.get_loc(str(yr1[t]))
    #count = 0
    for c in range(0,crop-2):
        
        ETc=pd.DataFrame(variables.ETp[c,:,day:day+day_end])
        
        ETc=ETc.T
       
        stage = crop_kc[crop_kc.columns[c+5]]
        
        
        ETc=ETc.join(stage)
        ETc.columns = [*ETc.columns[:-1], 'stage']
        
        #ETc_sum=np.sum(ETc[:,:],axis = 1)
        ETc_sum=ETc.groupby("stage", dropna=True).sum()
        
        ETc_sum=ETc_sum.T
       
        
        
        ETa=pd.DataFrame(variables.ETa[c,:,day:day+day_end])
        ETa=ETa.T
        ETa=ETa.join(stage)
        ETa.columns = [*ETa.columns[:-1], 'stage']
        #ETc_sum=np.sum(ETc[:,:],axis = 1)
        ETa_sum=ETa.groupby("stage", dropna=True).sum()
        ETa_sum=ETa_sum.T
        
        variables.ETp_f_1=disagg_a(ETc_sum.s1, variables.ETp_f_1,grid_code,farmer_code,c,t)
        variables.ETp_f_2=disagg_a(ETc_sum.s2, variables.ETp_f_2,grid_code,farmer_code,c,t)
        variables.ETp_f_3=disagg_a(ETc_sum.s3, variables.ETp_f_3,grid_code,farmer_code,c,t)
        variables.ETp_f_4=disagg_a(ETc_sum.s4, variables.ETp_f_4,grid_code,farmer_code,c,t)
        
        variables.ETa_f_1=disagg_a(ETa_sum.s1, variables.ETa_f_1,grid_code,farmer_code,c,t)
        variables.ETa_f_2=disagg_a(ETa_sum.s2, variables.ETa_f_2,grid_code,farmer_code,c,t)
        variables.ETa_f_3=disagg_a(ETa_sum.s3, variables.ETa_f_3,grid_code,farmer_code,c,t)
        variables.ETa_f_4=disagg_a(ETa_sum.s4, variables.ETa_f_4,grid_code,farmer_code,c,t)
        
        IWR_f=pd.DataFrame(variables.IWRmet_c_f_mm[c,:,day:day+day_end])
        IWR_f=IWR_f.T
        IWR_f=IWR_f.join(stage)
        IWR_f.columns = [*IWR_f.columns[:-1], 'stage']
        IWR_f=IWR_f.groupby("stage", dropna=True).sum()
        IWR_f=IWR_f.T
        
        #variables.IWRmet_c_f_mm_year[c,:,t]=IWR_f
        
        CWR_p1=((variables.ETp_f_1[c,:,t]))*farmer_profile.include
        CWR_p2=((variables.ETp_f_2[c,:,t]))*farmer_profile.include
        CWR_p3=((variables.ETp_f_3[c,:,t]))*farmer_profile.include
        CWR_p4=((variables.ETp_f_4[c,:,t]))*farmer_profile.include
        
        CWR_a1=((variables.ETa_f_1[c,:,t]+ IWR_f.s1))*farmer_profile.include
        CWR_a2=((variables.ETa_f_2[c,:,t]+ IWR_f.s2))*farmer_profile.include
        CWR_a3=((variables.ETa_f_3[c,:,t]+ IWR_f.s3))*farmer_profile.include
        CWR_a4=((variables.ETa_f_4[c,:,t]+ IWR_f.s4))*farmer_profile.include
        
        #CWR_a=variables.ETa_f_irr[c,:,day:day+day_end]
        ky1 = crop_var.iloc[20,c+1]
        ky2 = crop_var.iloc[21,c+1]
        ky3= crop_var.iloc[22,c+1]
        ky4 = crop_var.iloc[23,c+1]
        
        #CWP = crop_ratio.iloc[a.item(),c+4]
        CWP = crop_ratio.iloc[a.item(),c+5]
        #CWR=np.sum(CWR_p)
        #ACWR=np.sum(CWR_a)
        #ACWR=np.transpose(np.sum(CWR_a,axis = 1))
        ##ration of et and potential
        r1=np.where(CWR_p1==0,0,(1-(ky1*(1-(CWR_a1/CWR_p1)))))
        r2=np.where(CWR_p2==0,0,(1-(ky2*(1-(CWR_a2/CWR_p2)))))
        r3=np.where(CWR_p3==0,0,(1-(ky3*(1-(CWR_a3/CWR_p3)))))
        r4=np.where(CWR_p4==0,0,(1-(ky4*(1-(CWR_a4/CWR_p4)))))
        
        r1=np.where(r1<0,0,r1)
        r2=np.where(r2<0,0,r2)
        r3=np.where(r3<0,0,r3)
        r4=np.where(r4<0,0,r4)
        
        red = r1*r2*r3*r4
        variables.Yield[c,:,t]=CWP*red
        irr = farm_irr.iloc[:,column_index1]
        variables.Yield_irr[c,:,t]=variables.Yield[c,:,t]*irr
        variables.Yield_rain[c,:,t]=variables.Yield[c,:,t]*(1-irr)
        #variables.Yield[c,:,t]=np.where(CWR_p==0,0,(1-(ky*(1-(CWR_a/CWR_p)))))
        aa = np.where(CWR_p1==0,0,variables.Yield[c,:,t]/CWP)
        #bb = np.where(CWR_p1==0,0,1)
        #count= count + bb
        variables.avg_yield[:,t] = aa + variables.avg_yield[:,t]
    variables.avg_yield[:,t]=variables.avg_yield[:,t]/3
    return variables.Yield
