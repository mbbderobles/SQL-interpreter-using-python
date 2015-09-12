import readTable,sqldelete,sqlSelect,sqlUpdate

#query = ['select','*','from','sales_h',',','sales_d'];

def main(query,):
	if(query[0].lower() == "select"):
		sqlselect.evaluate(query[1:],readTable.tb,readTable.data)
	elif(query[0].lower() == "update"):
		sqlUpdate.update(readTable.data,query)
	else:
		print("delete function here")
		sqldelete.processDelQuery(readTable.data,query)
		#to check print the dictionary for sales_h
		
main()
cols = readTable.getColumns("sales_h",readTable.tb)
readTable.printTableRows(readTable.data,"sales_h",cols)
