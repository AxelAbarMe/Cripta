"""Pruebas de la caché persistente en disco (§4.4): CacheDisco sobre AlmacenDiscoArchivos.

Revisan que lo guardado se lea igual, que la versión forme parte de la clave (una versión
nueva no ve lo de la vieja) y que un archivo dañado cuente como "no está" en vez de lanzar
una excepción. El último test revisa que ServicioCatalogo pida una ficha dañada en el mismo
lote que las que faltan, y que la deje reparada en disco.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.infraestructura.test_cache_disco -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.dto.contenido_sala_dto import ContenidoSalaDTO
from cripta.dto.entidad_dto import entidad_desde_json
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from tests.cliente_falso import ClienteFalso
from tests.cripta_artificial import construir

DATOS = construir(filas=2, columnas=2)


def ficha(ficha_id):
    # Busca la ficha en la lista de la cripta artificial y la convierte en DTO
    for ficha_json in DATOS["fichas"]:
        if ficha_json["id"] == ficha_id:
            return entidad_desde_json(ficha_json)
    return None


class TestCacheDisco(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)
        self.disco = CacheDisco(AlmacenDiscoArchivos(self.carpeta))

    def danar(self, parte_del_nombre):
        # Sobrescribe con texto que no es JSON el archivo cuyo nombre contiene "parte_del_nombre"
        for archivo in self.carpeta.iterdir():
            if parte_del_nombre in archivo.name:
                archivo.write_text("{esto ya no es json", encoding="utf-8")

    def test_ficha_guardada_se_lee_igual(self):
        self.disco.guardar_ficha("cat-1", ficha("itm_daga"))
        self.assertEqual(self.disco.leer_ficha("cat-1", "itm_daga"), ficha("itm_daga"))
        self.assertTrue(self.disco.existe_ficha("cat-1", "itm_daga"))

    def test_ficha_que_no_esta(self):
        self.assertIsNone(self.disco.leer_ficha("cat-1", "itm_pocion"))
        self.assertFalse(self.disco.existe_ficha("cat-1", "itm_pocion"))

    def test_otra_version_del_catalogo_no_ve_lo_guardado(self):
        self.disco.guardar_ficha("cat-1", ficha("itm_daga"))
        self.assertFalse(self.disco.existe_ficha("cat-2", "itm_daga"))

    def test_ficha_danada_cuenta_como_que_no_esta(self):
        self.disco.guardar_ficha("cat-1", ficha("itm_antorcha"))
        self.danar("itm_antorcha")
        self.assertIsNone(self.disco.leer_ficha("cat-1", "itm_antorcha"))   # sin lanzar excepción
        self.assertFalse(self.disco.existe_ficha("cat-1", "itm_antorcha"))

    def test_esqueleto_y_contenido_se_guardan_por_version_de_la_cripta(self):
        pagina = PaginaEsqueletoDTO.desde_json(DATOS["paginas"][0])
        contenido = ContenidoSalaDTO.desde_json(DATOS["contenido"][0])
        self.disco.guardar_pagina("cripta-x", "v1", pagina)
        self.disco.guardar_contenido_sala("cripta-x", "v1", contenido)
        self.assertEqual(self.disco.leer_pagina("cripta-x", "v1", pagina.pagina), pagina)
        self.assertEqual(self.disco.leer_contenido_sala("cripta-x", "v1", contenido.id), contenido)
        # Con otra versión de la cripta no aparece nada
        self.assertIsNone(self.disco.leer_pagina("cripta-x", "v2", pagina.pagina))
        self.assertFalse(self.disco.existe_contenido("cripta-x", "v2", contenido.id))

    def test_contenido_danado_cuenta_como_que_no_esta(self):
        contenido = ContenidoSalaDTO.desde_json(DATOS["contenido"][0])
        self.disco.guardar_contenido_sala("cripta-x", "v1", contenido)
        self.danar("contenido")
        self.assertFalse(self.disco.existe_contenido("cripta-x", "v1", contenido.id))

    def test_el_catalogo_pide_la_ficha_danada_junto_con_las_que_faltan_y_la_repara(self):
        # En disco: la daga sana y la antorcha dañada. La poción no está.
        self.disco.guardar_ficha("cat-1", ficha("itm_daga"))
        self.disco.guardar_ficha("cat-1", ficha("itm_antorcha"))
        self.danar("itm_antorcha")
        cliente = ClienteFalso(DATOS["fichas"], DATOS["contenido"], DATOS["paginas"], DATOS["general"],
                               version_catalogo="cat-1")
        catalogo = ServicioCatalogo(cliente, cache_disco=self.disco)

        catalogo.solicitar(["itm_daga", "itm_antorcha", "itm_pocion"])
        for ficha_id in ("itm_pocion", "itm_antorcha", "itm_daga"):
            self.assertEqual(catalogo.obtener(ficha_id), ficha(ficha_id))

        # Un solo lote a la red con la poción y la antorcha; la daga salió del disco
        lotes = [ids for metodo, ids in cliente.llamadas if metodo == "obtener_catalogo"]
        self.assertEqual(len(lotes), 1)
        self.assertEqual(len(lotes[0]), 2)
        self.assertIn("itm_pocion", lotes[0])
        self.assertIn("itm_antorcha", lotes[0])
        # La antorcha quedó guardada de nuevo, sana
        self.assertTrue(self.disco.existe_ficha("cat-1", "itm_antorcha"))


if __name__ == "__main__":
    unittest.main()