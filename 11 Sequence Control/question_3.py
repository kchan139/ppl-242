"""
Assume that 
    class Assign(Stmt) in AST is declared with field lhs and rhs in Expr type.  The types of the left hand side and right hand side are the same.
    The visitor CodeGeneration has field emit keeping an object of Emitter 
    Object is passed to the parameter o of visitId has 2 fields:
        Field frame keeps object Frame. 
        Field sym of the argument keeps a list of Symbol which has three fields: name (str type), mtype (Type type) and value (Val type). The Val type has two concrete classes: Index with field value in int type and CName with field value in str type. An Index object keeps the index of the variable while a CName keeps the name of the class name (used for global variable). The first element of sym contains the identifier which belongs to the innermost referencing environment while the last element of sym contains one in the outermost referencing environment (global).
    When visiting the expression in the left hand side or the right hand side of the assignment statement, object Access must be passed to parameter o where Access has 3 fields:
        frame and sym are similar to the object passed to parameter o 
        Field isLeft in boolean type indicates the identifier in the left (isLeft true) or in the right (isLeft false).
The method visitAssign must print out the code of the assignment statement (use method printout of Emitter)
Based on the above assumption, write method visitAssign(self,ctx,o) of visitor CodeGeneration? Your code is at line 230.
"""
def visitAssign(self, assignment_stmt, context):
    rhs_code, rhs_type = self.visit(assignment_stmt.rhs, Access(context.frame, context.sym, False))
    lhs_code, lhs_type = self.visit(assignment_stmt.lhs, Access(context.frame, context.sym, True))

    if isinstance(lhs_type, FloatType) and isinstance(rhs_type, IntType):
        rhs_code += self.emit.emitI2F(context.frame)

    self.emit.printout(rhs_code)
    self.emit.printout(lhs_code)

    return context