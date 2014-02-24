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

if False:
    r0 = requests.get('http://geocoder.ca',
                       params=dict(addresst='52+ST+NE', stno='1440',
                                   city='calgary', prov='ab', geoit='XML')).text
    print r0
    r1 = requests.get('http://geocoder.ca',
                      params=dict(addresst='16+AV+SE+&+36+ST+SE',# stno='1440',
                                  city='calgary', prov='ab', geoit='XML')).text
    print r1

    sys.exit(0)

def quote(s):
    return s.strip()##.replace(' ', '+')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/24.0'}

def get_lat_lng(line):
    if '&' in line:
        resp = requests.get('http://geocoder.ca',
                            params=dict(addresst=line.replace(' ', '+'),
                                        city='calgary', prov='ab', geoit='XML')).text
    else:
        number, rest = line.split(' ', 1)
        resp = requests.get('http://geocoder.ca',
                            params=dict(addresst=rest.replace(' ', '+'), stno=number,
                                        city='calgary', prov='ab', geoit='XML')).text

    dom = minidom.parseString(resp)
    lat = dom.getElementsByTagName('latt')[0].firstChild.wholeText
    lng = dom.getElementsByTagName('longt')[0].firstChild.wholeText
    
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
        for line in f.readlines()[:500]:
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
