Sugar.addModal('edit-in-place', {

	display: function(mode, modal) {
	
		// '.edit' -> '.edit-in-place.modal .mode-display .edit'	
		mode.listen('.edit-handle', 'click', function(evt, parentMode, parentModal) {
			evt.stop();
			parentModal.setMode('edit');
			var input   = parentModal.find('input[type=text]');
			input.value = parentModal.find('.value').innerHTML;

			input.setFocus();
			input.selectAll();
		});
	
	},

	edit: function(mode, modal) {

		// 'form' -> '.edit-in-place.modal .mode-edit form'
		mode.listen('form', 'submit', function(evt, parentMode, parentModal) {
			evt.stop();
			var newValue = parentMode.find('input[type=text]').el.value;
			var display  = parentModal.find('.value');
			display.el.innerHTML = newValue;
			parentModal.setMode('display');
		});

	}

});

Sugar.addModal('add-in-place', {

	button: function(mode, modal) {
	
		mode.listen('.add-handle', 'click', function(evt, parentMode, parentModal) {
			evt.stop();
			parentModal.setMode('add');
			var input   = parentModal.find('input[type=text]');
			input.value = parentModal.find('.value').innerHTML;

			input.setFocus();
			input.selectAll();
		});
	
	},

	add: function(mode, modal) { 
		mode.listen('.add-handle', 'click', function(evt, parentMode, parentModal) {
			evt.stop();
			parentModal.setMode('button');
		});
	}

});

Sugar.addModal('collapse-in-place', {

	expanded: function(mode, modal) {
	
		mode.listen('.collapse-handle', 'click', function(evt, parentMode, parentModal) {
			evt.stop();
			parentModal.setMode('collapsed');
		});
	
	},

	collapsed: function(mode, modal) { 
		mode.listen('.collapse-handle', 'click', function(evt, parentMode, parentModal) {
			evt.stop();
			parentModal.setMode('expanded');
		});
	}

});