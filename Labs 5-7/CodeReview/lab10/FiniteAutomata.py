class FiniteAutomata:
    def __init__(self, fileName):
        self._initialState = None
        self._finalState = []
        self._states = []
        self._alphabet = []
        self._transitions = {}
        self.readFromFile(fileName)

    def readFromFile(self, fileName):
        with open(fileName, 'r') as file:
            file.readline()
            states = file.readline()
            self._states = states.strip().split(', ')

            file.readline()
            alphabet = file.readline()
            self._alphabet = alphabet.strip().split(', ')

            file.readline()
            initialState = file.readline()
            self._initialState = initialState.strip()

            file.readline()
            finalStates = file.readline()
            self._finalState = finalStates.strip().split(', ')

            file.readline()
            while True:
                line = file.readline()
                if len(line) == 0:
                    break
                line = line.strip().split(', ')
                firstState = line[0]
                symbol = line[1]
                currentKey = (firstState, symbol)
                nextState = line[2]
                if currentKey not in self._transitions.keys():
                    self._transitions[currentKey] = []
                self._transitions[currentKey].append(nextState)

    # A FA is deterministic if for each pair of state-value there is a unique next state
    def isDeterministicFA(self):
        count = 0
        for key in self._transitions.keys():
            if len(self._transitions[key]) <= 1:
                count += 1
        if count == len(self._transitions.keys()):
            return True
        return False

    def validFA(self):
        if self._initialState not in self._states:
            return False
        for state in self._finalState:
            if state not in self._states:
                return False
        return True

    def displayMenuFA(self):
        print('1. Get states')
        print('2. Get alphabet')
        print('3. Get initial state')
        print('4. Get final states')
        print('5. Get transitions')
        print('6. Check if string is accepted')
        print('0. Exit')

    def checkIsAccepted(self, string):
        if self.isDeterministicFA():
            currentState = self._initialState
            for symbol in string:
                currentKey = (currentState, symbol)
                if currentKey in self._transitions.keys():
                    nextState = self._transitions[currentKey][0]
                    currentState = nextState
                else:
                    return False
            if currentState in self._finalState:
                return True
        return False

    def toStringTransitions(self):
        result = "\n"
        for key in self._transitions.keys():
            result += "δ("+key[0] + ", " + key[1] + ") = " + self._transitions[key][0] + "\n"
        return result

    def start(self):
        if self.validFA():
            print("The FA is valid")
            while True:
                self.displayMenuFA()
                try:
                    inp = int(input('Enter your choice: '))
                except ValueError:
                    print("Not a valid input type.")
                    break
                if inp == 1:
                    print("The states of the FA are: ", self._states)
                elif inp == 2:
                    print("The alphabet of the FA is: ", self._alphabet)
                elif inp == 3:
                    print("The initial state of the FA is: ", self._initialState)
                elif inp == 4:
                    print("The final states of the FA are: ", self._finalState)
                elif inp == 5:
                    print("The transitions of the FA are: ", self.toStringTransitions())
                elif inp == 6:
                    print("Is deterministic: ", self.isDeterministicFA())
                    string = input("Enter a string:")
                    if self.checkIsAccepted(string):
                        print("\nIs accepted by the FA\n")
                    else:
                        print("\nIs not accepted by the FA\n")
                else:
                    break
        else:
            print("The FA is not valid")

