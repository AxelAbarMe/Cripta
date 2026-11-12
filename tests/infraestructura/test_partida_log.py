"""Pruebas de la bitácora de partida para --replay: EscritorBitacoraPartida,
LectorBitacoraPartida y diferencias_de_version.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.infraestructura.test_partida_log -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.excepciones import CriptaBitacoraError
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.partida_log import (
    EscritorBitacoraPartida, LectorBitacoraPartida, diferencias_de_version,
)
from cripta.modelo.accion import Accion as A
from cripta.servicios.servicio_partida import ServicioPartida
from tests.cliente_falso import ClienteFalso

ENCABEZADO = {"id_cripta": "cripta-01", "version_cripta": "fd58f7743b9e",
              "version_catalogo": "be68d322d2f5", "semilla": 42}
ACCIONES = ({"tipo": "mover", "direccion": "N"},
            {"tipo": "atacar", "instancia": "e-201"},
            {"tipo": "esperar"})


class TestBitacoraPartida(unittest.TestCase):
    def setUp(self):
        # Cada test usa una carpeta temporal propia que se borra al terminar
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = str(Path(carpeta.name) / "partida.log")

    def escribir(self, encabezado=ENCABEZADO, acciones=ACCIONES):
        escritor = EscritorBitacoraPartida(self.ruta, encabezado)
        for accion in acciones:
            escritor.registrar_accion(accion)

    def test_lo_escrito_se_lee_igual(self):
        self.escribir()
        encabezado, acciones = LectorBitacoraPartida(self.ruta).leer()
        self.assertEqual(encabezado, {**ENCABEZADO, "tipo": "encabezado"})
        self.assertEqual(acciones, ACCIONES)

    def test_una_partida_nueva_en_la_misma_ruta_reemplaza_la_anterior(self):
        self.escribir()
        self.escribir({**ENCABEZADO, "semilla": 7}, ({"tipo": "esperar"},))
        encabezado, acciones = LectorBitacoraPartida(self.ruta).leer()
        self.assertEqual(encabezado["semilla"], 7)
        self.assertEqual(acciones, ({"tipo": "esperar"},))

    def test_la_ultima_linea_cortada_se_ignora_y_se_avisa(self):
        self.escribir()
        with open(self.ruta, "a", encoding="utf-8") as archivo:
            archivo.write('{"tipo": "mov')        # el programa se cerró a mitad de escribir
        lector = LectorBitacoraPartida(self.ruta)
        _, acciones = lector.leer()
        self.assertEqual(acciones, ACCIONES)
        self.assertTrue(lector.ultima_linea_incompleta)

    def test_un_archivo_sano_no_avisa_linea_cortada(self):
        self.escribir()
        lector = LectorBitacoraPartida(self.ruta)
        lector.leer()
        self.assertFalse(lector.ultima_linea_incompleta)

    def test_una_linea_rota_en_medio_es_error(self):
        self.escribir()
        lineas = Path(self.ruta).read_text(encoding="utf-8").splitlines()
        lineas[1] = "esto no es json"
        Path(self.ruta).write_text("\n".join(lineas) + "\n", encoding="utf-8")
        with self.assertRaises(CriptaBitacoraError):
            LectorBitacoraPartida(self.ruta).leer()

    def test_archivo_que_no_existe_o_vacio_es_error(self):
        with self.assertRaises(CriptaBitacoraError):
            LectorBitacoraPartida(self.ruta).leer()
        Path(self.ruta).write_text("", encoding="utf-8")
        with self.assertRaises(CriptaBitacoraError):
            LectorBitacoraPartida(self.ruta).leer()

    def test_si_la_primera_linea_no_es_encabezado_es_error(self):
        Path(self.ruta).write_text('{"tipo": "esperar"}\n', encoding="utf-8")
        with self.assertRaises(CriptaBitacoraError):
            LectorBitacoraPartida(self.ruta).leer()

    def test_escribir_con_encabezado_incompleto_es_error_de_programacion(self):
        # ValueError y no CriptaBitacoraError: es un error del código que llama, no del archivo
        with self.assertRaises(ValueError):
            EscritorBitacoraPartida(self.ruta, {"id_cripta": "cripta-01"})


class TestDiferenciasDeVersion(unittest.TestCase):
    def test_mismas_versiones_no_hay_diferencias(self):
        self.assertEqual(diferencias_de_version(ENCABEZADO, "fd58f7743b9e", "be68d322d2f5"), ())

    def test_cada_version_distinta_se_reporta(self):
        self.assertEqual(len(diferencias_de_version(ENCABEZADO, "otra", "be68d322d2f5")), 1)
        self.assertEqual(len(diferencias_de_version(ENCABEZADO, "otra", "otra")), 2)


def _ficha(identificador, comportamiento, rango=None):
    ficha = {"id": identificador, "clase": "enemigo", "nombre": identificador, "vida_max": 1000, "ataque": 10,
             "defensa": 0, "velocidad": 100, "comportamiento": comportamiento}
    if rango is not None:
        ficha["rango"] = rango
    return ficha


def _servicio_sintetico():
    """Cripta de tres salas en fila con un cazador, un errante y un rastreador en la sala inicial."""
    salidas = {1: {"E": {"sala": 2, "costo": 100}}, 2: {"O": {"sala": 1}, "E": {"sala": 3, "costo": 100}},
               3: {"O": {"sala": 2}}}
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    contenido = [{"sala": i, "enemigos": [], "objetos": [], "trampas": []} for i in salidas]
    contenido[0]["enemigos"] = [{"instancia": "e-1", "tipo": "ent_cazador"},
                                {"instancia": "e-2", "tipo": "ent_errante"},
                                {"instancia": "e-3", "tipo": "ent_rastreador"}]
    fichas = [_ficha("ent_cazador", "cazador", 600), _ficha("ent_errante", "errante"),
              _ficha("ent_rastreador", "rastreador")]
    general = {"id": "c1", "version": "v1", "salas_total": 3, "paginas": 1, "salas_por_pagina": 50,
               "sala_inicial": 1, "sala_salida": 3, "llave_salida": "itm_llave", "presupuesto_solicitudes": 9,
               "inventario_max": 10, "jugador": {"vida_max": 100000, "ataque": 6, "defensa": 2, "velocidad": 100}}
    cliente = ClienteFalso(fichas, contenido, [{"pagina": 1, "total_paginas": 1, "salas": salas}], general)
    return ServicioPartida(cliente, ContadorSolicitudes(), asincrono=False)


class TestEnemigosNoEscribenEnLaBitacora(unittest.TestCase):
    def test_turnos_de_cazador_errante_y_rastreador_no_generan_lineas(self):  # FR-TER-021
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        ruta = str(Path(carpeta.name) / "partida.log")
        servicio = _servicio_sintetico()
        self.addCleanup(servicio.cerrar)
        servicio.iniciar_nueva("c1", 42, ruta)
        # Esperar y atacar con los tres en la sala, luego alejarse y volver a esperar para que se muevan y esperen
        acciones = [A("esperar"), A("esperar"), A("mover", "E"), A("mover", "E"), A("esperar"), A("esperar"),
                    A("esperar"), A("mover", "O"), A("esperar")]
        for accion in acciones:
            self.assertTrue(servicio.ejecutar(accion).aceptada)
        self.assertGreater(len([m for m in servicio.partida.mensajes() if "te ataca" in m]), 0)
        lineas = Path(ruta).read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lineas), 1 + len(acciones))   # el encabezado y una línea por acción del jugador
        _, registradas = LectorBitacoraPartida(ruta).leer()
        self.assertEqual(list(registradas), [a.a_dict() for a in acciones])


if __name__ == "__main__":
    unittest.main()