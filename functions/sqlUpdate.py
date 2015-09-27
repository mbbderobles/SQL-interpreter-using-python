# Evaluates the update statement
import sqlUtils
def update(tb,data,query):
	i = 3													# Starts with 4th element in the list
	tbl = query[1]											# Stores the table name to tbl
	if("where" in query or "WHERE" in query):				# Checks if query contains the WHERE clause
		wIndex = sqlUtils.getWhereIndex(query)
		pk = sqlUtils.getKeysFromCond(data,tb,tbl,query[wIndex+1:])	# Gets list of rows to be updated
		j = 0
		while(j < len(pk)):
			i=3
			while(i < wIndex):
				if(sqlUtils.isPrimary(tb,tbl,query[i])):							# Checks for duplicate entry of primary key
					if(query[i+2] not in query[wIndex:] and sqlUtils.isPrimaryValue(tbl,data,query[i+2])):	# or_no=1234 WHERE ...
						print("ERROR: Duplicate entry %s for key 'PRIMARY'" % query[i+2]) 
						j = len(pk)
						break
					elif(query[i+2] in query[wIndex:] and sqlUtils.isPrimaryValue(tbl,data,query[i+2])):
						temp = query[wIndex:].index(query[i+2])
						temp+=wIndex
						if(query[temp-2] == query[i] and query[temp] == query[i+2] and query[i] == "="):	# or_no=1234 WHERE or_no=1234
							print("huhu")
						else:
							print("ERROR: Duplicate entry %s for key 'PRIMARY'" % query[i+2])
							j = len(pk)
							break
					else:																# or_no=1234 WHERE reg_date=1234
						print("huhu")
				else:
					data[tbl][pk[j]][query[i]] = query[i+2]
				i+=4
			j+=1
	else:																# No WHERE clause
		while(i < len(query)):											# Updates all rows
			for j in data[tbl].keys():
				data[tbl][j][query[i]] = query[i+2]
			i+=4