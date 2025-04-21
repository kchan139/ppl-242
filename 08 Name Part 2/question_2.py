"""
Given the AST declarations as follows:

class Program: #decl:List[VarDecl],exp:Exp
class VarDecl: #name:str,typ:Type
class Type(ABC): #abstract class
class IntType(Type)
class FloatType(Type)
class BoolType(Type)
class Exp(ABC): #abstract class
class BinOp(Exp): #op:str,e1:Exp,e2:Exp #op is +,-,*,/,&&,||, >, <, ==, or  !=
class UnOp(Exp): #op:str,e:Exp #op is -, !
class IntLit(Exp): #val:int
class FloatLit(Exp): #val:float
class BoolLit(Exp): #val:bool
class Id(Exp): #name:str

and the Visitor class is declared as follows:

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o):pass
    def visitVarDecl(self,ctx:VarDecl,o): pass
    def visitIntType(self,ctx:IntType,o):pass
    def visitFloatType(self,ctx:FloatType,o):pass
    def visitBoolType(self,ctx:BoolType,o):pass
    def visitBinOp(self,ctx:BinOp,o): pass
    def visitUnOp(self,ctx:UnOp,o):pass
    def visitIntLit(self,ctx:IntLit,o): pass 
    def visitFloatLit(self,ctx,o): pass
    def visitBoolLit(self,ctx,o): pass
    def visitId(self,ctx,o): pass

Rewrite the body of the methods in class StaticCheck to check the following type constraints:

+ , - and * accept their operands in int or float type and return float type if at least 
    one of their operands is in float type, otherwise, return int type

/ accepts their operands in int or float type and returns float type

!, && and || accept their operands in bool type and return bool type

>, <, == and != accept their operands in any type but must in the same type and return bool type
    the type of an Id is from the declarations, if the Id is not in the declarations, exception 
    UndeclaredIdentifier should be raised with the name of the Id. 

If the expression does not conform the type constraints, the StaticCheck will raise exception 
    TypeMismatchInExpression with the innermost sub-expression that contains type mismatch.
"""

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o):
        env = {}
        for decl in ctx.decl:
            self.visit(decl, env)
        return ctx.exp.accept(self, env)

    def visitVarDecl(self, ctx:VarDecl, o):
        o[ctx.name] = ctx.typ.accept(self, o)
    
    def visitIntType(self, ctx:IntType, o):
        return 'int'
    
    def visitFloatType(self, ctx:FloatType, o):
        return 'float'
    
    def visitBoolType(self, ctx:BoolType, o):
        return 'bool'
    
    def visitBinOp(self,ctx:BinOp,o):
        type1 = self.visit(ctx.e1, o)
        type2 = self.visit(ctx.e2, o)
        
        if ctx.op in ['+','-','*']:
            if type1 not in ['int', 'float'] or type2 not in ['int', 'float']:
                raise TypeMismatchInExpression(ctx)
            return 'float' if 'float' in [type1, type2] else 'int'
        if ctx.op in ['/']:
            if type1 not in ['int', 'float'] or type2 not in ['int', 'float']:
                raise TypeMismatchInExpression(ctx)
            return 'float'
        if ctx.op in ['!','&&','||']:
            if type1 != 'bool' or type2 != 'bool':
                raise TypeMismatchInExpression(ctx)
            return 'bool'
        if ctx.op in ['<','>','==','!=']:
            if type1 != type2:
                raise TypeMismatchInExpression(ctx)
            return 'bool'

    def visitUnOp(self,ctx:UnOp,o):
        type_e = self.visit(ctx.e, o)
        
        if ctx.op == '-':
            if type_e not in ['int', 'float']:
                raise TypeMismatchInExpression(ctx)
            return type_e
        if ctx.op == '!':
            if type_e != 'bool':
                raise TypeMismatchInExpression(ctx)
            return 'bool'

    def visitIntLit(self,ctx:IntLit,o):
        return 'int'

    def visitFloatLit(self,ctx,o):
        return 'float'

    def visitBoolLit(self,ctx,o):
        return 'bool'
        
    def visitId(self,ctx,o):
        if ctx.name not in o:
            raise UndeclaredIdentifier(ctx.name)
        return o[ctx.name]