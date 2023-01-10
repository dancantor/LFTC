from recursive_descendant import Configuration


class ParsingTreeNode:
    def __init__(self, value, index):
        self.index = index
        self.father = -1
        self.sibling = -1
        self.value = value
        self.production = -1

    def __str__(self):
        return str(self.value) + " " + str(self.father) + " " + str(self.sibling) + " " + str(self.production)


class ParsingTree:
    def __init__(self, grammar):
        self.grammar = grammar
        self.config = Configuration(grammar.S)
        self.iteration = 0
        self.tree = []
        self.words = []

    def parse(self):
        fathers = [-1]
        for index in range(0, len(self.config.work_stack)):
            if type(self.config.work_stack[index]) == tuple:  # non terminal with production
                self.tree.append(ParsingTreeNode(self.config.work_stack[index][0], index))
                self.tree[index].production = self.config.work_stack[index][1]
            else:
                self.tree.append(ParsingTreeNode(self.config.work_stack[index], index))  # terminal

        for index in range(0, len(self.config.work_stack)):
            if type(self.config.work_stack[index]) == tuple:
                self.tree[index].father = fathers[0]
                fathers = fathers[1:]
                len_production = len(self.config.work_stack[index][1])
                child_indexes = []
                for i in range(0, len_production):
                    child_indexes.append(index + i + 1)
                    fathers.insert(0, index)
                for i in range(0, len_production):
                    if self.tree[child_indexes[i]].production != -1:
                        offset = self.get_production_depth(child_indexes[i])
                        for j in range(i + 1, len_production):
                            child_indexes[j] += offset
                for i in range(0, len_production - 1):
                    self.tree[child_indexes[i]].sibling = child_indexes[i + 1]
            else:
                self.tree[index].father = fathers[0]
                fathers = fathers[1:]

    def get_production_depth(self, index):
        prod_right_side = self.config.work_stack[index][1]
        depth = len(prod_right_side)
        for i in range(1, len(prod_right_side) + 1):
            if type(self.config.work_stack[index + i]) == tuple:
                depth += self.get_production_depth(index + i)
        return depth

    def write_tree_to_file(self, filename):
        file = open(filename + ".out", "w")

        for pos in range(0, len(self.config.work_stack)):
            node = self.tree[pos]
            file.write(str(pos) + " " + str(node) + "\n")
        file.close()
