"""Pruebas de ServicioPartida parte 2: guardar, cargar (con su bitácora), puntaje final y ranking.
Usan la cripta real de fixtures/. Se ejecutan desde la raíz del proyecto con:
    python -m unittest tests.servicios.test_servicio_partida_guardado -v
"""
import dataclasses
import tempfile
import unittest
from pathlib import Path

from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.infraestructura.puntajes_disco import RepositorioPuntajes
from cripta.modelo.accion import Accion as A
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.puntajes import Puntaje
from cripta.servicios.servicio_partida import ServicioPartida
from tests.servicios.test_servicio_partida import ClienteContado, juego

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


if __name__ == "__main__":
    unittest.main()