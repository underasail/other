from stravalib.client import Client
import urllib.request
import time
import matplotlib.pyplot as plt
from matplotlib import ticker
from sklearn.linear_model import LinearRegression
import numpy as np
import polyline
from os import listdir
from os.path import isfile, join
import gpxpy
from matplotlib import cm
from PIL import Image
from io import BytesIO
from urllib import request
import gmplot
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

m_to_mi = 125/201168
mps_to_mph = 2.236936

client = Client()
client_id = 21059


"""Visit https://www.strava.com/oauth/authorize?client_id=21059&redirect_uri=http://localhost:8282/&response_type=code&scope=activity:read_all
to approve access to activity:read_all scope
Then copy "code" from resulting url. Paste below.
url returned will be in form: http://localhost:8282/?state=&code=6aa803f4673bf84fec2a479e137fae9f1b59b575&scope=read,activity:read_all
Info from: https://stackoverflow.com/questions/52880434/problem-with-access-token-in-strava-api-v3-get-all-athlete-activities/52888659
"""

client_secret=''
code = ''

access_token = client.exchange_code_for_token(client_id = client_id,
                                              client_secret = client_secret,
                                              code = code)

athlete = client.get_athlete()
print("For {id}, I now have an access token {token}".format(id = athlete.id, 
                                                     token = access_token))

#%%

################################################
# Pulling down all Strava activities using API #
################################################


activities = []
total_dist = 0
avg_spds = []
cumm_dists = [0]
dists = [0]
cumm_e_times = [0]
cumm_m_times = [0]
total_m_time = 0
weekly_com = []
week_com = []
week_dates = []
last_activity_wd = 0
i = 0
comm_dist = 0
for activity in client.get_activities(after = "2016-03-14T00:00:00Z"):
    activities.append(activity)
    if activity.type == 'Ride':
        # activity object attributes here :https://pythonhosted.org/stravalib/api.html#stravalib.model.Activity
        # print(activity.distance.__dict__) = {'_num': 5093.0, '_unit': LeafUnit('m', True)}
        miles_dist = activity.distance._num * m_to_mi
        total_dist += miles_dist
        cumm_dists.append(cumm_dists[-1] + miles_dist/1000)
        cumm_e_times.append(cumm_e_times[-1] + activity.elapsed_time.seconds/(60*60*100))
        cumm_m_times.append(cumm_m_times[-1] + activity.moving_time.seconds/(60*60*100))
        dists.append(miles_dist)
        total_m_time += activity.moving_time.seconds/(60*60*24)
        i += 1
        average_speed = activity.average_speed._num
        if average_speed > 0:
            avg_spds.append(average_speed * mps_to_mph) 
        else:
            pass
        if activity.commute == True:
            if activity.start_date.weekday() == 0 and last_activity_wd != 0:
                week_dates.append(activity.start_date)
                weekly_com.append(sum(week_com))
                week_com = []
            else:
                pass
            week_com.append(miles_dist)
            last_activity_wd = activity.start_date.weekday()
            comm_dist += miles_dist
        else:
            pass
    else:
        pass

dollars_saved = comm_dist / 28 * 3.05

#with open('activities_list.pkl', 'wb') as f:
#    pickle.dump(activities, f, pickle.HIGHEST_PROTOCOL)

#with open('activities_list.pkl', 'rb') as f:
#    activities = pickle.load(f)

print("Total Distance (mi): {0}\n"
      "Average Speed (mph): {1}\n"
      "Gas Money Saved ($): {2}\n".format(round(total_dist, 2), 
                                          round(sum(avg_spds)/i, 2),
                                          round(dollars_saved, 2)))

#%%

fig, ax1 = plt.subplots()

