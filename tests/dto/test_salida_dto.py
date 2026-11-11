"""Pruebas del campo costo de SalidaDTO (FR-TER-001, FR-TER-016).
Se ejecuta con:  py -m unittest tests.dto.test_salida_dto -v
"""
import unittest

from cripta.dto.sala_dto import SalaDTO
from cripta.dto.salida_dto import SalidaDTO


class TestSalidaDtoCosto(unittest.TestCase):
    def test_sin_costo_queda_en_none(self):  # FR-TER-001
        self.assertIsNone(SalidaDTO.desde_json({"sala": 2}).costo)

    def test_costo_nulo_queda_en_none(self):  # FR-TER-001
        self.assertIsNone(SalidaDTO.desde_json({"sala": 2, "costo": None}).costo)

    def test_costo_valido_se_conserva(self):  # FR-TER-001
        self.assertEqual(SalidaDTO.desde_json({"sala": 2, "costo": 1}).costo, 1)
        self.assertEqual(SalidaDTO.desde_json({"sala": 2, "costo": 250}).costo, 250)

    def test_costo_menor_que_uno_lanza_value_error(self):  # FR-TER-016
        for invalido in (0, -5):
            with self.subTest(costo=invalido):
                with self.assertRaises(ValueError) as ctx:
                    SalidaDTO.desde_json({"sala": 7, "costo": invalido})
                self.assertIn(str(invalido), str(ctx.exception))

    def test_costo_no_entero_lanza_value_error(self):  # FR-TER-016
        for invalido in ("100", 2.5, True):
            with self.subTest(costo=invalido):
                with self.assertRaises(ValueError):
                    SalidaDTO.desde_json({"sala": 7, "costo": invalido})

    def test_mensaje_de_sala_incluye_sala_y_direccion(self):  # FR-TER-016
        datos = {"id": 12, "nombre": "Sala 12", "salidas": {"E": {"sala": 13, "costo": 0}}}
        with self.assertRaises(ValueError) as ctx:
            SalaDTO.desde_json(datos)
        mensaje = str(ctx.exception)
        self.assertIn("12", mensaje)
        self.assertIn("E", mensaje)


if __name__ == "__main__":
    unittest.main()
