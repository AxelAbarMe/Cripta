"""Equivalencia de alternativas medidas por niebla_rutas (FR-NIE-018)."""
import unittest
import json

from cripta.bench.cargas_bench import (
    _comparar_costos_con_mapa,
    _comparar_revelacion,
    _comparar_reversion,
    DIRECTORIO_FIXTURES_BENCH,
    _elegir_fixture_referencia,
    _seleccion_lineal,
    _siguiente_paso_costos_guardados,
)
from cripta.modelo.ruta_conocida import siguiente_paso


class TestServicioBench(unittest.TestCase):
    def test_revelacion_y_reversion_equivalentes(self):
        """FR-NIE-018, SC-NIE-004: las alternativas dejan conocimiento equivalente."""
        referencia = _elegir_fixture_referencia()
        revelacion = _comparar_revelacion(referencia, 7, 41)
        reversion = _comparar_reversion(referencia, 7, 41)
        self.assertTrue(revelacion[0])
        self.assertTrue(reversion[0])
        self.assertEqual(len(revelacion[1]), 2)
        self.assertEqual(len(revelacion[2]), 2)
        self.assertGreater(revelacion[1][0], 0)
        self.assertGreater(revelacion[2][0], 0)
        self.assertEqual(len(reversion[1]), 2)
        self.assertEqual(len(reversion[2]), 2)
        self.assertGreater(reversion[1][0], 0)
        self.assertGreater(reversion[2][0], 0)
        self.assertGreater(reversion[3], 0)

    def test_rutas_y_costos_equivalentes_sobre_fixture_mayor(self):
        """FR-NIE-018, SC-NIE-002 y SC-NIE-004: algoritmos coinciden sin fijar id."""
        referencia = _elegir_fixture_referencia()
        self.assertGreater(referencia["salas"], 0)
        self.assertGreater(referencia["salidas"], 0)
        otra_referencia = _elegir_fixture_referencia()
        self.assertTrue(referencia["consultas"])
        self.assertEqual(referencia["consultas"], otra_referencia["consultas"])
        conocimiento = referencia["conocimiento"]
        for origen, destino in referencia["consultas"]:
            with self.subTest(origen=origen, destino=destino):
                self.assertIsNotNone(siguiente_paso(conocimiento, origen, destino))
                self.assertEqual(
                    siguiente_paso(conocimiento, origen, destino),
                    _seleccion_lineal(conocimiento, origen, destino),
                )
                self.assertEqual(
                    siguiente_paso(conocimiento, origen, destino),
                    _siguiente_paso_costos_guardados(conocimiento, origen, destino),
                )
        self.assertTrue(_comparar_costos_con_mapa(referencia))
        maximo = 0
        elegidos = []
        for carpeta in DIRECTORIO_FIXTURES_BENCH.iterdir():
            ruta = carpeta / "general.json"
            if not ruta.is_file():
                continue
            with ruta.open(encoding="utf-8") as archivo:
                total = json.load(archivo)["salas_total"]
            if total > maximo:
                maximo, elegidos = total, [carpeta.name]
            elif total == maximo:
                elegidos.append(carpeta.name)
        self.assertEqual(referencia["salas"], maximo)
        self.assertEqual(referencia["id"], min(elegidos))


if __name__ == "__main__":
    unittest.main()
