#!/usr/bin/python

# Authored by Gordon Hart, June 2015

import collections

class Reagent:
	'''
	holds the ingredient information
	'''

	def __init__(self, _name):
		self.name = _name
		self.locations = []

	def addLocation(self, **kwargs):
		locAttributes = collections.OrderedDict()
		for key, value in kwargs.iteritems():
			locAttributes[key] = value
		self.locations.append(locAttributes)

	def getName(self): return self.name
	def getLocations(self): return self.locations