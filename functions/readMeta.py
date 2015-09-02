#read metadata

def readMetaData():
<<<<<<< HEAD
	fReader = open("./../data/metadata","r")
	counter = 0
	tables = {} #list of tables from the metadata
	tbl = '' #temp var for the name of the tables
=======
	fReader = open("./data/metadata","r")
	counter = 0
	
	tables = {} #list of tables from the metadata
	tbl = '' #temp var for the name of the tables
	counter += 1
>>>>>>> b937df2a03503806eb5c49319cc8997bdf508f24
	for line in fReader:
		if(line[-1]=='\n'):
			line = line[:-1] #removes \n
		cols = line.split(",")
		if(len(cols)==1):	#creates a hash for a certain table
			tables[cols[0]] = {}
			tbl = cols[0];
			counter = 0
		else:			#creates a hash for each column of a table
			tables[tbl][counter] = []
<<<<<<< HEAD
			tables[tbl][counter].append(cols[0]) #name
			tables[tbl][counter].append(cols[1]) #type

			if(len(cols) > 3):		 #length
				tables[tbl][counter].append(cols[2]+','+cols[3])
			else:
				tables[tbl][counter].append(cols[2])

			if(counter == 0):
				tables[tbl][counter].append(True)
			else:
				tables[tbl][counter].append(False)

		
=======
			tables[tbl][counter].append(cols[0])
			tables[tbl][counter].append(cols[1]) #type
			tables[tbl][counter].append(int(cols[2])) #length
			
			if(len(cols) > 3):
				tables[tbl][counter].append(True)
			else:
				tables[tbl][counter].append(False)
>>>>>>> b937df2a03503806eb5c49319cc8997bdf508f24
			counter += 1

	return tables

<<<<<<< HEAD
tb = readMetaData()

#prints the table data
for i in tb.keys():
	print("\n",i.upper(),": ") #prints the table name
	print("\t\tCOLUMN\t\t\t\tTYPE\t\t\t\tLENGTH\t\t\t\tISPK") #prints the headers
	for j in tb[i].keys():	#prints each column details in a row
		for k in tb[i][j]:
			print("\t%20s\t" %k,end=" ")
		print()
	print()
=======
#tb = readMetaData()
'''
#prints the table data
for i in tb.keys():
	print("\n",i.upper(),": ") #prints the table name
	print("\tCOLUMN\t\tTYPE\t\tLENGTH\t\tISPK") #prints the headers
	for j in tb[i].keys():	#prints each column details in a row
		for k in tb[i][j]:
			print("\t%s\t" %k,end=" ")
		print()
	print()
'''
>>>>>>> b937df2a03503806eb5c49319cc8997bdf508f24
