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


def pagina_de(numero, total, ids):
    salas = [{"id": i, "nombre": f"S{i}", "salidas": {}} for i in ids]
    return PaginaEsqueletoDTO.desde_json({"pagina": numero, "total_paginas": total, "salas": salas})


class TestCriptaMapaObtener(unittest.TestCase):
    def test_sala_existente_devuelve_su_sala(self):  # FR-TER-001
        mapa = armar()
        self.assertEqual(mapa.obtener(1).id, 1)
        self.assertEqual(mapa.obtener(2).id, 2)

    def test_sala_inexistente_devuelve_none(self):  # FR-TER-001
        mapa = armar()
        self.assertIsNone(mapa.obtener(3))

    def test_ids_fuera_de_rango_devuelven_none(self):  # FR-TER-001
        mapa = armar()
        self.assertIsNone(mapa.obtener(0))
        self.assertIsNone(mapa.obtener(-1))
        self.assertIsNone(mapa.obtener(10 ** 6))
        self.assertIsNone(CriptaMapa().obtener(1))

    def test_paginas_en_desorden_con_huecos(self):  # FR-TER-001
        mapa = CriptaMapa()
        mapa.agregar_pagina(pagina_de(2, 3, [30, 12]))
        mapa.agregar_pagina(pagina_de(1, 3, [5, 20]))
        mapa.agregar_pagina(pagina_de(3, 3, [1, 44]))
        for sala_id in (1, 5, 12, 20, 30, 44):
            self.assertEqual(mapa.obtener(sala_id).id, sala_id)
        for sala_id in (0, 2, 13, 29, 43, 45):
            self.assertIsNone(mapa.obtener(sala_id))
        self.assertEqual(len(mapa), 6)
        self.assertEqual([s.id for s in mapa.todas_las_salas()], [1, 5, 12, 20, 30, 44])

    def test_pagina_repetida_se_ignora(self):  # FR-TER-001
        mapa = CriptaMapa()
        mapa.agregar_pagina(pagina_de(1, 1, [3, 4]))
        primera = mapa.obtener(3)
        mapa.agregar_pagina(pagina_de(1, 1, [3, 4]))
        self.assertIs(mapa.obtener(3), primera)
        self.assertEqual(len(mapa), 2)


if __name__ == "__main__":
    unittest.main()
