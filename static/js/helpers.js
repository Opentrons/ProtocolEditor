
function collapse(elID, clicked) { //partially replaced by modals already, hopefully deprecated soon
	//hide the section and change the text of the hide/show link
	var e = document.getElementById(elID);
	if(e.style.display != 'none') {
		e.style.display = 'none';
		clicked.innerHTML = 'show';
	} else {
		e.style.display = 'block';
		clicked.innerHTML = 'hide';
	}
}

function removeDiv(elID, clicked) {
	var alertString = "Are you sure you want to delete this element?";
	alertString += "\n\nThis will delete this element and ALL dependent elements.";

	if(confirm(alertString)){
		var divList = document.getElementsByClassName(elID);
		for(var i=0; i<divList.length; i++){ //go through each block with the name and delete it if it corresponds to the delete button clicked
			if(divList[i].contains(clicked)){
				divList[i].remove();
			}
		}
	}
}

function showAddBox(elID, clicked) { //partially replaced by modals already, hopefully deprecated soon
	document.getElementById(elID).style.display = 'block';
	clicked.innerHTML = '';
}

function confirmProcess(proceedID) {
	//check the hidden form element "proceedID" to see if there has been a file loaded already
	//if a file has been loaded, "proceedID" will say "no", leading the user to confirm the scheduled load
	//if no file is loaded (new session), it will continue without alerting the user
	var prompt = document.getElementById("proceedID").value;

	if(prompt != "yes") {
		var alertString = "Unfinished business!";
		alertString += "\nLoading a new file will erase any unsaved changes.";
		alertString += "\n\nClick 'ok' to proceed without saving.";

		if (confirm(alertString)) { //user confirmed save
			document.getElementById(proceedID).value = "yes";
		} else {
			return false;
		}
	}
}

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////

function addLine(id, firstIdentifier, secondIdentifier) {
	var newLine = '<div class="row">';
	newLine += '<div class="col-md-6">' + editable(firstIdentifier) + '</div>';
	newLine += '<div class="col-md-6">' + editable(secondIdentifier) + '</div>';
	newLine += '</div>';
	document.getElementById(id).innerHTML += newLine;
}

function addZebra(id, firstIdentifier, secondIdentifier) {
	var newLine = '<div class="row zebra">';
	newLine += '<div class="col-md-6">' + editable(firstIdentifier) + '</div>';
	newLine += '<div class="col-md-5">' + editable(secondIdentifier) + '</div>';
	newLine += '<div class="col-md-1"><a href="javascript:void(0)" onclick="removeDiv(\'zebra\', this);">&times;</a></div>';
	newLine += '</div>';
	document.getElementById(id).innerHTML += newLine;
}

function addPoint(id, firstIdentifier, secondIdentifier) {
	var newLine = '<div class="row zebra">';
	newLine += '<div class="col-md-6 ' + firstIdentifier + '">f1</div>';
	newLine += '<div class="col-md-5">' + editable(secondIdentifier) + '</div>';
	newLine += '<div class="col-md-1"><a href="javascript:void(0)" onclick="removeDiv(\'zebra\', this);">&times;</a></div>';
	newLine += '</div>';
	newLine += '<div class="row zebra">';
	newLine += '<div class="col-md-6 ' + firstIdentifier + '">f2</div>';
	newLine += '<div class="col-md-5">' + editable(secondIdentifier) + '</div>';
	newLine += '<div class="col-md-1"><a href="javascript:void(0)" onclick="removeDiv(\'zebra\', this);">&times;</a></div>';
	newLine += '</div>';
	document.getElementById(id).innerHTML += newLine;
}

//helper method
function editable(blockName) {
  var out = '\
  <div class="edit-in-place modalComponent mode-display"> \
    <div class="mode display"> \
      <span class="edit-handle value ' + blockName + '" style="cursor:pointer;"><span style="color:#fb3f0f">[ Undefined ]</span></span> \
    </div> \
    <div class="mode edit"> \
      <form action="/user/1/edit" method="post"> \
        <input type="text" value="" name="name" class="edit-input" /> \
        <input type="submit" value="Save" class="btn tron-red" style="padding:0px 10px 0px 10px;font-size:10px;" /> \
      </form> \
    </div> \
  </div>';
  return out;
}

