"""Decisiones del cazador en su turno (T027), sobre criptas sintéticas armadas dentro de la prueba.
Los ayudantes de abajo (grafo, armar_partida...) los reutilizan las otras pruebas del cazador.
Se ejecuta desde la raíz del proyecto con:  py -m unittest tests.modelo.test_cazador_decisiones -v
"""
import unittest

from cripta.constantes import direccion_opuesta
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from tests.cliente_falso import ClienteFalso

RANGO_SABUESO = 600       # rango real del sabueso óseo según el plan
RANGO_ESPECTRO = 2400     # rango real del espectro acechador según el plan


def grafo(conexiones):
    """Convierte [(origen, direccion, destino, costo), ...] en las salidas de ambos lados de cada conexión."""
    salidas = {}
    for origen, direccion, destino, costo in conexiones:
        salidas.setdefault(origen, {})[direccion] = {"sala": destino, "costo": costo}
        salidas.setdefault(destino, {})[direccion_opuesta(direccion)] = {"sala": origen, "costo": costo}
    return salidas


def construir_mapa(conexiones):
    """CriptaMapa sin partida, para probar la búsqueda de rutas sola."""
    salidas = grafo(conexiones)
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    mapa = CriptaMapa()
    mapa.agregar_pagina(PaginaEsqueletoDTO.desde_json({"pagina": 1, "total_paginas": 1, "salas": salas}))
    mapa.sincronizar_puertas()
    return mapa


def _id_ficha(rango):
    return "ent_cz_sin_rango" if rango is None else f"ent_cz_{rango}"


def _ficha_cazador(rango, velocidad):
    ficha = {"id": _id_ficha(rango), "clase": "enemigo", "nombre": "Cazador", "vida_max": 1000, "ataque": 10,
             "defensa": 0, "velocidad": velocidad, "comportamiento": "cazador"}
    if rango is not None:
        ficha["rango"] = rango
    return ficha


def armar_partida(salidas, cazadores, velocidad_jugador=1000, velocidad_cazador=100, semilla=3):
    """La sala 1 es la inicial. `cazadores` es [(sala, instancia, rango), ...] y rango puede ser None.
    El jugador es veloz para poder recorrer varias salidas antes del primer turno del cazador (t=100)."""
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    contenido = [{"sala": i, "enemigos": [], "objetos": [], "trampas": []} for i in salidas]
    fichas = []
    for sala, instancia, rango in cazadores:
        for entrada in contenido:
            if entrada["sala"] == sala:
                entrada["enemigos"].append({"instancia": instancia, "tipo": _id_ficha(rango)})
        if _id_ficha(rango) not in [f["id"] for f in fichas]:
            fichas.append(_ficha_cazador(rango, velocidad_cazador))
    general = {"id": "c1", "version": "v1", "salas_total": len(salas), "paginas": 1, "salas_por_pagina": 50,
               "sala_inicial": 1, "sala_salida": max(salidas), "llave_salida": "itm_llave",
               "presupuesto_solicitudes": 9, "inventario_max": 10,
               "jugador": {"vida_max": 100000, "ataque": 6, "defensa": 2, "velocidad": velocidad_jugador}}
    cliente = ClienteFalso(fichas, contenido, [{"pagina": 1, "total_paginas": 1, "salas": salas}], general)
    datos = cliente.obtener_general("c1")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "c1", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(datos.paginas)
    partida = Partida(datos, mapa, catalogo, precarga, semilla)
    partida.iniciar()
    return partida, mapa


def tiempo(partida):
    return partida.vista().tiempo


def recorrer(partida, direcciones):
    for direccion in direcciones:
        if not partida.ejecutar_accion(A("mover", direccion)).aceptada:
            raise AssertionError(f"El jugador no pudo moverse hacia {direccion}")


def avanzar_hasta(partida, instante):
    """El jugador espera hasta que el reloj llega a `instante`. Un enemigo con turno en ese instante ya actuó."""
    for _ in range(2000):
        if tiempo(partida) >= instante or partida.desenlace() != "en_curso":
            return
        partida.ejecutar_accion(A("esperar"))
    raise AssertionError("El reloj no llegó al instante pedido")


def cazador_de(mapa, instancia):
    for sala in mapa.todas_las_salas():
        for enemigo in list(sala.enemigos_activos) + list(sala.enemigos_dormidos):
            if enemigo.instancia_id == instancia:
                return enemigo
    raise AssertionError(f"No existe el enemigo {instancia}")


class TestDecisionesDelCazador(unittest.TestCase):
    PASILLO = grafo([(1, "E", 2, 250)])

    def test_en_la_misma_sala_ataca_con_costo_100(self):  # FR-TER-009
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertTrue(any("te ataca" in m for m in partida.mensajes()))
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_con_ruta_abierta_y_distancia_dentro_del_rango_se_mueve_con_el_costo_de_la_salida(self):  # FR-TER-012
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 250)

    def test_sin_ruta_abierta_espera_con_costo_100(self):  # FR-TER-011
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_con_distancia_mayor_al_rango_espera_con_costo_100(self):  # FR-TER-011
        largo = grafo([(1, "E", 2, 490), (2, "E", 3, 490)])   # distancia 980 contra rango 600
        partida, mapa = armar_partida(largo, [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E", "E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_el_mismo_mapa_con_rango_2400_si_persigue(self):  # FR-TER-011, FR-TER-012
        largo = grafo([(1, "E", 2, 490), (2, "E", 3, 490)])
        partida, mapa = armar_partida(largo, [(1, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E", "E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 490)

    def test_no_le_afecta_la_niebla_atraviesa_salas_que_el_jugador_no_visito(self):  # FR-TER-014
        conexiones = [(1, "E", 2, 400), (1, "N", 3, 50), (3, "E", 4, 50), (4, "S", 2, 50)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 3)
        self.assertIsNone(mapa.obtener(3).rastro_ultima_visita)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 50)


class TestCazadorSinRango(unittest.TestCase):
    PASILLO = grafo([(1, "E", 2, 100)])

    def test_si_comparte_sala_ataca(self):  # FR-TER-008
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", None)])
        avanzar_hasta(partida, 100)
        self.assertTrue(any("te ataca" in m for m in partida.mensajes()))
        self.assertEqual(cazador_de(mapa, "e-1").tiempo_siguiente, 200)

    def test_si_no_comparte_sala_espera_con_costo_100_aunque_haya_ruta_cercana(self):  # FR-TER-008
        partida, mapa = armar_partida(self.PASILLO, [(1, "e-1", None)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_al_activarse_agrega_a_la_bitacora_un_aviso_con_el_id_de_la_ficha(self):  # FR-TER-008
        partida, _ = armar_partida(self.PASILLO, [(1, "e-1", None)])
        self.assertTrue(any(_id_ficha(None) in m for m in partida.mensajes()))

    def test_un_cazador_con_rango_valido_no_agrega_ese_aviso(self):  # FR-TER-008
        partida, _ = armar_partida(self.PASILLO, [(1, "e-1", RANGO_SABUESO)])
        self.assertFalse(any(_id_ficha(RANGO_SABUESO) in m for m in partida.mensajes()))


if __name__ == "__main__":
    unittest.main()
