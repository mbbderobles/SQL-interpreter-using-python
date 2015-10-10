import readTable
import readMeta
import os

def getRecordsFromTextFile():
	data = {}
	tb = readMeta.tb
	for i in tb.keys():
		cols = readTable.getColumns(i.lower(),tb)
		#vRecords = readTable.getRowsFromTable(i.lower(),cols) #get the records from textfile. #Modified on the next line.
		data[i]=readTable.getRowsFromTable(i.lower(),cols)
		#data = readTable.addTableToHash(data,i.lower(),vRecords) #place the records to hash table.
	
	return data,readMeta.tb


def writeRecordsToTextFile(data):
	tb = readMeta.tb
	for i in data.keys():
		cols = readTable.getColumns(i.lower(),tb)
		vColumnCount = len(cols) #get the number of columns on the table.
		vRecFile = "./data/"+i.lower()+".txt"
		fRecTextFile = open(vRecFile,'w') #overwrite the existing table textfile into a new textfile.
		cols.pop(0)
		for a in data[i].keys():
			count = 0
			fRecTextFile.write(a)
			lis = data[i][a]
			fRecTextFile.write('|')
			count+=1
			for b in cols:
				fRecTextFile.write(data[i][a][b]) #print the record to the textfile.
				if(count<vColumnCount-1):
					fRecTextFile.write('|')
					count+=1
			fRecTextFile.write('\n') #print newline on the textfile. it means that we will print a new record row.
		fRecTextFile.close()


#records = getRecordsFromTextFile()
#writeRecordsToTextFile(records)

##for checking purposes only. this can be deleted
#records = getRecordsFromTextFile()

#for k in records.keys():
#	print("\t%s\t" % k.upper(), end="")
#	print()

#	for k in records[k].keys():
#		print("\t%s\t " % k, end="")
#		print()
#for checking purposes only. this can be deleted
#	input('next')
