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
	"""

	def __init__(self, ingredients_section):
		"""
		Initialize with information attributes from 'ingredients' JSON section.
		"""
		self.ingredients_section = ingredients_section
		self.attributes = OrderedDict()

		for key in self.ingredients_section:
			self.attributes[key] = self.ingredients_section[key]

	#note that this rendering does not add "ingredients" prefix
	def render_as_json(self):
		return json.dumps(self.ingredients_section, indent=2)
