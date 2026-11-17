"""Pruebas de la vista de la partida: costo de cada salida e indicador de cazador (FR-TER-024).
Se ejecuta con:  py -m unittest tests.modelo.test_vista_partida -v
"""
import unittest

from tests.cripta_cazadores import RANGO_SABUESO, armar_partida, cazador_de

SALIDAS = {
    1: {"E": {"sala": 2, "costo": 250}, "N": {"sala": 3}},
    2: {"O": {"sala": 1, "costo": 250}},
    3: {"S": {"sala": 1}},
}


class TestVistaPartidaTerreno(unittest.TestCase):
    def test_la_vista_trae_el_costo_declarado_y_el_100_por_defecto(self):  # FR-TER-024
        partida, _ = armar_partida(SALIDAS, [])
        costos = {s.direccion: s.costo for s in partida.vista().salidas}
        self.assertEqual(costos, {"E": 250, "N": 100})

    def test_solo_el_cazador_se_marca_como_cazador(self):  # FR-TER-024
        partida, mapa = armar_partida(SALIDAS, [(1, "e-1", RANGO_SABUESO), (1, "e-2", RANGO_SABUESO)])
        cazador_de(mapa, "e-2").comportamiento = "errante"
        marcas = {e.instancia: e.es_cazador for e in partida.vista().enemigos}
        self.assertEqual(marcas, {"e-1": True, "e-2": False})

    def test_un_cazador_sin_rango_valido_tambien_se_marca(self):  # FR-TER-024
        partida, _ = armar_partida(SALIDAS, [(1, "e-1", None)])
        enemigos = partida.vista().enemigos
        self.assertEqual(len(enemigos), 1)
        self.assertTrue(enemigos[0].es_cazador)


if __name__ == "__main__":
    unittest.main()
