"""
As in the previous question, when a task is added into expression classes, new methods are added into these classes. 
Please change the way these classes are implemented in such a way that these classes do not change their contents 
when new tasks are added into these classes: 

- Define class Eval to calculate the value of an expression

- Define class PrintPrefix to return the string corresponding to the expression in prefix format

- Define class PrintPostfix to return the string corresponding to the expression in postfix format

Let x be an object expressing an expression, x.accept(Eval()) will return the value of the expression x, 
x.accept(PrintPrefix()) will return the expression in prefix format and x.accept(PrintPostfix()) will 
return the expression in postfix format. 

Be careful that you are not allowed to use type(), isinstance() when implementing this exercise 

Tip: Use Visitor pattern.
"""

from abc import ABC, abstractmethod

class Exp(ABC):
    @abstractmethod
    def accept(self):
        pass

class BinExp(Exp):
    def __init__(self, left: Exp, op: str, right: Exp):
        self.left  = left
        self.op    = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_BinExp(self)

class UnExp(Exp):
    def __init__(self, op: str, operand: Exp):
        self.op      = op
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_UnExp(self)

class IntLit(Exp):
    def __init__(self, val: int):
        self.val = val

    def accept(self, visitor):
        return visitor.visit_IntLit(self)

class FloatLit(Exp):
    def __init__(self, val: float):
        self.val = val

    def accept(self, visitor):
        return visitor.visit_FloatLit(self)

class Visitor(ABC):
    def visit_BinExp(self):
        pass

    def visit_UnExp(self):
        pass

    def visit_IntLit(self):
        pass

    def visit_FloatLit(self):
        pass

class Eval(Visitor):
    def visit_BinExp(self, exp):
        op = exp.op
        left = exp.left.accept(self)
        right = exp.right.accept(self)
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        
    def visit_UnExp(self, exp):
        op = exp.op
        operand = exp.operand.accept(self)
        if op == '+': 
            return operand
        else: 
            return - operand

    def visit_IntLit(self,exp):
        return exp.val
    
    def visit_FloatLit(self,exp):
        return exp.val

class PrintPrefix(Visitor):
    def visit_BinExp(self, exp):
        op = exp.op
        left = exp.left.accept(self)
        right = exp.right.accept(self)
        return op + ' ' + left + right
    
    def visit_UnExp(self, exp):
        op = exp.op
        operand = exp.operand.accept(self)
        return op + '. ' + operand
    
    def visit_IntLit(self, exp):
        return str(exp.val) + ' '
    
    def visit_FloatLit(self, exp):
        return str(exp.val) + ' '
    
class PrintPostfix(Visitor):
    def visit_BinExp(self, exp):
        op = exp.op
        left = exp.left.accept(self)
        right = exp.right.accept(self)
        return left + right + op + ' '
    
    def visit_UnExp(self, exp):
        op = exp.op
        operand = exp.operand.accept(self)
        return str(operand) + op + '. '
    
    def visit_IntLit(self, exp):
        return str(exp.val) + ' '
    
    def visit_FloatLit(self, exp):
        return str(exp.val) + ' '