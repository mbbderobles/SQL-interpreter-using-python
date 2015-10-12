import sqlUtils
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
 
 
#returns the column type of a given column- using data from readMeta.tb
#if type is int or float, considered as int, all the rest are considered as str
def determineColType(metaTB, tableName, columnName):
    datatype = ""
    for i in metaTB[tableName]:
        if(metaTB[tableName][i][0]==columnName):
            datatype = metaTB[tableName][i][1]
         #   print(datatype)
            break
    
    if(datatype == "int" ):
        return "int"
    elif(datatype == "float"):
         return "float"
    else:
        return "str"
    
#converts a given data according to dataType
def convertValue(dataType, data):
    temp=data
    if(dataType =="str"):
        temp = data[1:-1].__str__()     # strip quotation marks before converting
    elif(dataType == "int"):
        temp = int(float(data))
    elif(dataType == "float"):
        temp = float(data)
      
    return temp
#==================================================================


# returns the list of keys that satisfies the where clause
#if valueToSearch is found given the columnName, add to KeyList the keys
#IMPT NOTE: conversion of datatype of values is necessary for proper comparison
#  622 > 2455 for a string type but 622 < 2455 for an int datatype
#  datatypes are based on the specified type in metadata

def getKeyListInTable(metadataTb, tableName, sourceData, columnName, valueToSearch, logicOp):
    keyList=[]  
    dtype = determineColType(metadataTb,tableName,columnName) 
    convertedValueSearch =   convertValue(dtype,valueToSearch)
    # columnName is primary, check the outer k value in sourceData
    if(sqlUtils.isPrimary(metadataTb,tableName,columnName)):        
        for k in sourceData:
            if(logicOp == "="):
                if(convertValue(dtype,k) == convertedValueSearch): 
                    keyList.append(k) 
            elif(logicOp == "<"):    
                if( convertValue(dtype,k) < convertedValueSearch):     
                    keyList.append(k)  
            elif(logicOp == ">"):                       
                if( convertValue(dtype,k) > convertedValueSearch):                                    
                    keyList.append(k)  
            else:
                if(convertValue(dtype,k) != convertedValueSearch):                 
                    keyList.append(k)     
    else:
    #else columnName is not primary
        for k in sourceData:         
            for key,value in sourceData[k].items():  
                if(key == columnName):
                    if(logicOp == "="):
                        if( convertValue(dtype,value) == convertedValueSearch):                                         
                            keyList.append(k)  
                        #   print(value)     
                    elif(logicOp == "<"):    
                        if( convertValue(dtype,value) < convertedValueSearch):                 
                            keyList.append(k)
                         #   print(value)  
                    elif(logicOp == ">"):                       
                        if( convertValue(dtype,value) > convertedValueSearch):                                            
                            keyList.append(k) 
                         #   print(value) 
                    else:
                        if( convertValue(dtype,value) != convertedValueSearch):                 
                            keyList.append(k) 
                         #   print(value)                  
   # print(keyList)      
    return keyList


# assumes whereStmt to be in the format of '<column> <logical op> <value>'
def getKeysStmtEval(metadataTb, tableName, tableSource,unitWhereStmt):
    #print(unitWhereStmt)
    searchColumn = unitWhereStmt[0]   #column given in where clause
        
    if(unitWhereStmt[1] == "="):
        logicalOp= "=";
            
    elif(unitWhereStmt[1] == "<"):
        logicalOp= "<";
            
    elif(unitWhereStmt[1] == ">"):
        logicalOp= ">";
            
    else:   #assumes the only operator left is !=
        logicalOp= "!=";
    searchVal = unitWhereStmt[2]   #value to search
        
    keyList = getKeyListInTable(metadataTb, tableName, tableSource,searchColumn, searchVal, logicalOp)
    #print("===")
    #print(keyList)
    return keyList

#INTERSECTION of keys given two list of keys 
def mergeKeysIntersect(primaryList, listToAdd):
    tempList=[]
    for val in listToAdd:
        if val in primaryList:
           tempList.append(val)              
    
    return tempList      

