import copy


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self):
        self.capacity = 7
        self.nr_of_values = 0
        self.list_of_values = [None] * 7

    def hash(self, k):
        if isinstance(k, int):
            return k % self.capacity
        sum = 0
        for letter in k:
            sum += ord(letter)
        return sum % self.capacity

    def insert(self, key, value):
        if self.nr_of_values != 0 and self.capacity // self.nr_of_values < 2:
            self.extend_capacity()
        node = self.list_of_values[self.hash(key)]
        if node is None:
            self.list_of_values[self.hash(key)] = Node(key, value)
            self.nr_of_values += 1
            return
        if node.key == key:
            node.value = value
            self.nr_of_values += 1
            return
        while node.next is not None:
            if node.key == key:
                node.value = value
                self.nr_of_values += 1
                return
            node = node.next
        node.next = Node(key, value)
        self.nr_of_values += 1

    def get(self, key):
        node = self.list_of_values[self.hash(key)]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def extend_capacity(self):
        self.capacity *= 2
        self.recompute_hash()

    def recompute_hash(self):
        copy_list = copy.deepcopy(self.list_of_values)
        self.list_of_values = [None] * self.capacity
        self.nr_of_values = 0
        for node in copy_list:
            copy_node = copy.deepcopy(node)
            while copy_node is not None:
                self.insert(copy_node.key, copy_node.value)
                copy_node = copy_node.next

    def get_position(self, key):
        node = self.list_of_values[self.hash(key)]
        position = 0
        while node is not None:
            if node.key == key:
                return self.hash(key), position
            node = node.next
            position = position + 1
        return None

    def __str__(self):
        string_builder = ""
        for node in self.list_of_values:
            while node is not None:
                string_builder += f"{node.key} - {node.value}\n"
                node = node.next
        return string_builder

map = HashTable()

map.insert('ab', 3)
map.insert('ac', 3)
map.insert('aac', 19)
map.insert('abb', 20)
map.insert('a', 5)
map.insert('ae', 13)