color = 'purple'
ax1.set_xlabel('Rides')
ax1.set_ylabel('Cummulative Distance (mi x $10^{3}$)', color = color)
ax1.plot(range(0, len(cumm_dists)), cumm_dists, color = color, zorder = 10)
ax1.tick_params(axis = 'y', labelcolor = color)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
final_dist = cumm_dists[-1]
total_rides = len(cumm_dists)
ax1.annotate(str(round(final_dist * 1000)) + " miles", xy=(total_rides, final_dist), 
            xytext=(total_rides - 250, final_dist - 1.7), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3,angleA=0,angleB=90"))
plt.ylim(ymin = 0)
plt.xlim(0, len(dists))

ax2 = ax1.twinx()
#ax3 = ax1.twinx()
#
color = 'firebrick'
ax2.set_ylabel('per Ride Distance (mi)', color = color)
ax2.bar(range(0, len(dists)), dists, width = 1.0, color = color, zorder = 2)
ax2.set_ylim(ymin = 0)
#plt.yticks([], [])
f_100_ind = dists.index(max(dists[:100]))
ax2.annotate("1st 100 mile ride", xy=(f_100_ind, dists[f_100_ind]), 
            xytext=(f_100_ind + 75, dists[f_100_ind] + 15), 
            arrowprops=dict(arrowstyle="->", connectionstyle = "angle3,angleA=0,angleB=90"))
ax2.annotate("", xy=(490, 25), xytext=(600, 25), 
             arrowprops=dict(arrowstyle="|-|"))
ax2.annotate("Summer Internship", xy=(545, 30), xytext=(600, 55), 
             arrowprops=dict(arrowstyle="->", connectionstyle = "angle3,angleA=0,angleB=90"))
#ax2.set_ylabel('Cummulative Moving Time (hr x $10^{2}$)', color = color)
#ax2.plot(range(0, len(cumm_m_times)), cumm_m_times, color = color)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
#ax2.spines['right'].set_visible(False)
ax2.tick_params(axis = 'y', labelcolor = color)
#ax2.set_ylim(ymin = 0)
##plt.xlim(xmin = 0)
#
#color = 'tab:green'
#ax3.spines["right"].set_position(("axes", 1.2))
#ax3.spines['top'].set_visible(False)
#ax3.spines['left'].set_visible(False)
#ax3.set_ylabel('Cummulative Elapsed Time (hr x $10^{2}$)', color=color)
#ax3.plot(range(0, len(cumm_e_times)), cumm_e_times, color = color)
#ax3.tick_params(axis = 'y', labelcolor = color)
#ax3.set_ylim(ymin = 0)
##plt.xlim(xmin = 0)

fig.set_size_inches(6, 4)
plt.savefig('ride_distance.svg', bbox_inches = 'tight', format = 'svg')
plt.show()

#%%

fig, ax = plt.subplots()

color = 'purple'
#plt.bar(range(0, len(weekly_com)), weekly_com, width = 0.5)
plt.bar(week_dates, weekly_com, width = 2.0, color = color)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation = 45)

fig.set_size_inches(6, 4)
plt.savefig('weekly_commute_miles.svg', bbox_inches = 'tight', format = 'svg')
plt.show()

#%%

#x = np.array(range(1, len(avg_spds) + 1)).reshape(-1, 1)
#reg = LinearRegression().fit(x, avg_spds)
#modeled_y = reg.predict(x)
#
#plt.plot(x, avg_spds)
#plt.plot(x, modeled_y)

#%%

