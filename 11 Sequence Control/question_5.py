"""
Assume that
    class While(Stmt) in AST is declared with fields expr  in Expr type; stmt in Stmt type. \
    The visitor CodeGeneration has field emit keeping an object of Emitter 
    Object is passed to the parameter o of visitId has 2 fields:
        Field frame keeps object Frame. 
        Field sym of the argument keeps a list of Symbol which has three fields: name (str type), mtype (Type type) and value (Val type). The Val type has two concrete classes: Index with field value in int type and CName with field value in str type. An Index object keeps the index of the variable while a CName keeps the name of the class name (used for global variable). The first element of sym contains the identifier which belongs to the innermost referencing environment while the last element of sym contains one in the outermost referencing environment (global).
    When visiting the expression of the if statement, object Access must be passed to parameter o where Access has 3 fields:
        frame and sym are similar to the object passed to parameter o 
        Field isLeft in boolean type indicates the identifier in the left (isLeft true) or in the right (isLeft false).
The method visitWhile must print out the code of the while statement (use method printout of Emitter).Note generating labels for break and continue statements inside the while statement 
Based on the above assumption, write method visitWhile(self,ctx,o) of visitor CodeGeneration? Your code is at line 265 .
"""
def visitWhile(self, while_stmt, context):
    current_frame = context.frame
    current_frame.enterLoop()
    self.emit.printout(self.emit.emitLABEL(current_frame.getContinueLabel(), current_frame))

    # tuple(code, type)
    condition_code, _ = self.visit(while_stmt.expr, Access(context.frame, context.sym, False))
    self.emit.printout(condition_code)

    true_label = current_frame.getNewLabel()
    self.emit.printout(self.emit.emitIFTRUE(true_label, current_frame))
    self.emit.printout(self.emit.emitGOTO(current_frame.getBreakLabel(), current_frame))
    self.emit.printout(self.emit.emitLABEL(true_label, current_frame))

    self.visit(while_stmt.stmt, context)
    self.emit.printout(self.emit.emitGOTO(current_frame.getContinueLabel(), current_frame))
    self.emit.printout(self.emit.emitLABEL(current_frame.getBreakLabel(), current_frame))

    current_frame.exitLoop()