"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from .StaticError import *
from functools import reduce

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"

class GetEnv(BaseVisitor, Utils):
    def __init__(self):
        pass
        
      
    def visitProgram(self, ast: Program, o):
        o = [
            [Symbol("getInt", MType([], IntType())),
            Symbol("putInt", MType([IntType()], VoidType())),
            Symbol("putIntLn", MType([IntType()], VoidType())),
            Symbol("getFloat", MType([], FloatType())),
            Symbol("putFloat", MType([FloatType()], VoidType())),
            Symbol("putFloatLn", MType([FloatType()], VoidType())),
            Symbol("getBool", MType([], BoolType())),
            Symbol("putBool", MType([BoolType()], VoidType())),
            Symbol("putBoolLn", MType([BoolType()], VoidType())),
            Symbol("getString", MType([], StringType())),
            Symbol("putString", MType([StringType()], VoidType())),
            Symbol("putStringLn", MType([StringType()], VoidType())),
            Symbol("putLn", MType([], VoidType()))]
            ]
        methods = []
        for decl in ast.decl:
            if isinstance(decl, FuncDecl):
                o = self.visit(decl, o)
            elif isinstance(decl, MethodDecl):
                # o = self.visit(decl, o)
                methods += [decl]
            elif isinstance(decl, StructType):
                o = self.visit(decl, o)
            elif isinstance(decl, InterfaceType):
                o = self.visit(decl, o)
        
        for method in methods:
            o = self.visitMethodDecl(method, o)
        return o
    
    
    # FuncDecl(Decl):
    # name: str
    # params: List[ParamDecl]
    # retType: Type # VoidType if there is no return type
    # body: Block
    def visitFuncDecl(self, ast: FuncDecl, o):
        if self.lookup(ast.name, o[0], lambda x: x.name) is not None:
            raise Redeclared(Function(), ast.name)
        
        params = []
        for p in ast.params:
            params = self.visit(p, params)
            
        func_type = MType([param.mtype for param in params], ast.retType)
        o[0] += [Symbol(ast.name, func_type)]
        return o

    # MethodDecl(Decl):             # FuncDecl(Decl):               StructType(Type):
    # receiver: str                 # name: str                         name: str
    # recType: Type                 # params: List[ParamDecl]           elements:List[tuple[str,Type]]
    # fun: FuncDecl                 # retType: Type                     methods:List[MethodDecl]
                                    # body: Block
    
    def visitMethodDecl(self, ast: MethodDecl, c):
        o = [[]] + c
        for symbol in c[0]:
            if symbol.name == ast.recType.name:                     # kiem tra recType co ton tai trong scope
                
                if type(symbol.mtype) is StructType:                
                    for method in symbol.mtype.methods:                
                        if method.fun.name == ast.fun.name:         # kiem tra method co ton tai trong struct
                            raise Redeclared(Method(), ast.fun.name)
                        
                    o[0] += [Symbol(ast.receiver, symbol.mtype)]                    
                    for param in ast.fun.params:
                        o[0] = self.visit(param, o[0])
                        
                    symbol.mtype.methods += [ast]                   # them method vao struct
                    
                    # o = self.visit(ast.fun.body, o)
                    return c
                # elif type(recType) is InterfaceType:
                #     recType = recType.name 
        
        # print("MethodDecl not found recType Error: ", ast)
        
        return c
    
    
    # ParamDecl(Decl):
    # parName: str
    # parType: Type
    def visitParamDecl(self, ast: ParamDecl, o):
        if self.lookup(ast.parName, o, lambda x: x.name) is not None:
            raise Redeclared(Parameter(), ast.parName)
        
        o += [Symbol(ast.parName, ast.parType)]
        return o
    
    
    # InterfaceType(Type):
    # name: str
    # methods:List[Prototype]
    def visitInterfaceType(self, ast: InterfaceType, o):
        if self.lookup(ast.name, o[0], lambda x: x.name) is not None:
            raise Redeclared(Type(), ast.name)
        o[0] += [Symbol(ast.name, ast)]
        return o

    # StructType(Type):
    # name: str
    # elements:List[tuple[str,Type]]
    # methods:List[MethodDecl]
    def visitStructType(self, ast: StructType, o):
        if self.lookup(ast.name, o[0], lambda x: x.name) is not None:
            raise Redeclared(Type(), ast.name)
        o[0] += [Symbol(ast.name, ast)]
        return o
    
    
    def visitFuncCall(self,ast,c):
        pass
    


