from Parser import Configuration


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

    def build_tree_from_configuration(self, configuration: Configuration):
        return
        #TODO