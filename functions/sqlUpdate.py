# Evaluates the update statement

import sqlWhere

def update(data,query):
	i = 3											# Start with 4th element in the list
	if("where" in query or "WHERE" in query):		# Check if query contains the where clause
		sqlWhere.sampleStmt.remove("where")
		sqlWhere.processWhereStmt(sampleStmt)
	else:
		while(i < len(query)):						# Modify all rows of the specified column/s
			for j in data[query[1]].keys():
				data[query[1]][j][query[i]] = query[i+2]
			i+=3