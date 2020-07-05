import time
import requests
import csv

url_base  = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid"

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

with open('gretadata2.csv',encoding='utf-8') as astroin:
    read = csv.reader(astroin, delimiter=',')
    header=astroin.readline()  

    with open('gretaout.csv', 'w', newline='') as csvfile_out:
      my_writer = csv.writer(csvfile_out)

      i = 0
      for row in read:            
        lats = row[11]
        lats = lats.replace("[","") 
        lats = lats.replace("]","")     
        lata = lats.split(', ')
        lat= float(lata[0])+float(lata[1])/60+float(lata[2])/3600     
        lons = row[12]
        lons = lons.replace("[","") 
        lons = lons.replace("]","")     
        lona = lons.split(', ')
        lon= float(lona[0])+float(lona[1])/60+float(lona[2])/3600
        payload = {
         'lat1':lat,
         'lat2':lat,
         'lon1':lon,
         'lon2':lon,
         'magneticComponent':'f',
         'elevation':'400',
         'resultFormat':'json',
         'startMonth': '4',
         'startDay': '21',
         'endMonth': '4', 
         'endDay': '21',
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


