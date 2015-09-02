from ply import *
import lexer

tokens = lexer.tokens

#precedence = (('left', 'AND', 'OR'),('right','UMINUS'))

strings = []
cols = []

def p_program(p):
	'''program : statement SEMICOLON'''

def p_statement(p):
	'''statement : SELECT select_statement'''
#		| UPDATE update_statement
#		| DELETE delete_statement'''
	strings.insert(0,p[1])

def p_select_statement(p):
	'''select_statement : ASTERISK FROM IDENTIFIER
		| columns FROM IDENTIFIER
               | ASTERISK FROM IDENTIFIER where_statement
		| columns FROM IDENTIFIER where_statement'''
	global cols
	strings.insert(0,p[3])
	strings.insert(0,p[2])
	if(p[1]=='*'):
		strings.insert(0,p[1])
	else:
		strings.append(list(cols))
		cols = []

def p_columns(p):
	'''columns : IDENTIFIER COMMA columns
		| IDENTIFIER'''
#	if len(p) > 2:				#inserts the commas to the list
#		strings.insert(0,p[2])		#is this needed? O_O
	strings.insert(0,p[1])

def p_where_statement(p):
	'''where_statement : WHERE expression'''
	strings.insert(0,p[1])

def p_expression(p):
	'''expression : expression AND expression
		| expression OR expression
		| IDENTIFIER EQUAL NUMBER
		| IDENTIFIER EQUAL STRING
		| IDENTIFIER LESSTHAN NUMBER
		| IDENTIFIER GREATERTHAN NUMBER
		| IDENTIFIER NOTEQUAL STRING
		| IDENTIFIER NOTEQUAL NUMBER'''
	if p[2]=='=' or p[2]=='!=' or p[2]=='>' or p[2]=='<':
		strings.append(p[1])
		strings.append(p[2])
		strings.append(p[3])
	elif p[2]=='and' or p[2]=='AND' or p[2]=='or' or p[2]=='OR':
		strings.insert(0,p[2])

def p_error(p):
	if p:
		print("   Syntax error at", p.value)
	else:
		print("   Syntax error at EOF")


parser = yacc.yacc()

def parse(query):
	global strings
	strings = []
	parser.parse(query)
	return strings

