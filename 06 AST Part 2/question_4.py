"""
Given the grammar of MP as follows:

program: mptype EOF;
arraytype:  primtype dimens  ;
mptype: primtype | arraytype;
primtype: INTTYPE | FLOATTYPE; 
dimens: dimen+;
dimen: '[' num '..' num ']';
num: '-'? INTLIT;
INTLIT: [0-9]+ ;
INTTYPE: 'integer';
FLOATTYPE: 'real';

and AST classes as follows:

class Type():abstract
class CompoundType(Type):abstract
class UnionType(CompoundType):#firstType:Type,secondType:primType
class ArrayType(CompoundType):#indexType:Type,eleType:primType
class PrimType(Type):abstract
class IntType(PrimType): pass
class FloatType(PrimType): pass
class RangeType(PrimType): #lowbound:int; highbound:int
class Id: #name:str

Please copy the following class into your answer and modify the bodies of its methods to generate the AST of a MP input?

class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return None

    def visitMptype(self,ctx:MPParser.MptypeContext):
        return None

    def visitArraytype(self,ctx:MPParser.ArraytypeContext):
        return None

    def visitPrimtype(self,ctx:MPParser.PrimtypeContext): 
        return None

    def visitDimens(self,ctx:MPParser.DimensContext):
        return None  

    def visitDimen(self,ctx:MPParser.DimenContext):
        return None

    def visitNum(self,ctx:MPParser.DimenContext):
        return None
"""

class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.mptype())

    def visitMptype(self,ctx:MPParser.MptypeContext):
        if ctx.primtype():
            return self.visit(ctx.primtype())
        else:
            return self.visit(ctx.arraytype())

    def visitArraytype(self,ctx:MPParser.ArraytypeContext):
        idx = self.visit(ctx.dimens())
        ele = self.visit(ctx.primtype())
        return ArrayType(idx, ele)

    def visitPrimtype(self,ctx:MPParser.PrimtypeContext): 
        if ctx.INTTYPE():
            return IntType()
        else:
            return FloatType()

    def visitDimens(self,ctx:MPParser.DimensContext):
        dimens = [self.visit(dimen) for dimen in ctx.dimen()]
        res = dimens[0]
        dimlen = len(dimens)
        
        for i in range(1, dimlen):
            res = UnionType(res, dimens[i])
        
        return res

    def visitDimen(self,ctx:MPParser.DimenContext):
        low = self.visit(ctx.num(0))
        high = self.visit(ctx.num(1))
        return RangeType(low, high)

    def visitNum(self,ctx:MPParser.DimenContext):
        num = int(ctx.INTLIT().getText())
        if ctx.getChildCount() > 1:
            return -num
        return num