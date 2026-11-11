"""Pruebas del campo rango de EnemigoDTO (FR-TER-008, FR-TER-017).
Se ejecuta con:  py -m unittest tests.dto.test_enemigo_dto -v
"""
import unittest

from cripta.dto.enemigo_dto import EnemigoDTO


def ficha(comportamiento="cazador", **extra):
    datos = {"id": "ent_x", "clase": "enemigo", "nombre": "X", "vida_max": 10, "ataque": 3,
             "defensa": 1, "velocidad": 100, "comportamiento": comportamiento}
    datos.update(extra)
    return datos


class TestEnemigoDtoRango(unittest.TestCase):
    def test_cazador_sin_rango_valido_queda_en_none(self):  # FR-TER-008
        casos = {"nulo": {"rango": None}, "ausente": {}, "no entero": {"rango": "5"},
                 "decimal": {"rango": 2.5}, "cero": {"rango": 0}, "negativo": {"rango": -3}}
        for nombre, extra in casos.items():
            with self.subTest(caso=nombre):
                self.assertIsNone(EnemigoDTO.desde_json(ficha(**extra)).rango)

    def test_cazador_con_rango_valido_lo_almacena(self):  # FR-TER-008
        self.assertEqual(EnemigoDTO.desde_json(ficha(rango=1)).rango, 1)
        self.assertEqual(EnemigoDTO.desde_json(ficha(rango=400)).rango, 400)

    def test_no_cazador_tolera_rango_nulo_o_ausente(self):  # FR-TER-017
        self.assertIsNone(EnemigoDTO.desde_json(ficha("errante")).rango)
        self.assertIsNone(EnemigoDTO.desde_json(ficha("rastreador", rango=None)).rango)


if __name__ == "__main__":
    unittest.main()
