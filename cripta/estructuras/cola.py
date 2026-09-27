class Node:
    def __init__(self, value):
        self.value = value
        self.next = None 
        
class Cola:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, value):
        new_node = Node(value)
        if self.rear is None:  # Empty queue
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:  # Queue became empty
            self.rear = None
        return value

    def peek(self):
        return None if self.front is None else self.front.value

    def is_empty(self):
        return self.front is None