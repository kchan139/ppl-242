"""
Given the grammar of MP as follows:

program: exp EOF;
exp: (term ASSIGN)* term;
term: factor COMPARE factor | factor;
factor: operand (ANDOR operand)*; 
operand: ID | INTLIT | BOOLIT | '(' exp ')';
INTLIT: [0-9]+ ;
BOOLIT: 'True' | 'False' ;
ANDOR: 'and' | 'or' ;
ASSIGN: '+=' | '-=' | '&=' | '|=' | ':=' ;
COMPARE: '=' | '<>' | '>=' | '<=' | '<' | '>' ;
ID: [a-z]+ ;

and AST classes as follows:

class Expr(ABC):
class Binary(Expr):  #op:string;left:Expr;right:Expr
class Id(Expr): #value:string
class IntLiteral(Expr): #value:int
class BooleanLiteral(Expr): #value:boolean

Please copy the following class into your answer and modify the bodies of its methods to generate the AST of a MP input?

class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return None

    def visitExp(self,ctx:MPParser.ExpContext):
        return None

    def visitTerm(self,ctx:MPParser.TermContext): 
        return None

    def visitFactor(self,ctx:MPParser.FactorContext):
        return None

    def visitOperand(self,ctx:MPParser.OperandContext):
        return None
"""

from functools import reduce
class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.exp())
        
    def visitExp(self,ctx:MPParser.ExpContext):
        res = self.visit(ctx.getChild(ctx.getChildCount() - 1))
        
        l_ass = [i.getText() for i in ctx.ASSIGN()[::-1]]
        l_term = [self.visit(i) for i in ctx.term()[:-1][::-1]]
        zip_assterm = zip(l_ass,l_term)
        
        return reduce(lambda a, e: 
            Binary(e[0], e[1], a), 
            zip_assterm, 
            res
        )
    
    def visitTerm(self,ctx:MPParser.TermContext): 
        if ctx.COMPARE():
            op = ctx.COMPARE().getText()
            left = self.visit(ctx.factor(0))
            right = self.visit(ctx.factor(1))
            return Binary(op, left, right)
        else:
            return self.visit(ctx.factor(0))
            
    def visitFactor(self,ctx:MPParser.FactorContext):
        res = self.visit(ctx.operand(0))
        
        l_op = [i.getText() for i in ctx.ANDOR()]
        l_operand = [self.visit(i) for i in ctx.operand()[1:]]
        zip_opoperand = zip(l_op,l_operand)
        
        return reduce(lambda a, e: 
            Binary(e[0], a, e[1]), 
            zip_opoperand, 
            res
        )
    
    def visitOperand(self,ctx:MPParser.OperandContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.BOOLIT():
            return BooleanLiteral(ctx.BOOLIT().getText())
        else:
            return self.visit(ctx.exp())