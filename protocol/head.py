from collections import OrderedDict
import json

class Head():
	"""
	Top-level head item holds the attributes that are specified at the head of
	each JSON protocol document.

	# "head" : {
	#   "p200" : {
	#     "tool" : "pipette",
	#     "tip-racks" : [
	#       {
	#         "container" : "p200-rack"
	#       }
	#     ],
	#     "trash-container" : {
	#       "container" : "trash"
	#     },
	#     "multi-channel" : True,
	#     "axis" : "a",
	#     "volume" : 250,
	#     "down-plunger-speed" : 300,
	#     "up-plunger-speed" : 500,
	#     "tip-plunge" : 8,
	#     "extra-pull-volume" : 20,
	#     "extra-pull-delay" : 200,
	#     "distribute-percentage" : 0.1,
	#     "points" : [
	#       {
	#         "f1" : 10,
	#         "f2" : 6
	#       },
	#       {
	#         "f1" : 25,
	#         "f2" : 23
	#       },
	#       {
	#         "f1" : 50,
	#         "f2" : 49
	#       },
	#       {
	#         "f1" : 200,
	#         "f2" : 200
	#       }
	#     ]
	#   }
	# }
	
	this object holds the key="head" value as a complete python OrderedDict
	"""

	def __init__(self, head_section):
		"""
		Initialize with information attributes from 'head' JSON section.
		"""
		self.head_section = head_section
		self.attributes = OrderedDict()

		for key in self.head_section:
			self.attributes[key] = self.head_section[key]

	#note that this rendering does not add "head" prefix
	def render_as_json(self):
		return json.dumps(self.head_section, indent=2)


	#editing methods
	
	def delete_tiprack(self, idx1, idx2):
		"""deletes a tiprack obj, specified by idx2 in the tip-racks list for
		a head object specified by idx1
		
		"""
		try:
			print '\n\nhead delete_tiprack\n\n'
			key = self.head_section.keys()[idx1]		#get the pipette key from the index
			if self.head_section.has_key(key):
				del self.head_section[key]['tip-racks'][idx2]
		except Exception as e:
			msg = e.strerror
			print '\n\nhead delete_tiprack errmsg=',msg, '\n\n'
		finally:
			# return {'head' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def delete_by_index(self, idx):
		"""deletes an item in the head section at Level 1
		idx is an integer
		1.  idx is returned from ajax using html id of the form "head.idx"  ex: "head.0"
		2.  idx is converted into the key of the head value/object to be deleted
		3.  the dict for the revised head_section is returned
		
		"""
		try:
			print '\n\nhead delete_by_index\n\n'
			key = self.head_section.keys()[idx]		#get the key from the index
			if self.head_section.has_key(key):
				del self.head_section[key]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			print '\n\nhead delete_by_index errmsg=',msg, '\n\n'
		finally:
			# return {'head' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def add_tiprack(self, idx):
		"""adds a tiprack obj in the tip-racks list for a head object specified by idx
		
		"""
		try:
			print '\n\nhead add_tiprack\n\n'
			tr = {"container" : "p200-rack"}	#default tip-rack
			key = self.head_section.keys()[idx]		#get the key from the index
			if self.head_section.has_key(key):
				self.head_section[key]["tip-racks"].append(tr)
				
		except Exception as e:
			msg = e.strerror
			print '\n\nhead add_tiprack errmsg=',msg, '\n\n'
		finally:
			# return {'head' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def add(self):
		"""append an head value/object to the ordered head dict at Level 1
		1.  new_head_dict is the head dict containing the new head key and attributes
		2.  new_head_dict is of the form:
				{"P200" :
					{"tool" : "pipette",
					"tip-racks" : [{"container" : "p200-rack"}],
					"trash-container" : {"container" : "trash"},
					"multi-channel" : True,
					"axis" : "a",
					"volume" : 250,
					"down-plunger-speed" : 300,
					"up-plunger-speed" : 500,
					"tip-plunge" : 8,
					"extra-pull-volume" : 20,
					"extra-pull-delay" : 200,
					"distribute-percentage" : 0.1,
					"points" : [
						{"f1" : 10,"f2" : 6},
						{"f1" : 25,"f2" : 23},
						{"f1" : 50,"f2" : 49},
						{"f1" : 200,"f2" : 200}
						]
					}
				}
		3.  the dict for the revised head_section is returned
		
		"""
		try:
			print '\n\nhead add\n\n'
			name = "tool_name"
			t = ("tool", "pipette")
			tr = ("tip-racks",[{"container" : "tiprack_name"}])
			tc = ("trash-container","trash_container_name")
			mc = ("multi-channel", True)
			a = ("axis", "a")
			v = ("volume", 250)
			dps = ("down-plunger-speed", 300)
			ups = ("up-plunger-speed", 500)
			tp = ("tip-plunge", 8)
			epv = ("extra-pull-volume", 20)
			epd = ("extra-pull-delay", 200)
			dp = ("distribute-percentage", 0.1)
			p = ("points",[{"f1" : 10,"f2" : 6},
						{"f1" : 25,"f2" : 23},
						{"f1" : 50,"f2" : 49},
						{"f1" : 200,"f2" : 200}])
			
			new_head_dict = OrderedDict([t,tr,tc,mc,a,v,dps,ups,tp,epv,epd,dp,p])
			self.head_section[name] = new_head_dict
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			print '\n\nhead add errmsg=',msg, '\n\n'
		finally:
			# return {'head' : {key:msg}}	#need error requirments
			return self.render_as_json()
		
	def modify_by_index_index_key(self, idx1, idx2, new_head_dict):
		"""modify an attribute, by name(key2), for an head list element, selected by index idx2,
			for a reagent, selected by index(idx1) in the head_section ordered dict
		1.  new_head_dict is of the form {"key2" : value (string or integer)}
		2.  nothing is returned since the GUI already contains the changes
		
		"""
		try:
			print '\n\nhead modify_by_index_index_key\n\n'
			key1 = self.head_section.keys()[idx1]
			key2 = new_head_dict.keys()[0]
			#print "\n\nidx1=",idx1, "  idx2=",idx2, "  key1=",key1,"  key2=", key2
			self.head_section[key1][idx2][key2] = new_head_dict[key2]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			print '\n\nhead modify_by_index_index_key errmsg=',msg, '\n\n'
		finally:
			# return {'head' : {key:msg}}	# section temporarily commented pending error response requirement
			pass

	def fix_logical(self, in_val):
		"""function to convert quoted logical values
			to python format
		
		"""
		out_val = None
		print '\n\nin_val:', in_val
		print '\n\nin_val is string?:', isinstance(in_val, basestring)
		if isinstance(in_val, basestring):
			out_val = in_val.strip() in ['True', 'true']
		elif isinstance(in_val, bool):
			out_val = in_val
		else:
			out_val = None
		return out_val
		
	def modify_by_block(self, idx, data):
		"""modifies an item in the head section at Level 1
		idx is an integer
		1.  idx is returned from ajax using html id of the form "head.idx"  ex: "head.0"
		2.  idx is converted into the key of the head value/object to be modified
		3.  data is the head dict block that was modified in the gui
		4.  the dict for the entire revised head_section is returned
		
		"""
		try:
			print '\n\nhead modify_by_block\n\n'
			print 'data is:\n\n', data
			name = data.keys()[0]		#get the tool name in the data block
			print 'name is: ', name

			if self.head_section.has_key(name):
				self.head_section[name] = data[name]		#name didn't change, so use it
			else:
				self.delete_by_index(idx)	#delete the existing tool
				self.head_section[name] = data[name]
				
			#make sure any quoted logical is a python logical
			mc = self.fix_logical(self.head_section[name]['multi-channel'])
			self.head_section[name]['multi-channel'] = mc

			msg = 'OK'
		except Exception as e:
			msg = e
			print '\n\nhead modify_by_block errmsg=',msg, '\n\n'
		finally:
			# return {'ingredients' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()