"""Pruebas de HeapMinimo

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_heap_min -v
"""
import random
import unittest

from cripta.estructuras.heap_min import HeapMinimo
from cripta.modelo.reloj import EventoProgramado


def vaciar(heap):
    salida = []
    while True:
        valor = heap.eliminar_minimo()
        if valor is None:
            return salida
        salida.append(valor)


class TestHeapMinimo(unittest.TestCase):
    def test_vacio_devuelve_none(self):
        self.assertIsNone(HeapMinimo().eliminar_minimo())

    def test_un_solo_elemento(self):
        heap = HeapMinimo()
        heap.insertar(7)
        self.assertEqual(heap.eliminar_minimo(), 7)
        self.assertIsNone(heap.eliminar_minimo())

    def test_extrae_en_orden_ascendente(self):
        heap = HeapMinimo()
        for x in (5, 3, 8, 1, 9, 2, 7):
            heap.insertar(x)
        self.assertEqual(vaciar(heap), [1, 2, 3, 5, 7, 8, 9])

    def test_duplicados_se_conservan(self):
        heap = HeapMinimo()
        for x in (4, 4, 2, 2, 4):
            heap.insertar(x)
        self.assertEqual(vaciar(heap), [2, 2, 4, 4, 4])

    def test_aleatorio_coincide_con_el_orden_de_referencia(self):
        azar = random.Random(11)
        datos = [azar.randint(0, 50) for _ in range(300)]
        heap = HeapMinimo()
        for x in datos:
            heap.insertar(x)
        self.assertEqual(vaciar(heap), sorted(datos))   # sorted solo como oráculo de la prueba

    def test_intercalar_insertar_y_extraer(self):
        heap = HeapMinimo()
        for x in (10, 4, 6):
            heap.insertar(x)
        self.assertEqual(heap.eliminar_minimo(), 4)
        heap.insertar(1)
        heap.insertar(5)
        self.assertEqual(vaciar(heap), [1, 5, 6, 10])

    def test_empate_de_tiempo_lo_decide_la_secuencia(self):
        # §2.3: menor tiempo y luego menor secuencia, sin importar el orden de inserción
        heap = HeapMinimo()
        for tiempo, secuencia in ((100, 3), (100, 1), (50, 9), (100, 2), (50, 4)):
            heap.insertar(EventoProgramado(tiempo, secuencia, lambda: None))
        self.assertEqual([(e.tiempo, e.secuencia) for e in vaciar(heap)],
                         [(50, 4), (50, 9), (100, 1), (100, 2), (100, 3)])

    def test_muchos_empates_mantienen_el_orden_total(self):
        azar = random.Random(3)
        heap = HeapMinimo()
        pares = [(azar.randint(0, 5), s) for s in range(200)]
        azar.shuffle(pares)
        for tiempo, secuencia in pares:
            heap.insertar(EventoProgramado(tiempo, secuencia, lambda: None))
        obtenidos = [(e.tiempo, e.secuencia) for e in vaciar(heap)]
        self.assertEqual(obtenidos, sorted(pares))


if __name__ == "__main__":
    unittest.main()