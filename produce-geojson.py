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

for year in years:
    features = []
    i = 0
    for collision in collisions:
        if int(collision.startmonth[:4]) != year:
            continue

        addr = collision.address
        if addr in geocoded:
            lat, lng = geocoded[addr]
            month = collision.startmonth[-2:]
            month = datetime.date(int(year), int(month), 01).strftime('%B')

            desc = 'Address: %s<br />%s <b>%s</b>' % (collision.address, month, year)
            p = geojson.Feature(geometry=geojson.Point((float(lat), float(lng))),
                                properties=dict(name=addr,
                                                description=desc),
                                id=i)

            features.append(p)
            i += 1

    if i > 0:
        with open('processed/collisions-%d.geojson' % year, 'w') as f:
            f.write(geojson.dumps(geojson.FeatureCollection(features)))
