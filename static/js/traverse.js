/*
	Authored by Gordon Hart
	June 2015

	NOTE: Many of the methods used here are NOT efficient in the slightest.
	This script was written under the assumption that the JSON files fed in
	correspond to REAL experiements.
*/

function traverse(idToSet) { //traverse dom
	if(checkEditing()){ //check if there are unsaved values
		var myString = '{';

		myString += addDeck();
		myString += addHead();
		myString += addIngredients();
		myString += addInstructions();

		myString += newLine("}", 0);
		sendOut(idToSet, myString);
	}
}

function checkEditing() { //check if there are unsaved changes
	var edits = document.getElementsByClassName("mode-edit");
	var ret = true;

	if(edits.length != 0){
		var alertString = "Unfinished business!\nYou have made changes that have not been saved.";
		alertString += "\n\nClick 'ok' to continue without saving.";

		if (confirm(alertString)) { //user confirmed save
   			ret = true;
		} else { //user cancelled save
			document.getElementById('hiddenID').value = "null";
   			ret = false;
		}
	} return ret;
}

function sendOut(id, newText) {
	document.getElementById(id).value = newText;
}

//function traverseToAdd() { //traverse method for use when adding new }

/////////////////////////////////
///// ASSEMBLE JSON METHODS /////
/////////////////////////////////

function addDeck() { //piece the deck back together as a JSON object
	var deckString = newLine('"deck": { ', 1);

	var names = document.getElementsByClassName("deckName");
	var types = document.getElementsByClassName("deckType");

	for(var i=0; i<names.length; i++) {
		var name = stripWhiteSpace(names[i].textContent);
		var type = stripWhiteSpace(types[i].textContent);
		deckString += newLine('"' + name + '": { ', 2);
		deckString += newLine('"labware": "' + type + '"', 3);
		deckString += newLine('},', 2);
	}
	deckString = removeLast(deckString); //cut off last comma
	deckString += newLine('},\n', 1);

	return deckString;
}

function addHead() { //piece the head back together as a JSON object
	var headString = newLine('"head": { ', 1);

	var headItems = document.getElementsByClassName("headItem");
	var headNames = document.getElementsByClassName("headName");
	var headTypes = document.getElementsByClassName("headType");
	var headTrashes = document.getElementsByClassName("headTrash");
	var headTipRacks = document.getElementsByClassName("headTipRack");
	var headAttrKeys = document.getElementsByClassName("headAttrKey");
	var headAttrValues = document.getElementsByClassName("headAttrValue");

	var pointSets = document.getElementsByClassName("pointSet");
	var pointNames = document.getElementsByClassName("pointName");
	var pointValues = document.getElementsByClassName("pointValue");

	for(var i=0; i<headNames.length; i++) {
		var headName = stripWhiteSpace(headNames[i].textContent);
		headString += newLine('"' + headName + '" : {', 2);

		var headType = stripWhiteSpace(headTypes[i].textContent);
		headString += newLine('"tool": "' + headType + '",', 3);

		headString += newLine('"tip-racks": [', 3);
		for(var j=0; j<headTipRacks.length; j++) {
			if(headItems[i].contains(headTipRacks[j])) {
				var tipRack = stripWhiteSpace(headTipRacks[j].textContent);
				headString += newLine('{', 4);
				headString += newLine('"container": "' + tipRack + '"', 5);
				headString += newLine('},', 4);
			}
		}
		headString = removeLast(headString);
		headString += newLine('],', 3);

		var headTrash = stripWhiteSpace(headTrashes[i].textContent);
		headString += newLine('"trash-container": {', 3);
		headString += newLine('"container": "' + headTrash + '"', 4);
		headString += newLine('},', 3);

		for(var k=0; k<headAttrKeys.length; k++){ //go through attributes
			if(headItems[i].contains(headAttrKeys[k])){
				var key = stripWhiteSpace(headAttrKeys[k].textContent);
				var value = stripWhiteSpace(headAttrValues[k].textContent);

				var quotedValue = quotesIfString(value);
				headString += newLine('"' + key + '": ' + quotedValue + ',', 3);
			}
		}	

		headString += newLine('"points": [ ', 3);
		for(var k=0; k<pointSets.length; k++){ //add calibration points
			if(headItems[i].contains(pointSets[k])) {
				headString += newLine('{', 4);

				for(var n=0; n<pointNames.length; n++){
					if(pointSets[k].contains(pointNames[n])) {
						var name = stripWhiteSpace(pointNames[n].textContent);
						var value = stripWhiteSpace(pointValues[n].textContent);

						var quotedValue = quotesIfString(value);
						headString += newLine('"' + name + '": ' + quotedValue + ',', 5);
					}
				}
				headString = removeLast(headString);
				headString += newLine('},', 4);
			}
		}
		headString = removeLast(headString);
		headString += newLine(']', 3);

		headString += newLine('},', 2);
	}
	headString = removeLast(headString);
	headString += newLine('},\n', 1);

	return headString;
}

