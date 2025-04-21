"""
To express an arithmetic expression, there are 5 following classes:

- Exp: general arithmetic expression

- BinExp(left,op,right): an arithmetic expression that contains one binary operators (+,-,*,/) and two operands

- UnExp(op,operand): an arithmetic expression that contains one unary operator (+,-) and one operand

- IntLit(val): an arithmetic expression that contains one integer number

- FloatLit(val): an arithmetic expression that contains one floating point number

Define these classes in Python (their parents, attributes, methods) such that their objects can response 
to eval() message by returning the value of the expression. For example, let object x express the arithmetic 
expression 3 + 4 * 2.0, x.eval() must return 11.0
"""

from abc import ABC, abstractmethod

class Exp(ABC):
    @abstractmethod
    def eval(self):
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

class IntLit(Exp):
    def __init__(self, val: int):
        self.val = val

    def eval(self):
        return self.val

class FloatLit(Exp):
    def __init__(self, val: float):
        self.val = val

    def eval(self):
        return self.val