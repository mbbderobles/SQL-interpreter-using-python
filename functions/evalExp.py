import readTable,sqldelete,sqlUpdate

#query = ["UPDATE","sales_h","SET","register_date","=","11/11/2015","cashier_id","=","0000"];
query = ["Delete","*", "from", "sales_h"]; #still working on the where expression

def main():
	if(query[0].lower() == "select"):
		print("select function here")
	elif(query[0].lower() == "update"):
		sqlUpdate.update(readTable.data,query)
	else:
		print("delete function here")
		sqldelete.processDelQuery(readTable.data,query)
		#to check print the dictionary for sales_h
		
main()
cols = readTable.getColumns("sales_h",readTable.tb)
readTable.printTableRows(readTable.data,"sales_h",cols)