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
        expect = """var,x,string,=,asdhjkas,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,109))
        
    def test110(self):
        input = """var x string = "asdhjkas\\t";"""
        expect = """var,x,string,=,asdhjkas\\t,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,110))
        
    def test111(self):
        input = """var x string = "asdhjkas\\";"""
        expect = """var,x,string,=,Unclosed string: asdhjkas\\";"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,111))
        
    def test112(self):
        input = """var x string = "asdhjkas\\\\\\\"";"""
        expect = """var,x,string,=,asdhjkas\\\\\\\",;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,112))
        
    def test113(self):
        input = """var x int = 0b1101010;"""
        expect = """var,x,int,=,0b1101010,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,113)) 
    
    def test114(self):
        input = """var x int = 0b1231010;"""
        expect = """var,x,int,=,0b1,231010,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,114)) 
        
    # def testDecimalInvalid(self):
    #     input = """var x int = 012345;"""
    #     expect = """var,x,int,=,ErrorToken 012345"""  # Leading zero không hợp lệ
    #     self.assertTrue(TestLexer.checkLexeme(input, expect, 115))
    
    def test115(self):
        input = """var x string = "asdahsjkd;"""
        expect = """var,x,string,=,Unclosed string: asdahsjkd;"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,115)) 
        
    def test116(self):
        input = """
        const a = 2;
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
        # need to fix
        intput = """010.010e-020"""
        expect = "0,10.010e-0,20,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(intput,expect,118))
        
    # def test_119(self):
    #     """UNCLOSE_STRING"""
    #     self.assertTrue(TestLexer.checkLexeme(""" "VOTIEN\\n" ""","Unclosed string: VOTIEN", 119))
    
    def test120(self):
        input = """var x int = 09.e-002;"""
        expect = """var,x,int,=,0,9.e-0,0,2,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,120))
        
    def test121(self):
        input = """var x int = 0452.;"""
        expect = """var,x,int,=,0,452.,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,121))
        
    def test122(self):
        input = """ "test122 \\r" """
        expect = """test122 \\r,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,122))
        
    def test123(self):
        input = """ "test123\\f" """
        expect = """Illegal escape in string: test123\\f"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,123))
        
        # string dont support ''
    # def test124(self):
    #     input = """'test124\\t'''"""
    #     expect = """'test124\\t''',<EOF>"""
    #     self.assertTrue(TestLexer.checkLexeme(input,expect,124))
    
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
        input = """foo() /* 
        /* a */ /* b */ 
        */
        x:=3
        """
        expect = """foo,(,),;,x,:=,3,;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,127))