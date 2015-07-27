from collections import OrderedDict

class Container():
	"""
	Second-level Container object. Each container holds its own information about type,
	name, and location.

	Containers are children of the Deck class.
	"""

	def __init__(self, name, info):
		"""
		Initialize with full characteristics.

		"my_name": {
			"labware": "my_type",
			"slot": "my_slot"
		}
		"""
		self.name = name

		self.attributes = OrderedDict()
		for key in info:
			self.attributes[key] = info[key]