"""
Let AST of a programming language be defined as follows:

class Program: #decl:List[Decl]
class Decl(ABC): #abstract class
class VarDecl(Decl): #name:str,typ:Type
class ConstDecl(Decl): #name:str,val:Lit
class FuncDecl(Decl): #name:str,param:List[VarDecl],body:List[Decl]
class Type(ABC): #abstract class
class IntType(Type)
class FloatType(Type)
class Lit(ABC): #abstract class
class IntLit(Lit): #val:int

and exceptions:

class RedeclaredVariable(Exception): #name:str
class RedeclaredConstant(Exception): #name:str
class RedeclaredFunction(Exception): #name:str

Implement the methods of the following class Visitor to travel on the 
above AST to detect redeclared declarations (throw the exception 
corresponding to the second declaration with the same name) in the same scope:

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o:object):pass
    def visitVarDecl(self,ctx:VarDecl,o:object):pass
    def visitConstDecl(self,ctx:ConstDecl,o:object):pass
    def visitFuncDecl(self,ctx:FuncDecl,o:object):pass
    def visitIntType(self,ctx:IntType,o:object):pass
    def visitFloatType(self,ctx:FloatType,o:object):pass
    def visitIntLit(self,ctx:IntLit,o:object):pass

x = Program([
    VarDecl("b",IntType()),
    FuncDecl("a",[VarDecl("a",FloatType())],[
        ConstDecl("c",IntLit(3)),
        VarDecl("b",IntType()),
        VarDecl("c",IntType())
    ])
])
"""

class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        o = []
        for decl in ctx.decl:
            o.append(self.visit(decl, o))

    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        return ctx.name

    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        return ctx.name

    def visitFuncDecl(self, ctx:FuncDecl, o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        
        local_env = []
        
        for param in ctx.param:
            if param.name in local_env:
                raise RedeclaredVariable(param.name)
            local_env.append(param.name)
        
        for decl in ctx.body:
            local_env.append(self.visit(decl, local_env))
        
        return ctx.name

    def visitIntType(self,ctx:IntType,o:object):
        pass

    def visitFloatType(self,ctx:FloatType,o:object):
        pass

    def visitIntLit(self,ctx:IntLit,o:object):
        pass
