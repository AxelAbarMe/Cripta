"""Decisiones del cazador en su turno (T027), sobre criptas sintéticas armadas dentro de la prueba.
Los ayudantes compartidos (grafo, armar_partida...) están en tests/cripta_cazadores.py.
Se ejecuta desde la raíz del proyecto con:  py -m unittest tests.modelo.test_cazador_decisiones -v
"""
import unittest

from tests.cripta_cazadores import (
    RANGO_ESPECTRO, RANGO_SABUESO, armar_partida, avanzar_hasta, cazador_de, grafo, id_ficha, recorrer,
)


class TestDecisionesDelCazador(unittest.TestCase):
    PASILLO = grafo([(1, "E", 2, 250)])

    def test_en_la_misma_sala_ataca_con_costo_100(self):  # FR-TER-009
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertTrue(any("te ataca" in m for m in partida.mensajes()))
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_con_ruta_abierta_y_distancia_dentro_del_rango_se_mueve_con_el_costo_de_la_salida(self):  # FR-TER-012
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 250)

    def test_sin_ruta_abierta_espera_con_costo_100(self):  # FR-TER-011
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_con_distancia_mayor_al_rango_espera_con_costo_100(self):  # FR-TER-011
        largo = grafo([(1, "E", 2, 490), (2, "E", 3, 490)])   # distancia 980 contra rango 600
        partida, mapa = armar_partida(largo, [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E", "E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_el_mismo_mapa_con_rango_2400_si_persigue(self):  # FR-TER-011, FR-TER-012
        largo = grafo([(1, "E", 2, 490), (2, "E", 3, 490)])
        partida, mapa = armar_partida(largo, [(1, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E", "E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 490)

    def test_no_le_afecta_la_niebla_atraviesa_salas_que_el_jugador_no_visito(self):  # FR-TER-014
        conexiones = [(1, "E", 2, 400), (1, "N", 3, 50), (3, "E", 4, 50), (4, "S", 2, 50)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 3)
        self.assertIsNone(mapa.obtener(3).rastro_ultima_visita)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 50)


class TestCazadorSinRango(unittest.TestCase):
    PASILLO = grafo([(1, "E", 2, 100)])

    def test_si_comparte_sala_ataca(self):  # FR-TER-008
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", None)])
        avanzar_hasta(partida, 100)
        self.assertTrue(any("te ataca" in m for m in partida.mensajes()))
        self.assertEqual(cazador_de(mapa, "e-1").tiempo_siguiente, 200)

    def test_si_no_comparte_sala_espera_con_costo_100_aunque_haya_ruta_cercana(self):  # FR-TER-008
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", None)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_al_activarse_agrega_a_la_bitacora_un_aviso_con_el_id_de_la_ficha(self):  # FR-TER-008
        partida, _ = armar_partida(self.PASILLO, [(1, "e-1", None)])
        self.assertTrue(any(id_ficha(None) in m for m in partida.mensajes()))

    def test_un_cazador_con_rango_valido_no_agrega_ese_aviso(self):  # FR-TER-008
        partida, _ = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        self.assertFalse(any(id_ficha(RANGO_SABUESO) in m for m in partida.mensajes()))


if __name__ == "__main__":
    unittest.main()
