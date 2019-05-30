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
#plymouth_rock = [41.958205, -70.661860]
port_royal_historic_site = [44.710825, -65.609631]


with open('can_cords.tsv', 'r') as cords_file, \
    open('can_areas.tsv', 'r') as areas_file, \
    open('can_regions.tsv', 'r') as regions_file:
    cords_reader = csv.reader(cords_file, delimiter = '\t')
    areas_reader = csv.reader(areas_file, delimiter = '\t')
    regions_reader = csv.reader(regions_file, delimiter = '\t')
    for cords_row, areas_row, regions_row in zip(cords_reader, areas_reader, regions_reader):
        if cords_row[0] == areas_row[0] == regions_row[0]:
            name = cords_row[0]
            names.append(name)
#            dists.append((geopy.distance.vincenty((0, easternmost_long), 
#                                                  (0, cords_row[1])).miles)/100)
            lat = cords_row[1:4]
            lon = cords_row[5:8]
            lat_dec = float(lat[0].rstrip('Â°')) + \
                      float(lat[1].rstrip('â€²'))/60 + \
                      float(lat[2].rstrip('â€³'))/3600
            lon_dec = float(lon[0].rstrip('Â°')) + \
                      float(lon[1].rstrip('â€²'))/60 + \
                      float(lon[2].rstrip('â€³'))/3600
            dists.append((geopy.distance.vincenty(port_royal_historic_site, 
                                                  (lat_dec, -lon_dec)
                                                  ).km)/100)
            areas.append(float(areas_row[1])/10000)
            regions.append(regions_row[1])
        else:
            print('Alignment Error')

#names = names[:-2]  # remove AK/HI
#dists = dists[:-2]
#areas = areas[:-2]
#regions = regions[:-2]

b, m = polyfit(dists, areas, 1)
#%%

fig = plt.subplots(figsize = (5, 5))
ax = plt.subplot(1, 1, 1)
plt.scatter(dists, areas, color = regions, zorder = 2)
plt.plot(dists, b + m * np.array(dists), '-', color = 'black', zorder = 1)

plt.xlim(0, 50)
plt.ylim(0, 215)

plt.xlabel('Orthodromic Distance from Port-Royal to\nProvince/Territory Geographic Center (km x $10^{2}$)', x = 0.5, fontsize = 12)
plt.ylabel('Total Province/Territory Area (km$^2$ x $10^{4}$)', x = 0.5, fontsize = 12)
#plt.title('Things are bigger out west (and Texas)\n', fontweight='bold')
plt.title('Province/Territory Area in Canada as a Function of\nDistance from Point of Colonization\n', fontweight='bold')

nu_ind = names.index("Nunavut")
ax.annotate("Nunavut", xy=(dists[nu_ind] + 0.4, areas[nu_ind]), 
            xytext=(dists[nu_ind] + 8, areas[nu_ind] - 14), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

yu_ind = names.index("Yukon")
ax.annotate("Yukon", xy=(dists[yu_ind] - 0.4, areas[yu_ind]), 
            xytext=(dists[yu_ind] - 14, areas[yu_ind] - 15), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

pe_ind = names.index("Prince Edward Island")
ax.annotate("Prince Edward Island", xy=(dists[pe_ind] + 0.4, areas[pe_ind]), 
            xytext=(dists[pe_ind] + 5, areas[pe_ind] + 17), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

on_ind = names.index("Ontario")
ax.annotate("Ontario", xy=(dists[on_ind] - 0.4, areas[on_ind]), 
            xytext=(dists[on_ind] - 10, areas[on_ind] - 15), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))

qu_ind = names.index("Quebec")
ax.annotate("Quebec", xy=(dists[qu_ind] + 0.4, areas[qu_ind]), 
            xytext=(dists[qu_ind] + 4, areas[qu_ind] - 15), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3"))


We = mpatches.Patch(color='gold', label='Western Region')
CA = mpatches.Patch(color='firebrick', label='Central/Arctic Region')
At = mpatches.Patch(color='green', label='Atlantic Region')

#left_legend = plt.legend(handles = [NE, SE, MW], loc = 'upper left')
#right_legend = plt.legend(handles = [SW, We], loc = 'upper right')
#ax.add_artist(left_legend)
left_legend = plt.legend(handles = [We, CA, At], loc = 'upper left')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('none')  # Keeps vertical ticks hidden
ax.xaxis.set_ticks_position('none')  # Keeps horizontal ticks hidden on top
plt.savefig('distVarea_can.png', bbox_inches = 'tight', format = 'png', 
            dpi = 600)