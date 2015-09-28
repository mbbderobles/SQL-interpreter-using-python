from tabulate import tabulate

tb = {}
data = {}

''' START OF UTILITY FUNCTIONS HERE '''

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
			print(tokens)
			while i<len(tokens):
				if(tokens[i]!=','):
					if(tokens[i-1]==',' or i==0):
						cols.extend(getColumns(tokens[i]))
				i = i+1
	#if rows are in query
	else:
		i = tokens.pop(0)
		while(i.lower()!='from'):
			if(i.lower() == 'from'):
				break;
			elif(i!=','):
				cols.append(i)
			i = tokens.pop(0)
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
			return 'string'

''' checks if two clauses are type compatible '''
def typeCompatible(var1,var2):
	type1 = getType(var1)
	if(type1):
		type2 = getType(var2)
		if(type2):
			if(type1==type2):
				return True,type1,type2
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
			print('less than')
			if(t1!='string'):
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
				print('< cannot be used on type string')
		elif(sign=='>'):
			print('greater than')
			if(t1!='string'):
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
				print('< cannot be used on type string')
		elif(sign=='!='):
			print('not equal')
			var1PK = isPK(var1[0],var1[2])
			var2PK = isPK(var2[0],var2[2])
		
			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				for k in data[var2[0]].keys():
					if(var1PK and var2PK):	#if both PK
						if(j!=k):
							data1.append(j)
							data2.append(k)
					elif(var1PK):	#if first is PK
						if(j!=data[var2[0]][k][var2[2]]):
							data1.append(j)
							data2.append(k)
					elif(var2PK):	#if second is PK
						if(data[var1[0]][j][var1[2]]!=k):
							data1.append(j)
							data2.append(k)
					else:	#if both are not PK
						if(data[var2[0]][j][var2[2]]!=data[var1[0]][k][var1[2]]):
							data1.append(j)
							data2.append(k)
		
		return data1,data2 #PKs of 1st table, 2nd table
	else:
		return [],[]

def evaluateJoinWithOnOneRight(var1,sign,var2,tables,result):
	comp,t1,t2 = typeCompatible(var1,var2)
	if(comp): #if compatible
		data1 = []
		#if equality
		if(sign=='='):
			var1PK = isPK(var1[0],var1[2])
			
			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				if(var1PK):	#if first is PK
					if(j==var2[0]):
						data1.append(j)
				else:	#if both are not PK
					if(data[var1[0]][j][var1[2]]==var2[0]):
						data1.append(j)
		elif(sign=='<'):
			print('less than')
			if(t1!='string'):
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
				print('< cannot be used on type string')
		elif(sign=='>'):
			print('greater than')
			if(t1!='string'):
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
				print('< cannot be used on type string')
		elif(sign=='!='):
			print('not equal')
			var1PK = isPK(var1[0],var1[2])
			
			# ++ GETTING THE PK's of the matching data
			for j in data[var1[0]].keys():
				if(var1PK):	#if first is PK
					if(j!=var2[0]):
						data1.append(j)
				else:	#if both are not PK
					if(data[var1[0]][j][var1[2]]!=var2[0]):
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
	in1 = tables.index(var1tbl)
	in2 = tables.index(var2tbl)

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

'''adds the result of the or '''
def addFilterTwoVar(temp1,temp2,var1tbl,var2tbl,tables,result,rCopy):
	in1 = tables.index(var1tbl)
	in2 = tables.index(var2tbl)
	
	j=0
	while
	


''' removes the rows that did not satisfy the query '''
def filterOneVar(temp1,var1tbl,tables,result):
	in1 = tables.index(var1tbl)

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
		if(tbl in tables):
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
	
# + END OF UTILITY FUNCTIONS +++++++++++++++++++++++++++++++++++++++++++++++++++

''' START OF QUERY FUNCTIONS HERE '''

