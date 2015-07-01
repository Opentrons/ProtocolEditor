#!/usr/bin/python

# Authored by Gordon Hart, June 2015

from motion import Motion

class Action:
	'''
	master class for all actions
	'''
	myType = 'default'

	def __init__(self):
		self.myMotions = []

	def getType(self):
		return self.myType

	def addMotion(self, _motion):
		self.myMotions.append(_motion)

	def getMotions(self): return self.myMotions

######################
##### SUBCLASSES #####
######################

class Transfer(Action):
	'''
	subclass of Action, transfer liquid from loc1 to loc2
	'''
	myType = "transfer"

class Distribute(Action):
	'''
	class for the distribute function
	'''
	myType = "distribute"

class Consolidate(Action):
	'''
	class for the consolidate function
	'''
	myType = "consolidate"

class Mix(Action):
	'''
	class for the mix function
	'''
	myType = "mix"
