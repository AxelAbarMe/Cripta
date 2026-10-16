"""Pruebas de ServicioPartida (arma la partida, escribe la bitácora, reporta), con la cripta real de fixtures/.

El ClienteOffline no cuenta solicitudes, así que se envuelve en un cliente que las cuenta y respeta el
presupuesto igual que ClienteHttp. Se ejecuta desde la raíz del proyecto con:
    python -m unittest tests.servicios.test_servicio_partida -v
"""
import dataclasses
import tempfile
import unittest
from pathlib import Path

from cripta.excepciones import CriptaApiError, CriptaLimiteError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.modelo.accion import Accion as A
from cripta.modelo.inventario import ObjetoInventario
from cripta.servicios.servicio_partida import ServicioPartida

CRIPTA = "cripta-01"
VERSION_CATALOGO = "cat-prueba"   # solo para comparar estados guardados


class ClienteContado:
    """Cuenta cada llamada como una solicitud de red y lanza CriptaLimiteError al pasarse del presupuesto."""

    def __init__(self, contador, falla_en=None):
        self._base = ClienteOffline("fixtures")
        self._contador = contador
        self._falla_en = falla_en
        self.llamadas = []

    def __getattr__(self, nombre):
        metodo = getattr(self._base, nombre)

        def llamar(*argumentos):
            if self._contador.restantes < 1:
                raise CriptaLimiteError(self._contador.presupuesto_maximo)
            self._contador.registrar_solicitud()
            self.llamadas.append(nombre)
            if nombre == self._falla_en:
                raise CriptaApiError(nombre, 500, "falla simulada")
            return metodo(*argumentos)
        return llamar


def armar(cache_disco=None, tamano=25, falla_en=None):
    contador = ContadorSolicitudes()
    cliente = ClienteContado(contador, falla_en)
    servicio = ServicioPartida(ClienteGeneral(cliente), contador, cache_disco, tamano, asincrono=False)
    return servicio, contador, cliente


def iniciar(servicio, ruta_bitacora=None, semilla=5):
    servicio.iniciar_nueva(CRIPTA, semilla, ruta_bitacora)
    servicio.partida._jugador.vida_max = servicio.partida._jugador.vida = 1000   # las ratas no matan en la prueba


def sin_mensajes(estado):
    # Una acción rechazada deja su motivo en los mensajes pero no se anota en la bitácora: es lo único que
    # una partida reproducida puede tener distinto
    return dataclasses.replace(estado, mensajes=())


def juego(estado):
    """Lo que es estado del juego. Quedan fuera los mensajes (solo se muestran) y que una sala tenga su
    contenido cargado (es infraestructura): ninguno de los dos se deshace."""
    return (estado.reloj_actual, estado.siguiente_secuencia, estado.rng, estado.acciones_jugador,
            estado.enemigos_derrotados, estado.jugador, estado.eventos,
            [(s.sala_id, s.rastro, s.puertas_cerradas) for s in estado.salas])


