"""Aceptación de US2 y US3 (cazador): ataque, ruta de costo mínimo, desempate, espera, puertas y activación.
Usa criptas sintéticas en memoria (sin datos de ninguna cripta real). Se ejecuta con:
    py -m unittest tests.aceptacion.test_cazador_persecucion -v
"""
import unittest

from cripta.modelo.accion import Accion as A
from cripta.modelo.efectos import EfectoCierrePuerta
from tests.modelo.test_cazador_decisiones import (
    RANGO_ESPECTRO, RANGO_SABUESO, armar_partida, avanzar_hasta, cazador_de, grafo, recorrer,
)


def indices_de_ataque(partida, instancia):
    return [i for i, m in enumerate(partida.mensajes()) if f"[{instancia}]" in m and "te ataca" in m]


class TestAtaqueYRutaDeCostoMinimo(unittest.TestCase):
    def test_cazador_en_la_sala_del_jugador_ataca_con_costo_100(self):  # US2-1, FR-TER-009
        partida, mapa = armar_partida(grafo([(1, "E", 2, 250)]), [(1, "e-1", RANGO_SABUESO)])
        avanzar_hasta(partida, 100)
        self.assertEqual(len(indices_de_ataque(partida, "e-1")), 1)
        self.assertEqual(cazador_de(mapa, "e-1").tiempo_siguiente, 200)

    def test_elige_la_ruta_de_150_y_no_la_directa_de_300(self):  # US2-2, Apéndice B caso 3, FR-TER-010, FR-TER-012
        conexiones = [(1, "E", 2, 300), (1, "N", 3, 50), (3, "E", 4, 50), (4, "S", 2, 50)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 3)                # primer paso de la ruta de 150
        self.assertEqual(cazador.tiempo_siguiente, 100 + 50)    # y su costo es el de esa salida

    def test_el_costo_de_moverse_es_el_de_la_salida_atravesada(self):  # US2-3, FR-TER-012
        partida, mapa = armar_partida(grafo([(1, "E", 2, 330)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 330)

    def test_con_distancia_igual_al_rango_se_mueve(self):  # FR-TER-011, FR-TER-012
        partida, mapa = armar_partida(grafo([(1, "E", 2, 300), (2, "E", 3, 300)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E", "E"])      # distancia 600 y rango 600: la espera exige distancia mayor
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 300)

    def test_en_la_misma_sala_ataca_aunque_el_rango_sea_el_minimo_y_la_sala_este_aislada(self):  # FR-TER-009
        partida, mapa = armar_partida(grafo([(1, "E", 2, 490)]), [(1, "e-1", 1)])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 100)
        self.assertEqual(len(indices_de_ataque(partida, "e-1")), 1)
        self.assertEqual(cazador_de(mapa, "e-1").tiempo_siguiente, 200)


class TestDesempateYEspera(unittest.TestCase):
    def test_dos_vecinas_con_el_mismo_costo_minimo_va_a_la_de_menor_id(self):  # US3-1, Apéndice B caso 4, FR-TER-013
        # El jugador pasa por la 3 hasta la 4. Desde la 1 ambas rutas cuestan 100 y la de menor id es la 2 (este)
        conexiones = [(1, "N", 3, 40), (3, "E", 4, 60), (1, "E", 2, 60), (2, "N", 4, 40)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["N", "E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 60)

    def test_sin_ruta_abierta_espera_con_costo_100(self):  # US3-2, Apéndice B caso 1, FR-TER-011
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_ruta_abierta_pero_distancia_mayor_al_rango_espera_con_costo_100(self):  # US3-3, Apéndice B caso 2, FR-TER-011
        partida, mapa = armar_partida(grafo([(1, "E", 2, 490), (2, "E", 3, 490)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E", "E"])      # distancia 980 contra rango 600
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_una_puerta_de_la_ruta_se_cierra_entre_dos_turnos_y_decide_como_desde_cero(self):  # US3-4, Apéndice B caso 5, FR-TER-015
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100), (2, "E", 3, 100)]), [(1, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E", "E"])
        EfectoCierrePuerta(partida._reloj, mapa, 2, "E", 130, partida._avisar_cierre_de_puerta).programar_cierre()
        avanzar_hasta(partida, 100)       # t=100 la puerta sigue abierta y el cazador avanza a la sala 2
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        avanzar_hasta(partida, 200)       # t=150 la puerta se cierra y en t=200 ya no hay ruta
        self.assertFalse(mapa.puerta_transitable(2, "E"))
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 300)

    def test_el_cazador_no_abre_puertas_cerradas(self):  # US3-5, FR-TER-014
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E"])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 600)
        self.assertEqual(cazador_de(mapa, "e-1").sala_actual, 1)
        self.assertFalse(mapa.puerta_transitable(1, "E"))

    def test_la_niebla_no_le_afecta_cruza_salas_que_el_jugador_nunca_visito(self):  # US3-5, FR-TER-014
        conexiones = [(1, "E", 2, 300), (1, "N", 3, 50), (3, "E", 4, 50), (4, "S", 2, 50)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 190)       # el cazador ya cruzó la 3 y está en la 4, y su turno de t=200 no ocurrió
        self.assertIsNone(mapa.obtener(3).rastro_ultima_visita)
        self.assertIsNone(mapa.obtener(4).rastro_ultima_visita)
        self.assertEqual(cazador_de(mapa, "e-1").sala_actual, 4)


class TestActivacionYMuerte(unittest.TestCase):
    def test_activaciones_simultaneas_programan_sus_primeros_turnos_por_id_de_instancia(self):  # FR-TER-022
        # e-2 se declara antes que e-1 en el contenido, e-1 debe actuar primero
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]),
                                      [(2, "e-2", RANGO_SABUESO), (2, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        primero, segundo = indices_de_ataque(partida, "e-1"), indices_de_ataque(partida, "e-2")
        self.assertEqual((len(primero), len(segundo)), (1, 1))
        self.assertLess(primero[0], segundo[0])

    def test_cazador_en_sala_no_visitada_permanece_dormido(self):  # supuesto de activación, P1 §2.4
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100), (2, "E", 3, 100)]), [(3, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 800)
        for sala in mapa.todas_las_salas():
            self.assertEqual(sala.enemigos_activos, [], f"sala {sala.id}")   # la 3 sigue sin cargar ni activar a nadie

    def test_cazador_dormido_se_activa_cuando_el_jugador_entra_a_su_sala(self):  # supuesto de activación, P1 §2.4
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100), (2, "E", 3, 100)]), [(3, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E", "E"])
        self.assertTrue(cazador_de(mapa, "e-1").activo)

    def test_cazador_que_muere_en_combate_no_actua_en_su_turno_programado(self):  # FR-TER-015
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_SABUESO)])
        cazador = cazador_de(mapa, "e-1")
        cazador.vida = 1
        partida.ejecutar_accion(A("atacar", "e-1"))
        self.assertFalse(cazador.esta_vivo())
        avanzar_hasta(partida, 300)
        self.assertEqual(indices_de_ataque(partida, "e-1"), [])

    def test_cazador_con_vida_cero_y_turno_pendiente_no_produce_ninguna_accion(self):  # FR-TER-015
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_SABUESO)])
        cazador = cazador_de(mapa, "e-1")
        cazador.vida = 0                  # muerto sin cancelar su evento: el turno debe ignorarlo
        avanzar_hasta(partida, 300)
        self.assertEqual(indices_de_ataque(partida, "e-1"), [])
        self.assertEqual(cazador.tiempo_siguiente, 100)


if __name__ == "__main__":
    unittest.main()
