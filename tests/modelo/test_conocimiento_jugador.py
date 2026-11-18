"""Pruebas del conocimiento del jugador para la capacidad 002."""
import unittest
from types import SimpleNamespace

from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.sala_dto import SalaDTO
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.historial_retroceso import HistorialRetroceso
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.jugador_inicial_dto import JugadorInicialDTO
from cripta.modelo.partida import Partida
from cripta.modelo.accion import Accion
from cripta.modelo.inventario import ObjetoInventario
from cripta.dto.llave_dto import LlaveDTO
from cripta.modelo.conocimiento_jugador import (
    ConocimientoJugador,
    SalaConocida,
    SalidaConocida,
)


def crear_mapa(salas):
    mapa = CriptaMapa()
    dto = PaginaEsqueletoDTO(
        pagina=1,
        total_paginas=1,
        salas=tuple(SalaDTO.desde_json(sala) for sala in salas),
    )
    mapa.agregar_pagina(dto)
    mapa.sincronizar_puertas()
    return mapa


def salida(destino, costo=100, cerrada=False, llave=None, cierre=None):
    return {
        "sala": destino,
        "costo": costo,
        "cerrada": cerrada,
        "llave": llave,
        "cierre_automatico": cierre,
    }


class PrecargaSintetica:
    def __init__(self, mapa):
        self.mapa = mapa

    def preparar_sala(self, sala_id):
        return self.mapa.obtener(sala_id)

    def precargar_desde(self, sala_id):
        return None


def crear_partida_sintetica(salas, sala_inicial=1):
    mapa = crear_mapa(salas)
    general = CriptaGeneralDTO("sintetica", "1", len(salas), 1, len(salas), sala_inicial,
                               max(s["id"] for s in salas), "llave", 10, 4,
                               JugadorInicialDTO(100, 10, 0, 100))
    partida = Partida(general, mapa, object(), PrecargaSintetica(mapa), 1)
    partida.iniciar()
    return partida


