from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):
     # Grammar: program: list_decl EOF;
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        # Gọi visit cho rule list_decl và tạo node Program
        decls = self.visit(ctx.list_decl())
        return Program(decls)
    
    # Grammar: list_decl: list_decl declared_stmt SEMICOLON | declared_stmt SEMICOLON;
    def visitList_decl(self, ctx: MiniGoParser.List_declContext):
        if ctx.list_decl():
            # list_decl declared_stmt SEMICOLON
            return self.visit(ctx.list_decl()) + [self.visit(ctx.declared_stmt())]
        else:
            # declared_stmt SEMICOLON
            return [self.visit(ctx.declared_stmt())]
    
    # Grammar: declared_stmt: vardecl | constdecl | structdecl | funcdecl | methoddecl | interfacedecl;
    def visitDeclared_stmt(self, ctx: MiniGoParser.Declared_stmtContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        elif ctx.constdecl():
            return self.visit(ctx.constdecl())
        elif ctx.structdecl():
            return self.visit(ctx.structdecl())
        elif ctx.funcdecl():
            return self.visit(ctx.funcdecl())
        elif ctx.methoddecl():
            return self.visit(ctx.methoddecl())
        elif ctx.interfacedecl():
            return self.visit(ctx.interfacedecl())
        else:
            return None

    # Grammar: vardecl: vardecl1 | vardecl2;
    def visitVardecl(self, ctx: MiniGoParser.VardeclContext):
        if ctx.vardecl1():
            return self.visit(ctx.vardecl1())
        else:
            return self.visit(ctx.vardecl2())
    
    # Grammar: vardecl1: VAR ID (atomictype | arraytype)? ASSIGN expr;
    def visitVardecl1(self, ctx: MiniGoParser.Vardecl1Context):
        varName = ctx.ID().getText()
        # Xử lý kiểu của biến nếu có (atomictype hoặc arraytype)
        if ctx.atomictype():
            varType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            varType = self.visit(ctx.arraytype())
        else:
            varType = None
        # Xử lý biểu thức khởi tạo
        varInit = self.visit(ctx.expr())
        return VarDecl(varName, varType, varInit)
    
    # Grammar: vardecl2: VAR ID (atomictype | arraytype);
    def visitVardecl2(self, ctx: MiniGoParser.Vardecl2Context):
        varName = ctx.ID().getText()
        # Xử lý kiểu của biến nếu có
        if ctx.atomictype():
            varType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            varType = self.visit(ctx.arraytype())
        else:
            varType = None
        # Không có biểu thức khởi tạo
        return VarDecl(varName, varType, None)
    
    # Grammar: constdecl: CONST ID ASSIGN expr;
    def visitConstdecl(self, ctx: MiniGoParser.ConstdeclContext):
        conName = ctx.ID().getText()
        iniExpr = self.visit(ctx.expr())
        # Ở đây chưa có khai báo kiểu cho hằng, đặt conType là None
        return ConstDecl(conName, None, iniExpr)
 
    # Grammar: structdecl: TYPE ID STRUCT L_BRACE list_field R_BRACE;
    def visitStructdecl(self, ctx: MiniGoParser.StructdeclContext):
        structName = ctx.ID().getText()
        fields = self.visit(ctx.list_field())
        # Chưa xử lý phần method của struct, truyền danh sách rỗng
        return StructType(structName, fields, [])
    
    # Grammar: list_field: list_field field | field;
    def visitList_field(self, ctx: MiniGoParser.List_fieldContext):
    # Nếu có con list_field, tức alternative: list_field field
        if ctx.list_field():
            left_fields = self.visit(ctx.list_field())
            current_field = self.visit(ctx.field())
            return left_fields + [current_field]
        else:
            # Alternative chỉ có field
            return [self.visit(ctx.field())]
    
    # Grammar: field: ID (atomictype | arraytype) SEMICOLON;
    def visitField(self, ctx: MiniGoParser.FieldContext):
        fieldName = ctx.ID().getText()
        if ctx.atomictype():
            fieldType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            fieldType = self.visit(ctx.arraytype())
        else:
            fieldType = None
        return (fieldName, fieldType)
    
    # Grammar: funcdecl: FUNC ID L_PAREN list_parameter R_PAREN (atomictype | arraytype)? L_BRACE list_stmt R_BRACE;
    def visitFuncdecl(self, ctx: MiniGoParser.FuncdeclContext):
        funcName = ctx.ID().getText()
        params = self.visit(ctx.list_parameter()) if ctx.list_parameter() else []
        if ctx.atomictype():
            retType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            retType = self.visit(ctx.arraytype())
        else:
            retType = VoidType()  # Mặc định nếu không có kiểu trả về
        body = Block(self.visit(ctx.list_stmt()))
        return FuncDecl(funcName, params, retType, body)
    
    # Grammar: list_parameter: paramprime | ;
    def visitList_parameter(self, ctx: MiniGoParser.List_parameterContext):
        if ctx.paramprime():
            return self.visit(ctx.paramprime())
        else:
            return []
    
    # Grammar: paramprime: paramprime COMMA parameter | parameter;
    def visitParamprime(self, ctx: MiniGoParser.ParamprimeContext):     
        # Nếu có alternative đệ quy: paramprime COMMA parameter
        if ctx.paramprime():
            left_params = self.visit(ctx.paramprime())
            current_params = self.visit(ctx.parameter())
            return left_params + current_params
        else:
            # Alternative chỉ có parameter
            return self.visit(ctx.parameter())
    
    # Grammar: parameter: list_ID (atomictype | arraytype);
    def visitParameter(self, ctx: MiniGoParser.ParameterContext):
        if ctx.atomictype():
            paramType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            paramType = self.visit(ctx.arraytype())
        else:
            paramType = None
        # list_ID trả về danh sách tên tham số
        ids = self.visit(ctx.list_ID())
        return [ParamDecl(i, paramType) for i in ids]
    
    # Grammar: list_ID: list_ID COMMA ID | ID;
    def visitList_ID(self, ctx: MiniGoParser.List_IDContext):
        if ctx.list_ID():
            left = self.visit(ctx.list_ID())
            current_id = ctx.ID().getText()
            return left + [current_id]
        else:
            # Alternative chỉ có một ID
            return [ctx.ID().getText()]
    
    # Grammar: methoddecl:
    # FUNC L_PAREN ID ID R_PAREN ID L_PAREN list_parameter R_PAREN (atomictype | arraytype)? L_BRACE list_stmt R_BRACE;
    def visitMethoddecl(self, ctx: MiniGoParser.MethoddeclContext):
        # ID(0): receiver name, ID(1): receiver type, ID(2): method name
        receiver = ctx.ID(0).getText()
        recType = Id(ctx.ID(1).getText())
        methodName = ctx.ID(2).getText()
        params = self.visit(ctx.list_parameter()) if ctx.list_parameter() else []
        if ctx.atomictype():
            retType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            retType = self.visit(ctx.arraytype())
        else:
            retType = VoidType()
        body = Block(self.visit(ctx.list_stmt()))
        func = FuncDecl(methodName, params, retType, body)
        return MethodDecl(receiver, recType, func)

    # Grammar: interfacedecl: TYPE ID INTERFACE L_BRACE list_methodInterface R_BRACE;
    def visitInterfacedecl(self, ctx: MiniGoParser.InterfacedeclContext):
        interfaceName = ctx.ID().getText()
        methods = self.visit(ctx.list_methodInterface())
        return InterfaceType(interfaceName, methods)
    
    # Grammar: list_methodInterface: list_methodInterface methodInterface | methodInterface;
    def visitList_methodInterface(self, ctx: MiniGoParser.List_methodInterfaceContext):
        if ctx.list_methodInterface():
            left_methods = self.visit(ctx.list_methodInterface())
            right_method = self.visit(ctx.methodInterface())
            return left_methods + [right_method]
        else:
            return [ self.visit(ctx.methodInterface())]
            
        
    
    # Grammar: methodInterface: ID L_PAREN list_parameter R_PAREN (atomictype | arraytype | ) SEMICOLON;
    def visitMethodInterface(self, ctx: MiniGoParser.MethodInterfaceContext):
        methodName = ctx.ID().getText()
        params = self.visit(ctx.list_parameter()) if ctx.list_parameter() else []
        if params != []:
            params = [param.parType for param in params]
            
        if ctx.atomictype():
            retType = self.visit(ctx.atomictype())
        elif ctx.arraytype():
            retType = self.visit(ctx.arraytype())
        else:
            retType = VoidType()
        return Prototype(methodName, params, retType)

    # Grammar: atomictype: INT | FLOAT | STRING | BOOLEAN | ID;
    def visitAtomictype(self, ctx: MiniGoParser.AtomictypeContext):
        token = ctx.getText()
        if token == "int":
            return IntType()
        elif token == "float":
            return FloatType()
        elif token == "string":
            return StringType()
        elif token == "boolean":
            return BoolType()
        else:
            # Nếu không phải các kiểu có sẵn, coi là kiểu người dùng định nghĩa
            return Id(token)
    
    # Grammar: arraytype: arraytype1 atomictype;
    def visitArraytype(self, ctx: MiniGoParser.ArraytypeContext):
        eleType = self.visit(ctx.atomictype())
        dimens = self.visit(ctx.arraytype1())
        return ArrayType(dimens, eleType)
    
    # Grammar: 
    # arraytype1:
    #    arraytype1 L_BRACKET (INT_LIT | ID) R_BRACKET
    #  | L_BRACKET (INT_LIT | ID) R_BRACKET;
    def visitArraytype1(self, ctx: MiniGoParser.Arraytype1Context):
        if ctx.arraytype1():
            left = self.visit(ctx.arraytype1())
            if ctx.INT_LIT():
                return left + [IntLiteral(int(ctx.INT_LIT().getText()))]
            else:
                return left + [Id(ctx.ID().getText())]
        else:
            if ctx.INT_LIT():
                return [IntLiteral(int(ctx.INT_LIT().getText()))]
            else:
                return [Id(ctx.ID().getText())]
    # --------------------------------------------------------------------------------
    
    # Grammar: list_stmt: list_stmt stmt | stmt | ;
    def visitList_stmt(self, ctx: MiniGoParser.List_stmtContext):
        # Nếu không có con nào (empty alternative), trả về danh sách rỗng
        if ctx.getChildCount() == 0:
            return []
        # Nếu có phần list_stmt con, nghĩa là sử dụng alternative: list_stmt stmt
        if ctx.list_stmt():
            left_list = self.visit(ctx.list_stmt())
            current_stmt = self.visit(ctx.stmt())
            return left_list + [current_stmt]
        elif ctx.stmt():
            # Alternative: stmt
            return [self.visit(ctx.stmt())]
        else:
            return []
    
    # Grammar: 
    # stmt: ( declared_stmt 
    #       | assignment_stmt 
    #       | if_stmt 
    #       | loop_stmt 
    #       | break_stmt 
    #       | continue_stmt 
    #       | functionCall_stmt 
    #       | methodCall_stmt 
    #       | return_stmt ) SEMICOLON;
    def visitStmt(self, ctx: MiniGoParser.StmtContext):
        # Kiểm tra từng lựa chọn có trong stmt và gọi visit tương ứng
        if ctx.declared_stmt():
            return self.visit(ctx.declared_stmt())
        elif ctx.assignment_stmt():
            return self.visit(ctx.assignment_stmt())
        elif ctx.if_stmt():
            return self.visit(ctx.if_stmt())
        elif ctx.loop_stmt():
            return self.visit(ctx.loop_stmt())
        elif ctx.break_stmt():
            return self.visit(ctx.break_stmt())
        elif ctx.continue_stmt():
            return self.visit(ctx.continue_stmt())
        elif ctx.functionCall_stmt():
            return self.visit(ctx.functionCall_stmt())
        elif ctx.methodCall_stmt():
            return self.visit(ctx.methodCall_stmt())
        elif ctx.return_stmt():
            return self.visit(ctx.return_stmt())
        else:
            return None

    # Grammar: 
    # assignment_stmt: lhs (DECLARE_ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN) expr;
    def visitAssignment_stmt(self, ctx: MiniGoParser.Assignment_stmtContext):
        lhs_node = self.visit(ctx.lhs())
        expr_node = self.visit(ctx.expr())
        op = ctx.getChild(1).getText()  # Lấy toán tử (vd: ":=", "+=", etc.)
        if op == ":=":
            return Assign(lhs_node, expr_node)
        else:
            # Với các augmented assignment (+=, -=, ...), chuyển thành dạng:
            # lhs = lhs op expr  -->  BinaryOp(op, lhs, expr)
            base_op = op[0]  # Lấy ký tự đầu (vd: '+' từ "+=")
            new_rhs = BinaryOp(base_op, lhs_node, expr_node)
            return Assign(lhs_node, new_rhs)

    # Grammar: 
    # if_stmt: IF L_PAREN expr R_PAREN L_BRACE list_stmt R_BRACE else_if_stmt else_stmt;
    def visitIf_stmt(self, ctx: MiniGoParser.If_stmtContext):
        condition = self.visit(ctx.expr())
        then_block = Block(self.visit(ctx.list_stmt()))
        else_if_part = self.visit(ctx.else_if_stmt()) if ctx.else_if_stmt() is not None else None
        else_part = self.visit(ctx.else_stmt()) if ctx.else_stmt() is not None else None
        
        if else_if_part is None:
            return If(condition, then_block, else_part)
        else:
            cur_if = else_if_part.elseStmt
            last_if = else_if_part
            while isinstance(cur_if, If):
                last_if = cur_if
                cur_if = cur_if.elseStmt
            
            if last_if.elseStmt is None :
                last_if.elseStmt = else_part
            return If(condition, then_block, else_if_part)
    
    # Grammar: 
    # else_if_stmt: else_if_stmt ELSE IF expr L_BRACE list_stmt R_BRACE | ;
    def visitElse_if_stmt(self, ctx: MiniGoParser.Else_if_stmtContext):
        # Nếu không có else-if thì trả về None
        if ctx.getChildCount() == 0:
            return None
        else:
            # Nếu có, ta xây dựng một node If cho lần đầu tiên và lồng dần nếu còn nhiều hơn
            condition = self.visit(ctx.expr())
            then_block = Block(self.visit(ctx.list_stmt()))
            else_if_part = self.visit(ctx.else_if_stmt())
            return If(condition, then_block, else_if_part)
    
    # Grammar: 
    # else_stmt: ELSE L_BRACE list_stmt R_BRACE | ;
    def visitElse_stmt(self, ctx: MiniGoParser.Else_stmtContext):
        if ctx.getChildCount() == 0:
            return None
        else:
            return Block(self.visit(ctx.list_stmt()))
    
    # Grammar: 
    # loop_stmt:
    #   FOR expr L_BRACE list_stmt R_BRACE
    # | FOR assignment_stmt SEMICOLON expr SEMICOLON assignment_stmt L_BRACE list_stmt R_BRACE
    # | FOR vardecl SEMICOLON expr SEMICOLON assignment_stmt L_BRACE list_stmt R_BRACE
    # | FOR ID COMMA ID DECLARE_ASSIGN RANGE expr L_BRACE list_stmt R_BRACE
    # | FOR '_' COMMA ID DECLARE_ASSIGN RANGE expr L_BRACE list_stmt R_BRACE;
    def visitLoop_stmt(self, ctx: MiniGoParser.Loop_stmtContext):
        # Nếu chỉ có expr L_BRACE list_stmt R_BRACE -> ForBasic
        
        if ctx.getChildCount() == 5:
            cond = self.visit(ctx.expr())
            loop_block = Block(self.visit(ctx.list_stmt()))
            return ForBasic(cond, loop_block)
        # Nếu có cấu trúc: assignment_stmt ; expr ; assignment_stmt
        elif ctx.assignment_stmt() is not None and len(ctx.assignment_stmt()) == 2:
            init = self.visit(ctx.assignment_stmt(0))
            cond = self.visit(ctx.expr())
            update = self.visit(ctx.assignment_stmt(1))
            loop_block = Block(self.visit(ctx.list_stmt()))
            return ForStep(init, cond, update, loop_block)
        # Nếu có cấu trúc: vardecl ; expr ; assignment_stmt
        elif ctx.vardecl() is not None:
            init = self.visit(ctx.vardecl())
            cond = self.visit(ctx.expr())
            update = self.visit(ctx.assignment_stmt(0))
            loop_block = Block(self.visit(ctx.list_stmt()))
            return ForStep(init, cond, update, loop_block)
        # Nếu có dạng foreach: FOR ID COMMA ID DECLARE_ASSIGN RANGE expr L_BRACE list_stmt R_BRACE
        else:
            # Giả sử các token ID xuất hiện theo thứ tự: [idx, value, arrayID]
            ids = ctx.ID()
            if len(ids) == 2:
                idx = Id(ids[0].getText())
                value = Id(ids[1].getText())
            else:
                # Nếu không đủ, đặt giá trị mặc định
                idx = Id("_")
                value = Id(ids[0].getText())
            
            arr = self.visit(ctx.expr())
            loop_block = Block(self.visit(ctx.list_stmt()))
            return ForEach(idx, value, arr, loop_block)
    
    # Grammar: break_stmt: BREAK;
    def visitBreak_stmt(self, ctx: MiniGoParser.Break_stmtContext):
        return Break()
    
    # Grammar: continue_stmt: CONTINUE;
    def visitContinue_stmt(self, ctx: MiniGoParser.Continue_stmtContext):
        return Continue()
    
    # Grammar: 
    # functionCall_stmt: ID L_PAREN list_expr R_PAREN | ID L_PAREN R_PAREN;
    def visitFunctionCall_stmt(self, ctx: MiniGoParser.FunctionCall_stmtContext):
        funcName = ctx.ID().getText()
        args = self.visit(ctx.list_expr()) if ctx.list_expr() is not None else []
        return FuncCall(funcName, args)
    
    # Grammar: 
    # methodCall_stmt: methodCall L_PAREN list_expr? R_PAREN;
    def visitMethodCall_stmt(self, ctx: MiniGoParser.MethodCall_stmtContext):
        meth = self.visit(ctx.methodCall())
        args = self.visit(ctx.list_expr()) if ctx.list_expr() is not None else []
        if isinstance(meth, ArrayCell):
            receiver = meth.arr
            return MethCall(receiver, "", args)
        elif isinstance(meth, FieldAccess):
            receiver = meth.receiver
            metName = meth.field
            return MethCall(receiver, metName, args)
        elif isinstance(meth, MethCall):
            receiver = meth.receiver
            metName = meth.funName
            return MethCall(receiver, metName, args)
          
        
    # Grammar: 
    # methodCall:
    #    methodCall ( L_BRACKET expr R_BRACKET | DOT validCall)
    #    | ID;
    def visitMethodCall(self, ctx: MiniGoParser.MethodCallContext):
        if ctx.getChildCount() == 1:
            return Id(ctx.ID().getText())
        else:
            left = self.visit(ctx.methodCall())
            if ctx.L_BRACKET():
                # Truy cập mảng: methodCall [ expr ]
                
                index = self.visit(ctx.expr())
                if isinstance(left, ArrayCell):
                    return ArrayCell(left.arr,left.idx + [index])
                else:
                    return ArrayCell(left, [index])
            elif ctx.DOT():
                # Truy cập thuộc tính: lhs . validCall
                field = self.visit(ctx.validCall())
                if isinstance(field, Id):
                    return FieldAccess(left, field.name)
                elif isinstance(field, FuncCall):
                    return MethCall(left, field.funName, field.args)
        
        
    
    # Grammar: validCall: functionCall_stmt | ID;
    def visitValidCall(self, ctx: MiniGoParser.ValidCallContext):
        if ctx.functionCall_stmt():
            return self.visit(ctx.functionCall_stmt())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        else:
            return None
    
    # Grammar: return_stmt: RETURN expr | RETURN;
    def visitReturn_stmt(self, ctx: MiniGoParser.Return_stmtContext):
        if ctx.expr():
            ret_expr = self.visit(ctx.expr())
        else:
            ret_expr = None
        return Return(ret_expr)
    
    # Grammar: 
    # lhs: ID | lhs L_BRACKET expr R_BRACKET | lhs DOT ID;
    def visitLhs(self, ctx: MiniGoParser.LhsContext):
        # Nếu chỉ là ID
        if ctx.getChildCount() == 1:
            return Id(ctx.ID().getText())
        # Nếu có cú pháp: lhs L_BRACKET expr R_BRACKET -> ArrayCell
        if ctx.L_BRACKET():
            # Gọi đệ quy để lấy phần lhs ban đầu
            left = self.visit(ctx.lhs())
            index = self.visit(ctx.expr())
            if isinstance(left, ArrayCell):
                return ArrayCell(left.arr,left.idx + [index])
            else:
                return ArrayCell(left, [index])
            
        # Nếu có cú pháp: lhs DOT ID -> FieldAccess
        if ctx.DOT():
            receiver = self.visit(ctx.lhs())
            field = ctx.ID().getText()
            return FieldAccess(receiver, field)
        return None
    
    # -------------------------------------------------
    
    # Grammar: list_expr: expr | expr COMMA list_expr;
    def visitList_expr(self, ctx: MiniGoParser.List_exprContext):
        # Thu thập tất cả các biểu thức trong danh sách
        if ctx.list_expr():
            left = self.visit(ctx.expr())
            right = self.visit(ctx.list_expr())
            return [left] + right
        else:
            return [self.visit(ctx.expr())]
    
    # Grammar: expr: expr OR expr1 | expr1;
    def visitExpr(self, ctx: MiniGoParser.ExprContext):
        if ctx.OR():
            # Nếu có OR, tạo BinaryOp với toán tử "||"
            left = self.visit(ctx.expr())
            right = self.visit(ctx.expr1())
            return BinaryOp("||", left, right)
        else:
            return self.visit(ctx.expr1())
    
    # Grammar: expr1: expr1 AND expr2 | expr2;
    def visitExpr1(self, ctx: MiniGoParser.Expr1Context):
        if ctx.AND():
            left = self.visit(ctx.expr1())
            right = self.visit(ctx.expr2())
            return BinaryOp("&&", left, right)
        else:
            return self.visit(ctx.expr2())
    
    # Grammar: expr2: expr2 (EQUAL | NOT_EQ | LESS | LESS_EQ | GREATER | GREATER_EQ) expr3 | expr3;
    def visitExpr2(self, ctx: MiniGoParser.Expr2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3())
        else:
            left = self.visit(ctx.expr2())
            op = ctx.getChild(1).getText()  # Lấy toán tử so sánh
            right = self.visit(ctx.expr3())
            return BinaryOp(op, left, right)
    
    # Grammar: expr3: expr3 (ADD | SUB) expr4 | expr4;
    def visitExpr3(self, ctx: MiniGoParser.Expr3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr4())
        else:
            left = self.visit(ctx.expr3())
            op = ctx.getChild(1).getText()  # Lấy "+" hoặc "-"
            right = self.visit(ctx.expr4())
            return BinaryOp(op, left, right)
    
    # Grammar: expr4: expr4 (MULT | DIV | MOD) expr5 | expr5;
    def visitExpr4(self, ctx: MiniGoParser.Expr4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr5())
        else:
            left = self.visit(ctx.expr4())
            op = ctx.getChild(1).getText()  # Lấy "*" hoặc "/" hoặc "%"
            right = self.visit(ctx.expr5())
            return BinaryOp(op, left, right)
    
    # Grammar: expr5: (NOT | SUB) expr5 | expr6;
    def visitExpr5(self, ctx: MiniGoParser.Expr5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr6())
        else:
            op = ctx.getChild(0).getText()  # Lấy "!" hoặc "-"
            body = self.visit(ctx.expr5())
            return UnaryOp(op, body)
    
    # Grammar: expr6: expr6 (L_BRACKET expr R_BRACKET | DOT validCall) | expr7;
    def visitExpr6(self, ctx: MiniGoParser.Expr6Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr7())
        else:
            left = self.visit(ctx.expr6())
            if ctx.L_BRACKET():
                # Truy cập mảng: lhs [ expr ]
                index = self.visit(ctx.expr())
                
                if isinstance(left, ArrayCell):
                    return ArrayCell(left.arr,left.idx + [index])
                else:
                    return ArrayCell(left, [index])
                    
            elif ctx.DOT():
                # Truy cập thuộc tính: lhs . validCall
                field = self.visit(ctx.validCall())
                if isinstance(field, Id):
                    return FieldAccess(left, field.name)
                elif isinstance(field, FuncCall):
                    return MethCall(left, field.funName, field.args)
                
               
                # elif isinstance(field, Struc):
            
    
    # Grammar: expr7:
    #    ID
    #    | literal
    #    | arraytype arraylit
    #    | ID struct
    #    | functionCall_stmt
    #    | methodCall_stmt
    #    | L_PAREN expr R_PAREN;
    def visitExpr7(self, ctx: MiniGoParser.Expr7Context):
        # Nếu chỉ là ID
        if ctx.ID() and ctx.getChildCount() == 1:
            return Id(ctx.ID().getText())
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.arraylit():
            # Giả sử rule: arraytype arraylit
            eleType = self.visit(ctx.arraytype())
            value = self.visit(ctx.arraylit())
            # Để đơn giản, để danh sách dimensions rỗng
            return ArrayLiteral(eleType.dimens, eleType.eleType, value)
        elif ctx.getChild(0).getText() == "(":
            # Biểu thức trong ngoặc
            return self.visit(ctx.expr())
        elif ctx.functionCall_stmt():
            return self.visit(ctx.functionCall_stmt())
        elif ctx.methodCall_stmt():
            return self.visit(ctx.methodCall_stmt())
        elif ctx.ID() and ctx.struct():
            # Xử lý: ID struct
            structName = ctx.ID().getText()
            elements = self.visit(ctx.struct())
            return StructLiteral(structName, elements)
        else:
            return self.visitChildren(ctx)
    
    # Grammar: literal: INT_LIT | FLOAT_LIT | STRING_LIT | BOOLEAN_LIT | NIL_LIT;
    def visitLiteral(self, ctx: MiniGoParser.LiteralContext):
        text = ctx.getText()
        if ctx.INT_LIT():
            return IntLiteral(int(text))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(text))
        elif ctx.STRING_LIT():
            # Loại bỏ dấu nháy đầu và cuối
            return StringLiteral(text[1:-1])
        elif ctx.BOOLEAN_LIT():
            return BooleanLiteral(text.lower() == "true")
        elif ctx.NIL_LIT():
            return NilLiteral()
        else:
            return None
    
    # Grammar: arraylit: L_BRACE list_arrayElement R_BRACE;
    def visitArraylit(self, ctx: MiniGoParser.ArraylitContext):
        # Trả về danh sách các phần tử mảng; có thể bọc trong node ArrayLiteral nếu cần
        return self.visit(ctx.list_arrayElement())
    
    # Grammar: list_arrayElement: list_arrayElement COMMA arrayElement | arrayElement;
    def visitList_arrayElement(self, ctx: MiniGoParser.List_arrayElementContext):
        if ctx.list_arrayElement():
            left = self.visit(ctx.list_arrayElement())
            right = self.visit(ctx.arrayElement())
            return left + [right]
        else:
            return [self.visit(ctx.arrayElement())]
    
    # Grammar: arrayElement: ID | literal | arraylit | ID struct;
    def visitArrayElement(self, ctx: MiniGoParser.ArrayElementContext):
        if ctx.struct():
            name = ctx.ID().getText()
            elements = self.visit(ctx.struct())
            return StructLiteral(name,elements)
        else:
            return self.visit(ctx.getChild(0))
    
    # Grammar: struct: L_BRACE list_struct_field? R_BRACE;
    def visitStruct(self, ctx: MiniGoParser.StructContext):
        if ctx.list_struct_field():
            return self.visit(ctx.list_struct_field())
        else:
            return []
    
    # Grammar: list_struct_field: list_struct_field COMMA fieldprime | fieldprime;
    def visitList_struct_field(self, ctx: MiniGoParser.List_struct_fieldContext):
        if ctx.list_struct_field():
            left = self.visit(ctx.list_struct_field())
            right = self.visit(ctx.fieldprime())
            return left + [right]
        else:
            return [self.visit(ctx.fieldprime())]
    
    # Grammar: fieldprime: ID COLON expr;
    def visitFieldprime(self, ctx: MiniGoParser.FieldprimeContext):
        fieldName = ctx.ID().getText()
        expr_node = self.visit(ctx.expr())
        return (fieldName, expr_node)
    
    # Grammar: getInt : GETINT L_PAREN R_PAREN ;
    def visitGetInt(self, ctx: MiniGoParser.GetIntContext):
        return FuncCall("getInt", [])
    
    # Grammar: putInt : PUTINT L_PAREN expr R_PAREN ;
    def visitPutInt(self, ctx: MiniGoParser.PutIntContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putInt", [arg])
    
    # Grammar: putIntLn: PUTINTLN L_PAREN expr R_PAREN ;
    def visitPutIntLn(self, ctx: MiniGoParser.PutIntLnContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putIntLn", [arg])
    
    # Grammar: getFloat : GETFLOAT L_PAREN R_PAREN ;
    def visitGetFloat(self, ctx: MiniGoParser.GetFloatContext):
        return FuncCall("getFloat", [])
    
    # Grammar: putFloat : PUTFLOAT L_PAREN expr R_PAREN ;
    def visitPutFloat(self, ctx: MiniGoParser.PutFloatContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putFloat", [arg])
    
    # Grammar: putFloatLn : PUTFLOATLN L_PAREN expr R_PAREN ;
    def visitPutFloatLn(self, ctx: MiniGoParser.PutFloatLnContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putFloatLn", [arg])
    
    # Grammar: getBool : GETBOOL L_PAREN R_PAREN ;
    def visitGetBool(self, ctx: MiniGoParser.GetBoolContext):
        return FuncCall("getBool", [])
    
    # Grammar: putBool : PUTBOOL L_PAREN expr R_PAREN ;
    def visitPutBool(self, ctx: MiniGoParser.PutBoolContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putBool", [arg])
    
    # Grammar: putBoolLn : PUTBOOLLN L_PAREN expr R_PAREN ;
    def visitPutBoolLn(self, ctx: MiniGoParser.PutBoolLnContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putBoolLn", [arg])
    
    # Grammar: getString : GETSTRING L_PAREN R_PAREN ;
    def visitGetString(self, ctx: MiniGoParser.GetStringContext):
        return FuncCall("getString", [])
    
    # Grammar: putString : PUTSTRING L_PAREN expr R_PAREN ;
    def visitPutString(self, ctx: MiniGoParser.PutStringContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putString", [arg])
    
    # Grammar: putStringLn: PUTSTRINGLN L_PAREN expr R_PAREN ;
    def visitPutStringLn(self, ctx: MiniGoParser.PutStringLnContext):
        arg = self.visit(ctx.expr())
        return FuncCall("putStringLn", [arg])
    
    # Grammar: putLn : PUTLN L_PAREN R_PAREN ;
    def visitPutLn(self, ctx: MiniGoParser.PutLnContext):
        return FuncCall("putLn", [])
    

    
