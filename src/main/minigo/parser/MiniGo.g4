grammar MiniGo;
// MSSV: 2212548 

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language = Python3;
}

program: decl+ EOF;

decl: funcdecl | vardecl;

vardecl: 'var' ID 'int' ';';

funcdecl: 'func' ID '(' ')' '{' '}' ';';

// reserved keywords
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
TRUE: 'true';
FALSE: 'false';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';
NIL: 'nil';

// Operators
ADD: '+';
SUB: '-';
MULT: '*';
DIV: '/';
MOD: '%';
EQUAL: '==';
NOT_EQ: '!=';
LESS: '<';
LESS_EQ: '<=';
GREATER: '>';
GREATER_EQ: '>=';
AND: '&&';
OR: '||';
NOT: '!';
DECLARE_ASSIGN: ':=';
ASSIGN: '=';
ADD_ASSIGN: '+=';
SUB_ASSIGN: '-=';
MUL_ASSIGN: '*=';
DIV_ASSIGN: '/=';
MOD_ASSIGN: '%=';

DOT: '.';
COMMA: ',';
COLON: ':';
SEMICOLON: ';';
// DOUBLE_QUOTE: '"';

// Separators
L_PAREN: '(';
R_PAREN: ')';
L_BRACKET: '[';
R_BRACKET: ']';
L_BRACE: '{';
R_BRACE: '}';

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

// Literal

NIL_LIT: NIL;
BOOLEAN_LIT: TRUE | FALSE;

fragment DIGIT: [0-9];
fragment NONE_ZERO_DIGIT: [1-9];
fragment BIN_INT: ('0b' | '0B') [01]+;
fragment OCT_INT: ('0o' | '0O') [0-7]+;
fragment HEX_INT: ('0x' | '0X') [0-9a-fA-F]+;
fragment DECIMAL: '0' | NONE_ZERO_DIGIT DIGIT*;

INT_LIT: DECIMAL | BIN_INT | OCT_INT | HEX_INT;

fragment EXPONENT_PART: [eE] [+-]? DECIMAL;
FLOAT_LIT: DECIMAL '.' DIGIT* EXPONENT_PART?;

fragment ESC_SEQ: '\\' [ntr"\\];
fragment ALLOWED_CHAR: ESC_SEQ | ~["\\];
STRING_LIT: '"' ALLOWED_CHAR* '"' {self.text = self.text[1:-1];};

// Comment
LINE_COMMENT: DIV DIV ~[\r\n]* -> skip;
BLOCK_COMMENT: DIV MULT .*? MULT DIV -> skip;

NL: '\n' -> skip; //skip newlines

WS: [ \t\r\f]+ -> skip; // skip spaces, tabs 

ERROR_CHAR: . { raise ErrorToken(self.text) };
ILLEGAL_ESCAPE: .;
UNCLOSE_STRING: .;