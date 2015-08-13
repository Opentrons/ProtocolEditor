function toggle(clicked, showID) {
	/*
	toggles the displayed "Item" block by adding/removing the "active" tag
	based on which button was clicked.
	
	"Item" blocks are: Information, Deck, Head, and Ingredients.
	*/
	var toggles = document.getElementById("Toggle").children;
	for(var i=0; i<toggles.length; i++){ // remove active from all toggle buttons
		if(toggles[i].classList.contains("active")){
			toggles[i].classList.remove("active");
		}
	}
	clicked.classList.add("active"); // add active class to proper toggle button

	var items = document.getElementById("Item").children;
	for(var i=0; i<items.length; i++){ // remove active from all items
		if(items[i].classList.contains("active")){
			items[i].classList.remove("active");
		}
	}
	document.getElementById(showID).classList.add("active"); // add active class to proper item
}

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

function view(clicked) {
	/*
	ID of form: "instruction.0.1"
		- first number refers to tool number
		- second number refers to move number for that tool
	*/
	var clicked_id = clicked.id;
	var id_parts = clicked_id.split('.'); // split ID based on period

	var id_main = id_parts[0] + "." + id_parts[1] + '.' + id_parts[2];
	var id_nav = id_main + ".nav";

	if(clicked.classList.contains("view")){
		document.getElementById(id_main).classList.remove("view");
		document.getElementById(id_nav).classList.remove("view");
	} else {
		document.getElementById(id_main).classList.add("view");
		document.getElementById(id_nav).classList.add("view");
	}
}

function showInstruction(clicked) { // always shows the block
	var clicked_id = clicked.id;
	var id_parts = clicked_id.split('.'); // split ID based on period

	var id_main = id_parts[0] + "." + id_parts[1] + '.' + id_parts[2];
	var id_nav = id_main + ".nav";

	if(!clicked.classList.contains("view")){
		document.getElementById(id_main).classList.add("view");
		document.getElementById(id_nav).classList.add("view");
	}
}

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

document.addEventListener('click', function(event){
	/*
	Highlights the group currently being edited on click, unhighlights when
	something other than it is clicked.

	Will eventually be used to save entire blocks of modifications when the block
	is clicked away from. For not it is just for display.
	*/
	var clicked = event.srcElement;
	var editing = document.getElementsByClassName('editing');

	for(var i=0; i<editing.length; i++) {
		editing[i].classList.remove('editing');
	}

	var current = clicked;
	var parents = [ current ];
	while(current.parentNode.nodeName != 'SECTION') {
		parents.push(current.parentNode);
		current = current.parentNode;
	}

	for(var i=0; i<parents.length; i++) {
		console.log(parents[i].classList);
		if(parents[i].classList.contains('grouping')) {
			parents[i].classList.add('editing');
		}
	}
});

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

$(window).scroll(function(e){ 
	/*
	JQuery listener to keep the instructions toggle menu stuck to the top of the page
	and the instructions edits to the bottom of the page.
	*/
	var screen_to_top = $(window).scrollTop() + 25;

	//INSTRUCTIONS TOGGLE
	var instr_toggler = $("#InstructionsToggle");
	var instr_block = $("#InstructionsDisplay");

	var instr_left = $("#InstructionsLeft");
//	var instr_actions = $("#InstructionsActions");

	var instr_toggle_to_top = instr_toggler.offset().top;
	var instr_block_to_top = instr_block.offset().top;

	if(instr_toggle_to_top < screen_to_top) {
		instr_left.addClass('sticky');
//		instr_toggler.addClass('sticky');
//		instr_actions.addClass('sticky');
	} else if(instr_block_to_top > screen_to_top) {
		instr_left.removeClass('sticky');
//		instr_toggler.removeClass('sticky');
//		instr_actions.removeClass('sticky');
	}
});

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

function clickSubmit(key, parent) { // this funciton simulates a click on the submit button on blur for modal editing
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

	submitButton.onclick = edit_modify(parentID, key, parent.children[0].value); // set the input button's onclick function, then click the button
	// this is a sort of roundabout way to do this, yes, but the Modals framework is listening for a button click so this method will do
	submitButton.click(); // simulate click on the input[type=submit] within the form 'parent'
}

////////////////////////////////////////////
////////////////////////////////////////////
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

//		console.log("change img");
//		del_button.innerHTML = 'click here to CANCEL delete'; // change to confirm picture
	} else {
		el_to_del.parentNode.removeChild(el_to_del); // delete the node in question
		edit_delete(el_to_del.id); // contact the edit function for deleting to update the backend of the deletion
	}
}

function cancelRemove(div_to_cancel) {
	div_to_cancel.classList.remove('confirm');

	div_to_cancel.children[0].classList.remove('hidden');
	div_to_cancel.children[1].classList.add('hidden');
}

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

function showAddInstruction(buttonDiv) {
	var hideLink = buttonDiv.children[0];
	var buttonGroup = buttonDiv.children[1];

	if(hideLink.classList.contains('hidden')) {
		hideLink.classList.remove('hidden');
		buttonGroup.classList.add('hidden');
	} else {
		hideLink.classList.add('hidden');
		buttonGroup.classList.remove('hidden');
	}
}

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

function getExpandStructure() {
	var instructions = document.getElementsByClassName('action-block-nav');
	var expands = [];

	for(var i=0; i<instructions.length; i++) {
		if(instructions[i].classList.contains('view')) {
			expands.push(true);
		} else {
			expands.push(false);
		}
	}

	return expands;
}

function applyExpandStructure(structure) {
	var instructions = document.getElementsByClassName('action-block-nav');

	for(var i=0; i<instructions.length; i++) {
		if(structure[i]) {
			view(instructions[i]);
		}
	}
}

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

function showInserts(clicked) {
//	var instrID = 'instructions.' + String(instr_num);
//	var toolChildren = document.getElementById(instrID).children;
	if(clicked.classList.contains('active')) {
		clicked.classList.remove('active');
	} else {
		clicked.classList.add('active');
	}

	var inserts = document.getElementsByClassName('insert-block');
	for(var i=0; i<inserts.length; i++) {
		if(inserts[i].classList.contains('view')) {
			inserts[i].classList.remove('view');
		} else {
			inserts[i].classList.add('view');
		}
	}
}


