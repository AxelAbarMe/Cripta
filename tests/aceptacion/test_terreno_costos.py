"""Aceptación de US1 (terreno): el intervalo de tiempo virtual escala con el costo de la salida cruzada.
Usa una cripta sintética en memoria (sin datos de ninguna cripta real). Se ejecuta con:
    py -m unittest tests.aceptacion.test_terreno_costos -v
"""
import unittest

from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.excepciones import CriptaDatosInvalidosError
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.efectos import EfectoCambioVelocidad
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from tests.cliente_falso import ClienteFalso


def _ficha_enemigo(comportamiento):
    return {"id": "ent_x", "clase": "enemigo", "nombre": "Bicho", "vida_max": 1000, "ataque": 1,
            "defensa": 0, "velocidad": 100, "comportamiento": comportamiento}


def crear_partida(salidas, velocidad=100, comportamiento=None, semilla=3):
    """`salidas` es {id_sala: {direccion: {"sala": destino, "costo": opcional}}}. La sala 1 es la inicial.
    Si hay `comportamiento`, la sala 1 empieza con un enemigo de ese comportamiento."""
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    contenido = [{"sala": i, "enemigos": [], "objetos": [], "trampas": []} for i in salidas]
    fichas = []
    if comportamiento is not None:
        contenido[0]["enemigos"] = [{"instancia": "e-1", "tipo": "ent_x"}]
        fichas = [_ficha_enemigo(comportamiento)]
    general = {"id": "c1", "version": "v1", "salas_total": len(salas), "paginas": 1, "salas_por_pagina": 50,
               "sala_inicial": 1, "sala_salida": max(salidas), "llave_salida": "itm_llave",
               "presupuesto_solicitudes": 9, "inventario_max": 10,
               "jugador": {"vida_max": 1000, "ataque": 6, "defensa": 2, "velocidad": velocidad}}
    cliente = ClienteFalso(fichas, contenido, [{"pagina": 1, "total_paginas": 1, "salas": salas}], general)
    datos = cliente.obtener_general("c1")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "c1", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(datos.paginas)
    partida = Partida(datos, mapa, catalogo, precarga, semilla)
    partida.iniciar()
    return partida, mapa


def corredor(costo_ida=None, costo_vuelta=None):
    # Sala 1 y sala 2 unidas por E/O, el costo se puede declarar en un lado, en el otro o en ninguno
    este = {"sala": 2} if costo_ida is None else {"sala": 2, "costo": costo_ida}
    oeste = {"sala": 1} if costo_vuelta is None else {"sala": 1, "costo": costo_vuelta}
    return {1: {"E": este}, 2: {"O": oeste}}


def tiempo(partida):
    return partida.vista().tiempo


class TestTerrenoCostosJugador(unittest.TestCase):
    def test_salida_de_costo_250_cuesta_250_en_ida_y_vuelta(self):  # US1-1, FR-TER-001, FR-TER-002, FR-TER-003
        partida, _ = crear_partida(corredor(costo_ida=250, costo_vuelta=250))
        self.assertTrue(partida.ejecutar_accion(A("mover", "E")).aceptada)
        self.assertEqual(tiempo(partida), 250)
        self.assertTrue(partida.ejecutar_accion(A("mover", "O")).aceptada)
        self.assertEqual(tiempo(partida), 500)

    def test_salida_sin_costo_cuesta_100(self):  # US1-2, FR-TER-001
        partida, _ = crear_partida(corredor())
        partida.ejecutar_accion(A("mover", "E"))
        self.assertEqual(tiempo(partida), 100)
        partida.ejecutar_accion(A("mover", "O"))
        self.assertEqual(tiempo(partida), 200)

    def test_costo_1_con_velocidad_200_da_intervalo_al_menos_1(self):  # US1-3, Apéndice B caso 6, FR-TER-004
        partida, _ = crear_partida(corredor(costo_ida=1, costo_vuelta=1), velocidad=200)
        partida.ejecutar_accion(A("mover", "E"))
        self.assertGreaterEqual(tiempo(partida), 1)
        self.assertEqual(tiempo(partida), 1)

    def test_cambio_de_velocidad_a_mitad_del_cruce_reprograma_a_250(self):  # US1-4, Apéndice B caso 7, FR-TER-005
        partida, _ = crear_partida(corredor(costo_ida=400, costo_vuelta=400))
        jugador = partida._jugador

        def acelerar():
            partida._con_retroceso(EfectoCambioVelocidad(partida._reloj, jugador, 100, 1000)).aplicar()

        partida._reloj.programar(100, acelerar, "velocidad de prueba")
        partida.ejecutar_accion(A("mover", "E"))   # velocidad 100 y costo 400: terminaría en t=400
        self.assertEqual(jugador.velocidad, 200)
        self.assertEqual(tiempo(partida), 250)     # quedaban 300 a velocidad 100, ahora 150 a velocidad 200

    def test_esperar_y_atacar_conservan_costo_100_con_salidas_costosas(self):  # US1-5, FR-TER-006
        salidas = {1: {"E": {"sala": 2, "costo": 250}, "N": {"sala": 3, "costo": 400}},
                   2: {"O": {"sala": 1, "costo": 250}}, 3: {"S": {"sala": 1, "costo": 400}}}
        partida, _ = crear_partida(salidas, comportamiento="guardian")
        partida.ejecutar_accion(A("esperar"))
        self.assertEqual(tiempo(partida), 100)
        self.assertTrue(partida.ejecutar_accion(A("atacar", "e-1")).aceptada)
        self.assertEqual(tiempo(partida), 200)


