#!/usr/bin/python
# coding: utf8

from geocoder.locationiq import LocationIQQuery

class LocationIQReverse(LocationIQQuery):
  provider = 'locationiq'
  method = 'reverse'

if __name__ == '__main__':
  g = LocationIQReverse("45.3, -75.4")
  g.debug()
