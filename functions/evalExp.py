# Determines the type of statement to evaluate and calls the appropriate function

import readTable,sqlDelete,sqlSelect,sqlUpdate,sqlUtils,time

#query = ['update','sales_h','set','sales_gross_amount','=','12345',',','or_no','=','386-337381','WHERE','or_no','=','386-337380']
#query = ['delete', 'from', 'sales_h', 'where','cashier_id', '=', '622', 'or','customer_id', '=', '0', 'or','or_no','>','386-337338','or','sales_gross_amount','>','50']
#query = ['select','*','from','sales_h'];

def main(query,data,tb):
	start_time = time.time()

	if(query[0].lower() == "select"):									#evaluates select statement
		sqlSelect.evaluate(query[1:],tb,data)
	elif(query[0].lower() == "update"):									#evaluates update statement
		sqlUpdate.update(data,tb,query)
	elif(query[0].lower() == "delete"):	
		sqlDelete.processDelQuery(tb,data,query)					#evaluates delete statement
		
		#to check print the dictionary for sales_h
	else:
		sqlUtils.descTable(tb,query[1])						#evaluates desc statement

	qTime = round(time.time() - start_time, 4)
	print(" (%s sec)" % qTime)

'''
start_time = time.time()
main(query)
qTime = round(time.time() - start_time, 4)
cols = readTable.getColumns("sales_h",readTable.tb)
readTable.printTableRows(readTable.data,"sales_h",cols)
print("(%s sec)" % qTime)
'''