############################################
## Making heatmap image from API polylines #
############################################
#
## Low res
#
#fig = plt.figure(facecolor = '0.05')
#ax = plt.Axes(fig, [0., 0., 1., 1.], )
#ax.set_aspect('equal')
#ax.set_axis_off()
#fig.add_axes(ax)
#
#llcrnrlat = 25.392981
#llcrnrlon = -80.592667
#urcrnrlon = -80.077994
#urcrnrlat = 26.276087
#center = [25.834533999999998, -80.3353305]
#
#m = Basemap(projection = 'merc', llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat, 
#            llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon, 
#            lat_ts = center[0], resolution = 'f')
#
#i = 0
#for activity in activities:
#    lat = []
#    lon = []
#    try:
#        pl = polyline.decode(activity.map.summary_polyline)
#        for cords in pl:
#            latitude = cords[0]
#            longitude = cords[1]
#            if 26.276087 > latitude > 25.392981 and \
#            -80.077994 > longitude > -80.592667:
#                lat.append(cords[0])
#                lon.append(cords[1])
#        if len(lon) > 1:
#            lon, lat = m(lon, lat)
#            m.plot(lon, lat, color = 'white', lw = 0.075, alpha = 0.2, 
#                   marker = None)
#        else:
#            pass
#    except TypeError:
#        pass
#    i += 1
#    print(i)
#
##m.drawcoastlines(color = 'white')
#m.drawmapboundary(fill_color = '#2a3454')
#m.fillcontinents(color = '#212121', lake_color = '#2a3454')
##plt.show()
#
#plt.gca().set_axis_off()
#plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, 
#                    wspace = 0)
#plt.margins(0, 0)
#plt.gca().xaxis.set_major_locator(ticker.NullLocator())
#plt.gca().yaxis.set_major_locator(ticker.NullLocator())
#
##plt.show()
#filename = 'stravaAnalysis'
#plt.savefig(filename + '_lowres.png', format = 'png', pad_inches = 0, 
#            dpi = 3600, facecolor = fig.get_facecolor(), 
#            bbox_inches = 'tight')
#plt.cla()
#plt.clf()
#plt.close("all")
#
##%%
#Image.MAX_IMAGE_PIXELS = None
#
#im = Image.open(filename + '_lowres.png')
#newimdata = []
#for pixel in im.getdata():
##    print(pixel)
##    if pixel != (105, 105, 105, 255):
##        print(pixel)
#    value = pixel[0]
#    newpixel = ()
#    if pixel == (33, 33, 33, 255) or pixel == (42, 52, 84, 255):
#        newpixel = pixel
##        pass
#    else:
#        for entry in cm.plasma(value):
#            nv = int(entry * 255)
#            newpixel = newpixel + (nv,)
#    newimdata.append(newpixel)
#
#newim = Image.new(im.mode,im.size)
#newim.putdata(newimdata)
#newim.save(filename + '_heatmap_lowres.png')

#%%

######################################################
# Plotting from API polylines on Google Maps in html #
######################################################

#center = [25.861074000000002, -80.289717]
#
#gmap = gmplot.GoogleMapPlotter(center[0], center[1], 10)
#gmap.apikey = ''
#
#for activity in activities:
#    lat = []
#    lon = []
#    try:
#        pl = polyline.decode(activity.map.summary_polyline)
#        for cords in pl:
#            latitude = cords[0]
#            longitude = cords[1]
#            if 26.276087 > latitude > 25.446061 and \
#            -80.077994 > longitude > -80.501440:
#                lat.append(cords[0])
#                lon.append(cords[1])
#    except TypeError:
#        pass
#    gmap.plot(lat, lon, 'black', edge_width = 1.0)
#
#gmap.draw(filename + '.html')

#%%

#################################
# Use streams for raw GPS cords #
#################################

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

llcrnrlat = 25.392981
llcrnrlon = -80.778059
urcrnrlon = -80.077994
urcrnrlat = 26.276087
center = [25.834533999999998, (llcrnrlon + urcrnrlon)/2]

m = Basemap(projection = 'merc', llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat, 
            llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon, lat_ts = center[0], 
            epsg = 2236)

gmap_highres = gmplot.GoogleMapPlotter(center[0], center[1], 10)
gmap_highres.apikey = ''

streams_latlng_woBadGPS = {}
with open('streams_latlng_woBadGPS_dict.pkl', 'rb') as f:
    streams_latlng_woBadGPS = pickle.load(f)

streams_entries = []
for activity in activities:
    if '(Bad GPS)' not in activity.name and activity.map.summary_polyline != None:
        streams_entries.append(activity.id)

max_temps = [0]
i = len(streams_latlng_woBadGPS)
for activity in activities[len(streams_entries) - 1:]:
    time.sleep(1.51)  # 600 requests per 15 min (900 sec/600 req) = 1.5 s/req
#    i += 1
    if '(Bad GPS)' not in activity.name and activity.id not in streams_latlng_woBadGPS.keys():
        lat = []
        lon = []
        num = activity.id
        stream = client.get_activity_streams(num, types = ['latlng', 'temp'], 
                                             resolution = 'high')
        try:
            latlngs = list(stream['latlng'].data)
            streams_latlng_woBadGPS.setdefault(num, []).append(latlngs)
