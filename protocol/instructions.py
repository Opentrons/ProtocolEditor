#!/user/bin/python 
# from moves import transfer, distribute, consolidate, mix
# from copy import copy, deepcopy
from collections import OrderedDict
import json


class Instructions():
    """Instructions class
    The instructions section takes the form:
    "instructions": [
        {
          "tool": "p200",
          "groups": [
            {
              "transfer": [
                {
                  "from": {
                    "container": "trough",
                    "location": "A1",
                    "tip-offset": -2,
                    "delay" : 2000,
                    "touch-tip" : true
                  },
                  "to": {
                    "container": "plate-1",
                    "location": "A1",
                    "touch-tip" : true
                  },
                  "volume": 100,
                  "blowout" : true,
                  "extra-pull" : true
                }
              ]
            },
            {
              "distribute":
              {
                "from": {
                  "container": "trough",
                  "location": "A1"
                },
                "to": [
                  {
                    "container": "plate-2",
                    "location": "A2",
                    "volume" : 20,
                    "touch-tip" : true
                  },
                  {
                    "container": "plate-2",
                    "location": "A3",
                    "volume" : 30,
                    "touch-tip" : true
                  },
                  {
                    "container": "plate-2",
                    "location": "A4",
                    "volume" : 100,
                    "touch-tip" : true
                  }
                ],
                "blowout" : true
              }
            },
            {
              "consolidate":
              {
                "from": [
                  {
                    "container": "plate-2",
                    "location": "A2",
                    "volume" : 20,
                    "touch-tip" : true
                  },
                  {
                    "container": "plate-2",
                    "location": "A3",
                    "volume" : 30,
                    "touch-tip" : true
                  },
                  {
                    "container": "plate-2",
                    "location": "A4",
                    "volume" : 100,
                    "touch-tip" : true
                  }
                ],
                "to": {
                  "container": "plate-3",
                  "location": "A5",
                  "touch-tip" : true
                },
                "blowout" : true
              }
            },
            {
              "mix": [
                {
                  "container": "plate-1",
                  "location": "A5",
                  "volume" : 100,
                  "repetitions" : 5,
                  "blowout" : true,
                  "liquid-tracking" : true
                }
              ]
            }
          ]
        }
      ]
    
    """
    
    def __init__(self, instructions_section):
        """Initialize with information attributes from 'instructions' JSON section.
    
        """
        self.instructions_section = instructions_section

    #note that this rendering does not add "instructions" prefix
    def render_as_json(self):
        return json.dumps(self.instructions_section, indent=2)
    
    
    #function to generate default objects
    def get_default_move(self, obj_type):
        """default move object factory by object type
        
        obj_type is a string with values: 'transfer', 'distribute', 'consolidate' or 'mix'
        
        """
        if obj_type == 'transfer':
            #generate from_dict object
            #make into a list
            fc = ('container','from_container_name')
            fl = ('location','A1')
            fto = ('tip-offset', -2)
            fd = ('delay', 2000)
            ftt = ('touch-tip', True)
            from_dict = OrderedDict([fc,fl,fto,fd,ftt])
            from_list = []
            from_list.extend([from_dict,from_dict,from_dict])
            
            #generate to_dict object
            #make into a list
            tc = ('container','to_container_name')
            tl = ('location','A1')
            ttt = ('touch-tip', True)
            to_dict = OrderedDict([tc,tl,ttt])
            to_list = []
            to_list.extend([to_dict,to_dict,to_dict])
            
            #define attributes
            v = ('volume',100)
            b = ('blowout', True)
            ep = ('extra-pull', True)
            
            #aggregate into complete group object
            move_element = OrderedDict([('from',from_dict),('to',to_dict),v,b,ep])
            group_obj = {'transfer' : [move_element,move_element,move_element]}
            
        elif obj_type == 'distribute':
            #generate from_dict object
            fc = ('container','from_container_name')
            fl = ('location','A1')
            # fto = ('tip-offset', -2)
            # fd = ('delay', 2000)
            # ftt = ('touch-tip', True)
            # from_dict = OrderedDict([fc,fl,fto,fd,ftt])
            from_dict = OrderedDict([fc,fl])
            
            #generate to_dict object
            #make into a list
            tc = ('container','to_container_name')
            tl = ('location','A1')
            v = ('volume',100)  #added to transfer
            ttt = ('touch-tip', True)
            # to_dict = OrderedDict([tc,tl,ttt])
            to_dict = OrderedDict([tc,tl,v,ttt])
            to_list = []
            to_list.extend([to_dict,to_dict,to_dict])
            
            #define attributes
            #v = ('volume',100)
            b = ('blowout', True)
            #ep = ('extra-pull', True)
            
            #aggregate into complete group object
            # group_obj = OrderedDict([('From',from_dict),('To',to_dict),v,b,ep])
            group_obj = OrderedDict([('From',from_dict),('To',to_list),b])
            
        elif obj_type == 'consolidate':
            #generate from_dict object
            #make into a list
            fc = ('container','from_container_name')
            fl = ('location','A1')
            # fto = ('tip-offset', -2)
            # fd = ('delay', 2000)
            v = ('volume',100)  #added to transfer
            ftt = ('touch-tip', True)
            # from_dict = OrderedDict([fc,fl,fto,fd,ftt])
            from_dict = OrderedDict([fc,fl,v,ftt])
            from_list = []
            from_list.extend([from_dict,from_dict,from_dict])
            
            #generate to_dict object
            tc = ('container','to_container_name')
            tl = ('location','A1')
            ttt = ('touch-tip', True)
            to_dict = OrderedDict([tc,tl,ttt])
            
            #define attributes
            #v = ('volume',100)
            b = ('blowout', True)
            #ep = ('extra-pull', True)
            
            #aggregate into complete group object
            # group_obj = OrderedDict([('From',from_dict),('To',to_dict),v,b,ep])
            group_obj = OrderedDict([('From',from_list),('To',to_dict),b])
        elif obj_type == 'mix':
            pass
        
        return group_obj


    #editing methods
    def delete_by_index(self, idx1, idx2):
        """deletes an item in the instructions section at Level 2 corresponding to an
        dict item in the groups list
        
        idx1 and idx2 are integers
        1.  idx1 and idx2 are returned from ajax using html id of the form "instructions.idx1.idx2"  ex: "instructions.1.1"
        2.  the dict for the revised instructions_section is returned
        
        """
        try:
            #print '\n\nSelected Group:', self.instructions_section[idx1]['groups'][idx2],'\n\n'
            del self.instructions_section[idx1]['groups'][idx2]
            msg = 'OK'
        except Exception as e:
            msg = e.strerror
            # print 'errmsg=',msg
        finally:
            # return {'instructions' : {key:msg}}	# section temporarily commented pending error response requirement
            return self.render_as_json()

    def add_transfer(self, idx1):
        """append an instructions value/object to the ordered instructions dict at Level 1
        
        1. idx1 gives the tool object
        1.  new_instructions_dict is the instructions dict containing the new instructions key and attributes
        2.  new_instructions_dict is of the form (for a transfer):
            {
              "transfer": [
                {
                  "from": {
                    "container": "trough",
                    "location": "A1",
                    "tip-offset": -2,
                    "delay" : 2000,
                    "touch-tip" : true
                  },
                  "to": {
                    "container": "plate-1",
                    "location": "A1",
                    "touch-tip" : true
                  },
                  "volume": 100,
                  "blowout" : true,
                  "extra-pull" : true
                }
              ]
            }
        3.  the dict for the revised instructions_section is returned
        """
        # #generate from_dict object
        # fc = ('container','from_container_name')
        # fl = ('location','A1')
        # fto = ('tip-offset', -2)
        # fd = ('delay', 2000)
        # ftt = ('touch-tip', True)
        # from_dict = OrderedDict([fc,fl,fto,fd,ftt])
        # 
        # #generate to_dict object
        # tc = ('container','to_container_name')
        # tl = ('location','A1')
        # ttt = ('touch-tip', True)
        # to_dict = OrderedDict([tc,tl,ttt])
        # 
        # #define attributes
        # v = ('volume',100)
        # b = ('blowout', True)
        # ep = ('extra-pull', True)
        # 
        # #aggregate into complete group object
        # group_obj = OrderedDict([('From',from_dict),('To',to_dict),v,b,ep])
        group_obj = self.get_default_move('transfer')
        
        #add to instructions section and return rendered section
        self.instructions_section[idx1]['groups'].append(group_obj)
        return self.render_as_json()
    
    def insert_transfer(self, idx1, idx2):
        """append an instructions value/object to the ordered instructions dict at Level 1
        
        1. idx1 gives the tool object index.
        2. idx2 gives the insertion point in the groups list, with new transfer inserted before idx2
        3.  new_instructions_dict is the instructions dict containing the new instructions key and attributes
        4.  new_instructions_dict is of the form (for a transfer):
            {
              "transfer": [
                {
                  "from": {
                    "container": "trough",
                    "location": "A1",
                    "tip-offset": -2,
                    "delay" : 2000,
                    "touch-tip" : true
                  },
                  "to": {
                    "container": "plate-1",
                    "location": "A1",
                    "touch-tip" : true
                  },
                  "volume": 100,
                  "blowout" : true,
                  "extra-pull" : true
                }
              ]
            }
        3.  the dict for the revised instructions_section is returned
        """
        #generate from_dict object
        fc = ('container','from_container_name')
        fl = ('location','A1')
        fto = ('tip-offset', -2)
        fd = ('delay', 2000)
        ftt = ('touch-tip', True)
        from_dict = OrderedDict([fc,fl,fto,fd,ftt])
        
        #generate to_dict object
        tc = ('container','to_container_name')
        tl = ('location','A1')
        ttt = ('touch-tip', True)
        to_dict = OrderedDict([tc,tl,ttt])
        
        #define attributes
        v = ('volume',100)
        b = ('blowout', True)
        ep = ('extra-pull', True)
        
        #aggregate into complete group object
        group_obj = OrderedDict([('From',from_dict),('To',to_dict),v,b,ep])
        
        #insert into instructions section and return rendered section
        self.instructions_section[idx1]['groups'].insert(idx2, group_obj)
        return self.render_as_json()

            