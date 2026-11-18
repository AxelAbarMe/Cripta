"""Casos de aceptaci?n de niebla e ir a para los escenarios cubiertos por T013."""
import unittest
from types import SimpleNamespace

from cripta.modelo.accion import Accion
from cripta.controlador.controlador_cripta import ControladorCripta, Orden
from cripta.infraestructura.estado_guardado import EV_ANTORCHA_APAGAR, EV_TURNO_ACTOR
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.enemigo import Enemigo
from cripta.modelo.trampa import Trampa
from tests.modelo.test_conocimiento_jugador import crear_partida_sintetica, salida

ANTORCHA = SimpleNamespace(id="antorcha-t013", clase="antorcha", nombre="Antorcha", peso=1, valor=1, duracion=2000)


class TestAceptacionNiebla(unittest.TestCase):
    """B-NIE-004 y B-NIE-005: FR-NIE-005, FR-NIE-024, SC-NIE-001 y SC-NIE-005."""

    def test_B_NIE_004_antorcha_revela_vecinas_sin_cargar_amenazas(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Vecina", "salidas": {"O": salida(2)}},
        ))
        ficha_enemigo = SimpleNamespace(
            id="enemigo-t013", nombre="Guardián", vida_max=10, ataque=1, defensa=0,
            velocidad=100, comportamiento="guardián", suelta=(), rango=None,
        )
        enemigo = Enemigo("enemigo-dormido", ficha_enemigo, 3)
        trampa = Trampa("trampa-vecina", "trp_dardos")
        vecina_objetivo = partida._mapa.obtener(3)
        vecina_objetivo.enemigos_dormidos.append(enemigo)
        vecina_objetivo.trampas.append(trampa)
        partida._jugador.inventario.recoger(ObjetoInventario("antorcha-t013", ANTORCHA))
        self.assertTrue(partida.ejecutar_accion(Accion("usar", 0)).aceptada)
        vida_previa = partida._jugador.vida
        self.assertTrue(any(evento.datos and evento.datos[0] == EV_ANTORCHA_APAGAR
                            for evento in partida._reloj.eventos_vigentes()))

        resultado = partida.ejecutar_accion(Accion("mover", "E"))

        self.assertTrue(resultado.aceptada)
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "explorada")
        self.assertFalse(vecina_objetivo.contenido_cargado)
        self.assertEqual(vecina_objetivo.enemigos_dormidos, [enemigo])
        self.assertEqual(vecina_objetivo.enemigos_activos, [])
        self.assertEqual(vecina_objetivo.trampas, [trampa])
        self.assertFalse(enemigo.activo)
        self.assertIsNone(enemigo.evento_pendiente)
        self.assertFalse(any(evento.datos and evento.datos[0] == EV_TURNO_ACTOR and evento.datos[1] == enemigo.instancia_id
                             for evento in partida._reloj.eventos_vigentes()))
        self.assertTrue(trampa.armada)
        self.assertEqual(partida._jugador.vida, vida_previa)

    def test_B_NIE_005_pergamino_revierte_entrada_y_revelacion_por_antorcha(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Vecina", "salidas": {"O": salida(2)}},
        ))
        partida._jugador.inventario.recoger(ObjetoInventario("antorcha-t013", ANTORCHA))
        partida._jugador.inventario.recoger(ObjetoInventario(
            "pergamino-1", SimpleNamespace(clase="pergamino_retroceso", nombre="Pergamino")
        ))
        self.assertTrue(partida.ejecutar_accion(Accion("usar", 0)).aceptada)
        previo = partida._conocimiento.proyectar()

        partida.ejecutar_accion(Accion("mover", "E"))
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "explorada")
        partida.ejecutar_accion(Accion("pergamino"))

        self.assertEqual(partida._jugador.sala_actual, 1)
        self.assertEqual(partida._conocimiento.proyectar(), previo)

    def test_B_NIE_001_destino_no_explorado_no_mueve(self):
        """FR-NIE-009, escenario 3.1 y SC-NIE-002: el destino avistado se rechaza."""
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Oculta", "salidas": {"O": salida(1)}},
        ))
        resultado = partida.siguiente_paso(2)
        self.assertEqual(resultado.direccion, None)
        self.assertEqual(resultado.motivo, "destino_no_explorado")
        self.assertEqual(partida.vista().tiempo, 0)

    def test_B_NIE_002_cierre_observado_elimina_la_ruta(self):
        """FR-NIE-012 y FR-NIE-015, escenario 3.4 y SC-NIE-003: la memoria se actualiza al observar."""
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2, llave="k")}},
            {"id": 2, "nombre": "Paso", "salidas": {"O": salida(1, llave="k"), "E": salida(3)}},
            {"id": 3, "nombre": "Lejos", "salidas": {"O": salida(2)}},
        ))
        self.assertTrue(partida.ejecutar_accion(Accion("mover", "E")).aceptada)
        self.assertTrue(partida.ejecutar_accion(Accion("mover", "E")).aceptada)
        partida._mapa.cerrar_puerta(1, "E")
        self.assertEqual(partida.siguiente_paso(1).direccion, "O")
        class ServicioFalso:
            def __init__(self, modelo):
                self.partida = modelo
                self.acciones = []

            def ejecutar(self, accion):
                self.acciones.append(accion)
                return self.partida.ejecutar_accion(accion)

        class VistaFalsa:
            def __init__(self):
                self.motivos = []

            def mostrar_aviso(self, texto):
                pass

            def mostrar_error(self, texto):
                raise AssertionError(texto)

            def mostrar_motivos_viaje(self, motivos):
                raise AssertionError("Un paso rechazado no presenta motivos de viaje")

        controlador = ControladorCripta(ServicioFalso(partida), VistaFalsa())
        self.assertIsNone(controlador._ejecutar_paso_viaje(1, "O"))
        resultado = partida.siguiente_paso(1)
        self.assertEqual((resultado.direccion, resultado.motivo), (None, "sin_ruta"))

    def test_B_NIE_003_enemigos_dormidos_dan_motivo_de_parada(self):
        """FR-NIE-013 y FR-NIE-020, escenarios 3.5 y 3.13 y SC-NIE-003."""
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Intermedia", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Destino", "salidas": {"O": salida(2)}},
        ))
        partida._conocimiento.al_entrar(2, False)
        partida._conocimiento.al_entrar(3, False)
        ficha = SimpleNamespace(id="guardia", nombre="Guardia", vida_max=10, ataque=1,
                                defensa=0, velocidad=100, comportamiento="guardián", suelta=(), rango=None)
        partida._mapa.obtener(2).enemigos_dormidos.append(Enemigo("guardia-dormido", ficha, 2))
        partida._jugador.vida_max = partida._jugador.vida = 1000

        class ServicioFalso:
            def __init__(self, modelo):
                self.partida = modelo

            def ejecutar(self, accion):
                return self.partida.ejecutar_accion(accion)

        class VistaFalsa:
            def __init__(self):
                self.motivos = []

            def mostrar_aviso(self, texto):
                pass

            def mostrar_error(self, texto):
                raise AssertionError(texto)

            def mostrar_motivos_viaje(self, motivos):
                self.motivos = motivos

        vista = VistaFalsa()
        controlador = ControladorCripta(ServicioFalso(partida), vista)
        controlador._procesar(Orden("ir_a", 3), partida.vista())
        self.assertEqual(partida._jugador.sala_actual, 2)
        self.assertTrue(partida._mapa.obtener(2).enemigos_activos[0].activo)
        self.assertIn("enemigos_vivos", vista.motivos)
        self.assertNotIn("llegada_destino", vista.motivos)

        partida_sin_enemigo = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Intermedia", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Destino", "salidas": {"O": salida(2)}},
        ))
        partida_sin_enemigo._conocimiento.al_entrar(2, False)
        partida_sin_enemigo._conocimiento.al_entrar(3, False)
        partida_sin_enemigo._jugador.vida_max = partida_sin_enemigo._jugador.vida = 1000
        vista_positiva = VistaFalsa()
        controlador_positivo = ControladorCripta(ServicioFalso(partida_sin_enemigo), vista_positiva)
        controlador_positivo._procesar(Orden("ir_a", 3), partida_sin_enemigo.vista())
        self.assertEqual(partida_sin_enemigo._jugador.sala_actual, 3)
        self.assertIn("llegada_destino", vista_positiva.motivos)

    def test_B_NIE_006_pergamino_retrocede_un_paso_y_no_hay_continuacion(self):
        """FR-NIE-017, escenario 3.11 y SC-NIE-003: el pergamino revierte solo el movimiento ejecutado."""
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Paso", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Paso final", "salidas": {"O": salida(2), "E": salida(4)}},
            {"id": 4, "nombre": "Destino", "salidas": {"O": salida(3)}},
        ))
        partida._conocimiento.al_entrar(2, False)
        partida._conocimiento.al_entrar(3, False)
        partida._jugador.inventario.recoger(ObjetoInventario(
            "pergamino-1", SimpleNamespace(clase="pergamino_retroceso", nombre="Pergamino")
        ))
        class ServicioFalso:
            def __init__(self, modelo):
                self.partida = modelo
                self.acciones = []

            def ejecutar(self, accion):
                self.acciones.append(accion)
                return self.partida.ejecutar_accion(accion)

        class VistaFalsa:
            def __init__(self):
                self.motivos = []

            def mostrar_aviso(self, texto):
                pass

            def mostrar_error(self, texto):
                raise AssertionError(texto)

            def mostrar_motivos_viaje(self, motivos):
                self.motivos.append(motivos)

        servicio = ServicioFalso(partida)
        controlador = ControladorCripta(servicio, VistaFalsa())
        self.assertIsNone(controlador._ejecutar_paso_viaje(4, "E"))
        tiempo_primer_paso = partida.vista().tiempo
        self.assertIsNone(controlador._ejecutar_paso_viaje(4, "E"))
        self.assertEqual(partida._jugador.sala_actual, 3)
        acciones_antes = len(servicio.acciones)
        motivos_antes = tuple(controlador._vista.motivos)
        self.assertEqual(tiempo_primer_paso, 100)
        controlador._procesar(Orden("pergamino"), partida.vista())
        self.assertEqual((partida._jugador.sala_actual, partida.vista().tiempo), (2, tiempo_primer_paso))
        self.assertEqual(len(servicio.acciones), acciones_antes + 1)
        self.assertEqual(servicio.acciones[-1].tipo, "pergamino")
        self.assertEqual(tuple(controlador._vista.motivos), motivos_antes)


if __name__ == "__main__":
    unittest.main()
