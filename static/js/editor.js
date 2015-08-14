
/*
'editor.js' contains the frontend functions responsible for edits,
including deletes, modify, etc.

These functions prepare the the inputs for 'sender.js' to send
back to the server.
*/

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
	if(section == 'deck') { // the block being edited is a container block
		var children = block.children;
		var name = getKeyValue(children[0]);

		out[name['value']] = {}; // assemble the full JSON snippet for this container
		for(var i=1; i<children.length-1; i++) {
			var pair = getKeyValue(children[i]);
			out[name['value']][pair['key']] = pair['value'];
		}
	} else if(section == 'ingredients') { // editing an ingredient block
		var children = block.children;
		var name = getKeyValue(children[0]);

		out[name['value']] = [];

		for(var i=0; i<children.length; i++) {
			if(children[i].classList.contains('grouping')) {
				var locNode = children[i];
				var newLoc = {};

				for(var j=0; j<locNode.children.length; j++){
					if(locNode.children[j].classList.contains('key-value')) {
						console.log(locNode.children[j]);
						var pair = getKeyValue(locNode.children[j]);
						newLoc[pair['key']] = pair['value'];
					}
				}

				out[name['value']].push(newLoc);
			}
		}
		console.log(JSON.stringify(out));
//		console.log(children);
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
