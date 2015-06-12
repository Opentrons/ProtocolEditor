from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, Response, make_response
from parser import Parser
from outputter import Outputter

#APPLICATION
app = Flask(__name__)
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

		jsonOut = Outputter()
		out = jsonOut.getJSON()
	#	filename = "testtest"

		response = make_response(out)
		response.headers["Content-Disposition"] = "attachment; filename=%s.json" % filename
		return response
	else: return landing_page()
		
# read data in from the file upload form
@app.route('/process', methods=['GET', 'POST'])
def process():
	if request.method == 'POST':
		req = request.files['fileJSON']
		inputJSON = req.getvalue()
		filename = req.filename
		filename = filename[0:len(filename)-5] #cut out the ".json"

		if inputJSON is not '':
			p = Parser(inputJSON) #instantiate new parser with the JSON from POST

			### GET DECK ITEMS ###
			deck = p.parseDeck()
			deckItems = deck.getContainers() #get the list of items
			deckList = []
			for deckItem in deckItems:
				temp = dict(name=deckItem.getName(), type=deckItem.getType())
				deckList.append(temp)

			### GET HEAD ITEMS ###
			head = p.parseHead()
			headItems = head.getTools() #get the list of items
			headList = []
			
			for headItem in headItems:
				temp = {}
				temp['attr'] = headItem.getAttr() #get misc attributes dict
				temp['name'] = headItem.getName()
				temp['type'] = headItem.getType()
				temp['trash'] = headItem.getTrash()
				temp['tipRacks'] = headItem.getTipRacks() #there can be multiple tipracks
				headList.append(temp)

			### GET INGREDIENTS ###
			ingr = p.parseIngredients()
			ingrList = []

			### GET INSTRUCTIONS ###
			instructions = p.parseInstructions()
			instrGroups = instructions.getGroups() #get the list of items
			instrList = []

			for group in instrGroups:
				acts = group.getActions()
				temp = dict(tool=group.getTool(), instr=[])

				for act in acts:
					myMoves = act.getMotions()
					moves = []
					for move in myMoves: #loop through motion list
						moveAttr = move.getAttributes()
						moves.append(moveAttr)

					temp['instr'].append(dict(type=act.getType(), moves=moves))

				instrList.append(temp)

			return render_template('items.html', fileName=filename, headList=headList, instrList=instrList, deckList=deckList, ingrList=ingrList)
		
		else:
			return landing_page()
	else:
		return landing_page()



if __name__ == '__main__':
	app.run(debug=True)
