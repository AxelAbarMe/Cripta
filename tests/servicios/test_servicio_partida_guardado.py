"""Pruebas de ServicioPartida parte 2: guardar, cargar (con su bitácora), puntaje final y ranking.
Usan la cripta congelada de tests/datos/. Se ejecutan desde la raíz del proyecto con:
    python -m unittest tests.servicios.test_servicio_partida_guardado -v
"""
import dataclasses
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.infraestructura.puntajes_disco import RepositorioPuntajes
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.linea_tiempo import LineaTiempo
from cripta.modelo.partida import Partida
from cripta.modelo.puntajes import Puntaje
from cripta.servicios.servicio_partida import ServicioPartida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from cripta.infraestructura.cliente_offline import ClienteOffline
from tests.servicios.test_servicio_partida import ClienteContado, juego
from tests.modelo.test_conocimiento_jugador import crear_mapa, salida

CRIPTA = "cripta-01"


class ClienteSalaCuatro(ClienteContado):
    """La cripta de pruebas, pero con la sala inicial en la 4 (junto a la salida) para poder ganar enseguida."""

    def __getattr__(self, nombre):
        llamar = super().__getattr__(nombre)
        if nombre != "obtener_general":
            return llamar
        return lambda *argumentos: dataclasses.replace(llamar(*argumentos), sala_inicial=4)


class ClienteOtroCatalogo(ClienteContado):
    def __getattr__(self, nombre):
        llamar = super().__getattr__(nombre)
        if nombre != "obtener_version_catalogo":
            return llamar
        return lambda *argumentos: dataclasses.replace(llamar(*argumentos), version="cat-otra")


def armar(clase_cliente=ClienteContado, repositorio=None):
    contador = ContadorSolicitudes()
    servicio = ServicioPartida(
        ClienteGeneral(clase_cliente(contador)), contador, asincrono=False, repositorio_puntajes=repositorio
    )
    return servicio


def iniciar(servicio, ruta_bitacora=None, semilla=5):
    servicio.iniciar_nueva(CRIPTA, semilla, ruta_bitacora)
    servicio.partida._jugador.vida_max = servicio.partida._jugador.vida = 1000   # las ratas no matan en la prueba


ANTES = [A("recoger", "itm_antorcha"), A("mover", "N"), A("esperar"), A("atacar", "e-201")]
DESPUES = [A("atacar", "e-201"), A("esperar"), A("atacar", "e-202"), A("mover", "S"), A("mover", "N"), A("esperar")]


def estado_de(servicio):
    return servicio.partida.a_estado_guardado(servicio.version_catalogo)


