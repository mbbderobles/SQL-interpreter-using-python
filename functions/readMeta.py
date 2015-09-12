# Reads the metadata file from the data folder

def readMetaData():
	fReader = open("./data/metadata","r")
	counter = 0
	tables = {}								#list of tables from the metadata
	tbl = ''								#temp var for the name of the tables
	for line in fReader:
		if(line[-1]=='\n'):
			line = line[:-1]				#removes \n
		cols = line.split(",")
		if(len(cols)==1):					#creates a hash for a certain table
			tables[cols[0]] = {}
			tbl = cols[0];
			counter = 0
		else:								#creates a hash for each column of a table
			tables[tbl][counter] = []
			tables[tbl][counter].append(cols[0])	 #name
			tables[tbl][counter].append(cols[1]) 	 #type

			if(len(cols) > 3):						 #length
				tables[tbl][counter].append(cols[2]+','+cols[3])
			else:
				tables[tbl][counter].append(cols[2])

			if(counter == 0):						#first column written is always the primary key
				tables[tbl][counter].append(True)
			else:
				tables[tbl][counter].append(False)

		
			counter += 1

	return tables

tb = readMetaData()