import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """func main() {};"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def test_more_complex_program(self):
        """More complex program"""
        input = """var x int ;"""
        expect = str(Program([VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
    def test_call_without_parameter(self):
        """More complex program"""
        input = """func main () {}; var x int ;"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([])),VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,302))
    
    def test_const_decl(self):
        """Test khai báo hằng số"""
        input = "const a = 10;"
        expect = str(Program([ConstDecl("a", None, IntLiteral(10))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 303))

    def test_struct_decl(self):
        """Test khai báo struct"""
        input = "type Person struct { name string ; age int ; };"
        expect = str(Program([StructType("Person", [("name", StringType()), ("age", IntType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 304))
        
    def test_func_decl_with_params(self):
        """Test khai báo hàm có tham số và kiểu trả về"""
        input = "func sum(a int, b int) int { return a + b; };"
        expect = str(Program([
            FuncDecl("sum", 
                     [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                     IntType(), 
                     Block([Return(BinaryOp("+", Id("a"), Id("b")))]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 305))
        
    def test_method_decl(self):
        """Test khai báo phương thức (method)"""
        input = "func (r R) foo() {};"
        expect = str(Program([MethodDecl("r", Id("R"), FuncDecl("foo", [], VoidType(), Block([])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 306))
        
    def test_interface_decl(self):
        """Test khai báo giao diện (interface)"""
        input = "type I interface { foo(); };"
        expect = str(Program([InterfaceType("I", [Prototype("foo", [], VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 307))
        
    def test_array_decl_with_init(self):
        """Test khai báo mảng"""
        input = "var arr [3][2][1]int;"
        expect = str(Program([
                            VarDecl(
                                "arr",
                                ArrayType([IntLiteral(3), IntLiteral(2), IntLiteral(1)],IntType()),
                                None
                            )
                        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 308))
        
    def test_augmented_assignment(self):
        """Test phép gán cộng dồn trong thân hàm"""
        input = "func main() { x += 5; };"
        expect = str(Program([FuncDecl("main", [], VoidType(), 
                                       Block([Assign(Id("x"), BinaryOp( "+",Id("x"), IntLiteral(5)))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 309))
        
    def test_if_else_stmt(self):
        """Test cấu trúc if - else trong thân hàm"""
        input = "func main() { if (x < 10) { putInt(x); } else { putInt(0); }; };"
        expect = str(Program([FuncDecl("main", [], VoidType(), 
                                       Block([If(BinaryOp( "<", Id("x"), IntLiteral(10)), 
                                                  Block([FuncCall("putInt", [Id("x")])]), 
                                                  Block([FuncCall("putInt", [IntLiteral(0)])]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 310))
        
    def test_for_step_loop(self):
        """Test vòng lặp for dạng step trong hàm main"""
        input = "func main() { for x := 0; x < 10; x := x + 1 { putInt(x); }; };"
        expect = str(Program([FuncDecl("main", [], VoidType(), 
                                       Block([ForStep(Assign(Id("x"), IntLiteral(0)),
                                                      BinaryOp("<", Id("x"),  IntLiteral(10)),
                                                      Assign(Id("x"), BinaryOp( "+", Id("x"), IntLiteral(1))),
                                                      Block([FuncCall("putInt", [Id("x")])]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 311))
        
    def test_for_basic_loop(self):
        """Test vòng lặp for cơ bản (ForBasic)"""
        input = "func main() { for x < 10 { putInt(x); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                     Block([
                         ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
                                  Block([FuncCall("putInt", [Id("x")])]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 312))
        
    def test_constdecl(self):
        input = "const a = 1;"
        expect = str(Program([ConstDecl("a", None, IntLiteral(1))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 313))
        
    def test_funccall(self):
        input = "const a = foo(1);"
        expect = str(Program([ConstDecl("a",None,FuncCall("foo",[IntLiteral(1)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 314))
        
    def test315(self):
        input = """const a = foo( a[2][3] ); """
        expect = str(Program([ConstDecl("a",None,FuncCall("foo",[ArrayCell(Id("a"),[IntLiteral(2),IntLiteral(3)])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 315))
        
    def test316(self):
        input = """
            type A interface {
                Add(x, y int) int;
            }
"""
        expect = str(Program([
                            InterfaceType(
                                "A",
                                [
                                    Prototype(
                                        "Add",
                                        [
                                            IntType(),
                                            IntType()
                                        ],
                                        IntType()
                                    )
                                ]
                            )
                        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 316))
        
    def test_nested_if_stmt(self):
        """Test cấu trúc if - else if - else lồng nhau"""
        input = "func main() { if (x == 0) { putInt(0); } else if (x < 0) { putInt(-1); } else { putInt(1); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                     Block([
                         If(BinaryOp("==", Id("x"), IntLiteral(0)),
                            Block([FuncCall("putInt", [IntLiteral(0)])]),
                            If(BinaryOp("<", Id("x"), IntLiteral(0)),
                               Block([FuncCall("putInt", [UnaryOp("-", IntLiteral(1))])]),
                               Block([FuncCall("putInt", [IntLiteral(1)])])
                            )
                         )
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 317))
        
    def test_unary_expression(self):
        """Test biểu thức đơn thuần với toán tử đơn (UnaryOp)"""
        input = "func main() { putInt(-x); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                     Block([FuncCall("putInt", [UnaryOp("-", Id("x"))])]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))
        
    def test_for_each_loop(self):
        """Test vòng lặp for-each"""
        input = "func main() { for _, v := range arr { putInt(v); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         ForEach(Id("_"), Id("v"), Id("arr"),
                                 Block([FuncCall("putInt", [Id("v")])]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 319))
        
    def test_method_call(self):
        """Test method call"""
        input = "func main() { p.foo(5); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         MethCall(Id("p"), "foo", [IntLiteral(5)])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))
        
    def test_field_access(self):
        """Test field access trong biểu thức"""
        input = "func main() { putInt(x.y); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         FuncCall("putInt", [FieldAccess(Id("x"), "y")])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))
        
    def test_array_literal_with_init(self):
        """Test khai báo mảng với khởi tạo bằng array literal"""
        input = "func main() { var a [3]int = [3]int{1,2,3}; putInt(a[0]); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         VarDecl("a", 
                                 ArrayType([IntLiteral(3)], IntType()),
                                 ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])),
                         FuncCall("putInt", [ArrayCell(Id("a"), [IntLiteral(0)])])
                     ]))
        ]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 322))
        
    def test_struct_literal(self):
        """Test khai báo struct literal"""
        input = "func main() { var p Person = Person{ name:\"John\", age:30 }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         VarDecl("p",
                                 Id("Person"),
                                 StructLiteral("Person", [("name", StringLiteral("John")), ("age", IntLiteral(30))]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 323))
        
    def test_matrix_array_literal(self):
        """Test khai báo mảng 2 chiều với array literal lồng nhau và truy cập phần tử"""
        input = "func main() { var mat [2][2]int = [2][2]int{{1,2},{3,4}}; putInt(mat[1][0]); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                Block([
                    VarDecl("mat", 
                        ArrayType([IntLiteral(2), IntLiteral(2)], IntType()),
                        ArrayLiteral([IntLiteral(2), IntLiteral(2)], IntType(), [
                           [IntLiteral(1), IntLiteral(2)],
                           [IntLiteral(3), IntLiteral(4)]
                        ])
                    ),
                    FuncCall("putInt", [ArrayCell(Id("mat"), [IntLiteral(1), IntLiteral(0)])])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 324))
        
    def test_assignment_statement(self):
        """Test assignment statement sử dụng ':=' operator"""
        input = "func main() { x := 10; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                Block([
                    Assign(Id("x"), IntLiteral(10))
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 325))

    def test_binary_operation_precedence(self):
        """Test biểu thức nhị phân với đúng thứ tự ưu tiên"""
        input = "func main() { putInt(a + b * c - d); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                Block([
                    FuncCall("putInt", [
                        BinaryOp("-", BinaryOp("+", Id("a"), BinaryOp("*", Id("b"), Id("c"))), Id("d"))
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))
        
    def test_nested_function_call(self):
        """Test lời gọi hàm lồng nhau làm đối số của hàm khác"""
        input = "func main() { putInt(foo(bar(1))); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), 
                Block([
                    FuncCall("putInt", [
                        FuncCall("foo", [
                            FuncCall("bar", [IntLiteral(1)])
                        ])
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))
        
    def test_logical_unary_expression(self):
        """Test biểu thức với toán tử logic và đơn trong câu lệnh if"""
        input = "func main() { if (!a && b) { putInt(1); } else { putInt(0); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        BinaryOp("&&", UnaryOp("!", Id("a")), Id("b")),
                        Block([FuncCall("putInt", [IntLiteral(1)])]),
                        Block([FuncCall("putInt", [IntLiteral(0)])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))
        
    def test_break_statement(self):
        """Test break statement inside for loop"""
        input = "func main() { for x < 10 { break; }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
                                  Block([Break()]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 329))

    def test_continue_statement(self):
        """Test continue statement inside for loop"""
        input = "func main() { for x < 10 { continue; }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
                                  Block([Continue()]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))

    def test_if_without_else(self):
        """Test if statement without else branch"""
        input = "func main() { if (a > b) { putInt(a); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         If(BinaryOp(">", Id("a"), Id("b")),
                            Block([FuncCall("putInt", [Id("a")])]),
                            None)
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))

    def test_return_without_expr(self):
        """Test return statement with no expression"""
        input = "func main() { return; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([Return(None)]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 332))

    def test333(self):
        """Test chained method call"""
        input = """const VoTien = foo( [1]int{1}, [1][1]int{2} ); """
        expect = str(Program([ConstDecl("VoTien",None,FuncCall("foo",[ArrayLiteral([IntLiteral(1)],IntType(),[IntLiteral(1)]),ArrayLiteral([IntLiteral(1),IntLiteral(1)],IntType(),[IntLiteral(2)])]))]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 333))
        
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
        
    def test_11(self):
        """Test function call with array literals"""
        input = """const VoTien = foo( [1]int{1}, [1][1]int{2} ); """
        expect = str(Program([ConstDecl("VoTien", None, FuncCall("foo", [ArrayLiteral([IntLiteral(1)], IntType(), [IntLiteral(1)]), ArrayLiteral([IntLiteral(1), IntLiteral(1)], IntType(), [IntLiteral(2)])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 11))

    def test_12(self):
        """Test multiple variable declarations"""
        input = """
            var Votien = 1;
            var Votien int;
            var Votine int = 1;
"""
        expect = str(Program([VarDecl("Votien", None, IntLiteral(1)), VarDecl("Votien", IntType(), None), VarDecl("Votine", IntType(), IntLiteral(1))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 12))

    def test_13(self):
        """Test function declarations with and without parameters"""
        input = """
            func foo() int {return;}
            func foo(a int, b int) {return;}
"""
        expect = str(Program([FuncDecl("foo", [], IntType(), Block([Return(None)])), FuncDecl("foo", [ParamDecl("a", IntType()), ParamDecl("b", IntType())], VoidType(), Block([Return(None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 13))

    def test_14(self):
        """Test method declaration"""
        input = """
            func (Votien v) foo(Votien int) {return;}
"""
        expect = str(Program([MethodDecl("Votien", Id("v"), FuncDecl("foo", [ParamDecl("Votien", IntType())], VoidType(), Block([Return(None)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 14))

    def test_15(self):
        """Test struct type declaration with one field"""
        input = """
            type Votien struct {
                a int;
            }
"""
        expect = str(Program([StructType("Votien", [("a", IntType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 15))

    def test_16(self):
        """Test repeated struct type declaration with one field"""
        input = """
            type Votien struct {
                a int;
            }
"""
        expect = str(Program([StructType("Votien", [("a", IntType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 16))

    def test_17(self):
        """Test function with variable and constant declarations"""
        input = """
            func votien() {
                var a int;
                const a = nil;
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([VarDecl("a", IntType(), None), ConstDecl("a", None, NilLiteral())]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 17))

    def test_18(self):
        """Test function with assignment statement"""
        input = """
            func votien() {
                a += 1;
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1)))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 18))

    def test_19(self):
        """Test function with break and continue statements"""
        input = """
            func votien() {
                break;
                continue;
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([Break(), Continue()]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 19))

    def test_20(self):
        """Test function with function and method calls"""
        input = """
            func votien() {
                foo(1, 2);
                a[2].foo(1, 3);
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([FuncCall("foo", [IntLiteral(1), IntLiteral(2)]), MethCall(ArrayCell(Id("a"), [IntLiteral(2)]), "foo", [IntLiteral(1), IntLiteral(3)])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 20))
        
    def test_21(self):
        """Test function with simple if statement"""
        input = """
            func votien() {
                if(1) {return;}
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([If(IntLiteral(1), Block([Return(None)]), None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 21))

    def test_22(self):
        """Test function with if-else statement"""
        input = """
            func votien() {
                if(1) {
                    a := 1;
                } else {
                    a := 1;
                }
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([If(IntLiteral(1), Block([Assign(Id("a"), IntLiteral(1))]), Block([Assign(Id("a"), IntLiteral(1))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 22))

    def test_23(self):
        """Test function with nested if-else-if statements"""
        input = """
            func votien() {
                if(1) { return;
                } else if(1) {
                    a := 1;
                } else if(2) {
                    a := 1;
                }
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([If(IntLiteral(1), Block([Return(None)]), If(IntLiteral(1), Block([Assign(Id("a"), IntLiteral(1))]), If(IntLiteral(2), Block([Assign(Id("a"), IntLiteral(1))]), None)))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 23))

    def test_24(self):
        """Test function with basic and step for loops"""
        input = """
            func votien() {
                for i < 10 {return;}
                for var i = 0; i < 10; i += 1  {return;}
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([ForBasic(BinaryOp("<", Id("i"), IntLiteral(10)), Block([Return(None)])), ForStep(VarDecl("i", None, IntLiteral(0)), BinaryOp("<", Id("i"), IntLiteral(10)), Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))), Block([Return(None)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 24))

    def test_25(self):
        """Test function with for-each loop"""
        input = """
            func votien() {
                for index, value := range array[2] {return;}
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([ForEach(Id("index"), Id("value"), ArrayCell(Id("array"), [IntLiteral(2)]), Block([Return(None)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 25))

    def test_26(self):
        """Test constant with binary operations on booleans"""
        input = """
            const a = true + false - true;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("-", BinaryOp("+", BooleanLiteral(True), BooleanLiteral(False)), BooleanLiteral(True)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 26))

    def test_27(self):
        """Test constant with logical operations"""
        input = """
            const a = 1 && 2 || 3;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("||", BinaryOp("&&", IntLiteral(1), IntLiteral(2)), IntLiteral(3)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 27))

    def test_28(self):
        """Test constant with mixed arithmetic and logical operations"""
        input = """
            const a = 1 + 2 && 3;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("&&", BinaryOp("+", IntLiteral(1), IntLiteral(2)), IntLiteral(3)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 28))

    def test_29(self):
        """Test constant with subtraction and modulo"""
        input = """
            const a = 1 - 2 % 3;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("-", IntLiteral(1), BinaryOp("%", IntLiteral(2), IntLiteral(3))))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 29))

    def test_30(self):
        """Test constant with unary and binary operations"""
        input = """
            const a = 1 + -2 - 1;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("-", BinaryOp("+", IntLiteral(1), UnaryOp("-", IntLiteral(2))), IntLiteral(1)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 30))

    def test_31(self):
        """Test constant with array literal and struct"""
        input = """
            const a = [1]ID{Votien{}};
"""
        expect = str(Program([ConstDecl("a", None, ArrayLiteral([IntLiteral(1)], Id("ID"), [StructLiteral("Votien", [])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 31))

    def test_32(self):
        """Test constant with multi-dimensional float array literal"""
        input = """
            const a = [1][3]float{1.};
"""
        expect = str(Program([ConstDecl("a", None, ArrayLiteral([IntLiteral(1), IntLiteral(3)], FloatType(), [FloatLiteral(1.0)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 32))

    def test_33(self):
        """Test constant with struct literal and multiple fields"""
        input = """
            const a = ID{a: 1, b: true};
"""
        expect = str(Program([ConstDecl("a", None, StructLiteral("ID", [("a", IntLiteral(1)), ("b", BooleanLiteral(True))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 33))

    def test_34(self):
        """Test constant with struct literal containing array"""
        input = """
            const a = ID{a: [1]int{1}};
"""
        expect = str(Program([ConstDecl("a", None, StructLiteral("ID", [("a", ArrayLiteral([IntLiteral(1)], IntType(), [IntLiteral(1)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 34))

    def test_35(self):
        """Test constant with struct literal and single field"""
        input = """
            const a = ID{b: true};
"""
        expect = str(Program([ConstDecl("a", None, StructLiteral("ID", [("b", BooleanLiteral(True))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 35))

    def test_36(self):
        """Test constant with multiple logical AND operations"""
        input = """
            const a = 0 && 1 && 2;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("&&", BinaryOp("&&", IntLiteral(0), IntLiteral(1)), IntLiteral(2)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 36))

    def test_37(self):
        """Test constant with multiple logical OR operations"""
        input = """
            const a = 0 || 1 || 2;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("||", BinaryOp("||", IntLiteral(0), IntLiteral(1)), IntLiteral(2)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 37))

    def test_38(self):
        """Test constant with chained comparison operators"""
        input = """
            const a = 0 >= 1 <= 2;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("<=", BinaryOp(">=", IntLiteral(0), IntLiteral(1)), IntLiteral(2)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 38))

    def test_39(self):
        """Test constant with arithmetic operations"""
        input = """
            const a = 0 + 1 - 2;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("-", BinaryOp("+", IntLiteral(0), IntLiteral(1)), IntLiteral(2)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 39))

    def test_40(self):
        """Test constant with multiplication and division"""
        input = """
            const a = 0 * 1 / 2;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("/", BinaryOp("*", IntLiteral(0), IntLiteral(1)), IntLiteral(2)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 40))

    def test_41(self):
        """Test constant with nested unary operations"""
        input = """
            const a = !-!2;
"""
        expect = str(Program([ConstDecl("a", None, UnaryOp("!", UnaryOp("-", UnaryOp("!", IntLiteral(2)))))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 41))

    def test_42(self):
        """Test constant with complex expression"""
        input = """
            const a = 1 && 2 || 3 >= 4 + 5 * -6;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("||", BinaryOp("&&", IntLiteral(1), IntLiteral(2)), BinaryOp(">=", IntLiteral(3), BinaryOp("+", IntLiteral(4), BinaryOp("*", IntLiteral(5), UnaryOp("-", IntLiteral(6)))))))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 42))

    def test_43(self):
        """Test constant with multiple comparison operators"""
        input = """
            const a = 1 > 2 < 3 >= 4 <= 5 == 6;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("==", BinaryOp("<=", BinaryOp(">=", BinaryOp("<", BinaryOp(">", IntLiteral(1), IntLiteral(2)), IntLiteral(3)), IntLiteral(4)), IntLiteral(5)), IntLiteral(6)))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 43))

    def test_44(self):
        """Test constant with comparison and addition"""
        input = """
            const a = 1 >= 2 + 3;
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp(">=", IntLiteral(1), BinaryOp("+", IntLiteral(2), IntLiteral(3))))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 44))

    def test_45(self):
        """Test constant with multi-dimensional array access"""
        input = """
            const a = a[1][2][3][4];
"""
        expect = str(Program([ConstDecl("a", None, ArrayCell(Id("a"), [IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 45))

    def test_46(self):
        """Test constant with array access using expression"""
        input = """
            const a = a[1 + 2];
"""
        expect = str(Program([ConstDecl("a", None, ArrayCell(Id("a"), [BinaryOp("+", IntLiteral(1), IntLiteral(2))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 46))

    def test_47(self):
        """Test constant with nested field access"""
        input = """
            const a = a.b.c.d.e;
"""
        expect = str(Program([ConstDecl("a", None, FieldAccess(FieldAccess(FieldAccess(FieldAccess(Id("a"), "b"), "c"), "d"), "e"))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 47))

    def test_48(self):
        """Test constant with field access on struct literal"""
        input = """
            const a = ID {}.a;
"""
        expect = str(Program([ConstDecl("a", None, FieldAccess(StructLiteral("ID", []), "a"))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 48))

    def test_49(self):
        """Test constant with array access on struct field"""
        input = """
            const a = ID {}.a[2];
"""
        expect = str(Program([ConstDecl("a", None, ArrayCell(FieldAccess(StructLiteral("ID", []), "a"), [IntLiteral(2)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 49))

    def test_50(self):
        """Test constant with chained method calls"""
        input = """
            const a = a.b().c().d();
"""
        expect = str(Program([ConstDecl("a", None, MethCall(MethCall(MethCall(Id("a"), "b", []), "c", []), "d", []))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 50))
        
    def test_51(self):
        """Test constant with function call and method call"""
        input = """
            const a = a().d();
"""
        expect = str(Program([ConstDecl("a", None, MethCall(FuncCall("a", []), "d", []))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 51))

    def test_52(self):
        """Test constant with complex nested calls and access"""
        input = """
            const a = a[1].b.c()[2].d.e();
"""
        expect = str(Program([ConstDecl("a", None, MethCall(FieldAccess(ArrayCell(MethCall(FieldAccess(ArrayCell(Id("a"), [IntLiteral(1)]), "b"), "c", []), [IntLiteral(2)]), "d"), "e", []))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 52))

    def test_53(self):
        """Test constant with binary operation and parentheses"""
        input = """
            const a = a * (nil - "a");
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("*", Id("a"), BinaryOp("-", NilLiteral(), StringLiteral("a"))))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 53))

    def test_54(self):
        """Test constant with function calls and addition"""
        input = """
            const a = f() + f(1 + 2, 3.);
"""
        expect = str(Program([ConstDecl("a", None, BinaryOp("+", FuncCall("f", []), FuncCall("f", [BinaryOp("+", IntLiteral(1), IntLiteral(2)), FloatLiteral(3.0)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 54))

    def test_55(self):
        """Test constant with array access on function call"""
        input = """
            const a = foo()[2];
"""
        expect = str(Program([ConstDecl("a", None, ArrayCell(FuncCall("foo", []), [IntLiteral(2)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 55))

    def test_56(self):
        """Test constant with simple identifier"""
        input = """
            const a = a;
"""
        expect = str(Program([ConstDecl("a", None, Id("a"))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 56))

    def test_57(self):
        """Test variable declaration with custom type"""
        input = """
            var a Votien = 1.;
"""
        expect = str(Program([VarDecl("a", Id("Votien"), FloatLiteral(1.0))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 57))

    def test_58(self):
        """Test variable declaration with multi-dimensional array type"""
        input = """
            var a [2][3]int;
"""
        expect = str(Program([VarDecl("a", ArrayType([IntLiteral(2), IntLiteral(3)], IntType()), None)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 58))

    def test_59(self):
        """Test variable declaration with initialization"""
        input = """
            var a = 1;
"""
        expect = str(Program([VarDecl("a", None, IntLiteral(1))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 59))

    def test_60(self):
        """Test struct type declaration"""
        input = """
            type Votien struct {
                a int;
            }
"""
        expect = str(Program([StructType("Votien", [("a", IntType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 60))

    def test_61(self):
        """Test repeated struct type declaration"""
        input = """
            type Votien struct {
                a int;
            }
"""
        expect = str(Program([StructType("Votien", [("a", IntType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 61))

    def test_62(self):
        """Test struct type with multiple fields"""
        input = """
            type Votien struct {
                a  int;
                b  boolean;
            }
"""
        expect = str(Program([StructType("Votien", [("a", IntType()), ("b", BoolType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 62))

    def test_63(self):
        """Test struct type with array field"""
        input = """
            type Votien struct {
                a  int;
                b  boolean;
                c  [2]Votien;
            }
"""
        expect = str(Program([StructType("Votien", [("a", IntType()), ("b", BoolType()), ("c", ArrayType([IntLiteral(2)], Id("Votien")))], [])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 63))

    def test_64(self):
        """Test interface type with no-parameter method"""
        input = """
            type Votien interface {
                Add() ;
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [], VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 64))
        
    def test_65(self):
        """Test interface type with single-parameter method"""
        input = """
            type Votien interface {
                Add(a int) ;
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [IntType()], VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 65))
        
    def test_66(self):
        """Test interface type with two-parameter method"""
        input = """
            type Votien interface {
                Add(a int, b int) ;
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [IntType(), IntType()], VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 66))

    def test_67(self):
        """Test interface type with multiple parameters of same type"""
        input = """
            type Votien interface {
                Add(a, c int, b int) ;
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [IntType(), IntType(), IntType()], VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 67))

    def test_68(self):
        """Test interface type with array return type"""
        input = """
            type Votien interface {
                Add(a, c int, b int) [2]string;
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [IntType(), IntType(), IntType()], ArrayType([IntLiteral(2)], StringType()))])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 68))

    def test_69(self):
        """Test interface type with multiple method signatures"""
        input = """
            type Votien interface {
                Add() [2]string;
                Add() ID;
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [], ArrayType([IntLiteral(2)], StringType())), Prototype("Add", [], Id("ID"))])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 69))

    def test_70(self):
        """Test interface type with simple method"""
        input = """
            type Votien interface {
                Add();
            }
"""
        expect = str(Program([InterfaceType("Votien", [Prototype("Add", [], VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 70))
        
    def test_71(self):
        """Test simple function declaration"""
        input = """
            func foo() {return;}
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Return(None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 71))

    def test_72(self):
        """Test function with array parameter"""
        input = """
            func foo(a [2]ID) {return;}
"""
        expect = str(Program([FuncDecl("foo", [ParamDecl("a", ArrayType([IntLiteral(2)], Id("ID")))], VoidType(), Block([Return(None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 72))

    def test_73(self):
        """Test function with mixed parameter types"""
        input = """
            func foo(a int, b [1]int) {return;}
"""
        expect = str(Program([FuncDecl("foo", [ParamDecl("a", IntType()), ParamDecl("b", ArrayType([IntLiteral(1)], IntType()))], VoidType(), Block([Return(None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 73))

    def test_74(self):
        """Test function with array return type"""
        input = """
            func foo() [2]int {return;}
"""
        expect = str(Program([FuncDecl("foo", [], ArrayType([IntLiteral(2)], IntType()), Block([Return(None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 74))

    def test_75(self):
        """Test simple method declaration"""
        input = """
            func (Cat c) foo() {return;}
"""
        expect = str(Program([MethodDecl("Cat", Id("c"), FuncDecl("foo", [], VoidType(), Block([Return(None)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 75))

    def test_76(self):
        """Test method with array parameter"""
        input = """
            func (Cat c) foo(a [2]ID) {return;}
"""
        expect = str(Program([MethodDecl("Cat", Id("c"), FuncDecl("foo", [ParamDecl("a", ArrayType([IntLiteral(2)], Id("ID")))], VoidType(), Block([Return(None)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 76))

    def test_77(self):
        """Test method with mixed parameter types"""
        input = """
            func (Cat c) foo(a int, b [1]int) {return;}
"""
        expect = str(Program([MethodDecl("Cat", Id("c"), FuncDecl("foo", [ParamDecl("a", IntType()), ParamDecl("b", ArrayType([IntLiteral(1)], IntType()))], VoidType(), Block([Return(None)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 77))

    def test_78(self):
        """Test method with array return type"""
        input = """
            func (Cat c) foo() [2]int {return;}
"""
        expect = str(Program([MethodDecl("Cat", Id("c"), FuncDecl("foo", [], ArrayType([IntLiteral(2)], IntType()), Block([Return(None)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 78))

    def test_79(self):
        """Test mixed declarations"""
        input = """
            var a = 1;
            const b = 2;
            type a struct{a float;}
            type b interface {foo();}
            func foo(){return;}
            func (Cat c) foo() [2]int {return;}
"""
        expect = str(Program([VarDecl("a", None, IntLiteral(1)), ConstDecl("b", None, IntLiteral(2)), StructType("a", [("a", FloatType())], []), InterfaceType("b", [Prototype("foo", [], VoidType())]), FuncDecl("foo", [], VoidType(), Block([Return(None)])), MethodDecl("Cat", Id("c"), FuncDecl("foo", [], ArrayType([IntLiteral(2)], IntType()), Block([Return(None)])))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 79))

    def test_80(self):
        """Test function with multiple complex array parameters"""
        input = """
            func foo(a, b, c, d [ID][2][c] ID) {return;}
"""
        expect = str(Program([FuncDecl("foo", [ParamDecl("a", ArrayType([Id("ID"), IntLiteral(2), Id("c")], Id("ID"))), ParamDecl("b", ArrayType([Id("ID"), IntLiteral(2), Id("c")], Id("ID"))), ParamDecl("c", ArrayType([Id("ID"), IntLiteral(2), Id("c")], Id("ID"))), ParamDecl("d", ArrayType([Id("ID"), IntLiteral(2), Id("c")], Id("ID")))], VoidType(), Block([Return(None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 80))

    def test_81(self):
        """Test function with constant declaration"""
        input = """
            func foo(){
                const a = 1.;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([ConstDecl("a", None, FloatLiteral(1.0))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 81))

    def test_82(self):
        """Test function with variable declaration"""
        input = """
            func foo(){
                var a = 1.;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([VarDecl("a", None, FloatLiteral(1.0))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 82))

    def test_83(self):
        """Test function with array variable declaration"""
        input = """
            func foo(){
                var a [1]int = 1;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([VarDecl("a", ArrayType([IntLiteral(1)], IntType()), IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 83))

    def test_84(self):
        """Test function with uninitialized variable declaration"""
        input = """
            func foo(){
                var a int;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([VarDecl("a", IntType(), None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 84))

    def test_85(self):
        """Test function with multiple assignment operators"""
        input = """
            func foo(){
                a += 1;
                a -= 1;
                a *= 1;
                a /= 1;
                a %= 1;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))), Assign(Id("a"), BinaryOp("-", Id("a"), IntLiteral(1))), Assign(Id("a"), BinaryOp("*", Id("a"), IntLiteral(1))), Assign(Id("a"), BinaryOp("/", Id("a"), IntLiteral(1))), Assign(Id("a"), BinaryOp("%", Id("a"), IntLiteral(1)))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 85))

    def test_86(self):
        """Test function with array assignment using expression"""
        input = """
            func foo(){
                a[1 + 1] := 1;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Assign(ArrayCell(Id("a"), [BinaryOp("+", IntLiteral(1), IntLiteral(1))]), IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 86))

    def test_87(self):
        """Test function with nested array and field assignment"""
        input = """
            func foo(){
                a[2].b.c[2] := 1;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Assign(ArrayCell(FieldAccess(FieldAccess(ArrayCell(Id("a"), [IntLiteral(2)]), "b"), "c"), [IntLiteral(2)]), IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 87))

    def test_88(self):
        """Test function with multiple complex assignments"""
        input = """
            func foo(){
                a["s"][foo()] := a[2][2][3];
                a[2] := a[3][4];
                b.c.a[2] := b.c.a[2];
                b.c.a[2][3] := b.c.a[2][3];
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Assign(ArrayCell(Id("a"), [StringLiteral("s"), FuncCall("foo", [])]), ArrayCell(Id("a"), [IntLiteral(2), IntLiteral(2), IntLiteral(3)])), Assign(ArrayCell(Id("a"), [IntLiteral(2)]), ArrayCell(Id("a"), [IntLiteral(3), IntLiteral(4)])), Assign(ArrayCell(FieldAccess(FieldAccess(Id("b"), "c"), "a"), [IntLiteral(2)]), ArrayCell(FieldAccess(FieldAccess(Id("b"), "c"), "a"), [IntLiteral(2)])), Assign(ArrayCell(FieldAccess(FieldAccess(Id("b"), "c"), "a"), [IntLiteral(2), IntLiteral(3)]), ArrayCell(FieldAccess(FieldAccess(Id("b"), "c"), "a"), [IntLiteral(2), IntLiteral(3)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 88))

    def test_89(self):
        """Test function with field assignment"""
        input = """
            func foo(){
                a.b := 1;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Assign(FieldAccess(Id("a"), "b"), IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 89))

    def test_90(self):
        """Test function with nested field and array assignment"""
        input = """
            func foo(){
                a.b[2].c := 1;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Assign(FieldAccess(ArrayCell(FieldAccess(Id("a"), "b"), [IntLiteral(2)]), "c"), IntLiteral(1))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 90))

    def test_91(self):
        """Test function with break and continue"""
        input = """
            func foo(){
                break;
                continue;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Break(), Continue()]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 91))

    def test_92(self):
        """Test function with multiple return statements"""
        input = """
            func foo(){
                return;
                return foo() + 2;
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([Return(None), Return(BinaryOp("+", FuncCall("foo", []), IntLiteral(2)))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 92))

    def test_93(self):
        """Test function with various calls"""
        input = """
            func foo(){
                foo();
                foo(foo(), 2);
                a.foo();
                a[2].c.foo(foo(), 2);
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([FuncCall("foo", []), FuncCall("foo", [FuncCall("foo", []), IntLiteral(2)]), MethCall(Id("a"), "foo", []), MethCall(FieldAccess(ArrayCell(Id("a"), [IntLiteral(2)]), "c"), "foo", [FuncCall("foo", []), IntLiteral(2)])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 93))

    def test_94(self):
        """Test function with multiple if statements"""
        input = """
            func foo(){
                if(1) {return;}
                if(1 + 1) {
                    return 1;
                    return;
                }
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([If(IntLiteral(1), Block([Return(None)]), None), If(BinaryOp("+", IntLiteral(1), IntLiteral(1)), Block([Return(IntLiteral(1)), Return(None)]), None)]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 94))

    def test_95(self):
        """Test function with nested if-else statements"""
        input = """
            func foo(){
                if(1) { return;
                } else if(1) {
                    return 1;
                    return;
                } else {return;}
                if(1) {return;
                } else {
                    return 1;
                    return;
                }
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([If(IntLiteral(1), Block([Return(None)]), If(IntLiteral(1), Block([Return(IntLiteral(1)), Return(None)]), Block([Return(None)]))), If(IntLiteral(1), Block([Return(None)]), Block([Return(IntLiteral(1)), Return(None)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 95))

    def test_96(self):
        """Test function with multiple else-if branches"""
        input = """
            func foo(){
                if(1) {
                    return 1;
                } else if(2) {
                    return 2;
                } else if(3) {
                    return 3;
                } else if(4) {
                    return 4;
                }
            }
"""
        expect = str(Program([FuncDecl("foo", [], VoidType(), Block([If(IntLiteral(1), Block([Return(IntLiteral(1))]), If(IntLiteral(2), Block([Return(IntLiteral(2))]), If(IntLiteral(3), Block([Return(IntLiteral(3))]), If(IntLiteral(4), Block([Return(IntLiteral(4))]), None))))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 96))

    def test_97(self):
        """Test function with complex for loops"""
        input = """
            func votien() {
                for a.i[8] {
                    return;
                    return 1;
                }
                for i := 0; i[1] < 10; i *= 2 + 3  {
                    return;
                    return 1;
                }
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([ForBasic(ArrayCell(FieldAccess(Id("a"), "i"), [IntLiteral(8)]), Block([Return(None), Return(IntLiteral(1))])), ForStep(Assign(Id("i"), IntLiteral(0)), BinaryOp("<", ArrayCell(Id("i"), [IntLiteral(1)]), IntLiteral(10)), Assign(Id("i"), BinaryOp("*", Id("i"), BinaryOp("+", IntLiteral(2), IntLiteral(3)))), Block([Return(None), Return(IntLiteral(1))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 97))

    def test_98(self):
        """Test function with for-each loop and array literal"""
        input = """
            func votien() {
                for index, value := range [2]int{1, 2} {
                    return;
                    return 1;
                }
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([ForEach(Id("index"), Id("value"), ArrayLiteral([IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)]), Block([Return(None), Return(IntLiteral(1))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 98))

    def test_99(self):
        """Test function with nested method call"""
        input = """
            func votien() {
                a.b.c[2].d()
            }
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([MethCall(ArrayCell(FieldAccess(FieldAccess(Id("a"), "b"), "c"), [IntLiteral(2)]), "d", [])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 99))

    def test_100(self):
        """Test function with complex array literal return"""
        input = """
            func votien() {
                return [2] ID { {1}, {"2"}, {nil}, {struc{}} };
                return "THANKS YOU, PPL1 ";
            };
"""
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([Return(ArrayLiteral([IntLiteral(2)], Id("ID"), [[IntLiteral(1)], [StringLiteral("2")], [NilLiteral()], [StructLiteral("struc", [])]])), Return(StringLiteral("THANKS YOU, PPL1 "))]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 100))
        
    def test_101(self):
        """Test function with complex array literal return"""
        input = """
             func votien() {
                a.b()
            } 
            """
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([MethCall(Id("a"), "b", [])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 101))
        
    def test_102(self):
        
        input = """
             func votien() {
                a[1][2].a()
            } 
            """
        expect = str(Program([FuncDecl("votien", [], VoidType(), Block([MethCall(ArrayCell(Id("a"), [IntLiteral(1),IntLiteral(2)]), "a", [])]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 102))
        
    # def test_103(self):
        
    #     input = """
    #          func votien() {
    #             a().a()
    #         } 
    #         """
    #     expect = str(Program([FuncDecl("votien", [], VoidType(), Block([MethCall(FuncCall("a", []), "a", [])]))]))
    #     self.assertTrue(TestAST.checkASTGen(input, expect, 103))