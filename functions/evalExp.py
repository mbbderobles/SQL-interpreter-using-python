import readTable,sqldelete,sqlselect

#query = ['select','*','from','sales_h',',','sales_d'];

def main(query,):
	if(query[0].lower() == "select"):
		sqlselect.evaluate(query[1:],readTable.tb,readTable.data)
	elif(query[0].lower() == "update"):
		update(query)
	else:
		print("delete function here")
		sqldelete.processDelQuery(readTable.data,query)
		#to check print the dictionary for sales_h
		

def update(query):
	i = 3											# Start with 4th element in the list
	if("where" in query or "WHERE" in query):		# Check if query contains the where clause
		print("to be continued...")
	else:
		while(i < len(query)):						# Modify all rows of the specified column/s
			for j in readTable.data[query[1]].keys():
				readTable.data[query[1]][j][query[i]] = query[i+2]
			i+=3

#main(query)
#print()
#query2 = ['select','link_or','register_date','or_no','from','sales_h',',','sales_d']
#main(query2)
