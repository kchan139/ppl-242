"""
Assume that
    class For(Stmt) in AST is declared with fields idx in Id, ini, end, upd  in Expr type; stmt in Stmt type. \
    The visitor CodeGeneration has field emit keeping an object of Emitter 
    Object is passed to the parameter o of visitId has 2 fields:
        Field frame keeps object Frame. 
        Field sym of the argument keeps a list of Symbol which has three fields: name (str type), mtype (Type type) and value (Val type). The Val type has two concrete classes: Index with field value in int type and CName with field value in str type. An Index object keeps the index of the variable while a CName keeps the name of the class name (used for global variable). The first element of sym contains the identifier which belongs to the innermost referencing environment while the last element of sym contains one in the outermost referencing environment (global).
    When visiting the expression of the if statement, object Access must be passed to parameter o where Access has 3 fields:
        frame and sym are similar to the object passed to parameter o 
        Field isLeft in boolean type indicates the identifier in the left (isLeft true) or in the right (isLeft false).
The method visitFor must print out the code of the for statement (use method printout of Emitter).Note generating labels for break and continue statements inside the for statement 
Based on the above assumption, write method visitFor(self,ctx,o) of visitor CodeGeneration? Your code is at line 280 .
"""
def visitFor(self, for_stmt, context):
    current_frame = context.frame
    current_frame.enterLoop()

    break_label = current_frame.getBreakLabel()
    continue_label = current_frame.getContinueLabel()
    loop_start_label = current_frame.getNewLabel()

    loop_variable = for_stmt.idx
    initialization_code, _ = self.visit(for_stmt.ini, Access(current_frame, context.sym, False))
    self.emit.printout(initialization_code)

    loop_variable_code, _ = self.visit(loop_variable, Access(current_frame, context.sym, True))
    self.emit.printout(loop_variable_code)
    self.emit.printout(self.emit.emitLABEL(loop_start_label, current_frame))

    loop_variable_code, _ = self.visit(loop_variable, Access(current_frame, context.sym, False))
    self.emit.printout(loop_variable_code)

    condition_code, _ = self.visit(for_stmt.end, Access(current_frame, context.sym, False))
    self.emit.printout(condition_code)

    comparison_code = self.emit.emitREOP('<=', IntType(), current_frame)
    self.emit.printout(comparison_code)
    self.emit.printout(self.emit.emitIFFALSE(break_label, current_frame))

    self.visit(for_stmt.stmt, context)
    self.emit.printout(self.emit.emitLABEL(continue_label, current_frame))

    update_code, _ = self.visit(for_stmt.upd, Access(current_frame, context.sym, False))
    self.emit.printout(update_code)

    loop_variable_code, _ = self.visit(loop_variable, Access(current_frame, context.sym, False))
    self.emit.printout(loop_variable_code)

    addition_code = self.emit.emitADDOP('+', IntType(), current_frame)
    self.emit.printout(addition_code)

    loop_variable_code, _ = self.visit(loop_variable, Access(current_frame, context.sym, True))
    self.emit.printout(loop_variable_code)
    self.emit.printout(self.emit.emitGOTO(loop_start_label, current_frame))
    self.emit.printout(self.emit.emitLABEL(break_label, current_frame))

    current_frame.exitLoop()