#!/usr/bin/python

# Authored by Gordon Hart, June 2015

from container import Container

class Deck:
	'''
	holds the information about containers on the deck
	'''

	def __init__(self):
		self.containers = []

	def addContainer(self, cont):
		self.containers.append(cont) # add container to end of list

	def getContainers(self):
		return self.containers

	def toString(self):
		out = ""
		for cont in self.containers:
			out = out + cont.toString()
		return out
