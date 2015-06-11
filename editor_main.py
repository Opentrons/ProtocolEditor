from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
#from parser import Parser
from parser_v2 import Parser

#CONFIGURATION
DEBUG = True

#APPLICATION
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def landing_page():
	return render_template('items.html', fileName="[empty]")
		
# read data in from the file upload form
@app.route('/process', methods=['GET', 'POST'])
def process():
	if request.method == 'POST':
		req = request.files['fileJSON']
		inputJSON = req.getvalue()
		fileName = req.filename

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
				temp['attr'] = headItem.getAttr() #get misc attributes dict
				temp['name'] = headItem.getName()
				temp['type'] = headItem.getType()
				temp['trash'] = headItem.getTrash()
#				temp['tipRacks'] = head
				headList.append(temp)

			### GET INGREDIENTS ###
			ingr = p.parseIngredients()
			ingrList = []

			### GET INSTRUCTIONS ###
			instructions = p.parseInstructions()
			instrGroups = instructions.getGroups() #get the list of items
#			print len(instrGroups)
			instrList = []

			for group in instrGroups:
				acts = group.getActions()
				temp = dict(tool=group.getTool(), instr=[])
				
#				print len(acts)
#				print acts

				for act in acts:
					myMoves = act.getMotions()
#					print len(myMoves)
					moves = []
					for move in myMoves: #loop through motion list
						moveAttr = move.getAttributes()
						moves.append(moveAttr)
#					print len(moves)

					temp['instr'].append(dict(type=act.getType(), moves=moves))
# 					moves[:] = []#clear move list

				instrList.append(temp)

#			print instrList


#			actions = [dict(fromLoc=req, toLoc=inputJSON, vol="vol", blowout="blowout")]
			#items = [dict(name="testName", type="testType"), dict(name="test2", type="type2")]
#			return render_template('items.html', actions=actions, deckList=deckList, headList=headList)
			return render_template('items.html', fileName=fileName, headList=headList, instrList=instrList, deckList=deckList, ingrList=ingrList)
		
		else:
			return landing_page()
	else:
		return landing_page()


if __name__ == '__main__':
	app.run()