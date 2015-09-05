import readTable, readMeta

#using sales_h table as sample - variable readTable.data has sales_h dictionary
#only retrieves one key
def dataExistsInCol(sourceData, valueToSearch):
    for k in sourceData:
        for key,value in sourceData[k].items():
           if(valueToSearch==value):                            
               print(key +" ::")
               return k
    return None
        
print(readTable.data['sales_h'])
print(dataExistsInCol(readTable.data['sales_h'], '220'))