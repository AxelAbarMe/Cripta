"""Pruebas de la decisión del enemigo sobre un mapa pequeño armado a mano.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.modelo.test_comportamiento_enemigo -v
"""
import random
import unittest
from types import SimpleNamespace as N

from cripta.dto.sala_dto import SalaDTO
from cripta.modelo.comportamiento_enemigo import decidir_accion_enemigo
from cripta.modelo.cripta_mapa import CriptaMapa

# Sala 5 al centro con vecinas 2 (N), 8 (S), 6 (E) y 4 (O); la vecina del este está cerrada con llave
SALAS = (
    {"id": 5, "nombre": "Centro", "salidas": {"N": {"sala": 2}, "S": {"sala": 8}, "E": {"sala": 6, "cerrada": True, "llave": "k"},
                                              "O": {"sala": 4}}},
    {"id": 2, "nombre": "Norte", "salidas": {"S": {"sala": 5}}},
    {"id": 8, "nombre": "Sur", "salidas": {"N": {"sala": 5}}},
    {"id": 6, "nombre": "Este", "salidas": {"O": {"sala": 5, "cerrada": True, "llave": "k"}}},
    {"id": 4, "nombre": "Oeste", "salidas": {"E": {"sala": 5}}},
)


def mapa():
    mapa = CriptaMapa()
    mapa.agregar_pagina(N(salas=[SalaDTO.desde_json(s) for s in SALAS]))
    mapa.sincronizar_puertas()
    return mapa


def enemigo(comportamiento, sala=5):
    return N(sala_actual=sala, comportamiento=comportamiento)


class TestDecisionEnemigo(unittest.TestCase):
    def test_comparte_sala_con_el_jugador_ataca(self):
        for comportamiento in ("guardian", "errante", "rastreador"):
            self.assertEqual(decidir_accion_enemigo(enemigo(comportamiento), 5, mapa(), random.Random(1), 0), ("atacar", None))

    def test_guardian_espera(self):
        self.assertEqual(decidir_accion_enemigo(enemigo("guardián"), 2, mapa(), random.Random(1), 0), ("esperar", None))

    def test_errante_nunca_elige_una_puerta_cerrada(self):
        m, azar = mapa(), random.Random(7)
        direcciones = {decidir_accion_enemigo(enemigo("errante"), 99, m, azar, 0)[1] for _ in range(60)}
        self.assertEqual(direcciones, {"N", "S", "O"})

    def test_errante_sin_salidas_abiertas_espera(self):
        self.assertEqual(decidir_accion_enemigo(enemigo("errante", sala=6), 99, mapa(), random.Random(1), 0), ("esperar", None))

    def test_rastreador_sigue_el_rastro_mas_fresco(self):
        m = mapa()
        m.obtener(2).marcar_visita(100)
        m.obtener(8).marcar_visita(250)
        self.assertEqual(decidir_accion_enemigo(enemigo("rastreador"), 99, m, random.Random(1), 300), ("mover", "S"))

    def test_rastreador_con_rastros_iguales_elige_la_sala_de_menor_id(self):
        m = mapa()
        m.obtener(8).marcar_visita(200)
        m.obtener(2).marcar_visita(200)
        m.obtener(4).marcar_visita(200)
        self.assertEqual(decidir_accion_enemigo(enemigo("rastreador"), 99, m, random.Random(1), 300), ("mover", "N"))

    def test_rastro_de_400_o_mas_no_sirve_y_de_399_si(self):
        m = mapa()
        m.obtener(2).marcar_visita(0)
        self.assertEqual(decidir_accion_enemigo(enemigo("rastreador"), 99, m, random.Random(1), 400), ("esperar", None))
        self.assertEqual(decidir_accion_enemigo(enemigo("rastreador"), 99, m, random.Random(1), 399), ("mover", "N"))

    def test_rastreador_ignora_vecinas_con_puerta_cerrada_aunque_tengan_rastro(self):
        m = mapa()
        m.obtener(6).marcar_visita(290)
        self.assertEqual(decidir_accion_enemigo(enemigo("rastreador"), 99, m, random.Random(1), 300), ("esperar", None))

    def test_rastreador_sin_rastro_espera(self):
        self.assertEqual(decidir_accion_enemigo(enemigo("rastreador"), 99, mapa(), random.Random(1), 50), ("esperar", None))


if __name__ == "__main__":
    unittest.main()