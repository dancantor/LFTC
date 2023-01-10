import re

from Parser import Parser
from Table import Table


class ParserOutput:
    def __init__(self, filename):
        self.parser = Parser(filename)
        self.table = Table(filename)
        self.errMessage = ""

    #TODO not necessary a problem, considering that you respected the same naming condition on the whole
    # project, but it would have been nicer to respect coding conventions from python language
    def displayParsingByDerivations(self, output):
        firstProduction = self.parser._grammar._prodList[int(output[0])]
        result = str(firstProduction[0]) + "=>(" + output[0] + ") " + str(firstProduction[1])
        initial = firstProduction[1]
        for state in output:
            if int(state) != 0:
                result += "=>(" + state + ") "
                currentProduction = self.parser._grammar._prodList[int(state)]
                left = currentProduction[0]
                right = currentProduction[1]
                initial = initial.replace(left, right, 1)
                result += initial
        print(result)
        return result

    def initialiseStacks(self, input):
        self.workStack = ['0']
        self.inputStack = []
        for symbol in input:
            self.inputStack.append(symbol)
        self.outputBand = []

    def parse(self, seq):
        table = self.table.getTable()
        print(self.table.toStringTable(table))

        self.initialiseStacks(seq)

        while len(self.workStack) != 0:
            state = int(self.workStack[-1])
            if len(self.inputStack) > 0:
                symbol = self.inputStack.pop(0)
            else:
                symbol = None
            try:
                self.checkActionForState(symbol, table, state)
            except Exception as e:
                print(e)

        result = self.displayParsingByDerivations(self.outputBand)
        if self.errMessage == "":
            self.writeToFile("output/parserOutput.out", result)

    def shift(self, symbol, table, state):
        self.workStack.append(symbol)
        self.workStack.append(str(table[state][symbol]))

    def accept(self):
        if (len(self.inputStack)) != 0:
            self.errMessage += "\nCan't be parsed"
            raise Exception("Can't be parsed")
        self.workStack = []
    # TODO Don't have anything else to comment, maybe handling the conflict would have been also nice
    def reduce(self, table, state):
        global rIndex
        possibleReduceIndex = table[state]["ACTION"][-1]
        isInt = re.search("^0$|^[+-]*[1-9][0-9]*$", possibleReduceIndex)
        if isInt:
            rIndex = int(possibleReduceIndex)
        else:
            print("Can't be parsed")
            self.errMessage += "\nCan't be parsed"
            self.writeToFile("output/parserOutput.out", self.errMessage)
            exit(1)

        production = self.parser._grammar._prodList[rIndex]
        leftOperand = production[0]
        rightOperand = production[1]
        self.workStack.pop()

        removeFromWorkStack = []
        for symbol in rightOperand:
            removeFromWorkStack.append(symbol)

        while len(removeFromWorkStack) > 0 and len(self.workStack) > 0:
            lastFromWorkStack = self.workStack[-1]
            if lastFromWorkStack.isnumeric():
                self.workStack.pop()
            lastFromWorkStack = self.workStack[-1]
            if lastFromWorkStack == removeFromWorkStack[-1]:
                removeFromWorkStack.pop()
            self.workStack.pop()

        if len(removeFromWorkStack) != 0:
            self.errMessage += "\nerror at parsing reduce"
            raise (Exception('error at parsing reduce'))

        self.inputStack.insert(0, leftOperand)
        self.outputBand.insert(0, str(rIndex))

    def checkActionForState(self, symbol, table, state):
        if symbol is not None:
            if symbol not in table[state]:
                self.errMessage += "\nSymbol " + symbol + " not in table for state " + str(state)
                raise Exception("Symbol " + symbol + " not in table for state " + str(state))
            elif table[state][symbol] is not None and table[state]["ACTION"] == "shift":
                self.shift(symbol, table, state)
        if symbol is None:
            if table[state]["ACTION"] == "accept":
                self.accept()
            else:
                self.reduce(table, state)

    def writeToFile(self, fileName, result):
        with open(fileName, 'w') as file:
            file.write(result)

    def readFromFile(self, fileName):
        # TODO file was not closed
        file = open(fileName, 'r')
        return file.readline()
