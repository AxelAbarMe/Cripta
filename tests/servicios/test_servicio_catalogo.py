"""Pruebas de ServicioCatalogo (§4.3 y §4.4): estadísticas, lotes y desalojo LRU con fichas en uso.

El caso con disco (ficha dañada que viaja en el mismo lote) está en
tests/infraestructura/test_cache_disco.py; el desalojo durante una partida real, en
tests/modelo/test_servicio_partida.py. Aquí se prueba el catálogo solo, con un cliente falso.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.servicios.test_servicio_catalogo -v
"""
import unittest

from cripta.servicios.servicio_catalogo import ServicioCatalogo
from tests.cliente_falso import ClienteFalso
from tests.cripta_artificial import construir

DATOS = construir(filas=2, columnas=2)

# Fichas sin "suelta": cada obtener() trae exactamente una ficha y no deja pendientes
SIN_SUELTA = ("ent_murcielago", "itm_daga", "itm_antorcha", "trp_dardos")


def armar(tope=100, en_uso=None):
    cliente = ClienteFalso(DATOS["fichas"], DATOS["contenido"], DATOS["paginas"], DATOS["general"])
    if en_uso is None:
        catalogo = ServicioCatalogo(cliente, tamano_maximo=tope)
    else:
        # lambda: el catálogo consulta la lista cada vez que va a desalojar, así ve los cambios
        catalogo = ServicioCatalogo(cliente, tamano_maximo=tope, fichas_en_uso=lambda: tuple(en_uso))
    return catalogo, cliente


class TestEstadisticasYLotes(unittest.TestCase):
    def test_uno_por_uno_y_juntos_cuentan_lo_mismo(self):
        # Una sala con dos ratas y una daga: la rata aparece dos veces
        ids_sala = ["ent_rata", "ent_rata", "itm_daga"]
        uno_por_uno, _ = armar()
        for ficha_id in ids_sala:
            uno_por_uno.obtener(ficha_id)
        juntos, _ = armar()
        juntos.obtener_varias(ids_sala)
        for catalogo in (uno_por_uno, juntos):
            self.assertEqual((catalogo.estadisticas.aciertos, catalogo.estadisticas.fallos), (1, 2))

    def test_obtener_varias_respeta_el_orden_y_las_repeticiones(self):
        catalogo, _ = armar()
        fichas = catalogo.obtener_varias(["itm_daga", "ent_rata", "itm_daga"])
        self.assertEqual([f.id for f in fichas], ["itm_daga", "ent_rata", "itm_daga"])

    def test_lo_que_ya_esta_en_memoria_no_se_vuelve_a_pedir(self):
        catalogo, cliente = armar()
        catalogo.obtener_varias(["ent_murcielago", "itm_daga"])
        lotes_antes = cliente.contar("obtener_catalogo")
        catalogo.obtener_varias(["ent_murcielago", "itm_daga"])
        self.assertEqual(cliente.contar("obtener_catalogo"), lotes_antes)
        self.assertEqual(catalogo.estadisticas.aciertos, 2)

    def test_los_ids_descubiertos_viajan_juntos_en_un_lote(self):
        catalogo, cliente = armar()
        catalogo.solicitar(["itm_daga", "itm_antorcha", "trp_dardos"])
        catalogo.obtener("itm_daga")          # hace falta ya: arrastra a las otras dos en el mismo lote
        catalogo.obtener("itm_antorcha")
        catalogo.obtener("trp_dardos")
        self.assertEqual(cliente.contar("obtener_catalogo"), 1)
        self.assertFalse(catalogo.hay_pendientes())

    def test_tope_menor_a_uno_se_rechaza(self):
        with self.assertRaises(ValueError):
            armar(tope=0)


class TestDesalojo(unittest.TestCase):
    def pedir(self, catalogo, ids):
        for ficha_id in ids:
            catalogo.obtener(ficha_id)

    def test_sin_fichas_en_uso_sale_la_menos_usada(self):
        catalogo, _ = armar(tope=2, en_uso=[])
        self.pedir(catalogo, SIN_SUELTA[:3])          # murciélago, daga, antorcha
        self.assertEqual(catalogo.ids_en_memoria(), ("itm_antorcha", "itm_daga"))
        self.assertEqual(catalogo.estadisticas.desalojadas, 1)

    def test_usar_una_ficha_la_salva_del_desalojo(self):
        catalogo, _ = armar(tope=2, en_uso=[])
        self.pedir(catalogo, ("ent_murcielago", "itm_daga", "ent_murcielago", "itm_antorcha"))
        # El murciélago se volvió a usar después de la daga: la menos usada ahora es la daga
        self.assertEqual(catalogo.ids_en_memoria(), ("itm_antorcha", "ent_murcielago"))

    def test_una_ficha_en_uso_no_se_desaloja(self):
        catalogo, _ = armar(tope=2, en_uso=["ent_murcielago"])
        self.pedir(catalogo, SIN_SUELTA[:3])
        # El murciélago era la menos usada, pero está en uso: sale la daga en su lugar
        self.assertEqual(catalogo.ids_en_memoria(), ("itm_antorcha", "ent_murcielago"))

    def test_si_todas_estan_en_uso_se_pasa_del_tope(self):
        catalogo, _ = armar(tope=2, en_uso=list(SIN_SUELTA[:3]))
        self.pedir(catalogo, SIN_SUELTA[:3])
        self.assertEqual(len(catalogo), 3)
        self.assertEqual(catalogo.estadisticas.desalojadas, 0)

    def test_cuando_deja_de_estar_en_uso_vuelve_a_poder_salir(self):
        en_uso = ["ent_murcielago"]
        catalogo, _ = armar(tope=2, en_uso=en_uso)
        self.pedir(catalogo, SIN_SUELTA[:3])
        en_uso.clear()                                  # murió el murciélago
        catalogo.obtener("trp_dardos")
        self.assertNotIn("ent_murcielago", catalogo.ids_en_memoria())
        self.assertEqual(len(catalogo), 2)

    def test_la_marca_de_en_uso_no_queda_pegada(self):
        # La marca es temporal: se pone para elegir la víctima y se quita enseguida
        en_uso = ["ent_murcielago"]
        catalogo, _ = armar(tope=3, en_uso=en_uso)
        self.pedir(catalogo, SIN_SUELTA)               # 4 fichas con tope 3: un desalojo con la marca puesta
        for entrada in catalogo._indice.elementos():
            self.assertFalse(entrada.en_uso, entrada.id)


if __name__ == "__main__":
    unittest.main()