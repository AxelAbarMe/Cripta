"""Pruebas de ControladorCripta con una vista falsa y la cripta congelada de tests/datos/ (sin red ni teclado).

La vista falsa devuelve opciones y órdenes de una lista y anota todo lo que el controlador le muestra.
Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.controlador.test_controlador_cripta -v
"""
import dataclasses
import tempfile
import unittest
from pathlib import Path

from cripta.controlador.controlador_cripta import ControladorCripta, Orden
from cripta.excepciones import CriptaApiError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.infraestructura.puntajes_disco import RepositorioPuntajes
from cripta.modelo.inventario import ObjetoInventario
from cripta.vista.vista_base import VistaBase
from tests.servicios.test_servicio_partida import ClienteContado
from tests.servicios.test_servicio_partida_guardado import armar

CRIPTA = "cripta-01"


class ClientePresupuestoAmplio(ClienteContado):
    """Igual que la cripta de pruebas pero con presupuesto holgado: cargar vuelve a pedir lo básico (sin caché de disco)."""

    def __getattr__(self, nombre):
        llamar = super().__getattr__(nombre)
        if nombre != "obtener_general":
            return llamar
        return lambda *argumentos: dataclasses.replace(llamar(*argumentos), presupuesto_solicitudes=99)


class VistaFalsa(VistaBase):
    def __init__(self, ordenes=(), confirmaciones=(), nombre="Ana", opciones=("iniciar", "salir"), cripta=CRIPTA):
        self.ordenes, self.confirmaciones, self.opciones = list(ordenes), list(confirmaciones), list(opciones)
        self.nombre, self.cripta = nombre, cripta
        self.estados, self.avisos, self.errores, self.ordenados = [], [], [], []
        self.resultados, self.finales, self.preguntas = [], [], []
        self.historias = []
        self.ultimo_vista = None

    def pedir_opcion_menu(self):
        return self.opciones.pop(0)

    def mostrar_creditos(self):
        pass

    def mostrar_puntajes_globales(self, puntajes):
        self.puntajes = puntajes

    def elegir_cripta(self, criptas):
        return self.cripta

    def mostrar_estado(self, vista, mensajes):
        self.estados.append((vista, mensajes))
        self.ultimo_vista = vista

    def pedir_orden(self, vista):
        # Si ya no quedan órdenes, la prueba termina volviendo al menú
        return self.ordenes.pop(0) if self.ordenes else Orden("salir")

    def mostrar_aviso(self, texto):
        self.avisos.append(texto)

    def mostrar_error(self, texto):
        self.errores.append(texto)

    def mostrar_inventario_ordenado(self, criterio, objetos):
        self.ordenados.append((criterio, tuple(objetos)))

    def pedir_texto(self, pregunta):
        return self.nombre

    def confirmar(self, pregunta):
        self.preguntas.append(pregunta)
        if "Reintentar" in pregunta:
            return False     # evita un bucle infinito si el estado no se puede leer
        return self.confirmaciones.pop(0) if self.confirmaciones else True

    def mostrar_resultado(self, desenlace, resumen, nombre, ranking, puntajes):
        self.resultados.append((desenlace, resumen, nombre, ranking, puntajes))

    def mostrar_final(self, datos):
        self.finales.append(datos)

    def mostrar_historia(self, resumen, referencia):
        self.historias.append((resumen, referencia))