function addIngredients() { //piece the ingredients section back together as a JSON object
	var ingrString = newLine('"ingredients": { ', 1);

	var blocks = document.getElementsByClassName("reagentBlock");
	var subBlocks = document.getElementsByClassName("reagentSubBlock");
	var names = document.getElementsByClassName("reagentName");
	var keys = document.getElementsByClassName("reagentAttrKey");
	var values = document.getElementsByClassName("reagentAttrValue");

	for(var i=0; i<names.length; i++) {
		var name = stripWhiteSpace(names[i].textContent);
		ingrString += newLine('"' + name + '": [', 2);

		for(var j=0; j<subBlocks.length; j++){ //loop through attribute groups
			if(blocks[i].contains(subBlocks[j])) { //if it's a descendant, add it
				ingrString += newLine('{', 3);

				for(var k=0; k<keys.length; k++){ //loop through attributes
					if(subBlocks[j].contains(keys[k])) { //if it's a descendant, add it
						var key = stripWhiteSpace(keys[k].textContent);
						var value = stripWhiteSpace(values[k].textContent);

						var quotedValue = quotesIfString(value);
						ingrString += newLine('"' + key + '": ' + quotedValue + ',', 4);
					}
				}
				ingrString = removeLast(ingrString);
				ingrString += newLine('},', 3);
			}
		}
		ingrString = removeLast(ingrString);
		ingrString += newLine('],', 2);
	}
	ingrString = removeLast(ingrString);
	ingrString += newLine('},\n', 1);

	return ingrString;
}

function addInstructions() { //piece the instructions back together as a JSON object
	
	//this is a monster. 
	//beware
	
	var instrString = newLine('"instructions": [', 1);

	// structure for getting values back from the moves
	var instrTools = document.getElementsByClassName("instrTool");
	var instrMoves = document.getElementsByClassName("instrMove");
	var instrBlocks = document.getElementsByClassName("instrBlock");
	
	var moveBlocks = document.getElementsByClassName("moveBlock");

	var fromBlocks = document.getElementsByClassName("fromBlock");
	var fromLocKeys = document.getElementsByClassName("fromLocKey");
	var fromLocValues = document.getElementsByClassName("fromLocValue");

	var toBlocks = document.getElementsByClassName("toBlock");
	var toLocKeys = document.getElementsByClassName("toLocKey");
	var toLocValues = document.getElementsByClassName("toLocValue");

	var attrBlocks = document.getElementsByClassName("attrBlock");
	var otherAttrKeys = document.getElementsByClassName("otherAttrKey");
	var otherAttrValues = document.getElementsByClassName("otherAttrValue");

	for(var i=0; i<instrTools.length; i++) {
		var tool = stripWhiteSpace(instrTools[i].textContent);
		instrString += newLine('{', 2);
		instrString += newLine('"tool": "' + tool + '",', 3);
		instrString += newLine('"groups": [ ', 3);

		var toolBlock = document.getElementsByClassName(tool);

		console.log(moveBlocks.length); //TEST TEST TEST TEST

		for(var j=0; j<moveBlocks.length; j++) {
			if(toolBlock[0].contains(moveBlocks[j])){
				var thisBlock = moveBlocks[j];

				instrString += newLine('{', 4);
				moveName = stripWhiteSpace(instrMoves[j].textContent); //add name

				if(moveName == "transfer"){
					instrString += newLine('"transfer": [ ', 5);

					/*
					THIS FUNCTION NEEDS A SERIOUS OVERHAUL.
					
					the current method of matching up fromBlocks, toBlocks, and attrBlocks
					does NOT work in all cases. 

					there must be some measure in place to group together moves within actions,
					and add each block within that move sequentially.
					*/

					for(var k=0; k<fromBlocks.length; k++){
						if (thisBlock.contains(fromBlocks[k])) {
							instrString += newLine('{', 6);
							instrString += newBlock("from", fromLocKeys, fromLocValues, fromBlocks[k], 6); //add from characteristics
							instrString += newBlock("to", toLocKeys, toLocValues, toBlocks[k], 6); //add to characteristics
							instrString += newAttrs(otherAttrKeys, otherAttrValues, attrBlocks[k], 6);
							instrString += newLine('},', 6);
						} //NOTE: we are able to do this in one move as such because transfers are always 1:1
					}
					instrString = removeLast(instrString);
					instrString += newLine(']', 5);

				} else if (moveName == 'distribute') {
					instrString += newLine('"distribute": { ', 5);

					for(var k=0; k<fromBlocks.length; k++){
						if (thisBlock.contains(fromBlocks[k])) {
							instrString += newBlock("from", fromLocKeys, fromLocValues, fromBlocks[k], 6); //add from characteristics

							instrString += newLine('"to": [', 6)
							for(var m=0; m<toBlocks.length; m++) {
								if(thisBlock.contains(toBlocks[m])){
									instrString += newLine('{', 7);
									instrString += newAttrs(toLocKeys, toLocValues, toBlocks[m], 7); //add to characteristics
									instrString += newLine('},', 7);
								}
							}
							instrString = removeLast(instrString);
							instrString += newLine('],', 6);
							instrString += newAttrs(otherAttrKeys, otherAttrValues, thisBlock, 6);
						}
					}
					instrString += newLine('}', 5);
				} else if (moveName == 'consolidate') {
					instrString += newLine('"consolidate": { ', 5);

					for(var k=0; k<toBlocks.length; k++){
						if (thisBlock.contains(toBlocks[k])) {
							instrString += newLine('"from": [ ', 6)
							for(var m=0; m<fromBlocks.length; m++) {
								if(thisBlock.contains(fromBlocks[m])){
									instrString += newLine('{', 7);
									instrString += newAttrs(fromLocKeys, fromLocValues, fromBlocks[m], 7); //add to characteristics
									instrString += newLine('},', 7);
								}
							} 
							instrString = removeLast(instrString);
							instrString += newLine('],', 6);

							instrString += newBlock("to", toLocKeys, toLocValues, toBlocks[k], 6); //add from characteristics

							instrString += newAttrs(otherAttrKeys, otherAttrValues, thisBlock, 6); 
						} 
					} 
					instrString += newLine('}', 5); 
				} else if (moveName == 'mix') {
					instrString += newLine('"mix": [ ', 5);
					for(var k=0; k<attrBlocks.length; k++){
						if(thisBlock.contains(attrBlocks[k])) {
							instrString += newLine('{', 6);
							instrString += newAttrs(otherAttrKeys, otherAttrValues, attrBlocks[k], 6); 
							instrString += newLine('},', 6);
						}
					}
					instrString = removeLast(instrString);
					instrString += newLine(']', 5);
				}

				instrString += newLine('},', 4);
			}
		}
		instrString = removeLast(instrString);
		instrString += newLine(']', 3);
		instrString += newLine('},', 2);
	}

	instrString = removeLast(instrString);
	instrString += newLine(']', 1);

	return instrString;
}

