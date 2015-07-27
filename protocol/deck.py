from container import Container
from collections import OrderedDict

class Deck():
	"""
	Top-level Deck item holds a list for each of the Containers specified
	in the protocol.

	Deck is a child of the Master class.
	"""

	def __init__(self, json):
		"""
		Initialize with empty list of containers and its section of the protocol.
		"""
		self.json_section = json
		self.containers = OrderedDict()

		self.create_deck()


	def create_deck(self):
		"""
		This function instantiates all container children based off of the information
		passed over in the JSON protocol section.
		"""
		for container_name in self.json_section:
			new_container = Container(container_name, self.json_section[container_name]) # container is responsible for putting itself together
			self.containers[container_name] = new_container # set contiainer in dictionary with its name as the key

