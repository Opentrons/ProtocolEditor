from collections import OrderedDict

class Info():
	"""
	Top-level Info item holds the attributes that are specified at the head of
	each JSON protocol document.

	MASTER
		|-- INFO
	"""

	def __init__(self, json):
		"""
		Initialize with information attributes from 'info' JSON section.
		"""
		self.json_section = json
		self.attributes = OrderedDict()

		for key in self.json_section:
			self.attributes[key] = self.json_section[key]

