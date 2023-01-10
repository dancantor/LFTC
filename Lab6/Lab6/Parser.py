import copy

from Grammar import Grammar
from Representation import ParsingTree


class Configuration:
    def     __init__(self, starting_symbol):
        self.s = 'q'
        self.i = 0
        self.working_stack: list = ['eps']
        self.input_stack: list = starting_symbol.copy()
    def __str__(self):
        return f"s={self.s}\ni={self.i}\nworking_stack={self.working_stack}\ninput_stack={self.input_stack}"

    def get_head_of_input_stack(self):
        return self.input_stack[0]

    def get_head_of_work_stack(self):
        return self.working_stack[len(self.working_stack) - 1]


class DescendentRecursiveParser:
    def __init__(self, _grammar):
        self.grammar = _grammar
        self.configuration = Configuration(self.grammar.starting_symbols)

    def expand(self):
        head_of_input_stack = self.configuration.input_stack[0]
        self.configuration.working_stack.append((head_of_input_stack, 0))
        self.configuration.input_stack.pop(0)
        copy_production = self.grammar.productions[head_of_input_stack][0]
        copy_production.extend(self.configuration.input_stack)
        self.configuration.input_stack = list(filter(lambda a: a != '', copy_production))
        if self.configuration.working_stack[0] == 'eps':
            self.configuration.working_stack = self.configuration.working_stack[1:]

    def advance(self):
        head_of_input_stack = self.configuration.input_stack[0]
        self.configuration.i += 1
        self.configuration.working_stack.append(head_of_input_stack)
        self.configuration.input_stack.pop(0)
        if len(self.configuration.input_stack) == 0:
            self.configuration.input_stack.append('eps')

    def success(self):
        self.configuration.s = 'f'

    def momentary_insuccess(self):
        # print("---momentary insuccess---")
        self.configuration.s = "b"

    def back(self):
        # print("---back---")
        production = self.configuration.working_stack.pop()
        self.configuration.input_stack = [production] + self.configuration.input_stack
        self.configuration.i -= 1

    def another_try(self):
        # print("---another try---")
        last_nt = self.configuration.working_stack.pop()  # (nt, production_nr)
        if last_nt[1] + 1 < len(self.grammar.productions[last_nt[0]]):  # .get_productions_for_non_terminal(last_nt[0])):
            self.configuration.s = "q"
            # put working next production for the nt
            next_production = (last_nt[0], last_nt[1] + 1)
            self.configuration.working_stack.append(next_production)
            # change production on top input
            len_last_production = len(self.grammar.productions[last_nt[0]][last_nt[1]])  # .get_productions_for_non_terminal(last_nt[0])[last_nt[1]])
            # delete last production from input
            self.configuration.input_stack = self.configuration.input_stack[len_last_production:]
            # put new production in input
            next_production = self.grammar.productions[last_nt[0]][last_nt[1] + 1]  # .get_productions_for_non_terminal(last_nt[0])[last_nt[1] + 1]
            self.configuration.input_stack = list(filter(lambda a: a != ' ', (next_production + self.configuration.input_stack)))
        elif self.configuration.i == 0 and last_nt[0] == self.grammar.starting_symbols[0]:  # .get_start_symbol():
            self.configuration.s = "e"
        else:
            # change production on top input
            len_last_production = len(self.grammar.productions[last_nt[0]][last_nt[1]])  # .get_productions_for_non_terminal(last_nt[0])[last_nt[1]])
            # delete last production from input_stack
            self.configuration.input_stack = self.configuration.input_stack[len_last_production:]
            self.configuration.input_stack = [last_nt[0]] + self.configuration.input_stack

    def descendent_recursive_algorithm(self, word='', filename=''):
        if filename != '':
            with open(filename, 'r') as program:
                word = program.read()
        while self.configuration.s != 'f' and self.configuration.s != 'e':
            if self.configuration.s == 'q':
                if self.configuration.i == len(word) and self.configuration.input_stack[0] == 'eps':
                    self.success()
                else:
                    if self.grammar.check_if_nonterminal(self.configuration.get_head_of_input_stack()):
                        self.expand()
                    elif self.configuration.get_head_of_input_stack() == word[self.configuration.i]:
                        self.advance()
                    else:
                        self.momentary_insuccess()
            elif self.configuration.s == 'b':
                if self.grammar.check_if_terminal(self.configuration.get_head_of_work_stack()):
                    self.back()
                else:
                    self.another_try()
        if self.configuration.s == 'e':
            print(self.configuration)
            return "Error on parsing the sequence"
        # representation = ParsingTree().build_tree_from_configuration()
        # return representation
        print(self.configuration)


grammar = Grammar('g2.txt')
parser = DescendentRecursiveParser(grammar)
parser.descendent_recursive_algorithm(filename='p1.rg.txt')
