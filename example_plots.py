# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:18:17 2022

@author: 3980723
"""
#%% 
# external libraries
import seaborn as sns           # sns.__version__ == '0.11.0'
import matplotlib.pyplot as plt # matplotlib.__version__ == '3.5.0'

import fancyplots as fp


# get builtin data
data = sns.load_dataset("exercise")

order = ['rest', 'walking', 'running']
hue_order = ['1 min', '15 min', '30 min']

#%%  Plain connected stripplot with three categories

fig, ax = plt.subplots(dpi=300)
# add connected points (shows individual data points and connects pairs)     
fp.connected_stripplot(
    data= data,
    x='kind', order=order,
    y='pulse',
    connect_by='id',
    ax=ax
)

#%%  Plain connected stripplot with three categories split across three other categories

fig, ax = plt.subplots(dpi=300)
# add connected points (shows individual data points and connects pairs)     
fp.connected_stripplot(
    data= data,
    x='kind', order=order,
    y='pulse',
    hue='time', hue_order=hue_order,
    connect_by='id',
    connectorzorder=10,
    ax=ax,    
)

#%% Combined with a violin plot

# create a figure and axes
fig, ax = plt.subplots(dpi=300)

# create the violin plot (shows smoothed distribution) 
sns.violinplot(
    data= data,
    x='kind', order=order,
    y='pulse',
    ax=ax
)

# add connected points (shows individual data points and connects pairs)     
fp.connected_stripplot(
    data= data,
    x='kind', order=order,
    y='pulse',
    connect_by='id',
    connectorzorder=10,
    markercolor='k',
    ax=ax,    
)


#%% Combined with a violin plot with hues
# create a figure and axes
fig, ax = plt.subplots(dpi=300)

# create the violin plot (shows smoothed distribution) 
sns.violinplot(
    data= data,
    x='kind', order=order,
    y='pulse',
    hue='time', hue_order=hue_order,
    ax=ax
)

# add connected points (shows individual data points and connects pairs)     
fp.connected_stripplot(
    data= data,
    x='kind', order=order,
    y='pulse',
    hue='time', hue_order=hue_order,
    connect_by='id',
    connectorzorder=10,
    markercolor='k',
    ax=ax,    
)
