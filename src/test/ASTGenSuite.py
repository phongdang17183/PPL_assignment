import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
#     def test_simple_program(self):
#         """Simple program: int main() {} """
#         input = """func main() {};"""
#         expect = str(Program([FuncDecl("main",[],VoidType(),Block([]))]))
#         self.assertTrue(TestAST.checkASTGen(input,expect,300))

#     def test_more_complex_program(self):
#         """More complex program"""
#         input = """var x int ;"""
#         expect = str(Program([VarDecl("x",IntType(),None)]))
#         self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
#     def test_call_without_parameter(self):
#         """More complex program"""
#         input = """func main () {}; var x int ;"""
#         expect = str(Program([FuncDecl("main",[],VoidType(),Block([])),VarDecl("x",IntType(),None)]))
#         self.assertTrue(TestAST.checkASTGen(input,expect,302))
    
#     def test_const_decl(self):
#         """Test khai báo hằng số"""
#         input = "const a = 10;"
#         expect = str(Program([ConstDecl("a", None, IntLiteral(10))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 303))

#     def test_struct_decl(self):
#         """Test khai báo struct"""
#         input = "type Person struct { name string ; age int ; };"
#         expect = str(Program([StructType("Person", [("name", StringType()), ("age", IntType())], [])]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 304))
        
#     def test_func_decl_with_params(self):
#         """Test khai báo hàm có tham số và kiểu trả về"""
#         input = "func sum(a int, b int) int { return a + b; };"
#         expect = str(Program([
#             FuncDecl("sum", 
#                      [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
#                      IntType(), 
#                      Block([Return(BinaryOp("+", Id("a"), Id("b")))]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 305))
        
#     def test_method_decl(self):
#         """Test khai báo phương thức (method)"""
#         input = "func (r R) foo() {};"
#         expect = str(Program([MethodDecl("r", Id("R"), FuncDecl("foo", [], VoidType(), Block([])))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 306))
        
#     def test_interface_decl(self):
#         """Test khai báo giao diện (interface)"""
#         input = "type I interface { foo(); };"
#         expect = str(Program([InterfaceType("I", [Prototype("foo", [], VoidType())])]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 307))
        
#     def test_array_decl_with_init(self):
#         """Test khai báo mảng"""
#         input = "var arr [3][2][1]int;"
#         expect = str(Program([
#                             VarDecl(
#                                 "arr",
#                                 ArrayType([IntLiteral(3), IntLiteral(2), IntLiteral(1)],IntType()),
#                                 None
#                             )
#                         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 308))
        
#     def test_augmented_assignment(self):
#         """Test phép gán cộng dồn trong thân hàm"""
#         input = "func main() { x += 5; };"
#         expect = str(Program([FuncDecl("main", [], VoidType(), 
#                                        Block([Assign(Id("x"), BinaryOp( "+",Id("x"), IntLiteral(5)))]))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 309))
        
#     def test_if_else_stmt(self):
#         """Test cấu trúc if - else trong thân hàm"""
#         input = "func main() { if (x < 10) { putInt(x); } else { putInt(0); }; };"
#         expect = str(Program([FuncDecl("main", [], VoidType(), 
#                                        Block([If(BinaryOp( "<", Id("x"), IntLiteral(10)), 
#                                                   Block([FuncCall("putInt", [Id("x")])]), 
#                                                   Block([FuncCall("putInt", [IntLiteral(0)])]))]))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 310))
        
#     def test_for_step_loop(self):
#         """Test vòng lặp for dạng step trong hàm main"""
#         input = "func main() { for x := 0; x < 10; x := x + 1 { putInt(x); }; };"
#         expect = str(Program([FuncDecl("main", [], VoidType(), 
#                                        Block([ForStep(Assign(Id("x"), IntLiteral(0)),
#                                                       BinaryOp("<", Id("x"),  IntLiteral(10)),
#                                                       Assign(Id("x"), BinaryOp( "+", Id("x"), IntLiteral(1))),
#                                                       Block([FuncCall("putInt", [Id("x")])]))]))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 311))
        
#     def test_for_basic_loop(self):
#         """Test vòng lặp for cơ bản (ForBasic)"""
#         input = "func main() { for x < 10 { putInt(x); }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                      Block([
#                          ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
#                                   Block([FuncCall("putInt", [Id("x")])]))
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 312))
        
#     def test_constdecl(self):
#         input = "const a = 1;"
#         expect = str(Program([ConstDecl("a", None, IntLiteral(1))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 313))
        
#     def test_funccall(self):
#         input = "const a = foo(1);"
#         expect = str(Program([ConstDecl("a",None,FuncCall("foo",[IntLiteral(1)]))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 314))
        
