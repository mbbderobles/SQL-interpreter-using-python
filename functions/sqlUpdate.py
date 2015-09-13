# Evaluates the update statement

import sqlWhere,sqlUtils,readTable

def update(tb,data,query):
	i = 3																# Starts with 4th element in the list
	if("where" in query or "WHERE" in query):							# Checks if query contains the where clause
		if("where" in query):
			wIndex = query.index('where')
		else:
			wIndex = query.index('WHERE')

		col = query[wIndex+1]
		tbl = sqlUtils.isPrimary(tb,col)
		if(tbl != "false"):
			while(i < wIndex):											# Update 1 row of the specified column/s
				data[tbl][query[wIndex+3]][query[i]] = query[i+2]
				i+=3
	else:
		while(i < len(query)):											# Update ALL rows of the specified column/s
			for j in data[query[1]].keys():
				data[query[1]][j][query[i]] = query[i+2]
			i+=3