class PruebaServicioPartida(unittest.TestCase):
    def test_arranque_en_frio_cuenta_las_solicitudes_y_reporta(self):
        servicio, contador, cliente = armar()
        iniciar(servicio)
        self.assertEqual(cliente.llamadas[:3], ["obtener_general", "obtener_version_catalogo", "obtener_pagina_esqueleto"])
        self.assertEqual(contador.presupuesto_maximo, 9)     # lo fijó la cripta, no el programa
        self.assertLessEqual(contador.realizadas, contador.presupuesto_maximo)
        reporte = servicio.reporte_final()
        for texto in ("Solicitudes realizadas:", "Presupuesto máximo: 9", "aciertos=", "fallos=", "Precarga:"):
            self.assertIn(texto, reporte)
        servicio.cerrar()

    def test_con_la_cache_caliente_solo_quedan_las_dos_verificaciones_de_version(self):
        with tempfile.TemporaryDirectory() as carpeta:
            disco = CacheDisco(AlmacenDiscoArchivos(carpeta))
            primero, _, _ = armar(disco)
            iniciar(primero)
            primero.ejecutar(A("mover", "N"))
            primero.cerrar()
            segundo, contador, cliente = armar(disco)
            iniciar(segundo)
            segundo.ejecutar(A("mover", "N"))
            self.assertEqual(cliente.llamadas, ["obtener_general", "obtener_version_catalogo"])
            segundo.cerrar()

    def test_la_bitacora_solo_anota_las_acciones_aceptadas_y_el_pergamino(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = str(Path(carpeta) / "partida.log")
            servicio, _, _ = armar()
            iniciar(servicio, ruta, semilla=42)
            ficha = servicio._catalogo.obtener("itm_pergamino_retroceso")
            servicio.partida._jugador.inventario.recoger(ObjetoInventario("p0", ficha))
            acciones = [A("esperar"), A("mover", "S"), A("mover", "N"), A("pergamino")]   # "S" no existe en la sala 1
            resultados = [servicio.ejecutar(a) for a in acciones]
            self.assertEqual([r.aceptada for r in resultados], [True, False, True, True])
            encabezado, anotadas = LectorBitacoraPartida(ruta).leer()
            self.assertEqual(
                (encabezado["id_cripta"], encabezado["semilla"], encabezado["version_cripta"]),
                (CRIPTA, 42, servicio.datos_generales.version),
            )
            self.assertEqual(encabezado["version_catalogo"], servicio.version_catalogo)
            self.assertEqual(anotadas, ({"tipo": "esperar"}, {"tipo": "mover", "direccion": "N"}, {"tipo": "pergamino"}))
            servicio.cerrar()

    def test_reproducir_la_bitacora_da_la_misma_partida(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = str(Path(carpeta) / "partida.log")
            original, _, _ = armar()
            iniciar(original, ruta, semilla=7)
            guion = [A("mover", "N"), A("esperar"), A("mover", "O"), A("atacar", "e-201"), A("esperar"), A("atacar", "e-202")]
            for accion in guion:
                original.ejecutar(accion)
            encabezado, anotadas = LectorBitacoraPartida(ruta).leer()

            reproducida, _, _ = armar()
            iniciar(reproducida, None, semilla=encabezado["semilla"])
            for datos in anotadas:
                self.assertTrue(reproducida.ejecutar(A.desde_dict(datos)).aceptada)
            a, b = original.partida, reproducida.partida
            self.assertEqual(sin_mensajes(a.a_estado_guardado(VERSION_CATALOGO)), sin_mensajes(b.a_estado_guardado(VERSION_CATALOGO)))
            self.assertEqual((a.vista(), a.puntaje()), (b.vista(), b.puntaje()))
            original.cerrar()
            reproducida.cerrar()

    def test_fichas_en_uso(self):
        servicio, _, _ = armar()
        iniciar(servicio)
        p = servicio.partida
        self.assertCountEqual(p.fichas_en_uso(), ["itm_antorcha"])           # solo el suelo de la sala inicial
        servicio.ejecutar(A("recoger", "itm_antorcha"))
        self.assertCountEqual(p.fichas_en_uso(), ["itm_antorcha"])           # ahora en el inventario
        servicio.ejecutar(A("mover", "N"))
        en_uso = p.fichas_en_uso()
        self.assertEqual(en_uso.count("ent_rata_gigante"), 2)                # dos ratas vivas
        self.assertIn("trp_dardos", en_uso)
        self.assertIn("itm_daga_oxidada", en_uso)                            # el suelo de la sala donde está
        servicio.cerrar()

    def test_con_la_cache_chica_nunca_se_desaloja_una_ficha_en_uso(self):
        with tempfile.TemporaryDirectory() as carpeta:
            servicio, contador, _ = armar(CacheDisco(AlmacenDiscoArchivos(carpeta)), tamano=3)
            iniciar(servicio)
            for accion in [A("recoger", "itm_antorcha"), A("mover", "N"), A("esperar"), A("atacar", "e-201"),
                           A("esperar"), A("mover", "S"), A("mover", "N")]:
                servicio.ejecutar(accion)
                servicio.partida.vista()
                p = servicio.partida
                sala = p._sala_actual()
                # Lo que se consulta por id (inventario, suelo y trampas de la sala actual) no puede haberse desalojado.
                # Un enemigo sí puede faltar en la caché: se desalojó mientras dormía y conserva su propia ficha
                consultadas = set(p._jugador.inventario.fichas_en_uso()) | set(sala.objetos_en_suelo) \
                    | {t.tipo_catalogo for t in sala.trampas}
                self.assertTrue(consultadas <= set(servicio._catalogo.ids_en_memoria()), accion.a_dict())
            self.assertGreater(servicio._catalogo.estadisticas.recuperadas_disco, 0)   # desalojó y recuperó, sin red
            self.assertLessEqual(contador.realizadas, contador.presupuesto_maximo)
            servicio.cerrar()

    def test_si_la_infraestructura_falla_en_una_accion_la_partida_queda_como_estaba(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = str(Path(carpeta) / "partida.log")
            servicio, contador, _ = armar(tamano=3)           # sin disco y con caché chica: se agota el presupuesto
            iniciar(servicio, ruta)
            fallo = False
            for accion in [A("recoger", "itm_antorcha"), A("mover", "N"), A("esperar"), A("atacar", "e-201"),
                           A("esperar"), A("mover", "S"), A("mover", "N"), A("esperar"), A("mover", "S")]:
                antes = servicio.partida.a_estado_guardado(VERSION_CATALOGO)
                anotadas_antes = LectorBitacoraPartida(ruta).leer()[1]
                try:
                    servicio.ejecutar(accion)
                except CriptaLimiteError:
                    fallo = True
                    self.assertEqual(juego(servicio.partida.a_estado_guardado(VERSION_CATALOGO)), juego(antes))
                    self.assertEqual(LectorBitacoraPartida(ruta).leer()[1], anotadas_antes)   # la que falló no se anotó
                    break
            self.assertTrue(fallo, "la prueba debía agotar el presupuesto")
            servicio.cerrar()

    def test_si_la_infraestructura_falla_a_mitad_de_un_movimiento_se_deshace_lo_ya_cambiado(self):
        servicio, _, _ = armar()
        iniciar(servicio)
        p = servicio.partida
        antes = p.a_estado_guardado(VERSION_CATALOGO)
        obtener = servicio._catalogo.obtener

        def falla_con_la_trampa(ficha_id):    # la trampa se activa DESPUÉS de que el jugador ya entró a la sala 2
            if ficha_id == "trp_dardos" and p._jugador.sala_actual == 2:
                raise CriptaLimiteError(9)
            return obtener(ficha_id)
        servicio._catalogo.obtener = falla_con_la_trampa
        with self.assertRaises(CriptaLimiteError):
            servicio.ejecutar(A("mover", "N"))
        self.assertEqual(juego(p.a_estado_guardado(VERSION_CATALOGO)), juego(antes))   # sigue en la sala 1, sin rastro ni enemigos activos
        servicio._catalogo.obtener = obtener
        self.assertTrue(servicio.ejecutar(A("mover", "N")).aceptada)     # y reintentar funciona
        limpio, _, _ = armar()
        iniciar(limpio)
        limpio.ejecutar(A("mover", "N"))
        self.assertEqual(sin_mensajes(p.a_estado_guardado(VERSION_CATALOGO)), sin_mensajes(limpio.partida.a_estado_guardado(VERSION_CATALOGO)))
        servicio.cerrar()
        limpio.cerrar()

    def test_si_falla_al_iniciar_no_queda_partida(self):
        servicio, _, _ = armar(falla_en="obtener_contenido")
        with self.assertRaises(CriptaApiError):
            iniciar(servicio)
        with self.assertRaises(RuntimeError):
            servicio.partida


if __name__ == "__main__":
    unittest.main()