
/*
'sender.js' contains all of the functions responsible for edit functions,
including the AJAX calls to communicate with the Flask app, and the frontend
functions responsible for deleting/modifying the display of the information
on an edit.
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

	console.log(out);
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
		// if it's an ingredient and the ID is of form 'ingredients.0.2' then it is a location
		changes['ef'] = 'add_loc';
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

////////////////////////////////////////////
///////// FRONTEND EDIT FUNCTIONS //////////
////////////////////////////////////////////

function getBlock(block) {
	/*
	getBlock takes an ID as input and assembles the block-level JSON for edit_modify_block.
	Ends with a call to edit_modify_block.
	*/
	var id_parts = block.id.split('.');
	var section = id_parts[0];

	out = {};
	if(section == 'deck') {
		var children = block.children;
		var name = getKeyValue(children[0]);

		out[name['value']] = {};
		for(var i=1; i<children.length-1; i++) {
			var pair = getKeyValue(children[i]);
			out[name['value']][pair['key']] = pair['value'];
		}
	}

	edit_modify_block(block.id, out); // call the AJAX function to edit by block
}

function getKeyValue(kvblock) {
	/*
	returns a key-value pair from the key-value block of form (found in keyvalue.html):
	<div class="key-value">
		<span class="key">{{ key }}</span>
		<span class="value">
			<div class="edit-in-place modalComponent mode-display">
				<div class="mode display">
					<span class="edit-handle value" style="cursor:pointer;">{{ value }}</span>
				</div>
				<div class="mode edit">
					<form action="/user/1/edit" method="post">
						<input type="text" value="{{ value }}" name="name" class="edit-input" onblur="clickSubmit('{{ key }}', this.parentNode);" />
						<input type="submit" value="Save" class="save-edit hidden" />
					</form>
				</div>
			</div>
		</span>
	</div>
	*/
	var key = kvblock.children[0].innerHTML;
	var value = kvblock.children[1].children[0].children[0].children[0].innerHTML;

	var out = {};
	out['key'] = key;
	out['value'] = value;
	return out;
}

function clickSubmit(key, parent) {
	/*
	This funciton simulates a click on the submit button on blur for modal editing.
	*/
	var submitButton = parent.children[1];

	var parentID = null;
	var cur = parent;
	while(parentID == null) { // keep going up and up until we reach an item that has an ID
		cur = cur.parentNode; // using this method allows for a non-uniform ID setting pattern
		if(cur.hasAttribute("id")) { // that works well with the highly variable protocol format
			parentID = cur.id;
//			console.log(parentID);
		}
	}

	parentID_parts = parentID.split('.');
	if(parentID_parts[0] == 'deck') {
		console.log(document.getElementById(parentID));
	}

	submitButton.onclick = edit_modify(parentID, key, parent.children[0].value); // set the input button's onclick function, then click the button
	// this is a sort of roundabout way to do this, yes, but the Modals framework is listening for a button click so this method will do
	submitButton.click(); // simulate click on the input[type=submit] within the form 'parent'
	// triggers an edit_modify() and changes the <input> text field back into a <span>
}

function removeSection(del_button) {
	/*
	First confirms delete and then deletes the parent node of the button clicked.

	Completes the deletion on the front end, then informs the backend of
	the deletion via AJAX.
	*/
	el_to_del = del_button.parentNode; // this is the button nested in the delete section nested in the el to delete

	if(!del_button.classList.contains('confirm')) { // first click, must still confirm?
		del_button.classList.add('confirm');

		del_button.children[0].classList.add('hidden');
		del_button.children[1].classList.remove('hidden');
	} else {
		el_to_del.parentNode.removeChild(el_to_del); // delete the node in question
		edit_delete(el_to_del.id); // contact the edit function for deleting to update the backend of the deletion
	}
}

function cancelRemove(div_to_cancel) {
	/*
	Resets the 'removeSection' display back to normal if the 'cancel'
	button is clicked.
	*/
	div_to_cancel.classList.remove('confirm');

	div_to_cancel.children[0].classList.remove('hidden'); // re-show the little 'x' for the delete
	div_to_cancel.children[1].classList.add('hidden'); // hide the large DELETE and CANCEL buttons
}
