// MSSV: 2212548 
grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
lastToken = None

def emit(self):
	token = super().emit()
	if token.type not in (self.NL, self.UNCLOSE_STRING, self.ILLEGAL_ESCAPE, self.ERROR_CHAR):
		self.lastToken = token
		
	if token.type == self.UNCLOSE_STRING:
		raise UncloseString(token.text)
	elif token.type == self.ILLEGAL_ESCAPE:
		raise IllegalEscape(token.text)
	elif token.type == self.ERROR_CHAR:
		raise ErrorToken(token.text)
	return token
}

options{
	language = Python3;
}

program: list_decl EOF;

list_stmt: list_stmt stmt | stmt | ;

list_decl: list_decl declared_stmt SEMICOLON| declared_stmt SEMICOLON;

stmt:
	(
		declared_stmt
		| assignment_stmt
		| if_stmt
		| loop_stmt
		| break_stmt
		| continue_stmt
		| functionCall_stmt
		//	| specialCall_stmt
		| methodCall_stmt
		| return_stmt
	) SEMICOLON;

assignment_stmt:
    lhs (
    		DECLARE_ASSIGN
    		| ADD_ASSIGN
    		| SUB_ASSIGN
    		| MUL_ASSIGN
    		| DIV_ASSIGN
    		| MOD_ASSIGN
    	) expr;

//assignment_stmt: normalAssign | arrayAssign | structAssign;
//normalAssign:
//	expr (
//		DECLARE_ASSIGN
//		| ADD_ASSIGN
//		| SUB_ASSIGN
//		| MUL_ASSIGN
//		| DIV_ASSIGN
//		| MOD_ASSIGN
//	) expr;
//arrayAssign: expr DECLARE_ASSIGN array;
//structAssign: expr DECLARE_ASSIGN ID struct;

lhs:
    ID
    | lhs L_BRACKET expr R_BRACKET
    | lhs DOT ID;


if_stmt: (IF L_PAREN expr R_PAREN L_BRACE list_stmt R_BRACE) else_if_stmt else_stmt;
else_if_stmt:
	else_if_stmt ELSE IF expr L_BRACE list_stmt R_BRACE
	|;
else_stmt: ELSE L_BRACE list_stmt R_BRACE |;

loop_stmt:
	FOR expr L_BRACE list_stmt R_BRACE
	| FOR assignment_stmt SEMICOLON expr SEMICOLON assignment_stmt L_BRACE list_stmt R_BRACE
	| FOR vardecl SEMICOLON expr SEMICOLON assignment_stmt L_BRACE list_stmt R_BRACE
	| FOR ID COMMA ID DECLARE_ASSIGN RANGE ID L_BRACE list_stmt R_BRACE
	| FOR '_' COMMA ID DECLARE_ASSIGN RANGE ID L_BRACE list_stmt R_BRACE;
break_stmt: BREAK;
continue_stmt: CONTINUE;
functionCall_stmt:
	ID L_PAREN list_expr R_PAREN
	| ID L_PAREN R_PAREN;
//specialCall_stmt: getInt | putInt | putIntLn | getFloat | putFloat | putFloatLn | getBool | putBool | putBoolLn | getString | putString | putStringLn | putLn ;
methodCall_stmt: methodCall L_PAREN list_expr? R_PAREN;
methodCall:
    methodCall ( L_BRACKET expr R_BRACKET  |L_PAREN list_expr? R_PAREN | DOT validCall)
    | ID;

return_stmt: RETURN expr | RETURN;

//  special funtion
 getInt : GETINT L_PAREN R_PAREN ;
 putInt : PUTINT L_PAREN expr R_PAREN ;
 putIntLn: PUTINTLN L_PAREN expr R_PAREN ;
 getFloat : GETFLOAT L_PAREN R_PAREN ;
 putFloat : PUTFLOAT L_PAREN expr R_PAREN ;
 putFloatLn : PUTFLOATLN L_PAREN expr R_PAREN ;
 getBool : GETBOOL L_PAREN R_PAREN ;
 putBool : PUTBOOL L_PAREN expr R_PAREN ;
 putBoolLn : PUTBOOLLN L_PAREN expr R_PAREN ;
 getString : GETSTRING L_PAREN R_PAREN ;
 putString : PUTSTRING L_PAREN expr R_PAREN ;
 putStringLn: PUTSTRINGLN L_PAREN expr R_PAREN ;
 putLn : PUTLN L_PAREN R_PAREN ;

