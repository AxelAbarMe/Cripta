"""Pruebas de la resolución del costo de cada conexión en CriptaMapa (FR-TER-001, FR-TER-002, FR-TER-016).
Se ejecuta con:  py -m unittest tests.modelo.test_cripta_mapa_costos -v
"""
import unittest

from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.excepciones import CriptaDatosInvalidosError
from cripta.modelo.cripta_mapa import CriptaMapa


def armar(costo_este=None, costo_oeste=None):
    # Sala 1 conecta con la 2 por E y la 2 con la 1 por O
    este = {"sala": 2} if costo_este is None else {"sala": 2, "costo": costo_este}
    oeste = {"sala": 1} if costo_oeste is None else {"sala": 1, "costo": costo_oeste}
    pagina = PaginaEsqueletoDTO.desde_json({"pagina": 1, "total_paginas": 1, "salas": [
        {"id": 1, "nombre": "A", "salidas": {"E": este}},
        {"id": 2, "nombre": "B", "salidas": {"O": oeste}},
    ]})
    mapa = CriptaMapa()
    mapa.agregar_pagina(pagina)
    return mapa


class TestCriptaMapaCostos(unittest.TestCase):
    def test_sin_costo_en_ningun_lado_vale_100(self):  # FR-TER-002
        mapa = armar()
        self.assertEqual(mapa.costo_de_conexion(1, "E"), 100)
        self.assertEqual(mapa.costo_de_conexion(2, "O"), 100)

    def test_costo_en_un_solo_lado_rige_en_ambos_sentidos(self):  # FR-TER-002
        mapa = armar(costo_este=250)
        self.assertEqual(mapa.costo_de_conexion(1, "E"), 250)
        self.assertEqual(mapa.costo_de_conexion(2, "O"), 250)
        mapa = armar(costo_oeste=250)
        self.assertEqual(mapa.costo_de_conexion(1, "E"), 250)
        self.assertEqual(mapa.costo_de_conexion(2, "O"), 250)

    def test_mismo_costo_en_ambos_lados_se_acepta(self):  # FR-TER-002
        mapa = armar(costo_este=40, costo_oeste=40)
        self.assertEqual(mapa.costo_de_conexion(1, "E"), 40)

    def test_costos_distintos_fallan_al_llegar_la_segunda_sala(self):  # FR-TER-002
        def pagina(numero, sala):
            return PaginaEsqueletoDTO.desde_json({"pagina": numero, "total_paginas": 2, "salas": [sala]})
        mapa = CriptaMapa()
        mapa.agregar_pagina(pagina(1, {"id": 1, "nombre": "A", "salidas": {"E": {"sala": 2, "costo": 250}}}))
        with self.assertRaises(CriptaDatosInvalidosError) as ctx:
            mapa.agregar_pagina(pagina(2, {"id": 2, "nombre": "B", "salidas": {"O": {"sala": 1, "costo": 300}}}))
        self.assertIn("construir el mapa", ctx.exception.operacion)
        self.assertIn("esqueleto de la cripta", ctx.exception.ruta)
        self.assertIn("1", ctx.exception.detalle)
        self.assertIn("2", ctx.exception.detalle)


if __name__ == "__main__":
    unittest.main()
