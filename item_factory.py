import os, json
from jinja2 import Environment, PackageLoader, FileSystemLoader
from collections import OrderedDict


def get_html(section, input_json):
	"""
	Utility function that takes a section and JSON block and returns
	the proper HTML for the item(s) in question.
	"""
	env = Environment(loader=FileSystemLoader('templates')) # set up template environment
	html_response = ''

	if section == 'deck':
		template = env.get_template('modules/deck.html')
		html_response = template.module.render(input_json)

	elif section == 'head':
		template = env.get_template('modules/head.html')
		html_response = template.module.render(input_json)

	elif section == 'ingredients':
		template = env.get_template('modules/ingredients.html')
		html_response = template.module.render(input_json)

	elif section == 'instructions':
		template = env.get_template('modules/instructions.html')
		html_response = template.module.render(input_json)

	return html_response

