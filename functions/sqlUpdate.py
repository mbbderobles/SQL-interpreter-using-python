# Evaluates the update statement
import sqlUtils
def update(tb,data,query):
	i = 3													# Starts with 4th element in the list
	tbl = query[1]											# Stores the table name to tbl
	if("where" in query or "WHERE" in query):				# Checks if query contains the WHERE clause
		wIndex = sqlUtils.getWhereIndex(query)
		if("AND" in query or "and" in query or "OR" in query or "or" in query):
			sqlUtils.getKeysFromCond(data,tbl,query[wIndex+1:])
		else:
			if(sqlUtils.isPrimary(tb,tbl,query[wIndex+1])):				# Checks if column is a primary key
				while(i < wIndex):										# Updates 1 row
					data[tbl][query[wIndex+3]][query[i]] = query[i+2]
					i+=4
			else:														# Column is not a primary key
				for j in data[tbl].keys():								# Updates some rows
					i=3
					if(data[tbl][j][query[wIndex+1]] == query[wIndex+3]):
						while(i < wIndex):
							data[tbl][j][query[i]] = query[i+2]
							i+=4
	else:																# No WHERE clause
		while(i < len(query)):											# Updates all rows
			for j in data[tbl].keys():
				data[tbl][j][query[i]] = query[i+2]
			i+=4