// --------------------------------------------------------Declared statement--------------------------------------------------//
declared_stmt:
	vardecl
	| constdecl
	| structdecl
	| funcdecl
	| methoddecl
	| interfacedecl;
vardecl: vardecl1 | vardecl2 
// | arraydecl
;
vardecl1: VAR ID (atomictype | arraytype)? ASSIGN expr;
vardecl2: VAR ID (atomictype | arraytype);
// arraydecl: 
// 	VAR ID arraytype 
// 	| VAR ID arraytype ASSIGN expr;

constdecl: CONST ID ASSIGN expr;

structdecl: TYPE ID STRUCT L_BRACE list_field R_BRACE;
list_field: list_field field | field ;
field: ID (atomictype | arraytype) SEMICOLON;

funcdecl:
	FUNC ID L_PAREN list_parameter R_PAREN (atomictype | arraytype)? L_BRACE list_stmt R_BRACE;
list_parameter: paramprime |;
paramprime: paramprime COMMA parameter | parameter;
parameter: list_ID (atomictype | arraytype);
list_ID: list_ID COMMA ID | ID;

methoddecl:
	FUNC L_PAREN ID ID R_PAREN ID L_PAREN list_parameter R_PAREN (atomictype | arraytype)? L_BRACE list_stmt
		R_BRACE;

interfacedecl:
	TYPE ID INTERFACE L_BRACE list_methodInterface R_BRACE;
list_methodInterface:
	list_methodInterface methodInterface
	| methodInterface;
methodInterface: ID L_PAREN list_parameter R_PAREN (atomictype | arraytype | ) SEMICOLON;

// TYPE
atomictype: INT | FLOAT | STRING | BOOLEAN | ID;
arraytype: arraytype1 atomictype;
arraytype1:
	arraytype1 L_BRACKET (INT_LIT | ID) R_BRACKET
	| L_BRACKET (INT_LIT | ID) R_BRACKET; // chi moi co intlit co the TH : [x]

// --------------------------------------------------------literal--------------------------------------------------//
literal:
	INT_LIT
	| FLOAT_LIT
	| STRING_LIT
	| BOOLEAN_LIT
	| NIL_LIT
	// | array
	// | ID struct
	;

arrayElement: ID | literal | arraylit | ID struct
	// | expr
	;
list_arrayElement:
	list_arrayElement COMMA arrayElement
	| arrayElement;
arraylit: L_BRACE list_arrayElement R_BRACE;


struct: L_BRACE list_struct_field? R_BRACE;
list_struct_field:
	list_struct_field COMMA fieldprime
	| fieldprime;
fieldprime: ID COLON expr;

// --------------------------------------------------------expression--------------------------------------------------//
list_expr: expr | expr COMMA list_expr;
expr: expr OR expr1 | expr1;
expr1: expr1 AND expr2 | expr2;
expr2:
	expr2 (
		EQUAL
		| NOT_EQ
		| LESS
		| LESS_EQ
		| GREATER
		| GREATER_EQ
	) expr3
	| expr3;
expr3: expr3 (ADD | SUB) expr4 | expr4;
expr4: expr4 (MULT | DIV | MOD) expr5 | expr5;
expr5: (NOT | SUB) expr5 | expr6;
expr6: expr6 (L_BRACKET expr R_BRACKET | DOT validCall) | expr7;
expr7:
	ID
	| literal
	| arraytype arraylit
	| ID struct
	| functionCall_stmt
	| methodCall_stmt
	| L_PAREN expr R_PAREN;
validCall:
    functionCall_stmt
    | ID
