from prettytable import PrettyTable

from Parser import Parser


class Table:
    def __init__(self, file):
        self.parser=Parser(file)
    # TODO very nice choice of splitting the table as a separate class and working with pretty table for creating it
    def getTable(self):
        states = self.parser.computeCanonicalCollection()
        table = []
        for i in range(len(states)):
            table.append({})
        stateNr = 0
        for state in states:
            shift = 0
            reduce = 0
            accept = 0
            nrOfProductionsForState = len(state)
            elemInTable = table[stateNr]

            for prod in state:
                element = prod[1][0]
                dotPos = element.index('.')
                beforeDot = element[:dotPos]
                afterDot = element[dotPos + 1:].strip()

                if len(afterDot) == 0:
                    # dot is at the end for prod. of S’
                    if prod[0] == 'S\'' and beforeDot == self.parser._grammar.getStartingSymbol():
                        accept += 1

                    # dot is at the end, but not for S’
                    elif prod[0] != 'S\'':
                        reduce += 1
                        elem = [prod[0], beforeDot]
                        productionPos = self.parser._grammar._prodList.index(elem)
                else:
                    # dot is not at the end
                    shift += 1

            # one column for action/state (for a state, action is unique because prediction is ignored)
            if shift == nrOfProductionsForState:
                elemInTable['ACTION'] = 'shift'

            elif reduce == nrOfProductionsForState:
                elemInTable['ACTION'] = 'reduce' + str(productionPos)

            elif accept == nrOfProductionsForState:
                elemInTable['ACTION'] = 'accept'
            else:
                raise (Exception('error for state ' + str(state)))

            # goto: one column for each symbol in N+T
            union = self.parser._grammar.getNonTerminals() + self.parser._grammar.getTerminals()
            for symbol in union:
                nextState = self.parser.goTo(state, symbol)
                if nextState in states:
                    indexOfNextState = states.index(nextState)
                    elemInTable[symbol] = indexOfNextState
            stateNr += 1

        return table

    def toStringTable(self, table):
        result = PrettyTable(['STATE', 'ACTION', 'GOTO'])
        stateNr = 0
        for pair in table:
            for k in pair.keys():
                for v in pair.values():
                    if (pair.get(k) == v):
                        if k == 'ACTION':
                            result.add_row([stateNr, str(v), " "])
                        else:
                            result.add_row([stateNr, "", str(k) + ": s" + str(v)])
            stateNr += 1

        return str(result)
