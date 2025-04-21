"""
Assume that 
    class Id in AST is declared with field name in str type. 
    The visitor CodeGeneration has field emit keeping an object of Emitter 
    Object Frame is kept in field frame of the argument passed to parameter o of visitId. In addition, field sym of the argument keeps a list of Symbol which has three fields: name (str type), mtype (Type type) and value (Val type). The Val type has two concrete classes: Index with field value in int type and CName with field value in str type. An Index object keeps the index of the variable while a CName keeps the name of the class name (used for global variable). The first element of sym contains the identifier which belongs to the innermost referencing environment while the last element of sym contains one in the outermost referencing environment (global).
    The method visitId must return a pair of jasmin code of a read value of the identifier onto the operand stack and the type of the identifier (one object of a subclass of class Type)
Based on the above assumption, write method visitId(self,ctx,o) of visitor CodeGeneration? Your code is at line 160.
Remind that class Type has subclasses: IntType, FloatType, VoidType, StringType, ArrayType.
"""
def visitId(self,ctx,o):
    lst_ = [x for x in o.sym if x.name == ctx.name]
    id_ = lst_[0]
    if isinstance(id_.value, Index):
        return self.emit.emitREADVAR(id_.name, id_.mtype,id_.value.value, o.frame), id_.mtype
    elif isinstance(id_.value, CName):
        return self.emit.emitGETSTATIC(id_.value.value + '/'+id_.name, id_.mtype, o.frame), id_.mtype