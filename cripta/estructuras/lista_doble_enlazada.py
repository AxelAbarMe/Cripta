class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class ListaDobleEnlazada:
    def __init__(self):
        self.head = None

    def agregar(self, value):
        new_node = Node(value)
        if self.head is None:  # Empty list
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        new_node.prev = current

    def eliminar(self, value):
        if self.head is None:  # Empty list
            return
        if self.head.data == value:  # Remove head
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            return
        current = self.head
        while current and current.data != value:
            current = current.next
        if current:  # Node found
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev

    def buscar(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False