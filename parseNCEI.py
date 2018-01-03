#! /usr/bin/python3

import csv
from matplotlib import pyplot

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
        if row[station] not in station_dict:
            station_dict[row[station]] = [[], [], [], []]
            station_dict[row[station]][0].append(row[date])
            station_dict[row[station]][1].append(row[Tmax])
            station_dict[row[station]][2].append(row[Tmin])
            station_dict[row[station]][3].append(row[Tavg])
        else:
            station_dict[row[station]][0].append(row[date])
            station_dict[row[station]][1].append(row[Tmax])
            station_dict[row[station]][2].append(row[Tmin])
            station_dict[row[station]][3].append(row[Tavg])
        """
        dict structure should be:
        {'station1': [[date1, date2, ...] [Tmax1, Tmax2, ...], 
        [Tmin1, Tmin2, ...], [Tavg1, Tavg2, ...]]}
        """

pyplot.figure(figsize = (250, 20))
pyplot.plot(\
station_dict['USW00012839'][0], station_dict['USW00012839'][1], 'b-', \
station_dict['USC00081306'][0], station_dict['USC00081306'][1], 'b-', \
station_dict['USW00092811'][0], station_dict['USW00092811'][1], 'b-', \
station_dict['USC00085667'][0], station_dict['USC00085667'][1], 'b-', \
station_dict['USW00012839'][0], station_dict['USW00012839'][2], 'g-', \
station_dict['USC00081306'][0], station_dict['USC00081306'][2], 'g-', \
station_dict['USW00092811'][0], station_dict['USW00092811'][2], 'g-', \
station_dict['USC00085667'][0], station_dict['USC00085667'][2], 'g-', \
station_dict['USW00012839'][0], station_dict['USW00012839'][3], 'r-', \
station_dict['USC00081306'][0], station_dict['USC00081306'][3], 'r-', \
station_dict['USW00092811'][0], station_dict['USW00092811'][3], 'r-', \
station_dict['USC00085667'][0], station_dict['USC00085667'][3], 'r-' \
)
pyplot.title('Miami Temperature from August 2015 to December 2017\n', \
size = 'x-large', weight = 'bold')
pyplot.ylabel('Temperature (Fahrenheit)', style = 'italic')
pyplot.xlabel('Date', style = 'italic')
pyplot.xticks(rotation = 'vertical')
pyplot.show()



