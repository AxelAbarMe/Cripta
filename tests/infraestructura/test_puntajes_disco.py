"""Pruebas del archivo de puntajes (§2.12): RepositorioPuntajes sobre AlmacenDiscoArchivos.

Revisan que los puntajes se guarden y se lean igual, y sobre todo que un archivo dañado o de
otro formato dé error en vez de tratarse como vacío: si se tratara como vacío, el siguiente
registro lo sobrescribiría y se perderían todos los puntajes anteriores.
El orden del ranking se prueba en tests/modelo/test_servicio_partida_guardado.py.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.infraestructura.test_puntajes_disco -v
"""
import json
import tempfile
import unittest

from cripta.excepciones import CriptaPuntajesError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.puntajes_disco import CLAVE_PUNTAJES, FORMATO_PUNTAJES, RepositorioPuntajes
from cripta.modelo.puntajes import Puntaje

ANA = Puntaje("Ana", "cripta-01", "v1", 40, 3, 900, True)
BETO = Puntaje("Beto", "cripta-01", "v1", 12, 0, 300, False)

FILA_VALIDA = {"nombre_jugador": "Ana", "cripta_id": "cripta-01", "cripta_version": "v1",
               "acciones_jugador": 40, "enemigos_derrotados": 3, "tiempo_final": 900, "victoria": True}


class TestRepositorioPuntajes(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.almacen = AlmacenDiscoArchivos(carpeta.name)
        self.repositorio = RepositorioPuntajes(self.almacen)

    def escribir_crudo(self, texto):
        self.almacen.escribir(CLAVE_PUNTAJES, texto.encode("utf-8"))

    def escribir_filas(self, filas, formato=FORMATO_PUNTAJES):
        self.escribir_crudo(json.dumps({"formato": formato, "puntajes": filas}))

    def test_sin_archivo_la_tabla_esta_vacia(self):
        self.assertEqual(len(self.repositorio.cargar()), 0)

    def test_lo_registrado_se_lee_igual_y_en_el_mismo_orden(self):
        self.repositorio.registrar(ANA)
        self.repositorio.registrar(BETO)
        # Otro repositorio sobre la misma carpeta: lo lee del archivo, no de memoria
        otro = RepositorioPuntajes(self.almacen)
        self.assertEqual(otro.cargar().registros(), (ANA, BETO))

    def test_archivo_que_no_es_json_es_error_y_no_se_sobrescribe(self):
        self.escribir_crudo("{esto no es json")
        with self.assertRaises(CriptaPuntajesError):
            self.repositorio.cargar()
        with self.assertRaises(CriptaPuntajesError):
            self.repositorio.registrar(ANA)
        # El archivo dañado sigue ahí tal cual: no se reemplazó por una tabla con solo Ana
        self.assertEqual(self.almacen.leer(CLAVE_PUNTAJES), b"{esto no es json")

    def test_otro_formato_es_error(self):
        self.escribir_filas([FILA_VALIDA], formato=1)      # un archivo de antes de agregar "victoria"
        with self.assertRaises(CriptaPuntajesError):
            self.repositorio.cargar()

    def test_sin_lista_de_puntajes_es_error(self):
        self.escribir_crudo(json.dumps({"formato": FORMATO_PUNTAJES}))
        with self.assertRaises(CriptaPuntajesError):
            self.repositorio.cargar()

    def test_una_fila_con_un_campo_invalido_es_error(self):
        filas_malas = (
            "no es un objeto",
            {**FILA_VALIDA, "nombre_jugador": 7},          # texto que no es texto
            {**FILA_VALIDA, "tiempo_final": -5},           # entero negativo
            {**FILA_VALIDA, "acciones_jugador": True},     # bool no cuenta como entero
            {**FILA_VALIDA, "victoria": "sí"},             # victoria que no es verdadero/falso
        )
        for fila in filas_malas:
            with self.subTest(fila=fila):
                self.escribir_filas([FILA_VALIDA, fila])
                with self.assertRaises(CriptaPuntajesError):
                    self.repositorio.cargar()

    def test_una_fila_sin_victoria_es_error(self):
        sin_victoria = dict(FILA_VALIDA)
        del sin_victoria["victoria"]
        self.escribir_filas([sin_victoria])
        with self.assertRaises(CriptaPuntajesError):
            self.repositorio.cargar()


if __name__ == "__main__":
    unittest.main()