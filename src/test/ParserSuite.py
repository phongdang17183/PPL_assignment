import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: void main() {} """
        input = """var arr [3]int = a;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))

    def test_more_complex_program(self):
        """More complex program"""
        input = """func foo () {x:=1;
        };"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))
    
    def test_wrong_miss_close(self):
        """Miss ) void main( {}"""
        input = """func main({};"""
        expect = "Error on line 1 col 11: {"
        self.assertTrue(TestParser.checkParser(input,expect,203))
    def test_wrong_variable(self):
        input = """var int;"""
        expect = "Error on line 1 col 5: int"
        self.assertTrue(TestParser.checkParser(input,expect,204))
    def test_wrong_index(self):
        input = """var i ;"""
        expect = "Error on line 1 col 7: ;"
        self.assertTrue(TestParser.checkParser(input,expect,205))
        
    def test206(self):
        input = """const x = [5][0]string{1, \"string\"};"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,206))
        
    def test207(self):
        input = """const i = [1.]ID{1, 3};"""
        expect = """Error on line 1 col 12: 1."""
        self.assertTrue(TestParser.checkParser(input,expect,207))
        
    def test208(self):
        input = """
                                    func Add() {
                                        2 - 2 += 2;       
                                    }
"""
        expect = """Error on line 3 col 41: 2"""
        self.assertTrue(TestParser.checkParser(input,expect,208))
        
    def test209(self):
        input = """
            type Point struct {
                x, y float;
                label string;
            }
            
            func move(p Point, dx float, dy float) {
                // Update coordinates
                p.x = p.x + dx;  /* Add dx */
                p.y = p.y + dy;  /* Add dy */
            }

            func main() {
                var p Point;
                p.x = 1;
                p.y = 2;
                move(p, 3.0, 4.0);
            }
            """
        expect = """Error on line 3 col 18: ,"""
        self.assertTrue(TestParser.checkParser(input,expect,209))
        
    def test210(self):
        input = """
            type Calculator interface {
                                        
                Add(x, y int) int;
                Subtract(a, b float, c int) [3]ID;
                Reset()
                                        
                SayHello(name string);
                                        
            }
            type abc interface {
                a123();
            }                                                                       
        """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input,expect,210))
        
    def test211(self):
        input = """
            type Point struct {
                y float;
                label string;
            }
            
            func move(p Point, dx float, dy float) {
                // Update coordinates
                p.x := p.x + dx  /* Add dx */
                p.y := p.y + dy;  /* Add dy */
            }

            func main() {
                var p Point;
                p.x := 1;
                p.y := 2;
                move(p, 3.0, 4.0);
            }
            """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input,expect,211))
        
    def test212(self):
        input = """
            type Calculator interface {
                Add(x, y int) int;
                Subtract(a, b float, c int) [3]ID;
                Reset()
                SayHello(name string);
            }
            type abc interface {
                a123();
            }                                                                       
        """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input,expect,212))
        
    def test213(self):
        input = """    
            var arr [][3]int = 2 + 3 / 4;
        """
        expect = """Error on line 2 col 22: ]"""
        self.assertTrue(TestParser.checkParser(input,expect,213))

    def test214(self):
        input = """
                                    func A() {
                                        if (x > 2) 
                                        {
                                            if (){}
                                        } 
                                    }"""
        expect = "Error on line 3 col 53: ;"
        self.assertTrue(TestParser.checkParser(input,expect,214))
    
    def test215(self):
        input = """
                                    func Add() {
                                        for var i [2]int = 0; foo().a.b();  {
                                            // loop body
                                        }
                                    }"""
        expect = "Error on line 3 col 77: {"
        self.assertTrue(TestParser.checkParser(input,expect,215))
        
    def test216(self):
        # 216. Chương trình đơn giản: khai báo biến
        input = "var a int;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 216))

    def test217(self):
        # 217. Khai báo hằng số hợp lệ
        input = "const a = 10;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 217))

    def test218(self):
        # 218. Hàm main đơn giản với return rỗng
        input = "func main() { return; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 218))

    def test219(self):
        # 219. Khai báo struct hợp lệ
        input = "type Point struct { x int; y int; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 219))

    def test220(self):
        # 220. Hàm chứa if statement không có else
        input = "func main() { if a < 10 { var a int; } ;};"
        expect = "Error on line 1 col 18: a"
        self.assertTrue(TestParser.checkParser(input, expect, 220))

    def test221(self):
        # 221. Hàm chứa if-else statement
        input = "func main() { if a < 10 { var a int; } else { var b int; }; };"
        expect = "Error on line 1 col 18: a"
        self.assertTrue(TestParser.checkParser(input, expect, 221))

    def test222(self):
        # 222. Hàm chứa for loop theo dạng: FOR expr L_BRACE list_stmt R_BRACE
        input = "func main() { for (a < 10) { var a int; } ;};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 222))

    def test223(self):
        # 223. Hàm chứa for loop với assignment (init, condition, post) 
        input = "func main() { for a:=0; a<10; a:=a+1 { var a int; }; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 223))

    def test224(self):
        # 224. For loop với vardecl ở phần khởi tạo
        input = "func main() { for var a int; a<10; a:=a+1 { }; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 224))

    def test225(self):
        # 225. For loop theo dạng: FOR ID COMMA ID DECLARE_ASSIGN RANGE ID L_BRACE list_stmt R_BRACE
        input = "func main() { for i,j:=range arr { var a int; }; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 225))

    def test226(self):
        # 226. For loop theo dạng: FOR '_' COMMA ID DECLARE_ASSIGN RANGE ID L_BRACE list_stmt R_BRACE
        input = "func main() { for _ ,i:=range arr { }; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 226))

    def test227(self):
        # 227. Hàm chứa break statement
        input = "func main() { break; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 227))

    def test228(self):
        # 228. Hàm chứa continue statement
        input = "func main() { continue; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 228))

    def test229(self):
        # 229. Hàm chứa function call statement
        input = "func main() { foo(); };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 229))

    def test230(self):
        # 230. Hàm chứa method call statement
        input = "func main() { obj.method(); };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 230))

    def test231(self):
        # 231. Hàm với return có biểu thức
        input = "func foo() { return a; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 231))

    def test232(self):
        # 232. Khai báo struct (lặp lại để kiểm tra)
        input = "type Point struct { x int; y int; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 232))

    def test233(self):
        # 233. Khai báo biến với gán (vardecl1)
        input = "var a int := 10;"
        expect = "Error on line 1 col 11: :="
        self.assertTrue(TestParser.checkParser(input, expect, 233))

    def test234(self):
        # 234. Khai báo mảng không khởi tạo
        input = "var arr [10]int;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 234))

    def test235(self):
        # 235. Khai báo hằng số với biểu thức
        input = "const a = 10+20;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 235))

    def test236(self):
        # 236. Hàm với tham số và kiểu trả về
        input = "func add(a int, b int) int { return a+b; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 236))

    def test237(self):
        # 237. Method declaration hợp lệ
        input = "func (Receiver Type) Method(param int) int { return param; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 237))

    def test238(self):
        # 238. Khai báo interface với nhiều method
        input = """\
    type I interface {
        Foo(a int);
        Bar();
    };"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 238))

    def test239(self):
        # 239. Hàm với assignment đơn giản
        input = "func main() { a:=10; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 239))

    def test240(self):
        # 240. Assignment với mảng (lhs là mảng)
        input = "func main() { arr[0]:=5; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 240))

    def test241(self):
        # 241. Assignment với member access (lhs là p.x)
        input = "func main() { p.x:=10; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 241))

    def test242(self):
        # 242. Hàm với return biểu thức số
        input = "func main() { return 42; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 242))

    def test243(self):
        # 243. Hàm với khai báo biến và assignment bên trong body
        input = "func main() { var x int; x:=x+1; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 243))

    def test244(self):
        # 244. Hàm với compound assignment (+=)
        input = "func main() { var a int; a+=5; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 244))

    def test245(self):
        # 245. Hàm với biểu thức phức tạp trong assignment
        input = "func main() { var a int; a:=b+c*d-e/f%g; };"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 245))

    def test246(self):
        # 246. Lỗi: Thiếu dấu chấm phẩy cuối khai báo biến
        input = "var a int"
        expect = "Error on line 1 col 10: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 246))

    def test247(self):
        # 247. Lỗi: Thiếu dấu chấm phẩy cuối khai báo hằng số
        input = "const a = 10"
        expect = "Error on line 1 col 13: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test248(self):
        # 248. Lỗi: Hàm bị thiếu cặp dấu () sau tên hàm
        input = "func main { return; };"
        expect = "Error on line 1 col 11: {"
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test249(self):
        # 249. Lỗi: Hàm main chứa if statement không đóng đủ ngoặc
        input = "func main() { if a < 10 { var a int; }"
        expect = "Error on line 1 col 18: a"
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test250(self):
        # 250. Lỗi: For loop thiếu dấu chấm phẩy giữa phần khởi tạo và điều kiện
        input = "func main() { for a:=0 a<10; a:=a+1 { var a int; } };"
        expect = "Error on line 1 col 24: a"
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test251(self):
        # 251. Lỗi: Khai báo biến sai cú pháp (thừa kiểu)
        input = "var a int int;"
        expect = "Error on line 1 col 11: int"
        self.assertTrue(TestParser.checkParser(input, expect, 251))

    def test252(self):
        # 252. Lỗi: Khai báo hằng số thiếu biểu thức
        input = "const a = ;"
        expect = "Error on line 1 col 11: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 252))

    def test253(self):
        # 253. Lỗi: Khai báo struct thiếu dấu chấm phẩy giữa các trường
        input = "type Point struct { x int y int; };"
        expect = "Error on line 1 col 27: y"
        self.assertTrue(TestParser.checkParser(input, expect, 253))

    def test254(self):
        # 254. Lỗi: Khai báo mảng thiếu từ khóa ASSIGN khi khởi tạo literal
        input = "var arr [10]int {1,2,3};"
        expect = "Error on line 1 col 17: {"
        self.assertTrue(TestParser.checkParser(input, expect, 254))

    def test255(self):
        # 255. Lỗi: Hàm bị thiếu danh sách tham số (thiếu dấu ())
        input = "func main( { return; } );"
        expect = "Error on line 1 col 12: {"
        self.assertTrue(TestParser.checkParser(input, expect, 255))

    def test256(self):
        # 256. Lỗi: Method declaration sai định dạng receiver (thiếu ID thứ hai)
        input = "func (Receiver) Method(param int) int { return param; };"
        expect = "Error on line 1 col 15: )"
        self.assertTrue(TestParser.checkParser(input, expect, 256))

    def test257(self):
        # 257. Lỗi: Interface declaration bị thiếu dấu chấm phẩy sau method
        input = "type I interface { Foo(a int) }"
        expect = "Error on line 1 col 31: }"
        self.assertTrue(TestParser.checkParser(input, expect, 257))

    def test258(self):
        # 258. Lỗi: Trong hàm, assignment thiếu biểu thức bên phải
        input = "func main() { a := ; };"
        expect = "Error on line 1 col 20: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 258))

    def test259(self):
        # 259. Lỗi: Trong hàm, biểu thức không hoàn chỉnh
        input = "func main() { a + ; };"
        expect = "Error on line 1 col 17: +"
        self.assertTrue(TestParser.checkParser(input, expect, 259))

    def test260(self):
        # 260. Lỗi: Method call không có tên method (sau dấu chấm phải có ID)
        input = "func main() { obj.(); };"
        expect = "Error on line 1 col 19: ("
        self.assertTrue(TestParser.checkParser(input, expect, 260))

    def test261(self):
        # 261. Lỗi: Struct literal thiếu dấu phẩy giữa các trường
        input = "func main() { Point{ x: 10 y: 20 }; };"
        expect = "Error on line 1 col 20: {"
        self.assertTrue(TestParser.checkParser(input, expect, 261))

    def test262(self):
        # 262. Lỗi: Array literal có dấu phẩy thừa (trailing comma không hợp lệ)
        input = "func main() { {1,2,} };"
        expect = "Error on line 1 col 15: {"
        self.assertTrue(TestParser.checkParser(input, expect, 262))

    def test263(self):
        # 263. Lỗi: Function call có tham số sai (dấu phẩy đứng trước đối số)
        input = "func main() { foo(,); };"
        expect = "Error on line 1 col 19: ,"
        self.assertTrue(TestParser.checkParser(input, expect, 263))

    def test264(self):
        # 264. Lỗi: Sử dụng từ khóa dự trữ làm tên biến
        input = "func main() { var if int; };"
        expect = "Error on line 1 col 19: if"
        self.assertTrue(TestParser.checkParser(input, expect, 264))

    def test265(self):
        # 265. Lỗi: Extra token sau chương trình
        input = "var a int; var b int; extra"
        expect = "Error on line 1 col 23: extra"
        self.assertTrue(TestParser.checkParser(input, expect, 265))
        
    def test266(self):
        # 266. 
        input = """
            func (p Person) Greet() string {
                if (1) {return;}
                else if (1) {}
            };  
            """
        expect = "Error on line 4 col 17: else"
        self.assertTrue(TestParser.checkParser(input, expect, 266))
        
    def test267(self):
        input = """    
            type Calculator struct {
                a int = 2;       
            }
        """
        expect = "Error on line 3 col 23: ="
        self.assertTrue(TestParser.checkParser(input, expect, 267))
        
    def test268(self):
        input ="""    
            type A interface {B()}
