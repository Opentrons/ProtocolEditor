from flask import Flask, request, session, jsonify, redirect, url_for, abort, render_template, flash, Response, make_response
from flask.ext.cache import Cache

from collections import OrderedDict
import json

from protocol.protocol import Protocol
from item_factory import ItemFactory


# CONFIG ===================================================================================

app = Flask(__name__) #APPLICATION
app.config.from_object(__name__)

app.secret_key = "protocol_editor" # encryption key for session variable, security isn't really an issue

# configure Jinja template engine
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.lstrip_blocks = True # strip the whitespace from jinja template lines
app.jinja_env.trim_blocks = True

cache = Cache(app, config={'CACHE_TYPE': 'simple'}) # initialize cache to store objects


# ROUTES ===================================================================================

@app.route('/')
def landing_page():
	return render_template('body.html', filename='[empty]')


@app.route('/save', methods=['GET', 'POST'])
def save_file():
	"""
	Retrieve the JSON from the Protocol object and stream it directly onto 
	the user's computer.
	"""
	m = cache.get('master') # get the protocol from the cache

	filename = request.form['filename'] # get the filename from the submitted form

	out = m.get_protocol() # get the JSON from the protocol object 

	response = make_response(out)
	response.headers["Content-Disposition"] = "attachment; filename=%s.json" % filename 

	cache.set('master', m) # put the protocol object back into the cache
	return response # stream the object back to the user's computer


@app.route('/process', methods=['GET', 'POST'])
def process_file():
	"""
	This route is called upon loading of a NEW protocol file.

	It instantiantiates the Master protocol object and will return a filled-out
	HTML form with the protocol's information if the input is valid, otherwise 
	returning a warning error message.
	"""
	if request.method == 'POST':
		req = request.files['protocol'] # get file from POST

		if req.filename != '': # a file has been uploaded
			input_protocol = req.getvalue() # raw text of JSON
			parsed_protocol = json.loads(input_protocol, object_pairs_hook=OrderedDict)

			filename = get_filename(req.filename)

			master = Protocol(parsed_protocol) # instantiate the master protocol object 
			cache.set('master', master) # store the protocol object in the cache

			return render_template('body.html', protocol=parsed_protocol, filename=filename)

	else:
		return landing_page() #return landing page if the page was refreshed


@app.route('/edit', methods=['GET', 'POST'])
def make_edit():
	"""
	This function is the point of communications between the client and server 
	side using AJAX as a communications pipeline.

	Returns a response of the new HTML for the section that was edited.
	"""
	m = cache.get('master') # retrieve the protocol object from the cache
	print m.deck.render_as_json()

	changes = request.args.get('changes') # read the changes variable from the postback
	changes = json.loads(changes) # parse changes variable to JSON
	print changes

	protocol_response = m.process_edit_msg(changes) # send the changes back to the protocol module for processing
	protocol_response = m.deck.render_as_json() # shouldn't need to do this--new JSON should come from the process_edit_msg method
	print protocol_response
	print m.deck.render_as_json()

#	if protocol_response is not None: # still need to somehow rerender the deck section
#		i.get_deck()

	cache.set('master', m) # put master back into the cache
	return jsonify(html=str(protocol_response)) # Flask mandates having a return response


@app.route('/add')
def add_item():
	"""
	Function receives a request for a new object of type specified in the AJAX call,
	and returns the HTML of the object to be added.
	"""
	i = ItemFactory()

	new_type = request.args.get('type')

	if new_type == 'container':
		item_html = i.get_container()
	elif new_type == 'reagent':
		item_html = i.get_reagent()
#	elif new_type == 'reagent_location':
#		item_html = i.get_reagent_location()
	elif new_type == 'pipette':
		item_html = i.get_pipette()

#	print item_html
	return jsonify(html=item_html)


# @app.route('/delete')
# def delete_item():
# 	print request.args.get('type')
# 	print request.args.get('id')

# 	return jsonify(test='delete')


# HELPERS ==================================================================================

def error_page(reason="", no_file=False):
	"""
	Return nofile page if no_file is set to true, otherwise return warning page
	with given reason for failure.
	"""
	if no_file:
		return render_template('warnings/nofile.html', fileName=get_filename())

	message = "%s.json could not be loaded." % get_filename()
	return render_template('warnings/warning.html', message=message, reason=reason, fileName=get_filename()) 


def get_filename(filename='[empty]'):
	"""
	Deals with the filename session variable. 
	If a file has not been uploaded successfully, return '[empty]', else returns the filename without extension.
	"""
	if filename != '[empty]':
		filename = filename[0:len(filename)-5]
		session['filename'] = filename

	return filename


def get_defaults():
	defaults_file = open('/static/resources/protocol_defaults.json', 'r')
	defaults_text = defaults_file.read()
	defaults_text.close()

	defaults_json = json.loads(defaults_text, object_pairs_hook=OrderedDict)
	return defaults_json()


# RUN ======================================================================================

if __name__ == '__main__':
	app.run(debug=True)
