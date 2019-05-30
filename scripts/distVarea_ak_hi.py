#! /usr/bin/python3

import csv
import geopy.distance
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from numpy.polynomial.polynomial import polyfit
import numpy as np

names = []
dists = []
areas = []
regions = []
easternmost_long = -66.949778


with open('states_cords.tsv', 'r') as cords_file, \
    open('states_areas.tsv', 'r') as areas_file, \
    open('states_regions.tsv', 'r') as regions_file:
    cords_reader = csv.reader(cords_file, delimiter = '\t')
    areas_reader = csv.reader(areas_file, delimiter = '\t')
    regions_reader = csv.reader(regions_file, delimiter = '\t')
    for cords_row, areas_row, regions_row in zip(cords_reader, areas_reader, regions_reader):
        names.append(cords_row[0])
        dists.append((geopy.distance.vincenty((0, easternmost_long), 
                                              (0, cords_row[1])).miles)/100)
        areas.append(float(areas_row[1])/10000)
        regions.append(regions_row[1])

b, m = polyfit(dists, areas, 1)
#%%

fig = plt.subplots(figsize = (5, 5))
ax = plt.subplot(1, 1, 1)
plt.scatter(dists, areas, color = regions, zorder = 2)
plt.plot(dists, b + m * np.array(dists), '-', color = 'black', zorder = 1)

plt.xlim(0, 100)
plt.ylim(0, 70)

plt.xlabel('Distance from Easternmost Point (mi x $10^{2}$)', x = 0.5, fontsize = 12)
plt.ylabel('Total State Area (mi$^2$ x $10^{4}$)', x = 0.5, fontsize = 12)
plt.title('Things are bigger out west (and Texas)\n', fontweight='bold')

tx_ind = names.index("Texas")
ax.annotate("Texas", xy=(dists[tx_ind] - 0.4, areas[tx_ind]), 
            xytext=(dists[tx_ind] - 8, areas[tx_ind] - 7), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

ri_ind = names.index("Rhode Island")
ax.annotate("Rhode Island", xy=(dists[ri_ind] + 0.4, areas[ri_ind]), 
            xytext=(dists[ri_ind] + 8, areas[ri_ind] + 1.5), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

me_ind = names.index("Maine")
ax.annotate("Maine", xy=(dists[me_ind] + 0.4, areas[me_ind]), 
            xytext=(dists[me_ind] + 1, areas[me_ind] + 8), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

wa_ind = names.index("Washington")
ax.annotate("Washington", xy=(dists[wa_ind] - 0.4, areas[wa_ind]), 
            xytext=(dists[wa_ind] + 10, areas[wa_ind] - 3), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

ca_ind = names.index("California")
ax.annotate("California", xy=(dists[ca_ind] - 0.4, areas[ca_ind]), 
            xytext=(dists[ca_ind] + 7, areas[ca_ind] + 8), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

ak_ind = names.index("Alaska")
ax.annotate("Alaska", xy=(dists[ak_ind] - 0.4, areas[ak_ind]), 
            xytext=(dists[ak_ind] - 14, areas[ak_ind] - 10), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

hi_ind = names.index("Hawaii")
ax.annotate("Hawaii", xy=(dists[hi_ind] - 0.4, areas[hi_ind]), 
            xytext=(dists[hi_ind] - 13, areas[hi_ind] + 8), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

NE = mpatches.Patch(color='navy', label='Northeast')
SE = mpatches.Patch(color='purple', label='Southeast')
MW = mpatches.Patch(color='green', label='Midwest')
SW = mpatches.Patch(color='firebrick', label='Southwest')
We = mpatches.Patch(color='gold', label='West')

#left_legend = plt.legend(handles = [NE, SE, MW], loc = 'upper left')
#right_legend = plt.legend(handles = [SW, We], loc = 'upper right')
#ax.add_artist(left_legend)
left_legend = plt.legend(handles = [NE, SE, MW, SW, We], loc = 'upper left')

#ax.set_xscale('symlog')
#ax.set_yscale('symlog')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('none')  # Keeps vertical ticks hidden
ax.xaxis.set_ticks_position('none')  # Keeps horizontal ticks hidden on top
plt.savefig('distVarea_ak_hi.png', 
            bbox_inches = 'tight', format = 'png', dpi = 600)