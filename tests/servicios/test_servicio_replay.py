"""Pruebas de ServicioReplay (--replay, §4.11) con la cripta real de fixtures/.

Se ejecuta desde la raíz del proyecto con:
    python -m unittest tests.servicios.test_servicio_replay -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.excepciones import CriptaBitacoraError
from cripta.modelo.accion import Accion as A
from cripta.servicios.servicio_replay import ServicioReplay
from tests.servicios.test_servicio_partida import CRIPTA, armar

GUION = [A("mover", "N"), A("esperar")]


class PruebaReplay(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "partida.log"
        self.original, _, _ = armar()
        self.original.iniciar_nueva(CRIPTA, 7, str(self.ruta))
        for accion in GUION:
            self.assertTrue(self.original.ejecutar(accion).aceptada)

    def tearDown(self):
        self.original.cerrar()
        self._carpeta.cleanup()

    def _reproducir(self, ruta=None):
        servicio, _, _ = armar()
        return ServicioReplay(servicio).reproducir(str(ruta or self.ruta))

    def _reescribir(self, cambiar):
        nueva = Path(self._carpeta.name) / "modificada.log"
        nueva.write_text(cambiar(self.ruta.read_text(encoding="utf-8")), encoding="utf-8")
        return nueva

    def test_reproduce_la_misma_partida(self):
        resultado = self._reproducir()
        self.assertTrue(resultado.fiel)
        self.assertEqual((resultado.acciones_reproducidas, resultado.acciones_en_log), (2, 2))
        self.assertEqual(resultado.puntaje, self.original.partida.puntaje())
        self.assertEqual(resultado.desenlace, self.original.partida.desenlace())

    def test_muestra_un_paso_por_accion_con_sus_mensajes(self):
        resultado = self._reproducir()
        self.assertEqual(len(resultado.pasos), 2)
        self.assertTrue(resultado.pasos[0].startswith("[1] mover N -> t=100"))
        self.assertIn(resultado.pasos[0], resultado.informe())

    def test_no_modifica_el_log(self):
        antes = self.ruta.read_bytes()
        self._reproducir()
        self.assertEqual(self.ruta.read_bytes(), antes)

    def test_version_distinta_no_se_reproduce(self):
        ruta = self._reescribir(lambda texto: texto.replace('"version_catalogo": "', '"version_catalogo": "x', 1))
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertEqual(resultado.acciones_reproducidas, 0)
        self.assertIsNone(resultado.desenlace)
        self.assertIn("catálogo", resultado.problemas[0])

    def test_log_parcial_no_se_reproduce(self):
        ruta = self._reescribir(lambda texto: texto.replace("}\n", ', "parcial": true}\n', 1))
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertIn("parcial", resultado.problemas[0])

    def test_accion_que_no_se_acepta_reporta_la_linea(self):
        ruta = self._reescribir(lambda texto: texto + '{"tipo": "abrir", "direccion": "S"}\n')
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertEqual(resultado.acciones_reproducidas, 2)
        self.assertIn("línea 4", resultado.problemas[0])

    def test_accion_invalida_reporta_la_linea(self):
        ruta = self._reescribir(lambda texto: texto + '{"tipo": "volar"}\n')
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertIn("línea 4", resultado.problemas[0])

    def test_ultima_linea_incompleta_se_avisa_y_se_reproduce(self):
        ruta = self._reescribir(lambda texto: texto + '{"tipo": "mov')
        resultado = self._reproducir(ruta)
        self.assertTrue(resultado.fiel)
        self.assertEqual(len(resultado.avisos), 1)

    def test_log_inexistente(self):
        with self.assertRaises(CriptaBitacoraError):
            self._reproducir(Path(self._carpeta.name) / "nada.log")


if __name__ == "__main__":
    unittest.main()