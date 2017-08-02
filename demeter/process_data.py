# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy import stats

def hist2(x, y, axis_labels=['x', 'y'], bins=100):
    
    plt.xlabel(axis_labels[0])
    plt.ylabel(axis_labels[1])

    plt.hist2d(x, y, bins=bins, cmap='YlGnBu', norm=LogNorm())

    cbar = plt.colorbar()

def calc_statitistic(x, y, statistics, bins=25):
    
    if type(bins) == int:
        bins = np.linspace(x.min(), x.max(), bins)
        
    
    stat = {key: stats.binned_statistic(x, y,
            statistic=statistics[key], bins=bins)[0]
            for key in statistics.keys()}
    
    stat['bins'] = bins
    stat['half_bin'] = (bins[1] - bins[0]) / 2.0
    
    return stat
