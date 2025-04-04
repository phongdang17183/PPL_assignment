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
        # input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),VarDecl("v",Id("S1"), None),ConstDecl("x",None,Id("v")),VarDecl("z",Id("S1"),Id("x")),VarDecl("k",Id("S2"),Id("x"))])
   
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
        type VO interface {foo() int;}

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