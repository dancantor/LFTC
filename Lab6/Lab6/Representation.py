


class ParsingTreeNode:
    def __init__(self, _index: int, _content: str, _parent, _sibling, _children):
        self.index = _index
        self.content = _content
        self.parent = _parent
        self.right_sibling = _sibling
        self.children = _children

    def get_first_child(self):
        return self.children[0]


class ParsingTree:
    def __init__(self):
        self.nodes_list = []

    def add_node(self, node: ParsingTreeNode):
        self.nodes_list.append(node)

    def build_tree_from_configuration(self, configuration, grammar):
        result_working = []
        parsing_table = []
        for el in configuration.working_stack:
            if type(el) is tuple:
                result_working.append(el)

        node = ParsingTreeNode(0, grammar.starting_symbols[0], -1, -1, [])
        parsing_table.append(node)
        while len(result_working) != 0:
            non_terminal, production_nr = result_working[0]
            result_working = result_working[1:]
            resulted_production = grammar.productions[non_terminal][production_nr]
            for el in resulted_production:
                parsing_table.append(ParsingTreeNode(parsing_table[-1].index + 1, el, ))