class PruebaGuardarYCargar(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.dir = Path(self._carpeta.name)

    def tearDown(self):
        self._carpeta.cleanup()

    def test_una_partida_cargada_sigue_igual_que_la_que_nunca_se_guardo(self):
        a = armar()
        iniciar(a)
        for accion in ANTES:
            a.ejecutar(accion)
        ruta = self.dir / "partida.bin"
        a.guardar(ruta)
        b = armar()
        b.cargar(ruta)
        self.assertEqual(juego(estado_de(a)), juego(estado_de(b)))       # recién cargada
        self.assertEqual(b.semilla, 5)
        for accion in DESPUES:
            self.assertEqual(a.ejecutar(accion).aceptada, b.ejecutar(accion).aceptada)
        self.assertEqual(juego(estado_de(a)), juego(estado_de(b)))       # y después de seguir jugando las dos
        self.assertEqual((a.partida.vista(), a.partida.puntaje()), (b.partida.vista(), b.partida.puntaje()))
        a.cerrar()
        b.cerrar()

    def test_la_partida_cargada_asigna_el_mismo_id_al_siguiente_objeto_recogido(self):  # FR-LIN-010, FR-LIN-021
        a = armar()
        iniciar(a)
        for accion in (A("recoger", "itm_antorcha"), A("soltar", 0)):    # el contador queda en 1 y el inventario vacío
            a.ejecutar(accion)
        ruta = self.dir / "partida.bin"
        a.guardar(ruta)
        b = armar()
        b.cargar(ruta)
        for servicio in (a, b):
            self.assertTrue(servicio.ejecutar(A("recoger", "itm_antorcha")).aceptada)
        ids = lambda servicio: [o.instancia_id for o in servicio.partida._jugador.inventario.objetos_en_orden()]
        self.assertEqual(ids(a), ["i-2"])
        self.assertEqual(ids(b), ids(a))
        a.cerrar()
        b.cerrar()

    def test_los_checkpoints_creados_tras_cargar_coinciden_con_los_de_la_original(self):  # FR-LIN-010, FR-LIN-017
        a = armar()
        iniciar(a)
        a.partida._linea = LineaTiempo(2)
        for accion in (A("recoger", "itm_antorcha"), A("soltar", 0), A("esperar"), A("esperar")):
            a.ejecutar(accion)
        ruta = self.dir / "partida.bin"
        a.guardar(ruta)
        b = armar()
        b.cargar(ruta)
        for accion in (A("recoger", "itm_antorcha"), A("esperar"), A("esperar")):
            self.assertEqual(a.ejecutar(accion).aceptada, b.ejecutar(accion).aceptada)
        linea_a, linea_b = estado_de(a).linea, estado_de(b).linea
        self.assertEqual(len(linea_a.checkpoints), 3)
        self.assertEqual(linea_b.checkpoints, linea_a.checkpoints)
        self.assertEqual(linea_b, linea_a)
        a.cerrar()
        b.cerrar()

    def test_cargar_restaura_la_bitacora_hasta_el_guardado_y_sigue_en_ella(self):
        a = armar()
        ruta_a, ruta = str(self.dir / "a.log"), self.dir / "partida.bin"
        iniciar(a, ruta_a, semilla=9)
        for accion in ANTES:
            a.ejecutar(accion)
        a.guardar(ruta)
        for accion in DESPUES:                  # una rama que se abandona al cargar
            a.ejecutar(accion)
        hasta_el_guardado = LectorBitacoraPartida(str(ruta) + ".log").leer()[1]
        self.assertLess(len(hasta_el_guardado), len(LectorBitacoraPartida(ruta_a).leer()[1]))

        b = armar()
        ruta_b = str(self.dir / "b.log")
        b.cargar(ruta, ruta_b)
        self.assertTrue(b.bitacora_completa)
        self.assertEqual(LectorBitacoraPartida(ruta_b).leer()[1], hasta_el_guardado)   # sin acciones de la rama abandonada
        for accion in [A("atacar", "e-202"), A("esperar"), A("mover", "S")]:
            b.ejecutar(accion)

        # La bitácora de lo cargado, reproducida desde cero, da la misma partida
        encabezado, acciones = LectorBitacoraPartida(ruta_b).leer()
        r = armar()
        iniciar(r, None, semilla=encabezado["semilla"])
        for datos in acciones:
            self.assertTrue(r.ejecutar(A.desde_dict(datos)).aceptada)
        self.assertEqual(juego(estado_de(b)), juego(estado_de(r)))
        for s in (a, b, r):
            s.cerrar()

    def test_si_falta_la_copia_de_la_bitacora_la_nueva_queda_marcada_como_parcial(self):
        a = armar()
        iniciar(a, str(self.dir / "a.log"))
        a.ejecutar(A("esperar"))
        ruta = self.dir / "partida.bin"
        a.guardar(ruta)
        Path(str(ruta) + ".log").unlink()
        b = armar()
        b.cargar(ruta, str(self.dir / "b.log"))
        self.assertFalse(b.bitacora_completa)
        encabezado, acciones = LectorBitacoraPartida(str(self.dir / "b.log")).leer()
        self.assertTrue(encabezado["parcial"])
        self.assertEqual(acciones, ())
        a.cerrar()
        b.cerrar()

    def test_una_bitacora_parcial_sigue_siendo_parcial_tras_guardar_y_cargar_otra_vez(self):
        a = armar()
        iniciar(a, str(self.dir / "a.log"))
        ruta1, ruta2 = self.dir / "uno.bin", self.dir / "dos.bin"
        a.guardar(ruta1)
        Path(str(ruta1) + ".log").unlink()
        b = armar()
        b.cargar(ruta1, str(self.dir / "b.log"))        # parcial: no se tiene lo anterior al guardado
        b.ejecutar(A("esperar"))
        b.guardar(ruta2)                                # guarda su bitácora, que sigue siendo parcial
        c = armar()
        c.cargar(ruta2, str(self.dir / "c.log"))
        self.assertFalse(c.bitacora_completa)
        self.assertTrue(LectorBitacoraPartida(str(self.dir / "c.log")).leer()[0]["parcial"])
        for servicio in (a, b, c):
            servicio.cerrar()

    def test_guardar_sin_bitacora_no_deja_una_copia_vieja(self):
        a = armar()
        iniciar(a, str(self.dir / "a.log"))
        ruta = self.dir / "partida.bin"
        a.guardar(ruta)
        self.assertTrue(Path(str(ruta) + ".log").is_file())
        sin = armar()
        iniciar(sin, None)
        sin.guardar(ruta)
        self.assertFalse(Path(str(ruta) + ".log").exists())
        a.cerrar()
        sin.cerrar()

    def test_un_guardado_de_otro_catalogo_no_se_carga_y_la_partida_en_curso_sigue(self):
        a = armar()
        iniciar(a)
        ruta = self.dir / "partida.bin"
        a.guardar(ruta)
        b = armar(ClienteOtroCatalogo)
        iniciar(b)
        en_curso = b.partida
        with self.assertRaises(CriptaFormatoIncompatibleError):
            b.cargar(ruta)
        self.assertIs(b.partida, en_curso)
        a.cerrar()
        b.cerrar()

    def test_cargar_un_archivo_que_no_existe_no_toca_la_partida_en_curso(self):
        a = armar()
        iniciar(a)
        en_curso = a.partida
        with self.assertRaises(FileNotFoundError):
            a.cargar(self.dir / "no_existe.bin")
        self.assertIs(a.partida, en_curso)
        a.cerrar()


class PruebaPuntajes(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.almacen = AlmacenDiscoArchivos(self._carpeta.name)
        self.repositorio = RepositorioPuntajes(self.almacen)

    def tearDown(self):
        self._carpeta.cleanup()

    def _ganar(self):
        s = armar(ClienteSalaCuatro, self.repositorio)
        iniciar(s)
        llave = s._catalogo.obtener("itm_llave_negra")
        s.partida._jugador.inventario.recoger(ObjetoInventario("k2", llave))
        s.ejecutar(A("abrir", "E"))
        s.ejecutar(A("mover", "E"))
        self.assertEqual(s.partida.desenlace(), "victoria")
        return s

    def test_entrar_a_la_salida_sin_la_llave_de_salida_no_gana(self):
        s = armar(ClienteSalaCuatro, self.repositorio)
        iniciar(s)
        llave = s._catalogo.obtener("itm_llave_negra")
        s.partida._jugador.inventario.recoger(ObjetoInventario("k2", llave))
        s.partida._datos = dataclasses.replace(s.partida._datos, llave_salida="itm_otra_llave")   # §2.12
        s.ejecutar(A("abrir", "E"))
        s.ejecutar(A("mover", "E"))
        self.assertEqual(s.partida.desenlace(), "en_curso")
        self.assertEqual(s.partida.vista().sala_id, s.partida._datos.sala_salida)

    def _perder(self):
        s = armar(ClienteContado, self.repositorio)
        s.iniciar_nueva(CRIPTA, 5)
        s.partida._jugador.vida = s.partida._jugador.vida_max = 1
        s.ejecutar(A("mover", "N"))
        for _ in range(6):
            if s.partida.desenlace() != "en_curso":
                break
            s.ejecutar(A("esperar"))
        self.assertEqual(s.partida.desenlace(), "derrota")
        return s

    def test_el_puntaje_se_registra_una_sola_vez_y_las_victorias_van_primero(self):
        perdida = self._perder()
        ranking = perdida.registrar_puntaje("Beto")
        self.assertEqual([(p.nombre_jugador, p.victoria) for p in ranking], [("Beto", False)])
        ganada = self._ganar()
        ranking = ganada.registrar_puntaje("  Ana ")
        self.assertEqual([(p.nombre_jugador, p.victoria) for p in ranking], [("Ana", True), ("Beto", False)])
        # la derrota tiene menos tiempo y aun así queda detrás de la victoria
        self.assertLess(perdida.partida.puntaje().tiempo_final, ganada.partida.puntaje().tiempo_final)
        with self.assertRaises(RuntimeError):
            ganada.registrar_puntaje("Ana")
        # quedó en disco: otra tabla leída desde el archivo ve los dos
        self.assertEqual(len(RepositorioPuntajes(self.almacen).cargar()), 2)
        self.assertEqual([p.nombre_jugador for p in ganada.ranking()], ["Ana", "Beto"])
        perdida.cerrar()
        ganada.cerrar()

    def test_no_se_registra_una_partida_en_curso_ni_con_nombre_vacio(self):
        s = armar(ClienteContado, self.repositorio)
        iniciar(s)
        with self.assertRaises(RuntimeError):
            s.registrar_puntaje("Ana")
        s.cerrar()
        g = self._ganar()
        with self.assertRaises(ValueError):
            g.registrar_puntaje("   ")
        g.cerrar()

    def test_el_ranking_es_solo_de_la_cripta_y_la_version_de_la_partida(self):
        ganada = self._ganar()
        self.repositorio.registrar(Puntaje("Otra versión", CRIPTA, "otra", 1, 0, 10, True))
        self.repositorio.registrar(Puntaje("Otra cripta", "cripta-99", ganada.datos_generales.version, 1, 0, 10, True))
        ranking = ganada.registrar_puntaje("Ana")
        self.assertEqual([p.nombre_jugador for p in ranking], ["Ana"])
        ganada.cerrar()


    def test_los_puntajes_globales_mezclan_criptas_con_las_victorias_primero(self):
        self.repositorio.registrar(Puntaje("Derrota", "cripta-99", "v9", 5, 3, 100, False))
        self.repositorio.registrar(Puntaje("Victoria", CRIPTA, "otra", 5, 0, 900, True))
        s = armar(ClienteContado, self.repositorio)
        self.assertEqual([p.nombre_jugador for p in s.puntajes_globales()], ["Victoria", "Derrota"])
        s.cerrar()

    def test_puntajes_globales_sin_tabla_configurada(self):
        with self.assertRaises(RuntimeError):
            armar(ClienteContado).puntajes_globales()


class PruebaConocimientoGuardado(unittest.TestCase):
    def test_proyecta_y_restaura_conocimiento_y_permite_retroceso_nuevo(self):
        servicio = armar()
        self.addCleanup(servicio.cerrar)
        iniciar(servicio)
        ficha = servicio._catalogo.obtener("itm_antorcha")
        servicio.partida._jugador.inventario.recoger(ObjetoInventario("antorcha-t010", ficha))
        pergamino = servicio._catalogo.obtener("itm_pergamino_retroceso")
        servicio.partida._jugador.inventario.recoger(ObjetoInventario("pergamino-t010", pergamino))
        self.assertTrue(servicio.ejecutar(A("usar", 0)).aceptada)
        self.assertTrue(servicio.ejecutar(A("mover", "N")).aceptada)
        estado = estado_de(servicio)
        original = servicio.partida._conocimiento.proyectar()
        self.assertIsNotNone(estado.conocimiento)
        sala_dos = next(sala for sala in original if sala.id_sala == 2)
        self.assertEqual(next(salida.estado_puerta for salida in sala_dos.salidas if salida.direccion == "E"), "cerrada")
        self.assertEqual(next(sala.estado for sala in original if sala.id_sala == 3), "explorada")
        cliente = ClienteOffline("tests/datos")
        general = cliente.obtener_general(CRIPTA)
        mapa = CriptaMapa()
        catalogo = ServicioCatalogo(cliente)
        precarga = ServicioPrecarga(cliente, CRIPTA, mapa, servicio_catalogo=catalogo, asincrono=False)
        self.addCleanup(precarga.cerrar)
        precarga.cargar_esqueleto(general.paginas)
        restaurada = Partida.desde_estado_guardado(estado, general, mapa, catalogo, precarga)
        self.assertEqual(restaurada._conocimiento.proyectar(), original)
        antes_de_nueva_entrada = restaurada._conocimiento.proyectar()
        self.assertTrue(restaurada.ejecutar_accion(A("mover", "N")).aceptada)
        self.assertNotEqual(restaurada._conocimiento.proyectar(), antes_de_nueva_entrada)
        self.assertTrue(restaurada.ejecutar_accion(A("pergamino")).aceptada)
        self.assertEqual(restaurada._conocimiento.proyectar(), antes_de_nueva_entrada)

    def test_conocimiento_completo_de_puertas_se_conserva_al_restaurar(self):
        salas = (
            {"id": 1, "nombre": "A", "salidas": {"E": salida(2, cerrada=True, llave="llave"), "N": salida(3)}},
            {"id": 2, "nombre": "B", "salidas": {"O": salida(1, cerrada=True, llave="llave"), "S": salida(3)}},
            {"id": 3, "nombre": "C", "salidas": {"S": salida(1), "N": salida(2)}},
        )
        mapa = crear_mapa(salas)
        general = SimpleNamespace(
            id="sintetica", version="1", sala_inicial=1, sala_salida=99, llave_salida="salida", inventario_max=4,
            jugador=SimpleNamespace(vida=100, vida_max=100, ataque=10, defensa=0, velocidad=100),
        )
        ficha = SimpleNamespace(id="antorcha", clase="antorcha", nombre="Antorcha", peso=1, valor=1, duracion=5000)

        class Catalogo:
            def obtener(self, ficha_id):
                return ficha

        class Precarga:
            def __init__(self, mapa_partida):
                self.mapa = mapa_partida

            def preparar_sala(self, sala_id):
                return self.mapa.obtener(sala_id)

            def precargar_desde(self, sala_id):
                return None

        partida = Partida(general, mapa, Catalogo(), Precarga(mapa), 7)
        partida.iniciar()
        partida._jugador.inventario.recoger(ObjetoInventario("antorcha", ficha))
        estado = partida.a_estado_guardado("catalogo")

        mapa_restaurado = crear_mapa(salas)
        restaurada = Partida.desde_estado_guardado(
            estado, general, mapa_restaurado, Catalogo(), Precarga(mapa_restaurado)
        )

        self.assertTrue(partida.ejecutar_accion(A("usar", 0)).aceptada)
        self.assertTrue(restaurada.ejecutar_accion(A("usar", 0)).aceptada)
        self.assertTrue(partida.ejecutar_accion(A("mover", "N")).aceptada)
        self.assertTrue(restaurada.ejecutar_accion(A("mover", "N")).aceptada)
        self.assertEqual(partida._conocimiento.proyectar(), restaurada._conocimiento.proyectar())
        sala_b = next(sala for sala in restaurada._conocimiento.proyectar() if sala.id_sala == 2)
        self.assertEqual(next(salida.estado_puerta for salida in sala_b.salidas if salida.direccion == "O"), "cerrada")

    def test_estado_sin_conocimiento_reconstruye_la_sala_actual_y_retroceso(self):
        servicio = armar()
        self.addCleanup(servicio.cerrar)
        iniciar(servicio)
        ficha_pergamino = servicio._catalogo.obtener("itm_pergamino_retroceso")
        servicio.partida._jugador.inventario.recoger(ObjetoInventario("pergamino-sin-conocimiento", ficha_pergamino))
        estado = dataclasses.replace(estado_de(servicio), conocimiento=None)
        cliente = ClienteOffline("tests/datos")
        general = cliente.obtener_general(CRIPTA)
        mapa = CriptaMapa()
        catalogo = ServicioCatalogo(cliente)
        precarga = ServicioPrecarga(cliente, CRIPTA, mapa, servicio_catalogo=catalogo, asincrono=False)
        self.addCleanup(precarga.cerrar)
        precarga.cargar_esqueleto(general.paginas)
        restaurada = Partida.desde_estado_guardado(estado, general, mapa, catalogo, precarga)
        previo = restaurada._conocimiento.proyectar()
        self.assertEqual(restaurada._conocimiento.estado_de_sala(restaurada._jugador.sala_actual), "explorada")
        self.assertTrue(restaurada.ejecutar_accion(A("mover", "N")).aceptada)
        self.assertTrue(restaurada.ejecutar_accion(A("pergamino")).aceptada)
        self.assertEqual(restaurada._conocimiento.proyectar(), previo)


    def test_conocimiento_binario_guardado_y_cargado_coincide_y_permite_ir_a_e_historia(self):
        # FR-NIE-006, SC-NIE-005: guardar/cargar en binario conserva el conocimiento completo:
        # estados de sala, observaciones de puertas y costos de salida. La partida cargada
        # calcula la misma ruta con ir_a y recupera el mismo mapa conocido para un instante anterior.
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        ruta = Path(carpeta.name) / "niebla.bin"

        # Juego original: recoger antorcha (accion 1), encender (accion 2) y moverse (accion 3).
        # Al mover con antorcha: sala destino explorada y vecinas avistadas; puerta observada y recordada.
        a = armar()
        self.addCleanup(a.cerrar)
        iniciar(a)
        self.assertTrue(a.ejecutar(A("recoger", "itm_antorcha")).aceptada)   # accion 1
        self.assertTrue(a.ejecutar(A("usar", 0)).aceptada)                   # accion 2: antorcha encendida
        sala_origen = a.partida.vista().sala_id
        t_antes_de_mover = a.partida.vista().tiempo                          # instante justo antes del movimiento
        self.assertTrue(a.ejecutar(A("mover", "N")).aceptada)                # accion 3: entrar a sala vecina
        sala_destino = a.partida.vista().sala_id
        conocimiento_original = a.partida._conocimiento.proyectar()

        # Verificar escenario de niebla: exploradas, avistadas y puerta observada (no «no_observada»)
        estados = [s.estado for s in conocimiento_original]
        self.assertIn("explorada", estados)
        self.assertIn("avistada", estados)
        sala_origen_vista = next(s for s in conocimiento_original if s.id_sala == sala_origen)
        puertas_observadas = [sal.estado_puerta for sal in sala_origen_vista.salidas if sal.estado_puerta != "no_observada"]
        self.assertTrue(len(puertas_observadas) > 0)

        # Ruta calculada con ir_a desde la posicion actual hacia el origen
        paso_a = a.partida.siguiente_paso(sala_origen)
        self.assertIsNotNone(paso_a.direccion)

        # Mapa conocido antes del movimiento (dos acciones vigentes antes: accion 3 es la siguiente)
        historia_antes_a = a.partida.consultar_accion(3)

        # Guardar en binario con ServicioPartida y cargar en servicio nuevo
        a.guardar(ruta)
        b = armar()
        self.addCleanup(b.cerrar)
        b.cargar(ruta)

        # 1. El conocimiento (estados de sala, puertas y costos) coincide exactamente
        conocimiento_b = b.partida._conocimiento.proyectar()
        self.assertEqual(conocimiento_b, conocimiento_original)

        # 2. ir_a calcula la misma ruta: mismo primer paso hacia el origen
        paso_b = b.partida.siguiente_paso(sala_origen)
        self.assertEqual(paso_b.direccion, paso_a.direccion)

        # 3. historia del instante anterior al movimiento muestra el mismo mapa conocido
        historia_antes_b = b.partida.consultar_accion(3)
        self.assertEqual(historia_antes_b.mapa_conocido, historia_antes_a.mapa_conocido)


if __name__ == "__main__":
    unittest.main()
