"""Prueba de humo de las cargas de medición: cada carga de CARGAS corre a escala mínima.

Revisa que devuelva una lista no vacía de Resultado sin lanzar excepciones (FR-TER-020).

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.bench.test_cargas_bench -v
"""
import inspect
import unittest

from cripta.bench.cargas_bench import CARGAS, Resultado

ESCALA_MINIMA = 0.01


class TestCargasBench(unittest.TestCase):
    def test_cada_carga_devuelve_resultados(self):
        """FR-TER-020: ninguna carga registrada lanza excepciones ni devuelve vacío."""
        for nombre, funcion in CARGAS:
            with self.subTest(carga=nombre):
                parametros = inspect.signature(funcion).parameters
                argumentos = {"escala": ESCALA_MINIMA}
                if "corridas" in parametros:
                    argumentos["corridas"] = 1
                resultados = funcion(**argumentos)
                self.assertIsInstance(resultados, list)
                self.assertGreater(len(resultados), 0)
                for resultado in resultados:
                    self.assertIsInstance(resultado, Resultado)


if __name__ == "__main__":
    unittest.main()
