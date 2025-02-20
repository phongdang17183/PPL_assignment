import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
      
    def test_lower_identifier(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("abc\tt","abc,t,<EOF>",101))
    
    def test_wrong_token(self):
        self.assertTrue(TestLexer.checkLexeme("ab?sVN","ab,ErrorToken ?",102))
        
    def test_keyword_var(self):
        """test keyword var"""
        self.assertTrue(TestLexer.checkLexeme("var abc int ;","var,abc,int,;,<EOF>",103))
    def test_keyword_func(self):
        """test keyword func"""
        self.assertTrue(TestLexer.checkLexeme("""func abc ( ) ""","""func,abc,(,),<EOF>""",104))
    
    def test105(self):
        input = "123"
        expect = "123,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,105))
        
    def test106(self):
        input = """/* ajshdajshd _ hahsdh / " asj */ int"""
        expect = """int,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,106))
        
        
    def test107(self):
        input = """int a = 3; \n a = a+ 3;"""
        expect = """int,a,=,3,;,a,=,a,+,3,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,107))
        
    def test108(self):
        input = """//asdhkasjd asdhasd \t \n  int"""
        expect = """int,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,108))
        
    def test109(self):
        input = """var x string = "asdhjkas";"""
        expect = """var,x,string,=,\"asdhjkas\",;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,109))
        
    def test110(self):
        input = """var x string = "asdhjkas\\t";"""
        expect = """var,x,string,=,\"asdhjkas\\t\",;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,110))
        
    def test111(self):
        input = """var x string = "asdhjkas\\";"""
        expect = """var,x,string,=,Unclosed string: "asdhjkas\\";"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,111))
        
    def test112(self):
        input = """var x string = "asdhjkas\\\\\\\"";"""
        expect = """var,x,string,=,\"asdhjkas\\\\\\\"\",;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,112))
        
    def test113(self):
        input = """var x int = 0b1101010;"""
        expect = """var,x,int,=,0b1101010,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,113)) 
    
    def test114(self):
        input = """var x int = 0b1231010;"""
        expect = """var,x,int,=,0b1,231010,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,114)) 
    
    def test115(self):
        input = """var x string = "asdahsjkd;"""
        expect = """var,x,string,=,Unclosed string: \"asdahsjkd;"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,115)) 
        
    def test116(self):
        input = """
        const a = 2
        """
        expect = """const,a,=,2,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,116)) 
        
    def test117(self):
        input = """/*  /* This is a /* nested
            multi-line
            comment.
                */ /* /* */"""
        expect = "<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,117))

    def test118(self):
        intput = """010.010e-020"""
        expect = "010.010e-020,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(intput,expect,118))
        
    def test_119(self):
        """UNCLOSE_STRING"""
        self.assertTrue(TestLexer.checkLexeme(""" "abcabc\n" ""","Unclosed string: \"abcabc", 119))
    
    def test120(self):
        input = """var x int = 09.e-002;"""
        expect = """var,x,int,=,09.e-002,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,120))
        
    def test121(self):
        input = """var x int = 0452.;"""
        expect = """var,x,int,=,0452.,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,121))
        
    def test122(self):
        input = """ "test122 \\r" """
        expect = """\"test122 \\r\",<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,122))
        
    def test123(self):
        input = """ "test123\\f" """
        expect = """Illegal escape in string: \"test123\\f"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,123))
        
        # string dont support ''
    def test124(self):
        input = """ 'test124\\t' """
        expect = """ErrorToken '"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,124))
    
    def test125(self):
        input = """/*
        /* a */ /* b */ 
        // 321231
        */ if /* */ /* */"""
        expect = """if,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,125))
        
    def test126(self):
        input = """var x:= 1
        """
        expect = """var,x,:=,1,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,126))
        
    def test127(self):
        input = """foo()
        x:=3;"""
        expect = """foo,(,),;,x,:=,3,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,127))
        
    def test128(self):
        input = """
                                    func Add() {
                                        2 - 2 += 2;       
                                    }
"""
        expect = """func,Add,(,),{,2,-,2,+=,2,;,},;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,128))
        
    def test129(self):
        input = """
            type Point struct 
            {
                x, y float
                label string
            }
          
            """
        expect = """type,Point,struct,{,x,,,y,float,;,label,string,;,},;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,129))
    
    def test130(self):
        input = """ "abc\n" """
        expect = """Unclosed string: \"abc"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,130))
        
    def test131(self):
        # 1. Kiểm tra Identifier đơn giản
        input = "abc"
        expect = "abc,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 131))

    def test132(self):
        # 2. Kiểm tra một số từ khóa
        input = "if else return"
        expect = "if,else,return,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 132))

    def test133(self):
        # 3. Kiểm tra các toán tử số học
        input = "+ - * / %"
        expect = "+,-,*,/,%,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 133))

    def test134(self):
        # 4. Kiểm tra string literal hợp lệ (sau khi bỏ ngoặc kép)
        input = '"Hello"'
        expect = "\"Hello\",<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 134))

    def test135(self):
        # 5. Kiểm tra illegal escape trong string literal
        input = '"Hello\\q"'
        expect = "Illegal escape in string: \"Hello\\q"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 135))

    def test136(self):
        # 6. Kiểm tra unclosed string
        input = '"abc\n'
        expect = "Unclosed string: \"abc"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 136))

    def test137(self):
        # 7. Kiểm tra float literal
        input = "3.14"
        expect = "3.14,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 137))

    def test138(self):
        # 8. Kiểm tra các integer literal hỗn hợp: decimal, binary, octal, hex.
        input = "123 0 045 0b1010 0x1A"
        # Lưu ý: "045" được tách thành token "0" và "45" theo luật của DECIMAL.
        expect = "123,0,0,45,0b1010,0x1A,<EOF>" 
        self.assertTrue(TestLexer.checkLexeme(input, expect, 138))

    def test139(self):
        # 9. Kiểm tra assignment với operator ':='
        input = "a:=5"
        expect = "a,:=,5,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 139))

    def test140(self):
        # 10. Kiểm tra function call với danh sách tham số
        input = "foo(1,2)"
        expect = "foo,(,1,,,2,),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 140))

    def test141(self):
        # 11. Kiểm tra dấu ngoặc đơn
        input = "( )"
        expect = "(,),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 141))

    def test142(self):
        # 12. Kiểm tra các dấu phân cách
        input = "( ) { } [ ] , . ; :"
        expect = "(,),{,},[,],,,.,;,:,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 142))

    def test143(self):
        # 13. Kiểm tra bỏ qua comment (line comment và block comment)
        input = "var x = 10; // comment\n/* block comment */ var y = 20;"
        expect = "var,x,=,10,;,var,y,=,20,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 143))

    def test144(self):
        # 14. Kiểm tra string literal với escape sequence hợp lệ
        input = '"Hello, World!\\n" "Line\\tTab"'
        expect = "\"Hello, World!\\n\",\"Line\\tTab\",<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 144))

    def test145(self):
        # 15. Kiểm tra tự động chèn ';' khi gặp newline sau token hợp lệ.
        # Vì sau một ID (token hợp lệ) và sau đó newline, lexer chuyển '\n' thành ';'
        input = "a\nb"
        expect = "a,;,b,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 145))

    def test146(self):
        # 16. Kiểm tra chèn ';' sau biểu thức.
        input = "a+b\nc"
        expect = "a,+,b,;,c,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 146))

    def test147(self):
        # 17. Kiểm tra khai báo biến đơn giản
        input = "var a int;"
        expect = "var,a,int,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 147))

    def test148(self):
        # 18. Kiểm tra khai báo hàm đơn giản
        input = "func main() { return; }"
        expect = "func,main,(,),{,return,;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 148))

    def test149(self):
        # 19. Kiểm tra khai báo struct
        input = "type Point struct { x int; y int; }"
        expect = "type,Point,struct,{,x,int,;,y,int,;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 149))

    def test150(self):
        # 20. Kiểm tra khai báo interface
        input = "type I interface { foo(); }"
        expect = "type,I,interface,{,foo,(,),;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 150))

    def test151(self):
        # 21. Kiểm tra khai báo hằng số
        input = "const a = 10;"
        expect = "const,a,=,10,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 151))

    def test152(self):
        # 22. Kiểm tra các assignment operator: +=, -=, *=, /=, %=
        input = "a+=b; a-=c; a*=d; a/=e; a%=f;"
        expect = "a,+=,b,;,a,-=,c,;,a,*=,d,;,a,/=,e,;,a,%=,f,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 152))

    def test153(self):
        # 23. Kiểm tra các toán tử so sánh: ==, !=, <, <=, >, >=
        input = "a==b; a!=c; a<d; a<=e; a>f; a>=g;"
        expect = "a,==,b,;,a,!=,c,;,a,<,d,;,a,<=,e,;,a,>,f,;,a,>=,g,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 153))

    def test154(self):
        # 24. Kiểm tra các toán tử logic: &&, ||, !
        input = "a&&b; a||c; !d;"
        expect = "a,&&,b,;,a,||,c,;,!,d,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 154))

    def test155(self):
        # 25. Kiểm tra khai báo mảng: var arr [10]int;
        input = "var arr [10]int;"
        expect = "var,arr,[,10,],int,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 155))

    def test156(self):
        # 26. Kiểm tra array literal: {1,2,3}
        input = "{1,2,3}"
        expect = "{,1,,,2,,,3,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 156))

    def test157(self):
        # 27. Kiểm tra struct literal: {x:10,y:20}
        input = "{x:10,y:20}"
        expect = "{,x,:,10,,,y,:,20,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 157))

    def test158(self):
        # 28. Kiểm tra compound identifier: a.b.c
        input = "a.b.c"
        expect = "a,.,b,.,c,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 158))

    def test159(self):
        # 29. Kiểm tra truy cập mảng lồng nhau: a[1][2]
        input = "a[1][2]"
        expect = "a,[,1,],[,2,],<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 159))

    def test160(self):
        # 30. Kiểm tra function call không có đối số: foo()
        input = "foo()"
        expect = "foo,(,),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 160))

    def test161(self):
        # 31. Kiểm tra method call: obj.method(1)
        input = "obj.method(1)"
        expect = "obj,.,method,(,1,),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 161))

    def test162(self):
        # 32. Kiểm tra for loop đơn giản: for i { }
        # (theo grammar: FOR expr L_BRACE list_stmt R_BRACE)
        input = "for i { }"
        expect = "for,i,{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 162))

    def test163(self):
        # 33. Kiểm tra for loop với assignment
        input = "for i:=0; i<10; i:=i+1 { }"
        expect = "for,i,:=,0,;,i,<,10,;,i,:=,i,+,1,{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 163))

    def test164(self):
        # 34. Kiểm tra for loop với 2 ID phân tách bởi dấu phẩy
        # (theo grammar: FOR ID COMMA ID DECLARE_ASSIGN RANGE ID L_BRACE list_stmt R_BRACE)
        input = "for a,b:=range arr { }"
        expect = "for,a,,,b,:=,range,arr,{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 164))

    def test165(self):
        # 35. Kiểm tra for loop với '_' và ID
        # (theo grammar: FOR '_' COMMA ID DECLARE_ASSIGN RANGE ID L_BRACE list_stmt R_BRACE)
        input = "for _ ,i:=range arr { }"
        expect = "for,_,,,i,:=,range,arr,{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 165))

    def test166(self):
        # 36. Kiểm tra break và continue
        input = "break; continue;"
        expect = "break,;,continue,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 166))

    def test167(self):
        # 37. Kiểm tra biểu thức số học phức tạp
        input = "a+b*c-d/e%f"
        expect = "a,+,b,*,c,-,d,/,e,%,f,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 167))

    def test168(self):
        # 38. Kiểm tra boolean literal
        input = "true false"
        expect = "true,false,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 168))

    def test169(self):
        # 39. Kiểm tra nil literal
        input = "nil"
        expect = "nil,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 169))

    def test170(self):
        # 40. Kiểm tra ngoặc đơn lồng nhau
        input = "((a))"
        expect = "(,(,a,),),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 170))

    def test171(self):
        # 41. Kiểm tra function call với biểu thức làm đối số
        input = "foo(a+b)"
        expect = "foo,(,a,+,b,),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 171))

    def test172(self):
        # 42. Kiểm tra biểu thức logic phức tạp
        input = "a&&b||!c"
        expect = "a,&&,b,||,!,c,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 172))

    def test173(self):
        # 43. Kiểm tra array literal với các phần tử hỗn hợp: số, identifier, và array literal lồng nhau
        input = "{1, a, {2,3}}"
        expect = "{,1,,,a,,,{,2,,,3,},},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 173))

    def test174(self):
        # 44. Kiểm tra ký tự không hợp lệ: sử dụng ký tự '@'
        input = "@"
        expect = "ErrorToken @"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 174))

    def test175(self):
        # 45. Kiểm tra illegal escape khác: ví dụ: "\\z"
        input = '"abc\\z"'
        expect = "Illegal escape in string: \"abc\\z" 
        self.assertTrue(TestLexer.checkLexeme(input, expect, 175))

    def test176(self):
        # 46. Kiểm tra unclosed string khác
        input = '"abc'
        expect = "Unclosed string: \"abc"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 176))

    def test177(self):
        # 47. Kiểm tra identifier có dấu gạch dưới đầu (_id)
        input = "var _id int;"
        expect = "var,_id,int,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 177))

    def test178(self):
        # 48. Kiểm tra float literal với exponent
        input = "1.23e+10"
        expect = "1.23e+10,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 178))

    def test179(self):
        # 49. Kiểm tra identifier chứa dấu gạch dưới
        input = "my_var"
        expect = "my_var,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 179))

    def test180(self):
        # 50. Kiểm tra danh sách các từ khóa dự trữ
        input = "if else for return func type struct interface const var break continue nil"
        expect = "if,else,for,return,func,type,struct,interface,const,var,break,continue,nil,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 180))

    def test181(self):
        # 51. Kiểm tra block comment lồng nhiều cấp
        input = "var a int; /* outer comment /* inner comment */ end outer */ var b int;"
        expect = "var,a,int,;,var,b,int,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 181))

    def test182(self):
        # 52. Kiểm tra nhiều dòng newline liên tiếp để kiểm tra tự động chèn dấu ';'
        input = "a\n\nb"
        expect = "a,;,b,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 182))

    def test183(self):
        # 53. Kiểm tra string literal chứa nhiều escape sequence hợp lệ
        input = '"Line\\n Tab\\t Carriage\\r Quote\\" Backslash\\\\"'
        expect = "\"Line\\n Tab\\t Carriage\\r Quote\\\" Backslash\\\\\",<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 183))

    def test184(self):
        # 54. Kiểm tra identifier trông giống từ khóa nhưng không phải từ khóa
        input = "if1 else2"
        expect = "if1,else2,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 184))

    def test185(self):
        # 55. Kiểm tra string literal chứa newline thật bên trong (sẽ bị báo lỗi unclosed)
        input = '"abc\ndef"'
        expect = "Unclosed string: \"abc"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 185))

    def test186(self):
        # 56. Kiểm tra bỏ qua block comment đơn giản
        input = "var a int; /* simple comment */ var b int;"
        expect = "var,a,int,;,var,b,int,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 186))

    def test187(self):
        # 57. Kiểm tra line comment có chứa các dấu // bên trong comment
        input = "var x = 5; // comment with // inside"
        expect = "var,x,=,5,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 187))

    def test188(self):
        # 58. Kiểm tra string literal liền kề identifier (không có khoảng trắng)
        input = '"Hello"world'
        expect = "\"Hello\",world,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 188))

    def test189(self):
        # 59. Kiểm tra khai báo mảng với mảng 2 chiều: var arr [10][20]int;
        input = "var arr [10][20]int;"
        expect = "var,arr,[,10,],[,20,],int,;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 189))

    def test190(self):
        # 60. Kiểm tra khai báo hằng số với array literal
        input = "const a = [3]int{1,2,3};"
        expect = "const,a,=,[,3,],int,{,1,,,2,,,3,},;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 190))

    def test191(self):
        # 61. Kiểm tra khai báo hàm không có tham số và không có kiểu trả về
        input = "func foo() { var a int; }"
        expect = "func,foo,(,),{,var,a,int,;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 191))

    def test192(self):
        # 62. Kiểm tra khai báo hàm có tham số và kiểu trả về
        input = "func foo(a int, b float) int { return a; }"
        expect = "func,foo,(,a,int,,,b,float,),int,{,return,a,;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 192))

    def test193(self):
        # 63. Kiểm tra khai báo method (theo cú pháp của methoddecl)
        input = "func (x MyType) Foo() { }"
        expect = "func,(,x,MyType,),Foo,(,),{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 193))

    def test194(self):
        # 64. Kiểm tra khai báo interface với nhiều method
        input = """
        type I interface {
            Foo(a int);
            Bar();
        }
        """
        expect = "type,I,interface,{,Foo,(,a,int,),;,Bar,(,),;,},;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 194))

    def test195(self):
        # 65. Kiểm tra biểu thức phức tạp với nhiều toán tử so sánh và logic
        input = "a==b&&c||d!=e<=f>=g"
        expect = "a,==,b,&&,c,||,d,!=,e,<=,f,>=,g,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 195))

    def test196(self):
        # 66. Kiểm tra dấu ngoặc đơn và ngoặc vuông lồng nhau
        input = "((a+[b*(c-d)]))"
        expect = "(,(,a,+,[,b,*,(,c,-,d,),],),),<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 196))

    def test197(self):
        # 67. Kiểm tra array literal lồng nhau (nested array literal)
        input = "{1, {2, {3}}}"
        # Các token mong đợi: { 1 , { 2 , { 3 } } }
        expect = "{,1,,,{,2,,,{,3,},},},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 197))

    def test198(self):
        # 68. Kiểm tra truy cập thành viên và chỉ số mảng trong biểu thức
        input = "a.b().c[2]"
        expect = "a,.,b,(,),.,c,[,2,],<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 198))

    def test199(self):
        # 69. Kiểm tra toán tử đơn: âm và phủ định logic
        input = "-a + !b"
        expect = "-,a,+,!,b,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 199))

    def test200(self):
        input = """ "123
        " """
        expect = "Unclosed string: \"123"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 200))
        
    def test201(self):
        input = """ "&\\&" """
        expect = "Illegal escape in string: \"&\\&"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 201))
        
    def test202(self):
        input = """ "\\z" """
        expect = "Illegal escape in string: \"\\z"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 202))