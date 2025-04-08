import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_redeclared(self):
        input = """
            const a = 1 ; var b = "abc"; var a int; """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_type_mismatch(self):
        input = """var a int = 1.2;"""
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.2))\n"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_identifier(self):
        input = Program([VarDecl("a",IntType(),Id("b"))])
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input,expect,402))
        
    def test_403(self):
        input = """func foo( x ,  b int,  x string) {};
            """
        expect = "Redeclared Parameter: x\n"
        self.assertTrue(TestChecker.test(input,expect,403))
    
    
    def test_404(self):
        input = """func main() {};
        var a = 1 ; const b = "abc"; const a = 2;
        """
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input,expect,404))
  
    def test_405(self): 
        input = """func A(){};
        func A() {};
        """
        expect = "Redeclared Function: A\n"
        self.assertTrue(TestChecker.test(input,expect,405))
    
    def test_406(self): 
        input = """type Person struct { name string ; age int ; };
        var A = 1 ; var b = "abc";
        type Person struct { name string ; age int ; };
        """
        expect = "Redeclared Type: Person\n"
        self.assertTrue(TestChecker.test(input,expect,406))
    
    def test_407(self): 
        input = """func main() {
            var a = 1 ; var b = "abc";
            const a = 2;
        }
        type Person struct { name string ; age int ; };
        """
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input,expect,407))
    
    def test_408(self):
        input = """type I interface { foo(a int, b int); foo1(); foo(); };
        type I interface { foo(); };
        """
        expect = "Redeclared Type: I\n"
        self.assertTrue(TestChecker.test(input,expect,408))
    
    def test_409(self):
        input = """ type Calculator interface {
                        Add(x, y int) int;
                        Subtract(a, b float, c int) float;
                        Reset();
                       Add()
                    };
        """
        expect = "Redeclared Prototype: Add\n"
        self.assertTrue(TestChecker.test(input,expect,409))
    
    def test_410(self):
        input = """type Person struct { x string ; x int ; };
        
        """
        expect = "Redeclared Field: x\n"
        self.assertTrue(TestChecker.test(input,expect,410))
    
    def test_411(self):
        input = """
        type Person struct { name string ; age int ; };
        type X struct { name string ; age int ; };
        
        func (p Person) foo(x int, a string) int { var aa = 1;};
        func (x Person) foo1(a int) int { var p = 1;};
        func (x X) foo1(a int) int { var p = 1;};
        func (x Person) foo1(a int) int { var p = 1;};
        
        """
        expect = "Redeclared Method: foo1\n"
        self.assertTrue(TestChecker.test(input,expect,411))
    
    def test_412(self):
        input = """
        func main() {
            var a = 1 ; var b = "abc";
            a := d;
        }
        """
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input,expect,412))
    
    def test_413(self):
        input = """
        func main() {
            var a = 1 ; var b = "abc";
            a := b;
        }
        """
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input,expect,413))
    
    def test_414(self):
        input = """
        func main() {
            var a = 1 ; var b = "abc";
            b := false;
            a := b;
        }
        """
        expect = "Type Mismatch: Assign(Id(b),BooleanLiteral(false))\n"
        self.assertTrue(TestChecker.test(input,expect,414))
    
    def test_415(self):
        input = """
        type foo struct { name string ; age int ; };
        func main() {
            var a = 1 ; var b = "abc";
            foo();
        }
        """
        expect = "Undeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input,expect,415))
    
    def test_416(self):
        input = """
        func foo() {};
        type phu struct { name phu2 ; age int ; };
        type A interface { foo(a int, b int); foo1();  };
        type Person struct { name phu ; age int ; };
        type phu2 struct { a int ; b string ; };
        func main() {
            var a int = 1 ; var b = "abc";
            var x Person;
            var name int = x.name.name.a.a;
        }
        """
        expect = "Type Mismatch: FieldAccess(FieldAccess(FieldAccess(FieldAccess(Id(x),name),name),a),a)\n"
        self.assertTrue(TestChecker.test(input,expect,416))
    
    def test_417(self):
        input = """
        func foo() {};
        type Person struct { name phu ; age int ; };
        type A interface { foo(a int, b int); foo1();  };
        func (x Person) foo(a int,  b string) int { var p = 1;};
        func main() {
            var a = 1 ; var b = "abc";
            var x Person;
          
           foo();
           x.foo1();
        }
        """
        expect = "Undeclared Method: foo1\n"
        self.assertTrue(TestChecker.test(input,expect,417))
    
    def test_418(self):
        input = """
            func foo() {};
            type phu struct { a string ; age int ; };
            type Person struct { name phu ; age int ; };
            type A interface { foo(a int, b int) int; foo1();  };
            func (x Person) foo(a int,  b string) int { var p = 1;};
            func main() {
                var a = 1 ; var b = "abc";
                var x Person;
                var y A;
                var z string = y.foo();
        }
        """
        expect = "Type Mismatch: VarDecl(z,StringType,MethodCall(Id(y),foo,[]))\n"
        self.assertTrue(TestChecker.test(input,expect,418))
        
    # Check lai thu tu 
    def test_419(self):
        input =  """
var A = 1;
type A struct {a int;}
        """
   
        expect = "Redeclared Variable: A\n"
        self.assertTrue(TestChecker.test(input,expect,419))
        
    def test_420(self):
        input = """
        func foo(b, c int){
            var a = true;
            if (a) {
                var a float = 1.02;
            } else {
                var a = 1.02;
            }
        }
        func main(){
            var a int = 1 ; var b = "abc";
            foo(a, b);
        }
        """ 
        expect = "Type Mismatch: FuncCall(foo,[Id(a),Id(b)])\n"
        self.assertTrue(TestChecker.test(input,expect,420))
    
    def test_421(self):
        input = """
            func foo(a string, b string) float {};
            type Person struct { name int ; age int ; };
            type A interface { foo(a int, b int) int; foo1();  };
            func (x Person) foo(a int,  b string) int { var p = 1;};
            func main() {
                var a = 1 ; var b = "abc";
                var x Person;
                var y A;
                var z int = x.foo("a", b);
        }
        """
        expect = "Type Mismatch: MethodCall(Id(x),foo,[StringLiteral(\"a\"),Id(b)])\n"
        self.assertTrue(TestChecker.test(input,expect,421))
    
    def test_422(self):
        input = """
func foo() {
    putFloat(1.0);
    putIntLn(1, 2);
}
        """
        expect = "Type Mismatch: FuncCall(putIntLn,[IntLiteral(1),IntLiteral(2)])\n"
        self.assertTrue(TestChecker.test(input,expect,422)) 

    def test_423(self):
        input = """
        func foo() {};
        type Person struct { name string ; age int ; };
        type A interface { foo(a int, b int) int; foo1();  };
        func (x Person) foo(a int,  b string) int { var p = 1;};
        func main() {
            const a = 1;
            var mat [2][2][1]float = [a][a][1]int{{1,2},{3,4}};
           
        }
        """
        expect = "Type Mismatch: VarDecl(mat,ArrayType(FloatType,[IntLiteral(2),IntLiteral(2),IntLiteral(1)]),ArrayLiteral([Id(a),Id(a),IntLiteral(1)],IntType,[[IntLiteral(1),IntLiteral(2)],[IntLiteral(3),IntLiteral(4)]]))\n"
        self.assertTrue(TestChecker.test(input,expect,423))
    
    def test_424(self):
        input = """
        func main() {
            var a [2][2][1]float = [2][2][1]int{{1,2},{3,4}};
            var p [2][2][2]float = a;
           
        }
        """
        expect = "Type Mismatch: VarDecl(p,ArrayType(FloatType,[IntLiteral(2),IntLiteral(2),IntLiteral(2)]),Id(a))\n"
        self.assertTrue(TestChecker.test(input,expect,424))
        
    def test_425(self):
        input = """
        func foo() {};
        type Person struct { name string ; age int ; };
        type A interface { foo(a int, b int) int; };
        func (x Person) foo(a int,  b int) int { var p = 1;};
        func main() {
            var a Person = Person{name: "John", age: 30};
            var p A = a;
            var q int = p;
        }
        """
        expect = "Type Mismatch: VarDecl(q,IntType,Id(p))\n"
        self.assertTrue(TestChecker.test(input,expect,425))
    
    def test_426(self):
        input = """
        type A struct {a [2]int;} 
        type B interface {foo() int;}

        func (v A) foo() int {return 1;}

        func foo(a A) {        // param la id chua check
            var b = A{a: [2]int{1, 2}};
            foo(b)
            const b = 1;
        }
        """
        expect = "Redeclared Constant: b\n"
        self.assertTrue(TestChecker.test(input,expect,426))
    
    def test_427(self):
        input = """
      
        func main() {
            var a = 1;
            if (a < 3) {
                var a = 1;
            } else if(a > 2) {
                var a = 2;
                var a int;
            }
            return a;
        }
        """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,427))
    
    def test_428(self):
        input = """
        type Person struct { name string ; age int ; };
        func (p Person) foo() int { return 1; }
        func foo1() int { return 2; }
        func main() {
            var v [1]string;
            var c float;
            var a = v[0] + 2;
            
        }
        """
        expect = "Type Mismatch: BinaryOp(ArrayCell(Id(v),[IntLiteral(0)]),+,IntLiteral(2))\n"
        self.assertTrue(TestChecker.test(input,expect,428))
    
    def test_429(self):
        input = """func main() { 
            var a = 1;
            var b = 2;
            if (a < b) { 
                putInt(1);
            } else if (a == b) { 
                putInt(0); 
            } else if (a > b) { 
                putInt(-1); 
            } else { 
                var a = "x" + "y";
                var b = a * true; 
            } 
        };"""
        expect = "Type Mismatch: BinaryOp(Id(a),*,BooleanLiteral(true))\n"
        self.assertTrue(TestChecker.test(input,expect,429))
    
    def test_430(self):
        input = """
        type A interface { foo(a int, b int) int;  };
        type Person struct { name string ; age int ; };
        func (x Person) foo(a int,  b int) int { var p = 1;};
        func foo(b int) A {
            
           foo(1)
           var a = 1;
           if (a < 3) {
               var a = 1;
           } else if(a > 2) {
               var a Person;
                return a;
           }
           return a
        };
        """
        expect = "Type Mismatch: Return(Id(a))\n"
        self.assertTrue(TestChecker.test(input,expect,430))
        
    def test_431(self):
        input = """

        func foo() {
    for 1 {
        return
    }
}
        """
        expect = "Type Mismatch: For(IntLiteral(1),Block([Return()]))\n"
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_432(self):
        input = """
        func foo () {
            const a = 1;
            for a < 1 {
                const a = 1;
                for a < 1 {
                    const a = 1;
                    const b = 1;
                }
                const b = 1;
                var a = 1;
            }
        }
        """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,432))   
    
    def test_433(self):
        input = """
        func main() {
            var mat [2][2][1]int = [2][2][1]int{{1,2},{3,4}};

            for index, value := range mat {
                if (value > 1) {
                    putInt(value);
                } else {
                    var a string = index;
                }
            }
        };
        """
        expect = "Type Mismatch: VarDecl(a,StringType,Id(index))\n"
        self.assertTrue(TestChecker.test(input,expect,433))
    
    def test_434(self):
        input = """
        func main() {
            var a = 1;
            var b = 2;
            if (a < b) { 
                putInt(1);
            } else if (a == b) { 
                putInt(0); 
            } else if (a > b) { 
                putInt(-1); 
            } else { 
                var a = "x" + "y";
                var b = a * true; 
            } 
        };
        """
        expect = "Type Mismatch: BinaryOp(Id(a),*,BooleanLiteral(true))\n"
        self.assertTrue(TestChecker.test(input,expect,434))
    
    def test_435(self):
        input = """
        type Person struct { a int ; b string ; };
        func main() {
            var b Person;
            var c [1]int;
            a := Person{a: 1, b: "abc"};
            b.a := 1;
            d := c[0];
            d := a.a
            b := c;
        };
        """
        expect = "Type Mismatch: Assign(Id(b),Id(c))\n"
        self.assertTrue(TestChecker.test(input,expect,435))
    
    def test_436(self):
        input = """
const a = 2;
func foo () {
    const a = 1;
    for var a = 1; a < 1; b += 2 {
        const b = 1;
    }
}
        """
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input,expect,436))
        
    def test_437(self): 
        input = """ func foo(a int, b string) float {}; func main() { var x = foo(1); }; """ 
        expect = "Type Mismatch: FuncCall(foo,[IntLiteral(1)])\n" 
        self.assertTrue(TestChecker.test(input, expect, 437))
        
    # Test 438: Gọi hàm với kiểu đối số không phù hợp.
    def test_438(self):
        input = """
            func foo(a int, b string) float {};
            func main() {
                var x = foo("hello", 2);
            }
        """
        expect = "Type Mismatch: FuncCall(foo,[StringLiteral(\"hello\"),IntLiteral(2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 438))

    # Test 439: Lệnh return trong hàm yêu cầu trả về kiểu int nhưng trả về chuỗi.
    def test_439(self):
        input = """
            func foo() int {
                return "abc";
            }
        """
        expect = "Type Mismatch: Return(StringLiteral(\"abc\"))\n"
        self.assertTrue(TestChecker.test(input, expect, 439))

    # Test 440: Lệnh return có biểu thức trong hàm kiểu void (trong MiniGo, hàm void không cho phép return có giá trị).
    def test_440(self):
        input = """
            func main() {
                return 1;
            }
        """
        expect = "Type Mismatch: Return(IntLiteral(1))\n"
        self.assertTrue(TestChecker.test(input, expect, 440))

    # Test 441: Dùng chỉ số không phải kiểu int khi truy cập mảng.
    def test_441(self):
        input = """
            func main() {
                var a [5]int;
                var x = a["1"];
            }
        """
        expect = "Type Mismatch: ArrayCell(Id(a),[StringLiteral(\"1\")])\n"
        self.assertTrue(TestChecker.test(input, expect, 441))

    # Test 442: Truy cập field trên giá trị không phải kiểu struct.
    def test_442(self):
        input = """
            func main() {
                var a int = 5;
                var x = a.name;
            }
        """
        expect = "Type Mismatch: FieldAccess(Id(a),name)\n"
        self.assertTrue(TestChecker.test(input, expect, 442))

    # Test 443: Truy cập field không tồn tại trong struct.
    def test_443(self):
        input = """
            type Person struct { name string; age int; };
            func main() {
                var p Person;
                var x = p.address;
            }
        """
        expect = "Undeclared Field: address\n"
        self.assertTrue(TestChecker.test(input, expect, 443))

    # Test 444: Gán giá trị cho biến kiểu interface với một struct mà không thực hiện đủ các method được yêu cầu.
    def test_444(self):
        input = """
            type Calculator interface { Add(a int, b int) int; };
            type MyCalculator struct { x int; };
            func (mc MyCalculator) Sub(a int, b int) int { return a - b; }
            func main() {
                var calc Calculator = MyCalculator{x: 10};
            }
        """
        expect = "Type Mismatch: VarDecl(calc,Id(Calculator),StructLiteral(MyCalculator,[(x,IntLiteral(10))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 444))

    # Test 445: Toán tử Unary "!" áp dụng cho kiểu không hợp lệ (int thay vì boolean).
    def test_445(self):
        input = """
            func main() {
                var a = !5;
            }
        """
        expect = "Type Mismatch: UnaryOp(!,IntLiteral(5))\n"
        self.assertTrue(TestChecker.test(input, expect, 445))

    # Test 446: Toán tử gán cộng hợp (+=) với kiểu không phù hợp.
    def test_446(self):
        input = """
            func main() {
                var a int = 1;
                a += "abc";
            }
        """
        expect = "Type Mismatch: BinaryOp(Id(a),+,StringLiteral(\"abc\"))\n"
        self.assertTrue(TestChecker.test(input, expect, 446))

    # Test 447: Vòng lặp for-each với biểu thức sau từ không phải kiểu mảng.
    def test_447(self):
        input = """
            func main() {
                var x int = 10;
                for i, v := range x {
                    putInt(1);
                }
            }
        """
        expect = "Type Mismatch: ForEach(Id(i),Id(v),Id(x),Block([FuncCall(putInt,[IntLiteral(1)])]))\n"
        self.assertTrue(TestChecker.test(input, expect, 447))

    # Test 448: Gọi method trên biến interface với kiểu đối số không phù hợp.
    def test_448(self):
        input = """
            type I interface { foo(a int) int; };
            type A struct { x int; };
            func (a A) foo(b int) int { return b; }
            func main() {
                var i I;
                i := A{x: 1};
                i.foo(1.2);
            }
        """
        expect = "Type Mismatch: MethodCall(Id(i),foo,[FloatLiteral(1.2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 448))

    # Test 449: Biểu thức nhị phân với toán tử "+" giữa int và boolean.
    def test_449(self):
        input = """
            func main() {
                var a int = 10;
                var b = a + true;
            }
        """
        expect = "Type Mismatch: BinaryOp(Id(a),+,BooleanLiteral(true))\n"
        self.assertTrue(TestChecker.test(input, expect, 449))

    # Test 450: Tái khai báo biến trong cùng một block (không cho phép redeclaration trong cùng phạm vi).
    def test_450(self):
        input = """
            func foo(a int) {
                
                    var x int = 5;
                    var x int = 6;
                
            }
        """
        expect = "Redeclared Variable: x\n"
        self.assertTrue(TestChecker.test(input, expect, 450))
        
        
        # Test 451: Sử dụng identifier chưa được khai báo (ở RHS của khai báo biến).
    def test_451(self):
        input = """
            func main() {
                var a = b;
            }
        """
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input, expect, 451))

    # Test 452: Sai số chiều của mảng khi khởi tạo (số phần tử trong literal khác với kích thước khai báo).
    def test_452(self):
        input = """
            func main() {
                var a [2]int = [3]int{1,2,3};
            }
        """
        expect = "Type Mismatch: VarDecl(a,ArrayType(IntType,[IntLiteral(2)]),ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 452))

    # Test 453: Toán tử nhân (*) áp dụng giữa float và string.
    def test_453(self):
        input = """
            func main() {
                var a = 2.5 * "test";
            }
        """
        expect = "Type Mismatch: BinaryOp(FloatLiteral(2.5),*,StringLiteral(\"test\"))\n"
        self.assertTrue(TestChecker.test(input, expect, 453))

    # Test 454: Toán tử Unary "-" áp dụng cho boolean.
    def test_454(self):
        input = """
            func main() {
                var a = -true;
            }
        """
        expect = "Type Mismatch: UnaryOp(-,BooleanLiteral(true))\n"
        self.assertTrue(TestChecker.test(input, expect, 454))

    # Test 455: Redeclared biến trong block nội bộ khi tên trùng với tham số (nằm cùng một scope).
    def test_455(self):
        input = """
            func main(x int) {
                
                    var x = 10;
                    var x = 20;
                
            }
        """
        expect = "Redeclared Variable: x\n"
        self.assertTrue(TestChecker.test(input, expect, 455))

    # Test 456: Sử dụng kiểu chưa được khai báo trong khai báo biến.
    def test_456(self):
        input = """
            func main() {
                var a MyInt = 5;
            }
        """
        expect = "Undeclared Identifier: MyInt\n"
        self.assertTrue(TestChecker.test(input, expect, 456))

    # Test 457: Toán tử && với toán hạng không phải boolean.
    def test_457(self):
        input = """
            func main() {
                var a = 5 && 10;
            }
        """
        expect = "Type Mismatch: BinaryOp(IntLiteral(5),&&,IntLiteral(10))\n"
        self.assertTrue(TestChecker.test(input, expect, 457))

    # Test 458: Truy cập field trên biến kiểu interface (không hỗ trợ field access).
    def test_458(self):
        input = """
            type I interface { foo() int; };
            func main() {
                var i I;
                var x = i.field;
            }
        """
        expect = "Type Mismatch: FieldAccess(Id(i),field)\n"
        self.assertTrue(TestChecker.test(input, expect, 458))

    # Test 459: Gán mảng với literal mảng mà kiểu phần tử không tương thích (string thay vì int).
    def test_459(self):
        input = """
            func main() {
                var a [2]int = [2]string{"one", "two"};
            }
        """
        expect = "Type Mismatch: VarDecl(a,ArrayType(IntType,[IntLiteral(2)]),ArrayLiteral([IntLiteral(2)],StringType,[StringLiteral(\"one\"),StringLiteral(\"two\")]))\n"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_460(self):
        input = """
            func foo(a [2]int) int { return 1; }
            func main() {
                var arr int;
                foo(arr);
            }
        """
        expect = "Type Mismatch: FuncCall(foo,[Id(arr)])\n"
        self.assertTrue(TestChecker.test(input, expect, 460))

    # Test 461: Gọi hàm có return type Void nhưng sử dụng trong biểu thức (không cho phép).
    def test_461(self):
        input = """
            func foo() {}
            func main() {
                var a = foo();
            }
        """
        expect = "Type Mismatch: FuncCall(foo,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 461))

    # Test 462: Sử dụng toán tử modulo (%) với một trong số toán hạng là float.
    def test_462(self):
        input = """
            func main() {
                var a = 5 % 2.0;
            }
        """
        expect = "Type Mismatch: BinaryOp(IntLiteral(5),%,FloatLiteral(2.0))\n"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_463(self):
        input = """
            func main() {
                var x string = 10;
            }
        """
        expect = "Type Mismatch: VarDecl(x,StringType,IntLiteral(10))\n"
        self.assertTrue(TestChecker.test(input, expect, 463))

    # Test 464: Gọi method trên biến không phải kiểu struct (sai receiver).
    def test_464(self):
        input = """
            type A struct { x int; };
            func (a A) foo() int { return a.x; }
            func main() {
                var b int = 10;
                b.foo();
            }
        """
        expect = "Type Mismatch: MethodCall(Id(b),foo,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 464))

    # Test 465: Sử dụng ArrayCell trên biến không phải kiểu mảng.
    def test_465(self):
        input = """
            func main() {
                var a int = 5;
                var b = a[0];
            }
        """
        expect = "Type Mismatch: ArrayCell(Id(a),[IntLiteral(0)])\n"
        self.assertTrue(TestChecker.test(input, expect, 465))

    # Test 466: Gọi method với số lượng đối số vượt quá định nghĩa.
    def test_466(self):
        input = """
            type A struct { x int; };
            func (a A) foo(b int) int { return b; }
            func main() {
                var a A;
                a.foo(1,2);
            }
        """
        expect = "Type Mismatch: MethodCall(Id(a),foo,[IntLiteral(1),IntLiteral(2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 466))

    # Test 467: Struct literal với field không tồn tại (dồn thêm field không khai báo).
    def test_467(self):
        input = """
            type Person struct { name string; age int; };
            func main() {
                var p Person = Person{name: "Alice", age: 30, address: "HCM"};
                p.address := "HN";
            }
        """
        expect = "Undeclared Field: address\n"
        self.assertTrue(TestChecker.test(input, expect, 467))

    # Test 468: Gọi method của interface mà method đó không tồn tại.
    def test_468(self):
        input = """
            type I interface { foo(a int) int; };
            func main() {
                var i I;
                i.foo2(1);
            }
        """
        expect = "Undeclared Method: foo2\n"
        self.assertTrue(TestChecker.test(input, expect, 468))

    # Test 469: Khai báo mảng với kích thước là identifier chưa được khai báo.
    def test_469(self):
        input = """
            func main() {
                var a [n]int;
            }
        """
        expect = "Undeclared Identifier: n\n"
        self.assertTrue(TestChecker.test(input, expect, 469))

    # Test 470: Gán literal struct của kiểu khác cho biến struct (incompatible struct types).
    def test_470(self):
        input = """
            type A struct { x int; };
            type B struct { x int; };
            func main() {
                var a A = B{x: 10};
            }
        """
        expect = "Type Mismatch: VarDecl(a,Id(A),StructLiteral(B,[(x,IntLiteral(10))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 470))
        
    def test_471(self):
        input = """
      
        func main() {
            var a = 1;
            if (3) {
                var a = 1;
            } else if(a > 2) {
                var a = 2;
                var a int;
            }
            return a;
        }
        """
        expect = "Type Mismatch: IntLiteral(3)\n"
        self.assertTrue(TestChecker.test(input,expect,471))
        
    def test_472(self):
        input = """
        type A struct { x int; };
        type B struct { x int; };
        func (a A) x(b int) int { return b; }
        func main() {
            var a = 1;
            if (3) {
                var a = 1;
            } else if(a > 2) {
                var a = 2;
                var a int;
            }
            return a;
        }
        """
        expect = "Redeclared Method: x\n"
        self.assertTrue(TestChecker.test(input,expect,472))
        
    def test_473(self):
        input = """
       
        func main() {
            var a = 1;
            var x = a + "ste"
        }
        """
        expect = "Type Mismatch: BinaryOp(Id(a),+,StringLiteral(\"ste\"))\n"
        self.assertTrue(TestChecker.test(input,expect,473))
        
        # Test 474: Gọi method với số lượng đối số không khớp định nghĩa.
    def test_474(self):
        input = """
            type A struct { x int; };
            func (a A) foo(c int, b int) int { return c + b; }
            func main(){
                var a A;
                a.foo(10);
            }
        """
        expect = "Type Mismatch: MethodCall(Id(a),foo,[IntLiteral(10)])\n"
        self.assertTrue(TestChecker.test(input, expect, 474))

    # Test 475: Gọi hàm với kiểu đối số không phù hợp.
    def test_475(self):
        input = """
            func foo(a int, b float) int { return a ; }
            func main(){
                foo(1.0, 2);
            }
        """
        expect = "Type Mismatch: FuncCall(foo,[FloatLiteral(1.0),IntLiteral(2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 475))

    # Test 476: Gán kết quả hàm (kiểu int) cho biến kiểu string.
    def test_476(self):
        input = """
            func foo() int { return 1; }
            func main() {
                var a string = foo();
            }
        """
        expect = "Type Mismatch: VarDecl(a,StringType,FuncCall(foo,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 476))

    # Test 477: Tái khai báo kiểu (type) với cùng tên.
    def test_477(self):
        input = """
            type Person struct { name string; };
            type Person struct { age int; };
            func main() {}
        """
        expect = "Redeclared Type: Person\n"
        self.assertTrue(TestChecker.test(input, expect, 477))

    # Test 478: Tái khai báo field trong struct.
    def test_478(self):
        input = """
            type Person struct { name string; name int; }
            func main() {}
        """
        expect = "Redeclared Field: name\n"
        self.assertTrue(TestChecker.test(input, expect, 478))

    # Test 479: Sử dụng identifier chưa được khai báo trong biểu thức số học.
    def test_479(self):
        input = """
            func main() {
                var a = b + 5;
            }
        """
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input, expect, 479))

    # Test 480: Sử dụng chỉ số mảng không phải kiểu int (float làm chỉ số).
    def test_480(self):
        input = """
            func main() {
                var arr [5]int;
                var x = arr[2.2];
            }
        """
        expect = "Type Mismatch: ArrayCell(Id(arr),[FloatLiteral(2.2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 480))

    # Test 481: Gán mảng 2 chiều cho biến mảng 1 chiều.
    def test_481(self):
        input = """
            func main(){
                var a [2]int;
                var b [2][1]int;
                a := b;
            }
        """
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 481))

    # Test 482: Toán tử "+" với string và int.
    def test_482(self):
        input = """
            func main(){
                var a = "Hello" + 123;
            }
        """
        expect = "Type Mismatch: BinaryOp(StringLiteral(\"Hello\"),+,IntLiteral(123))\n"
        self.assertTrue(TestChecker.test(input, expect, 482))

    # Test 483: Gọi hàm trả về void được sử dụng trong biểu thức số học.
    def test_483(self):
        input = """
            func foo(){ }
            func main(){
                var a = foo() + 1;
            }
        """
        expect = "Type Mismatch: FuncCall(foo,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 483))

    # Test 484: Truy cập field trên biến không phải kiểu struct.
    def test_484(self):
        input = """
            func main() {
                var a = 10;
                var b = a.name;
            }
        """
        expect = "Type Mismatch: FieldAccess(Id(a),name)\n"
        self.assertTrue(TestChecker.test(input, expect, 484))

    # Test 485: Gọi method không tồn tại trên kiểu struct.
    def test_485(self):
        input = """
            type A struct { x int; }
            func (a A) foo() int { return a.x; }
            func main() {
                var a A;
                a.bar();
            }
        """
        expect = "Undeclared Method: bar\n"
        self.assertTrue(TestChecker.test(input, expect, 485))

    # Test 486: Tái khai báo hàm (function) với cùng tên.
    def test_486(self):
        input = """
            func foo() int { return 1; }
            func foo() int { return 2; }
            func main(){}
        """
        expect = "Redeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 486))

    # Test 487: Gán giá trị float cho biến kiểu int.
    def test_487(self):
        input = """
            func main(){
                var a int = 1.0;
            }
        """
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.0))\n"
        self.assertTrue(TestChecker.test(input, expect, 487))

    # Test 488: Điều kiện trong lệnh if không phải kiểu boolean.
    def test_488(self):
        input = """
            func main(){
                if (5) {
                    putInt(1);
                }
            }
        """
        expect = "Type Mismatch: IntLiteral(5)\n"
        self.assertTrue(TestChecker.test(input, expect, 488))

    # Test 489: Điều kiện của vòng lặp for không phải kiểu boolean.
    def test_489(self):
        input = """
            func main(){
                for (1) {
                    putInt(1);
                }
            }
        """
        expect = "Type Mismatch: For(IntLiteral(1),Block([FuncCall(putInt,[IntLiteral(1)])]))\n"
        self.assertTrue(TestChecker.test(input, expect, 489))

    # Test 490: Tái khai báo biến trong block nội bộ với cùng tên với tham số.
    def test_490(self):
        input = """
            func main(x int) {
                
                    var x float;
                    var x int;
                
            }
        """
        expect = "Redeclared Variable: x\n"
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test_491(self):
        input = """
            func main(){
                var a = 1;
                a := 2;
                const a = 1;
            }
        """
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 491))

    # Test 492: Hàm không void có return rỗng.
    def test_492(self):
        input = """
            func foo() int {
                return;
            }
        """
        expect = "Type Mismatch: Return()\n"
        self.assertTrue(TestChecker.test(input, expect, 492))

    # Test 493: Hàm void có return kèm giá trị.
    def test_493(self):
        input = """
            func foo() {
                return 10;
            }
        """
        expect = "Type Mismatch: Return(IntLiteral(10))\n"
        self.assertTrue(TestChecker.test(input, expect, 493))

    # Test 494: Array literal có kích thước không khớp với kích thước khai báo (sử dụng constant).
    def test_494(self):
        input = """
            func main(){
                const n = 3;
                var a [n]int = [2]int{1,2};
            }
        """
        expect = "Type Mismatch: VarDecl(a,ArrayType(IntType,[Id(n)]),ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 494))

    # Test 495: Kích thước mảng được khai báo bằng literal không phải int.
    def test_495(self):
        input = """
            func main(){
                var a [1]A;
            }
        """
        expect = "Undeclared Identifier: A\n"
        self.assertTrue(TestChecker.test(input, expect, 495))

    # Test 496: Truy cập field và thực hiện phép toán với kiểu không tương thích.
    def test_496(self):
        input = """
            type Person struct { name string; age int; };
            func main(){
                var p = Person{name: "Bob", age: 25};
                var x = p.age + "1";
            }
        """
        expect = "Type Mismatch: BinaryOp(FieldAccess(Id(p),age),+,StringLiteral(\"1\"))\n"
        self.assertTrue(TestChecker.test(input, expect, 496))

    # Test 497: Sử dụng kiểu của tham số hàm mà chưa được khai báo.
    def test_497(self):
        input = """
            func foo(a string) int { return 1; }
            func main() { foo(1); }
        """
        expect = "Type Mismatch: FuncCall(foo,[IntLiteral(1)])\n"
        self.assertTrue(TestChecker.test(input, expect, 497))

    # Test 498: Cài đặt method trong struct không phù hợp với prototype của interface.
    def test_498(self):
        input = """
            type I interface { foo(a int) int; }
            type A struct { x int; }
            func (a A) foo(x int) float { return 1.0; }
            func main(){
                var i I = A{x:10};
            }
        """
        expect = "Type Mismatch: VarDecl(i,Id(I),StructLiteral(A,[(x,IntLiteral(10))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 498))

    # Test 499: Vòng lặp for-each sử dụng trên biến không phải kiểu mảng (sử dụng kiểu struct).
    def test_499(self):
        input = """
                type A struct { x int; }
            func main(){
                var a A;
                for i, v := range a {
                    putInt(1);
                }
            }
        """
        expect = "Type Mismatch: ForEach(Id(i),Id(v),Id(a),Block([FuncCall(putInt,[IntLiteral(1)])]))\n"
        self.assertTrue(TestChecker.test(input, expect, 499))

    # Test 500: Tái khai báo method trong cùng một struct.
    def test_500(self):
        input = """
            type A struct { x int; }
            func (a A) foo() int { return 1; }
            func (a A) foo() int { return 2; }
            func main(){}
        """
        expect = "Redeclared Method: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 500))