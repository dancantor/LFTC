from enum import Enum
import re
from SymbolTable import SymbolTableConstants, SymbolTableIdentifiers


class ScanningService:
    def __init__(self, filename, token_file):
        self.filename = filename
        self.token_file = token_file
        self.constant_table = SymbolTableConstants()
        self.identifiers_table = SymbolTableIdentifiers()
        self.pif = []
        self.reserved_words = []
        self.operators = []
        self.separators = []
        self.get_tokens()
        self.constants_count = 0

    def scan_file(self):
        with open(self.filename, 'r') as program:
            line_count = 0
            for line in program:
                line_count += 1
                line = line.replace('\n', '')
                operators_and_separators = '(->|==|!=|\+=|-=|\*=|\/=|<=|>=|[\+\-\*=\/<>!;\[\]\{\}\(\),;]|\|\||&&)'
                for word_with_sep_and_op in line.split():
                    for word in re.split(operators_and_separators, word_with_sep_and_op):
                        if word == '':
                            continue
                        if word == '->':
                            break
                        if word[0] == '"':
                            word = word[1:]
                        if word in self.reserved_words or word in self.operators or word in self.separators:
                            self.pif.append((word, 0))
                        elif self.is_identifier(word):
                            self.identifiers_table.add_identifier(word, None)
                            self.pif.append((TypeOfToken.IDENTIFIER, self.identifiers_table.get_position(word)))
                        elif self.is_constant(word):
                            self.constant_table.add_constant(self.constants_count, word)
                            self.constants_count += 1
                            self.pif.append((TypeOfToken.CONSTANT, self.constant_table.get_position(self.constants_count - 1)))
                        else:
                            print(f'Lexical error at line {line_count}')
                            return
            print('Lexically correct')
        with open('ST.out', 'w') as output:
            print(str(self.identifiers_table.table))
            output.write(str(self.identifiers_table.table))
        with open('PIF.out', 'w') as output:
            for key, value in self.pif:
                output.write(f"{key} - {value}\n")

    def get_tokens(self):
        should_add_in = TypeOfToken.RESERVED_WORD
        with open(self.token_file, 'r') as token_file:
            for line in token_file:
                line = line.replace('\n', '')
                if line == '[reserved_words]':
                    continue
                if line == '[operators]':
                    should_add_in = TypeOfToken.OPERATOR
                    continue
                if line == '[separators]':
                    should_add_in = TypeOfToken.SEPARATOR
                    continue
                if should_add_in == TypeOfToken.RESERVED_WORD:
                    self.reserved_words.append(line)
                if should_add_in == TypeOfToken.OPERATOR:
                    self.operators.append(line)
                if should_add_in == TypeOfToken.SEPARATOR:
                    self.separators.append(line)

    def is_identifier(self, string):
        pattern = re.compile("[~a-zA-Z][~a-zA-Z0-9]{0,256}")
        return pattern.fullmatch(string)

    def is_constant(self, string):
        pattern_integer = re.compile("0|[+-]?[1-9][0-9]*")
        pattern_char = re.compile("'[a-zA-Z0-9]'")
        pattern_string = re.compile('"[a-zA-Z0-9]*"')
        if pattern_integer.fullmatch(string) or pattern_char.fullmatch(string) or pattern_string.fullmatch(string):
            return True
        return False


class TypeOfToken(Enum):
    RESERVED_WORD = 1
    SEPARATOR = 2
    OPERATOR = 3
    IDENTIFIER = 4
    CONSTANT = 5


scan = ScanningService('p4.rg.txt', 'token.in')
scan.scan_file()
