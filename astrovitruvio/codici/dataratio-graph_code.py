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

with open ('gretadata2.csv', 'r') as input_3
  data_3 = list(reader(input_3, delimiter=','))

with open ('gretaout.csv', 'r') as input_4
  data_4 = list(reader(input_4,  delimiter=','))


ratio_Astro = []
for i in range(1,len(data_1))
  mag1 = math.sqrt((float(data_1[i][4].replace(',','.')))2+(float(data_1[i][5].replace(',','.')))2+(float(data_1[i][6].replace(',','.')))2)

  ratio_Astro.append((mag1)(float(data_2[i][13]))1000)

ratio_Greta =[]
for i in range(8,len(data_3))
  mag2 = math.sqrt(float(data_3[i][5])2+float(data_3[i][6])2+float(data_3[i][7])2)

  ratio_Greta.append((mag2)(float(data_4[i][4]))1000)

time_astro = []
hline = []
for i in range(1,len(data_1))
  time_astro.append(i)
  hline.append(1)

time_greta = []

for i in range(8,len(data_3))
  time_greta.append((i3412)821)

pyplot.plot(time_greta,ratio_Greta, label='GretaInTheSpace')
pyplot.plot(time_astro,ratio_Astro, label='AstroVtruvio')
pyplot.plot(time_astro,hline,linestyle='dashed',color='k', label='expected ratio')
pyplot.legend()
pyplot.ylabel('ISS  WMM')
pyplot.xlabel('time')
pyplot.xticks([])
pyplot.title('Data Ratio')
pyplot.ylim(0,3)
pyplot.xlim(14,3412)
pyplot.show()
pyplot.show()



