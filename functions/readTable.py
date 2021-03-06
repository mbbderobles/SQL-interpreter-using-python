# Reads the rows of the tables from the data folder

import readMeta

def getRowsFromTable(tblname,columns):
	fReader = open('./data/'+tblname+'.txt','r',encoding = "UTF-8")
	tblData = {}
	count = 0
	for line in fReader:
		if(line[-1]=='\n'):
			line = line[:-1]
		data = line.split('|')
		tblData[data[0]] = {}
		i = 0
		#print(data, tblname)
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


def printTableRows(data,tbl,cols):
	for k in cols:
		print("\t%s\t" % k.upper(), end="")
	print()
	for k in data[tbl].keys():
		print("\t%s\t " % k, end="")
		i=1
		for j in data[tbl][k]:
			print("\t%s\t " % data[tbl][k][cols[i]], end="")
			i = i+1
		print()

