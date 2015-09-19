#using sales_h table as sample - variable readTable.data has sales_h dictionary
#retrieved data are in list keyList

#======================utils=======================================
#taken from http://stackoverflow.com/questions/15357830/python-spliting-a-list-based-on-a-delimiter-word
#modified 
def regroupList(stmt, separator):
    sublist=[]
    for i in stmt:
        if(i==separator):
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
    if("AND" in whereStmt or "and" in whereStmt):
        andlist =  list( regroupList(whereStmt, "and"))
        print(andlist)
    elif("OR" in whereStmt or "or" in whereStmt):
        orlist =  list( regroupList(andlist[1], "or"))
        print(orlist)
    '''else:
        if(whereStmt[0] == readMeta.)'''


sampleStmt = ["where", "cashier_id", "=", "1054", "and", "sales_gross_amount", "=", "220", "or", "customer_id", "=", "0" ]
#processWhereStmt(sampleStmt[1:])

