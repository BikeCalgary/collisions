#!/usr/bin/env python

import csv

## parses the data here (e.g. to replace the codes with the strings)

## this maps a column-name to a hash of code -> string
code_types = {}
codes = csv.reader(open('codes.csv', 'r'))
codes.next()                    # skip header line
for row in codes:
    try:
        code_types[row[0]][int(row[1])] = row[2]
    except KeyError:
        code_types[row[0]] = {int(row[1]): row[2]}

class BikeCollision(object):
    def __init__(self, **kw):
        for (k, v) in kw.iteritems():
            setattr(self, k, v)

    def __str__(self):
        return '<BikeCollision "%s">' % self.injurylevel

collisions = []
bikes = csv.reader(open('bikecollisions.csv', 'r'))
column_names = bikes.next()
for row in bikes:
    kwargs = {}
    for (i, value) in enumerate(row):
        nm = column_names[i]
        if nm in code_types:
            # there's some weird data in the spreadsheet
            # probably using OCR to read faxes or something stupid
            if value == '*1':
                value = code_types[nm][1]
            elif value == '0*':
                value = 'unparsable'
            else:
                try:
                    value = code_types[nm][int(value)]
                except KeyError:
                    print "Can't find %s for %s" % (value, nm)
                    value = 'missing value'
        kwargs[nm.lower()] = value
    collisions.append(BikeCollision(**kwargs))

if False:
    for c in collisions:
        print c
print len(collisions), "collisions"
print len(filter(lambda x: 'MAJOR' in x.injurylevel, collisions)), "major injuries"
print len(filter(lambda x: 'NO INJURY' in x.injurylevel, collisions)), "no injuries"
