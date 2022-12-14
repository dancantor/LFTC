import re


class Grammar:
    def __init__(self, _filename):
        self.filename = _filename
        self.non_terminals_set = []
        self.terminals_set = []
        self.productions = {}
        self.starting_symbols = []
        self.read_grammar_from_file()

    def read_grammar_from_file(self):
        with open(self.filename, 'r') as program:
            line_count = -1
            start_of_productions = False
            start_of_starting_symbols = False
            for line in program:
                line = line.replace('\n', '')
                if line_count == 0:
                    for non_terminal in re.split('[ ,{}\n]', line):
                        if non_terminal != '':
                            self.non_terminals_set.append(non_terminal)
                if line_count == 1:
                    for terminal in re.split('[ ,{}\n]', line):
                        if terminal != '':
                            self.terminals_set.append(terminal)
                if line == 'start':
                    start_of_productions = True
                    continue
                if line == 'end':
                    start_of_productions = False
                    start_of_starting_symbols = True
                    continue
                if start_of_productions:
                    [left_side, right_side] = line.split(' -> ')
                    right_side_split = right_side.split(' | ')
                    self.productions[left_side] = []
                    for index, symbols in enumerate(right_side_split):
                        self.productions[left_side].append(re.split('(->|==|!=|\+=|-=|\*=|\/=|<=|>=|[ \+\-\*=\/<>!;\[\]\{\}\(\),;\n]|\|\||&&)', symbols))
                if start_of_starting_symbols:
                    for starting_symbol in re.split('[ ,{}\n]', line):
                        if starting_symbol != '':
                            self.starting_symbols.append(starting_symbol)
                line_count += 1

    def check_if_context_free_grammar(self):
        for left_side in self.productions.keys():
            if self.nr_of_symbols(left_side) > 1:
                return False
        return True

    def check_if_nonterminal(self, expression):
        if expression in self.non_terminals_set:
            return True
        return False

    def check_if_terminal(self, expression):
        if expression in self.terminals_set:
            return True
        return False

    def nr_of_symbols(self, symbols):
        count = 0
        for non_terminal in self.non_terminals_set:
            if non_terminal in symbols.split(' '):
                count += 1
        for terminal in self.terminals_set:
            if terminal in symbols:
                count += 1
        return count

    def __str__(self):
        grammar_string = ''
        grammar_string += f"N = {{{', '.join(self.non_terminals_set)}}}\n"
        grammar_string += f"E = {{{', '.join(self.terminals_set)}}}\n"
        grammar_string += f"P: \n"
        for key, value in self.productions.items():
            grammar_string += f"{key} -> "
            for symbols in value:
                grammar_string += ''.join(symbols) + ' | '
            grammar_string = grammar_string[:-3]
            grammar_string += '\n'
        grammar_string += f"S = {{{', '.join(self.starting_symbols)}}}"
        return grammar_string


# grammar = Grammar('g2.txt')
# print(grammar)
# print(grammar.check_if_context_free_grammar())
#
# grammar_no_context_free = Grammar('g1.txt')
# print(grammar_no_context_free)
# print(grammar_no_context_free.check_if_context_free_grammar())

