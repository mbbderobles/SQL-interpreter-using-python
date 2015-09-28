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

# Returns a list of primary keys based on the evaluation of conditions
# squery - list containing the conditions in the where clause (WHERE [condition])
def getKeysFromCond(data,tb,tbl,squery):
	pk = []												# Lists all pks that makes the condition true
	for j in data[tbl].keys():
		i=0
		while(i < len(squery)):							# Evaluates all conditions after WHERE clause
			if(isPrimary(tb,tbl,squery[i])):			# Checks if column is primary key
				if(evalCondition(j,squery[i+1],squery[i+2],getType(tb,tbl,j))):
					if(i==0):
						pk.append(j)
					elif(i>0 and squery[i-1].lower()=="or" and j not in pk):
						pk.append(j)
				else:
					if(i>0 and squery[i-1].lower()=="and" and j in pk):
						pk.remove(j)
			else:										# Columns is non-primary key
				if(evalCondition(data[tbl][j][squery[i]],squery[i+1],squery[i+2],getType(tb,tbl,squery[i]))):
					if(i==0):
						pk.append(j)
					elif(i>0 and squery[i-1].lower()=="or" and j not in pk):
						pk.append(j)
				else:
					if(i>0 and squery[i-1].lower()=="and" and j in pk):
						pk.remove(j)
			i+=4
	return pk

# Evaluates condition, returns true or false
def evalCondition(op1,op,op2,dType):
	if(op=="="):
		return (op1==op2)
	elif(op=="<"):
		if(dType == "int"):						# Converts values if needed
			return (int(op1)<int(op2))
		elif(dType == "float"):
			return (float(op1)<float(op2))
		else:
			return (op1<op2)
	elif(op==">"):
		if(dType == "int"):						# Converts values if needed
			return (int(op1)>int(op2))
		elif(dType == "float"):
			return (float(op1)>float(op2))
		else:
			return (op1>op2)
	elif(op=="!="):
		return (op1!=op2)

# Returns the data type of the column
def getType(tb,tbl,col):
	i = 0
	while(i<5):
		if(col == tb[tbl][i][0]):
			return tb[tbl][i][1]
		i+=1