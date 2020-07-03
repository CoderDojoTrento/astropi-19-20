from logzero import logger, logfile
from sense_hat import SenseHat
from ephem import readtle, degree
from datetime import datetime, timedelta
from time import sleep
import random
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

# Connect to the Sense Hat
sense = SenseHat()

# Set the led light to low
sense.low_light = True

# Set a logfile name
logfile(dir_path + "/astrovitruvio.log")

# Latest TLE data for ISS location
# Please update these values with the latest ones before running our program, thank you

name = "ISS (ZARYA)"
l1 = "1 25544U 98067A   19336.91239465 -.00004070  00000-0 -63077-4 0  9991"
l2 = "2 25544  51.6431 244.7958 0006616 354.0287  44.0565 15.50078860201433"
iss = readtle(name, l1, l2)

def create_csv_file(data_file):
    "Create a new CSV file and add the header row"
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "magx", "magy", "magz", "lat", "long", "gpitch", "groll", "gyaw")
        writer.writerow(header)

def add_csv_data(data_file, data):
    "Add a row of data to the data_file CSV"
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_latlon():

    iss.compute() # Get the lat/long values from ephem
    long_value = [float(i) for i in str(iss.sublong).split(":")]
    return (iss.sublat / degree, iss.sublong / degree)

# initialise the CSV file
data_file = dir_path + "/astrovitruvio_data.csv"
create_csv_file(data_file)

# store the start time
start_time = datetime.now()

# store the current time
# (these will be almost the same at the start)
now_time = datetime.now()

while (now_time < start_time + timedelta(minutes=178)):
    try:
        # collect data every 3 seconds
        sleep(3)
        
        # led animation
        sense.clear()
        riga = [0, 0, 0, 0, 0, 0, 0, 0]
        for x in range (0, 8):
            riga[x] = random.randint(1, 7)
        for x in range (0, 8):
            y = 0
            r = random.randint(0, 40)
            g = random.randint(20, 255)
            b = random.randint(20, 255)
            colour = (r, g, b)
            while y < riga[x]+1:
                sense.set_pixel(x, y, colour)
                y += 1
        
        
        logger.info("Data ed ora {}".format(datetime.now()))
        
        # get compass
        craw = sense.get_compass_raw()
        magx = craw['x']
        magy = craw['y']
        magz = craw['z']
        
        # get gyroscope
        graw = sense.get_gyroscope()
        gpitch = graw['pitch']
        groll = graw['roll']
        gyaw = graw['yaw']

        # get latitude and longitude
        lat, lon = get_latlon()

        # Save the data to the file
        data = (datetime.now(), lat, lon, magx, magy, magz, gpitch, groll, gyaw)
        add_csv_data(data_file, data)

        # update the current time
        now_time = datetime.now()

    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))