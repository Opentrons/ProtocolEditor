#!/usr/bin/python

import json
import sys

from head import Head
from tool import Tool

from deck import Deck
from container import Container

from ingredients import Ingredients

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
		self.parsed_json = json.loads(rawJson) #parse the json

	def parseHead(self):
		'''
		return a Head object with the the head information stored in it
		'''
		myHead = Head()

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

			myHead.addTool(myTool) #add new tool to the head

		return myHead #return head object


	def parseDeck(self):
		'''
		return a Deck object with the containers stored
		'''
		myDeck = Deck()

		mySection = self.parsed_json['deck']

		for key in mySection: 
			temp = Container(key, mySection[key]['labware'])
			#make new container with name corresponding to key, type to the labware element
			myDeck.addContainer(temp) #add containter to deck

		return myDeck


	def parseIngredients(self):
		'''
		return ingredients?
		'''
		myIngredients = Ingredients()
		return myIngredients

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
		myInstructions = Instructions()

		mySection = self.parsed_json['instructions']

		#had to get creative with the terminology in here.......
		for group in mySection: #loop through each group
			temp = Group(myInstructions)
			temp.addTool(group['tool']) #add the tool to this group
		
			commands = group['groups'] #get the commands list
			for command in commands: #loop through list of commands in group
				for key in command: #loop through in case there are multiple commands
					thisCommand = command[key]

					if key == 'transfer':
						act = Transfer(temp) #instantiate new transfer pointing to parent group
						
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
						act = Distribute(temp)

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
						act = Consolidate(temp)
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
						act = Mix(temp)

						for motion in thisCommand:
							newMotion = Motion(act)
							for name in motion:
								newMotion.addOtherAttribute(name, motion[name])
							act.addMotion(newMotion)
							
						temp.addAction(act)

			myInstructions.addGroup(temp)

		return myInstructions



