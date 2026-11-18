"""Pruebas de ruta y proyecciones de «ir a» (FR-NIE-009 a FR-NIE-021)."""
import unittest
from types import SimpleNamespace

from cripta.modelo.conocimiento_jugador import ConocimientoJugador
from cripta.modelo.accion import Accion
from cripta.modelo.resultado_partida import MapaConocido, ResultadoViaje
from cripta.modelo.ruta_conocida import siguiente_paso
from tests.modelo.test_conocimiento_jugador import crear_mapa, crear_partida_sintetica, salida


class TestRutaConocida(unittest.TestCase):
    """FR-NIE-009, 010, 014, 019 y 021, escenarios 3.1, 3.2, 3.9, 3.12 y 3.14."""

    def test_costo_minimo_y_desempate_por_menor_id(self):
        """FR-NIE-010, escenario 3.1: minimiza costos y desempata por id."""
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"N": salida(3, 2), "E": salida(2, 1)}},
            {"id": 2, "nombre": "Este", "salidas": {"O": salida(1, 1), "N": salida(4, 3)}},
            {"id": 3, "nombre": "Norte", "salidas": {"S": salida(1, 2), "E": salida(4, 2)}},
            {"id": 4, "nombre": "Destino", "salidas": {"S": salida(2, 3), "O": salida(3, 2)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        for sala_id in (2, 3, 4):
            conocimiento.al_entrar(sala_id, False)
        self.assertEqual(siguiente_paso(conocimiento, 1, 4), "E")
        self.assertEqual(1 + 3, 2 + 2)

    def test_elige_el_costo_total_menor(self):
        """FR-NIE-010, escenario 3.1: evita una ruta conocida más costosa."""
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"N": salida(3, 1), "E": salida(2, 2)}},
            {"id": 2, "nombre": "Este", "salidas": {"O": salida(1, 2), "N": salida(4, 1)}},
            {"id": 3, "nombre": "Norte", "salidas": {"S": salida(1, 1), "E": salida(4, 10)}},
            {"id": 4, "nombre": "Destino", "salidas": {"S": salida(2, 1), "O": salida(3, 10)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        for sala_id in (2, 3, 4):
            conocimiento.al_entrar(sala_id, False)
        self.assertEqual(siguiente_paso(conocimiento, 1, 4), "E")
        self.assertLess(2 + 1, 1 + 10)

    def test_puerta_no_observada_o_cerrada_no_se_cruza(self):
        """FR-NIE-010 y 014, escenario 3.2: solo se cruza una puerta abierta recordada."""
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2, 1, llave="llave")}},
            {"id": 2, "nombre": "Destino", "salidas": {"O": salida(1, 1, llave="llave")}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        conocimiento._explorar(2)
        self.assertIsNone(siguiente_paso(conocimiento, 1, 2))
        conocimiento.observar_puerta(1, "E")
        self.assertEqual(siguiente_paso(conocimiento, 1, 2), "E")
        mapa.cerrar_puerta(1, "E")
        conocimiento.observar_puerta(1, "E")
        self.assertIsNone(siguiente_paso(conocimiento, 1, 2))


class TestProyeccionesViaje(unittest.TestCase):
    """FR-NIE-007, 008 y 013, escenarios 1.1, 3.5 y 3.8."""

    def test_mapa_y_resultado_son_inmutables(self):
        """FR-NIE-007 y 008, escenario 1.1: proyecciones sin mutación."""
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Destino", "salidas": {"O": salida(1)}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        proyeccion = MapaConocido(conocimiento.proyectar())
        resultado = ResultadoViaje("E", None)
        self.assertEqual(tuple(sala.id_sala for sala in proyeccion.salas), (1, 2))
        with self.assertRaises(AttributeError):
            proyeccion.salas = ()
        with self.assertRaises(AttributeError):
            resultado.direccion = "N"
        self.assertEqual(resultado.motivo, None)

    def test_partida_proyecta_y_propone_sin_efectos(self):
        """FR-NIE-008, 009, 019 y 021, escenarios 1.1, 3.1, 3.12 y 3.14."""
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Galería", "salidas": {"O": salida(1)}},
            {"id": 3, "nombre": "Oculta", "salidas": {}},
        ))
        partida.ejecutar_accion(Accion("mover", "E"))
        proyeccion = partida.mapa_conocido()
        self.assertEqual(tuple(sala.id_sala for sala in proyeccion.salas), (1, 2))
        tiempo = partida.vista().tiempo
        mensajes = partida.mensajes()
        self.assertEqual(partida.siguiente_paso(2).motivo, "sala_actual")
        self.assertEqual(partida.siguiente_paso(3).motivo, "destino_no_explorado")
        paso = partida.siguiente_paso(1)
        self.assertEqual((paso.direccion, paso.motivo), ("O", None))
        self.assertEqual(partida.vista().tiempo, tiempo)
        self.assertEqual(partida.mensajes(), mensajes)
        self.assertEqual(partida.motivos_despues_de_paso(2, partida.vista().vida),
                         ("llegada_destino",))

    def test_resultado_representa_falta_de_ruta(self):
        """FR-NIE-013, escenario 3.14: ausencia de ruta es motivo de detención."""
        resultado = ResultadoViaje(None, "sin_ruta")
        self.assertIsNone(resultado.direccion)
        self.assertEqual(resultado.motivo, "sin_ruta")

    def test_motivos_reales_de_partida_en_orden_y_enemigos_vivos(self):
        """FR-NIE-013, escenarios 3.5 a 3.7: motivos reales tras completar paso."""
        from cripta.modelo.enemigo import Enemigo

        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Destino", "salidas": {"O": salida(1)}},
        ))
        partida.ejecutar_accion(Accion("mover", "E"))
        ficha = SimpleNamespace(
            nombre="Guardián", vida_max=10, ataque=1, defensa=0, velocidad=100,
            comportamiento="guardián", rango=None, suelta=(), id="guardián",
        )
        dormido = Enemigo("dormido", ficha, 2)
        partida._mapa.obtener(2).enemigos_dormidos.append(dormido)
        partida._jugador.vida -= 1
        self.assertEqual(
            partida.motivos_despues_de_paso(2, partida._jugador.vida + 1),
            ("llegada_destino", "enemigos_vivos", "daño_recibido"),
        )
        dormido.vida = 0
        self.assertEqual(partida.motivos_despues_de_paso(2, partida._jugador.vida),
                         ("llegada_destino",))
        activo = Enemigo("activo", ficha, 2)
        activo.activar()
        partida._mapa.obtener(2).enemigos_activos.append(activo)
        self.assertEqual(partida.motivos_despues_de_paso(1, partida._jugador.vida),
                         ("enemigos_vivos",))
        partida._jugador.vida = 0
        self.assertEqual(partida.motivos_despues_de_paso(2, 1), ())

    def test_destinos_invalidos_actuales_y_sin_ruta(self):
        """FR-NIE-009, 019 y 021, escenarios 3.12 y 3.14: rechazos sin ruta."""
        mapa = crear_mapa((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2, 1, cerrada=True, llave="llave")}},
            {"id": 2, "nombre": "Destino", "salidas": {"O": salida(1, 1, cerrada=True, llave="llave")}},
        ))
        conocimiento = ConocimientoJugador(mapa, 1)
        conocimiento.al_entrar(2, False)
        self.assertIsNone(siguiente_paso(conocimiento, 1, 99))
        self.assertIsNone(siguiente_paso(conocimiento, 1, 1))
        self.assertIsNone(siguiente_paso(conocimiento, 1, 2))

    def test_destino_fuera_del_mapa_es_inexistente_y_puerta_con_llave_no_es_ruta(self):
        """FR-NIE-009, 014 y 021, escenarios 3.1, 3.9 y 3.14."""
        from cripta.dto.llave_dto import LlaveDTO
        from cripta.modelo.inventario import ObjetoInventario

        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {
                "E": salida(2, 1, cerrada=True, llave="llave")}},
            {"id": 2, "nombre": "Destino", "salidas": {
                "O": salida(1, 1, cerrada=True, llave="llave")}},
        ))
        partida._conocimiento.al_entrar(2, False)
        llave = LlaveDTO("llave", "Llave", "llave", 0, 0, None)
        partida._jugador.inventario.recoger(ObjetoInventario("llave-instancia", llave))
        antes = (partida.vista().tiempo, partida.mensajes(),
                 partida.vista().retrocesos_posibles)
        self.assertEqual(partida.siguiente_paso(99).motivo, "destino_inexistente")
        self.assertEqual(partida.siguiente_paso(-1).motivo, "destino_inexistente")
        self.assertEqual(partida.siguiente_paso(2).motivo, "sin_ruta")
        self.assertTrue(partida._mapa.obtener(1).puertas.esta_cerrada("E"))
        despues = (partida.vista().tiempo, partida.mensajes(),
                   partida.vista().retrocesos_posibles)
        self.assertEqual(despues, antes)


if __name__ == "__main__":
    unittest.main()
