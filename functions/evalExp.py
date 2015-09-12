# Determines the type of statement to evaluate and calls the appropriate function

import readTable,sqlDelete,sqlSelect,sqlUpdate,sqlUtils

#query = ['select','*','from','sales_h',',','sales_d'];

def main(query):
	if(query[0].lower() == "select"):									#evaluates select statement
		sqlSelect.evaluate(query[1:],readTable.tb,readTable.data)
	elif(query[0].lower() == "update"):									#evaluates update statement
		sqlUpdate.update(readTable.data,query)
	elif(query[0].lower() == "delete"):
		sqlDelete.processDelQuery(readTable.data,query)					#evaluates delete statement
		#to check print the dictionary for sales_h
	else:
		sqlUtils.descTable(query[1])									#evaluates desc statement
