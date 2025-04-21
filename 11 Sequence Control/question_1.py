"""
Assume that 
    class Id in AST is declared with field name in str type. 
    The visitor CodeGeneration has field emit keeping an object of Emitter 
    Object is passed to the parameter o of visitId has 3 fields:
        Field frame keeps object Frame. 
        Field sym of the argument keeps a list of Symbol which has three fields: name (str type), mtype (Type type) and value (Val type). The Val type has two concrete classes: Index with field value in int type and CName with field value in str type. An Index object keeps the index of the variable while a CName keeps the name of the class name (used for global variable). The first element of sym contains the identifier which belongs to the innermost referencing environment while the last element of sym contains one in the outermost referencing environment (global).
        Field isLeft in boolean type indicates the identifier in the left (isLeft true) or in the right (isLeft false).
The method visitId must return a pair of jasmin code to read or write value of the identifier and the type of the identifier (one object of a subclass of class Type)
Based on the above assumption, write method visitId(self,ctx,o) of visitor CodeGeneration? Your code is at line 230.
"""
def visitId(self,ctx,o):
    id_list = list(filter(lambda x: x.name == ctx.name, o.sym))
    if id_list is None: 
        pass
    
    id_ = id_list[0]
    if o.isLeft:
        if type(id_.value) == Index:
            return self.emit.emitWRITEVAR(id_.name, id_.mtype, id_.value.value, o.frame), id_.mtype
        elif type(id_.value) == CName:
            return self.emit.emitPUTSTATIC(id_.value.value + '/' + id_.name, id_.mtype,o.frame), id_.mtype
    else:
        if type(id_.value) == Index:
            return self.emit.emitREADVAR(id_.name, id_.mtype, id_.value.value, o.frame), id_.mtype
        elif type(id_.value) == CName:
            return self.emit.emitGETSTATIC(id_.value.value + '/' + id_.name, id_.mtype,o.frame), id_.mtype