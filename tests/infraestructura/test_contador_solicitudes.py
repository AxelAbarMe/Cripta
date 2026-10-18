"""Pruebas de ContadorSolicitudes y de su reinicio entre partidas de una misma sesión.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.infraestructura.test_contador_solicitudes -v
"""
import unittest

from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from tests.servicios.test_servicio_partida import CRIPTA, armar


class TestContadorSolicitudes(unittest.TestCase):
    def test_registrar_cuenta_y_descuenta_de_los_restantes(self):
        contador = ContadorSolicitudes(3)
        contador.registrar_solicitud()
        self.assertEqual((contador.realizadas, contador.restantes), (1, 2))

    def test_restantes_nunca_es_negativo(self):
        contador = ContadorSolicitudes(1)
        contador.registrar_solicitud()
        contador.registrar_solicitud()
        self.assertEqual(contador.restantes, 0)

    def test_reiniciar_pone_en_cero_y_conserva_el_presupuesto(self):
        contador = ContadorSolicitudes(9)
        for _ in range(4):
            contador.registrar_solicitud()
        contador.reiniciar()
        self.assertEqual((contador.realizadas, contador.restantes, contador.presupuesto_maximo), (0, 9, 9))

    def test_la_segunda_partida_de_la_sesion_no_suma_las_de_la_primera(self):
        servicio, contador, _ = armar()
        servicio.iniciar_nueva(CRIPTA, 5)
        primera = contador.realizadas
        self.assertGreater(primera, 0)
        servicio.iniciar_nueva(CRIPTA, 5)
        self.assertEqual(contador.realizadas, primera)   # misma cripta y sin caché: mismo gasto, no el doble
        servicio.cerrar()


if __name__ == "__main__":
    unittest.main()