#     def test315(self):
#         input = """const a = foo( a[2][3] ); """
#         expect = str(Program([ConstDecl("a",None,FuncCall("foo",[ArrayCell(ArrayCell(Id("a"),[IntLiteral(2)]),[IntLiteral(3)])]))]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 315))
        
#     def test316(self):
#         input = """
#             type A interface {
#                 Add(x, y int) int;
#             }
# """
#         expect = str(Program([
#                             InterfaceType(
#                                 "A",
#                                 [
#                                     Prototype(
#                                         "Add",
#                                         [
#                                             ParamDecl("x", IntType()),
#                                             ParamDecl("y", IntType())
#                                         ],
#                                         IntType()
#                                     )
#                                 ]
#                             )
#                         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 316))
        
#     def test_nested_if_stmt(self):
#         """Test cấu trúc if - else if - else lồng nhau"""
#         input = "func main() { if (x == 0) { putInt(0); } else if (x < 0) { putInt(-1); } else { putInt(1); }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                      Block([
#                          If(BinaryOp("==", Id("x"), IntLiteral(0)),
#                             Block([FuncCall("putInt", [IntLiteral(0)])]),
#                             If(BinaryOp("<", Id("x"), IntLiteral(0)),
#                                Block([FuncCall("putInt", [UnaryOp("-", IntLiteral(1))])]),
#                                Block([FuncCall("putInt", [IntLiteral(1)])])
#                             )
#                          )
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 317))
        
#     def test_unary_expression(self):
#         """Test biểu thức đơn thuần với toán tử đơn (UnaryOp)"""
#         input = "func main() { putInt(-x); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                      Block([FuncCall("putInt", [UnaryOp("-", Id("x"))])]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 318))
        
#     def test_for_each_loop(self):
#         """Test vòng lặp for-each"""
#         input = "func main() { for _, v := range arr { putInt(v); }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          ForEach(Id("_"), Id("v"), Id("arr"),
#                                  Block([FuncCall("putInt", [Id("v")])]))
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 319))
        
#     def test_method_call(self):
#         """Test method call"""
#         input = "func main() { p.foo(5); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          MethCall(Id("p"), "foo", [IntLiteral(5)])
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 320))
        
#     def test_field_access(self):
#         """Test field access trong biểu thức"""
#         input = "func main() { putInt(x.y); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          FuncCall("putInt", [FieldAccess(Id("x"), "y")])
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 321))
        
#     def test_array_literal_with_init(self):
#         """Test khai báo mảng với khởi tạo bằng array literal"""
#         input = "func main() { var a [3]int = [3]int{1,2,3}; putInt(a[0]); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("a", 
#                                  ArrayType([IntLiteral(3)], IntType()),
#                                  ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])),
#                          FuncCall("putInt", [ArrayCell(Id("a"), [IntLiteral(0)])])
#                      ]))
#         ]))

#         self.assertTrue(TestAST.checkASTGen(input, expect, 322))
        
#     def test_struct_literal(self):
#         """Test khai báo struct literal"""
#         input = "func main() { var p Person = Person{ name:\"John\", age:30 }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          VarDecl("p",
#                                  Id("Person"),
#                                  StructLiteral("Person", [("name", StringLiteral("John")), ("age", IntLiteral(30))]))
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 323))
        
#     def test_matrix_array_literal(self):
#         """Test khai báo mảng 2 chiều với array literal lồng nhau và truy cập phần tử"""
#         input = "func main() { var mat [2][2]int = [2][2]int{{1,2},{3,4}}; putInt(mat[1][0]); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                 Block([
#                     VarDecl("mat", 
#                         ArrayType([IntLiteral(2), IntLiteral(2)], IntType()),
#                         ArrayLiteral([IntLiteral(2), IntLiteral(2)], IntType(), [
#                            [IntLiteral(1), IntLiteral(2)],
#                            [IntLiteral(3), IntLiteral(4)]
#                         ])
#                     ),
#                     FuncCall("putInt", [ArrayCell(ArrayCell(Id("mat"), [IntLiteral(1)]), [IntLiteral(0)])])
#                 ])
#             )
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 324))
        
#     def test_assignment_statement(self):
#         """Test assignment statement sử dụng ':=' operator"""
#         input = "func main() { x := 10; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                 Block([
#                     Assign(Id("x"), IntLiteral(10))
#                 ])
#             )
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 325))

#     def test_binary_operation_precedence(self):
#         """Test biểu thức nhị phân với đúng thứ tự ưu tiên"""
#         input = "func main() { putInt(a + b * c - d); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                 Block([
#                     FuncCall("putInt", [
#                         BinaryOp("-", BinaryOp("+", Id("a"), BinaryOp("*", Id("b"), Id("c"))), Id("d"))
#                     ])
#                 ])
#             )
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 326))
        
