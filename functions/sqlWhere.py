import readTable

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

#if valueToSearch is equal to 
def dataExistInTable(sourceData, valueToSearch):
    keyList=[]
    for k in sourceData:
        for key,value in sourceData[k].items():
           if(valueToSearch==value):                  
               keyList.append(k) 
               
    return keyList

#still under construction----
# aim is to have two separate lists for OR statements and AND statements - also need to consider precedence
def processWhereStmt(whereStmt):   
    andlist =  list( regroupList(whereStmt, "and"))
    print(andlist)
    orlist =  list( regroupList(andlist[1], "or"))
    print(orlist)
    print(andlist) # - need to remove the list of or from the and list
   
#print(readTable.data['sales_h'])
#print(dataExistInTable(readTable.data['sales_h'], '220'))
#sample where clause : 
sampleStmt = ["where", "cashier_id", "=", "1054", "and", "sales_gross_amount", "=", "220", "or", "customer_id", "=", "0" ]
#remove "where" element
sampleStmt.remove("where")
#processWhereStmt(sampleStmt)


