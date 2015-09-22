import sqlWhere

#assuming source has values
def deleteAll(source):
    sourceLen = len(source) + 1
    source.clear()
    print("Successfully deleted "+ sourceLen.__str__() + " rows." )
    
#deletes the values of the keys in keyList from source 
#assumes the source is a hash of a single table    
def deleteValues(source, keyList):
    cntr =0
    for j in keyList:
        cntr+= deleteKey(source, j)      
    if cntr > 0:   
        print("Deleted " , cntr , " rows successfully.")
    else:
        print("No rows were deleted.")
        
        
# deletes an entry from the source given a key, returns 1 if an entry is deleted and 0 otherwise   
def deleteKey(source, key):
    for k in source:    
        if k == key:    
         #   print("key= ", k,  ": val= "+ source[k].__str__()) 
            del source[k]
            return 1
    return 0
            
            

def findTableSource(query):
    nextInd = -1
    
    if "from" in query :
        i = query.index('from')
        nextInd = i + 1
       
    if "FROM" in query :
        i = query.index('FROM')
        nextInd = i + 1    
   
    return query[nextInd] # returns the table name

#calls appropriate delete function whether deleteAll or delete according to where statement    
def processDelQuery(dataSource,query):
 
    if("where" in query or "WHERE" in query): 
        wherelist= list(sqlWhere.regroupList(query, "where"))[1]       
        tableSrc = findTableSource(query)        
        keyList= sqlWhere.processWhereStmt(dataSource[tableSrc], wherelist)
     #   print(keyList)
        deleteValues(dataSource[tableSrc], keyList)
     # returned keys should be removed and stored back to dataSource
    else: # else no where clause in delete   
        deleteAll(dataSource[findTableSource(query)])
           