#            streams_latlng_woBadGPS[num] = latlngs
            for cords in latlngs:
                latitude = cords[0]
                longitude = cords[1]
                if 26.276087 > latitude > 25.392981 and \
                -80.077994 > longitude > -80.778059:
                    lat.append(cords[0])
                    lon.append(cords[1])
            if len(lon) > 1:
                lon, lat = m(lon, lat)
            else:
                pass
        except KeyError:  # if only time data
            pass
        except TypeError:  # if no gps data but gps dict available
            pass
        try:
            max_temp = max(stream['temp'].data)
            max_temps.append(max_temp)
        except:
            pass
    else:  # Bad GPS data
        pass
    print(len(activities) - i)
    i += 1

with open('streams_latlng_woBadGPS_dict.pkl', 'wb') as f:
    pickle.dump(streams_latlng_woBadGPS, f, pickle.HIGHEST_PROTOCOL)

print("Streams Dictionary Update Done")


for stream in streams_latlng_woBadGPS:
    lat = []
    lon = []
    try:
        latlngs = streams_latlng_woBadGPS[stream][0]
        for cords in latlngs:
            latitude = cords[0]
            longitude = cords[1]
            if 26.276087 > latitude > 25.392981 and \
            -80.077994 > longitude > -80.778059:
                lat.append(cords[0])
                lon.append(cords[1])
        if len(lon) > 1:
            lon, lat = m(lon, lat)
            m.plot(lon, lat, color = 'blue', lw = 0.075, alpha = 0.05, 
                   marker = None)
            # set alpha to zero for blank background
        else:
            pass
#        gmap_highres.plot(lat, lon, 'black', edge_width = 1.0)
    except KeyError:  # if only time data
        pass
    except TypeError:  # if no gps data but gps dict available
        pass

m.arcgisimage(service = 'Canvas/World_Dark_Gray_Base', xpixels = 3600, 
              ypixels = None, dpi = 3600, verbose = False)

filename = 'stravaAnalysis_Miami'
#filename = 'stravaAnalysis_Miami_black'
# comment out arcisimage lines for black background only
gmap_highres.draw(filename + '_highres.html')

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, 
                    wspace = 0)
plt.margins(0, 0)
plt.gca().xaxis.set_major_locator(ticker.NullLocator())
plt.gca().yaxis.set_major_locator(ticker.NullLocator())

plt.savefig(filename + '_highres.png', format = 'png', pad_inches = 0, 
            dpi = 3600, facecolor = fig.get_facecolor(), 
            bbox_inches = 'tight')
plt.cla()
plt.clf()
plt.close("all")

print("Miami Plot Done")

#%%

##blank = Image.open(filename + '_blank' + '_highres.png')
#blank = Image.open(filename + '_highres.png')
#plot = Image.open(filename + '_black' + '_highres.png')
#
#newimdatablank = []
#for pixel in blank.getdata():
#    value = pixel[2]
#    newpixel = ()
#    if pixel[2] > pixel[1] + 10:
#        newpixel = (0, 0, 0, 255)
#    else:
#        newpixel = pixel
#    newimdatablank.append(newpixel)
#newimblank = Image.new(blank.mode, blank.size)
#newimblank.putdata(newimdatablank)
#newimblank.save(filename + '_blank_highres.png')
#
#blank = Image.open(filename + '_blank' + '_highres.png')
#
#blank = blank.convert('RGBA')
#plot = plot.convert('RGBA')
#
#blend1 = Image.blend(blank, plot, alpha = 0.5)
#im = blend1
#im.save(filename + '_combo_highres.png')
#blend1.show()

#%%

top = cm.get_cmap('plasma', 256)
bottom = cm.get_cmap('plasma', 256)

newcolors = np.vstack((top(np.linspace(0.0, 0.5, 205)),
                       bottom(np.linspace(0.5, 1.0, 51))))
plasma_shift = ListedColormap(newcolors, name='plasma_shift')


Image.MAX_IMAGE_PIXELS = None