class TestConocimientoInicial(unittest.TestCase):
    """T001: FR-NIE-001, FR-NIE-003 y FR-NIE-008, escenarios 1.1, 1.3 y 1.4, SC-NIE-001."""

    def test_inicial_avistadas_desconocidas_y_proyeccion_sin_filtraciones(self):
        mapa = crear_mapa((
            {"id": 10, "nombre": "Entrada visible", "salidas": {"E": salida(20)}},
            {"id": 20, "nombre": "Sala oculta vecina", "salidas": {"O": salida(10), "S": salida(30)}},
            {"id": 30, "nombre": "Sala oculta lejana", "salidas": {"N": salida(20)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 10)

        self.assertEqual(conocimiento.estado_de_sala(10), "explorada")
        self.assertEqual(conocimiento.estado_de_sala(20), "avistada")
        self.assertEqual(conocimiento.estado_de_sala(30), "desconocida")
        self.assertIsInstance(conocimiento.sala_conocida(10), SalaConocida)
        proyeccion = conocimiento.proyectar()
        self.assertEqual(tuple(sala.id_sala for sala in proyeccion), (10, 20))
        avistada = proyeccion[1]
        self.assertEqual((avistada.estado, avistada.nombre, avistada.salidas), ("avistada", None, ()))
        self.assertNotIn("Sala oculta vecina", tuple(sala.nombre for sala in proyeccion))
        self.assertNotIn("Sala oculta lejana", tuple(sala.nombre for sala in proyeccion))


class TestDatosYSincronizacionDePuertas(unittest.TestCase):
    """T002: FR-NIE-002 y FR-NIE-004, escenarios 1.2 y 1.5, SC-NIE-001."""

    def test_datos_explorados_memoria_no_observada_y_observacion_desde_extremo(self):
        mapa = crear_mapa((
            {"id": 1, "nombre": "Entrada", "salidas": {"E": salida(2, 37, llave="llave")}},
            {"id": 2, "nombre": "Galeria", "salidas": {"O": salida(1, 37, llave="llave")}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        conocimiento.observar_puerta(1, "E")
        datos = conocimiento.sala_conocida(1)

        self.assertEqual(datos.nombre, "Entrada")
        self.assertEqual(len(datos.salidas), 1)
        self.assertIsInstance(datos.salidas[0], SalidaConocida)
        self.assertEqual((datos.salidas[0].direccion, datos.salidas[0].id_sala_destino), ("E", 2))
        self.assertEqual((datos.salidas[0].costo, datos.salidas[0].estado_puerta), (37, "abierta"))

        mapa.cerrar_puerta(1, "E")
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), "abierta")
        conocimiento.observar_puerta(2, "O")
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), "cerrada")
        self.assertEqual(conocimiento.estado_de_puerta(2, "O"), "cerrada")


class TestRevelacionConAntorcha(unittest.TestCase):
    """T003: FR-NIE-005, FR-NIE-022 y FR-NIE-023, escenarios 2.1, 3.15 y 3.16, SC-NIE-001."""

    def test_entrada_con_antorcha_revela_vecinas_y_solo_observa_puerta_incidente(self):
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1), "N": salida(3, cerrada=True, llave="k"), "E": salida(4)}},
            {"id": 3, "nombre": "Vecina cerrada", "salidas": {"S": salida(2, cerrada=True, llave="k"), "E": salida(5, cerrada=True, llave="otra")}},
            {"id": 4, "nombre": "Vecina abierta", "salidas": {"O": salida(2), "S": salida(6)}},
            {"id": 5, "nombre": "Desconocida", "salidas": {"O": salida(3, cerrada=True, llave="otra")}},
            {"id": 6, "nombre": "Otra desconocida", "salidas": {"N": salida(4)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)

        conocimiento.al_entrar(2, False)
        self.assertEqual(conocimiento.estado_de_sala(3), "avistada")
        self.assertEqual(conocimiento.estado_de_sala(4), "avistada")
        conocimiento.al_entrar(2, True)

        self.assertEqual(conocimiento.estado_de_sala(3), "explorada")
        self.assertEqual(conocimiento.estado_de_sala(4), "explorada")
        self.assertEqual(conocimiento.estado_de_sala(5), "avistada")
        self.assertEqual(conocimiento.estado_de_sala(6), "avistada")
        self.assertEqual(conocimiento.estado_de_puerta(2, "N"), "cerrada")
        self.assertEqual(conocimiento.estado_de_puerta(3, "S"), "cerrada")
        self.assertEqual(conocimiento.estado_de_puerta(3, "E"), "no_observada")
        self.assertEqual(conocimiento.estado_de_puerta(5, "O"), "no_observada")
        self.assertEqual(mapa.obtener(3).contenido_cargado, False)
        self.assertEqual((mapa.obtener(3).enemigos_dormidos, mapa.obtener(3).enemigos_activos), ([], []))
        self.assertEqual((mapa.obtener(3).trampas, mapa.obtener(3).objetos_en_suelo), ([], []))

    def test_encender_sin_entrada_no_revela_y_apagar_no_borra_conocimiento(self):
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Vecina", "salidas": {"O": salida(1)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)

        self.assertEqual(conocimiento.estado_de_sala(2), "avistada")
        conocimiento.al_entrar(1, True)
        self.assertEqual(conocimiento.estado_de_sala(2), "explorada")
        conocimiento.al_entrar(1, False)
        self.assertEqual(conocimiento.estado_de_sala(2), "explorada")


class TestInversasDelConocimiento(unittest.TestCase):
    """T004: FR-NIE-004, FR-NIE-005 y FR-NIE-024, escenarios 2.2 y 3.17, SC-NIE-001 y SC-NIE-005."""

    def test_retroceso_real_restaurar_salas_y_puertas_reveladas(self):
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Sala central", "salidas": {"O": salida(1), "N": salida(3, llave="puerta")}},
            {"id": 3, "nombre": "Revelada", "salidas": {"S": salida(2, llave="puerta"), "E": salida(4, cerrada=True, llave="k")}},
            {"id": 4, "nombre": "Oculta", "salidas": {"O": salida(3, cerrada=True, llave="k")}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        historial = HistorialRetroceso()
        conocimiento.registrador = historial.registrar_cambio
        estado_previo = tuple(conocimiento.estado_de_sala(i) for i in range(1, 5))
        puerta_previa = conocimiento.estado_de_puerta(2, "N")

        historial.iniciar_intervalo()
        conocimiento.al_entrar(2, True)
        historial.cerrar_intervalo()

        self.assertEqual(conocimiento.estado_de_sala(3), "explorada")
        self.assertEqual(conocimiento.estado_de_sala(4), "avistada")
        self.assertEqual(conocimiento.estado_de_puerta(2, "N"), "abierta")
        self.assertGreater(historial.deshacer_ultimo_intervalo(), 0)
        self.assertEqual(tuple(conocimiento.estado_de_sala(i) for i in range(1, 5)), estado_previo)
        self.assertEqual(conocimiento.estado_de_puerta(2, "N"), puerta_previa)

    def test_cierre_automatico_observable_desde_vecina_se_revierte_con_historial(self):
        from cripta.modelo.efectos import EfectoCierrePuerta

        mapa = crear_mapa((
            {"id": 1, "nombre": "Actual", "salidas": {"E": salida(2, cierre=5)}},
            {"id": 2, "nombre": "Vecina", "salidas": {"O": salida(1, cierre=5)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        conocimiento.observar_puerta(1, "E")
        mapa.abrir_puerta(1, "E")
        conocimiento.observar_puerta(1, "E")
        memoria_previa = conocimiento.estado_de_puerta(1, "E")
        historial = HistorialRetroceso()
        conocimiento.registrador = historial.registrar_cambio
        mapa.conectar_registrador(historial.registrar_cambio)
        efecto = EfectoCierrePuerta(
            None, mapa, 1, "E", 5,
            al_cerrar=lambda: conocimiento.observar_puerta(2, "O"),
        )

        historial.iniciar_intervalo()
        efecto._cerrar()
        historial.cerrar_intervalo()

        self.assertEqual(mapa.obtener(1).puertas.esta_cerrada("E"), True)
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), "cerrada")
        self.assertGreater(historial.deshacer_ultimo_intervalo(), 0)
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), memoria_previa)

    def test_cierre_automatico_no_observable_conserva_memoria_y_se_revierte(self):
        from cripta.modelo.efectos import EfectoCierrePuerta

        mapa = crear_mapa((
            {"id": 1, "nombre": "Actual", "salidas": {"E": salida(2, cierre=5)}},
            {"id": 2, "nombre": "Vecina", "salidas": {"O": salida(1, cierre=5)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        conocimiento.observar_puerta(1, "E")
        mapa.abrir_puerta(1, "E")
        conocimiento.observar_puerta(1, "E")
        memoria_previa = conocimiento.estado_de_puerta(1, "E")
        historial = HistorialRetroceso()
        conocimiento.registrador = historial.registrar_cambio
        mapa.conectar_registrador(historial.registrar_cambio)
        efecto = EfectoCierrePuerta(None, mapa, 1, "E", 5)

        historial.iniciar_intervalo()
        efecto._cerrar()
        historial.cerrar_intervalo()

        self.assertEqual(mapa.obtener(1).puertas.esta_cerrada("E"), True)
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), memoria_previa)
        self.assertGreater(historial.deshacer_ultimo_intervalo(), 0)
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), memoria_previa)


class TestSalidaSinPuertaCerrable(unittest.TestCase):
    """T005: FR-NIE-025, escenario 3.18, decisión del grupo."""

    def test_salida_sin_puerta_es_abierta_en_proyeccion_y_no_observada(self):
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Destino", "salidas": {"O": salida(1)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)

        proyeccion = conocimiento.sala_conocida(1)
        self.assertEqual(proyeccion.salidas[0].estado_puerta, "abierta")
        self.assertEqual(conocimiento.estado_de_puerta(1, "E"), "no_observada")


class TestIntegracionPartida(unittest.TestCase):
    """T007: FR-NIE-002, FR-NIE-004 y FR-NIE-015, caso B-NIE-002."""

    def test_entrada_observa_puertas_y_revela_vecinas(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Vecina", "salidas": {"O": salida(1), "S": salida(3)}},
            {"id": 3, "nombre": "Lejana", "salidas": {"N": salida(2)}},
        ))
        partida.ejecutar_accion(Accion("mover", "E"))
        self.assertEqual(partida._conocimiento.estado_de_sala(2), "explorada")
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "avistada")
        self.assertEqual(partida._conocimiento.estado_de_puerta(2, "S"), "abierta")

    def test_cierre_automatico_actualiza_conocimiento_en_un_extremo(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2, cerrada=True, llave="llave", cierre=150)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1, cerrada=True, llave="llave", cierre=150), "E": salida(3)}},
            {"id": 3, "nombre": "Final", "salidas": {"O": salida(2)}},
        ))
        llave = LlaveDTO("llave", "Llave", "llave", 0, 0, None)
        partida._jugador.inventario.recoger(ObjetoInventario("llave-instancia", llave))

        self.assertEqual(partida._conocimiento.estado_de_puerta(1, "E"), "cerrada")
        partida.ejecutar_accion(Accion("abrir", "E"))
        self.assertEqual(partida._conocimiento.estado_de_puerta(1, "E"), "abierta")
        resultado = partida.ejecutar_accion(Accion("mover", "E"))

        self.assertTrue(partida._mapa.obtener(1).puertas.esta_cerrada("E"))
        self.assertEqual(partida._conocimiento.estado_de_puerta(1, "E"), "cerrada")
        self.assertIn("Una puerta se cierra sola.", resultado.mensajes)

    def test_cierre_automatico_lejano_conserva_memoria_y_avisa(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1),
                                                              "E": salida(3, cerrada=True, llave="llave", cierre=350)}},
            {"id": 3, "nombre": "Vecina", "salidas": {"O": salida(2, cerrada=True, llave="llave", cierre=350),
                                                               "E": salida(4)}},
            {"id": 4, "nombre": "Lejana", "salidas": {"O": salida(3)}},
        ))
        llave = LlaveDTO("llave", "Llave", "llave", 0, 0, None)
        partida._jugador.inventario.recoger(ObjetoInventario("llave-instancia", llave))
        partida.ejecutar_accion(Accion("mover", "E"))
        partida.ejecutar_accion(Accion("abrir", "E"))
        partida.ejecutar_accion(Accion("mover", "E"))
        partida.ejecutar_accion(Accion("mover", "E"))
        memoria_previa = partida._conocimiento.estado_de_puerta(2, "E")
        partida._buscador._valido = True

        resultado = partida.ejecutar_accion(Accion("esperar"))

        self.assertEqual(partida._conocimiento.estado_de_puerta(2, "E"), memoria_previa)
        self.assertIn("Una puerta se cierra sola.", resultado.mensajes)
        self.assertFalse(partida._buscador._valido)

    def test_abrir_actualiza_conocimiento_con_accion_real(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2, cerrada=True, llave="llave")}},
            {"id": 2, "nombre": "Final", "salidas": {"O": salida(1, cerrada=True, llave="llave")}},
        ))
        llave = LlaveDTO("llave", "Llave", "llave", 0, 0, None)
        partida._jugador.inventario.recoger(ObjetoInventario("llave-instancia", llave))

        resultado = partida.ejecutar_accion(Accion("abrir", "E"))

        self.assertTrue(resultado.aceptada)
        self.assertEqual(partida._conocimiento.estado_de_puerta(1, "E"), "abierta")

    def test_pergamino_revierte_conocimiento_de_entrada_con_antorcha(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Vecina", "salidas": {"O": salida(2)}},
        ))
        ficha = SimpleNamespace(clase="pergamino_retroceso")
        partida._jugador.inventario.recoger(ObjetoInventario("pergamino", ficha))
        partida._antorcha_encendida = True
        partida.ejecutar_accion(Accion("mover", "E"))
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "explorada")
        partida.ejecutar_accion(Accion("pergamino"))
        self.assertEqual(partida._jugador.sala_actual, 1)
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "desconocida")


if __name__ == "__main__":
    unittest.main()
