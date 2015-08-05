from collections import OrderedDict

class Container():
	"""
	Second-level Container object. Each container holds its own information about type,
	name, and location.
	
	A container consists of a name with two attributes: "labware" and "slot"
	The name is assumed to be unique and serve as a uid

	Containers are children of the Deck class.
	"""

	def __init__(self, name, attr):
		"""
		Initialize with full characteristics.

		"my_name": {
			"labware": "my_type",
			"slot": "my_slot"
		}
		"""
		self.name = name
		self.attributes = attr

		# self.attributes = OrderedDict()
		# for key in attr:
		# 	self.attributes[key] = attr[key]