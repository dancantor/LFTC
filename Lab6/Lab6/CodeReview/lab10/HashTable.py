class HashTable:
    def __init__(self):
        self._size = 40
        self._ht = {}
        for i in range(self._size):
            self._ht[i] = []

    def getSize(self):
        return self._size

    def getSymbolOnPos(self, pos):
        return self._ht[pos]

    def hashFunction(self, symbol):  # sum of ascii characters % size of hash table
        sumAscii = 0
        for i in range(len(str(symbol))):
            sumAscii += ord(str(symbol)[i])
        return sumAscii % self._size

    def addSymbolToHT(self, symbol):
        positionInST = self.hashFunction(symbol)
        if symbol in self._ht[positionInST]:
            for posInList in range(len(self._ht[positionInST])):
                if symbol == self._ht[positionInST][posInList]:
                    return positionInST, posInList
            return -1
        self._ht[positionInST].append(symbol)
        return positionInST, len(self._ht[positionInST]) - 1

    def getPositionOfSymbol(self, symbol):
        positionInSt = self.hashFunction(symbol)
        if len(self._ht[positionInSt]) == 0:
            return -1
        return positionInSt
