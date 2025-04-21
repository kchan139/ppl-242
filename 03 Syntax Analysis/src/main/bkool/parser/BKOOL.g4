grammar BKOOL;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

//========== PARSER RULES ==========//

//====== Q1 ======//
// program
// 	: manyDecl EOF
// 	;	// write for program rule here using vardecl and funcdecl
// manyDecl
// 	: manyDecl varOrFuncDecl | varOrFuncDecl
// 	;
// varOrFuncDecl
// 	: vardecl | funcdecl
// 	;
// vardecl
// 	: 'vardecl' 
// 	;
// funcdecl
// 	: 'funcdecl' 
// 	;

//====== Q2 ======//
// program
// 	: manyDecl EOF
// 	;	// write for program rule here using vardecl and funcdecl
// manyDecl
// 	: manyDecl varOrFuncDecl | varOrFuncDecl
// 	;
// varOrFuncDecl
// 	: vardecl | funcdecl
// 	;
// vardecl
// 	: bkoolType idList SEMICOLON
// 	;
// bkoolType
// 	: INT | FLOAT
// 	;
// idList
// 	: ID idListTail
// 	;
// idListTail
// 	: COMMA ID idListTail 
// 	|
// 	;
// funcdecl
// 	: bkoolType ID paramDecl body
// 	;
// paramDecl
// 	: LPAREN paramList RPAREN
// 	;
// paramList
// 	: param paramListTail
// 	|
// 	;
// paramListTail
// 	: SEMICOLON param paramListTail
// 	|
// 	;
// param
// 	: bkoolType idList
// 	;
// body
// 	: 'body'
// 	;



//====== Q3 ======//
// program
// 	: manyDecl EOF
// 	;	// write for program rule here using vardecl and funcdecl
// manyDecl
// 	: manyDecl varOrFuncDecl | varOrFuncDecl
// 	;
// varOrFuncDecl
// 	: vardecl | funcdecl
// 	;
// vardecl
// 	: bkoolType idList SEMICOLON
// 	;
// bkoolType
// 	: INT | FLOAT
// 	;
// idList
// 	: ID idListTail
// 	;
// idListTail
// 	: COMMA ID idListTail 
// 	|
// 	;
// funcdecl
// 	: bkoolType ID paramDecl body
// 	;
// paramDecl
// 	: LPAREN paramList RPAREN
// 	;
// paramList
// 	: param paramListTail
// 	|
// 	;
// paramListTail
// 	: SEMICOLON param paramListTail
// 	|
// 	;
// param
// 	: bkoolType idList
// 	;
// body
// 	: LBRACK bodyContent RBRACK
// 	;
// bodyContent
// 	: manyDecl manyStmt
// 	| manyVarDecl 
// 	| manyStmt
//  |
// 	;
// manyVarDecl
// 	: manyVarDecl vardecl
// 	| vardecl
// 	;
// manyStmt
// 	: manyStmt stmt
// 	| stmt
// 	;
// stmt
// 	: assignStmt SEMICOLON
// 	| callStmt SEMICOLON
// 	| returnStmt SEMICOLON
// 	;
// assignStmt
// 	: ID ASSIGN expr
// 	;
// callStmt
// 	: ID LPAREN exprList RPAREN 
// 	;
// returnStmt
// 	: RETURN expr
// 	;
// exprList
// 	: expr exprListTail
// 	|
// 	;
// exprListTail
// 	: COMMA expr exprListTail
// 	|
// 	;
// expr
// 	: 'expr'
// 	;


//====== Q4 ======//
program
	: manyDecl EOF
	;	// write for program rule here using vardecl and funcdecl
manyDecl
	: manyDecl varOrFuncDecl | varOrFuncDecl
	;
varOrFuncDecl
	: vardecl | funcdecl
	;
vardecl
	: bkoolType idList SEMICOLON
	;
bkoolType
	: INT | FLOAT
	;
idList
	: ID idListTail
	;
idListTail
	: COMMA ID idListTail 
	|
	;
funcdecl
	: bkoolType ID paramDecl body
	;
paramDecl
	: LPAREN paramList RPAREN
	;
paramList
	: param paramListTail
	|
	;
paramListTail
	: SEMICOLON param paramListTail
	|
	;
param
	: bkoolType idList
	;
body
	: LBRACK bodyContent RBRACK
	;
bodyContent
	: manyDecl manyStmt
	| manyVarDecl 
	| manyStmt
	|
	;
manyVarDecl
	: manyVarDecl vardecl
	| vardecl
	;
manyStmt
	: manyStmt stmt
	| stmt
	;
stmt
	: assignStmt SEMICOLON
	| callStmt SEMICOLON
	| returnStmt SEMICOLON
	;
assignStmt
	: ID ASSIGN expr
	;
callStmt
	: ID LPAREN exprList RPAREN 
	;
returnStmt
	: RETURN expr
	;
exprList
	: expr exprListTail
	|
	;
exprListTail
	: COMMA expr exprListTail
	|
	;

expr
	: expr1 ADD expr
	| expr1
	;
expr1
	: expr2 SUB expr2
	| expr2
	;
expr2
	: expr2 mulOrDiv expr3
	| expr3
	;
expr3
	: INT_LIT 
	| FLOAT_LIT
	| ID
	| callStmt
	| subExpr
	;
subExpr
	: LPAREN expr RPAREN
	;

mulOrDiv
	: MUL | DIV
	;


//========== LEXER RULES ==========//

INT
	: 'int'
	;
FLOAT
	: 'float'
	;
COMMA
	: ','
	;
SEMICOLON
	: ';'
	;
LPAREN
	: '('
	;
RPAREN
	: ')'
	;
LBRACK
	: '{'
	;
RBRACK
	: '}'
	;
ASSIGN
	: '='
	;
RETURN
	: 'return'
	;
ADD
	: '+'
	;
SUB
	: '-'
	;
MUL
	: '*'
	;
DIV 
	: '/'
	;
INT_LIT
	: [0-9]+
	;
FLOAT_LIT
	: INT_LIT '.' INT_LIT
	;
ID
	: [a-zA-Z]+
	; // includes a sequence of alphabetic characters.
WS
	: [ \t\r\n] -> skip
	;
ERROR_CHAR
	: . {raise ErrorToken(self.text)}
	;