"""
Assume that 
    class If(Stmt) in AST is declared with fields expr  in Expr type; tstmt and estmt in Stmt type.  In case the if statement has no else, the estmt gets None value. 
    The visitor CodeGeneration has field emit keeping an object of Emitter 
    Object is passed to the parameter o of visitId has 2 fields:
        Field frame keeps object Frame. 
        Field sym of the argument keeps a list of Symbol which has three fields: name (str type), mtype (Type type) and value (Val type). The Val type has two concrete classes: Index with field value in int type and CName with field value in str type. An Index object keeps the index of the variable while a CName keeps the name of the class name (used for global variable). The first element of sym contains the identifier which belongs to the innermost referencing environment while the last element of sym contains one in the outermost referencing environment (global).
    When visiting the expression of the if statement, object Access must be passed to parameter o where Access has 3 fields:
        frame and sym are similar to the object passed to parameter o 
        Field isLeft in boolean type indicates the identifier in the left (isLeft true) or in the right (isLeft false).
The method visitIf must print out the code of the if statement (use method printout of Emitter)
Based on the above assumption, write method visitIf(self,ctx,o) of visitor CodeGeneration? Your code is at line 230.
"""
def visitIf(self, if_stmt, context):
    # tuple(code, type)
    condition_code, _ = self.visit(if_stmt.expr, Access(context.frame, context.sym, False))
    end_label = context.frame.getNewLabel()
    false_label = context.frame.getNewLabel()

    if if_stmt.estmt:
        self.emit.printout(condition_code)
        self.emit.printout(self.emit.emitIFFALSE(false_label, context.frame))
        self.visit(if_stmt.tstmt, context)
        self.emit.printout(self.emit.emitGOTO(end_label, context.frame))
        self.emit.printout(self.emit.emitLABEL(false_label, context.frame))
        self.visit(if_stmt.estmt, context)
        self.emit.printout(self.emit.emitLABEL(end_label, context.frame))
    else:
        self.emit.printout(condition_code)
        self.emit.printout(self.emit.emitIFFALSE(false_label, context.frame))
        self.visit(if_stmt.tstmt, context)
        self.emit.printout(self.emit.emitLABEL(false_label, context.frame))