"""Pruebas del script de auditoría de estructuras y patrones prohibidos.
Verifica la detección de errores y avisos en archivos de código fuente.
"""
import os
import tempfile
import unittest

from scripts.revisar_prohibidos import ejecutar, revisar_archivo


class TestRevisarProhibidos(unittest.TestCase):
    """Casos de prueba para las reglas de auditoría de código."""

    def test_importacion_prohibida(self):
        # Comprueba error y salida 1 ante importaciones de módulos vetados
        contenido = "import heapq\r\nfrom collections import deque\r\n"
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as archivo:
            archivo.write(contenido)
            ruta = archivo.name
        try:
            errores, avisos = revisar_archivo(ruta)
            self.assertGreaterEqual(len(errores), 2)
            self.assertEqual(len(avisos), 0)
            self.assertTrue(any("heapq" in err for err in errores))
            self.assertTrue(any("collections" in err for err in errores))
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 1)
        finally:
            os.remove(ruta)

    def test_llamada_sorted(self):
        # Comprueba error y salida 1 al invocar la función incorporada sorted
        contenido = "datos = [3, 1, 2]\r\nordenados = sorted(datos)\r\n"
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as archivo:
            archivo.write(contenido)
            ruta = archivo.name
        try:
            errores, avisos = revisar_archivo(ruta)
            self.assertEqual(len(errores), 1)
            self.assertEqual(len(avisos), 0)
            self.assertIn("sorted", errores[0])
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 1)
        finally:
            os.remove(ruta)

    def test_llamada_sort_metodo(self):
        # Comprueba error y salida 1 al llamar al método sort sobre un objeto
        contenido = "datos = [3, 1, 2]\r\ndatos.sort()\r\n"
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as archivo:
            archivo.write(contenido)
            ruta = archivo.name
        try:
            errores, avisos = revisar_archivo(ruta)
            self.assertEqual(len(errores), 1)
            self.assertEqual(len(avisos), 0)
            self.assertIn(".sort", errores[0])
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 1)
        finally:
            os.remove(ruta)

    def test_id_cripta_concreto(self):
        # Comprueba error y salida 1 ante cadenas con identificadores fijos
        contenido = "cripta_fija = 'cripta-01'\r\nentidad_fija = 'ent_rata'\r\n"
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as archivo:
            archivo.write(contenido)
            ruta = archivo.name
        try:
            errores, avisos = revisar_archivo(ruta)
            self.assertEqual(len(errores), 2)
            self.assertEqual(len(avisos), 0)
            self.assertTrue(any("cripta-01" in err for err in errores))
            self.assertTrue(any("ent_rata" in err for err in errores))
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 1)
        finally:
            os.remove(ruta)

    def test_dict_literal(self):
        # Comprueba aviso sin error y código de salida 0 para dict en carpetas del núcleo
        with tempfile.TemporaryDirectory() as temp_dir:
            carpeta = os.path.join(temp_dir, "cripta", "modelo")
            os.makedirs(carpeta, exist_ok=True)
            ruta = os.path.join(carpeta, "prueba_dict.py")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("registro = {'clave': 100}\r\n")
            errores, avisos = revisar_archivo(ruta)
            self.assertEqual(len(errores), 0)
            self.assertEqual(len(avisos), 1)
            self.assertTrue(any("dict" in av for av in avisos))
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 0)

    def test_punto_y_coma_en_comentario(self):
        # Comprueba aviso y salida 0 ante comentarios que contienen punto y coma
        contenido = "# Primer comentario normal\r\n# Segundo comentario con ; punto y coma\r\nvalor = 10\r\n"
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as archivo:
            archivo.write(contenido)
            ruta = archivo.name
        try:
            errores, avisos = revisar_archivo(ruta)
            self.assertEqual(len(errores), 0)
            self.assertEqual(len(avisos), 1)
            self.assertTrue(any(";" in av for av in avisos))
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 0)
        finally:
            os.remove(ruta)

    def test_codigo_limpio(self):
        # Comprueba que un código sin infracciones no genere errores ni avisos
        contenido = "def sumar(a, b):\r\n    return a + b\r\n"
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as archivo:
            archivo.write(contenido)
            ruta = archivo.name
        try:
            errores, avisos = revisar_archivo(ruta)
            self.assertEqual(len(errores), 0)
            self.assertEqual(len(avisos), 0)
            codigo = ejecutar([ruta])
            self.assertEqual(codigo, 0)
        finally:
            os.remove(ruta)


if __name__ == "__main__":
    unittest.main()
