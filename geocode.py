#!/usr/bin/env python

##
## this takes addresses, one per line (like from "to-geocode" output
## of collisions.py) and provides lat/lng for them in CSV style
## output, like "address, lat, lng"
##
## we're using the open.mapquestapi.com batch geocoder which takes 100
## at a time.
##

"http://www.mapquestapi.com/geocoding/v1/address?&key=YOUR-KEY-HERE&location=1555 Blake St,Denver,CO,80202"

import csv
from xml.dom import minidom
import requests
import sys
import json

mapquest_key = open('seekrit', 'r').read()

if False:
    r = requests.get('http://www.mapquestapi.com/geocoding/v1/address?key=%s&location=1440+52+ST+NE+Calgary,AB' % mapquest_key)

    for r in json.loads(r.text)['results']:
        loc = r['locations'][0]['displayLatLng']
        lat, lng = loc['lat'], loc['lng']
        print lat, lng

    sys.exit(0)


def quote(s):
    return s.strip().replace(' ', '+').replace('&', '&amp;')


def get_lat_lng(line):
    if '&' in line:
        a, b = line.split('&', 1)
        a = a + ',Calgary,AB'
        b = b + ',Calgary,AB'
        r = requests.get('http://www.mapquestapi.com/geocoding/v1/address?key=%s&location=%s' % (mapquest_key, quote(a + ' &amp; ' + b)))
    else:
        r = requests.get('http://www.mapquestapi.com/geocoding/v1/address?key=%s&location=%s' % (mapquest_key, quote(line + ',Calgary,AB')))

    data = json.loads(r.text)
    if len(data['results']) != 1:
        print "DING", data['results']

    for r in data['results']:
        if len(r['locations']) != 1:
            print "BLAM", len(r['locations'])
        loc = r['locations'][0]['displayLatLng']
        lat, lng = loc['lat'], loc['lng']
        return lat, lng
    
    return lat, lng

pre_existing = {}
try:
    with open('geocoded.csv', 'r') as exist_file:
        for (addr, lat, lng) in csv.reader(exist_file):
            pre_existing[addr] = (lat, lng)

except IOError:
    print "nothing pre-existing"

with open('geocoded.csv', 'wa') as outputfile:
    outputcsv = csv.writer(outputfile)
    with open("to-geocode", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line in pre_existing:
                print 'Already have "%s"' % line
                lat, lng = pre_existing[line]

            else:
                print line,
                sys.stdout.flush()
                lat, lng = get_lat_lng(line)
                print lat, lng

            if lat and lng:
                outputcsv.writerow([line, lat, lng])
            else:
                print "OH NOES", lat, lng
