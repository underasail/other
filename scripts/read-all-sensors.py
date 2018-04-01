#!/usr/bin/python
import os
import time
import logging
from systemd import journal

log = logging.getLogger('read-all-sensors')
log.addHandler(journal.JournaldLogHandler())
log.setLevel(logging.INFO)

sensors = {
    'accel_3d': ['in_accel_x_raw', 'in_accel_y_raw', 'in_accel_z_raw'],
    'gyro_3d': ['in_anglvel_x_raw', 'in_anglvel_y_raw', 
'in_anglvel_z_raw'],
    'als': ['in_illuminance_raw', 'in_intensity_both_raw']
}

i = 0

while i < 1:
    log.info("Reading from sensors (n=" + str(i+1) + ")")
    for dev in os.listdir('/sys/bus/iio/devices'):
        if dev.startswith('iio:device'):
            path = os.path.join('/sys/bus/iio/devices', dev)
            namepath = os.path.join(path, 'name')
            if not os.path.exists(namepath):
                continue
            name = open(namepath, 'r').read().strip()
        
            if name in sensors:
                log.info("Reading from " + name + " sensor")
                files = sensors[name]
                for f in files:
                    fpath = os.path.join(path, f)
                    try:
                        with open(fpath, 'r') as fh:
                            dat = fh.read()
                    except:
                        pass
    i += 1
    #time.sleep(2)

log.info("Sensor reading completed")
