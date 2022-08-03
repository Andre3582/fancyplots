# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 13:56:39 2022

@author: 3980723
"""

import numpy as np
from matplotlib import pyplot as plt

rng = np.random.default_rng()

def connected_scatterplot(data, x, y, connect_by, hue=None, order=None, hue_order=None, markersize=None, markercolor=None, palette=None, markeredgecolor=None, markeredgewidth=None, connectorwidth=1, connectorcolor=(0,0,0,0.4), connectorstyle=':', jitter=0.1, offset=0.2, ax=None, markerzorder=10, connectorzorder=0, **kwargs):
    
    # create a fig an axes if none is provided
    if ax is None:
        fig, ax = plt.subplots()
      
    
    # extract relevant data
    order = order if order is not None else data[x].unique()
    ycoords = dict()
    xcoords = dict()

    
    if hue is None:
        for i, x_value in enumerate(order):
            ycoords[x_value] = data[(data[x] == x_value)].sort_values(by=connect_by)[y]
            xcoords[x_value] = rng.uniform(-jitter/2,jitter/2, ycoords[x_value].size) + i
            
    else:      
        
        hue_order = hue_order if hue_order is not None else data[hue].unique()    
        
        for x_offset, x_value in enumerate(order):
            ycoords[x_value] = dict()
            xcoords[x_value] = dict()
            
            for hue_offset, hue_value in zip([-offset, offset], hue_order):
                ycoords[x_value][hue_value] = data[(data[x] == x_value) & (data[hue] == hue_value)].sort_values(by=connect_by)[y]
                xcoords[x_value][hue_value] = rng.uniform(-jitter/2, jitter/2, ycoords[x_value][hue_value].size) + hue_offset + x_offset # i determines main x-coordinate, hue_offset shifts it slightly to the left or right
    

    # do the plotting
    
    
    if hue is None: # if no hue is given
    
        # plot the scattered dots
        color_idx= 0
        for x_value in (order):
            ax.scatter(
                xcoords[x_value], 
                ycoords[x_value], 
                s=markersize, 
                color=palette[color_idx], 
                linewidth=markeredgewidth,
                zorder=markerzorder, 
                **kwargs
                )
            color_idx+=1
        
        # plot the connectors
        x_val1, x_val2 = order
        x_pairs = zip(xcoords[x_val1], xcoords[x_val2])
        y_pairs = zip(ycoords[x_val1], ycoords[x_val2])
        
        for x_pair, y_pair in zip(x_pairs, y_pairs):
            ax.plot(x_pair, y_pair, 
                    color=connectorcolor, 
                    linewidth=connectorwidth, 
                    linestyle=connectorstyle, 
                    zorder=connectorzorder
                    **kwargs)

   
    else: # if hue is given -> split the scatterd markers into two
        
        # plot the markers
        for x_value in (order):
            color_idx= 0
            for hue_value in (hue_order):
                ax.scatter(
                    xcoords[x_value][hue_value], ycoords[x_value][hue_value], 
                    s=markersize, 
                    color=palette[color_idx], 
                    edgecolor=markeredgecolor, 
                    linewidth=markeredgewidth,
                    label=hue_value, 
                    zorder=markerzorder, 
                    **kwargs
                    )
                
                color_idx+=1
        
        # plot the connectors
        for x_value in (order):
            h1, h2 = hue_order
            x_pairs = zip(xcoords[x_value][h1], xcoords[x_value][h2])
            y_pairs = zip(ycoords[x_value][h1], ycoords[x_value][h2])
            
            for x_pair, y_pair in zip(x_pairs, y_pairs):
                ax.plot(x_pair, y_pair, 
                        color=connectorcolor, 
                        linewidth=connectorwidth, 
                        linestyle=connectorstyle, 
                        zorder=connectorzorder,
                        **kwargs)
    
                
    # add default labels
    ax.set(**{
        'ylabel': y,
        'xlabel': x,
        'xticks': list(range(len(order))),
        'xticklabels': order
    })
    
    # add legend if hue is given
    if hue is not None:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:2], labels[:2], title=hue)
    
    return ax