#!/usr/bin/env python

from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, Response, make_response

from parser import Parser
from outputter import Outputter
from adder import Adder

import collections
import json

app = Flask(__name__) #APPLICATION
app.config.from_object(__name__)

##################
##### ROUTES #####
##################

@app.route('/')
def landing_page():
	return render_template('items.html', fileName="[empty]")


@app.route('/save', methods=['GET', 'POST'])
def save():
	if request.method == 'POST':
		filename = request.form['fileName']
#		time.sleep(1) #in case we want to build in a wait for the download
		out = request.form['hiddenValue'] #this is the JSON

		if(out != 'null'): #only save if there was actually an output
			response = make_response(out)
			response.headers["Content-Disposition"] = "attachment; filename=%s.json" % filename
			return response
		else: 
			return nothing() #intentional blank response

	else: return landing_page()
	

@app.route('/process', methods=['GET', 'POST']) # read data in from the file upload form
def process():
	if request.method == 'POST':
		req = request.files['fileJSON']
		inputJSON = req.getvalue()
		filename = req.filename
		filename = filename[0:len(filename)-5] #cut out the ".json"

		proceed = request.form['proceed'] #get the proceed form value
		if proceed != 'yes':
			return nothing() #do nothing if user cancelled processing the new file

		if inputJSON is not '': #if the input is sucessful (i.e. not empty)
			try:
				p = Parser(inputJSON) #instantiate new parser with the JSON from POST
			except ValueError, e: #instantiating parser will generate error is the JSON object passed is invalid
				return error_page("invalid JSON syntax", filename)

			if p.error != '': #have the parser check if all of the necessary pieces are present
				return error_page(p.error, filename)

			return items_page(p, filename)
		
		else:
			return render_template('nofile.html', fileName="[empty]")
	else:
		return landing_page() #return landing page if the page was refreshed


@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		#these three will be in every form
		inputJSON = request.form['fullJSON'] #the full JSON of existing elements
		filename = request.form['fileName'] #the filename of the current file
		addedJSON = request.form['newJSON'] #the JSON of new element being added
#		print addedJSON

		try:
			p = Parser(inputJSON)
		except ValueError, e:
			return error_page("invalid JSON syntax", filename)

		a = Adder(p, addedJSON)
		return items_page(p, filename)
	else:
		return landing_page()


@app.route('/refresh', methods=['GET', 'POST']) #reloads and rerenders page
def refresh():
	if request.method == 'POST':
		inputJSON = request.form['fullJSON'] #the full JSON of existing elements
		filename = request.form['fileName'] #the filename of the current file

		try:
			p = Parser(inputJSON)
		except ValueError, e:
			return error_page("invalid JSON syntax", filename)

		return items_page(p, filename)
	else:
		return landing_page()

###########################
##### HELPER METHODS ######
###########################

def items_page(parser, filename):
	out = Outputter(parser)
	deckList = out.getDeck()
	headList = out.getHead()
	ingrList = out.getIngredients()
	instrList = out.getInstructions()

	return render_template('items.html', fileName=filename, headList=headList, instrList=instrList, deckList=deckList, ingrList=ingrList)

def error_page(reason, filename):
	message = "%s.json could not be loaded." % filename
	return render_template('warning.html', message=message, reason=reason, fileName='[empty]') 

def confirm_load(): pass
def check_errors(): pass

def nothing():
	return ('', 204)

##################
##### TO RUN #####
##################

if __name__ == '__main__':
	app.run(debug=True, host= '0.0.0.0')
