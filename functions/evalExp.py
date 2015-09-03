import readTable

query = ["UPDATE","sales_h","SET","register_date","=","11/11/2015","cashier_id","=","0000"];

def main():
	if(query[0].lower() == "select"):
		print("select function here")
	elif(query[0].lower() == "update"):
		update(query)
	else:
		print("delete function here")


def update(query):
	i = 3											# Start with 4th element in the list
	if("where" in query or "WHERE" in query):		# Check if query contains the where clause
		print("to be continued...")
	else:
		while(i < len(query)):						# Modify all rows of the specified column/s
			for j in readTable.data[query[1]].keys():
				readTable.data[query[1]][j][query[i]] = query[i+2]
			i+=3

main()
cols = readTable.getColumns("sales_h",readTable.tb)
readTable.printTableRows(readTable.data,"sales_h",cols)