#!/usr/bin/env python

##
## this takes addresses, one per line (like from "to-geocode" output
## of collisions.py) and provides lat/lng for them.
##
## we're using the open.mapquestapi.com batch geocoder which takes 100
## at a time.
##

"http://www.mapquestapi.com/geocoding/v1/address?&key=YOUR-KEY-HERE&location=1555 Blake St,Denver,CO,80202"

from xml.dom import minidom
import requests
import sys

if False:
    print requests.get('http://geocoder.ca',
                       params=dict(addresst='52+ST+NE', stno='1440',
                                   city='calgary', prov='ab', geoit='XML')).text
    sys.exit(0)

def quote(s):
    return s.strip()##.replace(' ', '+')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/24.0'}

with open("to-geocode", "r") as f:
    for line in f.readlines()[10:12]:
        if '&' in line:
            print "intersection", line
            a, b = line.strip().split('&')
            resp = requests.get('http://geocoding.ca', 
                                params=dict(street1=quote(a),
                                            street2=quote(b),
                                            city='Calgary', prov='ab',
                                            geoit='XML'),
                                headers=headers)

        else:
            num, rest = line.split(' ', 1)
            try:
                num = int(num)
                rest = quote(rest)
                resp = requests.get('http://geocoding.ca', 
                                    params=dict(addresst=quote(rest), stno=str(num),
                                                city='calgary', prov='ab', geoit='XML'),
                                    headers=headers)
            except ValueError:
                addr = urllib2.quote(line.strip())
                resp = requests.get('http://geocoding.ca', 
                                    params=dict(addresst=rest, stno=str(num),
                                                city='calgary', prov='ab', geoit='XML'),
                                    headers=headers)

        if resp.status_code == 200:
            data = resp.text
            print data
            dom = minidom.parseString(data)
            lat = dom.getElementsByTagName('latt')[0].firstChild.wholeText
            lng = dom.getElementsByTagName('longt')[0].firstChild.wholeText

            print line.strip(), lat, lng
        else:
            print "ERROR", resp.status_code, resp.reason, line,
            
