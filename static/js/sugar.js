Sugar = {};

Sugar.modals = {};

Sugar.Element = function(el) {
	this.el = el;
};

Sugar.Element.prototype = {

	hasClass: function(className) {
		var regex = new RegExp('\\b'+className+'\\b');
		return regex.test(this.el.className);
	},

	addClass: function(className) {
		if (!this.hasClass(className)) {
			this.el.className += " " + className;
		}
	},

	removeClass: function(className) {
		var regex = new RegExp('\\b'+className+'\\b');
		this.el.className = this.el.className.replace(regex, '');
	},

	matches: function(selector, compareTo) {
		var needle = compareTo || this.el;
		try {
			var els = document.querySelectorAll(selector);
		} catch(e) {
			throw new Error("Invalid CSS selector: "+selector);
		}
		for (var i in els) {
			if (els[i]===needle) return true;
		}
		return false;
	},

	find: function(selector) {
		return new Sugar.Element(this.el.querySelector(selector));
	},

	getParent: function(selector) {
		if (this.matches(selector)) {
			return this;
		}
		var parent = this.el;
		while (parent = parent.parentNode) {
			if (this.matches(selector, parent)) {
				return new Sugar.Element(parent);
			}
		}
		return false;
	},

	setMode: function(mode) {
		var modalRoot = this.getParent('.modalComponent');
		modalRoot.el.className = modalRoot.el.className.replace(/\bmode-\w+\b/, '');
		modalRoot.addClass('mode-'+mode);
	}

};

Sugar.Event = function(e) {
	this.e = e;
};

Sugar.Event.prototype = {

	stop: function() {
		this.e.cancelBubble = true;
		if (this.e.stopPropagation) {
			this.e.stopPropagation();
		}
		if (this.e.preventDefault) {
			this.e.preventDefault();
		}
	}

};

Sugar.delegateEvent = function(selector, eventType, fun) {
	var root = document.body;
	root.addEventListener(eventType, function(e) {
		var suspects = root.querySelectorAll(selector);
		var target = e.target;
		for (var i = 0, l = suspects.length; i < l; i++) {
			var el = target;
			var p  = suspects[i];
			while(el && el !== root) {
				if (el === p) {
					e = new Sugar.Event(e);
					e.stop();
					fun.call(p, e, new Sugar.Element(el));
				}
				el = el.parentNode;
			}
		}
		return false;
	});
}

Sugar.Modal = function(name, modes) {

	this.modes = {};
	this.name  = name;
	this.sel   = ".modalComponent."+this.name;

	// Go through all the listed modes and run through their initializers. 
	for(var modeName in modes) {
		this.addMode(modeName, modes[modeName]);
	}

};

Sugar.Modal.prototype = {

	addCSSRule: function(rule) {
		var cssID  = 'sugar_dynamic-modal-css';
		var css = document.getElementById(cssID);
		if (!css) {
			css = document.createElement('style');
			css.innerHTML = '.modalComponent .mode { display: none; }\n';
			css.id = cssID;
			document.body.appendChild(css);
		}
		css.innerHTML += rule+'\n';
	},

	addMode: function(name, init) {
		this.modes[name] = new Sugar.Mode(name, this, init);
		this.addCSSRule(this.sel+'.mode-'+name+' .mode.'+name+' { display: block; }')
	}

};

Sugar.Mode = function(modeName, modal, init) {
	this.modal     = modal;
	this.modalName = modal.name;
	this.name  = modeName;
	this.scope     = '.mode.'+modeName;
	init(this, modal);
};

Sugar.Mode.prototype = {

	listen: function(selector, eventName, callback) {
		var scope = '.modalComponent.'+this.modalName+' '+this.scope;
		var modeName = this.name;
		Sugar.delegateEvent(scope+' '+selector, eventName, function(e, el) {
			e.stop();
			var parentMode  = el.getParent('.mode.'+modeName);
			var parentModal = el.getParent('.modalComponent');
			callback.apply(this, [e, parentMode, parentModal]);
		});
	}

};

Sugar.addModal = function(name, modals) {
	this.modals[name] = new Sugar.Modal(name, modals);
};