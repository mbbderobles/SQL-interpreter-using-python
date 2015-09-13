# Collection of extra functions

#desc statement
def descTable(tb,tbl):
	print("==========================================================================================")
	print("\tColumn Name\t\tType\t\tSize\t\tPrimary Key")
	print("==========================================================================================")
	for k in tb[tbl].keys():
		print("%20s%20s%20s%20s " % (tb[tbl][k][0], tb[tbl][k][1], tb[tbl][k][2], tb[tbl][k][3]))
	print("==========================================================================================")
	print()

#checks if the column is a primary key
#return the table name if TRUE, returns false otherwise
def isPrimary(tb,col):
	for k in tb.keys():
		i=0
		if(col == tb[k][i][0]):
			return k
			i = i+1
	return "false";