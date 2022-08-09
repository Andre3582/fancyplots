# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 13:56:39 2022

@author: 3980723
"""

import numpy as np
import seaborn as sns 
from matplotlib import pyplot as plt

rng = np.random.default_rng()

def connected_stripplot(data, x, y, connect_by, hue=None, order=None, hue_order=None, marker='o', markersize=None, markercolor=None, markeralpha=1, palette=sns.color_palette(), markeredgecolor=None, markeredgewidth=None, connectorwidth=2, connectorcolor=(0,0,0,0.7), connectorstyle='-', jitter=0.1, offset=0.2, ax=None, markerzorder=10, connectorzorder=0, **kwargs):
    
    """This function creates a stripplot with corresponding dots (values of the same categoty) connected by a line.
    
    The 'data', 'x', 'y', and 'hue' variables are equvalent to those of sns.stripplot.
    
    The 'connect_by' variable expects the column name by which the 'x' or 'hue' variables should be connected.
    
    It is highly recommended to explicitly pass the 'order' and 'hue_order' arguments to ensure correct plotting.
    
    """
    
    # create a fig an axes if none is provided
    if ax is None:
        fig, ax = plt.subplots()
      
    
    # extract relevant data
    order = order if (order is not None) else data[x].unique()
    ycoords = dict()
    xcoords = dict()

    
    if hue is None:
        for i, x_value in enumerate(order):
            ycoords[x_value] = data[(data[x] == x_value)].sort_values(by=connect_by)[y]
            xcoords[x_value] = rng.uniform(-jitter/2,jitter/2, ycoords[x_value].size) + i
            
    else:      
        
        hue_order = hue_order if (hue_order is not None) else data[hue].unique() 
        
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
                marker=marker,
                color=markercolor if markercolor is not None else palette[color_idx], 
                alpha=markeralpha,
                linewidth=markeredgewidth,
                edgecolor=markeredgecolor,
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
                    zorder=connectorzorder,
                    **kwargs)

   
    else: # if hue is given -> split the scatterd markers into two
    
        # if two markers are given (check if it is a list or np array), one for each hue map them to a dict.
        marker_dict = dict()
        if isinstance(marker, (list, np.ndarray)):            
            for i, hue_value in enumerate(hue_order):
                 marker_dict[hue_value] = marker[i]
        else:
            for i, hue_value in enumerate(hue_order):
                 marker_dict[hue_value] = marker
            
    
        # plot the markers
        for x_value in (order):
            color_idx= 0
            for hue_value in (hue_order):
                ax.scatter(
                    xcoords[x_value][hue_value], ycoords[x_value][hue_value], 
                    s=markersize,  
                    marker=marker_dict[hue_value],
                    color=markercolor if markercolor is not None else palette[color_idx],
                    alpha=markeralpha,
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
