
tb = {}
data = {}

''' START OF UTILITY FUNCTIONS HERE '''

def checkTable(table):
	if(table in tb.keys()):
		return True
	else:
		print('table \''+str(table)+'\' does not exist.')
		return False

''' +++ GET COLUMNS FROM METADATA '''
def getColumns(tableName):
	cols = []
	temp = tb[tableName]
	for i in temp.keys():
		cols.append(temp[i][0]) #sub zero since 1st element is columnName
	return cols

''' +++ GET COLUMNS FROM TO PRINT FROM THE QUERY '''
def getColsToPrint(tokens,join):
	cols = []
	#if select all
	if(tokens[0]=='*'):
		tokens.pop(0)
		tokens.pop(0)
		#if not join
		if not join:
			cols = getColumns(tokens[0])
		#if join
		else:
			i = 0;
			while i<len(tokens):
				if(tokens[i]!=','):
					if(tokens[i-1]==',' or i==0):
						if(checkTable(tokens[i])):
							cols.extend(getColumns(tokens[i]))
						else:
							return False,tokens
				i = i+1
	#if rows are in query
	else:
		i = tokens.pop(0)
		temp = []
		while(i.lower()!='from'):
			if(i.lower() == 'from'):
				break;
			elif(i==','):
				if(len(temp)==1):
					cols.append(temp[0])
				else:
					cols.append(temp[2])
				temp = []
			else:
				temp.append(i)
			i = tokens.pop(0)
		if(len(temp)==1):
			cols.append(temp[0])
		else:
			cols.append(temp[2])
	return cols,tokens #returns columns and the remaining tokens

''' gets the PK of a certain table '''
def getTablePK(tableName):
	return tb[tableName][0][0];
	
''' check if the query is cross product '''
def isCrossProduct(index,length):
	if(length-index > 2):
		return True
	else:
		return False

''' checks if the column is a PK '''
def isPK(tableName,column):
	if(tb[tableName][0][0] == column):
		return True
	else:
		return False

''' gets the tables from the query '''
def getTables(tokens,ext):
	tbl = [];
	i=0
	leng = 0
	#gets the list of tables in the query if it has JOIN or WHERE
	if(ext=="on"):
		leng = tokens.index('on')
	elif(ext=="where"):
		leng = tokens.index('where')
	else:
		leng = len(tokens)
	while(i<leng):
		if(tokens[i]!=','):
			tbl.append(tokens[i])
		i+=1
	return tbl,tokens[i:]

''' gets the table of the given column '''
def getTableOfCol(col):
	for tblName in tb.keys():
		for colIndex in tb[tblName].keys():
			if(tb[tblName][colIndex][0]==col):
				return tblName

def getSize(i):
	tbl = getTableOfCol(i)
	for j in range(0,len(tb[tbl].keys())):
		if(tb[tbl][j][1]=="date"):
			return 15
		if(tb[tbl][j][0]==i):
			return int(tb[tbl][j][2])

def tabulate(printData,headers):
	sizes = []
	size = 0
	for i in headers:
		x = getSize(i)
		if(len(i)>=x):
			sizes.append(len(i)+2)
			x = len(i)+2
		else:
			sizes.append(x)
		size += x

	#print(size)

	size += (3*len(sizes))+3
	pluss = '+'*size

	print(pluss)

	count = 0
	#print(headers)
	#print(sizes)
	for i in headers:
		print("|  {}".format(str(i).ljust(sizes[count])), end="")
		count += 1
	print('  |')

	print(pluss)

	for i in printData:
		count = 0
		for j in i:
			print("|  {}".format(str(j).ljust(sizes[count])), end="")
			count+=1
		print('  |')
	print(pluss)

# +++ TYPE FUNCTIONS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
''' gets the type of a variable or constant '''
def getType(var):
	if(len(var)>1):
		for i in tb[var[0]].keys():
			if(tb[var[0]][i][0] == var[2]):
				return tb[var[0]][i][1]
		else:
			print("unknown column","'"+var[2]+"'","in table",var[0])
			return False
	else:
		if(type(var[0]) == float):
			return 'float';
		elif(type(var[0]) == int):
			return 'int'
		elif(var[0].isdigit()):
			return 'int'
		else:
			return 'varchar'

''' checks if two clauses are type compatible '''
def typeCompatible(var1,var2):
	type1 = getType(var1)
	if(type1):
		type2 = getType(var2)
		if(type2):
			if(type1==type2):
				return True,type1,type2
			else:
				if(type1=='varchar' and type2=='date'):
					return True,'varchar','date'
				elif(type2=='varchar' and type1=='date'):
					return True,'date','varchar'
				else:
					print(type1,'is not compatible with',type2)
					return False,type1,type2
		else:
			return False,type1,type2
	else:
		return False,type1,''

