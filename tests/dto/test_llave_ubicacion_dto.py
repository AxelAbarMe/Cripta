"""Pruebas de LlaveUbicacionDTO (FR-TER-018).
Se ejecuta con:  py -m unittest tests.dto.test_llave_ubicacion_dto -v
"""
import unittest

from cripta.dto.llave_ubicacion_dto import LlaveUbicacionDTO


class TestLlaveUbicacionDto(unittest.TestCase):
    def test_con_enemigo(self):  # FR-TER-018
        dto = LlaveUbicacionDTO.desde_json({"id": "itm_llave_bronce", "sala": 4, "enemigo": "e-41"})
        self.assertEqual((dto.id, dto.sala, dto.enemigo), ("itm_llave_bronce", 4, "e-41"))

    def test_enemigo_nulo_o_ausente_implica_llave_en_el_suelo(self):  # FR-TER-018
        self.assertIsNone(LlaveUbicacionDTO.desde_json({"id": "k", "sala": 4, "enemigo": None}).enemigo)
        self.assertIsNone(LlaveUbicacionDTO.desde_json({"id": "k", "sala": 4}).enemigo)

    def test_campos_ausentes_lanzan_value_error_con_el_dato(self):  # FR-TER-018
        for datos, dato in (({"sala": 4}, "id"), ({"id": "k"}, "sala")):
            with self.subTest(falta=dato):
                with self.assertRaises(ValueError) as ctx:
                    LlaveUbicacionDTO.desde_json(datos)
                self.assertIn(dato, str(ctx.exception))

    def test_id_vacio_lanza_value_error(self):  # FR-TER-018
        with self.assertRaises(ValueError) as ctx:
            LlaveUbicacionDTO.desde_json({"id": "", "sala": 4})
        self.assertIn("id", str(ctx.exception))

    def test_sala_menor_que_uno_lanza_value_error(self):  # FR-TER-018
        with self.assertRaises(ValueError) as ctx:
            LlaveUbicacionDTO.desde_json({"id": "k", "sala": 0})
        self.assertIn("sala", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
