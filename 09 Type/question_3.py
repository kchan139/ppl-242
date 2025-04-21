"""
Given the AST declarations as follows:

class Program: #decl:List[Decl],stmts:List[Stmt]
class Decl(ABC): #abstract class
class VarDecl(Decl): #name:str
class FuncDecl(Decl): #name:str,param:List[VarDecl],local:List[Decl],stmts:List[Stmt]
class Stmt(ABC): #abstract class
class Assign(Stmt): #lhs:Id,rhs:Exp
class CallStmt(Stmt): #name:str,args:List[Exp]
class Exp(ABC): #abstract class
class IntLit(Exp): #val:int
class FloatLit(Exp): #val:float
class BoolLit(Exp): #val:bool
class Id(Exp): #name:str

and the Visitor class is declared as follows:

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o):pass
    def visitVarDecl(self,ctx:VarDecl,o): pass
    def visitFuncDecl(self,ctx:FuncDecl,o): pass
    def visitCallStmt(self,ctx:CallStmt,o):pass
    def visitAssign(self,ctx:Assign,o): pass
    def visitIntLit(self,ctx:IntLit,o): pass 
    def visitFloatLit(self,ctx,o): pass
    def visitBoolLit(self,ctx,o): pass
    def visitId(self,ctx,o): pass

Rewrite the body of the methods in class StaticCheck to infer the type of identifiers and check the following type constraints:

In an Assign, the type of lhs must be the same as that of rhs, otherwise, the exception TypeMismatchInStatement should be raised together with the Assign
the type of an Id is inferred from the above constraints in the first usage, 
if the Id is not in the declarations, exception UndeclaredIdentifier should be raised together with the name of the Id, or
If the Id cannot be inferred in the first usage, exception TypeCannotBeInferred should be raised together with the statement
For static referencing environment, this language applies the scope rules of block-structured programming language where a function is a block. When there is a declaration duplication of a name in a scope, exception Redeclared should be raised together with the second declaration.
In a call statement, the argument type must be the same as the parameter type. If there is no function declaration in the static referencing environment, exception UndeclaredIdentifier should be raised together with the function call name. If the numbers of parameters and arguments are not the same or at least one argument type is not the same as the type of the corresponding parameter, exception TypeMismatchInStatement should be raise with the call statement. If there is at least one parameter type cannot be resolved, exception TypeCannotBeInferred should be raised together with the call statement.
"""

class StaticCheck(Visitor):
    def visitProgram(self, ctx: Program, o):
        env = {}
        for decl in ctx.decl:
            self.visit(decl, env)
        for stmt in ctx.stmts:
            self.visit(stmt, env)

    def visitVarDecl(self, ctx: VarDecl, o):
        if ctx.name in o:
            raise Redeclared(ctx)
        o[ctx.name] = None

    def visitAssign(self, ctx: Assign, o):
        rhs_type = self.visit(ctx.rhs, o)
        lhs_type = self.visit(ctx.lhs, o)
        if lhs_type is None and rhs_type is None:
            raise TypeCannotBeInferred(ctx)

        if lhs_type is None:
            o[ctx.lhs.name] = rhs_type
            lhs_type = rhs_type

        elif rhs_type is None:
            self.infer_type(ctx.rhs, o, lhs_type)
            rhs_type = lhs_type

        if lhs_type != rhs_type:
            raise TypeMismatchInStatement(ctx)

    def visitBinOp(self, ctx: BinOp, o):
        left_type = self.visit(ctx.e1, o)
        right_type = self.visit(ctx.e2, o)

        int_ops = ['+', '-', '*', '/']
        float_ops = ['+.', '-.', '*.', '/.']
        int_bool_ops = ['>', '=']
        float_bool_ops = ['>.', '=.']

        if ctx.op in int_ops:
            result_type = 'int'
            expected = 'int'
        elif ctx.op in float_ops:
            result_type = 'float'
            expected = 'float'
        elif ctx.op in int_bool_ops:
            result_type = 'bool'
            expected = 'int'
        elif ctx.op in float_bool_ops:
            result_type = 'bool'
            expected = 'float'
        elif ctx.op in ['&&', '||', '>b', '=b']:
            result_type = 'bool'
            expected = 'bool'
        else:
            raise TypeMismatchInExpression(ctx)

        for operand, operand_type in zip([ctx.e1, ctx.e2], [left_type, right_type]):
            if operand_type is None:
                self.infer_type(operand, o, expected)

        left_type = self.visit(ctx.e1, o)
        right_type = self.visit(ctx.e2, o)
        if left_type != expected or right_type != expected:
            raise TypeMismatchInExpression(ctx)

        return result_type


    def visitUnOp(self, ctx: UnOp, o):
        expr_type = self.visit(ctx.e, o)

        if ctx.op == '-':
            expected = 'int'
            result = 'int'
        elif ctx.op == '-.':
            expected = 'float'
            result = 'float'
        elif ctx.op == '!':
            expected = 'bool'
            result = 'bool'
        elif ctx.op == 'i2f':
            expected = 'int'
            result = 'float'
        elif ctx.op == 'floor':
            expected = 'float'
            result = 'int'
        else:
            raise TypeMismatchInExpression(ctx)

        if expr_type is None:
            self.infer_type(ctx.e, o, expected)
            expr_type = self.visit(ctx.e, o)

        if expr_type != expected:
            raise TypeMismatchInExpression(ctx)

        return result

    def visitIntLit(self, ctx: IntLit, o): 
        return 'int'

    def visitFloatLit(self, ctx: FloatLit, o): 
        return 'float'

    def visitBoolLit(self, ctx: BoolLit, o): 
        return 'bool'

    def visitId(self, ctx: Id, o):
        if ctx.name not in o:
            raise UndeclaredIdentifier(ctx.name)
        return o[ctx.name]

    def infer_type(self, expr, env, typ):
        if isinstance(expr, Id):
            if expr.name not in env:
                raise UndeclaredIdentifier(expr.name)
            if env[expr.name] is None:
                env[expr.name] = typ
            elif env[expr.name] != typ:
                raise TypeMismatchInExpression(expr)
        elif isinstance(expr, (BinOp, UnOp)):
            self.visit(expr, env)
            
            
    def visitFuncDecl(self, ctx: FuncDecl, o):
        if ctx.name in o:
            raise Redeclared(ctx)
        o[ctx.name] = {
            "kind": "function",
            "params": {}
        }
        for p in ctx.param:
            self.visit(p, o[ctx.name]["params"])
        func_env = dict(o[ctx.name]["params"])
        
        for decl in ctx.local:
            self.visit(decl, func_env)
        for stmt in ctx.stmts:
            self.visit(stmt, func_env)
        for name in func_env:
            if name in o[ctx.name]["params"]:
                o[ctx.name]["params"][name]=func_env[name]
    
    def visitCallStmt(self, ctx: CallStmt, o):
        if ctx.name not in o or o[ctx.name]["kind"] != "function":
            raise UndeclaredIdentifier(ctx.name)
        param_env = o[ctx.name]["params"]
        if len(param_env) != len(ctx.args):
            raise TypeMismatchInStatement(ctx)
        param_names = list(param_env.keys())
        for i, arg in enumerate(ctx.args):
            param_name = param_names[i]
            param_type = param_env[param_name]
            arg_type = self.visit(arg, o)
            
            if param_type is None:
                if arg_type is None:
                    raise TypeCannotBeInferred(ctx)
                o[ctx.name]["params"][param_name] = arg_type
            elif param_type is not None and arg_type != param_type:
                if arg_type is not None:
                    raise TypeMismatchInStatement(ctx)
                o[arg.name] = param_type