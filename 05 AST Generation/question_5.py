"""
Given the grammar of MP as follows:

program: vardecl+ EOF;
vardecl: mptype ids ';' ;
mptype: INTTYPE | FLOATTYPE;
ids: ID (',' ID)*; 
INTTYPE: 'int';
FLOATTYPE: 'float';
ID: [a-z]+ ;

and AST classes as follows:

class Program:#decl:list(VarDecl)
class Type(ABC): pass
class IntType(Type): pass
class FloatType(Type): pass
class VarDecl: #variable:Id; varType: Type
class Id: #name:str

Please copy the following class into your answer and modify the bodies of its methods to generate the AST of a MP input?

class ASTGeneration(MPVisitor):
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return None

    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        return None

    def visitMptype(self,ctx:MPParser.MptypeContext):
        return None

    def visitIds(self,ctx:MPParser.IdsContext):
        return None
"""

class ASTGeneration(MPVisitor):
    
    def visitProgram(self,ctx:MPParser.ProgramContext):
        lst = [self.visit(x) for x in ctx.vardecl()]
        return Program([vardecl for sublst in lst for vardecl in sublst])

    def visitVardecl(self,ctx:MPParser.VardeclContext):
        mp_type = self.visit(ctx.mptype())
        return [VarDecl(mp_id, mp_type) for mp_id in self.visit(ctx.ids())]

    def visitMptype(self,ctx:MPParser.MptypeContext):
        return IntType() if ctx.INTTYPE() else FloatType()

    def visitIds(self,ctx:MPParser.IdsContext):
        return [Id(mp_id.getText()) for mp_id in ctx.ID()]