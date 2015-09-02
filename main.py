
# main.py ########################################
# Main program file
##################################################

import sys, os #for sytem operations

# USER-DEFINED FUNCTIONS #########################
sys.path.insert(0,'./functions/')

# All user-defined libraries (.py) must be placed in the functions folder.
# If the python file will be used here, import it below:
import lexer, parser 

# start ##########################################

query = ''
tokens = [] #list of tokens
os.system('clear')

while True:
	query = input(" group1sql>> ") #get query
	if query == 'exit': #exits the db
		break
	elif query == 'clear': #clears the screen
		os.system('clear')
	elif query[-1] != ';':
		print("   ERROR: Invalid syntax")
	else:
		#parse.check returns the first invalid token (if any)
		error = lexer.check(query)
		if(error): #check if there are no invalid tokens
			print("   ERROR: Invalid token near", error)
		else:
			print('   All tokens valid')
			tokens = parser.parse(query)
			if len(tokens) !=0: #the query is valid
				print("   Syntax is valid")
			else:
				print("   Syntax is invalid")
 		#if correct:
			#start query optimization and evaluation


# end of file ####################################
