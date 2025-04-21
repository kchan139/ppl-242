"""
Assume that 
    class VarDecl in AST is declared with field name in str type, typ in Type type. 
    The visitor CodeGeneration has field emit keepinasg an object of Emitter 
    Field frame of the argument passed to parameter o of visitVarDecl contains object Frame for a local/parameter declaration and None for a global declaration.
    The method visitVarDecl must print out a directive declaration in jasmin code (use method printout(str) of Emitter) and returns an object of Symbol which has field name in str type, mtype in Type type and val in Val type. The Val type has 2 concrete classes: Index with field value in int type  (contain index of variable) and CName with field value in str type (contains name of the class which can get from self.className)
Based on the above assumption, write method visitVarDecl(self,ctx,o) of visitor CodeGeneration? Your code is at line 160.
Remind that class Type has subclasses: IntType, FloatType, StringType, ArrayType.
"""
def visitVarDecl(self, ctx, o):
    if o.frame:
        idx = o.frame.getNewIndex()
        self.emit.printout(self.emit.emitVAR(idx, ctx.name, ctx.typ, o.frame.getStartLabel(),o.frame.getEndLabel()))
        return Symbol(ctx.name, ctx.typ, Index(idx))
    
    self.emit.printout(self.emit.emitATTRIBUTE(ctx.name, ctx.typ, False))
    return Symbol(ctx.name, ctx.typ, CName(self.className))