# ++++ JOIN STATEMENT WITH ON ++++++++++++++++++++++++++++++++++++++++++++++++++
def joinWithOn(tokens):
	cols,tokens = getColsToPrint(tokens,True);
	tables,tokens = getJoinTables(tokens)
	result = joinTables(tables)
	rCopy = result.copy()
	
	cond = 'and'
	nextCond = ''
	print(tokens)
	while(len(tokens)!=0):
		print()
		tokens = tokens[1:]
		signIndex = 0
		if('<' in tokens):
			signIndex = tokens.index('<')
		elif('>' in tokens):
			signIndex = tokens.index('>')
		elif('=' in tokens):
			signIndex = tokens.index('=')
		elif('!=' in tokens):
			signIndex = tokens.index('!=')
		else:
			signIndex = None

		sign = tokens[signIndex]
		var1 = tokens[0:signIndex]
		var2 = tokens[signIndex+1:]

		if('on' in var2 or 'and' in var2 or 'or' in var2):
			nearest = getNearest(var2)
			tokens = var2[nearest:]
			var2 = var2[:nearest]
			nextCond = tokens[0]
			print(nextCond)
		#elif and in var2 and or in var2
		else:
			tokens = []
		
		print('var1',var1)
		print('var2',var2)
		print('toks',tokens)

		if(len(var1)>1 and len(var2)>1):
			print('both side')
			temp1,temp2 = evaluateJoinWithOnTwo(var1,sign,var2,tables,result)
			if(cond=='and' or cond=='on'):
				result = filterTwoVar(temp1,temp2,var1[0],var2[0],tables,result)
			elif(cond=='or'):
				result = addFilterTwoVar(temp1,temp2,var1[0],var2[0],tables,result,rCopy)#!!!!!!!!!!
			#this is only for two tables
			#temp1,temp2 = evaluateJoinWithOn(var1,sign,var2,cols)
			#result = mergeTwo(tables,cols,var1[0],var2[0],temp1,temp2)
		elif(len(var1)>1):
			print('right side single')
			temp1 = evaluateJoinWithOnOneRight(var1,sign,var2,tables,result)
			result = filterOneVar(temp1,var1[0],tables,result)
		elif(len(var2)>1):
			print('left side single')
		else:
			print('both side single')
		cond = nextCond
	
	result = getColsFromKeys(cols,result,tables)
	
	if(result):
		print(tabulate(result,headers=cols,tablefmt="psql"))
		print("   ",len(result)," row(s) returned.\n")
	elif(type(result)!=bool and len(result)==0):
		print("   ",len(result)," row(s) returned.\n")

	#check if it has more than one condition
#	print("Columns: ",cols)	
#	print("Tables: ",tables)
#	print("Tokens: ",tokens)
		
# ++++ CROSS PRODUCT AND JOIN STATEMENT WITHOUT ON CLAUSE ++++++++++++++++++++++
def joinWithoutOn(tokens):
	#get columns and tokens to print
	cols,tokens = getColsToPrint(tokens,True);
	tables,tokens = getTables(tokens,'none')
	printData = []
	pK = []

	#print(tables)

	#get pK of each table
	for i in tables:
		pK.append(getTablePK(i))
	maxRows = 0
	maxTbl = ''
	numRows = 1
	temp = []

	#get total number of rows
	for i in tables:
		numRows *= len(data[i].keys())
		if len(data[i].keys()) > maxRows:
			maxRows = len(data[i].keys())
	print("result rows: ",numRows)
	print("biggest num rows: ",maxRows)

	#create list
	for i in range(0,numRows):
		printData.append([])

	#populate list (per column)
	it = 0
	for col in cols:
		counter=0;
		tbl = getTableOfCol(col)
		if(it==0):
			it = numRows//len(data[tbl].keys())
		else:
			it = it/len(data[tbl].keys())
		while counter<numRows:
			for k in data[tbl].keys():
				i = 0
				while(i<it):
					if(col==getTablePK(tbl)):
						printData[counter].append(k)
					else:
						printData[counter].append(data[tbl][k][col])
					counter += 1
					i+=1
	
	#printData
	print()
	if(len(printData)==0):
		print("   No rows returned\n");
	else:
		for i in printData:
			for k in range(0,len(cols)):
				print(" {}".format(i[k].ljust(30)),end="")
			print()
#		print(tabulate(printData,headers=cols,tablefmt="psql"))
		print("   ",len(printData)," row(s) returned.\n");

# ++++ SIMPLEST SELECT STATEMENT +++++++++++++++++++++++++++++++++++++++++++++++
def normalSelect(tokens):
	cols,tokens = getColsToPrint(tokens,'False');
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
	print()
	print(tabulate(printData,headers=cols,tablefmt="psql"))
	print("   ",counter," row(s) returned.\n")


# ++++ MAIN FUNCTION +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def evaluate(tokens,tables,rows):
	global tb
	global data
	tb = tables
	data = rows

	if ('where' in tokens or 'WHERE' in tokens) and ('join' in tokens or 'JOIN' in tokens): #can also have where+join-on here
		print('where+join function here')
	elif 'where' in tokens or 'WHERE' in tokens: #where only
		print('function with where here')
	elif 'join' in tokens or 'JOIN' in tokens: #join only
		tokens = [k.replace('join',',') for k in tokens]
		tokens = [k.replace('JOIN',',') for k in tokens]
		if('ON' in tokens or 'on' in tokens): #if there is an on statement
			tokens = [k.replace('ON','on') for k in tokens]
			tokens = [k.replace('OR','or') for k in tokens]
			tokens = [k.replace('AND','and') for k in tokens]
			joinWithOn(tokens)
		else:
			joinWithoutOn(tokens)
	else: #normal select statement
		index = tokens.index('from');
		if isCrossProduct(index,len(tokens)):
			joinWithoutOn(tokens)
		else:
			normalSelect(tokens)