#     def test_nested_function_call(self):
#         """Test lời gọi hàm lồng nhau làm đối số của hàm khác"""
#         input = "func main() { putInt(foo(bar(1))); };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(), 
#                 Block([
#                     FuncCall("putInt", [
#                         FuncCall("foo", [
#                             FuncCall("bar", [IntLiteral(1)])
#                         ])
#                     ])
#                 ])
#             )
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 327))
        
#     def test_logical_unary_expression(self):
#         """Test biểu thức với toán tử logic và đơn trong câu lệnh if"""
#         input = "func main() { if (!a && b) { putInt(1); } else { putInt(0); }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                 Block([
#                     If(
#                         BinaryOp("&&", UnaryOp("!", Id("a")), Id("b")),
#                         Block([FuncCall("putInt", [IntLiteral(1)])]),
#                         Block([FuncCall("putInt", [IntLiteral(0)])])
#                     )
#                 ])
#             )
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 328))
        
#     def test_break_statement(self):
#         """Test break statement inside for loop"""
#         input = "func main() { for x < 10 { break; }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
#                                   Block([Break()]))
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 329))

#     def test_continue_statement(self):
#         """Test continue statement inside for loop"""
#         input = "func main() { for x < 10 { continue; }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
#                                   Block([Continue()]))
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 330))

#     def test_if_without_else(self):
#         """Test if statement without else branch"""
#         input = "func main() { if (a > b) { putInt(a); }; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([
#                          If(BinaryOp(">", Id("a"), Id("b")),
#                             Block([FuncCall("putInt", [Id("a")])]),
#                             None)
#                      ]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 331))

#     def test_return_without_expr(self):
#         """Test return statement with no expression"""
#         input = "func main() { return; };"
#         expect = str(Program([
#             FuncDecl("main", [], VoidType(),
#                      Block([Return(None)]))
#         ]))
#         self.assertTrue(TestAST.checkASTGen(input, expect, 332))

    # def test333(self):
    #     """Test chained method call"""
    #     input = """const VoTien = foo( [1]int{1}, [1][1]int{2} ); """
    #     expect = str(Program([ConstDecl("VoTien",None,FuncCall("foo",[ArrayLiteral([IntLiteral(1)],IntType(),[IntLiteral(1)]),ArrayLiteral([IntLiteral(1),IntLiteral(1)],IntType(),[IntLiteral(2)])]))]))

    #     self.assertTrue(TestAST.checkASTGen(input, expect, 333))
        
    def test_1(self):
        """Test simple function call with integer argument"""
        input = """const VoTien = foo( 1 ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [IntLiteral(1)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 1))
        
    def test_2(self):
        """Test function call with multiple literal types"""
        input = """const VoTien = foo( 1.0, true, false, nil, "votien" ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [FloatLiteral(1.0), BooleanLiteral(True), BooleanLiteral(False), NilLiteral(), StringLiteral("votien")]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 2))

    def test_3(self):
        """Test function call with identifier argument"""
        input = """const VoTien = foo( id ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [Id("id")]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 3))

    def test_4(self):
        """Test function call with complex binary and unary expressions"""
        input = """const VoTien = foo( 1 + 2 - 3 && 5 - -1 ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [BinaryOp("&&", BinaryOp("-", BinaryOp("+", IntLiteral(1), IntLiteral(2)), IntLiteral(3)), BinaryOp("-", IntLiteral(5), UnaryOp("-", IntLiteral(1))))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 4))

    def test_5(self):
        """Test function call with chained comparison operators"""
        input = """const VoTien = foo( a > b <= c ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [BinaryOp("<=", BinaryOp(">", Id("a"), Id("b")), Id("c"))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 5))

    def test_6(self):
        """Test function call with multi-dimensional array access"""
        input = """const VoTien = foo( a[2][3] ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [ArrayCell(Id("a"), [IntLiteral(2), IntLiteral(3)])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 6))

    def test_7(self):
        """Test function call with nested field access"""
        input = """const VoTien = foo( a.b.c ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [FieldAccess(FieldAccess(Id("a"), "b"), "c")]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 7))

    def test_8(self):
        """Test function call with nested function and method calls"""
        input = """const VoTien = foo( a(), b.a(2, 3) ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [FuncCall("a", []), MethCall(Id("b"), "a", [IntLiteral(2), IntLiteral(3)])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 8))

    def test_9(self):
        """Test function call with binary operation and parentheses"""
        input = """const VoTien = foo( a * (1 + 2) ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [BinaryOp("*", Id("a"), BinaryOp("+", IntLiteral(1), IntLiteral(2)))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 9))

    def test_10(self):
        """Test function call with struct literals"""
        input = """const VoTien = foo( Votien {}, Votien {a: 1} ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [StructLiteral("Votien", []), StructLiteral("Votien", [("a", IntLiteral(1))])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 10))
        
    