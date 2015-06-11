#!/usr/bin/python

# Authored by Gordon Hart, June 2015

class Head:
	'''
	holds tool information
	'''
	def __init__(self):
		self.tools = [] #empty tool array

	def addTool(self, _tool):
		self.tools.append(_tool)

	def getTools(self):
		return self.tools

	def toString(self):
		out = ""
		return out