#!/user/bin/python 
from moves import transfer, distribute, consolidate, mix
from copy import copy, deepcopy


class Instructions():
    """Instructions class
    
    """
    
    inst_list = []
    
    def get_index(**kwargs):
        index = 2
        return index

    #editing methods
    #add/append
    @method
    def add(self, **kwargs):
        """appends a new instruction at the end of the instructions array
        
        """
        self.inst_list.append(move)
        
    #delete
    @method
    def delete(self, **kwargs):
        """deletes a specified instruction at the specified uid
        
        """
        j = get_index(uid)
        del self.inst_list[j]
        
    #copy
    @method
    def copy(self, **kwargs):
        """ copies (deep copy) and returns a specified instruction
            at the specifie uid
        """
        j = get_index(uid)
        return deepcopy(self.inst_list[j])
         
    #insert
    @method
    def insert(self, **kwargs):
        """inserts an instruction into the inst_list above specified uid
        """
        j = get_index(uid)
        self.inst_list.insert(j,move)
        
    
    #paste
    @method
    def paste(self, **kwargs):
        """same as insert except multiple distinct replicates can be pasted
        """
        j = get_index(**kwargs)
        for i in range(0, n-1):
            new_move = deepcopy(self.inst_list[uid])
            self.inst_list.insert(j,new_move)
            
    #replicate
    
    
    #modify
    @method
    def modify(self,**kwargs):
        """modifies the attributes of a single instruction
        """
        
        j = get_index(uid)
        cur_move = self.inst_list[j]
        
        #function to establish type of instruction
        #function to populate move parameters given the type from **kargs
        
        
    