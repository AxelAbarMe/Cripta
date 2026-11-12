"""Equivalencia de la reutilización (T026b, FR-TER-015): en cada turno de cada cazador, la decisión del
buscador que reutiliza su tabla debe ser igual a la de un buscador nuevo que calcula desde cero.
Cripta sintética en cuadrícula con costos por semilla. Se ejecuta con:
    py -m unittest tests.modelo.test_equivalencia_rutas -v
"""
import random
import unittest
from types import SimpleNamespace as N

from cripta.modelo.buscador_rutas import BuscadorRutas
from tests.modelo.test_cazador_decisiones import RANGO_ESPECTRO, RANGO_SABUESO, construir_mapa

LADO = 6
PASOS = 250
SEMILLAS = (1, 2, 3, 4, 5, 6)


def conexiones_de_cuadricula(azar):
    conexiones = []
    for fila in range(LADO):
        for columna in range(LADO):
            sala = fila * LADO + columna + 1
            if columna < LADO - 1:
                conexiones.append((sala, "E", sala + 1, azar.randint(20, 490)))
            if fila < LADO - 1:
                conexiones.append((sala, "S", sala + LADO, azar.randint(20, 490)))
    return conexiones


def puertas_de(mapa):
    """Cada conexión una sola vez: (sala, direccion) del lado de menor id."""
    puertas = []
    for sala in mapa.todas_las_salas():
        for direccion, destino in mapa.vecinos(sala.id):
            if sala.id < destino:
                puertas.append((sala.id, direccion))
    return puertas


def vecino_por(mapa, sala_id, direccion):
    for dir_vecina, destino in mapa.vecinos(sala_id):
        if dir_vecina == direccion:
            return destino
    raise AssertionError("dirección sin salida")


class Escenario:
    """Una secuencia de eventos del juego decidida solo por la semilla."""

    def __init__(self, semilla):
        self.azar = random.Random(semilla)
        self.mapa = construir_mapa(conexiones_de_cuadricula(self.azar))
        self.puertas = puertas_de(self.mapa)
        self.jugador = 1
        self.reutilizado = BuscadorRutas()
        self.cazadores = [
            N(sala_actual=self.azar.randint(2, LADO * LADO), rango=self.azar.choice((RANGO_SABUESO, RANGO_ESPECTRO)),
              activo=False, vivo=True)
            for _ in range(8)
        ]
        self.decisiones = 0
        self.movimientos = 0

    def mover_jugador(self):
        abiertas = [d for d, _ in self.mapa.vecinos(self.jugador) if self.mapa.puerta_transitable(self.jugador, d)]
        if abiertas:
            self.jugador = vecino_por(self.mapa, self.jugador, self.azar.choice(abiertas))
            self.reutilizado.invalidar()

    def cambiar_puerta(self):
        sala, direccion = self.azar.choice(self.puertas)
        if self.mapa.puerta_transitable(sala, direccion):
            self.mapa.cerrar_puerta(sala, direccion)
        else:
            self.mapa.abrir_puerta(sala, direccion)
        self.reutilizado.invalidar()

    def activar_cazador(self):
        dormidos = [c for c in self.cazadores if not c.activo and c.vivo]
        if dormidos:
            self.azar.choice(dormidos).activo = True    # no invalida, un rango mayor lo detecta el buscador

    def matar_cazador(self):
        vivos = [c for c in self.cazadores if c.vivo]
        if vivos:
            self.azar.choice(vivos).vivo = False        # no invalida

    def turno_de_cazadores(self, caso):
        for cazador in self.cazadores:
            if not (cazador.activo and cazador.vivo) or cazador.sala_actual == self.jugador:
                continue
            con_tabla = self.reutilizado.decidir_paso(cazador, self.jugador, self.mapa)
            desde_cero = BuscadorRutas().decidir_paso(cazador, self.jugador, self.mapa)
            caso.assertEqual(con_tabla, desde_cero, f"jugador en {self.jugador}, cazador en {cazador.sala_actual}")
            self.decisiones += 1
            if con_tabla[0] == "mover":
                cazador.sala_actual = vecino_por(self.mapa, cazador.sala_actual, con_tabla[1])
                self.movimientos += 1

    def correr(self, caso):
        eventos = (self.mover_jugador, self.mover_jugador, self.cambiar_puerta, self.activar_cazador,
                   self.activar_cazador, self.matar_cazador)
        for _ in range(PASOS):
            self.azar.choice(eventos)()
            self.turno_de_cazadores(caso)


class TestEquivalenciaDeRutas(unittest.TestCase):
    def test_la_decision_con_reutilizacion_es_igual_a_la_decision_desde_cero(self):  # FR-TER-015
        decisiones = movimientos = 0
        for semilla in SEMILLAS:
            with self.subTest(semilla=semilla):
                escenario = Escenario(semilla)
                escenario.correr(self)
                decisiones += escenario.decisiones
                movimientos += escenario.movimientos
        self.assertGreater(decisiones, 100)      # la prueba no es vacía
        self.assertGreater(movimientos, 20)      # y los cazadores sí persiguieron


if __name__ == "__main__":
    unittest.main()
