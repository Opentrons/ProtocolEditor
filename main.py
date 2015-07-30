from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, Response, make_response
from flask.ext.cache import Cache

import collections
import json

from protocol.master import Master


# CONFIG ===================================================================================

app = Flask(__name__) #APPLICATION
app.config.from_object(__name__)

app.secret_key = "protocol_editor" # encryption key for session variable, security isn't really an issue

cache = Cache(app, config={'CACHE_TYPE': 'simple'}) # initialize cache to store objects


# ROUTES ===================================================================================

@app.route('/')
def landing_page():
	return render_template('body.html', filename='[empty]')


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
			parsed_protocol = json.loads(input_protocol, object_pairs_hook=collections.OrderedDict)

			filename = get_filename(req.filename)
			return render_template('body.html', protocol=parsed_protocol, filename=filename)
#			master = Master(input_protocol) # instantiate master with the JSON object

#			if master.process() is not False: # Master() will return False if the JSON is not valid
#				print "success"
#				print master
#				return items_page(protocol=master.protocol)
#			else:
#				return error_page(reason="Invalid JSON syntax") # processing master failed, JSON was not valid

#		return error_page(no_file=True)
	else:
		return landing_page() #return landing page if the page was refreshed


# HELPERS ==================================================================================

#def items_page(protocol):
#	return render_template('body.html', protocol=protocol, filename=get_filename())


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


# RUN ======================================================================================

if __name__ == '__main__':
	app.run(debug=True)
