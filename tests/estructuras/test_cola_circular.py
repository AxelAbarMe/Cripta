"""Pruebas de ColaCircular y de BitacoraMensajes, su único usuario.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_cola_circular -v
"""
import unittest

from cripta.estructuras.cola_circular import ColaCircular, ColaCircularVaciaError
from cripta.modelo.bitacora_mensajes import BitacoraMensajes


class TestColaCircular(unittest.TestCase):
    def test_sacar_de_cola_vacia_lanza_error_propio(self):
        cola = ColaCircular(3)
        with self.assertRaises(ColaCircularVaciaError):
            cola.dequeue()
        with self.assertRaises(ColaCircularVaciaError):
            cola.peek()

    def test_el_error_propio_es_un_index_error(self):
        # Error de programación: se puede atrapar como IndexError, no como CriptaError
        with self.assertRaises(IndexError):
            ColaCircular(3).dequeue()

    def test_capacidad_menor_a_uno_se_rechaza(self):
        with self.assertRaises(ValueError):
            ColaCircular(0)

    def test_llena_sobrescribe_el_mas_antiguo(self):
        cola = ColaCircular(3)
        for x in (1, 2, 3, 4):
            cola.enqueue(x)
        self.assertEqual(cola.elementos(), (2, 3, 4))
        self.assertEqual(cola.dequeue(), 2)
        self.assertEqual(cola.elementos(), (3, 4))


class TestBitacoraMensajes(unittest.TestCase):
    def test_solo_guarda_los_ultimos_mensajes(self):
        bitacora = BitacoraMensajes(capacidad=2)
        for mensaje in ("entras a la sala 1", "una rata te ataca", "derrotas a la rata"):
            bitacora.agregar(mensaje)
        self.assertEqual(bitacora.mensajes(), ("una rata te ataca", "derrotas a la rata"))


if __name__ == "__main__":
    unittest.main()