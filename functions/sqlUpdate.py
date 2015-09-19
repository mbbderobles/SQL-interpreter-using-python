# Evaluates the update statement

import sqlUtils
def update(tb,data,query):
	i = 3													# Starts with 4th element in the list
	if("where" in query or "WHERE" in query):				# Checks if query contains the where clause
		wIndex = getWhereIndex(query)
		if("AND" in query or "and" in query or "OR" in query or "or" in query):
			print("under construction")
		else:
			if(sqlUtils.isPrimary(tb,query[1],query[wIndex+1])):
				while(i < wIndex):											# Update 1 row of the specified column/s
					data[query[1]][query[wIndex+3]][query[i]] = query[i+2]
					i+=3
			'''else:
				for j in data[query[1]].keys():
					if(tb,):
						while(i < len(query)):
							data[query[1]][j][query[i]] = query[i+2]
							i+=3'''
	else:
		while(i < len(query)):
			for j in data[query[1]].keys():
				data[query[1]][j][query[i]] = query[i+2]
			i+=3

def getWhereIndex(query):
	if("where" in query):
		return(query.index('where'))
	else:
		return(query.index('WHERE'))

'''def findColIndex(tb,tbl,col):
	for i in tb[tbl].keys():
		j=0
		tb[tbl][i]'''
