class Grammar:
    def __init__(self, N, E, S, P):
        self.N = N
        self.E = E
        self.S = S
        self.P = P

    @staticmethod
    def read_from_file(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            N = Grammar.parse_line(file.readline())
            E = Grammar.parse_line(file.readline())
            S = file.readline().split('=')[1].strip()
            file.readline()
            P = Grammar.parse_production([line.strip() for line in file])

            if not Grammar.validate(N, E, S, P):
                return "Input file does not have the right format!"

            return Grammar(N, E, S, P)

    @staticmethod
    def parse_line(line):
        symbols = []
        for value in line.strip().split('=', 1)[1].strip().split(' '):
            symbols.append(value.strip())
        return symbols

    @staticmethod
    def parse_production(prods):
        productions = {}

        for prod in prods:
            left, right = prod.split('->')
            left = left.strip()
            right = [value.strip().split() for value in right.split('|')]

            for value in right:
                if left in productions.keys():
                    productions[left].append(value)
                else:
                    productions[left] = [value]

        return productions

    @staticmethod
    def validate(N, E, S, P):
        if S not in N:
            return False
        for key in P.keys():
            if key not in N and key not in E:
                return False
            for production in P[key]:
                for elem in production:
                    if elem not in N and elem not in E and elem != 'E':
                        return False
        return True

    def check_if_non_terminal(self, value):
        return value in self.N

    def get_non_terminals(self):
        return ', '.join(self.N)

    def get_terminals(self):
        return ', '.join(self.E)

    def get_productions_for_non_terminal(self, non_terminal):
        if not self.check_if_non_terminal(non_terminal):
            raise Exception('Can only show productions for non-terminals')
        for key in self.P.keys():
            if key == non_terminal:
                return self.P[key]

    def get_all_productions(self):
        return ', '.join([' -> '.join([str(prod), str(self.P[prod])]) for prod in self.P])

    def is_cfg(self):
        for key in self.P.keys():
            if key not in self.N:
                return False
        return True

    def __str__(self):
        return 'N = { ' + self.get_non_terminals() + ' }\n' \
               + 'E = { ' + self.get_terminals() + ' }\n' \
               + 'P = { ' + self.get_all_productions() + ' }\n' \
               + 'S = ' + str(self.S) + '\n'