def getNearest(var):
	nearest = -1
	if('on' in var):
		nearest = var.index('on')
	if('and' in var):
		if(nearest==-1 or nearest>var.index('and')):
			nearest = var.index('and')
	if('or' in var):
		if(nearest==-1 or nearest>var.index('or')):
			nearest = var.index('or')
	return nearest

def greaterThanDate(date1,date2):
	if(date1[0]=='"' or date1[0]=="'"):
		date1 = date1[1:len(date1)-1];
	if(date2[0]=='"' or date2[0]=="'"):
		date2 = date2[1:len(date2)-1];
		
	d1 = date1.split('/')
	d2 = date2.split('/')

	if(len(d1)==3 and len(d2)==3):
		if(d1[2].isdigit() and d2[2].isdigit()):
			if(int(d1[2])>int(d2[2])):
				return True
			elif(int(d1[2])==int(d2[2])):
				if(d1[0].isdigit() and d2[0].isdigit()):
					if(int(d1[0])>int(d2[0])):
						return True
					elif(int(d1[0])==int(d2[0])):
						if(d1[1].isdigit() and d2[1].isdigit()):
							if(int(d1[1])>int(d2[1])):
								return True
							else:
								return False
					else:
						return False
			else:
				return False
	return False
	
def lessThanDate(date1,date2):
	if(date1[0]=='"' or date1[0]=="'"):
		date1 = date1[1:len(date1)-1];
	if(date2[0]=='"' or date2[0]=="'"):
		date2 = date2[1:len(date2)-1];

	d1 = date1.split('/')
	d2 = date2.split('/')
	
	if(len(d1)==3 and len(d2)==3):
		if(d1[2].isdigit() and d2[2].isdigit()):
			if(int(d1[2])<int(d2[2])):
				return True
			elif(int(d1[2])==int(d2[2])):
				if(d1[0].isdigit() and d2[0].isdigit()):
					if(int(d1[0])<int(d2[0])):
						return True
					elif(int(d1[0])==int(d2[0])):
						if(d1[1].isdigit() and d2[1].isdigit()):
							if(int(d1[1])<int(d2[1])):
								return True
							else:
								return False
					else:
						return False
			else:
				return False
	return False

# +++ JOIN ONLY FUNCTIONS ++++++++++++++++++++++++++++++++++++++++++++++++++++++

''' gets the tables for the join operation '''
def getJoinTables(tokens):
	tbl = [tokens.pop(0)];
	#gets the list of tables in the query if it has JOIN or WHERE
	
	while(',' in tokens):
		tbl.append(tokens.pop(tokens.index(',')+1))
		tokens.pop(tokens.index(','))
	
	return tbl,tokens

