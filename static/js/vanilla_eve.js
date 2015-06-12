function elementSugar(el) {

	if (!el) {
		return el;
	}

	if (el.hasClass && el.addClass && el.removeClass) {
		return el;
	}
	
	el.hasClass = function (className) {
		var regex = new RegExp('\\b'+className+'\\b');
		return regex.test(regex);
	}

	el.addClass = function(className) {
		if (!el.hasClass(className)) {
			el.className += " " + className;
		}
	}

	el.removeClass = function(className) {
		var regex = new RegExp('\\b'+className+'\\b');
		el.className = el.className.replace(regex, '');
	}

	el.swapClass = function(current, replace) {
		el.removeClass(current);
		el.addClass(replace);
	};

	el.matches = function(selector, el) {
		var els = document.querySelectorAll(selector);
		for (var i in els) {
			if (els[i]===el) return true;
		}
		return false;
	}

	el.find = function(selector) {
		return elementSugar(el.querySelector(selector));
	}

	el.getParent = function(selector) {
		var parent = el;
		while (parent = parent.parentNode) {
			if (el.matches(selector, parent)) {
				return elementSugar(parent);
			}
		}
	}

	return el;

}

function eventSugar(e) {
	e.stop = function() {
		e.cancelBubble = true;
		if (e.stopPropagation) {
			e.stopPropagation();
		}
		if (e.preventDefault) {
			e.preventDefault();
		}
	}
	return e;
}

/**
 * Super simple event delegation routine.
 */
function delegateEvent(selector, eventType, fun) {
	var root = root || document.body;
	root.addEventListener(eventType, function(e) {
		var suspects = root.querySelectorAll(selector);
		var target = e.target;
		for (var i = 0, l = suspects.length; i < l; i++) {
			var el = target;
			var p  = suspects[i];
			while(el && el !== root) {
				if (el === p) {
					return fun.call(p, eventSugar(e), elementSugar(el));
				}
				el = el.parentNode;
			}
		}
		return false;
	});
}

// All you need to do!
delegateEvent('.edit-in-place.mode-display .edit', 'click', function(e, el) {
	e.stop();
	el.getParent('.edit-in-place').swapClass('mode-display', 'mode-edit');
});

delegateEvent('.edit-in-place.mode-edit form', 'submit', function(e, el) {
	e.stop();
	parent = el.getParent('.edit-in-place');
	parent.swapClass('mode-edit', 'mode-display');
	var input   = parent.find('.when-edit').find('input[type=text]');
	var display = parent.find('.when-display').find('.value');
	display.innerHTML = input.value;
});