/////////////////////////////////
//////////// HELPER METHODS /////
/////////////////////////////////

function newBlock(name, keys, values, parentBlock, indentLevel) {
	var out = newLine('"' + name + '": {', indentLevel);

	for(var k=0; k<keys.length; k++){
		if(parentBlock.contains(keys[k])) {
			var key = stripWhiteSpace(keys[k].textContent);
			var value = stripWhiteSpace(values[k].textContent);
			var quotedValue = quotesIfString(value);

			out += newLine('"' + key + '": ' + quotedValue + ',',(indentLevel+1));
		}
	}
	out = removeLast(out);
	out += newLine('},', indentLevel);

	return out;
}

function newAttrs(keys, values, parentBlock, indentLevel) {
	var out = '';
//	console.log(parentBlock);
	for(var k=0; k<keys.length; k++){ //add other attributes
		if(parentBlock.contains(keys[k])) {
			var key = stripWhiteSpace(keys[k].textContent);
			var value = stripWhiteSpace(values[k].textContent);
			var quotedValue = quotesIfString(value);
			out += newLine('"' + key + '": ' + quotedValue + ',',indentLevel);
		}
	}
	out = removeLast(out);
	return out;
}

function newLine(text, tabcount) { //add a new line with given text and given # of leading tabs
	var out = '\n';
	for (var i=0; i<tabcount; i++) {
		out += '\t';
	}
	out += text;
	return out;
}

function quotesIfString(input) {
	trueOrFalse = /(false|true)/i;
	match = trueOrFalse.exec(input);
	if(match != null) { //match to flase or true, case insensitive
		out = String(input); //for some reason the input was an object
		out = out.toLowerCase();
		return out;
	} else if (!isNaN(input)){ //return if it's a number
		return input;
	}
	out = '"' + input + '"'; //add quotes, it's not a number or boolean
	return out;
}

function stripWhiteSpace(input) {
	var strInput = String(input);
	var output = strInput.trim();
	return output;
}

function removeLast(input) {
	var output = input.substring(0,input.length-1);
	return output;
}