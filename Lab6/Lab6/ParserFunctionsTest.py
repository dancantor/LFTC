from Grammar import Grammar
from Parser import DescendentRecursiveParser
from Parser import Configuration


def test_expand():
    print('~~~ TEST FOR EXPAND ~~~\n')
    grammar = Grammar('g2.txt')
    parser = DescendentRecursiveParser(grammar)
    parser.expand()
    print(parser.configuration)


def test_advance():
    print('~~~ TEST FOR ADVANCE ~~~\n')
    grammar = Grammar('g2.txt')
    parser = DescendentRecursiveParser(grammar)
    parser.expand()
    parser.advance()
    print(parser.configuration)


def test_success():
    print('~~~ TEST FOR SUCCESS ~~~\n')
    grammar = Grammar('g2.txt')
    parser = DescendentRecursiveParser(grammar)
    parser.success()
    print(parser.configuration)


def test_momentary_insuccess():
    print('\n~~~ TEST FOR MOMENTARY INSUCCESS ~~~\n')
    grammar = Grammar('g2.txt')
    parser = DescendentRecursiveParser(grammar)
    parser.momentary_insuccess()
    print(parser.configuration)


def test_back():
    print('\n~~~ TEST FOR BACK ~~~\n')
    grammar = Grammar('g2.txt')
    parser = DescendentRecursiveParser(grammar)
    parser.expand()
    parser.advance()
    parser.back()
    print(parser.configuration)


def test_another_try():
    print('\n~~~ TEST FOR ANOTHER TRY ~~~\n')
    grammar = Grammar('g1.txt')
    parser = DescendentRecursiveParser(grammar)
    parser.expand()
    parser.another_try()
    print(parser.configuration)


test_expand()
test_advance()
test_success()
test_momentary_insuccess()
test_back()
test_another_try()