//    | methodCall_stmt
    ;
// reserved keywords
NIL_LIT: NIL;
BOOLEAN_LIT: TRUE | FALSE;

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
// UNDERSCORE: '_';
// DOUBLE_QUOTE: '"';

// Separators
L_PAREN: '(';
R_PAREN: ')';
L_BRACKET: '[';
R_BRACKET: ']';
L_BRACE: '{';
R_BRACE: '}';

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

// special funtion
GETINT: 'getInt';
PUTINT: 'putInt';
PUTINTLN: 'putIntLn';
GETFLOAT: 'getFloat';
PUTFLOAT: 'putFloat';
PUTFLOATLN: 'putFloatLn';
GETBOOL: 'getBool';
PUTBOOL: 'putBool';
PUTBOOLLN: 'putBoolLn';
GETSTRING: 'getString';
PUTSTRING: 'putString';
PUTSTRINGLN: 'putStringLn';
PUTLN: 'putLn';

// Literal



fragment DIGIT: [0-9];
fragment NONE_ZERO_DIGIT: [1-9];

fragment BIN_PREFIX: '0b' | '0B';
fragment OCT_PREFIX: '0o' | '0O';
fragment HEX_PREFIX: '0x' | '0X';

fragment BIN_INT: BIN_PREFIX [01]+;
fragment OCT_INT: OCT_PREFIX [0-7]+;
fragment HEX_INT: HEX_PREFIX [0-9a-fA-F]+;
fragment DECIMAL: '0' | (NONE_ZERO_DIGIT DIGIT*);

INT_LIT: DECIMAL | BIN_INT | OCT_INT | HEX_INT;

fragment EXPONENT_PART: [eE] [+-]?  DIGIT+;
FLOAT_LIT: DIGIT+ '.' DIGIT* EXPONENT_PART?;

fragment ESC_SEQ: '\\' [ntr"\\];
fragment ALLOWED_CHAR: ESC_SEQ | ~[\n\r"\\];
STRING_LIT: '"' ALLOWED_CHAR* '"' ;

// Comment
LINE_COMMENT: DIV DIV ~[\r\n]* -> skip;
BLOCK_COMMENT:
	'/*' (NESTED_COMMENT | ~[*] | '*' ~[/])* '*/' -> skip;
fragment NESTED_COMMENT:
	'/*' (NESTED_COMMENT | ~[*] | '*' ~[/])* '*/';

NL:
	'\n' {
allowed_prev = [
    MiniGoLexer.ID,
    MiniGoLexer.INT_LIT, MiniGoLexer.FLOAT_LIT, MiniGoLexer.BOOLEAN_LIT, MiniGoLexer.STRING_LIT,
    MiniGoLexer.INT, MiniGoLexer.FLOAT, MiniGoLexer.NIL_LIT, MiniGoLexer.STRING,
    MiniGoLexer.RETURN, MiniGoLexer.CONTINUE, MiniGoLexer.BREAK,
    MiniGoLexer.R_PAREN, MiniGoLexer.R_BRACKET, MiniGoLexer.R_BRACE
]
if self.lastToken is not None and self.lastToken.type in allowed_prev:
    self.type = self.SEMICOLON
    self.text = ";"
    return self.emit()
else:
    self.skip()
};


WS: [ \t\r\f]+ -> skip; // skip spaces, tabs

// ERROR
ERROR_CHAR: . { raise ErrorToken(self.text) };

UNCLOSE_STRING:
	'"' ALLOWED_CHAR* ('\r\n' | '\n' | EOF) {
    if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
        raise UncloseString(self.text[0:-2])
    elif (self.text[-1] == '\n'):
        raise UncloseString(self.text[0:-1])
    else:
        raise UncloseString(self.text)
};
ILLEGAL_ESCAPE:
	'"' ALLOWED_CHAR* ESC_ILLEGAL {
	raise IllegalEscape(self.text)
};
fragment ESC_ILLEGAL: [\r] | '\\' (~[tnr"\\]);

