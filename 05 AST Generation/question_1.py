"""
Given the grammar of MP as follows:

program: vardecls EOF;
vardecls: vardecl vardecltail;
vardecltail: vardecl vardecltail | ;
vardecl: mptype ids ';' ;
mptype: INTTYPE | FLOATTYPE;
ids: ID ',' ids | ID; 
INTTYPE: 'int';
FLOATTYPE: 'float';
ID: [a-z]+ ;

Please copy the following class into your answer and modify the bodies of its methods to count the terminal nodes in the parse tree? Your code starts at line 10.

class TerminalCount(MPVisitor):
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return None

    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        return None

    def visitVardecltail(self,ctx:MPParser.VardecltailContext): 
        return None

    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        return None

    def visitMptype(self,ctx:MPParser.MptypeContext):
        return None

    def visitIds(self,ctx:MPParser.IdsContext):
        return None
"""

class TerminalCount(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return 1 + self.visit(ctx.vardecls())

    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())

    def visitVardecltail(self,ctx:MPParser.VardecltailContext): 
        if ctx.vardecl(): 
            return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())
        return 0

    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        return 1 + self.visit(ctx.mptype()) + self.visit(ctx.ids())

    def visitMptype(self,ctx:MPParser.MptypeContext):
        return 1
    
    def visitIds(self,ctx:MPParser.IdsContext):
        if ctx.ids(): 
            return 2 + self.visit(ctx.ids())
        return 1