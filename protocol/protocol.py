#!/usr/bin/python

from info import Info
from deck import Deck
# import info
# import deck
# from head import Head
# from ingredients import Ingredients
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
        #deck object
        self.deck = Deck(self.prot_dict['deck'])
        #ingredients object
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
        id_parts = msg_dict["id"].split("-")
        ef = msg_dict["ef"]
        data = msg_dict["data"]
        
        section =   id_parts[0]     #get the leading section of the id
        idx1 = int(id_parts[1])
        
        if section == 'info':
            if ef == 'modify':
                self.info.modify_by_key(idx1)      #get the index
                #nothing to return
                
        elif section == 'deck':
            if  ef == 'delete':
                retVal = self.deck.delete_by_index(idx1)
            elif ef == 'add':
                retVal = self.deck.add(data)
            elif ef == 'modify':
                self.deck.modify_by_index(idx1,data)
                retVal = None   #nothing to return
            
        elif section == 'head':
            pass
        
        elif section == 'ingredients':
            pass
        
        elif section == 'instructions':
            if ef == 'copy':
                inst.copy(data)
            elif ef == 'paste':
                inst.paste(data)
            elif ef == 'modify':
                inst.modify(data)
            elif ef == 'insert':
                inst.insert(data)
            elif ef == 'delete':
                inst.delete(data)
            
            return retVal
            
    