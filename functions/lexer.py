from ply import *	#imports the lex and yacc parser for python
			#make sure to install the PLY module on your PC.
			# TO INSTALL:
			#  - Download the PLY package on the net
			#  - look for the setup.py file
			#  - run the file on your terminal using the command:
			#	python3 setup.py install

# LIST OF TOKENS ############################
tokens = (
	'SELECT',
	'UPDATE',
	'DELETE',
	'FROM',
	'STRING',
	'NUMBER',
	'WHERE',
	'JOIN',
	'ON',
	'COMMA',
	'LESSTHAN',
	'GREATERTHAN',
	'EQUAL',
	'NOTEQUAL',
	'NOT',
	'ASTERISK',
	'SEMICOLON',
	'IDENTIFIER',
	'AND',
	'OR',
	'SET',
	'DESC'
)

# Regular expression for each token ########

t_SELECT = r'SELECT|select'
t_UPDATE = r'UPDATE|update';
t_DELETE = r'DELETE|delete';
t_DESC = r'DESC|desc';
t_FROM = r'FROM|from'
t_STRING = r'("[^"]*")|(\'[^\']*\')'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

t_WHERE = r'WHERE|where';
t_JOIN = r'JOIN|join'
t_ON = r'ON|on'
t_COMMA = r','
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_EQUAL = r'='
t_NOTEQUAL = r'!='
t_NOT = r'!'
t_ASTERISK = r'\*'
t_SEMICOLON = r';'
t_AND = r'AND|and'
t_OR = r'OR|or'
t_SET = r'SET|set'
#t_IDENTIFIER = r'[a-zA-Z_]+[^ \t\n=<,>!\'\";\~]*'
t_IDENTIFIER = r'\b(?:(?!select|update|delete|from|where|join|on|and|or|set|desc|SELECT|UPDATE|DELETE|FROM|WHERE|JOIN|ON|AND|OR|SET|DESC)\w)+[^ \t\n=<,>!\'\";\~]*\b'

t_ignore = ' \t';

#list of errors
errors = []

# If an invalid token was found ############
def t_error(t):
	errors.append(t.value[0])
	t.lexer.skip(1)

symTab = [] #contains all tokens from the user

# !function to be called ###################
# checks if there is an invalid token ######
# returns 1 if there is an invalid token   #
def check(query):
	global errors
	lexer = lex.lex()
	lexer.input(query)
	while True:
		tok = lexer.token()
		if not tok:
			break
#		print(tok)
	if errors: # if there are errors
		temp = errors[0]
		errors = []
		return temp
	else:
		return 0
