from collections import OrderedDict
import json

class Info():
	"""
	Top-level Info item holds the attributes that are specified at the head of
	each JSON protocol document.

	MASTER
		|-- INFO
		
	#	"info" : {
	#   "name" : "protocol_name",
	#   "description": "description of protocol",
	#   "create-date": "7/15/2015",
	# 	"version": "2"
	#	"run-notes": "notes"
	#   }
	
	this object holds the key="info" value as a complete python OrderedDict
	"""
			
	def __init__(self, info_section):
		"""
		Initialize with information attributes from 'info' JSON section.
		"""
		
		#this defines what fields the info_section should have and establishes the order
		self.info_section = OrderedDict([('name',None),('description',None),('create-date',None),
			('version',None),('run-notes',None)])
		
		for key in self.info_section.keys():
			if info_section.has_key(key):
				self.info_section[key] = info_section[key]
	
	#note that this rendering does not add "info" prefix
	def render_as_json(self):
		return json.dumps(self.info_section, indent=2)
	
	#editing methods
	
	#currently not used
	# def modify(self, new_dict):
	# 	"""modify for all key:value pairs
	# 	
	# 	new_dict contains all the info attributes, modified or not
	# 	"""
	# 	for key in self.info_section.keys():	#iterate over each attribute key in OrderedDict
	# 		if new_dict.has_key(key):
	# 			self.info_section[key] = new_dict[key]	#change value for each key to new_dict value
				
	def modify_by_key(self, new_dict):
		"""modify for a single key:value pair
		
		
		new_dict has the form {key:value} ex: {'description':'Elisa protocol'}
		1. new_dict is returned from ajax using html id of the form "info-key"  ex: "info-description"
		2. self.info_section[key] is updated using this function
		3. no return message is generated
		
		"""
		try:
			key = new_dict.keys()[0]
			if self.info_section.has_key(key):
				self.info_section[key] =  new_dict[key]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'info' : {key:msg}}	# section temporarily commented pending error response requirement
			pass
