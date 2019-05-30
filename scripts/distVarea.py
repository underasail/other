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
plymouth_rock = [41.958205, -70.661860]


with open('states_cords_2.tsv', 'r') as cords_file, \
    open('states_areas.tsv', 'r') as areas_file, \
    open('states_regions_census.tsv', 'r') as regions_file:
    cords_reader = csv.reader(cords_file, delimiter = '\t')
    areas_reader = csv.reader(areas_file, delimiter = '\t')
    regions_reader = csv.reader(regions_file, delimiter = '\t')
    for cords_row, areas_row, regions_row in zip(cords_reader, areas_reader, regions_reader):
        if cords_row[0] == areas_row[0] == regions_row[0]:
            names.append(cords_row[0])
#            dists.append((geopy.distance.vincenty((0, easternmost_long), 
#                                                  (0, cords_row[1])).miles)/100)
            dists.append((geopy.distance.vincenty(plymouth_rock, 
                                                  (cords_row[1], cords_row[2])
                                                  ).miles)/100)
            areas.append(float(areas_row[1])/10000)
            regions.append(regions_row[1])
        else:
            print('Alignment Error')

names = names[:-2]  # remove AK/HI
dists = dists[:-2]
areas = areas[:-2]
regions = regions[:-2]

b, m = polyfit(dists, areas, 1)
#%%

fig = plt.subplots(figsize = (5, 5))
ax = plt.subplot(1, 1, 1)
plt.scatter(dists, areas, color = regions, zorder = 2)
plt.plot(dists, b + m * np.array(dists), '-', color = 'black', zorder = 1)

plt.xlim(0, 27)
plt.ylim(0, 30)

plt.xlabel('Orthodromic Distance from Plymouth Rock\nto State Geographic Center (mi x $10^{2}$)', x = 0.5, fontsize = 12)
plt.ylabel('Land and Water State Area (mi$^2$ x $10^{4}$)', x = 0.5, fontsize = 12)
#plt.title('Things are bigger out west (and Texas)\n', fontweight='bold')
plt.title('Mainland State Area in the US as a Function of\nDistance from Point of Colonization\n', fontweight='bold')

tx_ind = names.index("Texas")
ax.annotate("Texas", xy=(dists[tx_ind] - 0.4, areas[tx_ind]), 
            xytext=(dists[tx_ind] - 6, areas[tx_ind] - 4), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

ri_ind = names.index("Rhode Island")
ax.annotate("Rhode Island", xy=(dists[ri_ind] + 0.4, areas[ri_ind]), 
            xytext=(dists[ri_ind] + 8, areas[ri_ind] + 1.5), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

me_ind = names.index("Maine")
ax.annotate("Maine", xy=(dists[me_ind] + 0.4, areas[me_ind]), 
            xytext=(dists[me_ind] + 1, areas[me_ind] + 4), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

wa_ind = names.index("Washington")
ax.annotate("Washington", xy=(dists[wa_ind] - 0.4, areas[wa_ind]), 
            xytext=(dists[wa_ind] - 10, areas[wa_ind] - 3), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

ca_ind = names.index("California")
ax.annotate("California", xy=(dists[ca_ind] - 0.4, areas[ca_ind]), 
            xytext=(dists[ca_ind] - 8, areas[ca_ind] + 3), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

#ax.annotate('Northeast', xy=(1, 12), xytext=(7, 12),
#            arrowprops={'arrowstyle': '<|-|>'}, color = 'navy')
#ax.annotate('Southwest', xy=(8, 15), xytext=(17, 15),
#            arrowprops={'arrowstyle': '<|-|>'}, color = 'purple')
#ax.annotate('Midwest', xy=(12, 18), xytext=(24, 18),
#            arrowprops={'arrowstyle': '<|-|>'}, color = 'green')
#ax.annotate('Southwest', xy=(22, 21), xytext=(32, 21),
#            arrowprops={'arrowstyle': '<|-|>'}, color = 'firebrick')
#ax.annotate('West', xy=(26, 24), xytext=(33, 24),
#            arrowprops={'arrowstyle': '<|-|>'}, color = 'gold')

NE = mpatches.Patch(color='lightseagreen', label='Northeast')
#SE = mpatches.Patch(color='purple', label='Southeast')
MW = mpatches.Patch(color='green', label='Midwest')
SW = mpatches.Patch(color='firebrick', label='South')
We = mpatches.Patch(color='gold', label='West')

#left_legend = plt.legend(handles = [NE, SE, MW], loc = 'upper left')
#right_legend = plt.legend(handles = [SW, We], loc = 'upper right')
#ax.add_artist(left_legend)
left_legend = plt.legend(handles = [NE, MW, SW, We], loc = 'upper left')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('none')  # Keeps vertical ticks hidden
ax.xaxis.set_ticks_position('none')  # Keeps horizontal ticks hidden on top
plt.savefig('distVarea_plyrock_census.png', 
            bbox_inches = 'tight', format = 'png', dpi = 600)