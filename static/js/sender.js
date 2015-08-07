/*

$(document).ready(function(){

	$('a#NewContainer').click(function(){ // on "NewContainer" anchor click
		$.getJSON('/add', {
			type: $('a#NewContainer').attr('type') // send request for new container to app
		}, function(data) { // return HTML for new container
			var new_container = document.createElement('div');

			new_container.classList.add('grouping');
			new_container.innerHTML = data.html;

			$('#containers').append(new_container); // add to list of containers
		});

	});

	$('a#NewReagent').click(function(){ // on "NewContainer" anchor click
		$.getJSON('/add', {
			type: $('a#NewReagent').attr('type') // send request for new container to app
		}, function(data) { // return HTML for new container
			var new_reagent = document.createElement('div');

			new_reagent.classList.add('content');
			new_reagent.innerHTML = data.html;

			$('#reagents').append(new_reagent); // add to list of containers
		});

	});

});

*/

//////////////////////////////////////
//////////////////////////////////////
//////////////////////////////////////

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
		document.getElementById("Deck").innerHTML = data.html; // reset html
		
		console.log(data.html);
		console.log("item " + id + " deleted.");
	});
}

function edit_add(id) {
	var data = {};
	if(id == 'deck'){
		data = {
			"container name": {
				"labware": "container type",
				"slot": "deck slot"
			}
		};
	}


	var changes = {
		"ef": "add",
		"id": id,
		"data": data
	};

	if(id == 'deck'){
		var out = {};
		out['changes'] = JSON.stringify(changes);

		$.getJSON('/edit', out, function(data) { // return HTML for new container
			document.getElementById("Deck").innerHTML = data.html; // reset html
		});
	}
}

function edit_copy() {

}

function edit_paste() {

}

function edit_insert() {

}