"""Pruebas de ListaEnlazada

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_lista_enlazada -v
"""
import unittest

from cripta.estructuras.lista_enlazada import ListaEnlazada

class TestListaEnlazada(unittest.TestCase):
    def test_agregar_y_buscar(self):
        lista = ListaEnlazada()
        for x in (1, 2, 3):
            lista.agregar(x)
        self.assertTrue(lista.buscar(2))
        self.assertFalse(lista.buscar(9))

    def test_eliminar_cabeza_medio_cola_y_ausente(self):
        lista = ListaEnlazada()
        for x in (1, 2, 3, 4):
            lista.agregar(x)
        for x in (1, 3, 4, 99):
            lista.eliminar(x)
        self.assertTrue(lista.buscar(2))
        for x in (1, 3, 4):
            self.assertFalse(lista.buscar(x))

    def test_vacia_no_falla(self):
        lista = ListaEnlazada()
        lista.eliminar(1)
        self.assertFalse(lista.buscar(1))

if __name__ == "__main__":
    unittest.main()