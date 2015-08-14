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
			key = self.head_section.keys()[idx1]		#get the pipette key from the index
			if self.head_section.has_key(key):
				del self.head_section[key]['tip-racks'][idx2]
		except Exception as e:
			msg = e.strerror
			# print 'errmsg=',msg
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
			key = self.head_section.keys()[idx]		#get the key from the index
			if self.head_section.has_key(key):
				del self.head_section[key]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			# print 'errmsg=',msg
		finally:
			# return {'head' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()
		
	def add_tiprack(self, idx):
		"""adds a tiprack obj in the tip-racks list for a head object specified by idx
		
		"""
		try:
			tr = {"container" : "p200-rack"}	#default tip-rack
			
			key = self.head_section.keys()[idx]		#get the key from the index
			if self.head_section.has_key(key):
				self.head_section[key]["tip-racks"].append(tr)
				
		except Exception as e:
			msg = e.strerror
			# print 'errmsg=',msg
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
			key1 = self.head_section.keys()[idx1]
			key2 = new_head_dict.keys()[0]
			#print "\n\nidx1=",idx1, "  idx2=",idx2, "  key1=",key1,"  key2=", key2
			self.head_section[key1][idx2][key2] = new_head_dict[key2]
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
		finally:
			# return {'head' : {key:msg}}	# section temporarily commented pending error response requirement
			pass

	def modify_by_block(self, idx, data):
		"""modifies an item in the head section at Level 1
		idx is an integer
		1.  idx is returned from ajax using html id of the form "head.idx"  ex: "head.0"
		2.  idx is converted into the key of the head value/object to be modified
		3.  the dict for the revised head_section is returned
		
		"""
		try:
			name = data.keys()[0]		#get the tool name in the data block
			if self.head_section.has_key(name):
				self.head_section[name] = data[name]		#name didn't change, so use it
			else:
				self.delete_by_index(idx)	#delete the existing tool
				self.head_section[name] = data[name]
			
			msg = 'OK'
		except Exception as e:
			msg = e.strerror
			# print 'errmsg=',msg
		finally:
			# return {'ingredients' : {key:msg}}	# section temporarily commented pending error response requirement
			return self.render_as_json()