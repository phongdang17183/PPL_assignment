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
                                 StructLiteral("Person", [("name", StringLiteral("\"John\"")), ("age", IntLiteral(30))]))
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

    def test_chained_method_call(self):
        """Test chained method call"""
        input = "func main() { p.foo().bar(1); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         MethCall(MethCall(Id("p"), "foo", []), "bar", [IntLiteral(1)])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 333))
    
    def test_arithmetic_expression_with_parentheses(self):
        """Test biểu thức số học với ngoặc"""
        input = "func main() { putInt((a+b)*c); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         FuncCall("putInt", [
                             BinaryOp("*", BinaryOp("+", Id("a"), Id("b")), Id("c"))
                         ])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 334))

    def test_function_call_multiple_args(self):
        """Test lời gọi hàm với nhiều đối số"""
        input = "func main() { foo(1,2,3); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         FuncCall("foo", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 335))

    def test_field_assignment(self):
        """Test gán giá trị cho trường (field assignment)"""
        input = "func main() { x.y := 10; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         Assign(FieldAccess(Id("x"), "y"), IntLiteral(10))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))

    def test_chained_field_access(self):
        """Test truy cập trường lồng nhau (chained field access)"""
        input = "func main() { putInt(a.b.c); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         FuncCall("putInt", [FieldAccess(FieldAccess(Id("a"), "b"), "c")])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))

    def test_function_with_parameter_no_body(self):
        """Test hàm với tham số nhưng thân hàm rỗng"""
        input = "func greet(name string) {};"
        expect = str(Program([
            FuncDecl("greet", [ParamDecl("name", StringType())], VoidType(), Block([]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 338))

    def test_method_decl_multiple_params(self):
        """Test khai báo phương thức với nhiều tham số và assignment trong thân"""
        input = "func (p Person) setAge(newAge int) { p.age := newAge; };"
        expect = str(Program([
            MethodDecl("p", Id("Person"),
                       FuncDecl("setAge", [ParamDecl("newAge", IntType())],
                                VoidType(),
                                Block([
                                    Assign(FieldAccess(Id("p"), "age"), Id("newAge"))
                                ])))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 339))

    def test_interface_multiple_prototypes(self):
        """Test khai báo giao diện với nhiều prototype phương thức"""
        input = """
            type I interface {
                foo();
                bar(x int) int;
            };
        """
        expect = str(Program([
            InterfaceType("I", [
                Prototype("foo", [], VoidType()),
                Prototype("bar", [IntType()], IntType())
            ])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))
        
    def test_nested_for_loop(self):
        """Test nested for loops (ForBasic lồng nhau)"""
        input = "func main() { for x < 10 { for y < 5 { putInt(y); }; }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    ForBasic(BinaryOp("<", Id("x"), IntLiteral(10)),
                        Block([
                            ForBasic(BinaryOp("<", Id("y"), IntLiteral(5)),
                                Block([FuncCall("putInt", [Id("y")])])
                            )
                        ])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 341))

    def test_return_expression(self):
        """Test return statement with a complex expression"""
        input = "func main() { return a + b * c; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Return(BinaryOp("+", Id("a"), BinaryOp("*", Id("b"), Id("c"))))
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 342))

    def test_chained_unary_operator(self):
        """Test chaining unary operators (e.g., !!a)"""
        input = "func main() { putInt(!!a); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    FuncCall("putInt", [UnaryOp("!", UnaryOp("!", Id("a")))])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))

    def test_function_call_in_expression(self):
        """Test function calls used within a binary expression"""
        input = "func main() { putInt(foo(1) + bar(2)); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    FuncCall("putInt", [
                        BinaryOp("+", FuncCall("foo", [IntLiteral(1)]), FuncCall("bar", [IntLiteral(2)]))
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))

    def test_method_call_with_array_access(self):
        """Test method call on an array element: a[0].foo()"""
        input = "func main() { a[0].foo(); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    MethCall(ArrayCell(Id("a"), [IntLiteral(0)]), "foo", [])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))

    def test_multiple_statements_in_block(self):
        """Test function body with multiple statements"""
        input = "func main() { x := 1; y := 2; putInt(x+y); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Assign(Id("x"), IntLiteral(1)),
                    Assign(Id("y"), IntLiteral(2)),
                    FuncCall("putInt", [BinaryOp("+", Id("x"), Id("y"))])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))

    def test_assignment_with_field_access(self):
        """Test assignment to a field: p.age := 30"""
        input = "func main() { p.age := 30; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Assign(FieldAccess(Id("p"), "age"), IntLiteral(30))
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))

    def test_binary_operation_mixed(self):
        """Test binary operation mixing different arithmetic operators"""
        input = "func main() { putInt((a - b) / c + d * e); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    FuncCall("putInt", [
                        BinaryOp("+", 
                            BinaryOp("/", BinaryOp("-", Id("a"), Id("b")), Id("c")),
                            BinaryOp("*", Id("d"), Id("e"))
                        )
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 348))

    def test_nested_method_call_chaining(self):
        """Test chained method calls: p.foo().bar().baz()"""
        input = "func main() { p.foo().bar().baz(); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    MethCall(MethCall(MethCall(Id("p"), "foo", []), "bar", []), "baz", [])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 349))

    def test_complex_if_nested(self):
        """Test if-else chain with multiple else-if branches"""
        input = "func main() { if (a < b) { putInt(1); } else if (a == b) { putInt(0); } else if (a > b) { putInt(-1); } else { putInt(2); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(BinaryOp("<", Id("a"), Id("b")),
                        Block([FuncCall("putInt", [IntLiteral(1)])]),
                        If(BinaryOp("==", Id("a"), Id("b")),
                           Block([FuncCall("putInt", [IntLiteral(0)])]),
                           If(BinaryOp(">", Id("a"), Id("b")),
                              Block([FuncCall("putInt", [UnaryOp("-", IntLiteral(1))])]),
                              Block([FuncCall("putInt", [IntLiteral(2)])])
                           )
                        )
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 350))
        
    def test_for_each_loop_with_underscore(self):
        """Test for-each loop với '_' làm index"""
        input = "func main() { for _, v := range arr { putInt(v); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         ForEach(Id("_"), Id("v"), Id("arr"),
                                 Block([FuncCall("putInt", [Id("v")])]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 351))

    def test_augmented_assignment_divide(self):
        """Test augmented assignment với '/=' operator"""
        input = "func main() { x /= 2; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         Assign(Id("x"), BinaryOp("/", Id("x"), IntLiteral(2)))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 352))

    def test_nested_unary_parentheses(self):
        """Test chaining unary operators: -(-x)"""
        input = "func main() { putInt(-(-x)); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         FuncCall("putInt", [UnaryOp("-", UnaryOp("-", Id("x")))])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 353))

    def test_multiple_function_calls(self):
        """Test gọi hàm liên tiếp trong cùng một block"""
        input = "func main() { foo(); bar(); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         FuncCall("foo", []),
                         FuncCall("bar", [])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 354))

    def test_method_call_on_array_access(self):
        """Test gọi method trên phần tử mảng: a[1].bar(3)"""
        input = "func main() { a[1].bar(3); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         MethCall(ArrayCell(Id("a"), [IntLiteral(1)]), "bar", [IntLiteral(3)])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 355))

    def test_complex_field_assignment(self):
        """Test assignment cho trường phức tạp: p.f[2].g := 100"""
        input = "func main() { p.f[2].g := 100; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         Assign(FieldAccess(ArrayCell(FieldAccess(Id("p"), "f"), [IntLiteral(2)]), "g"), IntLiteral(100))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))

    def test_var_decl_without_type(self):
        """Test khai báo biến không có kiểu tường minh nhưng có khởi tạo"""
        input = "func main() { var x = 5; putInt(x); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         VarDecl("x", None, IntLiteral(5)),
                         FuncCall("putInt", [Id("x")])
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 357))

    def test_const_decl_with_expression(self):
        """Test khai báo hằng số với biểu thức nhị phân"""
        input = "const pi = 3.14 + 0.00159;"
        expect = str(Program([
            ConstDecl("pi", None, BinaryOp("+", FloatLiteral(3.14), FloatLiteral(0.00159)))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 358))

    def test_method_decl_nonvoid_return(self):
        """Test khai báo phương thức với kiểu trả về không phải Void"""
        input = "func (r R) getVal() int { return 42; };"
        expect = str(Program([
            MethodDecl("r", Id("R"),
                       FuncDecl("getVal", [], IntType(),
                                Block([Return(IntLiteral(42))])))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))

    def test_nested_struct_literal(self):
        """Test struct literal lồng nhau trong khai báo biến"""
        input = "func main() { var s S = S{ a: 10, b: S{ a: 20, b: 0} }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                     Block([
                         VarDecl("s",
                                 Id("S"),
                                 StructLiteral("S", [
                                     ("a", IntLiteral(10)),
                                     ("b", StructLiteral("S", [
                                         ("a", IntLiteral(20)),
                                         ("b", IntLiteral(0))
                                     ]))
                                 ]))
                     ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 360))
        
    def test_recursive_function(self):
        """Test hàm đệ quy: tính giai thừa"""
        input = "func factorial(n int) int { if (n == 0) { return 1; } else { return n * factorial(n-1); }; };"
        expect = str(Program([
            FuncDecl("factorial", [ParamDecl("n", IntType())], IntType(),
                Block([
                    If(
                        BinaryOp("==", Id("n"), IntLiteral(0)),
                        Block([Return(IntLiteral(1))]),
                        Block([Return(BinaryOp("*", Id("n"), FuncCall("factorial", [BinaryOp("-", Id("n"), IntLiteral(1))])))])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 361))

    def test_compound_statements_in_function(self):
        """Test hàm với nhiều câu lệnh trong thân hàm"""
        input = "func main() { var a int = 10; putInt(a); putInt(20); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    VarDecl("a", IntType(), IntLiteral(10)),
                    FuncCall("putInt", [Id("a")]),
                    FuncCall("putInt", [IntLiteral(20)])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))

    def test_empty_function(self):
        """Test khai báo hàm không có câu lệnh trong thân hàm"""
        input = "func main() {};"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), Block([]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 363))

    def test_if_statement_without_else(self):
        """Test if statement không có nhánh else"""
        input = "func main() { if (x > 0) { putInt(x); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        BinaryOp(">", Id("x"), IntLiteral(0)),
                        Block([FuncCall("putInt", [Id("x")])]),
                        None
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 364))

    def test_for_basic_loop_without_assignment(self):
        """Test vòng lặp for cơ bản (ForBasic)"""
        input = "func main() { for (x < 5) { putInt(x); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    ForBasic(
                        BinaryOp("<", Id("x"), IntLiteral(5)),
                        Block([FuncCall("putInt", [Id("x")])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 365))

    def test_for_step_loop_variant(self):
        """Test vòng lặp for dạng step với tăng bước khác"""
        input = "func main() { for x := 0; x < 10; x := x + 2 { putInt(x); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    ForStep(
                        Assign(Id("x"), IntLiteral(0)),
                        BinaryOp("<", Id("x"), IntLiteral(10)),
                        Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral(2))),
                        Block([FuncCall("putInt", [Id("x")])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))

    def test_logical_expression_mixed(self):
        """Test biểu thức logic phức tạp với AND và OR"""
        input = "func main() { if ((a && b) || c) { putInt(1); } else { putInt(0); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        BinaryOp("||", BinaryOp("&&", Id("a"), Id("b")), Id("c")),
                        Block([FuncCall("putInt", [IntLiteral(1)])]),
                        Block([FuncCall("putInt", [IntLiteral(0)])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))

    def test_return_nil(self):
        """Test return statement với nil literal"""
        input = "func main() { return nil; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([Return(NilLiteral())])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))

    def test_unary_not_expression(self):
        """Test biểu thức với toán tử logic NOT"""
        input = "func main() { putInt(!flag); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([FuncCall("putInt", [UnaryOp("!", Id("flag"))])])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 369))

    def test_multiple_function_declarations(self):
        """Test khai báo nhiều hàm trong cùng một chương trình"""
        input = "func a() {}; func b() { putInt(2); };"
        expect = str(Program([
            FuncDecl("a", [], VoidType(), Block([])),
            FuncDecl("b", [], VoidType(), Block([FuncCall("putInt", [IntLiteral(2)])]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 370))

    def test_nested_if_without_else(self):
        """Test if statement lồng nhau mà không có nhánh else ở ngoài cùng"""
        input = "func main() { if (x < 0) { if (y < 0) { putInt(1); }; }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        BinaryOp("<", Id("x"), IntLiteral(0)),
                        Block([
                            If(
                                BinaryOp("<", Id("y"), IntLiteral(0)),
                                Block([FuncCall("putInt", [IntLiteral(1)])]),
                                None
                            )
                        ]),
                        None
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 371))

    def test_augmented_assignment_division(self):
        """Test augmented assignment với '/=' operator"""
        input = "func main() { x /= 2; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Assign(Id("x"), BinaryOp("/", Id("x"), IntLiteral(2)))
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 372))

    def test_function_parameter_array(self):
        """Test hàm với tham số là mảng"""
        input = "func foo(a [3]int) { putInt(a[0]); };"
        expect = str(Program([
            FuncDecl("foo", [ParamDecl("a", ArrayType([IntLiteral(3)], IntType()))], VoidType(),
                Block([
                    FuncCall("putInt", [ArrayCell(Id("a"), [IntLiteral(0)])])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 373))

    def test_struct_decl_with_array_field(self):
        """Test khai báo struct với một trường là mảng"""
        input = "type Matrix struct { data [3][3]int; };"
        expect = str(Program([
            StructType("Matrix", [("data", ArrayType([IntLiteral(3), IntLiteral(3)], IntType()))], [])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 374))

    def test_struct_literal_with_array_field(self):
        """Test struct literal với trường là mảng (chỉ chứa literal)"""
        input = "func main() { var m Matrix = Matrix{ data: [3][3]int{{1,2,3},{4,5,6},{7,8,9}} }; putInt(m.data[1][1]); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    VarDecl("m", Id("Matrix"),
                        StructLiteral("Matrix", [
                            ("data", ArrayLiteral( [IntLiteral(3), IntLiteral(3)], IntType(), [
                                [IntLiteral(1), IntLiteral(2), IntLiteral(3)],
                                [IntLiteral(4), IntLiteral(5), IntLiteral(6)],
                                [IntLiteral(7), IntLiteral(8), IntLiteral(9)]
                            ]))
                        ])
                    ),
                    FuncCall("putInt", [
                        ArrayCell(FieldAccess(Id("m"), "data"), [IntLiteral(1),IntLiteral(1)])
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 375))

    def test_const_decl_float(self):
        """Test khai báo hằng số với float literal"""
        input = "const pi = 3.1415;"
        expect = str(Program([
            ConstDecl("pi", None, FloatLiteral(3.1415))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 376))

    def test_const_decl_nil(self):
        """Test khai báo hằng số với nil literal"""
        input = "const nothing = nil;"
        expect = str(Program([
            ConstDecl("nothing", None, NilLiteral())
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 377))

    def test_simple_function_with_return(self):
        """Test hàm đơn giản có return"""
        input = "func main() { return 42; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), Block([Return(IntLiteral(42))]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 378))

    def test_if_else_with_unary(self):
        """Test if-else với biểu thức điều kiện chứa toán tử unary"""
        input = "func main() { if (!flag) { putInt(0); } else { putInt(1); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        UnaryOp("!", Id("flag")),
                        Block([FuncCall("putInt", [IntLiteral(0)])]),
                        Block([FuncCall("putInt", [IntLiteral(1)])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 379))

    def test_for_step_loop_simple(self):
        """Test vòng lặp for dạng step đơn giản"""
        input = "func main() { for x := 1; x < 5; x := x + 1 { putInt(x); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    ForStep(
                        Assign(Id("x"), IntLiteral(1)),
                        BinaryOp("<", Id("x"), IntLiteral(5)),
                        Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral(1))),
                        Block([FuncCall("putInt", [Id("x")])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 380))

    def test_break_continue_in_loop(self):
        """Test break và continue trong vòng lặp"""
        input = "func main() { for (i < 10) { if (i == 5) { break; } else { continue; }; }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    ForBasic(
                        BinaryOp("<", Id("i"), IntLiteral(10)),
                        Block([
                            If(
                                BinaryOp("==", Id("i"), IntLiteral(5)),
                                Block([Break()]),
                                Block([Continue()])
                            )
                        ])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 381))

    def test_function_call_within_expression(self):
        """Test lời gọi hàm nằm trong biểu thức nhị phân"""
        input = "func main() { putInt(foo(3) + 7); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    FuncCall("putInt", [
                        BinaryOp("+", FuncCall("foo", [IntLiteral(3)]), IntLiteral(7))
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 382))

    def test_method_decl_without_params(self):
        """Test khai báo phương thức không có tham số"""
        input = "func (p Person) printName() { putInt(p.name); };"
        expect = str(Program([
            MethodDecl("p", Id("Person"),
                FuncDecl("printName", [], VoidType(),
                    Block([FuncCall("putInt", [FieldAccess(Id("p"), "name")])])
                )
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 383))

    def test_interface_decl_single_prototype(self):
        """Test khai báo giao diện với một prototype"""
        input = "type I interface { foo(); };"
        expect = str(Program([
            InterfaceType("I", [Prototype("foo", [], VoidType())])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 384))

    def test_struct_literal_with_fields(self):
        """Test struct literal với các trường không phải mảng"""
        input = "func main() { var p Person = Person{ name: \"Alice\", age: 30 }; putInt(p.age); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    VarDecl("p", Id("Person"),
                        StructLiteral("Person", [
                            ("name", StringLiteral("\"Alice\"")),
                            ("age", IntLiteral(30))
                        ])
                    ),
                    FuncCall("putInt", [FieldAccess(Id("p"), "age")])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 385))


    def test_function_multiple_parameters_and_arithmetic(self):
        """Test hàm với nhiều tham số và biểu thức số học phức tạp"""
        input = "func add(a int, b int, c int) int { return a + b * c - (a - c); };"
        expect = str(Program([
            FuncDecl("add", [ParamDecl("a", IntType()), ParamDecl("b", IntType()), ParamDecl("c", IntType())], IntType(),
                Block([
                    Return(BinaryOp("-",
                        BinaryOp("+", Id("a"), BinaryOp("*", Id("b"), Id("c"))),
                        BinaryOp("-", Id("a"), Id("c"))
                    ))
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 386))

    def test_augmented_assignment_multiply(self):
        """Test augmented assignment với '*=' operator"""
        input = "func main() { x *= 3; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Assign(Id("x"), BinaryOp("*", Id("x"), IntLiteral(3)))
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))

    def test_complex_binary_expression_with_parentheses(self):
        """Test biểu thức nhị phân phức tạp với ngoặc"""
        input = "func main() { putInt((a - b) * (c + d)); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    FuncCall("putInt", [
                        BinaryOp("*",
                            BinaryOp("-", Id("a"), Id("b")),
                            BinaryOp("+", Id("c"), Id("d"))
                        )
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 388))

    def test_function_call_nested_argument(self):
        """Test lời gọi hàm với đối số là lời gọi hàm lồng nhau"""
        input = "func main() { putInt(foo(bar(2))); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    FuncCall("putInt", [
                        FuncCall("foo", [FuncCall("bar", [IntLiteral(2)])])
                    ])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 389))

    def test_method_call_chained_with_field_receiver(self):
        """Test method call với receiver là field access"""
        input = "func main() { p.address.getCity(); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    MethCall(FieldAccess(Id("p"), "address"), "getCity", [])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 390))

    def test_if_statement_without_else_simple(self):
        """Test if statement không có nhánh else (điều kiện là phép so sánh)"""
        input = "func main() { if (x >= 10) { putInt(x); }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        BinaryOp(">=", Id("x"), IntLiteral(10)),
                        Block([FuncCall("putInt", [Id("x")])]),
                        None
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 391))

    def test_return_without_expression(self):
        """Test return statement không có biểu thức"""
        input = "func main() { return; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(), Block([Return(None)]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 392))

    def test_multiple_function_declarations(self):
        """Test khai báo nhiều hàm trong cùng một chương trình"""
        input = "func f() {}; func g() { return 5; };"
        expect = str(Program([
            FuncDecl("f", [], VoidType(), Block([])),
            FuncDecl("g", [], VoidType(), Block([Return(IntLiteral(5))]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 393))

    def test_method_decl_with_params_and_return_expression(self):
        """Test khai báo phương thức với tham số và biểu thức trả về phức tạp"""
        input = "func (p Person) compute(x int, y int) int { return p.value + x - y; };"
        expect = str(Program([
            MethodDecl("p", Id("Person"),
                FuncDecl("compute", [ParamDecl("x", IntType()), ParamDecl("y", IntType())], IntType(),
                    Block([
                        Return(BinaryOp("-", 
                            BinaryOp("+", FieldAccess(Id("p"), "value"), Id("x")),
                            Id("y")
                        ))
                    ])
                )
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 394))

    def test_interface_decl_multiple_prototypes(self):
        """Test khai báo giao diện với nhiều prototype"""
        input = "type I interface { foo(); bar(x int) int; baz() string; };"
        expect = str(Program([
            InterfaceType("I", [
                Prototype("foo", [], VoidType()),
                Prototype("bar", [IntType()], IntType()),
                Prototype("baz", [], StringType())
            ])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 395))

    def test_struct_decl_multiple_fields(self):
        """Test khai báo struct với nhiều trường khác nhau"""
        input = "type Person struct { name string; age int; salary float; };"
        expect = str(Program([
            StructType("Person", [
                ("name", StringType()),
                ("age", IntType()),
                ("salary", FloatType())
            ], [])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 396))

    def test_assignment_to_nested_field(self):
        """Test assignment cho trường lồng nhau: p.info.score := 99"""
        input = "func main() { p.info.score := 99; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Assign(
                        FieldAccess(FieldAccess(Id("p"), "info"), "score"),
                        IntLiteral(99)
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 397))

    def test_if_else_nested(self):
        """Test if-else lồng nhau với nhiều nhánh"""
        input = ("func main() { "
                 "if (a < b) { if (c < d) { putInt(1); } else { putInt(2); }; } "
                 "else { putInt(3); }; };")
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    If(
                        BinaryOp("<", Id("a"), Id("b")),
                        Block([
                            If(
                                BinaryOp("<", Id("c"), Id("d")),
                                Block([FuncCall("putInt", [IntLiteral(1)])]),
                                Block([FuncCall("putInt", [IntLiteral(2)])])
                            )
                        ]),
                        Block([FuncCall("putInt", [IntLiteral(3)])])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 398))
        
    def test_for_loop_with_if_inside(self):
        """Test vòng lặp for dạng step với if bên trong vòng lặp, sử dụng modulo"""
        input = "func main() { for x := 0; x < 10; x := x + 1 { if (x % 2 == 0) { putInt(x); }; }; };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    ForStep(
                        Assign(Id("x"), IntLiteral(0)),
                        BinaryOp("<", Id("x"), IntLiteral(10)),
                        Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral(1))),
                        Block([
                            If(
                                BinaryOp("==", BinaryOp("%", Id("x"), IntLiteral(2)), IntLiteral(0)),
                                Block([FuncCall("putInt", [Id("x")])]),
                                None
                            )
                        ])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 400))

    def test_assignment_with_method_call(self):
        """Test assignment với field access ở lhs và method call làm rhs"""
        input = "func main() { p.age := p.getAge(); };"
        expect = str(Program([
            FuncDecl("main", [], VoidType(),
                Block([
                    Assign(
                        FieldAccess(Id("p"), "age"),
                        MethCall(Id("p"), "getAge", [])
                    )
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 401))
