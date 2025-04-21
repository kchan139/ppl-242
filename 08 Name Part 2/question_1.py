"""
Given the AST declarations as follows:

class Exp(ABC): #abstract class
class BinOp(Exp): #op:str,e1:Exp,e2:Exp #op is +,-,*,/,&&,||, >, <, ==, or  !=
class UnOp(Exp): #op:str,e:Exp #op is -, !
class IntLit(Exp): #val:int
class FloatLit(Exp): #val:float
class BoolLit(Exp): #val:bool

and the Visitor class is declared as follows:

class StaticCheck(Visitor):
    def visitBinOp(self,ctx:BinOp,o): pass
    def visitUnOp(self,ctx:UnOp,o):pass
    def visitIntLit(self,ctx:IntLit,o): pass 
    def visitFloatLit(self,ctx,o): pass
    def visitBoolLit(self,ctx,o): pass

Rewrite the body of the methods in class StaticCheck to check the following type constraints:

+ , - and * accept their operands in int or float type and return float type if at least 
    one of their operands is in float type, otherwise, return int type
/ accepts their operands in int or float type and returns float type
!, && and || accept their operands in bool type and return bool type
>, <, == and != accept their operands in any type but must in the same type and return bool type 
If the expression does not conform the type constraints, the StaticCheck will raise 
    exception TypeMismatchInExpression with the innermost sub-expression that contains type mismatch.
"""

class StaticCheck(Visitor):

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