"""
        expect = "Error on line 2 col 34: }"
        self.assertTrue(TestParser.checkParser(input, expect, 268))
        
    def test269(self):
        input = """
            func (c int) Add(x int) int {return ;}
"""
        expect = "Error on line 2 col 21: int"
        self.assertTrue(TestParser.checkParser(input, expect, 269))
        
    def test270(self):
        input = """

"""
        expect = "Error on line 3 col 1: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 270))
        
    def test271(self):
        input = """
                                    func Add() {
                                        a.foo() *= 2;       
                                    };"""
        expect = "Error on line 3 col 49: *="
        self.assertTrue(TestParser.checkParser(input, expect, 271))
        
    def test272(self):
        input = """
        const a = a.2; 
"""
        expect = "Error on line 2 col 21: 2"
        self.assertTrue(TestParser.checkParser(input, expect, 272))
        
    def test273(self):
        # 273. Empty input: không có gì trong chương trình
        input = ""
        expect = "Error on line 1 col 1: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 273))

    def test274(self):
        # 274. Input chỉ chứa khoảng trắng
        input = "   "
        expect = "Error on line 1 col 4: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 274))

    def test275(self):
        # 275. Input chỉ chứa comment (sẽ bị thiếu khai báo chương trình)
        input = "/* comment */"
        expect = "Error on line 1 col 14: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 275))

    def test276(self):
        # 276. Extra token sau chương trình hợp lệ
        input = "var a int; extra"
        expect = "Error on line 1 col 12: extra"
        self.assertTrue(TestParser.checkParser(input, expect, 276))

    def test277(self):
        # 277. Thiếu dấu chấm phẩy sau khai báo biến
        input = "var a int"
        expect = "Error on line 1 col 10: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 277))

    def test278(self):
        # 278. Function declaration thiếu dấu '}' kết thúc thân hàm
        input = "func main() { return; "
        expect = "Error on line 1 col 23: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 278))

    def test279(self):
        # 279. If statement: thiếu dấu ')' trước '{'
        input = "func main() { if (a < 10 { var a int; } };"
        expect = "Error on line 1 col 26: {"
        self.assertTrue(TestParser.checkParser(input, expect, 279))

    def test280(self):
        # 280. For loop: thiếu dấu chấm phẩy giữa phần khởi tạo và điều kiện
        input = "func main() { for a:=0 a<10; a:=a+1 { var a int; } };"
        expect = "Error on line 1 col 24: a"
        self.assertTrue(TestParser.checkParser(input, expect, 280))

    def test281(self):
        # 281. Assignment: thiếu biểu thức bên phải operator
        input = "func main() { a:= ; };"
        expect = "Error on line 1 col 19: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 281))

    def test282(self):
        # 282. Array literal có trailing comma (dấu phẩy thừa)
        input = "func main() { a:= [3]int {1,2,} };"
        expect = "Error on line 1 col 31: }"
        self.assertTrue(TestParser.checkParser(input, expect, 282))

    def test283(self):
        # 283. Method call: thiếu identifier sau dấu chấm
        input = "func main() { obj.(); };"
        expect = "Error on line 1 col 19: ("
        self.assertTrue(TestParser.checkParser(input, expect, 283))

    def test284(self):
        # 284. Function call: extra dấu phẩy đứng đầu danh sách tham số
        input = "func main() { foo(,1,2); };"
        expect = "Error on line 1 col 19: ,"
        self.assertTrue(TestParser.checkParser(input, expect, 284))

    def test285(self):
        # 285. Sử dụng từ khóa dự trữ làm identifier
        input = "func main() { var if int; };"
        expect = "Error on line 1 col 19: if"
        self.assertTrue(TestParser.checkParser(input, expect, 285))

    def test286(self):
        # 286. Function declaration thiếu cặp dấu () sau tên hàm
        input = "func main { return; };"
        expect = "Error on line 1 col 11: {"
        self.assertTrue(TestParser.checkParser(input, expect, 286))

    def test287(self):
        # 287. Method declaration: thiếu receiver (hoặc receiver sai định dạng)
        input = "func () Method(param int) int { return param; };"
        expect = "Error on line 1 col 7: )"
        self.assertTrue(TestParser.checkParser(input, expect, 287))

    def test288(self):
        # 288. Interface declaration: thiếu dấu chấm phẩy giữa các method
        input = "type I interface { Foo(a int) Bar(); };"
        expect = "Error on line 1 col 34: ("
        self.assertTrue(TestParser.checkParser(input, expect, 288))

    def test289(self):
        # 289. Struct declaration: thiếu dấu chấm phẩy giữa các trường
        input = "type Point struct { x int y int; };"
        expect = "Error on line 1 col 27: y"
        self.assertTrue(TestParser.checkParser(input, expect, 289))

    def test290(self):
        # 290. For loop: sử dụng assignment sai cú pháp (dùng '=' thay vì ':=')
        input = "func main() { for a=0; a<10; a=a+1 { var a int; } };"
        expect = "Error on line 1 col 20: ="
        self.assertTrue(TestParser.checkParser(input, expect, 290))

    def test291(self):
        # 291. Return statement: extra token sau return expression
        input = "func main() { return 42 extra; };"
        expect = "Error on line 1 col 25: extra"
        self.assertTrue(TestParser.checkParser(input, expect, 291))

    def test292(self):
        # 292. Unclosed block comment (để lexer báo lỗi)
        input = "/* unclosed comment"
        expect = "Error on line 1 col 1: /"
        self.assertTrue(TestParser.checkParser(input, expect, 292))

    def test293(self):
        # 293. Biểu thức: thiếu toán tử giữa hai toán hạng
        input = "func main() { a:= 1 2; };"
        expect = "Error on line 1 col 21: 2"
        self.assertTrue(TestParser.checkParser(input, expect, 293))

    def test294(self):
        # 294. Method call: thiếu dấu ')' kết thúc danh sách tham số
        input = "func main() { obj.method(1; };"
        expect = "Error on line 1 col 27: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 294))

    def test295(self):
        # 295. Hàm với nested parentheses không cân bằng
        input = "func main() { a:= (1+(2*3); };"
        expect = "Error on line 1 col 27: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 295))

    def test296(self):
        # 296. Khai báo biến: type không hợp lệ (thừa kiểu)
        input = "var a int float;"
        expect = "Error on line 1 col 11: float"
        self.assertTrue(TestParser.checkParser(input, expect, 296))

    def test297(self):
        # 297. For loop: thiếu dấu '}' kết thúc block loop
        input = "func main() { for a<10 { var a int; };"
        expect = "Error on line 1 col 39: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 297))

    def test298(self):
        # 298. If statement: có token không hợp lệ trong điều kiện
        input = "func main() { if (a < 10 extra) { var a int; } };"
        expect = "Error on line 1 col 26: extra"
        self.assertTrue(TestParser.checkParser(input, expect, 298))

    def test299(self):
        # 299. Function call: thiếu dấu ')' cuối đối số
        input = "func main() { foo(1,2; };"
        expect = "Error on line 1 col 22: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 299))

    def test300(self):
        # 300. Assignment: biểu thức không hoàn chỉnh (thiếu toán hạng sau '+')
        input = "func main() { a:= 5+; };"
        expect = "Error on line 1 col 21: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 300))

    # def test301(self):
    #     # 301. Khai báo mảng sai cú pháp: thiếu từ khóa ASSIGN khi khởi tạo literal
    #     input = "var arr [10]int {1,2,3};"
    #     expect = "Error on line 1 col 17: {"
    #     self.assertTrue(TestParser.checkParser(input, expect, 301))

    # def test302(self):
    #     # 302. Program: không đóng ngoặc nhọn cho thân hàm
    #     input = "func main() { var a int; "
    #     expect = "Error on line 1 col 26: <EOF>"
    #     self.assertTrue(TestParser.checkParser(input, expect, 302))
    
    # def test303(self):
    #     # 303. Program: ko có dấu chấm phẩy cuối khai báo struct
    #     input="type Person struct { name string; age int; }"
    #     expect="Error on line 1 col 45: <EOF>"
    #     self.assertTrue(TestParser.checkParser(input,expect,303))
        
    # def test304(self):
      
    #     input="""
    #                                         const a = [ID][2][VT]int{{{1}}}                              
    #                                     """
    #     expect="successful"
    #     self.assertTrue(TestParser.checkParser(input,expect,304))
        
    # def test305(self):
      
    #     input="""    
    #         var z [1]int = a[1][1][a + 1].foo()                       
    #     """
    #     expect="successful"
    #     self.assertTrue(TestParser.checkParser(input,expect,305))
        
    def test306(self):
      
        input="""    
            func main() { for var a int; a<10; a:=a+1 { } ;};                        
        """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,306))
        
    def test307(self):
        # struct va array trong array, array va struct trong struct 
        input = "var x [1]int = [1]int{ p { x: p{}, y : [5]int{1} }, {1}};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,307))

