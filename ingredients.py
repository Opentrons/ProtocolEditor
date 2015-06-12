#!/usr/bin/python

# Authored by Gordon Hart, June 2015

class Ingredients:
	'''
	holds the ingredient information
	'''

	def __init__(self):
		self.ingrs = [] #make empty ingredient array

	def addIngredient(self, ingredient):
		self.ingrs.append(ingredient)