im = Image.open(filename + '_highres.png')

#%%

blue_values = []
for pixel in im.getdata():
    value = pixel[2]
    newpixel = ()
    if pixel[2] > pixel[1] + 10:
        blue_values.append(value)

rng = range(0, 257)

blue_values_count = []
for i in rng:
    count = blue_values.count(i)
    blue_values_count.append(count)
    print(i, count)

#%%

fig = plt.subplots(figsize = (9, 4))
plt.subplot(1, 2, 1)
plot = plt.scatter(rng, blue_values_count, c = rng, cmap = cm.plasma)
plt.colorbar(plot)
# plt.ylim(0, 658508)
# plt.xlim(74, 250)

plt.subplot(1, 2, 2)
plot = plt.scatter(rng, blue_values_count, c = rng, cmap = plasma_shift)
plt.colorbar(plot)
# plt.ylim(0, 658508)
# plt.xlim(74, 250)
plt.show()
plt.close('all')

#%%

newimdata = []
min_value = 29
for pixel in im.getdata():
    value = pixel[2]
    newpixel = ()
    if pixel[2] > pixel[1] + 10:
        for entry in cm.plasma(value):
            nv = int(entry * 255)
            newpixel = newpixel + (nv,)
    elif pixel[0] < 50:
        newpixel = (16, 25, 41, 255)  # steelblueish
    else:
        newpixel = (0, 0, 0, 255)
    newimdata.append(newpixel)

newim = Image.new(im.mode, im.size)
newim.putdata(newimdata)
newim.save(filename + '_heatmap_highres.png')

print("Miami Heatmap Done")

#%%

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

llcrnrlat = 29.663265
llcrnrlon = -95.748257
urcrnrlon = -95.319346
urcrnrlat = 29.833552
center = [(llcrnrlat - urcrnrlat)/2 + llcrnrlat, 
          (llcrnrlon - urcrnrlon)/2 + llcrnrlon]

m = Basemap(projection = 'merc', llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat, 
            llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon, lat_ts = center[0], 
            epsg = 2846)

gmap_highres = gmplot.GoogleMapPlotter(center[0], center[1], 10)
gmap_highres.apikey = ''

i = 0
for stream in streams_latlng_woBadGPS:
#    i += 1
    lat = []
    lon = []
    try:
        latlngs = streams_latlng_woBadGPS[stream][0]
        for cords in latlngs:
            latitude = cords[0]
            longitude = cords[1]
            if 29.833552 > latitude > 29.663265 and \
            -95.319346 > longitude > -95.748257:
                lat.append(cords[0])
                lon.append(cords[1])
        if len(lon) > 1:
            lon, lat = m(lon, lat)
            m.plot(lon, lat, color = 'blue', lw = 0.075, alpha = 0.2, 
                   marker = None)
        else:
            pass
        gmap_highres.plot(lat, lon, 'black', edge_width = 1.0)
    except KeyError:  # if only time data
        pass
    except TypeError:  # if no gps data but gps dict available
        pass
#    print(i)

m.arcgisimage(service = 'Canvas/World_Dark_Gray_Base', xpixels = 3600, 
              ypixels = None, dpi = 3600, verbose = False)

filename = 'stravaAnalysis_Houston'
gmap_highres.draw(filename + '_highres.html')

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, 
                    wspace = 0)
plt.margins(0, 0)
plt.gca().xaxis.set_major_locator(ticker.NullLocator())
plt.gca().yaxis.set_major_locator(ticker.NullLocator())

plt.savefig(filename + '_highres.png', format = 'png', pad_inches = 0, 
            dpi = 3600, facecolor = fig.get_facecolor(), 
            bbox_inches = 'tight')
plt.cla()
plt.clf()
plt.close("all")

print("Houston Plot Done")


Image.MAX_IMAGE_PIXELS = None

im = Image.open(filename + '_highres.png')
newimdata = []
for pixel in im.getdata():
    value = pixel[2]
    newpixel = ()
    if pixel[2] > pixel[1] + 10:
        for entry in cm.plasma(value):
            nv = int(entry * 255)
            newpixel = newpixel + (nv,)
    elif pixel[0] < 50:
        newpixel = (16, 25, 41, 255)  # steelblueish
    else:
        newpixel = (0, 0, 0, 255)
    newimdata.append(newpixel)

