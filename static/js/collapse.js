//collapse sections on click for ease of reading
function collapse(id, clicked) {
	//hide the section and change the text of the hide/show link
	var e = document.getElementById(id);
	if(e.style.display != 'none') {
		e.style.display = 'none';
		clicked.innerHTML = 'show';
	} else {
		e.style.display = 'block';
		clicked.innerHTML = 'hide';
	}
}