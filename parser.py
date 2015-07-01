#!/usr/bin/python

import json
import sys
import collections

from head import Head
from tool import Tool

from deck import Deck
from container import Container

from ingredients import Ingredients
from reagent import Reagent

from actions import *
from group import Group
from instructions import Instructions

class Parser:
	'''
	handles the json input and generates the python objects
	corresponding to the head, deck, ingredient, and
	instruction items
	'''
	def __init__(self, rawJson): #send it a raw string of all of the json on instantiation
		self.parsed_json = json.loads(rawJson, object_pairs_hook=collections.OrderedDict) #parse the json into ordered dict

		self.error = self.properlyFormattedInput()
		self.head = None
		self.deck = None
		self.ingredients = None
		self.instructions = None

		if self.error == '': #instantiate the objects if they're there
			self.head = self.parseHead()
			self.deck = self.parseDeck()
			self.ingredients = self.parseIngredients()
			self.insructions = self.parseInstructions()

			self.update() #adds new connects if necessary


	def properlyFormattedInput(self):
		error = '' #pass by default
		if 'head' not in self.parsed_json:
			error += ' - - missing head section'
		if 'deck' not in self.parsed_json:
			error += ' - - missing deck section'
		if 'ingredients' not in self.parsed_json:
			error += ' - - missing ingredients section'
		if 'instructions' not in self.parsed_json:
			error += ' - - missing instructions section'

		return error


	def addInstruction(self, groupNum, instrType):
		if instrType == 'transfer':
			act = Transfer()
		elif instrType == 'distribute':
			act = Distribute()
		elif instrType == 'consolidate':
			act = Consolidate()
		elif instrType == 'mix':
			act = Mix()

		if act is not None:
			self.instructions.groups[groupNum].addAction(act) #add new motion to list


	def addContainer(self, name, kind): #create and add new container to list
		cont = Container(name, kind)
		self.deck.addContainer(cont)


	def addIngredient(self, name, volume, container, location):
		reag = Reagent(name)

		attr = collections.OrderedDict()
		attr['volume'] = volume
		attr['container'] = container
		attr['location'] = location

		reag.addLocation(**attr)
		self.ingredients.addReagent(reag) #add new reagent to list


	def addIngrLocation(self, parent, volume, container, location):
		newLoc = collections.OrderedDict()
		newLoc['volume'] = volume
		newLoc['container'] = container
		newLoc['location'] = location

		reags = self.ingredients.getReagents()
		for reag in reags: #go through list to find proper ingredient