newim = Image.new(im.mode, im.size)
newim.putdata(newimdata)
newim.save(filename + '_heatmap_highres.png')

print("Houston Heatmap Done")

#%%

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

llcrnrlat = 37.662741
llcrnrlon = -122.607818
urcrnrlon = -122.366769
urcrnrlat = 37.922877
center = [(llcrnrlat - urcrnrlat)/2 + llcrnrlat, 
          (llcrnrlon - urcrnrlon)/2 + llcrnrlon]

m = Basemap(projection = 'merc', llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat, 
            llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon, lat_ts = center[0], 
            epsg = 2846)

gmap_highres = gmplot.GoogleMapPlotter(center[0], center[1], 10)
gmap_highres.apikey = ''

i = 0
for stream in streams_latlng_woBadGPS:
#    i += 1
    lat = []
    lon = []
    try:
        latlngs = streams_latlng_woBadGPS[stream][0]
        for cords in latlngs:
            latitude = cords[0]
            longitude = cords[1]
            if urcrnrlat > latitude > llcrnrlat and \
            urcrnrlon > longitude > llcrnrlon:
                lat.append(cords[0])
                lon.append(cords[1])
        if len(lon) > 1:
            lon, lat = m(lon, lat)
            m.plot(lon, lat, color = 'blue', lw = 0.075, alpha = 0.2, 
                   marker = None)
        else:
            pass
        gmap_highres.plot(lat, lon, 'black', edge_width = 1.0)
    except KeyError:  # if only time data
        pass
    except TypeError:  # if no gps data but gps dict available
        pass
#    print(i)

m.arcgisimage(service = 'Canvas/World_Dark_Gray_Base', xpixels = 3600, 
              ypixels = None, dpi = 3600, verbose = False)

filename = 'stravaAnalysis_SF'
gmap_highres.draw(filename + '_highres.html')

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, 
                    wspace = 0)
plt.margins(0, 0)
plt.gca().xaxis.set_major_locator(ticker.NullLocator())
plt.gca().yaxis.set_major_locator(ticker.NullLocator())

plt.savefig(filename + '_highres.png', format = 'png', pad_inches = 0, 
            dpi = 3600, facecolor = fig.get_facecolor(), 
            bbox_inches = 'tight')
plt.cla()
plt.clf()
plt.close("all")

print("SF Plot Done")


Image.MAX_IMAGE_PIXELS = None

im = Image.open(filename + '_highres.png')
newimdata = []
for pixel in im.getdata():
    value = pixel[2]
    newpixel = ()
    if pixel[2] > pixel[1] + 10:
        for entry in cm.plasma(value):
            nv = int(entry * 255)
            newpixel = newpixel + (nv,)
    elif pixel[0] < 50:
        newpixel = (16, 25, 41, 255)  # steelblueish
    else:
        newpixel = (0, 0, 0, 255)
    newimdata.append(newpixel)

newim = Image.new(im.mode, im.size)
newim.putdata(newimdata)
newim.save(filename + '_heatmap_highres.png')

print("SF Heatmap Done")

#%%

#################
# Download GPXs #
#################

# Won't work; can't authenticate; use streams instead

#folder = 'C:\\Users\\Thompson\\Documents\\strava_gpxs\\'

#for activity in activities:
#    num = str(activity.id)
#    url = 'https://www.strava.com/activities/{0}/export_gpx'.format(num)
#    response = urllib.request.urlopen(url)
#    gpx_filename = "{0}{1}.gpx".format(folder, num)
#    with open(gpx_filename, 'wb') as f:
#        f.write(response.read())
    
        

#%%
#if time.time() > client.token_expires_at:
#    refresh_response = client.refresh_access_token(client_id=1234, client_secret='asdf1234',
#        refresh_token=client.refresh_token)
#    access_token = refresh_response['access_token']
#    refresh_token = refresh_response['refresh_token']
#    expires_at = refresh_response['expires_at']


