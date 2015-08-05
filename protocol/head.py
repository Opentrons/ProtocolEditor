from collections import OrderedDict
import json

class Head():
	"""
	Top-level head item holds the attributes that are specified at the head of
	each JSON protocol document.

	# "head" : {
	#   "p200" : {
	#     "tool" : "pipette",
	#     "tip-racks" : [
	#       {
	#         "container" : "p200-rack"
	#       }
	#     ],
	#     "trash-container" : {
	#       "container" : "trash"
	#     },
	#     "multi-channel" : true,
	#     "axis" : "a",
	#     "volume" : 250,
	#     "down-plunger-speed" : 300,
	#     "up-plunger-speed" : 500,
	#     "tip-plunge" : 8,
	#     "extra-pull-volume" : 20,
	#     "extra-pull-delay" : 200,
	#     "distribute-percentage" : 0.1,
	#     "points" : [
	#       {
	#         "f1" : 10,
	#         "f2" : 6
	#       },
	#       {
	#         "f1" : 25,
	#         "f2" : 23
	#       },
	#       {
	#         "f1" : 50,
	#         "f2" : 49
	#       },
	#       {
	#         "f1" : 200,
	#         "f2" : 200
	#       }
	#     ]
	#   }
	# }
	
	this object holds the key="head" value as a complete python OrderedDict
	"""

	def __init__(self, head_section):
		"""
		Initialize with information attributes from 'head' JSON section.
		"""
		self.head_section = head_section
		self.attributes = OrderedDict()

		for key in self.head_section:
			self.attributes[key] = self.head_section[key]

	#note that this rendering does not add "head" prefix
	def render_as_json(self):
		return json.dumps(self.head_section, indent=2)
