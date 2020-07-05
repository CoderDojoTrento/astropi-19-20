
from matplotlib import pyplot
from csv import reader 
from dateutil import parser
from datetime import datetime
import math

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

with open ('astrovitruvio_data_GOOD.csv', 'r') as input_1
  data_1 = list(reader(input_1, delimiter=';'))

with open ('astroout_4.csv', 'r') as input_2
  data_2 = list(reader(input_2,  delimiter=','))
  
magx_1 = [math.sqrt(float(i[4].replace(',','.'))2+(float(i[5].replace(',','.')))2+(float(i[6].replace(',','.')))2) for i in data_1[1]]

magx_2 = [(float(i[13]))1000 for i in data_2[1]]

def to_datetime(s)
  return datetime.strptime(s, '%d%m%Y %H%M%S')

time_series = [to_datetime(i[0] + ' ' + i[1]) for i in data_1[1]]
pyplot.plot(time_series,magx_1, label='ISS')
pyplot.plot(time_series,magx_2, label='WMM')
pyplot.legend()
pyplot.xlabel('time')
pyplot.xticks([])
pyplot.title('total intensity')
pyplot.ylim(0,100)
pyplot.xlim(to_datetime('09042020 222013'),to_datetime('10042020 011811'))
pyplot.show()

#10042020 011811
#09042020 222013