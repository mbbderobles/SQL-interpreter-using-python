# Checks if the tables and columns are valid
def checkSemantics(query,data,tb):
	cols_tb = []
	cols_query = []
	tableName = ""
	error = ""
	if(query[0].lower() == "select"):
		#getColumnsFromMetadata(tableName)
		print("Waley pa")
	elif(query[0].lower() == "update"):
		tableName = query[1]
		error = checkTable(tableName,tb)							# check if table exists
		if(error == False):
			cols_tb = getColumnsFromMetadata(tableName,tb)			# gets list of columns from metadata
			cols_query = getColumnsFromQuery(query,"update")		# gets list of columsn from query
			error = checkColumns(cols_query,cols_tb)				# check if columns exists
			if(error == False and ("where" in query or "WHERE" in query)):
				wIndex = getWhereIndex(query)
				cols_query = getColumnsFromWhereQuery(query[wIndex+1:])
				return (checkColumns(cols_query,cols_tb))			# check if columns in where clause exists
			else:
				return error
		else:
			return error											# error on table name
	elif(query[0].lower() == "delete"):	
		tableName = query[2]
		error = checkTable(tableName,tb)
		if(error == False and ("where" in query or "WHERE" in query)):
			wIndex = getWhereIndex(query)
			cols_tb = getColumnsFromMetadata(tableName,tb)			# gets list of columns from metadata
			cols_query = getColumnsFromWhereQuery(query[wIndex+1:])
			return (checkColumns(cols_query,cols_tb))				# check if columns in where clause exists
		else:
			return error

	else:
		print("Processing query "+ str(query))

# Gets the index of the WHERE keyword
def getWhereIndex(query):
	if("where" in query):
		return(query.index('where'))
	else:
		return(query.index('WHERE'))

# Checks whether the table exists
def checkTable(tableName,tb):
	if(tableName in tb.keys()):
			return False
	return tableName

# Gets the Columns of a table from metadata
def getColumnsFromMetadata(tableName,tb):
	cols_tb = []
	temp = tb[tableName]
	for i in temp.keys():
		cols_tb.append(temp[i][0])		#index zero since 1st element is columnName
	return cols_tb

# Gets the Columns of a table from query
def getColumnsFromQuery(query,statement):
	cols_query = []
	if(statement == "select"):
		print("Waley pa")
	elif(statement == "update"):
		i = 3
		if("where" in query or "WHERE" in query):
			wIndex = getWhereIndex(query)
			while(i < wIndex):
				cols_query.append(query[i])
				i+=4
		else:
			while(i < len(query)):
				cols_query.append(query[i])
				i+=4

	return cols_query

# Gets the Columns of a table from wherequery
def getColumnsFromWhereQuery(query):
	cols_query = []
	i=0
	while(i < len(query)):
		cols_query.append(query[i])
		i+=4
	return cols_query

# Checks whether the columns exist
def checkColumns(cols_query,cols_tb):
	i = 0
	while(i < len(cols_query)):
		if(cols_query[i] not in cols_tb):
			return cols_query[i]
		i += 1

	return False