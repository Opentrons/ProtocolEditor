#!/usr/bin/python

# Authored by Gordon Hart, June 2015

class Ingredients:
	'''
	holds the ingredient information
	'''

	def __init__(self):
		self.reagents = [] #make empty ingredient array

	def addReagent(self, _reagent):
		self.reagents.append(_reagent)

	def getReagents(self): return self.reagents