"""Pruebas de VectorOrdenado: inserción ordenada y búsqueda binaria.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_vector_ordenado -v
"""
import random
import unittest

from cripta.estructuras.vector import VectorOrdenado


class TestVectorOrdenado(unittest.TestCase):
    def test_vacio(self):
        vector = VectorOrdenado()
        self.assertEqual(len(vector), 0)
        self.assertIsNone(vector.buscar(1))
        self.assertFalse(vector.contiene(1))
        self.assertFalse(vector.eliminar(1))
        self.assertEqual(vector.elementos(), ())

    def test_insertar_mantiene_el_orden(self):
        vector = VectorOrdenado()
        for x in (5, 1, 4, 2, 3):
            vector.insertar(x)
        self.assertEqual(vector.elementos(), (1, 2, 3, 4, 5))

    def test_buscar_encuentra_y_no_encuentra(self):
        vector = VectorOrdenado()
        for x in (10, 20, 30):
            vector.insertar(x)
        self.assertEqual(vector.buscar(20), 20)
        self.assertIsNone(vector.buscar(25))
        self.assertTrue(vector.contiene(30))
        self.assertFalse(vector.contiene(5))

    def test_clave_personalizada(self):
        vector = VectorOrdenado(clave=lambda par: par[0])
        for par in ((3, "c"), (1, "a"), (2, "b")):
            vector.insertar(par)
        self.assertEqual(vector.buscar(2), (2, "b"))
        self.assertEqual([p[1] for p in vector.elementos()], ["a", "b", "c"])

    def test_eliminar_primero_medio_ultimo(self):
        vector = VectorOrdenado()
        for x in (1, 2, 3, 4, 5):
            vector.insertar(x)
        self.assertTrue(vector.eliminar(1))
        self.assertTrue(vector.eliminar(3))
        self.assertTrue(vector.eliminar(5))
        self.assertEqual(vector.elementos(), (2, 4))
        self.assertFalse(vector.eliminar(3))

    def test_claves_repetidas_conservan_el_orden_de_insercion(self):
        vector = VectorOrdenado(clave=lambda par: par[0])
        for par in ((1, "a"), (1, "b"), (0, "z"), (1, "c")):
            vector.insertar(par)
        self.assertEqual(vector.elementos(), ((0, "z"), (1, "a"), (1, "b"), (1, "c")))

    def test_aleatorio_todas_las_claves_se_encuentran(self):
        azar = random.Random(5)
        ids = list(range(1, 400))
        azar.shuffle(ids)
        vector = VectorOrdenado()
        for x in ids:
            vector.insertar(x)
        self.assertEqual(vector.elementos(), tuple(range(1, 400)))
        for x in (1, 137, 399):
            self.assertEqual(vector.buscar(x), x)
        self.assertIsNone(vector.buscar(0))
        self.assertIsNone(vector.buscar(400))


if __name__ == "__main__":
    unittest.main()