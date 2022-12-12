class RecursiveDescendantParser:
    def __init__(self):
        # q - normal state, b - back state, f - final state, e - error state
        self.__state = "q"
        self.__index = 0
        self.__input = [] #[self.grammar.get_start_symbol()]
        self.__working = []
        self.__grammar = []  # Grammar()

    def momentary_insuccess(self):
        # print("---momentary insuccess---")
        self.__state = "b"

    def back(self):
        # print("---back---")
        production = self.__working.pop()
        self.__input = [production] + self.__input
        self.__index -= 1

    def another_try(self):
        # print("---another try---")
        last_nt = self.__working.pop()  # (nt, production_nr)
        if last_nt[1] + 1 < len(self.__grammar): #.get_productions_for_non_terminal(last_nt[0])):
            self.__state = "q"
            # put working next production for the nt
            next_production = (last_nt[0], last_nt[1] + 1)
            self.__working.append(next_production)
            # change production on top input
            len_last_production = len(self.__grammar) #.get_productions_for_non_terminal(last_nt[0])[last_nt[1]])
            # delete last production from input
            self.__input = self.__input[len_last_production:]
            # put new production in input
            next_production = self.__grammar#.get_productions_for_non_terminal(last_nt[0])[last_nt[1] + 1]
            self.__input = next_production + self.__input
        elif self.__index == 1 and last_nt[0] == self.__grammar:#.get_start_symbol():
            self.__state = "e"
        else:
            # change production on top input
            len_last_production = len(self.__grammar)#.get_productions_for_non_terminal(last_nt[0])[last_nt[1]])
            # delete last production from input
            self.__input = self.__input[len_last_production:]
            self.__input = [last_nt[0]] + self.__input
