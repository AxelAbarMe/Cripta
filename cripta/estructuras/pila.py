class Node:
    def __init__(self, value):
        self.value = value
        self.next = None 

class Pila:
    def __init__(self):
        self.top = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self):
        return None if self.top is None else self.top

    def is_empty(self):
        return self.top is None
    
    