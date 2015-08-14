
/*
'viewer.js' contains all of the functions responsible for handling
the mechanics of the display.
*/

////////////////////////////////////////////
////////// ITEMS VIEW FUNCITONS ////////////
////////////////////////////////////////////

function toggleItem(clicked, showID) {
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
////////// INSTRUCTIONS VIEW FUNCTIONS /////
////////////////////////////////////////////

function toggleInstruction(clicked) {
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

function showInstruction(clicked) {
	/*
	Instead of toggling view, always expands the instructions, even if it
	is already expanded when this button is clicked.

	Built for use with the delete button.
	*/
	var clicked_id = clicked.id;
	var id_parts = clicked_id.split('.'); // split ID based on period

	var id_main = id_parts[0] + "." + id_parts[1] + '.' + id_parts[2];
	var id_nav = id_main + ".nav";

	if(!clicked.classList.contains("view")){
		document.getElementById(id_main).classList.add("view");
		document.getElementById(id_nav).classList.add("view");
	}
}

function showInserts(clicked) {
	/*
	Shows the "Insert New Instruction" buttons on click. For use in the 
	instructions navbar.
	*/
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

function showAddInstruction(buttonDiv) {
	/*
	Expands the "Insert New Instructions" button to the set of five
	buttons: one for each type of instruction (transfer, distribure,
	consolidate, mix), and one for Cancel.

	On cancel click, hides the grouping.
	*/
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
//////// EVENT LISTENERS ///////////////////
////////////////////////////////////////////

document.addEventListener('click', function(event){
	/*
	Highlights the group currently being edited on click, unhighlights when
	something other than it is clicked.

	Will eventually be used to save entire blocks of modifications when the block
	is clicked away from. For not it is just for display.
	*/
	var current = event.srcElement; // get the clicked element
	var previous = document.getElementsByClassName('editing')[0]; // only one block currently editing

	if(previous) { // if there is a node currently being edited
		previous.classList.remove('editing'); // remove the editing class
	}

	var parents = [ current ]; // initialize parent list with the clicked node
	// assemble list of parents until end or we reach a <section> block
	while(current.parentNode != null && current.parentNode.nodeName != 'SECTION') {
		parents.push(current.parentNode);
		current = current.parentNode;
	}

	for(var i=0; i<parents.length; i++) { // go through the nodes in the parents list
//		console.log(parents[i].classList);
		if(parents[i].classList != null) {
			if(parents[i].classList.contains('modifyBlock')) { // highlight the highest level grouping node to be edited

				current = parents[i]; // set this new grouping to be the current node
				current.classList.add('editing');

				break; // exit loop, we have found our node
			}
		}
	}

	if(current != previous && previous != null) { // if the new click is in a different block than prev, save changes
//		console.log("getBlock " + previous);
		getBlock(previous); // call the function in 'sender.js' to read the current block into JSON
	}

});

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

	var instr_toggle_to_top = instr_toggler.offset().top;
	var instr_block_to_top = instr_block.offset().top;

	if(instr_toggle_to_top < screen_to_top) {
		instr_left.addClass('sticky');
	} else if(instr_block_to_top > screen_to_top) {
		instr_left.removeClass('sticky');
	}
});

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

/* 
Functions to preserve the expanded structure of the instructions
upon an edit action that will overwrite the entire section.

NON-FUNCTIONAL CURRENTLY 

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
*/

