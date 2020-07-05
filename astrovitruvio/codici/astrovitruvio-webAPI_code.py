import time
import requests
import csv

url_base  = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid"

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

with open('astrovitruvio_data_GOOD.csv',encoding='utf-8') as astroin:
    read = csv.reader(astroin, delimiter=',')
    header=astroin.readline()  

    with open('astroout_4.csv', 'w', newline='') as csvfile_out:
      my_writer = csv.writer(csvfile_out)

      i = 0
      for row in read:            
        lats = row[2]
        lon = row[3]
        payload = {
         'lat1':lat,
         'lon1':lon,
         'magneticComponent':'f',
         'elevation':'400',
         'resultFormat':'json',
         'startMonth': '4',
         'startDay': '10',
         'endMonth': '4', 
         'endDay': '10',
          }
        r = requests.get(url_base, params=payload)
        diz = r.json()['result'][0]
        if i == 0:
          my_writer.writerow(sorted(diz.keys()))
        i += 1
        lista = [diz[x] for x in sorted(diz.keys())]
        pprint(lista)
        my_writer.writerow(lista)

        time.sleep(0.1)        
