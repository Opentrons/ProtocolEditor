#!/usr/bin/python

# Authored by Gordon Hart, June 2015

import json
import collections

class Adder:
	'''
	this is a helper class built to allow editor_main to add attributes 
	without having too much knowledge of the inner workings.

	it takes a JSON object corresponding to the new attribute to be added
	and makes moves accordingly

	each method has a corresponding method of the same name in adder.js
	'''
	def __init__(self, _parser, _newJSON):
		self.parser = _parser
		self.newJSON = json.loads(_newJSON, object_pairs_hook=collections.OrderedDict)
		
		#block statement to decide which action to take upon instantiation
		if self.newJSON["type"] == 'container': self.addContainer()
		elif self.newJSON["type"] == 'ingredient': self.addIngredient()
		elif self.newJSON["type"] == 'ingrLocation': self.addIngrLocation()
		elif self.newJSON["type"] == 'head': self.addHeadItem()
		elif self.newJSON["type"] == 'instruction': self.addInstruction()
		elif self.newJSON["type"] == 'motion': self.addMotion()

	def getParser(self): return self.parser

	def addContainer(self):
		name = self.newJSON['name']
		kind = self.newJSON['kind']
		self.parser.addContainer(name, kind)

	def addIngredient(self):
		name = self.newJSON['name']
		volume = self.newJSON['volume']
		container = self.newJSON['container']
		location = self.newJSON['location']
		self.parser.addIngredient(name, volume, container, location)

	def addIngrLocation(self):
		parent = self.newJSON['parent']
		volume = self.newJSON['volume']
		container = self.newJSON['container']
		location = self.newJSON['location']
		self.parser.addIngrLocation(parent, volume, container, location)

	def addHeadItem(self):
		pass

	def addInstruction(self):
		pass

	def addMotion(self):
		pass