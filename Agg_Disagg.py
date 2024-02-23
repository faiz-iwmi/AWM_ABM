# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
#import numpy_indexed as npi
from crop_farmer_data import *
from settings import *
#disaggregate grid data to farmers

def disagg(data_g, data_ag,grid_code,farmer_code,i, crop):
    for c in range(0,crop-2):
          grid_code.data_g=data_g[c][:][:,i]
          aa= grid_code.merge(farmer_code,how='left', left_on='grid_id', right_on='grid_id')
          #aa = aa[aa['farmer_id'].notna()]
          data_ag[c,:,i]=aa.data_g
          #idx = npi.indices(grid_code.grid_id, farmer_code.grid_id)
          #for k in range(len(idx)):
          #    b= grid_code.data[idx[k]]
          #    data_ag[c,k,i]=b
    return data_ag

# def disagg(data_g, data_ag, grid_code, farmer_code, i, crop):
#     grid_ids = grid_code['grid_id'].values
#     farmer_ids = farmer_code['grid_id'].values

#     for c in range(crop - 2):
#         grid_data_c_i = data_g[c][:, i]
#         mask = np.isin(grid_ids, farmer_ids)
#         filtered_grid_data = grid_data_c_i[mask]

#         data_ag[c, mask, i] = filtered_grid_data

#     return data_ag

# Example usage:
# data_g, data_ag are NumPy arrays
# grid_code, farmer_code are pandas DataFrames

# result = disagg(data_g, data_ag, grid_code, farmer_code, i, crop)

# def disagg(data_g, data_ag, grid_code, farmer_code, i, crop):
#     grid_ids_g = grid_code['grid_id'].values
#     data_g_values = data_g[:, :, i]
#     merged_df = grid_code.merge(farmer_code, how='left', left_on='grid_id', right_on='grid_id')
#     common_indices = np.searchsorted(grid_ids_g, merged_df['grid_id'].values)
#     data_ag[:, common_indices, i] = data_g_values[:, common_indices]

#     return data_ag




# def disagg_a(data_g, data_ag, grid_code, farmer_code, c, t):
#     grid_ids_g = grid_code['grid_id'].values
#     data_g_values = data_g
    
#     merged_df = grid_code.merge(farmer_code, how='left', on='grid_id')
#     data_ag[c, :, t] = merged_df['data_g'].values

#     return data_ag


# def disagg_n(data_g, data_ag, grid_code, farmer_code, i):
#     grid_ids_g = grid_code['grid_id'].values
#     data_g_values = data_g[:, i]

#     merged_df = grid_code.merge(farmer_code, how='left', on='grid_id')
#     data_ag[:, i] = merged_df['data_g'].values

#     return data_ag


##annual sum
def disagg_a(data_g, data_ag,grid_code,farmer_code,c,t):
    grid_code.data_g=data_g
    aa= grid_code.merge(farmer_code,how='left', left_on='grid_id', right_on='grid_id')
    
 
    data_ag[c,:,t]=aa.data_g   
    
    return data_ag


def disagg_n(data_g, data_ag,grid_code,farmer_code,i):
    grid_code.data_g=data_g[:,i]
    aa= grid_code.merge(farmer_code,how='left', left_on='grid_id', right_on='grid_id')
    
    data_ag[:,i]=aa.data_g   

    return data_ag



####aggrgate farmers data to grid
##here we match all farmers data to one grid based on matching....
##this is for sum
# =============================================================================
# def agg(data_g, data_ag,grid_code,farmer_code,i, crop):
#     for c in range(0,crop-2):
#         farmer_code.data_f=data_ag[c][:][:,i]
#         a=farmer_code.groupby('grid_id').sum()
#         data_g[c][:][:,i]=a.data_f
#     return data_g
# =============================================================================



def agg(data_g, data_ag, grid_code, farmer_code, i, crop):
    for c in range(0, crop-2):
        farmer_code_data_f = data_ag[c][:][:, i]
        farmer_code['data_f'] = farmer_code_data_f
        a = farmer_code.groupby('grid_id')['data_f'].sum()
        data_g[c][:][:, i] = a.reindex(grid_code['grid_id']).values

    return data_g

def agg_m(data_g, data_ag, grid_code, farmer_code, i, crop):
    for c in range(0, crop-2):
        farmer_code_data_f = data_ag[c][:][:, i]
        farmer_code['data_f'] = farmer_code_data_f
        a = farmer_code.groupby('grid_id')['data_f'].agg(np.nanmean)
        data_g[c][:][:, i] = a.reindex(grid_code['grid_id']).values

    return data_g
    
