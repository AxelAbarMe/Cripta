class Ordenamiento:
    def __init__(self, lista):
        self.lista = lista

    def insertion_sort(self):
        for i in range(1, len(self.lista)):
            key = self.lista[i]
            j = i - 1
            while j >= 0 and key < self.lista[j]:
                self.lista[j + 1] = self.lista[j]
                j -= 1
            self.lista[j + 1] = key

    def merge_sort(self):
        if len(self.lista) > 1:
            mid = len(self.lista) // 2
            left_half = self.lista[:mid]
            right_half = self.lista[mid:]

            left_sorter = Ordenamiento(left_half)
            right_sorter = Ordenamiento(right_half)

            left_sorter.merge_sort()
            right_sorter.merge_sort()

            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    self.lista[k] = left_half[i]
                    i += 1
                else:
                    self.lista[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                self.lista[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                self.lista[k] = right_half[j]
                j += 1
                k += 1

    def quick_sort(self):
        self._quick_sort_helper(0, len(self.lista) - 1)

    def _quick_sort_helper(self, low, high):
        if low < high:
            pi = self._partition(low, high)
            self._quick_sort_helper(low, pi - 1)
            self._quick_sort_helper(pi + 1, high)

    def _partition(self, low, high):
        pivot = self.lista[high]
        i = low - 1
        for j in range(low, high):
            if self.lista[j] < pivot:
                i += 1
                self.lista[i], self.lista[j] = self.lista[j], self.lista[i]
        self.lista[i + 1], self.lista[high] = self.lista[high], self.lista[i + 1]
        return i + 1

    def bubble_sort(self):
        n = len(self.lista)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.lista[j] > self.lista[j + 1]:
                    self.lista[j], self.lista[j + 1] = self.lista[j + 1], self.lista[j]

    def selection_sort(self):
        n = len(self.lista)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.lista[j] < self.lista[min_idx]:
                    min_idx = j
            self.lista[i], self.lista[min_idx] = self.lista[min_idx], self.lista[i]

    def heap_sort(self):
        n = len(self.lista)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(n, i)
        for i in range(n - 1, 0, -1):
            self.lista[i], self.lista[0] = self.lista[0], self.lista[i]
            self._heapify(i, 0)

    def _heapify(self, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self.lista[left] > self.lista[largest]:
            largest = left

        if right < n and self.lista[right] > self.lista[largest]:
            largest = right

        if largest != i:
            self.lista[i], self.lista[largest] = self.lista[largest], self.lista[i]
            self._heapify(n, largest)

    