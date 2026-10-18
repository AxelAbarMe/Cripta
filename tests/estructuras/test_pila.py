"""Pruebas de Pila

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_pila -v
"""
import unittest

from cripta.estructuras.pila import Pila

class TestPila(unittest.TestCase):
    def test_orden_lifo(self):
        pila = Pila()
        for x in (1, 2, 3):
            pila.push(x)
        self.assertEqual([pila.pop(), pila.pop(), pila.pop()], [3, 2, 1])

    def test_vacia(self):
        pila = Pila()
        self.assertTrue(pila.is_empty())
        self.assertIsNone(pila.pop())
        self.assertIsNone(pila.peek())

    def test_peek_no_quita_el_elemento(self):
        pila = Pila()
        pila.push("a")
        self.assertEqual(pila.peek(), "a")
        self.assertFalse(pila.is_empty())
        self.assertEqual(pila.pop(), "a")

if __name__ == "__main__":
    unittest.main()