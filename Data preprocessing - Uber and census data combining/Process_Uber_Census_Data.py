
import requests
import bs4
import csv
import sys
import codecs
import time
from datetime import datetime, timedelta
import os
from base64 import decodestring
import re
import json
import zipfile
from geojson import Feature, FeatureCollection, Point
import re
import os
import pyodbc
import time 

import pandas as pd
from shapely.geometry import Point, Polygon

def dictfetchall(cur):
    dataset = cur.fetchall()
    columns = [col[0] for col in cur.description]
    return [
        dict(zip(columns, row))
        for row in dataset
        ]

def GetNYCData():
    df = pd.read_csv('NewYork census data.csv', engine='python')
    print(df)
    return df.to_dict('records')


dbf = []
with open('US Census Tract Shape File.geojson', encoding="utf8") as geojson1:
    poly1_geojson = json.load(geojson1)
    for item in poly1_geojson['features']:
        dbf.append(item)
        #if item['properties']['Dist_name'] == 'Dhaka':
            #dbf.append(item)

print('Total = ', len(dbf))
print(dbf[0]['geometry']['coordinates'][0])
#exit()


censusdb = {}
data = GetNYCData()
for item in data:
    key = item['CensusID']
    censusdb[key] = {'CensusID': key, 'CensusName': item['CensusName'],  'MedianIncomeByPlaceofBirth': item['MedianIncomeByPlaceofBirth'],  'MedianIncome': item['MedianIncome'],  
    'TotalPopulation': item['TotalPopulation'],  'AvgPopulation': item['AvgPopulation'],  'Population5M': item['Population5M'],  'Population45M': item['Population45M'],  
    'Population4M': item['Population4M'],  'Population35M': item['Population35M'],  'Population3M': item['Population3M']}
    

df = pd.read_csv('uber-raw-data-sep14.csv', encoding = "ISO-8859-1", engine='python')
print(df)

for index, row in df.iterrows():
    hour_ = row['Date/Time']
    hour = int(str(hour_).split(':')[1])
    lat = row['Lat']
    longi = row['Lon']
    p1 = Point(longi, lat)

    for elem in dbf:
        try:
            poly = Polygon(elem['geometry']['coordinates'][0])
            if p1.within(poly):
                isfound = 1
                print('Matching: ', lat, ' AND ', longi, censusdb[elem['id']])
                income = float(censusdb[elem['id']]['MedianIncomeByPlaceofBirth'])
                median = float(censusdb[elem['id']]['MedianIncome'])
                population = float(censusdb[elem['id']]['TotalPopulation'])
                avg_population = float(censusdb[elem['id']]['AvgPopulation'])

                population5M = float(censusdb[elem['id']]['Population5M'])
                Population45M = float(censusdb[elem['id']]['Population45M'])
                population4M = float(censusdb[elem['id']]['Population4M'])
                population35M = float(censusdb[elem['id']]['Population35M'])
                population3M = float(censusdb[elem['id']]['Population3M'])

                datarow  = str(hour) +  "," + str(lat) +  "," + str(longi) + "," + str(row['Base']) + "," + str(income) + "," +  str(median) + "," + str(population) + "," + str(avg_population) + "," + str(population5M) + "," + str(Population45M) + "," + str(population4M) + "," + str(population35M) + "," + str(population3M) + "\n"
                file =  open('uber-raw-data-sep14_processed.csv', 'a', encoding="utf8")
                file.write(datarow)
                file.close()
                print(datarow)
                break
        except Exception as e:
            pass



