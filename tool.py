#!/usr/bin/python

# Authored by Gordon Hart, June 2015

import collections

class Tool:
	'''
	holds information about the individual tool
	'''
	def __init__(self, _name):
		self.name = _name
		self.tipRacks = []
		self.attributes = collections.OrderedDict() #generic attributes dictionary
		self.points = [] #list of dicts of calibration points

	def setType(self, _type):
		self.type = _type

	def setTrash(self, _trash):
		self.trash = _trash

	def addTipRack(self, _rack):
		self.tipRacks.append(_rack) #add this rack to the list of tip racks

	def addPoint(self, _f1, _f2):
		temp = collections.OrderedDict()
		temp['f1'] = _f1
		temp['f2'] = _f2
		self.points.append(temp)

	def addAttr(self, _key, _item):
		self.attributes[_key] = _item #add to dictionary

	def getName(self): return self.name
	def getType(self): return self.type
	def getTrash(self): return self.trash
	def getTipRacks(self): return self.tipRacks
	def getPoints(self): return self.points
	def getAttr(self): return self.attributes

	def toString(self):
		out = ''
		return out