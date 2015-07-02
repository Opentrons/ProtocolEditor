/* 
Adder.js tacks together the JSON objects for the new element to be added
and passes them off to the hidden input specified in the function call
*/

/*
FORM METHODS

each of the following methods has a corresponding method of the same name in adder.py.
these methods function by retrieving the values from the forms in question, and using them
to assemble a specially formatted json object that is passed over to the Flask app.
*/

function addContainer(form, hiddenID) {
	var out = '{ "type" : "container", ';
	out += '"name" : "' + form.name.value + '", ';
	out += '"kind" : "' + form.kind.value + '" }'; //assemble json

	document.getElementById(hiddenID).value = out; // add json to the hidden form
}

function addIngredient(form, hiddenID) {
	var out = '{ "type" : "ingredient", ';//assemble json
	out += '"name" : "' + form.name.value + '", ';
	out += '"volume" : "' + form.volume.value + '", ';
	out += '"container" : "' + form.container.value + '", ';
	out += '"location" : "' + form.location.value + '" }';

	document.getElementById(hiddenID).value = out; // add json to the hidden form
}

function addIngrLocation(form, hiddenID) {
	var out = '{ "type" : "ingrLocation", ';//assemble json
	out += '"parent" : "' + form.parentIngredient.value + '", ';
	out += '"volume" : "' + form.volume.value + '", ';
	out += '"container" : "' + form.container.value + '", ';
	out += '"location" : "' + form.location.value + '" }'; 

	document.getElementById(hiddenID).value = out; // add json to the hidden form
}

/*
STANDALONE METHODS

these methods operate by directly altering the classnames of the object in question.
the "addClassName" function goes in and adds the proper class name to the object
so that it will be picked up by the "traverse()" function called immediately afterwards.
*/

function addMotion(parent){ //set the appropriate class names for the attributes being added to be picked up by traverse.js
	addClassName("motionBlock", document.getElementsByClassName("new_motionBlock"), parent);

	addClassName("fromBlock", document.getElementsByClassName("new_fromBlock"), parent);
	addClassName("toBlock", document.getElementsByClassName("new_toBlock"), parent);
	addClassName("attrBlock", document.getElementsByClassName("new_attrBlock"), parent);
}

function addHeadItem(parent){ //add the proper class names
	addClassName("headItem", document.getElementsByClassName("new_headItem"), parent);
	addClassName("headName", document.getElementsByClassName("new_headName"), parent);
	addClassName("headType", document.getElementsByClassName("new_headType"), parent);
	addClassName("headTrash", document.getElementsByClassName("new_headTrash"), parent);
	addClassName("headTipRack", document.getElementsByClassName("new_headTipRack"), parent);

	addClassName("headAttrKey", document.getElementsByClassName("new_headAttrKey"), parent);
	addClassName("headAttrValue", document.getElementsByClassName("new_headAttrValue"), parent);

	addClassName("pointSet", document.getElementsByClassName("new_pointSet"), parent);
	addClassName("pointName", document.getElementsByClassName("new_pointName"), parent);
	addClassName("pointValue", document.getElementsByClassName("new_pointValue"), parent);
}

function addInstruction(parent, type) {
	var typeString = "new_" + type + "_moveBlock";
	var instrMoveString = "instrMove_" + type;

	addClassName("instrMove", document.getElementsByClassName(instrMoveString), parent)
	addClassName("moveBlock", document.getElementsByClassName(typeString), parent);
}

//////////////////////////////////////
//////////////// HELPER //////////////
//////////////////////////////////////

function addClassName(name, elements, parent){
	if(elements.length > 0){
		for(var i=0; i<elements.length; i++){
			if(parent.contains(elements[i])){
				elements[i].className += " " + name;
//				console.log(name);
			}
		}
	}
}
