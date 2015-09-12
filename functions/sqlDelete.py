import where

#assuming source has values
def deleteAll(source):
    source.clear()
    

def findTableSource(query):
    nextInd = -1
    
    if "from" in query :
        i = query.index('from')
        nextInd = i + 1
       
    if "FROM" in query :
        i = query.index('FROM')
        nextInd = i + 1    
   
    return query[nextInd] # returns the table name

    
def processDelQuery(dataSource,query):
    if("where" in query or "WHERE" in query):
        where.processWhereStmt() # should return keys
     # returned keys should be removed and stored back to dataSource
    else:    
        deleteAll(dataSource[findTableSource(query)])
    
