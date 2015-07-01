#!/usr/bin/python

import collections

class Outputter:
	'''
	this class takes the python class structure and parses it into HTML-ready packets
	'''
	def __init__(self, _parser): 
		'''
		Instantiate with a reference to the Parser object that holds
		the relevant information
		'''
		self.parser = _parser

	def getDeck(self):
		deck = self.parser.getDeck()
		deckItems = deck.getContainers() #get the list of items
		deckList = []
		for deckItem in deckItems:
			temp = dict(name=deckItem.getName(), type=deckItem.getType())
			deckList.append(temp)

		return deckList

	def getHead(self):
		head = self.parser.getHead()
		headItems = head.getTools() #get the list of items
		headList = []
		
		for headItem in headItems:
			temp = collections.OrderedDict()
			temp['attr'] = headItem.getAttr() #get misc attributes dict
			temp['name'] = headItem.getName()
			temp['type'] = headItem.getType()
			temp['trash'] = headItem.getTrash()
			temp['tipRacks'] = headItem.getTipRacks() #there can be multiple tipracks
			temp['points'] = headItem.getPoints()
			headList.append(temp)

		return headList

	def getIngredients(self):
		ingr = self.parser.getIngredients()
		reagentItems = ingr.getReagents()
		ingrList = []

		for reagent in reagentItems: #for reagent in list
			temp = collections.OrderedDict()
			temp['name'] = reagent.getName()
			temp['locs'] = []
			locations = reagent.getLocations()
			for location in locations: #for location in list
				attr = collections.OrderedDict()
				for key in location:
					attr[key] = location[key]
				temp['locs'].append(attr)

			ingrList.append(temp)

		return ingrList

	def getInstructions(self):
		instructions = self.parser.getInstructions()
		instrGroups = instructions.getGroups() #get the list of items
		instrList = []

		for group in instrGroups:
			acts = group.getActions()
			temp = dict(tool=group.getTool(), instr=[])

			for act in acts:
				myMoves = act.getMotions()
				moves = []
				for move in myMoves: #loop through motion list
					moveAttr = move.getAttributes()
					moves.append(moveAttr)

				temp['instr'].append(dict(type=act.getType(), moves=moves))

			instrList.append(temp)
			
		return instrList