"""Pruebas de la caché versionada de llaves (FR-TER-019).
Esqueleto, contenido y fichas de catálogo con versión distinta ya están cubiertos en
tests/infraestructura/test_cache_disco.py (test_esqueleto_y_contenido_se_guardan_por_version_de_la_cripta
y test_otra_version_del_catalogo_no_ve_lo_guardado), aquí solo se prueban las llaves.
Se ejecuta con:  py -m unittest tests.infraestructura.test_cache_llaves -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.dto.llave_ubicacion_dto import LlaveUbicacionDTO
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco

LLAVES = (LlaveUbicacionDTO(id="itm_llave_bronce", sala=3, enemigo="e-31"),
          LlaveUbicacionDTO(id="itm_llave_plata", sala=8, enemigo=None))


class TestCacheLlaves(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)
        self.disco = CacheDisco(AlmacenDiscoArchivos(self.carpeta))

    def test_llaves_con_la_version_correcta_se_recuperan(self):  # FR-TER-019
        self.disco.guardar_llaves("cripta-x", "v1", LLAVES)
        self.assertEqual(self.disco.leer_llaves("cripta-x", "v1"), LLAVES)

    def test_llaves_sin_guardar_se_tratan_como_ausentes(self):  # FR-TER-019
        self.assertIsNone(self.disco.leer_llaves("cripta-x", "v1"))

    def test_otra_version_de_cripta_se_trata_como_ausente_sin_borrar_archivos(self):  # FR-TER-019
        self.disco.guardar_llaves("cripta-x", "v1", LLAVES)
        antes = sorted(p.name for p in self.carpeta.iterdir())
        self.assertIsNone(self.disco.leer_llaves("cripta-x", "v2"))
        self.assertEqual(sorted(p.name for p in self.carpeta.iterdir()), antes)
        self.assertEqual(self.disco.leer_llaves("cripta-x", "v1"), LLAVES)

    def test_archivo_danado_cuenta_como_ausente(self):  # FR-TER-019
        self.disco.guardar_llaves("cripta-x", "v1", LLAVES)
        for archivo in self.carpeta.iterdir():
            archivo.write_text("{esto ya no es json", encoding="utf-8")
        self.assertIsNone(self.disco.leer_llaves("cripta-x", "v1"))


if __name__ == "__main__":
    unittest.main()
