#!/usr/bin/python

# Authored by Gordon Hart, June 2015

from group import Group

class Instructions:

	def __init__(self):
		self.groups = [] #instructions has list of groups

	def addGroup(self, group):
		self.groups.append(group) #add group to list

	def getGroups(self): return self.groups

	def toString(self):
		out = ""

		for group in self.groups:
			for action in group.actions:
				out = out + action.toString()

		return out