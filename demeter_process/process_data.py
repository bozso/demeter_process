# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def plot_hist2 (hist, axis_labels=['x', 'y'], lognorm=False, colorbar_label='Count', aspect_ratio=0.95, cmap='YlGnBu'):
    
    plt.xlabel(axis_labels[0])
    plt.ylabel(axis_labels[1])
    
    aspect = (hist[1][-1] - hist[1][0]) / (hist[2][-1] - hist[2][0]) * aspect_ratio
    
    if lognorm:
        from matplotlib.colors import LogNorm
        plt.imshow(np.rot90(hist[0]),
                   extent=[ hist[1][0], hist[1][-1], hist[2][0], hist[2][-1] ],
                   cmap=cmap, aspect=aspect, norm=LogNorm(), interpolation=None)
    else:
        plt.imshow(np.rot90(hist[0]),
                   extent=[ hist[1][0], hist[1][-1], hist[2][0], hist[2][-1] ],
                   cmap=cmap, aspect=aspect, interpolation=None)
    
    cbar = plt.colorbar()
    cbar.set_label(colorbar_label)

def calc_statitistic (x, y, statistics, bins=25):
    
    if type(bins) == int:
        bins = np.linspace(x.min(), x.max(), bins)
    
    stat = {key: stats.binned_statistic(x, y,
            statistic=statistics[key], bins=bins)[0]
            for key in statistics.keys()}
    
    stat['bins'] = bins
    stat['half_bin'] = (bins[1] - bins[0]) / 2.0
    
    return stat

def plot_statistic (stat, attribute='mean', err_bar=None, **kwargs):
    
    if 'fmt' not in kwargs.keys():
        kwargs['fmt'] = 'o'
    if 'color' not in kwargs.keys():
        kwargs['color'] = 'r'
    if 'c' not in kwargs.keys():
        kwargs['c'] = 'r'
        
    if np.any(err_bar):
        plt.errorbar(get_bin_centers(stat), stat[attribute],
                     xerr=stat['half_bin'], yerr=err_bar, **kwargs)
    else:
        plt.errorbar(get_bin_centers(stat), stat[attribute],
                     xerr=stat['half_bin'], **kwargs)

def get_bin_centers (stat):
    
    return stat['bins'][:-1] + stat['half_bin']

def poly_corr (filepath, x, fun=None):
    
    z = np.load(filepath)
    
    corr = np.polyval(z, x[~np.isnan(x)])
    
    if fun:
        return fun(corr)
    else:
        return corr

def interpol_corr (filepath, x, fun=None):
    
    xy = np.load(filepath)
    
    if xy.shape[0] == 2:
        corr = np.interp(x, xy[0,:], xy[1,:])
    elif xy.shape[1] == 2:
        corr = np.interp(x, xy[:,1], xy[:,1])
    else:
        print('{0} must contain a numpy array that has the shape of'
              '(:,2) or (:,2)'.format(filepath))
        return
    
    if fun:
        return fun(corr)
    else:
        return corr

remove_nan = lambda x: x[~np.isnan(x)]

def calc_dist(x, y, a, b):

    """
    Calculates the distance of points x,y from the line defined by
    the equation: y = ax + b
    """

    from math import sqrt

    return np.abs(a * x - y + b) / sqrt(a * a + 1)