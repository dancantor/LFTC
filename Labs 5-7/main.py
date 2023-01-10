from grammar import Grammar
from parsing_tree import ParsingTree
from recursive_descendant import recursive_descendant
from utils.functions import *


def print_menu():
    print("\n\n-----------------------\n"
          "1) Print grammar\n"
          "2) Print set of productions for a non-terminal\n"
          "3) Check if CFG\n"
          "4) Apply recursive descendant algorithm\n"
          "0) Exit\n"
          "-----------------------\n")


grammar = Grammar.read_from_file("./input/g1.txt")
# grammar = Grammar.readFile("./input/g2.txt")

is_done = False
print_menu()
while not is_done:
    cmd = int(input("cmd>>>"))
    if cmd == 1:
        print(grammar)
    elif cmd == 2:
        print("Give non-terminal>>>")
        nonTerminal = input()
        print(grammar.get_productions_for_non_terminal(nonTerminal))
    elif cmd == 3:
        is_cgf = grammar.is_cfg()
        if is_cgf:
            print("Grammar is CFG")
        else:
            print("Grammar is NOT CGF")
    elif cmd == 4:
        parser = ParsingTree(grammar)
        sequence = read_seq('./input/seq.txt')
        # sequence = read_pif('input/PIF.txt')

        result, productions = recursive_descendant(grammar, sequence, parser.config)
        if result:
            print("Success")
        else:
            print("Error")

        print("Productions\n", productions)

        parser.parse()
        parser.write_tree_to_file("./output/out1")
        # parser.write_tree_to_file("./output/out2")
    elif cmd == 0:
        print("Exit...")
        is_done = True
    else:
        print("Bad command!")
