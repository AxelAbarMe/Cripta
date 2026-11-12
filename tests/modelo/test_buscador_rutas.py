"""Pruebas de BuscadorRutas (T026) sobre grafos sintéticos armados dentro de la prueba.
Se asume decidir_paso(cazador, sala_jugador_id, mapa) con resultado (tipo, direccion, costo).
Se ejecuta desde la raíz del proyecto con:  py -m unittest tests.modelo.test_buscador_rutas -v
"""
import unittest
from types import SimpleNamespace as N

from cripta.modelo.buscador_rutas import BuscadorRutas
from tests.modelo.test_cazador_decisiones import RANGO_ESPECTRO, RANGO_SABUESO, construir_mapa

# Cinco salas con costos distintos. Desde la 1 las distancias son 2:50, 3:120, 4:200 y 5:210 (por la 4, no por la 2)
CONEXIONES = [(1, "E", 2, 50), (2, "E", 3, 70), (1, "N", 4, 200), (4, "E", 5, 10), (5, "S", 2, 400)]
DISTANCIAS = {1: 0, 2: 50, 3: 120, 4: 200, 5: 210}


def calculado(rango_max, sala_jugador=1):
    mapa = construir_mapa(CONEXIONES)
    buscador = BuscadorRutas()
    buscador.calcular_o_reutilizar(mapa, sala_jugador, rango_max)
    return buscador, mapa


class TestDistancias(unittest.TestCase):
    def test_distancias_de_costo_minimo_en_un_grafo_de_cinco_salas(self):  # FR-TER-010
        buscador, _ = calculado(RANGO_ESPECTRO)
        for sala, esperada in DISTANCIAS.items():
            self.assertEqual(buscador.distancia(sala), esperada, f"sala {sala}")

    def test_la_poda_no_pierde_ninguna_sala_con_distancia_dentro_del_rango(self):  # FR-TER-010
        for rango_max in (50, 120, 200, 210):
            buscador, _ = calculado(rango_max)
            for sala, real in DISTANCIAS.items():
                if real <= rango_max:
                    self.assertEqual(buscador.distancia(sala), real, f"sala {sala} con rango {rango_max}")

    def test_las_salas_fuera_del_rango_quedan_sin_distancia_o_con_una_mayor_al_rango(self):  # FR-TER-010
        buscador, _ = calculado(100)
        for sala, real in DISTANCIAS.items():
            if real > 100:
                distancia = buscador.distancia(sala)
                self.assertTrue(distancia is None or distancia > 100, f"sala {sala}: {distancia}")


class TestDesempate(unittest.TestCase):
    def test_con_dos_vecinas_empatadas_elige_la_de_menor_id_aunque_no_sea_la_primera_direccion(self):  # FR-TER-013
        # Desde la 1 al jugador en la 4: por la 3 (norte) o por la 2 (este) cuesta 100 en ambos casos
        mapa = construir_mapa([(1, "N", 3, 40), (3, "E", 4, 60), (1, "E", 2, 60), (2, "N", 4, 40)])
        cazador = N(sala_actual=1, rango=RANGO_SABUESO)
        self.assertEqual(BuscadorRutas().decidir_paso(cazador, 4, mapa), ("mover", "E", 60))

    def test_con_dos_vecinas_empatadas_elige_la_de_menor_id_tambien_si_esta_al_norte(self):  # FR-TER-013
        mapa = construir_mapa([(1, "N", 2, 40), (2, "E", 4, 60), (1, "E", 3, 60), (3, "N", 4, 40)])
        cazador = N(sala_actual=1, rango=RANGO_SABUESO)
        self.assertEqual(BuscadorRutas().decidir_paso(cazador, 4, mapa), ("mover", "N", 40))


class TestDecidirPaso(unittest.TestCase):
    def test_elige_el_primer_paso_de_la_ruta_de_menor_costo(self):  # FR-TER-010, FR-TER-012
        mapa = construir_mapa(CONEXIONES)
        cazador = N(sala_actual=5, rango=RANGO_SABUESO)
        self.assertEqual(BuscadorRutas().decidir_paso(cazador, 1, mapa), ("mover", "O", 10))

    def test_sin_salidas_abiertas_espera_con_costo_100(self):  # FR-TER-011
        mapa = construir_mapa(CONEXIONES)
        mapa.cerrar_puerta(1, "E")
        mapa.cerrar_puerta(1, "N")
        cazador = N(sala_actual=1, rango=RANGO_SABUESO)
        self.assertEqual(BuscadorRutas().decidir_paso(cazador, 3, mapa), ("esperar", None, 100))

    def test_con_distancia_mayor_al_rango_espera_con_costo_100(self):  # FR-TER-011
        mapa = construir_mapa([(1, "E", 2, 490), (2, "E", 3, 490)])
        cazador = N(sala_actual=1, rango=RANGO_SABUESO)
        self.assertEqual(BuscadorRutas().decidir_paso(cazador, 3, mapa), ("esperar", None, 100))

    def test_con_distancia_igual_al_rango_se_mueve(self):  # FR-TER-011, FR-TER-012
        mapa = construir_mapa([(1, "E", 2, 300), (2, "E", 3, 300)])
        cazador = N(sala_actual=1, rango=RANGO_SABUESO)
        self.assertEqual(BuscadorRutas().decidir_paso(cazador, 3, mapa), ("mover", "E", 300))


class TestReutilizacionEInvalidacion(unittest.TestCase):
    def test_sin_invalidar_la_tabla_se_reutiliza_y_no_se_recalcula(self):  # FR-TER-015
        buscador, mapa = calculado(RANGO_ESPECTRO)
        mapa.cerrar_puerta(1, "E")     # un cambio que el buscador no sabe, si recalculara lo vería
        buscador.calcular_o_reutilizar(mapa, 1, RANGO_ESPECTRO)
        self.assertEqual(buscador.distancia(2), 50)

    def test_invalidar_fuerza_el_recalculo_en_la_siguiente_consulta(self):  # FR-TER-015
        buscador, mapa = calculado(RANGO_ESPECTRO)
        mapa.cerrar_puerta(1, "E")
        buscador.invalidar()
        buscador.calcular_o_reutilizar(mapa, 1, RANGO_ESPECTRO)
        self.assertEqual(buscador.distancia(2), 610)    # ahora solo se llega por 1, 4, 5 y 2
        self.assertEqual(buscador.distancia(3), 680)

    def test_un_rango_mayor_al_calculado_recalcula(self):  # FR-TER-013, FR-TER-015
        buscador, mapa = calculado(100)
        buscador.calcular_o_reutilizar(mapa, 1, RANGO_ESPECTRO)
        self.assertEqual(buscador.distancia(5), 210)

    def test_un_rango_menor_o_igual_al_calculado_reutiliza(self):  # FR-TER-015
        buscador, mapa = calculado(RANGO_ESPECTRO)
        mapa.cerrar_puerta(1, "E")
        buscador.calcular_o_reutilizar(mapa, 1, 100)
        self.assertEqual(buscador.distancia(2), 50)

    def test_solo_recorre_salidas_abiertas_en_ese_instante(self):  # FR-TER-010, FR-TER-014
        mapa = construir_mapa(CONEXIONES)
        mapa.cerrar_puerta(2, "E")
        buscador = BuscadorRutas()
        buscador.calcular_o_reutilizar(mapa, 1, RANGO_ESPECTRO)
        self.assertIsNone(buscador.distancia(3))


if __name__ == "__main__":
    unittest.main()
