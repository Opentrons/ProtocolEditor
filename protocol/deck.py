from container import Container
from collections import OrderedDict
import json

class Deck():
	"""
	Top-level Deck item holds a list for each of the Containers specified
	in the protocol.

	Deck is a child of the Master class.
	
	# "deck" : {
	# 	"p200-rack" : {
	# 	  "labware" : "tiprack-200ul", 
	# 	  "slot": "A1"
	# 	},
	# 	"trough": {
	# 	  "labware": "trough-12row", 
	# 	  "slot": "C2"
	# 	},
	# 	"plate-1": {
	# 	  "labware": "96-flat", 
	# 	  "slot": "C1"
	# 	},
	# 	"plate-2": {
	# 	  "labware": "96-flat", 
	# 	  "slot": "D1"
	# 	}
	# }
	  
	this object holds the key="deck" value as a complete python OrderedDict
	"""

	def __init__(self, deck_section):
		"""
		Initialize with empty list of containers and its section of the protocol.
		"""
		self.deck_section = deck_section	#this is a possibly unordered dictionary of containers
		self.containers = OrderedDict()		#this will become an ordered dictionary of containers

		self.create_deck()	#this populates the containers ordered dictionary according to some order
		
	def create_deck(self):
		"""
		This function instantiates all container children based off of the information
		passed over in the JSON protocol section.
		"""
		for container_name in self.deck_section:
			#print container_name
			new_container = Container(container_name, self.deck_section[container_name]) # container is responsible for putting itself together
			self.containers[container_name] = new_container # set container in dictionary with its name as the key
			
		#print self.containers

	def occupied_slots(self):
		""" this function returns the number of slots with defined containers
		
		"""
		return len(self.containers.keys())
	
	#note that this rendering does not add "deck" prefix
	def render_as_json(self):
		#return json.dumps(self.containers, indent=2)
		return json.dumps(self.deck_section, indent=2)
	

	#editing methods
	
	#currently not used
	# def delete(self, key):
	# 	"""deletes an item in the deck section
	# 	
	# 	"""
	# 	try:
	# 		if self.deck_section.has_key(key):
	# 			del self.deck_section[key]
	# 		msg = 'OK'
	# 	except Exception as e:
	# 		msg = e.strerror
	# 	finally:
	# 		return {'deck' : {key:msg}}
	
	def delete_by_index(self, idx):
		"""deletes an item in the deck section
		idx is an integer
		1.  idx is returned from ajax using html id of the form "deck-idx"  ex: "deck-3"
		2.  idx is converted into the key of the deck container to be deleted
		3.  the dict for the revised deck_section is returned
		
		"""
		try:
			key = self.deck_section.keys()[idx]		#get the key from the index
			if self.deck_section.has_key(key):
				del self.deck_section[key]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'deck' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def add(self, new_container_dict):
		"""append a container object to the ordered containers dict
		1.  new_container_dict is the container dict containing the new key and attributes
		2.  new_container_dict is of the form {"container_name" : {"labware" : string, "slot" : string}}
		3.  the dict for the revised deck_section is returned
		
		"""
		try:
			name = new_container_dict.keys()[0]
			attr = new_container_dict[name]
			new_container = Container(name, attr)
			self.containers[new_container.name] = new_container
			self.deck_section[name] = attr
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'deck' : {key:msg}}
			return self.render_as_json()
		
	def modify_by_index(self, idx, new_container_dict):
		"""modify a deck container selected by index in the deck_section dict
		idx is an integer
		1.  idx is returned from ajax using html id of the form "deck-idx"  ex: "deck-3"
		2.  idx is converted into the key of the deck container to be modified
		3.  new_container_dict is the container dict containing the new attributes
		4.  new_container_dict is of the form {"container_name" : {"labware" : string, "slot" : string}}
		5.  nothing is returned since the GUI already contains the changes
		
		"""
		try:
			
			
			old_key = self.deck_section.keys()[idx]		#get the old_key from the index
			new_key = new_container_dict.keys()[0]	#get the new key from the new_container_dict
			attr = new_container_dict[new_key]		#get the attributes from the new_container_dict
			if new_key != old_key:
				self.deck_section[new_key] = self.deck_section.pop(old_key)	#change to the new key value
			self.deck_section[new_key] = attr	#set the attributes
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'deck' : {key:msg}}	# section temporarily commented pending error response requirement
			pass
	
