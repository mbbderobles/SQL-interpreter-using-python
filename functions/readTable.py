import readMeta

def getRowsFromTable(tblname,columns):
<<<<<<< HEAD
	fReader = open('./../data/'+tblname+'.txt','r')
=======
	fReader = open('./data/'+tblname+'.csv','r')
>>>>>>> b937df2a03503806eb5c49319cc8997bdf508f24
	tblData = {}
	for line in fReader:
		if(line[-1]=='\n'):
			line = line[:-1]
<<<<<<< HEAD
		data = line.split('|')
=======
		data = line.split(',')
>>>>>>> b937df2a03503806eb5c49319cc8997bdf508f24
		tblData[data[0]] = {}
		i = 0
		while i<len(columns):
			if i==0:
				i = i+1
				continue
			tblData[data[0]][columns[i]] = data[i]
			i = i+1
	return tblData

def getColumns(tableName,tables):
	cols = []
	temp = tables[tableName]
	for i in temp.keys():
		cols.append(temp[i][0]) #sub zero since 1st element is columnName
	return cols

def printTableRows(rows,cols):
	for k in cols:
		print("\t%s\t" % k.upper(), end="")
	print()
	for k in rows.keys():
		print("\t%s\t " % k, end="")
		i=1
		for j in rows[k]:
			print("\t%s\t " % rows[k][cols[i]], end="")
			i = i+1
		print()
		
tb = readMeta.readMetaData()
<<<<<<< HEAD
cols = getColumns("sales_h",tb)
rows = getRowsFromTable("sales_h",cols)
=======
cols = getColumns("student",tb)
rows = getRowsFromTable("student",cols)
>>>>>>> b937df2a03503806eb5c49319cc8997bdf508f24
printTableRows(rows,cols)