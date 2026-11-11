"""Pruebas de obtener_llaves y del costo de las salidas en ClienteOffline y ClienteFalso.
Se ejecuta con:  py -m unittest tests.infraestructura.test_cliente_offline_llaves -v
"""
import json
import tempfile
import unittest
from pathlib import Path

from cripta.dto.llave_ubicacion_dto import LlaveUbicacionDTO
from cripta.infraestructura.cliente_offline import ClienteOffline
from tests.cliente_falso import ClienteFalso


def escribir(ruta: Path, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos), encoding="utf-8")


class TestClienteOfflineLlaves(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.raiz = Path(carpeta.name)
        self.cliente = ClienteOffline(str(self.raiz))

    def test_obtener_llaves_lee_llaves_json(self):  # FR-TER-018
        escribir(self.raiz / "c1" / "llaves.json", {"llaves": [
            {"id": "itm_llave_bronce", "sala": 3, "enemigo": "e-31"},
            {"id": "itm_llave_plata", "sala": 8, "enemigo": None},
            {"id": "itm_llave_oro", "sala": 9},
        ]})
        llaves = self.cliente.obtener_llaves("c1")
        self.assertIsInstance(llaves, tuple)
        self.assertEqual(llaves, (
            LlaveUbicacionDTO(id="itm_llave_bronce", sala=3, enemigo="e-31"),
            LlaveUbicacionDTO(id="itm_llave_plata", sala=8, enemigo=None),
            LlaveUbicacionDTO(id="itm_llave_oro", sala=9, enemigo=None),
        ))

    def test_costo_de_las_salidas_se_lee_desde_fixtures(self):  # FR-TER-016
        escribir(self.raiz / "c1" / "salas" / "pagina_1.json", {"pagina": 1, "total_paginas": 1, "salas": [
            {"id": 1, "nombre": "A", "salidas": {"E": {"sala": 2, "costo": 250}, "S": {"sala": 3}}},
            {"id": 2, "nombre": "B", "salidas": {"O": {"sala": 1}}},
        ]})
        sala = self.cliente.obtener_pagina_esqueleto("c1", 1).salas[0]
        self.assertEqual(sala.este.costo, 250)
        self.assertIsNone(sala.sur.costo)

    def test_cliente_falso_cuenta_la_consulta_de_llaves_como_solicitud(self):  # FR-TER-018
        esperadas = (LlaveUbicacionDTO(id="k", sala=2, enemigo=None),)
        falso = ClienteFalso(llaves=esperadas)
        self.assertEqual(falso.obtener_llaves("c1"), esperadas)
        self.assertEqual(falso.contar("obtener_llaves"), 1)
        self.assertEqual(len(falso.llamadas), 1)


if __name__ == "__main__":
    unittest.main()
