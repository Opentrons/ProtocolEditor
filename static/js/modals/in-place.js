Sugar.addModal('edit-in-place', {

	display: function(mode, modal) {
	
		// '.edit' -> '.edit-in-place.modal .mode-display .edit'	
		mode.listen('.edit-handle', 'click', function(evt, parentMode, parentModal) {
//			evt.stop();
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