# def agg_n(data_g, data_ag,grid_code,farmer_code,i):
#     farmer_code.data_f=data_ag[:,i]
#     a=farmer_code.groupby('grid_id').sum()
#     data_g[:,i]=a.data_f
#     return data_g
 
# def agg_mean(data_g, data_ag,grid_code,farmer_code,i):
#     value = data_ag
#     value = np.where(value == 0, np.nan, value)
#     farmer_code.data_f=value
#     a = farmer_code.groupby('grid_id').agg(np.nanmean)
#     a = a.fillna(0)
#     data_g[:,i]=a.data_f
#     return data_g

# def agg_sum(data_ag,grid_code,farmer_code):
#     value = data_ag
#     farmer_code.data_f=value
#     a = farmer_code.groupby('grid_id').agg(np.sum)
#     a = a.data_f
#     return a



def agg_n(data_g, data_ag, grid_code, farmer_code, i):
    farmer_code['data_f'] = data_ag[:, i]
    a = farmer_code.groupby('grid_id')['data_f'].sum()
    data_g[:, i] = a.reindex(grid_code['grid_id']).values
    return data_g

def agg_mean(data_g, data_ag, grid_code, farmer_code, i):
    value = np.where(data_ag == 0, np.nan, data_ag)
    farmer_code['data_f'] = value
    a = farmer_code.groupby('grid_id')['data_f'].agg(np.nanmean)
    a = a.fillna(0)
    data_g[:, i] = a.reindex(grid_code['grid_id']).values
    return data_g

def agg_sum(data_ag, grid_code, farmer_code):
    farmer_code['data_f'] = data_ag
    a = farmer_code.groupby('grid_id')['data_f'].sum()
    return a.values



# def crop_agg(data_g, data_ag,grid_code,farmer_code,i,j, crop, crop_var):
#     for c in range(0,crop-2):
#         if c==0:
#             if j == crop_var.iloc[10,c+1]:
#                 farmer_code.data_f=data_ag[c][:][:,i]
#                 a=farmer_code.groupby('grid_id').sum()
#                 data_g[c][:][:,i]=a.data_f
#         elif c==1: #for groundnut
#             if j == crop_var.iloc[10,c+1]:
#                 farmer_code.data_f=data_ag[c][:][:,i]
#                 a=farmer_code.groupby('grid_id').sum()
#                 data_g[c][:][:,i]=a.data_f
                
#         else: #for wheat with c==2
#             if j == crop_var.iloc[10,c+1]:
#                 farmer_code.data_f=data_ag[c][:][:,i]
#                 a=farmer_code.groupby('grid_id').sum()
#                 data_g[c][:][:,i]=a.data_f
#     return data_g

# =============================================================================


def crop_agg(data_g, data_ag, grid_code, farmer_code, i, j, crop, crop_var):
    c_index = np.arange(0, crop-2)
    c_values = crop_var.iloc[10, c_index + 1].values

    if j in c_values:
        c_mask = c_values == j
        c_values_masked = c_values[c_mask]
        c_index_masked = c_index[c_mask]

        for c, c_var in zip(c_index_masked, c_values_masked):
            farmer_code['data_f'] = data_ag[c][:][:, i]
            a = farmer_code.groupby('grid_id')['data_f'].sum()
            data_g[c][:][:, i] = a.reindex(grid_code['grid_id']).values

    return data_g


#idx = npi.indices(y, x)

#https://stackoverflow.com/questions/58745162/best-way-to-compare-two-numpy-array-of-different-sizes

#https://www.geeksforgeeks.org/numpy-in1d-function-in-python/

#b=np.nonzero(np.in1d(farmer_code.grid_id,grid_code.grid_id))
#b=np.arange(farmer_code.grid_id.shape[0])[np.in1d(farmer_code.grid_id,grid_code.grid_id)]

#c=np.where(np.isin(a, b))
#a=np.nonzero(np.in1d(grid_code.grid_id,farmer_code.grid_id))

#https://stackoverflow.com/questions/46042469/compare-two-arrays-with-different-size-python-numpy
#np.arange(farmer_code.grid_id.shape[0])[np.in1d(grid_code.grid_id,farmer_code.grid_id)]
#a=farmer_code.grid_id
#b=grid_code.grid_id
#n = min(len(a), len(b))
#out_idx = np.flatnonzero(a[:n] == b[:n])
#out_val = b[out_idx] # or b[out_idx] both work

#https://stackoverflow.com/questions/32191029/getting-the-indices-of-several-elements-in-a-numpy-array-at-once
#b=farmer_code.grid_id
#a=grid_code.grid_id


#https://stackoverflow.com/questions/8251541/numpy-for-every-element-in-one-array-find-the-index-in-another-array



