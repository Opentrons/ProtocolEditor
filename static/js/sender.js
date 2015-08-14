
/*
'sender.js' contains all of the functions responsible for communicating
with the Flask application.

All functions are AJAX calls to asynchronously tie the front-end edits
to the backend.
*/

////////////////////////////////////////////
/////// AJAX CORE EDITING FUNCTIONS ////////
////////////////////////////////////////////

function edit_modify(id, key, value) {
	/*
	CORE EDITING FUNCTIONS: [Modify] Delete Copy Paste Add Insert

	Function sends an AJAX packet back to the Flask application with the data that is being
	changed for the item in question.

	Submit with the ID of the object in question, and the key and value being edited.
	*/
	var id_parts = id.split('.');
	var section = id_parts[0];

	if(section == 'info') { // this edit_modify (by key-value pair) is ONLY used for the info section
		var data = {}; // these are the actual changes being made
		data[key] = value;

		var changes = { // this is the information that goes along with the changes
			"ef": "modify",
			"id": id,
			"data": data
		};

		var out = {};
		out['changes'] = JSON.stringify(changes); // send over stringify'd version to avoid MultiDict (flattened) headache

		$.getJSON('/edit', out, function(data) { // return HTML for new container
			console.log("edit_modify() new values: (" + key + " --> " + value + ")");
		});
	}
}

function edit_modify_block(id, block) {
	/*
	CORE EDITING FUNCTIONS: [Modify] Delete Copy Paste Add Insert

	Same as above function edit_modify, but edits on the block level instead of the
	key-value level.
	*/
	var changes = { // this is the information that goes along with the changes
		"ef": "modify",
		"id": id,
		"data": block
	};

	var out = {};
	out['changes'] = JSON.stringify(changes); // send over stringify'd version to avoid MultiDict (flattened) headache

	$.getJSON('/edit', out, function(data) { // return HTML for new container
		console.log("edit_modify_block() changed block: " + id);
	});
}

function edit_delete(id) {
	/*
	CORE EDITING FUNCTIONS: Modify [Delete] Copy Paste Add Insert
	
	Receives an ID of the object being deleted and informs the backend via AJAX
	that the item in question has been removed.
	*/
	var id_parts = id.split('.');
	var section = id_parts[0];
	
	var changes = {
		"ef": "delete",
		"id": id,
		"data": {}
	}

	if(section == 'ingredients' && id_parts.length == 3) { 
		// if it's an ingredient and the ID is of form 'ingredients.0.2' then it is a location
		changes['ef'] = 'delete_loc';
	} else if(section == 'head' && id_parts.length == 3) {
		changes['ef'] = 'delete_tiprack';
	}

//	if(section == 'instructions') {
//		var instr_expand = getExpandStructure();
//	}

	var out = {}
	out['changes'] = JSON.stringify(changes); // this is how we're doing it, every time

	$.getJSON('/edit', out, function(data) { // must re-render entire section because the indeces have changed
		document.getElementById(section).innerHTML = data.html; // reset html
		
//		console.log(data.html);
//		console.log("item " + id + " deleted.");
	});

//	if(section == 'instructions') {
//		applyExpandStructure(instr_expand);
//	}
}

function edit_add(id) {
	/*
	CORE EDITING FUNCTIONS: Modify Delete Copy Paste [Add] Insert
	
	Sends the id of the type of object to be added and gets the HTML for the 
	new object in return, rewriting the section in question to show the new
	addition.
	*/
	var id_parts = id.split('.');
	var section = id_parts[0];

	var changes = {
		"ef": "add",
		"id": id,
		"data": {}
	};

	if(section == 'ingredients' && id_parts.length == 2) { 
		// if it's an ingredient and the ID is of form 'ingredients.0' then it is a location (add to ingredients.0)
		changes['ef'] = 'add_loc';
	} else if(section == 'head' && id_parts.length == 2) {
		changes['ef'] = 'add_tiprack'
	}

	var out = {};
	out['changes'] = JSON.stringify(changes);

	$.getJSON('/edit', out, function(data) { // return HTML for new container
		document.getElementById(section).innerHTML = data.html; // reset html
	});
}

function edit_add_instruction(id, moveType) {
	/*
	CORE EDITING FUNCTIONS: Modify Delete Copy Paste [Add] Insert
	
	Sends the id of the type of object to be added and gets the HTML for the 
	new object in return, rewriting the section in question to show the new
	addition.
	*/
	var changes = {
		"ef": "add_" + moveType,
		"id": id,
		"data": {}
	};

	var section = id.split('.')[0];

	var out = {};
	out['changes'] = JSON.stringify(changes);

	$.getJSON('/edit', out, function(data) { // return HTML for new container
		document.getElementById(section).innerHTML = data.html; // reset html
	});
}

function edit_insert(id, moveType) {
	var changes = {
		"ef": "insert_" + moveType,
		"id": id,
		"data": {}
	};

	var section = id.split('.')[0];

	var out = {};
	out['changes'] = JSON.stringify(changes);

	$.getJSON('/edit', out, function(data) { // return HTML for new container
		document.getElementById(section).innerHTML = data.html; // reset html
	});
}

function edit_copy() {

}

function edit_paste() {

}