#------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

class StaticChecker(BaseVisitor,Utils):
        
    
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = []
 
    
    def check(self):
        return self.visit(self.ast,self.global_envi)

    # Program(AST):
    # decl : List[Decl]
    def visitProgram(self,ast: Program, c):
        # env = self.global_envi
        env = GetEnv().visit(ast, c)
        for decl in ast.decl:
            env = self.visit(decl, env)
            

        # reduce(lambda acc,ele: [self.visit(ele,acc)] + acc , ast.decl,c)
        return env
    
    # ParamDecl(Decl):
    # parName: str
    # parType: Type
    def visitParamDecl(self, ast: ParamDecl, c):
        if self.lookup(ast.parName, c[0], lambda x: x.name) is not None:
            raise Redeclared(Parameter(), ast.parName)
        c[0] += [Symbol(ast.parName, ast.parType)]
        return c

    
    # VarDecl(Decl,BlockMember):
    # varName : str
    # varType : Type # None if there is no type
    # varInit : Expr # None if there is no initialization
    def visitVarDecl(self, ast: VarDecl, c):
    
        if self.lookup(ast.varName, c[0], lambda x: x.name) is not None:
            raise Redeclared(Variable(), ast.varName)
        
        if ast.varInit is None:         # chi khoi tao ko co gia tri
            self.visit(ast.varType, c)
            
            if type(ast.varType) is Id:
                found = self.lookup(ast.varType.name, c[-1], lambda x: x.name) # find a symbol in global env
                if found is None:
                    raise Undeclared(Identifier(), ast.varType.name)
                elif type(found.mtype) is StructType or type(found.mtype) is InterfaceType:
                    c[0] += [Symbol(ast.varName, found.mtype)]
            else:
                c[0] += [Symbol(ast.varName, ast.varType)]
                # print(c[0][0])
            
        else:                           # khoi tao co gia tri
            
            if ast.varType is None:                                             # khai bao khong co kieu
                 
                ast.varType = self.visit(ast.varInit, c)                        # visit literal to get literal type
                if type(ast.varType) is Symbol:                                 
                    
                    if type(ast.varType.mtype) is MType:                         # Symbol khi la funccall, methcall,
                        if type(ast.varType.mtype.rettype) is VoidType:
                            raise TypeMismatch(ast.varInit)
                        c[0] += [Symbol(ast.varName, ast.varType.mtype.rettype)]
                    else:
                        # chua hien thuc value cua fieldaccess                      fieldaccess
                        c[0] += [Symbol(ast.varName, ast.varType.mtype)]

                else:                                                           #  khi la literal
                    c[0] += [Symbol(ast.varName, ast.varType, ast.varInit)]     # struct lit va array lit is the same
                    # print(Symbol(ast.varName, ast.varType, ast.varInit))
                    
            else:                                                               # khai bao co kieu
                varInitType = self.visit(ast.varInit, c)
                # print("varInitType", varInitType)
                # print("ast.varType", ast.varType)
                
                if type(varInitType) is Symbol:                                 # expr -> varInitType: symbol
                    if type(varInitType.mtype) is MType:                        # func method call
                        if type(ast.varType) is not type(varInitType.mtype.rettype):
                            raise TypeMismatch(ast)
                    else:
                        if type(ast.varType) is not type(varInitType.mtype):     
                           
                            if type(ast.varType) is FloatType and type(varInitType.mtype) is IntType:  # gan int to float
                                pass
                                print("floaf-int")
                            elif type(ast.varType) is Id:                                              #struct || interface             
                                found = self.lookup(ast.varType.name, c[-1], lambda x: x.name) # kiem tra da khai bao chua
                                if found is None:
                                    raise Undeclared(Identifier(), ast.varType.name)
                                
                                if ast.varType.name == varInitType.mtype.name:
                                    pass
                                    # print("SType-SType", "Itype-Itype")
                                elif type(varInitType.mtype) is StructType :
                                    # print(found)
                                    if self.CheckIfStructHasAllInterfaceMethods(found, varInitType) is False:
                                        raise TypeMismatch(ast)                                            
                                else:
                                    raise TypeMismatch(ast)
                            else: 
                                raise TypeMismatch(ast)
                            
                        elif type(ast.varType) is ArrayType:
                            if type(ast.varType.eleType) is not type(varInitType.mtype.eleType):  # kiem tra kieu cua mang 
                                if type(ast.varType.eleType) is FloatType and type(varInitType.mtype.eleType) is IntType:  # gan int to float
                                    pass
                                else:
                                    raise TypeMismatch(ast)
                            
                            if len(ast.varType.dimens) != len(varInitType.mtype.dimens):          # va so chieu
                                raise TypeMismatch(ast)
                            
                            for i in range(len(ast.varType.dimens)):                        # kiem tra tung chieu co cung size?
                                lhs = ast.varType.dimens[i] # can be const or int literal
                                rhs = varInitType.mtype.dimens[i]
                                
                                if type(lhs) is not IntLiteral and type(lhs) is not Id:
                                    raise TypeMismatch(lhs)
                                elif type(lhs) is Id:
                                    lhsSymbol = self.visit(lhs, c)
                                    
                                    if type(lhsSymbol.value) is not IntLiteral:
                                        raise TypeMismatch(lhs)
                                    else:
                                        lhs = lhsSymbol.value
                                        
                                if type(rhs) is not IntLiteral and type(rhs) is not Id:
                                    raise TypeMismatch(rhs)
                                elif type(rhs) is Id:
                                    rhsSymbol = self.visit(rhs, c)
                                    if type(rhsSymbol.value) is not IntLiteral:
                                        raise TypeMismatch(rhs)
                                    else:
                                        rhs = rhsSymbol.value

                                if int(lhs.value) != int(rhs.value):
                                    raise TypeMismatch(ast)
                    c[0] += [Symbol(ast.varName, ast.varType)]
                else:                                                           # literal -> varInitType: Type
                    if type(ast.varType) is Id:                                 # struct || interface
                        found = self.lookup(ast.varType.name, c[-1], lambda x: x.name) # kiem tra da khai bao chua
                        if found is None:
                            raise Undeclared(Identifier(), ast.varType.name)
                        
                        if ast.varType.name == varInitType.name:
                            # print("SType-SType", "Itype-Itype")
                            pass
                        elif type(found.mtype) is InterfaceType and type(varInitType) is StructType:
                            varInitType = Symbol(ast.varName, varInitType)
                            if self.CheckIfStructHasAllInterfaceMethods(found, varInitType) is False:
                                raise TypeMismatch(ast)
                            c[0] += [Symbol(ast.varName, found.mtype)]
                            # print(c[0][-1])
                        else:
                            # print("unknowError vardecl: ", found.mtype)
                            raise TypeMismatch(ast)
                        
                        c[0] += [Symbol(ast.varName, found.mtype)]
                        return c
                    elif type(ast.varType) is not type(varInitType):              # primitive type
                        raise TypeMismatch(ast)
                    
                    elif type(varInitType) is ArrayType :                           #   array
                        if type(ast.varType.eleType) is not type(varInitType.eleType):  # kiem tra kieu cua mang 
                            if type(ast.varType.eleType) is FloatType and type(varInitType.eleType) is IntType:  # gan int to float
                                pass
                            else:
                                raise TypeMismatch(ast)
                            
                        if len(ast.varType.dimens) != len(varInitType.dimens):          # va so chieu
                            raise TypeMismatch(ast)
                        
                        for i in range(len(ast.varType.dimens)):                        # kiem tra tung chieu co cung size?
                            lhs = ast.varType.dimens[i] # can be const or int literal
                            rhs = varInitType.dimens[i]
                            
                            if type(lhs) is not IntLiteral and type(lhs) is not Id:
                                raise TypeMismatch(lhs)
                            elif type(lhs) is Id:
                                lhsSymbol = self.visit(lhs, c)
                                
                                if type(lhsSymbol.value) is not IntLiteral:
                                    raise TypeMismatch(lhs)
                                else:
                                    lhs = lhsSymbol.value
                                    
                            if type(rhs) is not IntLiteral and type(rhs) is not Id:
                                raise TypeMismatch(rhs)
                            elif type(rhs) is Id:
                                rhsSymbol = self.visit(rhs, c)
                                if type(rhsSymbol.value) is not IntLiteral:
                                    raise TypeMismatch(rhs)
                                else:
                                    rhs = rhsSymbol.value

                            if int(lhs.value) != int(rhs.value):
                                raise TypeMismatch(ast)
                            
                    
                    c[0] += [Symbol(ast.varName, ast.varType, ast.varInit)]
                
        # print(c[0][-1])
        return c
    
    def CheckIfStructHasAllInterfaceMethods(self, found: Symbol, varInitType: Symbol):
        
        structMethods = []
        
        for method in varInitType.mtype.methods:
            met = AST.Prototype(method.fun.name, [x.parType for x in method.fun.params], method.fun.retType)
            structMethods += [met]
        
        # print("found")
        # for i in found.mtype.methods:
        #    print(i)
        
        # print("varInitType")
        # for i in structMethods:
        #     print(i)
            
        for proto in  found.mtype.methods:
            res = self.lookup(proto.name, structMethods, lambda x: x.name)
            if res is None:
                return False
            else:
                if not self.prototype_equal(proto, res):
                    return False
                
        return True
    
    def prototype_equal(self,p1, p2):
        
        if len(p1.params) != len(p2.params):
            return False
        
        for t1, t2 in zip(p1.params, p2.params):
            if type(t1) is not type(t2):  
                return False
    
        if type(p1.retType) is Id and type(p2.retType) is Id:
            if p1.retType.name != p2.retType.name:
                return False
        elif type(p1.retType) != type(p2.retType):
            return False
        
        return True
    
    
    # ConstDecl(Decl,BlockMember):
    # conName : str
    # conType : Type # None if there is no type 
    # iniExpr : Expr
    def visitConstDecl(self, ast: ConstDecl, c):
        if self.lookup(ast.conName, c[0], lambda x: x.name) is not None:
            raise Redeclared(Constant(), ast.conName)
        
        initType = self.visit(ast.iniExpr, c)
    
        if ast.conType is None:
            ast.conType = initType

        if type(initType) is Symbol:
            c[0] += [Symbol(ast.conName, initType.mtype, initType.value)]
        else:
            c[0] += [Symbol(ast.conName, initType, ast.iniExpr)]
        
        return c
    
    # FuncDecl(Decl):
    # name: str
    # params: List[ParamDecl]
    # retType: Type # VoidType if there is no return type
    # body: Block
    def visitFuncDecl(self,ast: FuncDecl, c):
        func_scope = [[]] + c
        for param in ast.params:
            func_scope = self.visit(param, func_scope)
        
        reType = None
        if type(ast.retType) is Id:
            found = self.lookup(ast.retType.name, c[-1], lambda x: x.name)
            if found is None:
                raise Undeclared(Identifier(), ast.retType.name)
            reType = found.mtype
        else:
            reType = ast.retType
        func_scope[0] += [Symbol("MarkDownFunc", MType( ast.params, reType))]
        self.visit(ast.body, func_scope)
        return c

    # MethodDecl(Decl):             # FuncDecl(Decl):               StructType(Type):
    # receiver: str                 # name: str                         name: str
    # recType: Type                 # params: List[ParamDecl]           elements:List[tuple[str,Type]]
    # fun: FuncDecl                 # retType: Type                     methods:List[MethodDecl]
                                    # body: Block
    
    def visitMethodDecl(self, ast: MethodDecl, c):
        
        o = [[]] + c
        
        for symbol in c[-1]:
            if symbol.name == ast.recType.name:                     # kiem tra recType co ton tai trong scope
                
                if type(symbol.mtype) is StructType:                
                    for ele in symbol.mtype.elements:
                        if ele[0] == ast.fun.name:
                            raise Redeclared(Method(), ast.fun.name)
                    o[0] += [Symbol(ast.receiver, symbol.mtype)]    # them receiver vao local scope
                    for param in ast.fun.params:
                        o = self.visit(param, o)
                    o[0] += [Symbol("MarkDownFunc", MType( ast.fun.params, ast.fun.retType))]
                    o = self.visit(ast.fun.body, o)
                    return c
                # elif type(recType) is InterfaceType:
                #     recType = recType.name 
        
        # print("MethodDecl not found recType Error: ", ast)
        
        return c
    
    # StructType(Type):
    # name: str
    # elements:List[tuple[str,Type]]
    # methods:List[MethodDecl]
    def visitStructType(self, ast: StructType, c):
        o = [] 
        for ele in ast.elements:
            if self.lookup(ele[0], o, lambda x: x.name) is not None:
                raise Redeclared(Field(), ele[0])
            o += [Symbol(ele[0], ele[1])]
        return c
    
    # InterfaceType(Type):
    # name: str
    # methods:List[Prototype]
    def visitInterfaceType(self, ast: InterfaceType, c):
        o = []
        for proto in ast.methods:
            o = self.visit(proto, o)
            
        return c
    
    # Prototype(AST):
    # name: str
    # params:List[Type]
    # retType: Type # VoidType if there is no return type
    def visitPrototype(self, ast: Prototype, c):
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Prototype(), ast.name)
        c += [Symbol(ast.name, MType([param for param in ast.params], ast.retType))]
        return c
    
    
    # Assign(Stmt):
    # lhs: LHS (id, arraycell: eleType, fieldaccess: symbol)
    # rhs: Expr # if assign operator is +=, rhs is BinaryOp(+,lhs,rhs), similar to -=,*=,/=,%=
    def visitAssign(self, ast: Assign, c):
        isDeclare = False
        lhs = None
        carryInterface = None
        if type(ast.lhs) is Id:
            res = self.lookup(ast.lhs.name, c[0], lambda x: x.name)
            carryInterface = res
            if res is None:
                lhs = ast.lhs
                isDeclare = True
            elif type(res.mtype) is MType:
                lhs = res.mtype.rettype
            elif type(res.mtype) is Symbol:
                lhs = res.mtype.mtype
            else:
                lhs = res.mtype
        if type(ast.lhs) is ArrayCell:  
            lhs = self.visit(ast.lhs, c)
        if type(ast.lhs) is FieldAccess: 
            lhs = self.visit(ast.lhs, c).mtype
            
            
        rhs = self.visit(ast.rhs, c)        # can be Type ( literal )  || Symbol (expr)

        # print("lhs", lhs, "rhs", rhs)
        if type(rhs) is Symbol:
            rhsType = rhs.mtype
            if type(rhsType) is MType:
                rhsType = rhsType.rettype
            if type(lhs) is Id and isDeclare:            
                c[0] += [Symbol(lhs.name, rhs)]
            if type(lhs) is not type(rhsType):
                raise TypeMismatch(ast)
            else:
                if type(lhs) is ArrayType:
                    if type(lhs.eleType) is not type(rhsType.eleType):  # kiem tra kieu cua mang
                        raise TypeMismatch(ast)
                    if len(lhs.dimens) != len(rhsType.dimens):          # va so chieu
                        raise TypeMismatch(ast)
                    
                    # for i in range(len(lhs.dimens)):
                    #     print(lhs.dimens[i])
                    #     print(rhsType.dimens[i])
                if type(lhs) is StructType:
                    
                    pass
                return c
        else:
            if type(lhs) is Id and isDeclare:            
                c[0] += [Symbol(lhs.name, rhs)]
            elif type(lhs) is InterfaceType and type(rhs) is StructType:
                found = Symbol(lhs.name, lhs)
                init = Symbol(rhs.name, rhs)
                if self.CheckIfStructHasAllInterfaceMethods(found, init) is False:
                    raise TypeMismatch(ast)
                for symbol in c[0]:
                    if symbol.name == carryInterface.name and type(symbol.mtype) == InterfaceType:
                        symbol.mtype = rhs
                        break
            elif type(lhs) is not type(rhs):
                raise TypeMismatch(ast)
            else:
                if type(lhs) is ArrayType:
                    pass
                if type(lhs) is StructType:
                    pass
                return c
        return c
    
    
    # Id(Type,LHS):
    # name : str
    def visitId(self,ast: Id,c):
        for env in c:
            res = self.lookup(ast.name, env, lambda x: x.name)
            if res is not None:
                return res
       
        # Nếu không tìm thấy biến trong tất cả các scope, ném ra lỗi Undeclared
        raise Undeclared(Identifier(), ast.name)
    
    # Type Nodes
    def visitIntType(self, ast, c):
        return IntType()
    
    def visitFloatType(self, ast, c):
        return FloatType()
    
    def visitBoolType(self, ast, c):
        return BoolType()
    
    def visitStringType(self, ast, c):
        return StringType()
    
    def visitVoidType(self, ast, c):
        return VoidType()
    
    # ArrayType(Type):
    # dimens:List[Expr]
    # eleType:Type
    def visitArrayType(self, ast, c):
        # Giả sử ast có thuộc tính: dimens và eleType
        for dimen in ast.dimens:
            dimentype = self.visit(dimen, c)
            if type(dimentype) is Symbol:
                dimentype = dimentype.mtype
                if type(dimentype) is not IntType:
                    raise TypeMismatch(ast)
            if type(dimentype) is not IntType:
                raise TypeMismatch(ast)
        return ArrayType(ast.dimens, self.visit(ast.eleType, c))
    
    
    # Block(Stmt):
    # member:List[BlockMember]
    def visitBlock(self, ast: Block, c):
        for member in ast.member:
            self.visit(member, c)
        return c
    
    # If(Stmt):
    # expr:Expr
    # thenStmt:Stmt
    # elseStmt:Stmt # None if there is no else
    def visitIf(self, ast, c):
        condType = self.visit(ast.expr, c)
        if type(condType) is Symbol:
            condType = condType.mtype
        if type(condType) is MType:
            condType = condType.rettype
        if type(condType) is not BoolType:
            raise TypeMismatch(ast.expr)
        # print(condType)
        
        o = [[]] + c
        self.visit(ast.thenStmt, o)
        if ast.elseStmt:
            o = [[]] + c
            self.visit(ast.elseStmt, o)
        return None
    
    # ForBasic(Stmt):
    # cond:Expr
    # loop:Block
    def visitForBasic(self, ast, c):
        condType = self.visit(ast.cond, c)
        if type(condType) != type(BoolType()):
            raise TypeMismatch(ast)
        o = [[]] + c 
        self.visit(ast.loop, o)
        return None
    
    # ForStep(Stmt):
    # init:Stmt
    # cond:Expr
    # upda:Assign
    # loop:Block
    def visitForStep(self, ast, c):
        o = [[]] + c
        o = self.visit(ast.init, o)
        
        condType = self.visit(ast.cond, o)
        if type(condType) != type(BoolType()):
            raise TypeMismatch(ast)
        o = self.visit(ast.upda, o)
        self.visit(ast.loop, o)
        return c
    
    # ForEach(Stmt):
    # idx: Id
    # value: Id
    # arr: Expr
    # loop:Block
    def visitForEach(self, ast, c):
        # Duyệt qua mảng và thân vòng lặp
        arrayType = self.visit(ast.arr, c)
        if type(arrayType) is Symbol:
            arrayType = arrayType.mtype
        if type(arrayType) is MType:
            arrayType = arrayType.rettype
        if type(arrayType) is not ArrayType:
            raise TypeMismatch(ast)
        o = [[]] + c
        
        if ast.idx.name != '_':
            o[0] += [Symbol(ast.idx.name, IntType())]
        if ast.value.name != '_':
            o[0] += [Symbol(ast.value.name, arrayType.eleType)]
        
        
        self.visit(ast.loop, o)
        return None
    
    # Break và Continue
    def visitBreak(self, ast, c):
        return None
    
    def visitContinue(self, ast, c):
        return None
    
    # Return Statement
    def visitReturn(self, ast, c):
        

        if ast.expr is not None:
            returnType = self.visit(ast.expr, c)
        else:
            returnType = VoidType()
            
        if type(returnType) is Symbol:
            returnType = returnType.mtype
        if type(returnType) is MType:
            returnType = returnType.rettype
        # print("ReturnType", returnType)
        for index in range(len(c) - 1) :        # khong kiem tra global env
            env = c[index]
            for symbol in env:
                # print("symbol", symbol)
                if type(symbol.mtype) is MType:
                    if type(symbol.mtype.rettype) is not type(returnType):
                        
                        # print("symbol-returnType ",symbol, returnType)
                        if type(returnType) is StructType and type(symbol.mtype.rettype) is InterfaceType:
                            returnType = Symbol("returnStm", returnType)
                            newSymbol = Symbol(symbol.name, symbol.mtype.rettype) # old symbol la function, can chuyen rettype thanh mtype 
                            if self.CheckIfStructHasAllInterfaceMethods(newSymbol, returnType) is False:
                                raise TypeMismatch(ast)
                            else:
                                return None
                            
                        raise TypeMismatch(ast)
                    else:
                        # print("symbol-returnType ",symbol, returnType)
                        if type(returnType) is StructType or type(returnType) is InterfaceType:
                            if returnType.name != symbol.mtype.rettype.name:
                                raise TypeMismatch(ast)

                        return None         
        return None

    
    # ArrayCell(LHS):
    # arr:Expr
    # idx:List[Expr]
    def visitArrayCell(self, ast, c):
        arrType = self.visit(ast.arr, c)
        
        if type(arrType) is Symbol:
            arrType = arrType.mtype
        if type(arrType) is MType:
            arrType = arrType.rettype
        if type(arrType) is not ArrayType:
            raise TypeMismatch(ast)
        
        # print("ArrayCell", arrType)
        
        for idx in ast.idx:
            idxType = self.visit(idx, c)
            if type(idxType) is Symbol:
                idxType = idxType.mtype
            if type(idxType) is MType:
                idxType = idxType.rettype
            if type(idxType) is not IntType:
                raise TypeMismatch(ast)
        return arrType.eleType
    
    
    
    # BinaryOp(Expr):
    # op:str
    # left:Expr
    # right:Expr
    def visitBinaryOp(self, ast, c):
        leftType = self.visit(ast.left, c)
        rightType = self.visit(ast.right, c)

        if type(leftType) is Symbol:
            leftType = leftType.mtype
        if type(rightType) is Symbol:
            rightType = rightType.mtype
            
        if type(leftType) is MType:
            leftType = leftType.rettype
        if type(rightType) is MType:
            rightType = rightType.rettype
            
        if type(leftType) not in [BoolType, IntType, FloatType, StringType]:
            raise TypeMismatch(ast.left)
        elif type(rightType) not in [BoolType, IntType, FloatType, StringType]:
            raise TypeMismatch(ast.right)
        
        # print("BinaryOp", leftType, rightType)
        
        if ast.op in ['-', '*', '/']:
            if (isinstance(leftType, IntType) or isinstance(leftType, FloatType)) and \
               (isinstance(rightType, IntType) or isinstance(rightType, FloatType)):
                if isinstance(leftType, FloatType) or isinstance(rightType, FloatType):
                    return FloatType()
                return IntType()
            else:
                raise TypeMismatch(ast)
        elif ast.op in ['%']:
            if isinstance(leftType, IntType) and isinstance(rightType, IntType):
                return IntType()
            else:
                raise TypeMismatch(ast)
        elif ast.op in ['+']:
            
            if (isinstance(leftType, IntType) or isinstance(leftType, FloatType)) and \
               (isinstance(rightType, IntType) or isinstance(rightType, FloatType)):
                if isinstance(leftType, FloatType) or isinstance(rightType, FloatType):
                    return FloatType()
                return IntType() 
            elif isinstance(leftType, StringType) and isinstance(rightType, StringType):
                return StringType()
            else:
                raise TypeMismatch(ast)
            
        elif ast.op in ['&&', '||', '!']:
            if isinstance(leftType, BoolType) and isinstance(rightType, BoolType):
                return BoolType()
            else:
                raise TypeMismatch(ast)
        elif ast.op in ['<', '<=', '>', '>=', '==', '!=']:
            if type(leftType) is type(rightType):
                return BoolType()
            else:
                raise TypeMismatch(ast)
            
        return None
    
    # UnaryOp(Expr):
    # op:str
    # body:Expr
    def visitUnaryOp(self, ast, c):
        bodyType = self.visit(ast.body, c)
        if type(bodyType) is Symbol:
            bodyType = bodyType.mtype
        if type(bodyType) is MType:
            bodyType = bodyType.rettype
        # print("UnaryOp", bodyType)
        if ast.op == '-':
            if isinstance(bodyType, IntType) or isinstance(bodyType, FloatType):
                return bodyType
            else:
                raise TypeMismatch(ast)
        elif ast.op == '!':
            if isinstance(bodyType, BoolType):
                return BoolType()
            else:
                raise TypeMismatch(ast)
        return None
    
    
    # FieldAccess(LHS):         StructType(Type):
    # receiver:Expr             name: str
    # field:str                 elements:List[tuple[str,Type]]
    #                           methods:List[MethodDecl]
    ## chua hien thuc value ##
    def visitFieldAccess(self, ast: FieldAccess, c):
        receiver = self.visit(ast.receiver, c)              # kiem tra receiver co ton tai trong scope
        # print(receiver)
        if type(receiver) is Symbol:                        # neu ton tai thi kiem tra field co ton tai trong struct
            if type(receiver.mtype) is StructType:
                found = self.lookup(ast.field, receiver.mtype.elements, lambda x: x[0])     #tuple[str,Type]
                
                if found is None:
                    raise Undeclared(Field(), ast.field)
                
                if type(found[1]) is Id:
                    found1Type = self.lookup(found[1].name, c[-1], lambda x: x.name) # find a symbol in global env
                    if type(found1Type.mtype) is StructType:
                        return Symbol(found[0], found1Type.mtype)  # tra ve Symbol
                    
                return Symbol(found[0], found[1])  # tra ve Symbol
                
            else:
                raise TypeMismatch(ast)
        else:
            pass
            # print("FieldAcess unknowError:", receiver)
        return c
    
    
    # FuncCall(Expr,Stmt):
    # funName:str
    # args:List[Expr] # [] if there is no arg 
    def visitFuncCall(self, ast: FuncCall, c):
        res = self.lookup(ast.funName, c[-1], lambda x: x.name)
        if res is None or type(res.mtype) is not MType:
            raise Undeclared(Function(), ast.funName)

        args = []
        for arg in ast.args:
            tmp = self.visit(arg, c)
            if type(tmp) is Symbol:
                args += [tmp.mtype]
            else:
                args += [tmp]
        
       
        if len(args) != len(res.mtype.partype):
            raise TypeMismatch(ast)
        
        for i in range(len(args)):
            if type(args[i]) is not type(res.mtype.partype[i]):
                if type(res.mtype.partype[i]) is Id and type(args[i]) is StructType:
                    if res.mtype.partype[i].name != args[i].name:
                        raise TypeMismatch(ast)
                    else:
                        pass
                else:
                    raise TypeMismatch(ast)
        
        # print("c[0]")
        # for i in c[0]:
        #     print(i)
        return Symbol(ast.funName, res.mtype)
    
    # MethCall(Expr,Stmt):          StructType(Type):
    # receiver: Expr                 name: str
    # metName: str                   elements:List[tuple[str,Type]]
    # args:List[Expr]               methods:List[MethodDecl]
    
    # MethodDecl(Decl):             FuncDecl(Decl):
    # receiver: str                     name: str
    # recType: Type                     params: List[ParamDecl]
    # fun: FuncDecl                     retType: Type # VoidType if there is no return type
    #                                   body: Block
    def visitMethCall(self, ast: MethCall, c):
        receiver = self.visit(ast.receiver, c) 
        
        args = []
        for arg in ast.args:
            tmp = self.visit(arg, c)
            if type(tmp) is Symbol:
                args += [tmp.mtype]
            else:
                args += [tmp]
       
        # print(receiver)
        if type(receiver) is Symbol:
            if type(receiver.mtype) is StructType:
                found = self.lookup(ast.metName, receiver.mtype.methods, lambda x: x.fun.name) #MethodDecl
                if found is None:
                    raise Undeclared(Method(), ast.metName)
                
                methodFun = MType([param.parType for param in found.fun.params], found.fun.retType)
                if len(args) != len(methodFun.partype):
                    raise TypeMismatch(ast)
                
                for i in range(len(args)):
                    if type(args[i]) is not type(methodFun.partype[i]):
                        # print(args[i], methodFun.partype[i])
                        raise TypeMismatch(ast)
                # print("Method:", methodFun)
                return Symbol(ast.metName, methodFun)
            
            elif type(receiver.mtype) is InterfaceType:
                found = self.lookup(ast.metName, receiver.mtype.methods, lambda x: x.name)  #Prototype
                if found is None:
                    raise Undeclared(Method(), ast.metName)
                
                # chua check param ************************
                
                methodFun = MType(found.params, found.retType)
                # print("Method:", methodFun)
                return Symbol(ast.metName, methodFun)
            else:
                raise TypeMismatch(ast)
        else:
            raise TypeMismatch(ast)
            pass
        return c
    
    # Literals
    def visitIntLiteral(self, ast: IntLiteral, c):
        return IntType()
    
    def visitFloatLiteral(self, ast, c):
        return FloatType()
    
    def visitStringLiteral(self, ast, c):
        return StringType()
    
    def visitBooleanLiteral(self, ast, c):
        return BoolType()
    
    # ArrayLiteral(Literal):
    # dimens:List[Expr]
    # eleType: Type
    # value: NestedList
    def visitArrayLiteral(self, ast, c):
        # for element in ast.value:
        #     self.visit(element, c)
        return ArrayType(ast.dimens, ast.eleType)
    
    # StructLiteral(Literal):
    # name:str
    # elements: List[tuple[str,Expr]] # [] if there is no elements
    def visitStructLiteral(self, ast: StructLiteral, c):
        # for fieldName, expr in ast.elements:
        #     self.visit(expr, c)
        res = self.lookup(ast.name, c[-1], lambda x: x.name)
        if res is None:
            raise Undeclared(Identifier(),ast.name)
        
        return res.mtype
    def visitNilLiteral(self, ast, c):
        
        return None
    