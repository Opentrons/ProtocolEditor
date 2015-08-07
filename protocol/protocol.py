#!/usr/bin/python

from info import Info
from deck import Deck
# import info
# import deck
from head import Head
from ingredients import Ingredients
#from instructions import Instructions
#import Instructions

from collections import OrderedDict
import json

class Protocol():
    """Protocol class for containing editable objects and handling input data structure from gui/ajax
    prot_dict is the protocol dict to be edited

    """
    
    def __init__(self, prot_dict):
        """Initialize
        
        Initialize class with the input as a raw (unparsed) JSON-esque string, and create 
        top-level (Head, Deck, Instructions, and Ingredients) items as None objects.
        """
        self.prot_dict = prot_dict

        #aggregate objects
        #info object
        self.info = Info(self.prot_dict['info'])
        #head object
        self.head = Head(self.prot_dict['head'])
        #deck object
        self.deck = Deck(self.prot_dict['deck'])
        #ingredients object
        self.ingredients = Ingredients(self.prot_dict['ingredients'])

        #instructions object - list
        #inst = Instructions()
    
    
    #export json
    #import json
    #assemble


    #method for processing edit methods from ajax
    def process_edit_msg(self, msg_dict):
        """method to process editing message
        
        1.  msg is of the form {"id" : html-id, "ef" : edit_function_string, "data" : edit_data_dict}
        2.  html-id is the id of the relevent html tag ex: "deck-2", where deck is section, 2 is index
        3.  ef is the edit function: delete, modify, add, insert, copy, paste
        4.  edit_data_dict is a dict of editing data ex: { 'plate-1":{"labware":"96-flat", "slot":"C1"}}
        
        """
        id_parts = msg_dict["id"].split(".")
        ef = msg_dict["ef"]
        data = msg_dict["data"]

        section =   id_parts[0]     #get the leading section of the id

        retVal = None # set to None so it won't raise an error if unassigned

        try:
            idx1 = int(id_parts[1])
        except Exception, e:
            print e

        if section == 'info':
            if ef == 'modify':
                self.info.modify_by_key(data)      #get the index
        
        
        # # print 'section=',section, '  idx1=',idx1, '  ef=', ef
        # 
        # if section == 'info':
        #     if ef == 'modify':
        #         idx1 = int(id_parts[1])
        #         self.info.modify_by_key(idx1)      #get the index
                #nothing to return
                
        elif section == 'deck':
            if  ef == 'delete':
                idx1 = int(id_parts[1])
                retVal = self.deck.delete_by_index(idx1)
            elif ef == 'add':
                print 'add deck'
                # retVal = self.deck.add(data)
                retVal = self.deck.add()
            elif ef == 'modify':
                idx1 = int(id_parts[1])
                self.deck.modify_by_index(idx1,data)
                retVal = None   #nothing to return
            
        elif section == 'head':
            #id has form "head.0.1.volume" for 1st pipette, 
            if ef == 'delete':
                idx1 = int(id_parts[1])
                retVal = self.head.delete_by_index(idx1)
            elif ef == 'add':
                retVal = self.head.add(data)
            elif ef == 'modify':
                idx1 = int(id_parts[1])
                idx2 = int(id_parts[2])
                self.head.modify_by_index_index_key(idx1, idx2, data)
        
        elif section == 'ingredients':
            #id has form "ingredients.2.1.volume" for 3rd reagent, 1st list element, volume attribute
            if ef == 'delete':
                idx1 = int(id_parts[1])
                retVal = self.ingredients.delete_by_index(idx1)
            elif ef == 'add':
                retVal = self.ingredients.add()
            elif ef == 'modify':
                idx1 = int(id_parts[1])
                idx2 = int(id_parts[2])
                self.ingredients.modify_by_index_index_key(idx1, idx2, data)
                
        elif section == 'instructions':
            if ef == 'copy':
                pass
            elif ef == 'paste':
                pass
            elif ef == 'modify':
                pass
            elif ef == 'insert':
                pass
            elif ef == 'delete':
                pass
            
        return retVal
            

    # method for returning the protocol object
    def get_protocol(self):
        out = '"info": %s,' % self.info.render_as_json()
        out += '"deck": %s' % self.deck.render_as_json()
        # out += '"head": %s,' % self.head.render_as_json()
        # out += '"ingredients": %s,' % self.ingredients.render_as_json()
        # out += '"instructions": %s' % self.instructions.render_as_json()

        out = json.loads("{%s}" % out, object_pairs_hook=OrderedDict) # load into JSON object, preserving order
        
        # export as nicely spaced and indented JSON object (false is ordered, true is not..?)
        return json.dumps(out, indent=4, sort_keys=False)

    
    