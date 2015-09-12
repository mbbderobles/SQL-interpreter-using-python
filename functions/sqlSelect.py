from tabulate import tabulate

tb = {}
data = {}

def getColumns(tableName,tables):
	cols = []
	temp = tables[tableName]
	for i in temp.keys():
		cols.append(temp[i][0]) #sub zero since 1st element is columnName
	return cols

def getColsToPrint(tokens,join):
	cols = []
	if(tokens[0]=='*'):
		tokens.pop(0)
		tokens.pop(0)
		if not join:
			cols = getColumns(tokens[0],tb)
		else:
			i = 0;
			while i<len(tokens):
				if(tokens[i]!=','):
					cols.extend(getColumns(tokens[i],tb))
				i = i+1
	else:
		i = tokens.pop(0)
		while(i.lower()!='from'):
			if(i.lower() == 'from'):
				break;
			elif(i!=','):
				cols.append(i)
			i = tokens.pop(0)
	return cols,tokens

def getTablePK(tableName):
	return tb[tableName][0][0];
	
def isCrossProduct(index,length):
	if(length-index > 2):
		return True
	else:
		return False

def getTables(tokens):
	tbl = [];
	i=0
	while(i<len(tokens)):
		if(tokens[i]!=','):
			tbl.append(tokens[i])
		i+=1
	return tbl

def getTableOfCol(col):
	for tblName in tb.keys():
		for colIndex in tb[tblName].keys():
			if(tb[tblName][colIndex][0]==col):
				return tblName

def joinWithoutOn(tokens):
	cols,tokens = getColsToPrint(tokens,True);
	tables = getTables(tokens)
	printData = []
	pK = []
	for i in tables:
		pK.append(getTablePK(i))
	maxRows = 0
	maxTbl = ''
	numRows = 1
	temp = []
	for i in tables:
		numRows *= len(data[i].keys())
		if len(data[i].keys()) > maxRows:
			maxRows = len(data[i].keys())
			maxTbl = i
	print(numRows)
	print(maxRows)
	print(temp)
	for i in range(0,numRows):
		printData.append([])
	for col in cols:
		counter=0;
		while counter<numRows:
			tbl = getTableOfCol(col)
			for k in data[tbl].keys():
				if(col==getTablePK(tbl)):
					printData[counter].append(k)
				else:
					printData[counter].append(data[tbl][k][col])
				counter += 1
	print()
	if(len(printData)==0):
		print("   No rows returned\n");
	else:
		for i in printData:
			for k in i:
				print(k,"  ",end="")
			print()
		print("\n")
#		print(tabulate(printData,headers=cols,tablefmt="psql"))
		print("   ",len(printData)," rows returned.\n");

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
	print("   ",counter," rows returned.\n")

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
		print('function with join here')
	else: #normal select statement
		index = tokens.index('from');
		if isCrossProduct(index,len(tokens)):
			joinWithoutOn(tokens)
		else:
			normalSelect(tokens)