''' evaluates the joined tables given A condition '''
def evaluateJoinWithOnTwo(var1,sign,var2,tables,result):
	comp,t1,t2 = typeCompatible(var1,var2)
	if(comp): #if compatible
		data1 = []
		data2 = []
		#if equality
		if(sign=='='):
			var1PK = isPK(var1[0],var1[2])
			var2PK = isPK(var2[0],var2[2])
			
			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				for k in data[var2[0]].keys():
					if(var1PK and var2PK):	#if both PK
						if(j==k):
							data1.append(j)
							data2.append(k)
					elif(var1PK):	#if first is PK
						if(j==data[var2[0]][k][var2[2]]):
							data1.append(j)
							data2.append(k)
					elif(var2PK):	#if second is PK
						if(data[var1[0]][j][var1[2]]==k):
							data1.append(j)
							data2.append(k)
					else:	#if both are not PK
						if(data[var2[0]][j][var2[2]]==data[var1[0]][k][var1[2]]):
							data1.append(j)
							data2.append(k)
		elif(sign=='<'):
			if(t1=='date' or t2=='date'):
				var1PK = isPK(var1[0],var1[2])
				var2PK = isPK(var2[0],var2[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					for k in data[var2[0]].keys():
						if(var1PK and var2PK):	#if both PK
							if(lessThanDate(j,k)):
								data1.append(j)
								data2.append(k)
						elif(var1PK):	#if first is PK
							if(lessThanDate(j,data[var2[0]][k][var2[2]])):
								data1.append(j)
								data2.append(k)
						elif(var2PK):	#if second is PK
							if(lessThanDate(data[var1[0]][j][var1[2]],k)):
								data1.append(j)
								data2.append(k)
						else:	#if both are not PK
							if(lessThanDate(data[var2[0]][j][var2[2]],data[var1[0]][k][var1[2]])):
								data1.append(j)
								data2.append(k)
			elif(t1!='varchar'):
				var1PK = isPK(var1[0],var1[2])
				var2PK = isPK(var2[0],var2[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					for k in data[var2[0]].keys():
						if(var1PK and var2PK):	#if both PK
							if(float(j)<float(k)):
								data1.append(j)
								data2.append(k)
						elif(var1PK):	#if first is PK
							if(float(j)<float(data[var2[0]][k][var2[2]])):
								data1.append(j)
								data2.append(k)
						elif(var2PK):	#if second is PK
							if(float(data[var1[0]][j][var1[2]])<float(k)):
								data1.append(j)
								data2.append(k)
						else:	#if both are not PK
							if(float(data[var2[0]][j][var2[2]])<float(data[var1[0]][k][var1[2]])):
								data1.append(j)
								data2.append(k)
			else:
				print('< cannot be used on type varchar')
		elif(sign=='>'):
			#print('greater than')
			if(t1=='date' or t2=='date'):
				var1PK = isPK(var1[0],var1[2])
				var2PK = isPK(var2[0],var2[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					for k in data[var2[0]].keys():
						if(var1PK and var2PK):	#if both PK
							if(greaterThanDate(j,k)):
								data1.append(j)
								data2.append(k)
						elif(var1PK):	#if first is PK
							if(greaterThanDate(j,data[var2[0]][k][var2[2]])):
								data1.append(j)
								data2.append(k)
						elif(var2PK):	#if second is PK
							if(greaterThanDate(data[var1[0]][j][var1[2]],k)):
								data1.append(j)
								data2.append(k)
						else:	#if both are not PK
							if(greaterThanDate(data[var2[0]][j][var2[2]],data[var1[0]][k][var1[2]])):
								data1.append(j)
								data2.append(k)
			elif(t1!='varchar'):
				var1PK = isPK(var1[0],var1[2])
				var2PK = isPK(var2[0],var2[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					for k in data[var2[0]].keys():
						if(var1PK and var2PK):	#if both PK
							if(float(j)>float(k)):
								data1.append(j)
								data2.append(k)
						elif(var1PK):	#if first is PK
							if(float(j)>float(data[var2[0]][k][var2[2]])):
								data1.append(j)
								data2.append(k)
						elif(var2PK):	#if second is PK
							if(float(data[var1[0]][j][var1[2]])>float(k)):
								data1.append(j)
								data2.append(k)
						else:	#if both are not PK
							if(float(data[var2[0]][j][var2[2]])>float(data[var1[0]][k][var1[2]])):
								data1.append(j)
								data2.append(k)
			else:
				print('< cannot be used on type varchar')
		elif(sign=='!='):
			#print('not equal')
			var1PK = isPK(var1[0],var1[2])
			var2PK = isPK(var2[0],var2[2])
		
			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				for k in data[var2[0]].keys():
					if(var1PK and var2PK):	#if both PK
						if(str(j)!=str(k)):
							data1.append(j)
							data2.append(k)
					elif(var1PK):	#if first is PK
						if(str(j)!=str(data[var2[0]][k][var2[2]])):
							data1.append(j)
							data2.append(k)
					elif(var2PK):	#if second is PK
						if(str(data[var1[0]][j][var1[2]])!=str(k)):
							data1.append(j)
							data2.append(k)
					else:	#if both are not PK
						if(str(data[var2[0]][j][var2[2]])!=str(data[var1[0]][k][var1[2]])):
							data1.append(j)
							data2.append(k)
		
		return data1,data2 #PKs of 1st table, 2nd table
	else:
		return [],[]

def evaluateJoinWithOnOneRight(var1,sign,var2,tables,result): #right is single
	comp,t1,t2 = typeCompatible(var1,var2)
	if(comp): #if compatible
		data1 = []
		#if equality
		if(sign=='='):
			var1PK = isPK(var1[0],var1[2])

			if(type(var2[0])==str):
				if(var2[0][0]=='\"' or var2[0][0]=="'"):
					var2[0] = var2[0][1:len(var2[0])-1]

			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				if(var1PK):	#if first is PK
					if(str(j)==str(var2[0])):
						data1.append(j)
				else:	#if both are not PK
					if(str(data[var1[0]][j][var1[2]])==str(var2[0])):
						data1.append(j)
			#print(data1)
		elif(sign=='<'):
			#print('less than')
			if(t1=='date' or t2=='date'):
				var1PK = isPK(var1[0],var1[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					if(var1PK):	#if first is PK
						if(lessThanDate(j,var2[0])):
							data1.append(j)
					else:	#if both are not PK
						if(lessThanDate(data[var1[0]][j][var1[2]],var2[0])):
							data1.append(j)
			elif(t1!='varchar'):
				var1PK = isPK(var1[0],var1[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					if(var1PK):	#if first is PK
						if(float(j)<float(var2[0])):
							data1.append(j)
					else:	#if both are not PK
						if(float(data[var1[0]][j][var1[2]])<float(var2[0])):
							data1.append(j)
			else:
				print('< cannot be used on type varchar')
		elif(sign=='>'):
			#print('greater than')
			if(t1=='date' or t2=='date'):
				var1PK = isPK(var1[0],var1[2])
				
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					if(var1PK):	#if first is PK
						if(greaterThanDate(j,var2[0])):
							data1.append(j)
					else:	#if both are not PK
						if(greaterThanDate(data[var1[0]][j][var1[2]],var2[0])):
							data1.append(j)
			elif(t1!='varchar'):
				var1PK = isPK(var1[0],var1[2])
				
				# ++ GETTING THE PK's of the matching data
				for j in data[var1[0]].keys():
					if(var1PK):	#if first is PK
						if(float(j)>float(var2[0])):
							data1.append(j)
					else:	#if both are not PK
						if(float(data[var1[0]][j][var1[2]])>float(var2[0])):
							data1.append(j)
			else:
				print('< cannot be used on type varchar')
		elif(sign=='!='):
			#print('not equal')
			var1PK = isPK(var1[0],var1[2])
			
			#print(var2)
			if(type(var2[0])==str):
				if(var2[0][0]=='\"' or var2[0][0]=="'"):
					var2[0] = var2[0][1:len(var2[0])-1]
			#print(var2)
			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				if(var1PK):	#if first is PK
					if(str(j)!=str(var2[0])):
						data1.append(j)
				else:	#if both are not PK
					if(str(data[var1[0]][j][var1[2]])!=str(var2[0])):
						data1.append(j)
		return data1 #PKs of 1st table, 2nd table
	else:
		return []

def evaluateJoinWithOnOneLeft(var1,sign,var2,tables,result): #left is single
	comp,t1,t2 = typeCompatible(var1,var2)
	if(comp): #if compatible
		data1 = []
		#if equality
		if(sign=='='):
			var2PK = isPK(var2[0],var2[2])
			if(type(var1[0])==str):
				if(var1[0][0]=='\"' or var1[0][0]=="'"):
					var1[0] = var1[0][1:len(var1[0])-1]
			
			# ++ GETTING THE PK's of the matching data
			for j in data[var2[0]].keys():
				if(var2PK):	#if first is PK
					if(str(j)==str(var1[0])):
						data1.append(j)
				else:	#if both are not PK
					if(str(data[var2[0]][j][var2[2]])==str(var1[0])):
						data1.append(j)
		elif(sign=='<'):
			#print('less than')
			if(t1=='date' or t2=='date'):
				var2PK = isPK(var2[0],var2[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var2[0]].keys():
					if(var2PK):	#if first is PK
						if(lessThanDate(var1[0],j)):
							data1.append(j)
					else:	#if both are not PK
						if(lessThanDate(var1[0],data[var2[0]][j][var2[2]])):
							data1.append(j)
			elif(t1!='varchar'):
				var2PK = isPK(var2[0],var2[2])
			
				# ++ GETTING THE PK's of the matching data
				for j in data[var2[0]].keys():
					if(var2PK):	#if first is PK
						if(float(var1[0])<float(j)):
							data1.append(j)
					else:	#if both are not PK
						if(float(var1[0])<float(data[var2[0]][j][var2[2]])):
							data1.append(j)
			else:
				print('< cannot be used on type varchar')
		elif(sign=='>'):
			#print('greater than')
			if(t1=='date' or t2=='date'):
				var2PK = isPK(var2[0],var2[2])
				
				# ++ GETTING THE PK's of the matching data
				for j in data[var2[0]].keys():
					if(var2PK):	#if first is PK
						if(greaterThanDate(var1[0],j)):
							data1.append(j)
					else:	#if both are not PK
						if(greaterThanDate(var1[0],data[var2[0]][j][var2[2]])):
							data1.append(j)
			elif(t1!='varchar'):
				var2PK = isPK(var2[0],var2[2])
				
				# ++ GETTING THE PK's of the matching data
				for j in data[var2[0]].keys():
					if(var2PK):	#if first is PK
						if(float(var1[0])>float(j)):
							data1.append(j)
					else:	#if both are not PK
						if(float(var1[0])>float(data[var2[0]][j][var2[2]])):
							data1.append(j)
			else:
				print('< cannot be used on type varchar')
		elif(sign=='!='):
			#print('not equal')
			var2PK = isPK(var2[0],var2[2])
			if(type(var1[0])==str):
				if(var1[0][0]=='\"' or var1[0][0]=="'"):
					var1[0] = var1[0][1:len(var1[0])-1]
			
			# ++ GETTING THE PK's of the matching data
			for j in data[var2[0]].keys():
				if(var2PK):	#if first is PK
					if(str(j)!=str(var1[0])):
						data1.append(j)
				else:	#if both are not PK
					if(str(data[var2[0]][j][var2[2]])!=str(var1[0])):
						data1.append(j)
		
		return data1 #PKs of 1st table, 2nd table
	else:
		return []

''' gets the joined tables of all tables in the join query '''
def joinTables(tables):
	numRows = 1
	maxRows = 0
	result = []
	for i in tables:
		numRows *= len(data[i].keys())
		if len(data[i].keys()) > maxRows:
			maxRows = len(data[i].keys())
	#print("result rows: ",numRows)
	#print("biggest num rows: ",maxRows)

	result = []
	#create list
	for i in range(0,numRows):
		result.append([])

	it = 0
	for tbl in tables:
		counter=0;
		if(it==0):
			it = numRows//len(data[tbl].keys())
		else:
			it = it//len(data[tbl].keys())
		while counter<numRows:
			for k in data[tbl].keys():
				i = 0
				while(i<it):
					result[counter].append(k)
					counter += 1
					i+=1
	
	return result

''' removes the rows that did not satisfy the query '''
def filterTwoVar(temp1,temp2,var1tbl,var2tbl,tables,result):
	if(var1tbl in tables):
		in1 = tables.index(var1tbl)
	else:
		print('table',var1tbl,'was not selected')
		return False
	if(var2tbl in tables):
		in2 = tables.index(var2tbl)
	else:
		print('table',var2tbl,'was not selected')
		return False

	j = 0
	while j<len(result):
		i=0
		flag = False
		while(i<len(temp1) and i<len(temp2)):
			if(result[j][in1]==temp1[i] and result[j][in2]==temp2[i]):
				flag = True
				break
			i+=1
		if(not flag):
			result.pop(j)
		else:
			j+=1

#	print("After:")
#	for i in result:
#		print(i)
	return result

''' removes the rows that did not satisfy the query '''
def filterOneVar(temp1,var1tbl,tables,result):
	if(var1tbl in tables):
		in1 = tables.index(var1tbl)
	else:
		print('table',var1tbl,'was not selected')
		return False

	j = 0
	while j<len(result):
		i=0
		flag = False
		while(i<len(temp1)):
			if(result[j][in1]==temp1[i]):
				flag = True
				break
			i+=1
		if(not flag):
			result.pop(j)
		else:
			j+=1
	#print(result)
#	print("After:")
#	for i in result:
#		print(i)
	return result

''' gets the column(s) stated in the query from the filtered primary keys '''
def getColsFromKeys(cols,result,tables):
	
	printData = []
	
	for i in range(0,len(result)):
		printData.append([])
	
	for col in cols:
		counter=0;
		tbl = getTableOfCol(col)
		if(tbl):
			ind = tables.index(tbl)
			for k in result:
				if(col==getTablePK(tbl)):
					printData[counter].append(k[ind])
				else:
					printData[counter].append(data[tbl][k[ind]][col])
				counter += 1
		else:
			print('column',"'"+col+"'",'not in selected tables')
			return False

	return printData

def intersect(left,right):
	data = []
	
	i=0
	if(len(left)<len(right)):
		while(i<len(left)):
			if(left[i] in right):
				data.append(left[i])
			i+=1
	else:
		while(i<len(right)):
			if(right[i] in left):
				data.append(right[i])
			i+=1
			
	return data

def union(left,right):
	data = []
	
	i=0
	while(i<len(left)):
		if(left[i] not in data):
			data.append(left[i])
		i+=1
	i=0
	while(i<len(right)):
		if(right[i] not in data):
			data.append(right[i])
		i+=1

	return data

def evalAndOr(temp):
	#print('x:',temp)
	while('and' in temp):
		ind = temp.index('and')
		left = temp[ind-1]
		right = temp[ind+1]
		temp[ind] = intersect(left,right)
#		print(len(temp[ind]))
		temp.pop(ind+1)
		temp.pop(ind-1)
	
	while('or' in temp):
		ind = temp.index('or')
		left = temp[ind-1]
		right = temp[ind+1]
		temp[ind] = union(left,right)
#		print(len(temp[ind]))
		temp.pop(ind+1)
		temp.pop(ind-1)		
	return temp

def evaluateWhere(result,tables,tokens):
	temp = []
	nextCond = ''
	#print(result)
	while(len(tokens)!=0):
		tokens = tokens[1:]
		signIndex = -1
		if('<' in tokens):
			signIndex = tokens.index('<')
		if('>' in tokens):
			if(signIndex>tokens.index('>') or signIndex==-1):
				signIndex = tokens.index('>')
		if('=' in tokens):
			if(signIndex>tokens.index('=') or signIndex==-1):
				signIndex = tokens.index('=')
		if('!=' in tokens):
			if(signIndex>tokens.index('!=') or signIndex==-1):
				signIndex = tokens.index('!=')
		
		sign = tokens[signIndex]
		var1 = tokens[0:signIndex]
		var2 = tokens[signIndex+1:]
		
		if('on' in var2 or 'and' in var2 or 'or' in var2):
			nearest = getNearest(var2)
			tokens = var2[nearest:]
			var2 = var2[:nearest]
			nextCond = tokens[0]
		#elif and in var2 and or in var2
		else:
			tokens = []

		if(len(var1)>1 and len(var2)>1):
			#print('both side')
			temp1,temp2 = evaluateJoinWithOnTwo(var1,sign,var2,tables,result)
			x = filterTwoVar(temp1,temp2,var1[0],var2[0],tables,result.copy())
			if(x!=False):
				temp.append(x)
			else:
				return False
		elif(len(var1)>1):
			#print('right side single')
			temp1 = evaluateJoinWithOnOneRight(var1,sign,var2,tables,result)
			x = filterOneVar(temp1,var1[0],tables,result.copy())
			if(x!=False):
				temp.append(x)
			else:
				return False
		elif(len(var2)>1):
			#print('left side single')
			temp1 = evaluateJoinWithOnOneLeft(var1,sign,var2,tables,result)
			x = filterOneVar(temp1,var2[0],tables,result.copy())
			if(x!=False):
				temp.append(x)
			else:
				return False
		else:
			print('both side single')
		cond = nextCond
		if(len(tokens)!=0):
			temp.append(cond)
	
	#print('temp',temp)
	#print('before evalAndOr:',temp)
	result = evalAndOr(temp)
	return result
	
# + END OF UTILITY FUNCTIONS +++++++++++++++++++++++++++++++++++++++++++++++++++

''' START OF QUERY FUNCTIONS HERE '''
# ++++ JOIN STATEMENT WITH ON ++++++++++++++++++++++++++++++++++++++++++++++++++
def joinWithOn(tokens):
	cols,tokens = getColsToPrint(tokens,True);
	if(cols):
		tables,tokens = getJoinTables(tokens)
		result = joinTables(tables)
		
		temp = []
		nextCond = ''
		while(len(tokens)!=0):
	#		print(tokens)
			tokens = tokens[1:]
			signIndex = -1
			if('<' in tokens):
				signIndex = tokens.index('<')
			if('>' in tokens):
				if(signIndex>tokens.index('>') or signIndex==-1):
					signIndex = tokens.index('>')
			if('=' in tokens):
				if(signIndex>tokens.index('=') or signIndex==-1):
					signIndex = tokens.index('=')
			if('!=' in tokens):
				if(signIndex>tokens.index('!=') or signIndex==-1):
					signIndex = tokens.index('!=')

			sign = tokens[signIndex]
			var1 = tokens[0:signIndex]
			var2 = tokens[signIndex+1:]

			if('on' in var2 or 'and' in var2 or 'or' in var2):
				nearest = getNearest(var2)
				tokens = var2[nearest:]
				var2 = var2[:nearest]
				nextCond = tokens[0]
			#elif and in var2 and or in var2
			else:
				tokens = []

	#		print('var1',var1)
	#		print('var2',var2)
	#		print('toks',tokens)
	#		break

			if(len(var1)>1 and len(var2)>1):
				#print('both side')
				temp1,temp2 = evaluateJoinWithOnTwo(var1,sign,var2,tables,result)
				#print(temp1)
				#print(temp2)
				x = filterTwoVar(temp1,temp2,var1[0],var2[0],tables,result.copy())
				if(x!=False):
					temp.append(x)
				else:
					return False
			elif(len(var1)>1):
				#print('right side single')
				temp1 = evaluateJoinWithOnOneRight(var1,sign,var2,tables,result)
				#print(temp1)
				x = filterOneVar(temp1,var1[0],tables,result.copy())
				if(x!=False):
					temp.append(x)
				else:
					return False
			elif(len(var2)>1):
				#print('left side single')
				temp1 = evaluateJoinWithOnOneLeft(var1,sign,var2,tables,result)
				x = filterOneVar(temp1,var2[0],tables,result.copy())
				if(x!=False):
					temp.append(x)
				else:
					return False
			else:
				print('both side single')
			cond = nextCond
			if(len(tokens)!=0):
				temp.append(cond)
		
		temp = evalAndOr(temp)
		result = getColsFromKeys(cols,temp[0],tables)
		
		return result,cols
	return False,cols
	#check if it has more than one condition
#	print("Columns: ",cols)	
#	print("Tables: ",tables)
#	print("Tokens: ",tokens)
		
# ++++ CROSS PRODUCT AND JOIN STATEMENT WITHOUT ON CLAUSE ++++++++++++++++++++++
def joinWithoutOn(tokens):
	#get columns and tokens to print
	cols,tokens = getColsToPrint(tokens,True);
	if(cols):
		tables,tokens = getTables(tokens,'none')

		#populate list (per column)
		printData = joinTables(tables)
		result = getColsFromKeys(cols,printData,tables)	
		#printData
		return result,cols
	return False,cols

# ++++ CROSS PRODUCT AND JOIN STATEMENT WITHOUT ON CLAUSE ++++++++++++++++++++++
def joinWithWhereWithoutOn(tokens,where):
	#get columns and tokens to print
	cols,tokens = getColsToPrint(tokens,True);
	if(cols):
		tables,tokens = getTables(tokens,'none')

		result = joinTables(tables)
		result = evaluateWhere(result,tables,where)
		if(result!=False):
			#print('jwow',result)
			result = getColsFromKeys(cols,result[0],tables)
		
		#printData
		return result,cols
	return False,cols

# ++++ JOIN WITH WHERE WITH ON STATEMENT +++++++++++++++++++++++++++++++++++++++++++++++
def joinWithWhereWithOn(tokens,where):
	cols,tokens = getColsToPrint(tokens,True);
	if(cols):
		tables,tokens = getJoinTables(tokens)
		result = joinTables(tables)
		temp = []
		nextCond = ''
		while(len(tokens)!=0):
	#		print(tokens)
			tokens = tokens[1:]
			signIndex = -1
			if('<' in tokens):
				signIndex = tokens.index('<')
			if('>' in tokens):
				if(signIndex>tokens.index('>') or signIndex==-1):
					signIndex = tokens.index('>')
			if('=' in tokens):
				if(signIndex>tokens.index('=') or signIndex==-1):
					signIndex = tokens.index('=')
			if('!=' in tokens):
				if(signIndex>tokens.index('!=') or signIndex==-1):
					signIndex = tokens.index('!=')

			sign = tokens[signIndex]
			var1 = tokens[0:signIndex]
			var2 = tokens[signIndex+1:]

			if('on' in var2 or 'and' in var2 or 'or' in var2):
				nearest = getNearest(var2)
				tokens = var2[nearest:]
				var2 = var2[:nearest]
				nextCond = tokens[0]
			#elif and in var2 and or in var2
			else:
				tokens = []

	#		print('var1',var1)
	#		print('var2',var2)
	#		print('toks',tokens)
	#		break

			if(len(var1)>1 and len(var2)>1):
				#print('both side')
				temp1,temp2 = evaluateJoinWithOnTwo(var1,sign,var2,tables,result)
				#print('t1',temp1)
				#print('t2',temp2)
				x = filterTwoVar(temp1,temp2,var1[0],var2[0],tables,result.copy())
				if(x!=False):
					temp.append(x)
				else:
					return False
			elif(len(var1)>1):
				#print('right side single')
				temp1 = evaluateJoinWithOnOneRight(var1,sign,var2,tables,result)
				x = filterOneVar(temp1,var1[0],tables,result.copy())
				if(x!=False):
					temp.append(x)
				else:
					return False
			elif(len(var2)>1):
				#print('left side single')
				temp1 = evaluateJoinWithOnOneLeft(var1,sign,var2,tables,result)
				x = filterOneVar(temp1,var2[0],tables,result.copy())
				if(x!=False):
					temp.append(x)
				else:
					return False
			else:
				print('both side single')
			cond = nextCond
			if(len(tokens)!=0):
				temp.append(cond)
		
		#print('before on: ',temp)
		temp = evalAndOr(temp)
		#print('after on: ',temp)
		result = evaluateWhere(temp[0],tables,where)
		if(result!=False):
			#print('after where: ',result)
			result = getColsFromKeys(cols,result[0],tables)	
		
		return result,cols
	return False,cols
	#check if it has more than one condition
#	print("Columns: ",cols)	
#	print("Tables: ",tables)
#	print("Tokens: ",tokens)

def replaceAll(what,tokens):
	for li in what:
		new = []
		for j in tokens:
			if(type(j)==str):
				j = j.replace(li[0],li[1])
			new.append(j)
		tokens = new
	return tokens

# ++++ SIMPLEST SELECT STATEMENT +++++++++++++++++++++++++++++++++++++++++++++++
def normalSelect(tokens):
	cols,tokens = getColsToPrint(tokens,'False');

	if(cols):
		tables = tokens.pop(0)
		printData = []
		pK = getTablePK(tables)
		counter = 0
		for i in data[tables].keys():
			temp = []
			counter += 1
			for col in cols:
				if(col==pK):
					temp.append(i)
				else:
					temp.append(data[tables][i][col])
			printData.append(temp)
		
		return printData,cols
	return False,cols

def normalSelectWhere(tokens,where):
	cols,tokens = getColsToPrint(tokens,'False');
	#print(cols,tokens)
	if(cols):
		tables = tokens.pop(0)

		printData = []
		for i in data[tables].keys():
			printData.append([i])
		
		result = evaluateWhere(printData,tables,where)
		if(result!=False):
			result = getColsFromKeys(cols,result[0],tables)	
		return result,cols
	return False,cols

def joinWithoutOnWhere(tokens,where):
	cols,tokens = getColsToPrint(tokens,'False');
	if(cols):
		tables,tokens = getTables(tokens,'none')

		#populate list (per column)
		printData = joinTables(tables)
		result = evaluateWhere(printData,tables,where)
		if(result!=False):
			#print('jwow',result)
			result = getColsFromKeys(cols,result[0],tables)	

		return result,cols
	return False,cols

# ++++ MAIN FUNCTION +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def evaluate(tokens,tables,rows):
	global tb
	global data
	tb = tables
	data = rows
	#print(tokens)
	if ('where' in tokens or 'WHERE' in tokens) and ('join' in tokens or 'JOIN' in tokens): #can also have where+join-on here
		idex = 0
		if('where' in tokens):
			idex = tokens.index('where')
		elif('WHERE' in tokens):
			idex = tokens.index('WHERE')
		tempTok = tokens[0:idex]
		tokens = tokens[idex:]
		#print(tempTok)
		#print(tokens)
		
		result = []
		cols = []
		if('on' in tempTok or 'ON' in tempTok):
			#print('where with on')
			tempTok = replaceAll([['join',','],['JOIN',','],['ON','on'],['AND','and'],['OR','or']],tempTok)
			result,cols = joinWithWhereWithOn(tempTok,tokens)
		else:
			tempTok = replaceAll([['join',','],['JOIN',',']],tempTok)
			result,cols = joinWithWhereWithoutOn(tempTok,tokens)

		#print(result)
		if(result):
			print()
			if(len(result)==0):
				print("   No rows returned",end="");
			else:
				tabulate(result,cols)
				print("   ",len(result)," row(s) returned.",end="");
		elif(type(result)!=bool and len(result)==0):
			print("   ",len(result)," row(s) returned.",end="")

	elif 'where' in tokens or 'WHERE' in tokens: #where only
		idex = 0
		tokens = replaceAll([['AND','and'],['OR','or']],tokens)
		if('where' in tokens):
			idex = tokens.index('where')
		elif('WHERE' in tokens):
			idex = tokens.index('WHERE')
		tempTok = tokens[0:idex]
		tokens = tokens[idex:]
		
		index = 0
		if('from' in tempTok):
			index = tempTok.index('from');
		else:
			index = tempTok.index('FROM');

		if isCrossProduct(index,len(tempTok)):
			#print('crossproduct')
			result,cols = joinWithoutOnWhere(tempTok,tokens)
			if(result):
				tabulate(result,cols)
				print("   ",len(result)," row(s) returned.",end="");
			elif(type(result)!=bool and len(result)==0):
				print("   ",len(result)," row(s) returned.",end="")
		else:
			#print('not crossproduct')
			result,cols = normalSelectWhere(tempTok,tokens)
			if(result):
				tabulate(result,cols)
				print("   ",len(result)," row(s) returned.",end="");
			elif(type(result)!=bool and len(result)==0):
				print("   ",len(result)," row(s) returned.",end="")

	elif 'join' in tokens or 'JOIN' in tokens: #join only
		tokens = replaceAll([['join',','],['JOIN',',']],tokens)
		#print('start',	tokens)
		if('ON' in tokens or 'on' in tokens): #if there is an on statement
			tokens = replaceAll([['ON','on'],['AND','and'],['OR','or']],tokens)
			result,cols = joinWithOn(tokens)
			if(result):
				tabulate(result,cols)
				print("   ",len(result)," row(s) returned.",end="");
			elif(type(result)!=bool and len(result)==0):
				print("   ",len(result)," row(s) returned.",end="")
		else:
			result,cols = joinWithoutOn(tokens)
			if(result):
				tabulate(result,cols)
				print("   ",len(result)," row(s) returned.",end="");
			elif(type(result)!=bool and len(result)==0):
				print("   ",len(result)," row(s) returned.",end="")
	else: #normal select statement
		index = 0
		if('from' in tokens):
			index = tokens.index('from');
		else:
			index = tokens.index('FROM');
		if isCrossProduct(index,len(tokens)):
			printData,cols = joinWithoutOn(tokens)
			if(printData):
				tabulate(printData,cols)
				print("   ",len(printData)," row(s) returned.",end="")
			elif(type(printData)!=bool and len(printData)==0):
				print("   ",len(printData)," row(s) returned.",end="")
		else:
			printData,cols = normalSelect(tokens)
			if(printData):
				tabulate(printData,cols)
				print("   ",len(printData)," row(s) returned.",end="")
			elif(type(printData)!=bool and len(printData)==0):
				print("   ",len(printData)," row(s) returned.",end="")
