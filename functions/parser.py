from ply import *
import lexer

tokens = lexer.tokens

#precedence = (('left', 'AND', 'OR'),('right','UMINUS'))

strings = []

def p_program(p):
	'''program : statement SEMICOLON'''

def p_statement(p):
	'''statement : SELECT select_statement'''
#		| UPDATE update_statement
#		| DELETE delete_statement'''
	strings.insert(0,p[1])

def p_select_statement(p):
	'''select_statement : ASTERISK FROM IDENTIFIER
		| columns FROM IDENTIFIER'''
#               | ASTERISK FROM IDENTIFIER where_statement
#		| columns FROM IDENTIFIER where_statement'''
	if(p[1]=='*'):
		strings.insert(0,p[1])
	strings.append(p[2])
	strings.append(p[3])

def p_columns(p):
	'''columns : IDENTIFIER COMMA columns
		| IDENTIFIER'''
#	if len(p) > 2:				#inserts the commas to the list
#		strings.insert(0,p[2])		#is this needed? O_O
	strings.insert(0,p[1])

def p_error(p):
	if p:
		print("Syntax error at", p.value)
	else:
		print("Syntax error at EOF")

def parse(query):
	yacc.yacc()
	yacc.parse(query)
	print(strings)
