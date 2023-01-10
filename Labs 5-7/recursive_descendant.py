class Configuration:
    def __init__(self, starting_symbol):
        self.state = "q"
        self.index = 0
        self.work_stack = []
        self.input_stack = [starting_symbol]


def get_next_production(prod, prods):
    for i in range(len(prods)):
        if prod == prods[i] and i < len(prods) - 1:
            return prods[i + 1]
    return None


def recursive_descendant(grammar, sequence, config):
    while config.state != "f" and config.state != "e":
        if config.state == "q":
            if len(config.input_stack) == 0 and config.index == len(sequence):
                success(config)
            elif len(config.input_stack) == 0:
                momentary_insuccess(config)
            else:
                if config.input_stack[0] in grammar.N:
                    expand(config, grammar)
                else:
                    if config.index == len(sequence):
                        momentary_insuccess(config)
                    elif config.input_stack[0] == "E":
                        config.work_stack.append("E")
                        config.input_stack = config.input_stack[1:]
                    elif config.input_stack[0] == sequence[config.index]:
                        advance(config)
                    else:
                        momentary_insuccess(config)
        else:
            if config.state == "b":
                if config.work_stack[-1] in grammar.E:
                    if config.work_stack[-1] == 'E':
                        terminal = config.work_stack.pop(-1)
                        config.input_stack = [terminal] + config.input_stack
                    else:
                        back(config)
                else:
                    another_try(config, grammar)

    prod_rules = []
    if config.state == "e":
        return False, []
    else:
        for prod in config.work_stack:
            if len(prod) > 1:
                if prod[0] in grammar.P.keys():
                    if prod[1] in grammar.P[prod[0]]:
                        prod_rules.append(prod)

    return True, prod_rules


def expand(config, grammar):
    non_term = config.input_stack[0]
    first_prod_right = grammar.get_productions_for_non_terminal(non_term)[0]
    config.work_stack.append((non_term, first_prod_right))
    config.input_stack = first_prod_right + config.input_stack[1:]


def advance(config):
    config.index += 1
    config.work_stack.append(config.input_stack[0])
    config.input_stack = config.input_stack[1:]


def momentary_insuccess(config):
    config.state = "b"


def back(config):
    config.index = config.index - 1
    terminal = config.work_stack.pop(-1)
    config.input_stack = [terminal] + config.input_stack


def another_try(config, grammar):
    (left, right) = config.work_stack[-1]
    productions = [production for production in grammar.get_productions_for_non_terminal(left)]
    next_prod = get_next_production(right, productions)
    if next_prod:
        config.state = "q"
        config.work_stack.pop(-1)
        config.work_stack.append((left, next_prod))
        config.input_stack = config.input_stack[len(right):]
        config.input_stack = next_prod + config.input_stack
    elif config.index == 0 and left == grammar.S:
        config.state = "e"
    else:
        config.work_stack.pop(-1)
        if right == ["E"]:
            config.input_stack = [left] + config.input_stack
        else:
            config.input_stack = [left] + config.input_stack[len(right):]


def success(config):
    config.state = "f"

