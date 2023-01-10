from prettytable import PrettyTable

from Grammar import Grammar


class Parser:
    def __init__(self, filename):
        self._grammar = Grammar(filename)
    #TODO some comments for closure function would be nice
    def closure(self, items):
        if not items:
            return None
        closure = items
        ok = True
        while ok:
            ok = False
            for item in closure:
                dotPos = item[1][0].index('.')
                afterDot = item[1][0][dotPos + 1:].strip()
                if len(afterDot) > 0:

                    if (afterDot in self._grammar.getTerminals() or afterDot in self._grammar.getNonTerminals()):
                        firstAfterDot = afterDot
                    else:
                        firstAfterDot = afterDot[0]
                    if not self._grammar.isTerminal(firstAfterDot):
                        for prod in self._grammar.getProductionsForNonTerminal(firstAfterDot):
                            newProd = ""
                            for p in prod.split(" "):
                                if (p != " "):
                                    newProd += p
                            production = (firstAfterDot, ['.' + newProd])
                            if production not in closure:
                                closure.append(production)
                                ok = True

        return closure

    def goTo(self, state, symbol):
        # move the dot after symbol if symbol== first symbol after dot
        # then, return closure for this new item
        items = []
        for production in state:
            element = production[1][0]
            dotPos = element.index('.')
            beforeDot = element[:dotPos]
            afterDot = element[dotPos + 1:].strip().split(" ")

            if len(afterDot) != 0:
                if len(afterDot[0]) > 0:
                    firstSymbolAfterDot = afterDot[0][0]
                else:
                    firstSymbolAfterDot = ""

                rest = afterDot[0][1:]

                if firstSymbolAfterDot == symbol:
                    if len(rest) != 0:
                        newProd = (production[0], [beforeDot + firstSymbolAfterDot + '.' + rest[0]])
                    else:
                        newProd = (production[0], [beforeDot + firstSymbolAfterDot + '.'])
                    items += [newProd]

        return self.closure(items)
    #TODO We've done it the same, but maybe it would have been better to create classes for the operation
    # on grammars, rather than manipulating directly the strings
    def computeCanonicalCollection(self):
        initialProd = [('S\'', ['.' + self._grammar.getStartingSymbol()])]
        canonicalCollection = [self.closure(initialProd)]
        union = self._grammar.getNonTerminals() + " " + self._grammar.getTerminals()

        ccIsModified = True
        while ccIsModified:
            ccIsModified = False
            for state in canonicalCollection:
                for x in union.split(" "):
                    nextState = self.goTo(state, x)
                    if nextState is not None and nextState not in canonicalCollection:
                        canonicalCollection += [nextState]
                        ccIsModified = True
        return canonicalCollection

    def toStringCanonicalCollection(self):
        print("Canonical collection: ")
        pos = 0
        for c in self.computeCanonicalCollection():
            print("S" + str(pos) + "=", c, "\n")
            pos += 1




