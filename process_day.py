# -*- coding: utf-8 -*-

import demeter.read_data as rd
import demeter.process_data as pr
from os import listdir
import matplotlib.pyplot as plt
from scipy import stats

%matplotlib inline

data_dir = r'/home/istvan/work/demeter/IAP_data/1140/'
input_paths = [data_dir + path for path in listdir(data_dir)]

idx_frac, idx_whole = rd.read_idx(
                        '/home/istvan/work/demeter/geomag_indices/idx')

req = ['cnesjd', 'h', 'mlat', 'mlon', 'alt']
day, _ = rd.read_data(input_paths, required=req)

# half bin width for idx_frac
half_bin_frac = 0.0625

# half bin width for idx_whole
half_bin_whole = 0.5

day = day[(day['h']  < 1.4e4) & (day['h'] > 100) & (day['mlat'] > -60)
           & (day['mlat'] < 60)]


# bin number for H-ion densities
h_binnum = 1e3

# bin number for Phi_m
mlat_binnum = 120

# bin number for CNES Jd.
cnesjd_binnum = 250;


mlat_mean, mlat_bins, _ = stats.binned_statistic(day['mlat'],
                          day['h'], statistic='mean',
                          bins=mlat_binnum)

mlat_half_bin = (mlat_bins[1] - mlat_bins[0]) / 2.0

cnesjd_mean, cnesjd_bins, _ = stats.binned_statistic(day['cnesjd'],
                          day['h'], statistic='mean',
                          bins=cnesjd_binnum)

cnesjd_half_bin = (cnesjd_bins[1] - cnesjd_bins[0]) / 2.0

cnesjd_ap_mean, cnesjd_ap_bins, _ = stats.binned_statistic(day['cnesjd'],
                          day['h'], statistic='mean',
                          bins=cnesjd_binnum)

cnesjd_half_bin = (cnesjd_bins[1] - cnesjd_bins[0]) / 2.0



plt.figure(figsize=(10,8), dpi=100)

pr.hist2(day['mlat'], day['h'],
         axis_labels=[
         r'$\Phi_{\mathrm{m}}$ [deg]', 
         r'$n_{\mathrm{H}}$ [cm-3]'],
         bins=[mlat_binnum, h_binnum])

plt.plot(mlat_bins[0:-1] + mlat_half_bin, mlat_mean, 'k-',
         linewidth=2.5, label='Mean H-ion values')

plt.legend();



fig, ax1 = plt.subplots(figsize=(10,8), dpi=100)

pr.hist2(day['cnesjd'], day['h'],
         axis_labels=[
         'CNES Julian Day', 
         r'$n_{\mathrm{H}}$ [cm-3]'],
         bins=[mlat_binnum, h_binnum])

ax2 = ax1.twinx()

ax1.plot(cnesjd_bins[0:-1] + cnesjd_half_bin, cnesjd_mean, 'k-',
         linewidth=2.5, label='Mean H-ion values')
ax2.plot(idx_frac['cnesjd'] + half_bin_frac,
         idx_frac['ap'], 'r-')

ax2.set_ylabel('Ap index')

plt.legend();
