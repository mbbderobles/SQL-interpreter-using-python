# source of code: http://planspace.org/20150111-a_great_python_book_explains_hash_tables/
# see above link for explanation


class intDict(object):
    """A dictionary with integer keys"""

    def __init__(self, numBuckets):
        """Create an empty dictionary"""
        self.buckets = []
        self.numBuckets = numBuckets
        for i in range(numBuckets):
            self.buckets.append([])

    def addEntry(self, dictKey, dictVal):
        """Assumes dictKey an int. Adds an entry."""
        hashBucket = self.buckets[dictKey%self.numBuckets]
        for i in range(len(hashBucket)):
            if hashBucket[i][0] == dictKey:
                hashBucket[i] = (dictKey, dictVal)
                return
        hashBucket.append((dictKey, dictVal))

    def getValue(self, dictKey):
        """Assumes dictKey an int. Returns entry associated
           with the key dictKey"""
        hashBucket = self.buckets[dictKey%self.numBuckets]
        for e in hashBucket:
            if e[0] == dictKey:
                return e[1]
        return None

    def __str__(self):
        result = '{'
        for b in self.buckets:
            for e in b:
                result = result + str(e[0]) + ':' + str(e[1]) + ','
        return result[:-1] + '}' #result[:-1] omits the last comma
    
#--------new def modification------------------------

    def getKey(self, searchVal):
         for b in self.buckets:
            for e in b:
                for val1 in e[1]: # traverses all elements of the list
                    #print(val1)              
                    if val1 == searchVal:
                       return e[0]
#----------------------------------------    
# sample values  
    def returnCustTable():
        sampleDict = intDict(10)
        sampleDict.addEntry(1, ["Rodriquez","Matthew","043-084-4056","dictum.mi@nonduinec.com" ])
        sampleDict.addEntry(2, ["Goodwin","Noelani","098-018-2861","viverra.Donec.tempus@Crasinterdum.net" ])
        sampleDict.addEntry(3, ["Hubbard","Heidi","036-402-8374","venenatis@acipsumPhasellus.edu" ])
        sampleDict.addEntry(4, ["Ballard","Fay","023-287-4666","nec.luctus.felis@mi.com" ])
        sampleDict.addEntry(5, ["Schneider","Ciara","036-995-9643","sodales@lectus.org" ])
        sampleDict.addEntry(6, ["Charles","Ramona","051-648-4975","felis.Nulla.tempor@egetmollis.com" ])
        sampleDict.addEntry(7, ["Shields","Lunea","065-529-0905","mauris.eu@adipiscingelit.edu" ])
        sampleDict.addEntry(8, ["Hubbard","Curran","092-398-2912","auctor@rhoncusNullamvelit.ca" ])
        sampleDict.addEntry(9, ["Noble","Lamar","056-909-9252","ligula.Donec@ornareplacerat.ca" ])
        sampleDict.addEntry(10, ["Huff","Derek","080-243-7876","sem.elit@eleifendCras.ca" ])

        return sampleDict
    
print(intDict.returnCustTable())


