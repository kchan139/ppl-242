"""
Let AST of a programming language be defined as follows:

class Program: #decl:List[Decl]
class Decl(ABC): #abstract class
class VarDecl(Decl): #name:str,typ:Type
class ConstDecl(Decl): #name:str,val:Lit
class FuncDecl(Decl): #name:str,param:List[VarDecl],body:Tuple(List[Decl],List[Expr])
class Type(ABC): #abstract class
class IntType(Type)
class FloatType(Type)
class Expr(ABC): #abstract class
class Lit(Expr): #abstract class
class IntLit(Lit): #val:int
class Id(Expr): #name:str

and exceptions:

class RedeclaredVariable(Exception): #name:str
class RedeclaredConstant(Exception): #name:str
class RedeclaredFunction(Exception): #name:str
class UndeclaredIdentifier(Exception): #name:str

Implement the methods of the following class Visitor to travel on the 
above AST to detect undeclared declarations (throw the exception 
UndeclaredIdentifier). Note that the redeclared declarations exception 
also is thrown if a redeclared declaration is detected:

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o:object):pass
    def visitVarDecl(self,ctx:VarDecl,o:object):pass
    def visitConstDecl(self,ctx:ConstDecl,o:object):pass
    def visitFuncDecl(self,ctx:FuncDecl,o:object):pass
    def visitIntType(self,ctx:IntType,o:object):pass
    def visitFloatType(self,ctx:FloatType,o:object):pass
    def visitIntLit(self,ctx:IntLit,o:object):pass
    def visitId(self,ctx:Id,o:object):pass
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

    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        
        local_env = []
        
        for param in ctx.param:
            if param.name in local_env:
                raise RedeclaredVariable(param.name)
            # local_env.append(self.visit(param, local_env))
            local_env.append(param.name)
        
        for decl in ctx.body[0]:
            # local_env.append(self.visit(decl, local_env))
            if isinstance(decl, FuncDecl):
                local_env.append(
                    self.visit(decl, o + local_env + [ctx.name])
                )
            else:
                local_env.append(
                    self.visit(decl, local_env)
                )
                
        # local_env.append(ctx.name)
        local_env = o + local_env + [ctx.name]
        
        for expr in ctx.body[1]:
            self.visit(expr, local_env)
        
        return ctx.name

    def visitIntType(self,ctx:IntType,o:object):
        pass

    def visitFloatType(self,ctx:FloatType,o:object):
        pass

    def visitIntLit(self,ctx:IntLit,o:object):
        pass

    def visitId(self,ctx:Id,o:object):
        # print(ctx.name)
        def recursive_checker(obj):
            # print(obj)
            if ctx.name in obj:
                return True
            for ele in obj:
                # print(ele)
                if isinstance(ele, list):
                    return recursive_checker(ele)
                if ctx.name in ele:
                    return True
            return False
            
        if recursive_checker(o):
            return
        raise UndeclaredIdentifier(ctx.name)