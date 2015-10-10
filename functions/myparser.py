from ply import *
import lexer

tokens = lexer.tokens

#precedence = (('left', 'AND', 'OR'),('right','UMINUS'))

strings = []
cols = []
tbl = []
flag = 0
count = 0
gap = 3

def p_program(p):
	'''program : statement SEMICOLON'''
	global count
	global gap
	count = 0
	gap = 3

def p_statement(p):
	'''statement : SELECT select_statement
		| UPDATE update_statement
		| DELETE delete_statement'''
	
	strings.insert(0,p[1])

def p_columns(p):
	'''columns : IDENTIFIER
		| IDENTIFIER COMMA columns'''

	if (len(p) == 4) :
		strings.insert(0,p[2])
		strings.insert(0,p[1])
		
	elif (len(p) == 2) :
		strings.append(p[1])
	
	cols.insert(0,p[1])


def p_select_statement(p):
	
	'''select_statement : select_option from_statement
	| select_option from_statement where_statement expression
	| select_option from_statement join_statement expression2'''

			
def p_select_option(p):
	'''select_option : columns
	| ASTERISK'''
	
	if p[1] == '*' :
			strings.insert(0,p[1])


def p_from_statement(p):
	
	'''from_statement : FROM IDENTIFIER'''
	strings.append(p[1])
	strings.append(p[2])
	
	tbl.append(p[2])
	
	

def p_join_statement(p):
	'''join_statement : JOIN IDENTIFIER ON'''
	
	strings.append(p[1])
	strings.append(p[2])
	strings.append(p[3])	
	tbl.append(p[2])



def p_expression2(p):
	'''expression2 : IDENTIFIER EQUAL IDENTIFIER AND expression2
	| IDENTIFIER EQUAL IDENTIFIER OR expression2
	| IDENTIFIER EQUAL IDENTIFIER'''
	
	global count
	global gap
	global strings
	index = len(strings)-gap
	
	if(len(p) == 6):
		strings.insert(index,p[4])
		strings.insert(index,p[3])
		strings.insert(index,p[2])
		strings.insert(index,p[1])
		gap = gap + 4
	
	elif(len(p) == 4):
		strings.append(p[1])
		strings.append(p[2])
		strings.append(p[3])

	
	coLen = len(cols)
	count = 0
	flagp1 = 0
	flagp3 = 0
	
	print(cols)
	print("EXPRESSION 2")
	while(count < coLen):
		if(p[1] == cols[count]):
			flagp1 = 1
		if(p[3] != cols[count]):
			flagp3 = 1
		count = count + 1
	
	if(flagp1 == 0):
		cols.insert(0,p[1])
	if(flagp3 == 0):
		cols.insert(0,p[3])
	
	
	
def p_where_statement(p):
	'''where_statement : WHERE'''

	strings.append(p[1])

def p_expression(p):
	'''expression : IDENTIFIER EQUAL NUMBER AND expression
		| IDENTIFIER EQUAL STRING AND expression
		| IDENTIFIER LESSTHAN NUMBER AND expression
		| IDENTIFIER GREATERTHAN NUMBER AND expression
		| IDENTIFIER NOTEQUAL STRING AND expression
		| IDENTIFIER NOTEQUAL NUMBER AND expression
		| IDENTIFIER EQUAL NUMBER OR expression
		| IDENTIFIER EQUAL STRING OR expression
		| IDENTIFIER LESSTHAN NUMBER OR expression
		| IDENTIFIER GREATERTHAN NUMBER OR expression
		| IDENTIFIER NOTEQUAL STRING OR expression
		| IDENTIFIER NOTEQUAL NUMBER OR expression
		| IDENTIFIER EQUAL NUMBER 
		| IDENTIFIER EQUAL STRING
		| IDENTIFIER LESSTHAN NUMBER
		| IDENTIFIER GREATERTHAN NUMBER
		| IDENTIFIER NOTEQUAL STRING
		| IDENTIFIER NOTEQUAL NUMBER'''
	
	if (len(p) == 6) :

		global gap
		
		index = len(strings)-gap
		strings.insert(index,p[4])
		strings.insert(index,p[3])
		strings.insert(index,p[2])
		strings.insert(index,p[1])

		gap = gap + 4		

		
	elif (len(p) == 4) :
		strings.append(p[1])
		strings.append(p[2])
		strings.append(p[3])
		
	coLen = len(cols)
	count = 0
	flagp1 = 0
	
	while(count < coLen):
		if(p[1] == cols[count]):
			flagp1 = 1

		count = count + 1
	
	if(flagp1 == 0):
		cols.insert(0,p[1])



def p_update_statement(p):
	'''update_statement : IDENTIFIER SET columns2 where_statement expression
	| IDENTIFIER SET columns2'''
	
	if (len(p) == 6) :
		strings.insert(0,p[2])
		strings.insert(0,p[1])
	else :
		strings.insert(0,p[2])
		strings.insert(0,p[1])


	
def p_columns2(p):
	'''columns2 : IDENTIFIER EQUAL NUMBER COMMA columns2
	| IDENTIFIER EQUAL NUMBER''' 

	if (len(p) == 6) :
		strings.insert(0,p[4])
		strings.insert(0,p[3])
		strings.insert(0,p[2])
		strings.insert(0,p[1])

	elif (len(p) == 4) :
		strings.insert(0,p[3])
		strings.insert(0,p[2])
		strings.insert(0,p[1])

def p_delete_statement(p):
	'''delete_statement : from_statement
	| from_statement where_statement expression'''
	

def p_error(p):
	if p:
		print("   Syntax error at", p.value)
	else:
		print("   Syntax error at EOF")
		

	


myparser = yacc.yacc()
#count = 0

def parse(query):
	global strings
	strings = []
	myparser.parse(query)
	return strings