#UNION of keys - distinct
def mergeKeysUnion(primaryList, listToAdd):
    for val in listToAdd:
        if val not in primaryList:
            primaryList.append(val) 
            
    return primaryList   

  
# Where statement for single table source only where tableSource is the hash for the target table 
# outputs two separate lists for OR statements and AND statements 
#   - first level contains OR clauses
#   - second level contains AND clauses

def processWhereStmt(metadataTb, tableName, tableSource, whereStmt):
    keyList= []    
    regroupedList = []
    regroupedList2=[]
    
    newlist =[]
    for w in range(0, len(whereStmt)):
        newlist.append((whereStmt[w].__str__()).replace('\'', ''))   
    whereStmt= newlist
    #print(newlist)
    # 'or' exists in whereStmt
    if("OR" in whereStmt or "or" in whereStmt):
        regroupedList =  list( regroupList(whereStmt, "or"))
        #print(regroupedList)
                
        finalList=[]
        orlist =[]
        for cnt in range (0, len(regroupedList)): #first level lists contains OR clauses
            #print("round" + cnt.__str__())
            if("AND" in regroupedList[cnt] or "and" in regroupedList[cnt]):
                regroupedList2.append(list( regroupList(regroupedList[cnt], "and"))) #second level contains AND clauses
               # print(regroupedList2)
               # print(len(regroupedList2))
               
                #evaluation order for the regrouped list- first level of regroupedList2 contains the clauses for 'OR' operation (UNION)
                #  and inner level contains the clause for AND operation (INTERSECTION)
                andlist=[]
                firstList=[]
                for i in range(0,len(regroupedList2)):       
                    firstList=[]
                    # AND operations
                    for j in range(0, len(regroupedList2[i])):                
                        if j > 0 and j < len(regroupedList2[i]):                 
                            temp = firstList
                            firstList = mergeKeysIntersect(temp, getKeysStmtEval(metadataTb, tableName, tableSource,regroupedList2[i][j])) 
                             
                        else:
                            firstList = getKeysStmtEval(metadataTb, tableName, tableSource,regroupedList2[i][j])   
                         
                    
                    andlist.append(list(firstList))
                #print(andlist)
                
                # UNION of the and list in finallist
                
                for k in range(0, len(andlist)):
                    if k >0 and k < len(andlist):
                        temp = finalList
                        finalList = mergeKeysUnion(temp,andlist[k] )
                    else: 
                        finalList = andlist[k]
                   
                #print(finalList)               
                keyList= finalList  
                
            else: # no AND exists in second level 
                
                if cnt > 0 and cnt < len(regroupedList):   
                    temp = orlist
                    orlist = mergeKeysUnion(temp, getKeysStmtEval(metadataTb, tableName, tableSource,regroupedList[cnt]))
                else:
                    orlist = getKeysStmtEval(metadataTb, tableName, tableSource,regroupedList[cnt]) 
              
                #print(orlist)
                
            if len(finalList) == 0:
                    keyList = orlist
            else:  
                 tempp = keyList               
                 keyList= mergeKeysUnion(tempp,orlist) 
    
        
    #only 'and' exists in whereStmt
    elif("AND" in whereStmt or "and" in whereStmt):
        regroupedList =  list( regroupList(whereStmt, "and"))
        #print(regroupedList)
        andlist2=[]
        for cnt in range (0, len(regroupedList)): #first level lists contains AND clauses
            if cnt > 0 and cnt < len(regroupedList):   
                temp = andlist2
                andlist2 = mergeKeysIntersect(temp, getKeysStmtEval(metadataTb, tableName, tableSource,regroupedList[cnt]))
            else:
                andlist2 = getKeysStmtEval(metadataTb, tableName, tableSource,regroupedList[cnt]) 
                  
       # print(andlist2)
        keyList=andlist2
        
    #no 'and' nor 'or' exists in whereStmt        
    else:
            
        keyList= getKeysStmtEval(metadataTb, tableName, tableSource,whereStmt)
        
    #print(keyList)    
    return keyList
        
