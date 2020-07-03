from logzero import logger, logfile
from sense_hat import SenseHat
from ephem import readtle, degree
from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep
import random
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

# connect to the SenseHat
sh = SenseHat()

# set a logfile name
logfile("%s/gretainthespace.log" % (dir_path))

# please update latest TLE data for ISS location
name = "ISS (ZARYA)"
l1 = "1 25544U 98067A   20044.32408565  .00002939  00000-0  61158-4 0  9991"
l2 = "2 25544  51.6434 246.2798 0004853 268.2335  74.4275 15.49164447212652"
iss = readtle(name, l1, l2)

# set up camera
cam = PiCamera()
cam.resolution = (2544,1696)
cam.start_preview()

def create_csv_file(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Progress", "Temperature", "Humidity", "Magx", "Magy", "Magz",
                  "Pitch", "Roll", "Yaw", "Latitude", "Longitude")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_latlon():
    # get the lat/long values from ephem
    iss.compute()

    long_value = [float(i) for i in str(iss.sublong).split(":")]

    if long_value[0] < 0:
        long_value[0] = abs(long_value[0])
        cam.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        cam.exif_tags['GPS.GPSLongitudeRef'] = "E"
        
    cam.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2]*10)

    lat_value = [float(i) for i in str(iss.sublat).split(":")]

    if lat_value[0] < 0:
        lat_value[0] = abs(lat_value[0])
        cam.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        cam.exif_tags['GPS.GPSLatitudeRef'] = "N"

    cam.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2]*10)
    
    return str(lat_value), str(long_value)

# initialise the CSV file
data_file = "%s/gretadata.csv" % (dir_path)
create_csv_file(data_file)

# store the start time
start_time = datetime.now()

# store the current time
now_time = datetime.now()

photo_counter = 1

while (now_time < start_time + timedelta(minutes=177)):
    try:
        sleep(12)

        logger.info("{} iteration {}".format(datetime.now(), photo_counter))
        
        # get humidity
        hum = round(sh.humidity, 4)
        
        # get temperature
        temp = round(sh.temperature, 4)
        
        # get compass
        compass = sh.get_compass_raw()
        magx = compass["x"]
        magy = compass["y"]
        magz = compass["z"]
        
        # get orientation
        gyroscope = sh.get_gyroscope()
        pitch = gyroscope["pitch"]
        roll = gyroscope["roll"]
        yaw = gyroscope["yaw"]
        
        # get latitude and longitude
        lat, lon = get_latlon()
        
        # save the data to the file
        data = (datetime.now(), photo_counter, hum, temp, magx, magy, magz, pitch, roll, yaw, lat, lon)
        add_csv_data(data_file, data)
        
        # pad the integer value used in filename to 4 digits
        cam.capture("%s/gretaphoto_%s.jpg" % (dir_path, str(photo_counter).zfill(4)))
        
        photo_counter += 1
                
        # update the current time
        now_time = datetime.now()
        
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e)) 