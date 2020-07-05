from matplotlib import pyplot
from csv import reader 
from dateutil import parser
from datetime import datetime
import math

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

with open ('gretadata2.csv', 'r') as input_1:
  data_1 = list(reader(input_1, delimiter=','))

magx_1 = [math.sqrt(float(i[5].replace(',','.'))**2
+float(i[6].replace(',','.'))**2+float(i[7].replace(',','.'))**2) for i in data_1[8:]]

with open ('gretaout.csv', 'r') as input_2:
  data_2 = list(reader(input_2,  delimiter=','))
  
magx_2 = [(float(i[4]))/1000 for i in data_2[8:]]

time_series = [i[1] for i in data_1[8:]]

pyplot.plot(time_series,magx_1, label='ISS')
pyplot.plot(time_series,magx_2, label='WMM')
pyplot.legend()
pyplot.ylabel('total intensity (\u03bcT)')
pyplot.xlabel('time')
pyplot.axis([0,830,0,100])
pyplot.xticks([])
pyplot.title('GretaInTheSpace data')
pyplot.show()