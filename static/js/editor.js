
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

	DOM traversal... readers beware.
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

				var keyValues = getChildByClassName(locNode, 'key-value');
				for(var j=0; j<keyValues.length; j++){
					console.log(keyValues[j]);
					var pair = getKeyValue(keyValues[j]);
					newLoc[pair['key']] = pair['value'];
				}
				out[name['value']].push(newLoc);
			}
		}
	} else if(section == 'instructions') { // this is going to get ugly
//		var children = block.children;
		var name = getChildByClassName(block.children[0], 'action-title')[0].innerHTML;

		if(name == 'transfer') {
			out[name] = [];

			var actions = getChildByClassName(block, 'motion');
			console.log('actions length: ' + String(actions.length));

			for(var i=0; i<actions.length; i++) {
				var curMove = {};
				var motions = getChildByClassName(actions[i], 'action-attributes');

				for(var j=0; j<motions.length; j++) {
					var attributes = getChildByClassName(motions[j], 'key-value');

					if(motions[j].classList.contains('from')) { // add from attributes
						curMove['from'] = {}
						for(var k=0; k<attributes.length; k++) {
							var pair = getKeyValue(attributes[k]);
							curMove['from'][pair['key']] = pair['value'];
						}
					} else if(motions[j].classList.contains('to')) { // add to attributes
						curMove['to'] = {}
						for(var k=0; k<attributes.length; k++) {
							var pair = getKeyValue(attributes[k]);
							curMove['to'][pair['key']] = pair['value'];
						}
					} else { // add other attributes
						for(var k=0; k<attributes.length; k++) {
							var pair = getKeyValue(attributes[k]);
							curMove[pair['key']] = pair['value'];
						}
//						console.log('other');
					}
				}
				out[name].push(curMove);
			}
			
		} else if(name == 'distribute') {
			out[name] = {};

			var motions = getChildByClassName(block, 'action-attributes');
//			console.log(motions.length);

			for(var i=0; i<motions.length; i++) {
				console.log(motions[i]);
				var attributes = getChildByClassName(motions[i], 'key-value');

				if(motions[i].classList.contains('from')) { // add from attributes
					out[name]['from'] = {}
					for(var j=0; j<attributes.length; j++) {
						var pair = getKeyValue(attributes[j]);
						out[name]['from'][pair['key']] = pair['value'];
					}
				} else if(motions[i].classList.contains('to')) { // add to attributes
					out[name]['to'] = []
					
					var locations = getChildByClassName(motions[i], 'action');					

					for(var j=0; j<locations.length; j++) {
						var newLoc = {};
						var attributes = getChildByClassName(locations[j], 'key-value');

						for(var k=0; k<attributes.length; k++) {
							var pair = getKeyValue(attributes[k]);
							newLoc[pair['key']] = pair['value'];
						}
						out[name]['to'].push(newLoc);
					}

				} else { // add other attributes
//					console.log('other');
//					console.log(attributes.length);
					for(var j=0; j<attributes.length; j++) {
						var pair = getKeyValue(attributes[j]);
						out[name][pair['key']] = pair['value'];
					}
				}
			}

		} else if(name == 'consolidate') {
			out[name] = {};

			var motions = getChildByClassName(block, 'action-attributes');
			console.log(motions.length);

			for(var i=0; i<motions.length; i++) {
				console.log(motions[i]);
				var attributes = getChildByClassName(motions[i], 'key-value');

				if(motions[i].classList.contains('from')) { // add from attributes
					out[name]['from'] = []
					
					var locations = getChildByClassName(motions[i], 'action');					

					for(var j=0; j<locations.length; j++) {
						var newLoc = {};
						var attributes = getChildByClassName(locations[j], 'key-value');

						for(var k=0; k<attributes.length; k++) {
							var pair = getKeyValue(attributes[k]);
							newLoc[pair['key']] = pair['value'];
						}
						out[name]['from'].push(newLoc);
					}
				} else if(motions[i].classList.contains('to')) { // add to attributes
					out[name]['to'] = {}
					for(var j=0; j<attributes.length; j++) {
						var pair = getKeyValue(attributes[j]);
						out[name]['to'][pair['key']] = pair['value'];
					}
				} else { // add other attributes
					console.log('other');
					console.log(attributes.length);
					for(var j=0; j<attributes.length; j++) {
						var pair = getKeyValue(attributes[j]);
						out[name][pair['key']] = pair['value'];
					}
				}
			}

		} else { // it's a mix
			out[name] = [];

			var motions = getChildByClassName(block, 'action-attributes');
			var curMove = {};	
			
			for(var i=0; i<motions.length; i++) {
				var attributes = getChildByClassName(motions[i], 'key-value');

				for(var j=0; j<attributes.length; j++) {
					var pair = getKeyValue(attributes[j]);
					curMove[pair['key']] = pair['value'];
				}

				out[name].push(curMove);
				curMove = {}; // add and reset the current move
			}	
		}
	}
	
	console.log(JSON.stringify(out));
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

function getChildByClassName(parent, classname) {
	/*
	Helper function that returns the child node of a given parent with a given classname.

	If there are multiple, will return a list.
	*/
	var matches = [];

	for(var i=0; i<parent.children.length; i++) {
		if(parent.children[i].classList.contains(classname)) {
			matches.push(parent.children[i]);
		}
	}
//	console.log(matches);
	return matches; // returns full list of matches
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

////////////////////////////////////////////
///////// DELETE BLOCK FUNCTIONS ///////////
////////////////////////////////////////////

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
