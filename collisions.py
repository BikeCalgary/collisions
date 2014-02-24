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

def load_collisions(fileobj):
    collisions = []
    bikes = csv.reader(fileobj)
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
    return collisions


if __name__ == '__main__':
    with open('bikecollisions.csv', 'r') as f:
        collisions = load_collisions(f)

    print len(collisions), "collisions"
    print len(filter(lambda x: 'MAJOR' in x.injurylevel, collisions)), "major injuries"
    print len(filter(lambda x: 'NO INJURY' in x.injurylevel, collisions)), "no injuries"

    locations = {}
    quadrants = dict(NW=0, SW=0, NE=0, SE=0)
    addresses = set()
    years = set()
    for c in collisions:
        addresses.add(c.address)
        years.add(int(c.startmonth[:4]))
        if c.address != 'UNKNOWN':
            try:
                quadrants[c.address[-2:]] += 1
            except KeyError:
                quad = c.address.split('&')[0].strip()[-2:]
                try:
                    quadrants[quad] += 1
                except KeyError:
                    print "NO QUADRANT:", c.address
        try:
            locations[c.address] += 1
        except KeyError:
            locations[c.address] = 1
            
    print "unique addresses", len(addresses)
    years = list(years)
    years.sort()
    print "unique years:", years
    with open('to-geocode', 'w') as f:
        for a in addresses:
            f.write(a + '\n')

    locations = locations.items()
    locations.sort(lambda a, b: cmp(a[1], b[1]))
    locations.reverse()
    print "Top ten recurring locatinos:"
    for loc in locations[:10]:
        print "  %s (%d times)" % loc

    print quadrants.items()
