# Evaluates the update query

import sqlUtils,sqlWhere

# Processes the update query
# data - stores the table data
# tb - stores the table metadata
# query - contains the update query
def update(data,tb,query):
	tbl = query[1]											# Stores the table name to tbl
	#query = query[3:]										# Remove other elements in the list
	if("where" in query or "WHERE" in query):				# Checks if query contains the WHERE clause
		wIndex = sqlUtils.getWhereIndex(query)				# Gets the index of the WHERE keyword
		pk = sqlWhere.processWhereStmt(tb, tbl, data[tbl], query[wIndex+1:])	# Gets list of rows to be updated
		'''if(not isDuplicateEntry(data,tb,tbl,query[:wIndex],query[wIndex+1:],pk)):
			updateRows(data,tbl,query,pk,wIndex)'''
		print(pk)
		print(str(isDuplicateEntry(data,tb,tbl,query[:wIndex],query[wIndex+1:],pk)))
	else:													# No WHERE clause
		if(not isDuplicateEntry(data,tb,tbl,query,[],[])):
			updateAllRows(data,tbl,query)

# Updates all rows
# data - stores the table data
# tbl - stores the table name
# query - contains the update query
def updateAllRows(data,tbl,query):
	i=0
	while(i < len(query)):
		for j in data[tbl].keys():
			data[tbl][j][query[i]] = query[i+2]
		i+=4

# Updates some rows filtered by the WHERE clause
# data - stores the table data
# tb - stores the table metadata
# tbl - stores the table name
# query - contains the update query with 
# pk - stores the list of rows to be updated
def updateRows(data,tbl,query,pk,wIndex):
	j=0
	while(j < len(pk)):
		i=0
		while(i < wIndex):
			if(sqlUtils.isPrimary(tb,tbl,query[i])):
				print("????")
			else:
				data[tbl][pk[j]][query[i]] = query[i+2]
			i+=4
		j+=1

# Returns true if there is a duplicate entry in the primary key, false otherwise
def isDuplicateEntry(data,tb,tbl,changeList,whereList,pk):
	primaryKey = tb[tbl][0][0]			# Gets the primary key of the table
	
	if(primaryKey not in changeList):	# Checks if primary key is not part of the to be update columns
		return False
	elif(primaryKey in changeList and not whereList):	# Checks if primary key is part of the to be update columns and there's no WHERE clause
		return True
	elif(primaryKey in changeList and whereList):	# Checks if primary key is part of the to be update columns and there's a WHERE clause
		if(len(pk) > 1):							# Checks if there's more than 1 row to be updated
			return True
		elif(len(pk) == 1):							# Checks if there's only 1 row to be updated
			primaryValue1 = changeList[changeList.index(primaryKey) + 2]	# Gets the primary key value
			if(isPrimaryValue(tbl,data,primaryValue1)):						# Checks if primary key value already exists
				if(primaryKey in whereList):								# Checks if primary key is part of condition
					primaryValue2 = whereList[whereList.index(primaryKey) + 2]		# Gets the primary key value
					if(primaryValue1 == primaryValue2):
						return False
					else:
						return True
				else:
					return False
			else:
				return False
		else:						# No rows to be updated
			return False

# Returns true if value of the primary key already exists
def isPrimaryValue(tbl,data,val):
	if(val in data[tbl].keys()):
		return True
	return False