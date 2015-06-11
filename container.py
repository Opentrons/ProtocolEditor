#!/usr/bin/python

# Authored by Gordon Hart, June 2015

class Container:
	'''
	single container object.

	to be held in the deck class
	'''

	def __init__(self, _name, _type):
		self.name = _name
		self.type = _type

	def getName(self): return self.name
	def getType(self): return self.type

	def toString(self):
		out = "name: %s\ntype: %s\n\n" % (self.name, self.type)
		return out