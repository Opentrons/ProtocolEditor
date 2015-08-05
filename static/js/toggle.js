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

/*
function editValue(clicked) {
	clicked.
}
*/

function view(clicked) {
	if(clicked.classList.contains("view")){
		clicked.classList.remove("view");
	} else {
		clicked.classList.add("view");
	}
}

