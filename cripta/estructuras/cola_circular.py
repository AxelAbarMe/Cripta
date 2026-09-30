class ColaCircular:
    def __init__(self, size):
        self.size = size
        self.data = [None] * size
        self.front = 0
        self.rear = 0
        self.count = 0

    def enqueue(self, value):
        # Si la cola está llena y entra un nuevo elemento, sobrescribimos el elemento más antiguo
        self.data[self.rear] = value
        self.rear = (self.rear + 1) % self.size
        if self.count == self.size:
            self.front = (self.front + 1) % self.size
        else:
            self.count += 1

    def dequeue(self):
        if self.count == 0:
            raise Exception("Queue is empty")
        value = self.data[self.front]
        self.data[self.front] = None  # Opcional: limpiar la referencia para ayudar al recolector de basura
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return value

    def peek(self):
        if self.count == 0:
            raise Exception("Queue is empty")
        return self.data[self.front]

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.size

    def __len__(self):
        return self.count

    def elementos(self):
        # Del más antiguo al más reciente, sin exponer front/rear al que llama
        return tuple(self.data[(self.front + i) % self.size] for i in range(self.count))