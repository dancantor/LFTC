from HashTable import HashTable
from prettytable import PrettyTable


class SymbolTable:
    def __init__(self):
        self._ht = HashTable()

    def addSymbolToST(self, symbol):
        return self._ht.addSymbolToHT(symbol)

    def getPositionOfSymbol(self, symbol):
        return self._ht.getPositionOfSymbol(symbol)

    def getSize(self):
        return self._ht.getSize()

    def getSymbolOnPos(self, pos):
        return self._ht.getSymbolOnPos(pos)

    def __str__(self):
        result = PrettyTable(['ST_POS', 'SYMBOL'])

        for pos in range(self.getSize()):
            result.add_row([str(pos), str(self.getSymbolOnPos(pos))])

        return str(result)
