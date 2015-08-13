from collections import OrderedDict
import json

class Ingredients():
	"""
	Top-level Ingredients item holds the attributes that are specified at the head of
	each JSON protocol document.

# 	"ingredients" : {
#     "ReagentA": 
#     [
#       {
#         "container": "Reagents-1",
#         "location": "A3",
#         "volume": 25000
#       }
#     ],
# 
#     "ReagentB": 
#     [
#       {
#         "container": "Reagents-1",
#         "location": "A1",
#         "volume": 7000
#       }
#     ],
# 
#     "Standard1": 
#     [
#       {
#         "container": "Standards",
#         "location": "A1",
#         "volume": 125
#       }
#     ]   
#   }	
	
	this object holds the key="ingredients" value as a complete python OrderedDict
	ingredients is a ordered dict of key:value pairs where each value is a list.
	each reagent name (key) must be unique by definition in a dict of this type
	"""

	def __init__(self, ingredients_section):
		"""
		Initialize with information attributes from 'ingredients' JSON section.
		"""
		self.ingredients_section = ingredients_section


	#note that this rendering does not add "ingredients" prefix
	def render_as_json(self):
		return json.dumps(self.ingredients_section, indent=2)
	

	#editing methods
	
	def delete_by_key():
		pass
	
	def delete_by_index(self, idx):
		"""deletes an item in the ingredients section at Level 1
		idx is an integer
		1.  idx is returned from ajax using html id of the form "ingredients-idx"  ex: "ingredients-3"
		2.  idx is converted into the key of the ingredients value/object to be deleted
		3.  the dict for the revised ingredients_section is returned
		
		"""
		try:
			key = self.ingredients_section.keys()[idx]		#get the key from the index
			if self.ingredients_section.has_key(key):
				del self.ingredients_section[key]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			# print 'errmsg=',msg
		finally:
			# return {'ingredients' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def delete_by_index_index(self, idx1, idx2):
		"""deletes an item in the ingredients section at Level 2
		idx1 and idx2 are integers
		1.  idx1 and idx2 are returned from ajax using html id of the form "ingredients.idx1.idx2"  ex: "ingredients.3.1"
		2.  idx1 and id2 are converted into the keys of the corresponding ingredient and ingredient location to be deleted
		3.  the dict for the revised ingredients_section is returned
		
		"""
		try:
			key = self.ingredients_section.keys()[idx1]		#get the key from the index
			if self.ingredients_section.has_key(key):
				del self.ingredients_section[key][idx2]		#delete the dict with index idx2 from the list
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			# print 'errmsg=',msg
		finally:
			# return {'ingredients' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def add(self):
		"""append an ingredient value/object to the ordered ingredients dict at Level 1
		1.  new_ingredient_dict is an OrderedDict of the form:
				{"ingredient_name" : [{"container" : string, "location" : string, "volume":integer}]}
		2.  the dict for the revised ingredients_section is returned
		
		"""
		try:
			
			name = "ingredient_name"
			c = ("container","container_name")
			l = ("location","A1")
			v = ("volume",0)
			new_ingredient_dict = [ OrderedDict([c,l,v]) ]
			self.ingredients_section[name] = new_ingredient_dict
			print self.ingredients_section
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'ingredients' : {key:msg}}	#need error requirments
			return self.render_as_json()
		
		
	def add_by_index(self,idx1):
		"""append an ingredient location object to the list of a specified ingredients at Level 2
		1.  new_ingredient_dict is an OrderedDict of the form:
				{"ingredient_name" : [{"container" : string, "location" : string, "volume":integer}]}
		2.  idx1 is the index of the ingredient in the ingredients dict
		3.  the dict for the entire revised ingredients_section is returned
		
		"""
		try:
			key1 = self.ingredients_section.keys()[idx1]	#get the key for idx1
			#generate a default entry
			c = ("container","container_name")
			l = ("location","A1")
			v = ("volume",0)
			new_ingredient_dict = OrderedDict([c,l,v])
			
			#append the new location dict object to the list
			self.ingredients_section[key1].append(new_ingredient_dict)
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'ingredients' : {key:msg}}	#need error requirments
			return self.render_as_json()
		
	def modify_by_index_index_key(self, idx1, idx2, new_ingredient_dict):
		"""modify an attribute, by name(key2), for an ingredient list element, selected by index idx2,
			for a reagent, selected by index(idx1) in the ingredients_section ordered dict
		1.  new_ingredient_dict is of the form {"key2" : value (string or integer)}
		2.  nothing is returned since the GUI already contains the changes
		
		"""
		try:
			key1 = self.ingredients_section.keys()[idx1]
			key2 = new_ingredient_dict.keys()[0]
			#print "\n\nidx1=",idx1, "  idx2=",idx2, "  key1=",key1,"  key2=", key2
			self.ingredients_section[key1][idx2][key2] = new_ingredient_dict[key2]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'ingredients' : {key:msg}}	# section temporarily commented pending error response requirement
			pass
	

