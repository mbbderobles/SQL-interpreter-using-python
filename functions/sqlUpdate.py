# Evaluates the update statement

import sqlUtils
def update(tb,data,query):
	i = 3													# Starts with 4th element in the list
	tbl = query[1]											# Stores the table name to tbl
	if("where" in query or "WHERE" in query):				# Checks if query contains the where clause
		wIndex = sqlUtils.getWhereIndex(query)
		if("AND" in query or "and" in query or "OR" in query or "or" in query):
			print("under construction")
		else:
			if(sqlUtils.isPrimary(tb,tbl,query[wIndex+1])):
				while(i < wIndex):											# Updates 1 row of the specified column/s
					data[tbl][query[wIndex+3]][query[i]] = query[i+2]
					i+=3
			else:
				for j in data[tbl].keys():
					i=3
					if(data[tbl][j][query[wIndex+1]] == query[wIndex+3]):
						while(i < wIndex):
							data[tbl][j][query[i]] = query[i+2]
							i+=3
	else:
		while(i < len(query)):
			for j in data[tbl].keys():
				data[tbl][j][query[i]] = query[i+2]
			i+=3