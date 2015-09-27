# Determines the type of statement to evaluate and calls the appropriate function

import readTable,sqlDelete,sqlSelect,sqlUpdate,sqlUtils,time

query = ['update','sales_h','set','sales_gross_amount','=','12345',',','customer_id','=','9999',',','or_no','=','386-337380','WHERE','sales_gross_amount','>','200','and','register_date','=','7/16/2015','or','or_no','=','386-337380']
#query = ['delete', 'from', 'sales_h', 'where','cashier_id', '=', '622', 'or','customer_id', '=', '0', 'or','or_no','>','386-337338','or','sales_gross_amount','>','50']

def main(query):
	if(query[0].lower() == "select"):									#evaluates select statement
		sqlSelect.evaluate(query[1:],readTable.tb,readTable.data)
	elif(query[0].lower() == "update"):									#evaluates update statement
		sqlUpdate.update(readTable.tb,readTable.data,query)
	elif(query[0].lower() == "delete"):	
		print("Processing query "+ str(query))
		sqlDelete.processDelQuery(readTable.tb,readTable.data,query)					#evaluates delete statement
		
		#to check print the dictionary for sales_h
	else:
		sqlUtils.descTable(readTable.tb,query[1])						#evaluates desc statement

start_time = time.time()
main(query)
qTime = round(time.time() - start_time, 4)
cols = readTable.getColumns("sales_h",readTable.tb)
readTable.printTableRows(readTable.data,"sales_h",cols)
print("(%s sec)" % qTime)
