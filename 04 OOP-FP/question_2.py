"""
Extend the contents of classes Exp, BinExp, UnExp, IntLit, FloatLit such that they 
can response to printPrefix() message to return the string corresponding to the expression 
in prefix format. Note that, unary operator +/- is printed as +./-. in prefix format and 
there is a space after each operator or operand. For example, when receiving message printPrefix(), 
the object expressing the expression -4 + 3 * 2 will return the string "+ -. 4 * 3 2 "
"""

from abc import ABC, abstractmethod

class Exp(ABC):
    @abstractmethod
    def eval(self):
        pass

    @abstractmethod
    def printPrefix(self):
        pass

class BinExp(Exp):
    def __init__(self, left: Exp, op: str, right: Exp):
        self.left  = left
        self.op    = op
        self.right = right

    def eval(self):
        if self.op == '+':
            return self.left.eval() + self.right.eval()
        elif self.op == '-':
            return self.left.eval() - self.right.eval()
        elif self.op == '*':
            return self.left.eval() * self.right.eval()
        elif self.op == '/':
            return self.left.eval() / self.right.eval()
        else:
            return 0
        
    def printPrefix(self):
        return f"{self.op } " + self.left.printPrefix() + self.right.printPrefix()

class UnExp(Exp):
    def __init__(self, op: str, operand: Exp):
        self.op      = op
        self.operand = operand

    def eval(self):
        if self.op == '+':
            return self.operand.eval()
        elif self.op == '-':
            return -self.operand.eval()
        else:
            return 0
        
    def printPrefix(self):
        return f"{self.op }. " + self.operand.printPrefix()

class IntLit(Exp):
    def __init__(self, val: int):
        self.val = val

    def eval(self):
        return self.val
    
    def printPrefix(self):
        return f"{self.val } "

class FloatLit(Exp):
    def __init__(self, val: float):
        self.val = val

    def eval(self):
        return self.val

    def printPrefix(self):
        return f"{self.val } "