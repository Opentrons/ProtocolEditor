#!/usr/bin/python

class Motion:
	'''
	helper class for the sub-objects called "motions"
	that each transfer is comprised of one or more of 
	'''
	def __init__(self, _parent):
		self.parent = _parent
		self.fromAttr = []
		self.toAttr = []
		self.otherAttr = {}

	def addFrom(self, **kwargs):
		fromAttributes = {}
		for key, value in kwargs.iteritems():
			fromAttributes[key] = value
		self.fromAttr.append(fromAttributes) #fromAttr is a list of locations/corresponding attributes
	
	def addTo(self, **kwargs):
		toAttributes = {}
		for key, value in kwargs.iteritems():
			toAttributes[key] = value
		self.toAttr.append(toAttributes)

	def addOtherAttribute(self, _otherKey, _otherValue):
		self.otherAttr[_otherKey] = _otherValue

#	def setVolume(self, _vol):
#		self.volume = _vol

#	def setBlowout(self, _blowout):
#		self.blowout = _blowout


	def getAttributes(self):
		'''
		returns a dictionary of all of the attributes for this motion
		'''
		out = {}
		out['from'] = self.fromAttr
		out['to'] = self.toAttr
		out['other'] = self.otherAttr
#		out['volume'] = self.volume
#		out['blowout'] = self.blowout
		return out


#	def getFrom(self): return self.fromContainer
#	def getTo(self): return self.toContainer
#	def getVolume(self): return self.volume
#	def getBlowout(self): return self.blowout