#			print "%s , %s" % (reag.getName, parent)
			if 	reag.getName() == parent:
				reag.addLocation(**newLoc)
				return


	def update(self):
		for tool in self.head.getTools(): # go through tools and check that each has an instructions group
			exists = False
			for group in self.instructions.getGroups():
				if group.getTool() == tool.getName():
					exists = True

			if exists is False: #the section doesn't exist, add a new instruction group for the new tool
				newGroup = Group(self.instructions)
				newGroup.addTool(tool.getName())
				self.instructions.addGroup(newGroup)


	def getHead(self): return self.head
	def getDeck(self): return self.deck
	def getIngredients(self): return self.ingredients
	def getInstructions(self): return self.instructions



	'''
	PARSER METHODS

	These shouldn't be called anywhere but in the parser's instantiation.
	In fact, they should probably be private......
	'''

	def parseHead(self):
		'''
		return a Head object with the the head information stored in it
		'''
		self.head = Head()

		mySection = self.parsed_json['head'] #go to head section of json dict

		for tool in mySection: #this goes through head tool by tool
			toolName = tool
			thisTool = mySection[tool]

			myTool = Tool(toolName) #instantiate new tool with the name

			for key in thisTool: #go through section by keys
				thisItem = thisTool[key]
				if key == 'tool': #found the type
					myTool.setType(thisItem)
				elif key == 'trash-container': #found trash container
					myTool.setTrash(thisItem['container'])
				elif key == 'tip-racks':
					for rack in thisItem: #this is a list
						myTool.addTipRack(rack['container'])
				elif key == 'points':
					for point in thisItem:
						myTool.addPoint(point['f1'], point['f2'])
				else:
					myTool.addAttr(key, thisItem) #add attribute to tool's generic attribute list

			self.head.addTool(myTool) #add new tool to the head

		return self.head #return head object


	def parseDeck(self):
		'''
		return a Deck object with the containers stored
		'''
		self.deck = Deck()

		mySection = self.parsed_json['deck']

		for key in mySection: 
			temp = Container(key, mySection[key]['labware'])
			#make new container with name corresponding to key, type to the labware element
			self.deck.addContainer(temp) #add containter to deck

		return self.deck


	def parseIngredients(self):
		'''
		return ingredients?
		'''
		self.ingredients = Ingredients()

		mySection = self.parsed_json['ingredients']

		for key in mySection:
			section = mySection[key]
			reagent = Reagent(key)
			for location in section:
				locationAttributes = collections.OrderedDict()
				for key in location:
					newAttribute = location[key]
					locationAttributes[key] = newAttribute
				reagent.addLocation(**locationAttributes)
			self.ingredients.addReagent(reagent)

		return self.ingredients


	def parseInstructions(self):
		'''
		return Instructions object with following format

		Instructions:
			Group:
				Command:
					Action
					Action
					Action
				Command:
				Command:
			Group:
			Group:

		where Commands are Transfer, Distribute, Consolidate, Mix
		and Actions are To:From pairs
		'''
		self.instructions = Instructions()

		mySection = self.parsed_json['instructions']

		#had to get creative with the terminology in here.......
		for group in mySection: #loop through each group
			temp = Group(self.instructions)
			temp.addTool(group['tool']) #add the tool to this group
		
			commands = group['groups'] #get the commands list
			for command in commands: #loop through list of commands in group
				for key in command: #loop through in case there are multiple commands
					thisCommand = command[key]

					if key == 'transfer':
						act = Transfer() #instantiate new transfer pointing to parent group
						
						for motion in thisCommand: #loop through transfer motion list
							newMotion = Motion(act) #instantiate new motion with this transfer as parent
							for name in motion: #go through the dict items
								if name == 'from':
									newMotion.addFrom(**motion['from']) #pass references to the dictionary with from arguments
								elif name == 'to':
									newMotion.addTo(**motion['to'])
								else:
									newMotion.addOtherAttribute(name, motion[name])

							act.addMotion(newMotion)

						temp.addAction(act)

					elif key == 'distribute':
						act = Distribute()

						newMotion = Motion(act)

						for name in thisCommand: #go through dict
							if name == 'from':
								newMotion.addFrom(**thisCommand['from']) #pass references to the dictionary with from arguments
							elif name == 'to':
								for toLocation in thisCommand['to']:
#									print toLocation
									newMotion.addTo(**toLocation)
							else:
								newMotion.addOtherAttribute(name, thisCommand[name])
						act.addMotion(newMotion)
						temp.addAction(act)

					elif key == 'consolidate':
						act = Consolidate()
						newMotion = Motion(act)

						for name in thisCommand: #go through dict
							if name == 'from':
								for fromLocation in thisCommand['from']:
									newMotion.addFrom(**fromLocation) #pass references to the dictionary with from arguments
							elif name == 'to':
								newMotion.addTo(**thisCommand['to'])
							else:
								newMotion.addOtherAttribute(name, thisCommand[name])

						act.addMotion(newMotion)
						temp.addAction(act)

					elif key == 'mix':
						act = Mix()

						for motion in thisCommand:
							newMotion = Motion(act)
							for name in motion:
								newMotion.addOtherAttribute(name, motion[name])
							act.addMotion(newMotion)
							
						temp.addAction(act)

			self.instructions.addGroup(temp)

		return self.instructions

