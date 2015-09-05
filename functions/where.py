import readTable

#using sales_h table as sample - variable readTable.data has sales_h dictionary
#retrieved data are in list keyList

#if valueToSearch is equal to 
def dataExistInTable(sourceData, valueToSearch):
    keyList=[]
    for k in sourceData:
        for key,value in sourceData[k].items():
           if(valueToSearch==value):                  
               keyList.append(k) 
               
    return keyList

        
#print(readTable.data['sales_h'])
print(dataExistsInCol(readTable.data['sales_h'], '220'))