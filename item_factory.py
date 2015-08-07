import os, json
from jinja2 import Environment, PackageLoader, FileSystemLoader
from collections import OrderedDict


def get_html(section, input_json):
	"""
	Takes a section and JSON block and returns the proper HTML for the
	item(s) in question.
	"""
	env = Environment(loader=FileSystemLoader('templates')) # set up template environment
	html_response = ''

	if section == 'deck':
		template = env.get_template('modules/deck.html')
		html_response = template.module.render(input_json)

	return html_response


'''
class ItemFactory:
	"""
	The ItemFactory class is responsible for generating the HTML for
	new items to be added to the display by internally evaluating Jinja
	HTML templates.
	"""
	def __init__(self):
		self.env = Environment(loader=FileSystemLoader('templates')) # set up template environment


	def get_html(self, section, input_json):
		"""
		Takes a section and JSON block and returns the proper HTML for the
		item(s) in question.
		"""
		html_response = ''

		if section == 'deck':
			template = self.env.get_template('modules/deck.html')
			html_response = template.module.render(input_json)

		return html_response
'''