import readTable
import readMeta
import os

def getRecordsFromTextFile():
	data = {}
	tb = readMeta.tb
	for i in tb.keys():
		cols = readTable.getColumns(i.lower(),tb)
		vRecords = readTable.getRowsFromTable(i.lower(),cols)
		data = readTable.addTableToHash(data,i.lower(),vRecords)
	
	return data


def writeRecordsToTextFile(data):
	for i in data.keys():
		cols = readTable.getColumns(i.lower(),tb)
		vColumnCount = len(cols)
		vRecFile = "./data/"+i.lower()+".txt"
		fRecTextFile = open(vRecFile,'w')
		for a in data[i].keys():
			vCurrentColumn = 0
			for b in data[i][a]:
				vCurrentColumn = vCurrentColumn+1
				fRecTextFile.write(data[i][a][b])
				if vCurrentColumn > vColumnCount:
					fRecTextFile.write('|')#must first check if this is the last column before writing ('|').
			fRecTextFile.write('\n')
		fRecTextFile.close()


records = getRecordsFromTextFile()

for k in records.keys():
	print("\t%s\t" % k.upper(), end="")
	print()

	for k in records[k].keys():
		print("\t%s\t " % k, end="")
		print()

	input('next')
