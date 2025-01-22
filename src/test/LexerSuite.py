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
        expect = """var,x,string,=,asdhjkas,ErrorToken \\"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,111))
        
    def test111(self):
        input = """var x string = "asdhjkas\\\\\\\"";"""
        expect = """var,x,string,=,asdhjkas\\\\\\\",;,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input,expect,111))
        