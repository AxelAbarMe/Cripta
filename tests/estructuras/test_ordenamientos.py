"""Pruebas de Ordenamiento y del selector automático

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_ordenamientos -v
"""
import random
import unittest

from cripta.estructuras.ordenamiento_selector import (
    UMBRAL_PEQUENO, UMBRAL_PEQUENO_COSTOSA, elegir_algoritmo, medir_desorden, ordenar_auto,
)
from cripta.estructuras.ordenamientos import Ordenamiento

ALGORITMOS = ("insertion_sort", "merge_sort", "quick_sort", "bubble_sort", "selection_sort", "heap_sort")


class Item:
    """Elemento comparable solo por `clave` (como un objeto del inventario); `orden` distingue empates."""
    def __init__(self, clave, orden):
        self.clave, self.orden = clave, orden

    def __lt__(self, otro):
        return self.clave < otro.clave

    def __gt__(self, otro):
        return self.clave > otro.clave


def casos():
    azar = random.Random(21)
    return {
        "vacia": [],
        "un_elemento": [7],
        "dos_invertidos": [2, 1],
        "ordenada": list(range(50)),
        "inversa": list(range(50, 0, -1)),
        "duplicados": [3, 1, 3, 2, 1, 3, 2, 2],
        "todos_iguales": [4] * 20,
        "aleatoria": [azar.randint(0, 100) for _ in range(150)],
    }


class TestOrdenamientos(unittest.TestCase):
    def test_cada_algoritmo_ordena_cada_caso(self):
        for nombre in ALGORITMOS:
            for caso, datos in casos().items():
                with self.subTest(algoritmo=nombre, caso=caso):
                    lista = list(datos)
                    getattr(Ordenamiento(lista), nombre)()
                    self.assertEqual(lista, sorted(datos))   # sorted solo como oráculo de la prueba

    def test_ordena_en_su_sitio_y_conserva_el_mismo_objeto_lista(self):
        lista = [3, 1, 2]
        Ordenamiento(lista).merge_sort()
        self.assertEqual(lista, [1, 2, 3])

    def test_insercion_es_estable(self):
        items = [Item(1, k) if k % 2 else Item(0, k) for k in range(20)]
        Ordenamiento(items).insertion_sort()
        for anterior, actual in zip(items, items[1:]):
            if anterior.clave == actual.clave:
                self.assertLess(anterior.orden, actual.orden)

    def test_merge_es_estable(self):
        # Con empates, el orden original debe conservarse (importa en vistas del inventario por peso/valor)
        items = [Item(k % 3, k) for k in range(30)]
        Ordenamiento(items).merge_sort()
        for anterior, actual in zip(items, items[1:]):
            if anterior.clave == actual.clave:
                self.assertLess(anterior.orden, actual.orden)


class TestSelector(unittest.TestCase):
    def test_medir_desorden_extremos(self):
        self.assertEqual(medir_desorden([]), 0.0)
        self.assertEqual(medir_desorden([1]), 0.0)
        self.assertEqual(medir_desorden([1, 2, 3, 4]), 0.0)
        self.assertEqual(medir_desorden([4, 3, 2, 1]), 1.0)

    def test_medir_desorden_cuenta_pares_adyacentes_fuera_de_orden(self):
        self.assertAlmostEqual(medir_desorden([1, 3, 2, 4, 5]), 1 / 4)

    def test_lista_pequena_usa_insercion(self):
        azar = random.Random(1)
        lista = [azar.randint(0, 99) for _ in range(UMBRAL_PEQUENO)]
        self.assertEqual(elegir_algoritmo(lista), "insercion")

    def test_lista_grande_aleatoria_usa_merge(self):
        azar = random.Random(2)
        lista = [azar.randint(0, 9999) for _ in range(500)]
        self.assertEqual(elegir_algoritmo(lista), "merge")

    def test_lista_grande_casi_ordenada_usa_insercion(self):
        lista = list(range(500))
        lista[10], lista[11] = lista[11], lista[10]
        self.assertEqual(elegir_algoritmo(lista), "insercion")

    def test_lista_grande_inversa_usa_merge(self):
        self.assertEqual(elegir_algoritmo(list(range(500, 0, -1))), "merge")

    def test_comparacion_costosa_baja_el_umbral_de_lista_pequena(self):
        lista = list(range(UMBRAL_PEQUENO_COSTOSA, 0, -1))
        self.assertEqual(elegir_algoritmo(lista, comparacion_costosa=True), "insercion")
        mayor = list(range(UMBRAL_PEQUENO_COSTOSA + 5, 0, -1))
        self.assertEqual(elegir_algoritmo(mayor, comparacion_costosa=True), "merge")

    def test_ordenar_auto_ordena_y_devuelve_el_algoritmo_usado(self):
        azar = random.Random(4)
        for tamano in (5, 200):
            lista = [azar.randint(0, 999) for _ in range(tamano)]
            esperado = sorted(lista)
            usado = ordenar_auto(lista)
            self.assertEqual(lista, esperado)
            self.assertIn(usado, ("insercion", "merge"))


if __name__ == "__main__":
    unittest.main()