"""Pruebas del reloj virtual: intervalo mínimo, reescalado por cambio de velocidad y desempate por secuencia.
Se ejecuta con:  py -m unittest tests.modelo.test_reloj -v
"""
import unittest

from cripta.modelo.reloj import RelojEventos, calcular_intervalo, calcular_tiempo_reprogramado


class TestCalcularIntervalo(unittest.TestCase):
    def test_costo_1_con_velocidad_alta_da_al_menos_1(self):  # FR-TER-004
        self.assertGreaterEqual(calcular_intervalo(1, 200), 1)
        self.assertEqual(calcular_intervalo(1, 200), 1)
        self.assertEqual(calcular_intervalo(1, 10000), 1)

    def test_costo_y_velocidad_normales(self):  # FR-TER-001
        self.assertEqual(calcular_intervalo(100, 100), 100)
        self.assertEqual(calcular_intervalo(250, 100), 250)
        self.assertEqual(calcular_intervalo(400, 200), 200)


class TestCalcularTiempoReprogramado(unittest.TestCase):
    def test_velocidad_que_sube_acorta_el_tiempo_restante(self):  # FR-TER-005
        # Faltan 300 unidades (400 - 100). Al duplicar la velocidad faltan 150 y el evento cae en 250
        self.assertEqual(calcular_tiempo_reprogramado(400, 100, 100, 200), 250)

    def test_velocidad_que_baja_alarga_el_tiempo_restante(self):  # FR-TER-005
        self.assertEqual(calcular_tiempo_reprogramado(400, 100, 100, 50), 700)

    def test_el_resultado_es_tiempo_absoluto_y_nunca_queda_en_el_pasado(self):  # FR-TER-004, FR-TER-005
        self.assertEqual(calcular_tiempo_reprogramado(101, 100, 100, 1000), 101)
        self.assertGreater(calcular_tiempo_reprogramado(100, 100, 100, 200), 100)


class TestDesempateReloj(unittest.TestCase):
    def test_mismo_instante_gana_la_menor_secuencia(self):  # FR-TER-022
        reloj, orden = RelojEventos(), []
        a = reloj.programar(10, lambda: orden.append("a"))
        b = reloj.programar(10, lambda: orden.append("b"))
        self.assertLess(a.secuencia, b.secuencia)
        reloj.ejecutar_siguiente()
        reloj.ejecutar_siguiente()
        self.assertEqual(orden, ["a", "b"])

    def test_programar_en_otro_orden_no_cambia_el_desempate(self):  # FR-TER-022
        reloj, orden = RelojEventos(), []
        reloj.programar(20, lambda: orden.append("tarde"))
        reloj.programar(10, lambda: orden.append("x"))
        reloj.programar(10, lambda: orden.append("y"))
        while reloj.ejecutar_siguiente() is not None:
            pass
        self.assertEqual(orden, ["x", "y", "tarde"])

    def test_reprogramar_asigna_secuencia_nueva_y_pierde_el_desempate(self):  # FR-TER-005, FR-TER-022
        reloj, orden = RelojEventos(), []
        a = reloj.programar(10, lambda: orden.append("a"))
        reloj.programar(10, lambda: orden.append("b"))
        reloj.programar(10, lambda: orden.append("c"))
        nuevo = reloj.reprogramar(a, 10)
        self.assertGreater(nuevo.secuencia, a.secuencia)
        while reloj.ejecutar_siguiente() is not None:
            pass
        self.assertEqual(orden, ["b", "c", "a"])


if __name__ == "__main__":
    unittest.main()
