from info import Info
from deck import Deck
#from head import Head
#from ingredients import Ingredients
#from instructions import Instructions

from collections import OrderedDict
import json


class Master():
	"""
	The Master class can be thought of as the chief of all of the pieces
	necessary to run an experiment.

	Master aggregates and creates the Python object structure corresponding
	to the items and instructions found in the JSON protocol file.
	"""

	def __init__(self, json):
		"""
		Initialize class with the input as a raw (unparsed) JSON-esque string, and create 
		top-level (Head, Deck, Instructions, and Ingredients) items as None objects.
		"""
		self.protocol = json
		self.info, self.deck, self.head, self.ingredients, self.instructions = None, None, None, None, None

		self.display_protocol = OrderedDict() # instantiate empty output protocol dictionary


	def process(self):
		"""
		This function should be called immediately after instantiation of the Master object.

		Parse JSON and Instantiate each of the top-level items pointing to its section.

		If any of the sections is missing, raise a ValueError and return false to stop the
		procession of the program.
		"""
		try:
			self.protocol = json.loads(self.protocol, object_pairs_hook=OrderedDict) # load into ordered dictionary

			if 'info' in self.protocol:
				self.info = Info(self.protocol['info'])
			else: # instantiate blank Information section if it's not in the protocol file
				self.info = Info({ 'info': {} })

			self.deck = Deck(self.protocol['deck'])
#			self.head = Head(self.protocol['head'])
#			self.ingredients = Ingredients(self.protocol['ingredients'])
#			self.instructions = Instructions(self.protocol['instructions'])

		except (ValueError, KeyError) as e: # one of the necessary sections was not there, or the json file was invalid
			print e
			return False