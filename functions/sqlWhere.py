
#using sales_h table as sample - variable readTable.data has sales_h dictionary
#retrieved data are in list keyList

#======================utils=======================================
#taken from http://stackoverflow.com/questions/15357830/python-spliting-a-list-based-on-a-delimiter-word
#modified 
def regroupList(stmt, separator):
    sublist=[]
    for i in stmt:
        if i == separator:            
            yield sublist
            sublist = []
            continue
        sublist.append(i)
    yield sublist
 
#==================================================================


# returns the list of keys where the 
#if valueToSearch is found given the columnName, add to KeyList the keys
def getKeyListInTable(sourceData, columnName, valueToSearch):
    keyList=[]
    for k in sourceData:
        for key,value in sourceData[k].items(): 
           # print(key , value)                
            if(key == columnName):
                if(valueToSearch == value):                 
                    keyList.append(k)                            
    return keyList

#still under construction----
# aim is to have two separate lists for OR statements and AND statements - also need to consider precedence
# Where statement for single table source only where tableSource is the hash for the target table 
def processWhereStmt(tableSource, whereStmt):
    keyList= {}
    
    if("AND" in whereStmt or "and" in whereStmt):
        andlist =  list( regroupList(whereStmt, "and"))
        print(andlist)
    elif("OR" in whereStmt or "or" in whereStmt):
        orlist =  list( regroupList(andlist[1], "or"))
        print(orlist)
    #no and or or exists in where stmt
    # assumes whereStmt to be in the format of '<column> = <value>'
    #TODO -- need to handle other logical expressions 
    else:
        searchVal = whereStmt[2]   #value to search
        searchColumn = whereStmt[0]   #column given in where clause
        keyList = getKeyListInTable(tableSource,searchColumn, searchVal)
    return keyList

#sampleStmt = ["where", "sales_h",".","cashier_id", "=", "1054", "and", "sales_h",".","sales_gross_amount", "=", "220", "or", "sales_h",".","customer_id", "=", "0" ]
#processWhereStmt(sampleStmt)

