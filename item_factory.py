import os, json
from jinja2 import Environment, PackageLoader, FileSystemLoader
from collections import OrderedDict

class ItemFactory:
	"""
	The ItemFactory class is responsible for generating the HTML for
	new items to be added to the display by internally evaluating Jinja
	HTML templates.
	"""
	def __init__(self):
		# set up jinja environment
		parent_directory = os.path.dirname(os.path.abspath(__file__))
#		print parent_directory
		self.env = Environment(loader=FileSystemLoader('templates'))

		# get resource JSON
		self.resource = 'static/resources/items.json'

		try:
			item_file = open(self.resource, 'r')
			item_lines = item_file.read()
			item_dict = json.loads(item_lines, object_pairs_hook=OrderedDict)
			item_file.close()

			self.items = item_dict # this is where the JSON templates for the new items are held

		except IOError, e:
			self.items = e


	def get_container(self):
		container = self.env.get_template('items/container.html')
		container_html = container.module.draw('Container name', self.items['container']['Container name'])

		return container_html


	def get_reagent(self):
		reagent = self.env.get_template('items/reagent.html')
		reagent_html = reagent.module.draw('Reagent name', self.items['reagent']['Reagent name'])

		return reagent_html


	def get_pipette(self):
		pipette = self.env.get_template('items/pipette.html')
		pipette_html = pipette.module.draw('Reagent name', self.items['reagent']['Reagent name'])

		return pipette_html
