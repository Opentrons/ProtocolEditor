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