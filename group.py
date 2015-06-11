#!/usr/bin/python

# Authored by Gordon Hart, June 2015

from actions import *

class Group:
	'''
	group of actions
	'''
	def __init__(self, parent):
		self.parentInstructions = parent
		self.actions = []

	def addAction(self, act):
		self.actions.append(act)

	def addTool(self, _tool):
		self.tool = _tool


	def getActions(self): return self.actions
	def getTool(self): return self.tool