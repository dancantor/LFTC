import re

from FiniteAutomata import FiniteAutomata
from PIF import PIF
from ST import SymbolTable


def isConst(token):
    is_strConst = re.search("^[a-zA-Z]$", token)
    is_intConst = re.search("^0$|^[+-]*[1-9][0-9]*$", token)
    return is_strConst is not None or is_intConst is not None


def isIdentifier(token):
    identifier = re.search("^[a-zA-Z]+[a-zA-Z0-9]*$", token)
    return identifier is not None


def isComposedToken(t1, t2, t3):
    if (t1 == '=' and t2 == ':' and t3 == '=') or (
            t1 == '<' and t2 == '=' and
            t3 == '>') or (t1 == '=' and t2 == '=' and
                           t3 == '>'):
        return True
    return False


class Scanner:
    def __init__(self):
        self._st = SymbolTable()
        self._pif = PIF()
        self._operators = ['+', '-', '*', '/', '=:=', '<', '<=', '<=>', '>=', '^', '==>', '>', '%']
        self._separators = ['(', ')', ':', ' ', '[', ']', '/n', '"', ',', "$"]
        self._words = ['int', 'char', 'string', 'if', 'else', 'and', 'input', 'variable', 'for', 'in', 'range',
                       'display', 'vector', 'go', 'stop']

    def write_to_fileSt(self, fileName):
        with open(fileName, 'w') as file:
            file.write("For the ST, I used a hash table for representation\n")
            file.write(str(self._st))

    def write_to_filePIF(self, fileName):
        with open(fileName, 'w') as file:
            file.write(str(self._pif))

    def readFromFile(self, fileName):
        file = open(fileName, 'r')
        return file.readlines()

    def isReservedToken(self, token):
        if token in self._separators or token in self._operators or token in self._words:
            return True
        return False

    def scan(self, fileName):
        lines = self.readFromFile(fileName)
        lineNr = 0
        message = ""
        for line in lines:
            # get all words separated
            strConst = re.findall('"([^"]*)"', line)
            comments = re.findall('\$([^"]*)\$', line)

            dataOnLine = re.split('([^a-zA-Z0-9])', line)

            # get rid of blank space and new line characters
            data = []
            for element in dataOnLine:
                if element != '' and element != ' ' and element != '\n':
                    data.append(element)

            print(data)
            lineNr += 1
            i = 0
            while i < len(data):
                token = data[i]
                if token == "-" and re.search("^0$|^[+-]*[1-9][0-9]*$", data[i + 1]) and isIdentifier(
                        data[i - 1]) == False and isConst(data[i - 1]) == False and i != 0:
                    posInST = self._st.addSymbolToST(token + data[i + 1])
                    self._pif.addToPIF("CONSTANT", posInST)
                    i = i + 1
                elif i < len(data) - 3 and isComposedToken(token, data[i + 1], data[i + 2]):
                    if data[i + 3] == "-" or isConst(data[i + 3]) or isIdentifier(data[i + 3]) or data[i + 3] in self._words:
                        self._pif.addToPIF(token + data[i + 1] + data[i + 2], -1)
                    else:
                        message += 'Lexical error-> token ' + data[i + 3] + ' on line ' + str(lineNr) + "\n"
                    i = i + 2
                elif self.isReservedToken(token):
                    if token in [">", "<"] and data[i + 1] == "=":
                        self._pif.addToPIF(token + data[i + 1], -1)
                        i = i + 1
                    else:
                        self._pif.addToPIF(token, -1)
                elif isIdentifier(token) or isConst(token):
                    posInST = self._st.addSymbolToST(token)
                    if len(strConst) != 0 and token in strConst[0] or len(comments) != 0 and token in comments[0]:
                        self._pif.addToPIF('CONSTANT', posInST)
                    elif isIdentifier(token):
                        fa = FiniteAutomata('input/identifier.in')
                        print(fa.checkIsAccepted(token))
                        self._pif.addToPIF('ID', posInST)
                    else:
                        fa=FiniteAutomata('input/constant-integer.in')
                        print(fa.checkIsAccepted(token))
                        self._pif.addToPIF('CONSTANT', posInST)
                else:
                    message += 'Lexical error-> token ' + token + ' on line ' + str(lineNr) + "\n"
                i += 1

        self.write_to_fileSt('output/ST.out')
        self.write_to_filePIF('output/PIF.out')
        if message == "":
            message = "Lexically correct"
        return self._st, self._pif, message
