from SymbolTable import SymbolTableIdentifiers, SymbolTableConstants


class SymbolTableTests:
    def __init__(self):
        self.run_tests()

    def run_tests(self):
        identifiers = SymbolTableIdentifiers()
        identifiers.add_identifier('ana', 15)
        identifiers.add_identifier('test', 'aeio')
        identifiers.add_identifier('ioan', 13)
        identifiers.add_identifier('bcd', 19)
        identifiers.add_identifier('x', 'a')
        assert identifiers.get_identifier_value('ana') == 15
        assert identifiers.get_identifier_value('test') == 'aeio'
        assert identifiers.get_identifier_value('ioan') == 13
        assert identifiers.get_identifier_value('bcd') == 19
        assert identifiers.get_identifier_value('x') == 'a'

        constants = SymbolTableConstants()
        constants.add_constant(1, 'este')
        constants.add_constant(2, 15)
        constants.add_constant(3, 15.4)
        constants.add_constant(4, 'c')
        constants.add_constant(5, 3)

        assert constants.get_constant(1) == 'este'
        assert constants.get_constant(2) == 15
        assert constants.get_constant(3) == 15.4
        assert constants.get_constant(4) == 'c'
        assert constants.get_constant(5) == 3

tests = SymbolTableTests()
