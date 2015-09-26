 # Collection of extra functions

# desc statement
def descTable(tb,tbl):
	print("==========================================================================================")
	print("\tColumn Name\t\tType\t\tSize\t\tPrimary Key")
	print("==========================================================================================")
	for k in tb[tbl].keys():
		print("%20s%20s%20s%20s " % (tb[tbl][k][0], tb[tbl][k][1], tb[tbl][k][2], tb[tbl][k][3]))
	print("==========================================================================================")
	print()

# Checks if the column is a primary key of a table
def isPrimary(tb,tbl,col):
	if(col == tb[tbl][0][0]):
		return True
	return False

# Gets the index of the WHERE keyword
def getWhereIndex(query):
	if("where" in query):
		return(query.index('where'))
	else:
		return(query.index('WHERE'))

# Get primary keys based on the evaluation of conditions
# squery - list containing the conditions in the where clause (WHERE [condition])
def getKeysFromCond(data,tbl,squery):
	pk = []												# Lists all pks that makes the condition true
	for j in data[tbl].keys():
		i=0
		while(i < len(squery)):							# Evaluates all conditions after WHERE clause
			if(data[tbl][j][squery[i]] == squery[i+2]):
				if(i==0):
					pk.append(j)
				elif(i>0 and squery[i-1].lower()=="or" and j not in pk):
					pk.append(j)
			else:
				if(i>0 and squery[i-1].lower()=="and" and j in pk):
					pk.remove(j)
			i+=4
	print(pk)