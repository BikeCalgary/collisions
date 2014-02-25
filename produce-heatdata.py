#!/usr/bin/env python

## create a KML file from a (possily subset) of the collisions data,
## given a "geocoded" file that is a CSV file consising of "address,
## lat, lng" triples.

import datetime
import csv
import geojson

from collisions import load_collisions

## load the geocoded data we have
geocoded = {}
with open('geocoded.csv', 'r') as f:
    for (addr, lat, lng) in csv.reader(f):
        geocoded[addr] = (lat, lng)

with open('bikecollisions.csv', 'r') as f:
    collisions = load_collisions(f)

print len(collisions), "collisions loaded"

years = set()
for c in collisions:
    years.add(c.startmonth[:4])
years = map(int, list(years))
years.sort()
print "unique years %d -> %d" % (years[0], years[-1])

all_data = {}
for year in years:
    data = {}
    i = 0
    for collision in collisions:
        if int(collision.startmonth[:4]) != year:
            continue

        addr = collision.address
        if addr in geocoded:
            lat, lng = geocoded[addr]
            k = (float(lat), float(lng))
            print k
            try:
                data[k] += 1
            except KeyError:
                data[k] = 1


    with open('heatdata-%d.js' % year, 'w') as f:
        f.write('var the_data = [\n')
        for v in data.items():
            (lat, lng) = v[0]
            count = v[1]
            f.write('{lat: %f, lon: %f, value: %d},\n' % (lat, lng, count*250))
        f.write('];')

    for k, v in data.items():
        try:
            all_data[k] += v
        except KeyError:
            all_data[k] = v

with open('heatdata.js', 'w') as f:
    f.write('var the_data = [\n')
    for v in all_data.items():
        (lat, lng) = v[0]
        count = v[1]
        f.write('{lat: %f, lon: %f, value: %d},\n' % (lat, lng, count*250))
    f.write('];')
