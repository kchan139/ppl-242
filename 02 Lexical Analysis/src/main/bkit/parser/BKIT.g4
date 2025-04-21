grammar BKIT;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

program  : VAR COLON ID SEMI EOF ;

fragment Letter
	: [a-z]
	; 
fragment Digit
	: [0-9]
	;
fragment ScientificNotation
	: [eE] [+-]? Digit+
	;
fragment Octet
	: '0'
	| '1' Digit? Digit?
	| '2'  [0-4] Digit
	| '25' [0-5] 
	;

// Question 5
// PHP_INT
//     : '0'
// 	| [1-9] Digit* ('_' Digit+)*
// 	{ self.text = self.text.replace('_', '') }
//     ;

// Question 4
// IPV4
// 	: Octet '.' Octet '.' Octet '.' Octet
// 	;

// Question 3
// STRING 
// 	: '\'' ( ~('\''|'\\') | '\'\'')* '\''
// 	;

// Question 2
// REAL
// 	: Digit* '.' Digit+ ScientificNotation?
// 	| Digit+ '.' Digit* ScientificNotation?
// 	| Digit+ ScientificNotation
// 	;

// Question 1
ID
	: Letter (Letter | Digit)*
	;


SEMI: ';' ;

COLON: ':' ;

VAR: 'Var' ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

ERROR_CHAR: .  {raise ErrorToken(self.text)};
