"""Pruebas de a_estado_guardado (J9, etapa 1: de la partida viva a EstadoPartida), con la cripta real de fixtures/.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.modelo.test_guardado_ida -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.estado_guardado import (
    EV_ANTORCHA_APAGAR, EV_CIERRE_PUERTA, EV_REARME_TRAMPA, EV_TURNO_ACTOR,
)
from cripta.infraestructura.guardado_binario import GuardadoBinario
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga

VERSION_CATALOGO = "cat-prueba"


def crear_partida(semilla=5):
    cliente = ClienteOffline("fixtures")
    general = cliente.obtener_general("cripta-01")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "cripta-01", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(general.paginas)
    partida = Partida(general, mapa, catalogo, precarga, semilla)
    partida._jugador.vida_max = partida._jugador.vida = 1000   # para que las ratas no maten durante la prueba
    partida.iniciar()
    return partida, mapa, catalogo


def tipos(estado):
    return [(e.tipo, e.sujeto) for e in estado.eventos]


class PruebaGuardadoIda(unittest.TestCase):
    def test_estado_inicial(self):
        p, _, _ = crear_partida()
        e = p.a_estado_guardado(VERSION_CATALOGO)
        self.assertEqual((e.cripta_id, e.catalogo_version, e.semilla), ("cripta-01", VERSION_CATALOGO, 5))
        self.assertEqual((e.reloj_actual, e.acciones_jugador, e.enemigos_derrotados), (0, 0, 0))
        self.assertEqual((e.jugador.sala_actual, e.jugador.tiempo_siguiente, e.jugador.objetos), (1, 0, ()))
        self.assertEqual(e.jugador.indice_cursor, -1)
        cargadas = [s.sala_id for s in e.salas if s.contenido_cargado]
        self.assertEqual(cargadas, [1])                       # solo la sala a la que llegó el jugador
        self.assertEqual(e.salas[0].rastro, 0)
        self.assertEqual([s.rastro for s in e.salas[1:]], [-1] * (len(e.salas) - 1))
        self.assertEqual(e.eventos, ())                       # al jugador le toca decidir: no hay nada pendiente

    def test_tras_entrar_a_una_sala_con_enemigos_y_trampa(self):
        p, _, _ = crear_partida()
        p.ejecutar_accion(A("mover", "N"))
        e = p.a_estado_guardado(VERSION_CATALOGO)
        sala2 = next(s for s in e.salas if s.sala_id == 2)
        self.assertTrue(sala2.contenido_cargado)
        self.assertEqual([(x.instancia_id, x.activo) for x in sala2.enemigos], [("e-201", True), ("e-202", True)])
        self.assertFalse(sala2.trampas[0].armada)             # la pisó al entrar
        self.assertIn((EV_REARME_TRAMPA, sala2.trampas[0].instancia_id), tipos(e))
        self.assertIn((EV_TURNO_ACTOR, "e-201"), tipos(e))
        self.assertEqual(e.reloj_actual, e.jugador.tiempo_siguiente)   # el jugador está en su turno
        self.assertEqual(e.jugador.sala_actual, 2)

    def test_puerta_con_cierre_automatico_y_antorcha(self):
        p, mapa, cat = crear_partida()
        p.ejecutar_accion(A("recoger", "itm_antorcha"))
        p.ejecutar_accion(A("usar", 0))
        e = p.a_estado_guardado(VERSION_CATALOGO)
        self.assertIn((EV_ANTORCHA_APAGAR, "antorcha"), tipos(e))
        p.ejecutar_accion(A("mover", "N"))
        p._jugador.inventario.recoger(ObjetoInventario("k1", cat.obtener("itm_llave_bronce")))
        p.ejecutar_accion(A("abrir", "E"))
        e = p.a_estado_guardado(VERSION_CATALOGO)
        cierre = [x for x in e.eventos if x.tipo == EV_CIERRE_PUERTA]
        self.assertEqual([(x.sujeto, x.a) for x in cierre], [("2", 2)])   # sala 2, dirección E (índice 2)
        sala2 = next(s for s in e.salas if s.sala_id == 2)
        self.assertEqual(sala2.puertas_cerradas, (False, False, False, False))
        self.assertEqual(e.jugador.objetos[0].ficha_id, "itm_llave_bronce")

    def test_cada_evento_pendiente_se_puede_guardar_y_el_archivo_hace_ida_y_vuelta(self):
        p, mapa, _ = crear_partida(semilla=11)
        for accion in [A("mover", "N"), A("esperar"), A("esperar"), A("atacar", "e-201"), A("esperar")]:
            p.ejecutar_accion(accion)
        e = p.a_estado_guardado(VERSION_CATALOGO)
        self.assertEqual(len(e.eventos), len(p._reloj.eventos_vigentes()))
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "partida.bin"
            GuardadoBinario().guardar(ruta, e)
            self.assertEqual(GuardadoBinario().cargar(ruta), e)
            self.assertEqual(GuardadoBinario().cargar_sala(ruta, 2), next(s for s in e.salas if s.sala_id == 2))

    def test_misma_semilla_y_acciones_dan_el_mismo_estado(self):
        guiones = [A("mover", "N"), A("esperar"), A("atacar", "e-201"), A("esperar")]
        estados = []
        for _ in range(2):
            p, _, _ = crear_partida(semilla=3)
            for accion in guiones:
                p.ejecutar_accion(accion)
            estados.append(p.a_estado_guardado(VERSION_CATALOGO))
        self.assertEqual(estados[0], estados[1])

    def test_no_se_guarda_una_partida_terminada(self):
        p, _, _ = crear_partida()
        p._jugador.vida = 1
        p._jugador.vida_max = 1
        p.ejecutar_accion(A("mover", "N"))
        for _ in range(6):
            if p.desenlace() != "en_curso":
                break
            p.ejecutar_accion(A("esperar"))
        self.assertEqual(p.desenlace(), "derrota")
        with self.assertRaises(RuntimeError):
            p.a_estado_guardado(VERSION_CATALOGO)


if __name__ == "__main__":
    unittest.main()