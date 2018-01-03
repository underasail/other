#! /usr/bin/python3

import csv
from matplotlib import pyplot
from matplotlib import patches

station_dict = {}


datafile = '/home/underasail/Downloads/1166240.csv'
with open(datafile, newline='') as f:
    csvreader = csv.reader(f, delimiter = ',', quotechar='"')
    
    header = next(csvreader)
    station = header.index('STATION')
    name = header.index('NAME')
    lat = header.index('LATITUDE')
    long = header.index('LONGITUDE')
    elevation = header.index('ELEVATION')
    date = header.index('DATE')
    Tmax = header.index('TMAX')
    Tmin = header.index('TMIN')
    Tavg = header.index('TAVG')
    # establishes header from first line and creates readable indexes
    
    for row in csvreader:
        if not row[Tmax] or not row[Tmin] or not row[Tavg]:
            pass
        elif row[station] not in station_dict:
            station_dict[row[station]] = [[], [], [], []]
            station_dict[row[station]][0].append(row[date])
            station_dict[row[station]][1].append(int(row[Tmax]))
            station_dict[row[station]][2].append(int(row[Tmin]))
            station_dict[row[station]][3].append(int(row[Tavg]))
        else:
            station_dict[row[station]][0].append(row[date])
            station_dict[row[station]][1].append(int(row[Tmax]))
            station_dict[row[station]][2].append(int(row[Tmin]))
            station_dict[row[station]][3].append(int(row[Tavg]))
        """
        dict structure should be:
        {'station1': [[date1, date2, ...] [Tmax1, Tmax2, ...], 
        [Tmin1, Tmin2, ...], [Tavg1, Tavg2, ...]]}
        """

pyplot.figure(figsize = (250, 20))
pyplot.plot(\
station_dict['USW00012839'][0], station_dict['USW00012839'][1], 'r-', \
station_dict['USW00012839'][0], station_dict['USW00012839'][2], 'b-', \
station_dict['USW00012839'][0], station_dict['USW00012839'][3], 'g-', \
linewidth = 5)
# figure sizing and line plotting
pyplot.title('Miami Air Temperature\n', \
fontsize = '100', weight = 'bold')
pyplot.ylabel('\nTemperature (Fahrenheit)\n', style = 'italic', fontsize = 60)
pyplot.xlabel('\nDate (YYYY-MM-DD)\n', style = 'italic', fontsize = 60)
pyplot.xticks(rotation = 'vertical', fontsize = 15)
pyplot.yticks(fontsize = 20)
# labeling
pyplot.margins(x = 0, y = 0)
pyplot.axvspan('2015-08-01', '2015-12-31', color='yellow', alpha=0.25)
pyplot.axvspan('2016-01-01', '2016-12-31', color='cyan', alpha=0.25)
pyplot.axvspan('2017-01-01', '2017-12-31', color='#FF99FF', alpha=0.25)
ymin, ymax = pyplot.ylim()
pyplot.axhspan(ymin, 50, color='#FF9966', alpha=0.25)
pyplot.axhspan(ymin, 45, color='#FF6633', alpha=0.5)
# margins and highlighting of vertical and horizontal areas
yellow_patch = patches.Patch(color='yellow', \
label='Aug 01, 2015 - Dec 31, 2015')
cyan_patch = patches.Patch(color='cyan', \
label='Jan 01, 2016 - Dec 31, 2016')
pink_patch = patches.Patch(color='#FF99FF', \
label='Jan 01, 2017 - Dec 31, 2017')
legend_1 = pyplot.legend(handles = [yellow_patch, cyan_patch, pink_patch], \
fontsize = 50, loc = 'center left')
ax = pyplot.gca().add_artist(legend_1)
pyplot.legend(['Maximum Daily Temperature', 'Minimum Daily Temperature', \
'Average Daily Temperature'], fontsize = 50, loc = 'lower left')
# multi-legend setup
pyplot.show()

