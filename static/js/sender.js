/*	
CORE EDITING FUNCTIONS

AJAX functions corresponding to the six main editing functions:
	Modify Delete Copy Paste Add Insert
*/

function edit_modify(id, key, value) {
	/*
	CORE EDITING FUNCTIONS: [Modify] Delete Copy Paste Add Insert

	Function sends an AJAX packet back to the Flask application with the data that is being
	changed for the item in question.

	Submit with the ID of the object in question, and the key and value being edited.
	*/
	var data = {}; // these are the actual changes being made
	data[key] = value;

	var changes = { // this is the information that goes along with the changes
		"ef": "modify",
		"id": id,
		"data": data
	};

	var out = {};
	out['changes'] = JSON.stringify(changes); // send over stringify'd version to avoid MultiDict (flattened) headache

	console.log(changes);
	$.getJSON('/edit', out, function(data) { // return HTML for new container
		console.log("new values: (" + key + " --> " + value + ")");
	});
}

function edit_delete(id) {
	/*
	CORE EDITING FUNCTIONS: Modify [Delete] Copy Paste Add Insert
	
	Receives an ID of the object being deleted and informs the backend via AJAX
	that the item in question has been removed.
	*/
	var changes = {
		"ef": "delete",
		"id": id,
		"data": {}
	}

	var out = {}
	out['changes'] = JSON.stringify(changes); // this is how we're doing it, every time

	$.getJSON('/edit', out, function(data) { // must re-render entire section because the indeces have changed
		var section = id.split('.')[0];
		document.getElementById(section).innerHTML = data.html; // reset html
		
		console.log(data.html);
		console.log("item " + id + " deleted.");
	});
}

function edit_add(id) {
	/*
	CORE EDITING FUNCTIONS: Modify Delete Copy Paste [Add] Insert
	
	Sends the id of the type of object to be added and gets the HTML for the 
	new object in return, rewriting the section in question to show the new
	addition.
	*/
	var changes = {
		"ef": "add",
		"id": id,
		"data": {}
	};

	var out = {};
	out['changes'] = JSON.stringify(changes);

	if(id == 'deck'){
		$.getJSON('/edit', out, function(data) { // return HTML for new container
//			var section = id.split('.')[0];
			document.getElementById(id).innerHTML = data.html; // reset html
		});
	} else if (id == 'instructions') {
		$.getJSON('/edit', out, function(data) { // return HTML for new container
//			var section = id.split('.')[0];
			console.log(data.html);
			document.getElementById(id).innerHTML = data.html; // reset html
		});
	}
}

function edit_copy() {

}

function edit_paste() {

}

function edit_insert() {

}