# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
    
def plot_hist2 (hist, axis_labels=['x', 'y'], lognorm=False):
    
    plt.xlabel(axis_labels[0])
    plt.ylabel(axis_labels[1])
    
    aspect = (hist[1][-1] - hist[1][0]) / (hist[2][-1] - hist[2][0]) * 0.95
    
    if lognorm:
        from matplotlib.colors import LogNorm
        plt.imshow(np.rot90(hist[0]),
        extent=[ hist[1][0], hist[1][-1], hist[2][0], hist[2][-1] ],
        cmap='YlGnBu', norm=LogNorm(), aspect)
    else:
        plt.imshow(np.rot90(hist[0]),
        extent=[ hist[1][0], hist[1][-1], hist[2][0], hist[2][-1] ],
        cmap='YlGnBu', aspect)
        
    cbar = plt.colorbar()

def calc_statitistic (x, y, statistics, bins=25):
    
    if type(bins) == int:
        bins = np.linspace(x.min(), x.max(), bins)
    
    stat = {key: stats.binned_statistic(x, y,
            statistic=statistics[key], bins=bins)[0]
            for key in statistics.keys()}
    
    stat['bins'] = bins
    stat['half_bin'] = (bins[1] - bins[0]) / 2.0
    
    return stat

def plot_statistic (stat, attribute='mean', shaded=None,
                    color='b', alpha=0.5):
    
    plt.plot(stat['bins'][:-1] + stat['half_bin'], stat[attribute], 
    'k-', linewidth=2.5)
    
    if shaded:
        plt.fill_between(stat['bins'][:-1] + stat['half_bin'],
                 stat[attribute] - stat[shaded],
                 stat[attribute] + stat[shaded],
                 facecolor=color, alpha=alpha)