class TestTerrenoCostosEnemigos(unittest.TestCase):
    SALIDAS_COSTOSAS = {1: {"E": {"sala": 2, "costo": 250}, "N": {"sala": 4, "costo": 250}},
                        2: {"O": {"sala": 1, "costo": 250}}, 4: {"S": {"sala": 1, "costo": 250}}}

    def _enemigo(self, mapa):
        for sala in mapa.todas_las_salas():
            for enemigo in sala.enemigos_activos:
                return enemigo
        self.fail("No quedó ningún enemigo activo")

    def _jugador_cruza_y_enemigo_mueve(self, comportamiento):
        partida, mapa = crear_partida(self.SALIDAS_COSTOSAS, comportamiento=comportamiento)
        partida.ejecutar_accion(A("mover", "E"))   # el jugador queda en la sala 2 en t=250 y el enemigo actuó en t=100
        enemigo = self._enemigo(mapa)
        self.assertNotEqual(enemigo.sala_actual, 1)   # se movió: cruzó una salida de costo 250
        return enemigo

    def test_errante_programa_su_siguiente_turno_con_el_costo_de_la_salida(self):  # US1-6, FR-TER-007
        enemigo = self._jugador_cruza_y_enemigo_mueve("errante")
        self.assertEqual(enemigo.tiempo_siguiente, 100 + 250)
        self.assertEqual(enemigo.evento_pendiente.tiempo, 100 + 250)

    def test_rastreador_programa_su_siguiente_turno_con_el_costo_de_la_salida(self):  # US1-6, FR-TER-007
        enemigo = self._jugador_cruza_y_enemigo_mueve("rastreador")
        self.assertEqual(enemigo.sala_actual, 2)   # sigue el rastro del jugador
        self.assertEqual(enemigo.tiempo_siguiente, 100 + 250)
        self.assertEqual(enemigo.evento_pendiente.tiempo, 100 + 250)


class TestSimetriaDeCostos(unittest.TestCase):
    def test_costo_declarado_solo_en_el_lado_de_ida_rige_en_ambos_sentidos(self):  # FR-TER-002
        partida, _ = crear_partida(corredor(costo_ida=250))
        partida.ejecutar_accion(A("mover", "E"))
        self.assertEqual(tiempo(partida), 250)
        partida.ejecutar_accion(A("mover", "O"))
        self.assertEqual(tiempo(partida), 500)

    def test_costo_declarado_solo_en_el_lado_de_vuelta_rige_en_ambos_sentidos(self):  # FR-TER-002
        partida, _ = crear_partida(corredor(costo_vuelta=250))
        partida.ejecutar_accion(A("mover", "E"))
        self.assertEqual(tiempo(partida), 250)
        partida.ejecutar_accion(A("mover", "O"))
        self.assertEqual(tiempo(partida), 500)

    def test_sin_costo_en_ningun_lado_la_conexion_vale_100(self):  # FR-TER-002
        _, mapa = crear_partida(corredor())
        self.assertEqual((mapa.costo_de_conexion(1, "E"), mapa.costo_de_conexion(2, "O")), (100, 100))

    def test_costos_distintos_en_los_dos_lados_lanzan_error_con_las_salas(self):  # FR-TER-002
        pagina = PaginaEsqueletoDTO.desde_json({"pagina": 1, "total_paginas": 1, "salas": [
            {"id": 1, "nombre": "A", "salidas": {"E": {"sala": 2, "costo": 250}}},
            {"id": 2, "nombre": "B", "salidas": {"O": {"sala": 1, "costo": 300}}},
        ]})
        with self.assertRaises(CriptaDatosInvalidosError) as ctx:
            CriptaMapa().agregar_pagina(pagina)
        self.assertIn("costos distintos", ctx.exception.detalle)
        self.assertIn("1", ctx.exception.detalle)
        self.assertIn("2", ctx.exception.detalle)


if __name__ == "__main__":
    unittest.main()
