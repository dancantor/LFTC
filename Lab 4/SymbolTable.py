from HashTable import HashTable


class SymbolTableConstants:
    def __init__(self):
        self.table = HashTable()

    def add_constant(self, identifier, value):
        self.table.insert(identifier, value)

    def get_constant(self, identifier):
        return self.table.get(identifier)

    def get_position(self, identifier):
        return self.table.get_position(identifier)


class SymbolTableIdentifiers:
    def __init__(self):
        self.table = HashTable()

    def add_identifier(self, identifier, value):
        self.table.insert(identifier, value)

    def get_identifier_value(self, identifier):
        return self.table.get(identifier)

    def get_position(self, identifier):
        return self.table.get_position(identifier)