class BaseControlador(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.dir = Path(self._carpeta.name)
        self.repositorio = RepositorioPuntajes(AlmacenDiscoArchivos(self.dir / "puntajes"))
        self.servicio = armar(ClientePresupuestoAmplio, self.repositorio)

    def tearDown(self):
        self.servicio.cerrar()
        self._carpeta.cleanup()

    def jugar(self, vista, semilla=5):
        controlador = ControladorCripta(
            self.servicio, vista, ruta_guardado=str(self.dir / "p.sav"), ruta_bitacora=str(self.dir / "p.log"),
            semilla=semilla, leer_puntajes=lambda: self.repositorio.cargar().ordenados_por_tiempo())
        # La primera vez que se pide una orden se sube la vida: las ratas de la sala 2 no matan en la prueba
        pedir = vista.pedir_orden

        def pedir_con_vida(vista_partida):
            self.servicio.partida._jugador.vida_max = self.servicio.partida._jugador.vida = 1000
            vista.pedir_orden = pedir
            return pedir(vista_partida)
        vista.pedir_orden = pedir_con_vida
        controlador.ejecutar()
        return controlador


class TestFlujoDelMenu(BaseControlador):
    def test_salir_del_menu_cierra_el_servicio(self):
        vista = VistaFalsa(opciones=["salir"])
        self.jugar(vista)
        self.assertEqual(vista.estados, [])
        with self.assertRaises(RuntimeError):
            self.servicio.partida

    def test_volver_desde_la_eleccion_de_cripta_no_inicia_partida(self):
        vista = VistaFalsa(opciones=["iniciar", "salir"], cripta=None)
        self.jugar(vista)
        self.assertEqual(vista.estados, [])
        self.assertEqual(vista.errores, [])

    def test_salir_de_la_partida_pide_confirmacion_y_si_se_niega_sigue(self):
        vista = VistaFalsa(ordenes=[Orden("salir"), Orden("esperar"), Orden("salir")], confirmaciones=[False, True])
        self.jugar(vista)
        self.assertEqual(len(vista.preguntas), 2)
        self.assertEqual(vista.estados[-1][0].tiempo, 100)   # esperar sí se ejecutó tras negar la salida

    def test_un_error_de_red_al_listar_se_muestra_sin_romper_el_programa(self):
        class Falla:
            def listar_criptas(self):
                raise CriptaApiError("listar criptas", 500, "caído")

            def cerrar(self):
                pass
        vista = VistaFalsa(opciones=["iniciar", "salir"])
        ControladorCripta(Falla(), vista).ejecutar()
        self.assertEqual(len(vista.errores), 1)
        self.assertIn("caído", vista.errores[0])


class TestOrdenes(BaseControlador):
    def test_atacar_o_recoger_una_posicion_inexistente_avisa(self):
        vista = VistaFalsa(ordenes=[Orden("atacar", 0), Orden("recoger", 5)])
        self.jugar(vista)
        self.assertEqual(vista.avisos, ["No hay ese enemigo en la sala.", "No hay ese objeto en el suelo."])
        self.assertEqual(vista.ultimo_vista.tiempo, 0)

    def test_usar_equipar_o_soltar_sin_objeto_seleccionado_avisa(self):
        vista = VistaFalsa(ordenes=[Orden("usar"), Orden("equipar"), Orden("soltar")])
        self.jugar(vista)
        self.assertEqual(vista.avisos, ["No hay un objeto seleccionado en el inventario."] * 3)

    def test_abrir_una_puerta_que_no_se_puede_se_rechaza_con_motivo_y_sin_gastar_tiempo(self):
        vista = VistaFalsa(ordenes=[Orden("abrir", "N")])
        self.jugar(vista)
        self.assertEqual(len(vista.avisos), 1)
        self.assertEqual(vista.ultimo_vista.tiempo, 0)

    def test_pergamino_sin_nada_que_deshacer_avisa(self):
        vista = VistaFalsa(ordenes=[Orden("pergamino", 1)])
        self.jugar(vista)
        self.assertEqual(vista.avisos, ["No hay ninguna acción que se pueda deshacer."])

    def test_orden_desconocida_y_criterio_de_orden_invalido_avisan(self):
        vista = VistaFalsa(ordenes=[Orden("bailar"), Orden("ordenar", "color")])
        self.jugar(vista)
        self.assertEqual(vista.avisos, ["Orden desconocida: 'bailar'.", "Criterio de orden inválido: 'color'."])

    def test_recoger_ordenar_y_soltar(self):
        vista = VistaFalsa(ordenes=[Orden("recoger", 0), Orden("ordenar", "peso"), Orden("soltar")])
        self.jugar(vista)
        self.assertEqual(vista.errores, [])
        self.assertEqual(vista.ordenados[0][0], "peso")
        self.assertEqual(len(vista.ordenados[0][1]), 1)
        self.assertEqual(vista.ultimo_vista.inventario_cantidad, 0)       # se soltó
        self.assertEqual(len(vista.ultimo_vista.objetos_suelo), 1)

    def test_usar_la_antorcha_la_consume_y_queda_el_efecto(self):
        vista = VistaFalsa(ordenes=[Orden("recoger", 0), Orden("usar")])
        self.jugar(vista)
        self.assertEqual(vista.errores, [])
        self.assertEqual(vista.ultimo_vista.inventario_cantidad, 0)
        self.assertNotEqual(vista.ultimo_vista.efectos_activos, ())

    def test_mover_gasta_tiempo_y_cambia_de_sala(self):
        vista = VistaFalsa(ordenes=[Orden("mover", "N")])
        self.jugar(vista)
        self.assertEqual(vista.ultimo_vista.sala_id, 2)
        self.assertEqual(vista.ultimo_vista.tiempo, 100)


class TestRutaLarga(BaseControlador):
    LLAVE_BRONCE = [Orden("mover", "N"), Orden("mover", "N"), Orden("recoger", 0), Orden("mover", "S")]

    def test_abrir_con_llave_recoger_el_pergamino_y_deshacer(self):
        ordenes = self.LLAVE_BRONCE + [Orden("abrir", "E"), Orden("mover", "E"), Orden("recoger", 0), Orden("esperar")]
        vista = VistaFalsa(ordenes=ordenes)
        self.jugar(vista)
        antes = vista.ultimo_vista
        self.assertEqual((antes.sala_id, antes.pergaminos), (5, 1))
        vista = VistaFalsa(ordenes=ordenes + [Orden("pergamino", 1)])
        self.jugar(vista)
        despues = vista.ultimo_vista
        self.assertEqual(vista.errores, [])
        self.assertEqual(despues.pergaminos, 0)                 # el pergamino usado queda consumido (§2.11)
        self.assertLess(despues.tiempo, antes.tiempo)           # el reloj volvió atrás
        self.assertEqual(despues.sala_id, 5)

    def test_victoria_registra_el_puntaje_y_muestra_resultado_y_final(self):
        # Sala 1 -> 4 (tres pasos al norte), recoger la llave negra, abrir la puerta este y entrar a la salida
        ordenes = [Orden("mover", "N")] * 3 + [Orden("recoger", 0), Orden("abrir", "E"), Orden("mover", "E")]
        vista = VistaFalsa(ordenes=ordenes, nombre="Ana")
        self.jugar(vista)
        self.assertEqual(vista.errores, [])
        desenlace, resumen, nombre, ranking, puntajes = vista.resultados[0]
        self.assertEqual((desenlace, nombre), ("victoria", "Ana"))
        self.assertEqual(resumen.acciones_jugador, 6)
        self.assertEqual([p.nombre_jugador for p in ranking], ["Ana"])
        self.assertEqual(len(puntajes), 1)
        self.assertEqual(vista.finales[0].desenlace, "victoria")
        self.assertIn("Solicitudes realizadas", vista.finales[0].reporte)

    def test_victoria_sin_nombre_no_registra_puntaje(self):
        ordenes = [Orden("mover", "N")] * 3 + [Orden("recoger", 0), Orden("abrir", "E"), Orden("mover", "E")]
        vista = VistaFalsa(ordenes=ordenes, nombre="")
        self.jugar(vista)
        self.assertEqual(vista.resultados[0][3], ())
        self.assertEqual(self.repositorio.cargar().ordenados_por_tiempo(), ())


class TestGuardarYCargar(BaseControlador):
    def test_guardar_avisa_con_la_ruta_y_cargar_restaura_la_partida(self):
        vista = VistaFalsa(ordenes=[Orden("mover", "N"), Orden("guardar"), Orden("mover", "N"), Orden("cargar")],
                           confirmaciones=[True])
        self.jugar(vista)
        self.assertTrue(vista.avisos[0].startswith("Partida guardada en"))
        self.assertTrue(vista.avisos[1].startswith("Partida cargada desde"))
        self.assertEqual(vista.ultimo_vista.sala_id, 2)         # volvió al instante guardado

    def test_cargar_cancelado_no_reemplaza_la_partida(self):
        vista = VistaFalsa(ordenes=[Orden("guardar"), Orden("mover", "N"), Orden("cargar")], confirmaciones=[False])
        self.jugar(vista)
        self.assertEqual(vista.ultimo_vista.sala_id, 2)
        self.assertEqual(len(vista.avisos), 1)

    def test_cargar_sin_archivo_muestra_el_error_y_la_partida_sigue(self):
        vista = VistaFalsa(ordenes=[Orden("cargar"), Orden("esperar")], confirmaciones=[True])
        self.jugar(vista)
        self.assertEqual(len(vista.errores), 1)
        self.assertEqual(vista.ultimo_vista.tiempo, 100)


def _campos(estado):
    # Los grupos comparables de un VistaPartida o de un ResumenHistorico (los dos usan estos nombres)
    enemigos = tuple((e.instancia, e.vida, e.vida_max) for e in estado.enemigos)
    return (estado.tiempo, estado.sala_id, estado.vida, estado.vida_max, estado.ataque, estado.defensa,
            estado.velocidad, estado.efectos_activos, enemigos)


class VistaConInstantaneas(VistaFalsa):
    """Toma una fotografía del servicio cada vez que se pide una orden y puede preparar la partida antes de la primera."""

    def __init__(self, observar, preparar=None, **opciones):
        super().__init__(**opciones)
        self.observar, self.preparar, self.instantaneas = observar, preparar, []

    def pedir_orden(self, vista):
        if self.preparar is not None:
            self.preparar()
            self.preparar = None
        self.instantaneas.append(self.observar())
        return super().pedir_orden(vista)


class TestHistoria(BaseControlador):
    ESPERAS = [Orden("esperar")] * 3          # deja decisiones en 0, 100, 200 y 300 en la sala 1, sin enemigos

    def setUp(self):
        super().setUp()
        self.ruta_log = self.dir / "p.log"

    def observar(self):
        p = self.servicio.partida
        return (p.vista(), p.mensajes(), p.puntaje(), len(p._historial), len(p.linea_tiempo()),
                p._reloj.tiempo_actual, p._azar.getstate(), self.ruta_log.read_bytes())

    def jugar_sin_ajustes(self, vista):
        # A diferencia de jugar() no sube la vida del jugador: la historia parte del estado inicial real
        ControladorCripta(self.servicio, vista, ruta_guardado=str(self.dir / "p.sav"), ruta_bitacora=str(self.ruta_log),
                          semilla=5).ejecutar()

    def consultar(self, *consultas, preparar=None):
        ordenes = self.ESPERAS + [Orden("historia", c) for c in consultas]
        vista = VistaConInstantaneas(self.observar, preparar, ordenes=ordenes)
        self.jugar_sin_ajustes(vista)
        return vista

    def test_historia_por_instante_muestra_el_estado_de_ese_instante(self):  # FR-LIN-001, FR-LIN-003, FR-LIN-004
        vista = self.consultar("100")
        self.assertEqual(len(vista.historias), 1)
        resumen, referencia = vista.historias[0]
        self.assertEqual(referencia, "t=100")
        self.assertEqual(_campos(resumen), _campos(vista.estados[1][0]))

    def test_historia_por_accion_muestra_el_estado_justo_antes_de_la_accion(self):  # FR-LIN-003, FR-LIN-004
        vista = self.consultar("#3")
        self.assertEqual(len(vista.historias), 1)
        resumen, referencia = vista.historias[0]
        self.assertEqual(referencia, "#3")
        self.assertEqual(_campos(resumen), _campos(vista.estados[2][0]))

    def test_los_limites_cero_y_reloj_actual_son_validos(self):  # FR-LIN-001, FR-LIN-006
        vista = self.consultar("0", "300", "#1")
        self.assertEqual([r for _, r in vista.historias], ["t=0", "t=300", "#1"])
        self.assertEqual(_campos(vista.historias[0][0]), _campos(vista.estados[0][0]))
        self.assertEqual(_campos(vista.historias[1][0]), _campos(vista.estados[3][0]))
        self.assertEqual(_campos(vista.historias[2][0]), _campos(vista.estados[0][0]))

    def test_el_resumen_trae_los_siete_grupos(self):  # FR-LIN-004, SC-LIN-001
        historias = self.consultar("100").historias
        self.assertEqual(len(historias), 1)
        resumen = historias[0][0]
        for nombre in ("tiempo", "sala_id", "vida", "vida_max", "ataque", "defensa", "velocidad",
                       "inventario", "efectos_activos", "enemigos", "mapa_conocido"):
            self.assertTrue(hasattr(resumen, nombre), nombre)
        self.assertGreaterEqual(len(resumen.mapa_conocido), 1)

    def test_una_consulta_valida_no_cambia_nada_ni_se_registra(self):  # FR-LIN-005, SC-LIN-002
        vista = self.consultar("100", "#1", "0")
        self.assertEqual(len(vista.historias), 3)
        antes = vista.instantaneas[3]        # tras las tres esperas y antes de la primera consulta
        self.assertEqual(vista.instantaneas[4:], [antes] * 3)
        _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
        self.assertEqual(len(acciones), 3)

    def test_una_consulta_no_consume_tiempo(self):  # FR-LIN-005
        vista = VistaFalsa(ordenes=self.ESPERAS + [Orden("historia", "100"), Orden("esperar")])
        self.jugar_sin_ajustes(vista)
        self.assertEqual(len(vista.historias), 1)
        self.assertEqual([e[0].tiempo for e in vista.estados], [0, 100, 200, 300, 300, 400])

    RECHAZOS = (("10000", "reloj"), ("301", "reloj"), ("#0", "acción"), ("#4", "acción"), ("#99", "acción"),
                ("abc", None), ("#abc", None), ("#", None), ("-5", None), ("1.5", None), ("1 2", None),
                ("", None), (None, None))

    def test_toda_consulta_rechazada_informa_el_motivo(self):  # FR-LIN-006, FR-LIN-023, SC-LIN-007
        for argumento, palabra in self.RECHAZOS:
            with self.subTest(argumento=argumento):
                vista = self.consultar(argumento)
                self.assertEqual(vista.historias, [])
                self.assertEqual(vista.errores, [])
                self.assertEqual(len(vista.avisos), 1)
                self.assertNotEqual(vista.avisos[0].strip(), "")
                if palabra is not None:
                    self.assertIn(palabra, vista.avisos[0])

    def test_una_consulta_rechazada_no_produce_ningun_efecto(self):  # FR-LIN-023, SC-LIN-007
        for argumento, _ in self.RECHAZOS:
            with self.subTest(argumento=argumento):
                vista = self.consultar(argumento)
                self.assertEqual(len(vista.avisos), 1)
                self.assertNotIn("Orden desconocida", vista.avisos[0])
                self.assertEqual(vista.instantaneas[4], vista.instantaneas[3])
                _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
                self.assertEqual(len(acciones), 3)

    def test_tras_una_consulta_rechazada_el_juego_sigue(self):  # FR-LIN-023
        vista = VistaFalsa(ordenes=self.ESPERAS + [Orden("historia", "999"), Orden("esperar")])
        self.jugar_sin_ajustes(vista)
        self.assertEqual(len(vista.avisos), 1)
        self.assertIn("reloj", vista.avisos[0])
        self.assertEqual(vista.estados[-1][0].tiempo, 400)

    def test_tras_un_pergamino_las_acciones_revertidas_no_se_consultan(self):  # FR-LIN-006, FR-LIN-007
        def dar_pergamino():
            ficha = self.servicio._catalogo.obtener("itm_pergamino_retroceso")
            self.servicio.partida._jugador.inventario.recoger(ObjetoInventario("p0", ficha))
        ordenes = self.ESPERAS + [Orden("pergamino", 1), Orden("historia", "#3"), Orden("historia", "#2"),
                                  Orden("historia", "300"), Orden("historia", "200")]
        vista = VistaConInstantaneas(self.observar, dar_pergamino, ordenes=ordenes)
        self.jugar_sin_ajustes(vista)
        self.assertEqual(vista.estados[-1][0].tiempo, 200)       # el reloj volvió a 200
        self.assertEqual([r for _, r in vista.historias], ["#2", "t=200"])
        self.assertEqual(len(vista.avisos), 2)                   # #3 y t=300 ya no existen
        self.assertEqual(_campos(vista.historias[0][0]), _campos(vista.estados[1][0]))


if __name__ == "__main__":
    unittest.main()