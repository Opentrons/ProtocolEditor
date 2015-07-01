#!/usr/bin/python

import collections

class Motion:
	'''
	helper class for the sub-objects called "motions"
	that each transfer is comprised of one or more of 
	'''
	def __init__(self, _parent):
		self.parent = _parent
		self.fromAttr = []
		self.toAttr = []
		self.otherAttr = collections.OrderedDict()

	def addFrom(self, **kwargs):
		fromAttributes = collections.OrderedDict()
		for key, value in kwargs.iteritems():
			fromAttributes[key] = value
		self.fromAttr.append(fromAttributes) #fromAttr is a list of locations/corresponding attributes
	
	def addTo(self, **kwargs):
		toAttributes = collections.OrderedDict()
		for key, value in kwargs.iteritems():
			toAttributes[key] = value
		self.toAttr.append(toAttributes)

	def addOtherAttribute(self, _otherKey, _otherValue):
		self.otherAttr[_otherKey] = _otherValue

	def getAttributes(self):
		'''
		returns a dictionary of all of the attributes for this motion
		'''
		out = collections.OrderedDict()
		out['from'] = self.fromAttr
		out['to'] = self.toAttr
		out['other'] = self.otherAttr
		return out