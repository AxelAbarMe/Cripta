class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
class ListaDobleEnlazada:
    def __init__(self):
        self.head = None
        self.tail = None  # puntero al último nodo: evita recorrer la lista para insertar al final

    def agregar(self, value):
        # Insertar al final en O(1), aprovechando que tail siempre está disponible
        new_node = Node(value)
        if self.head is None:  # Lista vacía
            self.head = self.tail = new_node
            return
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def agregar_inicio(self, value):
        # Insertar al inicio en O(1), aprovechando que head siempre está disponible
        new_node = Node(value)
        if self.head is None:  # Lista vacía
            self.head = self.tail = new_node
            return
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def eliminar(self, value):
        if self.head is None:  # Lista vacía
            return
        if self.head.data == value:  # Eliminar la cabeza
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None  # la lista quedó vacía
            return
        current = self.head
        while current and current.data != value:
            current = current.next
        if current:  # Nodo encontrado
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            else:
                self.tail = current.prev  # se eliminó el último nodo: actualizar tail

    def buscar(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False