class Grammar:
    def __init__(self, fileName):
        self._nonTerminals = []
        self._terminals = []
        self._productions = {}
        self._S = ""
        self._prodList = []
        self.readFromFile(fileName)

    def getNonTerminals(self):
        return self._nonTerminals

    def getStartingSymbol(self):
        return self._S

    def getTerminals(self):
        return self._terminals

    def isTerminal(self, symbol):
        if symbol in self._terminals:
            return True
        return False

    def getProductionsForNonTerminal(self, nonTerminal):
        return self._productions[nonTerminal]

    def readFromFile(self, fileName):
        with open(fileName, 'r') as file:
            nonterminals = file.readline()
            self._nonTerminals = nonterminals[6:-2]

            terminals = file.readline()
            self._terminals = terminals[6:-2]

            self._S = file.readline()[4:-1]

            file.readline()
            newProductions = {}

            for nt in self._nonTerminals.strip().split(" "):
                newProductions[nt] = []

            while True:
                line = file.readline()
                if len(line) == 1:
                    break
                line = line.strip().split('->')
                nonTerminal = line[0].strip()
                productions = line[1].strip().split("|")
                if ' ' in nonTerminal:
                    newProductions[nonTerminal]=[]

                for p in productions:
                    p = p.strip()
                    p1=p.strip().split(" ")
                    finalP=''
                    for e in p1:
                        if(e!=' '):
                            finalP+=e
                    self._prodList.append([nonTerminal, finalP])
                    # p = p.strip().split(" ")
                    newProductions[nonTerminal].append(p)

                self._productions[nonTerminal] = newProductions[nonTerminal]

    def checkCGF(self):
        cfg = True
        if self._S not in self._nonTerminals:
            return not cfg
        for p in self._productions.keys():
            if ' ' in p:
                cfg = False
        return cfg

    def menu(self):
        print('1. Get nonterminals')
        print('2. Get terminals')
        print('3. Get productions')
        print('4. Get S')
        print('5. Get productions for a given nonTerminal')
        print('6. CFG check')
        print('0. Exit')

    def start(self):
        while True:
            self.menu()
            try:
                inp = int(input('Enter your choice: '))
            except ValueError:
                print("Not a valid input type.")
                break
            if inp == 1:
                print("The nonterminals are:", self._nonTerminals)
            elif inp == 2:
                print("The terminals are: ", self._terminals)
            elif inp == 3:
                print("The productions are: ", self._productions)
            elif inp == 4:
                print("S is : ", self._S)
            elif inp == 5:
                print("The productions for a given nonterminal are: ")
                nonterminal = input("Enter the wanted nonTerminal:")
                print(self.getProductionsForNonTerminal(nonterminal))
            elif inp == 6:
                if self.checkCGF():
                    print("\nIs CFG\n")
                else:
                    print("\nIs not CFG\n")
            else:
                break