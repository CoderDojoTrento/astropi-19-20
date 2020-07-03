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

# Connect to the Sense Hat
sense = SenseHat()
sense.lowlight=True

# Set a logfile name
logfile(dir_path + "/uranoteam.log")

# Please update the TLE
name = "ISS (ZARYA)"
l1 = "1 25544U 98067A   20044.32408565  .00002939  00000-0  61158-4 0  9991"
l2 = "2 25544  51.6434 246.2798 0004853 268.2335  74.4275 15.49164447212652"
iss = readtle(name, l1, l2)
iss.compute()

# Set up camera
camera = PiCamera()
camera.resolution = (2592, 1944)

def create_csv_file(data_file): #This function creates the uranoteam.csv file and adds the header row
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date","Time","Iteration", "Humidity", "Temperature","Latitude","Longitude","Height", "Pitch", "Roll", "Yaw", "AccelerometerX", "AccelerometerY", "AccelerometerZ")
        writer.writerow(header)

def add_csv_data(data_file, data): #This functions adds data to the uranoteam.csv file
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_latlon():
    """
    A function to write lat/long to EXIF data for photographs.
    Returns (lat, long)
    """
    iss.compute() # Get the lat/long values from ephem
    long_value = [float(i) for i in str(iss.sublong).split(":")]
    if long_value[0] < 0:
        long_value[0] = abs(long_value[0])
        camera.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        camera.exif_tags['GPS.GPSLongitudeRef'] = "E"
    camera.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2]*10)
    lat_value = [float(i) for i in str(iss.sublat).split(":")]
    if lat_value[0] < 0:
        lat_value[0] = abs(lat_value[0])
        camera.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        camera.exif_tags['GPS.GPSLatitudeRef'] = "N"
    camera.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2]*10)
    return (iss.sublat / degree, iss.sublong / degree)

# initialise the CSV file
data_file = dir_path + "/uranoteam.csv"
create_csv_file(data_file)
# store the start time
start_time = datetime.now()
# store the current time
now_time = datetime.now()
photo_counter=1
while (now_time < start_time + timedelta(minutes=178)):
    try:
        logger.info("{} iteration {}".format(datetime.now(), photo_counter))
        sense.clear(0,0,0)
        sense.set_pixel(photo_counter%8,0, (0,100,0))
        humidity = round(sense.humidity, 4)
        temperature = round(sense.temperature, 4)
        #Gets accelerometer's, gyroscope's and height's data once every 2 seconds
        for i in range(0,6):
            sense.set_pixel(i,1, (0,100,0))
            logger.info("{} various data {}".format(datetime.now(), i))
            #get accelerometer's data
            acceleration = sense.get_accelerometer_raw()
            accX = acceleration['x']
            accY = acceleration['y']
            accZ = acceleration['z']
            #get gyroscope's data
            o = sense.get_orientation()
            pitch = o["pitch"]
            roll = o["roll"]
            yaw = o["yaw"]
            # get latitude and longitude
            lat, lon = get_latlon()
            # get the height
            elev=iss.elevation
            # Save the data to the file
            data = (datetime.now(), photo_counter, humidity, temperature, lat, lon, elev, pitch, roll, yaw, accX, accY, accZ)
            add_csv_data(data_file, data)
            sleep(1.9)
        #Take a photo
        camera.capture(dir_path + "/foto_" + str(photo_counter).zfill(3) + ".jpg")
        photo_counter += 1
        # update the current time
        now_time = datetime.now()
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))