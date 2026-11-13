"""Aceptación de US2 y US3 (cazador): ataque, ruta de costo mínimo, desempate, espera, puertas y activación.
Usa criptas sintéticas en memoria (sin datos de ninguna cripta real). Se ejecuta con:
    py -m unittest tests.aceptacion.test_cazador_persecucion -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.constantes import direccion_opuesta
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.modelo.accion import Accion as A
from cripta.modelo.efectos import EfectoCierrePuerta
from cripta.servicios.servicio_partida import ServicioPartida
from tests.cliente_falso import ClienteFalso
from tests.cripta_cazadores import (
    RANGO_ESPECTRO, RANGO_SABUESO, id_ficha, ficha_cazador, armar_partida, avanzar_hasta, cazador_de, grafo,
    recorrer,
)


def indices_de_ataque(partida, instancia):
    return [i for i, m in enumerate(partida.mensajes()) if f"[{instancia}]" in m and "te ataca" in m]


class TestAtaqueYRutaDeCostoMinimo(unittest.TestCase):
    def test_cazador_en_la_sala_del_jugador_ataca_con_costo_100(self):  # US2-1, FR-TER-009
        partida, mapa = armar_partida(grafo([(1, "E", 2, 250)]), [(1, "e-1", RANGO_SABUESO)])
        avanzar_hasta(partida, 100)
        self.assertEqual(len(indices_de_ataque(partida, "e-1")), 1)
        self.assertEqual(cazador_de(mapa, "e-1").tiempo_siguiente, 200)

    def test_elige_la_ruta_de_150_y_no_la_directa_de_300(self):  # US2-2, Apéndice B caso 3, FR-TER-010, FR-TER-012
        conexiones = [(1, "E", 2, 300), (1, "N", 3, 50), (3, "E", 4, 50), (4, "S", 2, 50)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 3)                # primer paso de la ruta de 150
        self.assertEqual(cazador.tiempo_siguiente, 100 + 50)    # y su costo es el de esa salida

    def test_el_costo_de_moverse_es_el_de_la_salida_atravesada(self):  # US2-3, FR-TER-012
        partida, mapa = armar_partida(grafo([(1, "E", 2, 330)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 330)

    def test_con_distancia_igual_al_rango_se_mueve(self):  # FR-TER-011, FR-TER-012
        partida, mapa = armar_partida(grafo([(1, "E", 2, 300), (2, "E", 3, 300)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E", "E"])      # distancia 600 y rango 600: la espera exige distancia mayor
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 300)

    def test_en_la_misma_sala_ataca_aunque_el_rango_sea_el_minimo_y_la_sala_este_aislada(self):  # FR-TER-009
        partida, mapa = armar_partida(grafo([(1, "E", 2, 490)]), [(1, "e-1", 1)])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 100)
        self.assertEqual(len(indices_de_ataque(partida, "e-1")), 1)
        self.assertEqual(cazador_de(mapa, "e-1").tiempo_siguiente, 200)


class TestDesempateYEspera(unittest.TestCase):
    def test_dos_vecinas_con_el_mismo_costo_minimo_va_a_la_de_menor_id(self):  # US3-1, Apéndice B caso 4, FR-TER-013
        # El jugador pasa por la 3 hasta la 4. Desde la 1 ambas rutas cuestan 100 y la de menor id es la 2 (este)
        conexiones = [(1, "N", 3, 40), (3, "E", 4, 60), (1, "E", 2, 60), (2, "N", 4, 40)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["N", "E"])
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 100 + 60)

    def test_sin_ruta_abierta_espera_con_costo_100(self):  # US3-2, Apéndice B caso 1, FR-TER-011
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_ruta_abierta_pero_distancia_mayor_al_rango_espera_con_costo_100(self):  # US3-3, Apéndice B caso 2, FR-TER-011
        partida, mapa = armar_partida(grafo([(1, "E", 2, 490), (2, "E", 3, 490)]), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E", "E"])      # distancia 980 contra rango 600
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 1)
        self.assertEqual(cazador.tiempo_siguiente, 200)

    def test_una_puerta_de_la_ruta_se_cierra_entre_dos_turnos_y_decide_como_desde_cero(self):  # US3-4, Apéndice B caso 5, FR-TER-015
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100), (2, "E", 3, 100)]), [(1, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E", "E"])
        EfectoCierrePuerta(partida._reloj, mapa, 2, "E", 130, partida._avisar_cierre_de_puerta).programar_cierre()
        avanzar_hasta(partida, 100)       # t=100 la puerta sigue abierta y el cazador avanza a la sala 2
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 2)
        avanzar_hasta(partida, 200)       # t=150 la puerta se cierra y en t=200 ya no hay ruta
        self.assertFalse(mapa.puerta_transitable(2, "E"))
        self.assertEqual(cazador.sala_actual, 2)
        self.assertEqual(cazador.tiempo_siguiente, 300)

    def test_el_cazador_no_abre_puertas_cerradas(self):  # US3-5, FR-TER-014
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E"])
        mapa.cerrar_puerta(1, "E")
        avanzar_hasta(partida, 600)
        self.assertEqual(cazador_de(mapa, "e-1").sala_actual, 1)
        self.assertFalse(mapa.puerta_transitable(1, "E"))

    def test_la_niebla_no_le_afecta_cruza_salas_que_el_jugador_nunca_visito(self):  # US3-5, FR-TER-014
        conexiones = [(1, "E", 2, 300), (1, "N", 3, 50), (3, "E", 4, 50), (4, "S", 2, 50)]
        partida, mapa = armar_partida(grafo(conexiones), [(1, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 190)       # el cazador ya cruzó la 3 y está en la 4, y su turno de t=200 no ocurrió
        self.assertIsNone(mapa.obtener(3).rastro_ultima_visita)
        self.assertIsNone(mapa.obtener(4).rastro_ultima_visita)
        self.assertEqual(cazador_de(mapa, "e-1").sala_actual, 4)


class TestActivacionYMuerte(unittest.TestCase):
    def test_activaciones_simultaneas_programan_sus_primeros_turnos_por_id_de_instancia(self):  # FR-TER-022
        # e-2 se declara antes que e-1 en el contenido, e-1 debe actuar primero
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]),
                                      [(2, "e-2", RANGO_SABUESO), (2, "e-1", RANGO_SABUESO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 100)
        primero, segundo = indices_de_ataque(partida, "e-1"), indices_de_ataque(partida, "e-2")
        self.assertEqual((len(primero), len(segundo)), (1, 1))
        self.assertLess(primero[0], segundo[0])

    def test_cazador_en_sala_no_visitada_permanece_dormido(self):  # supuesto de activación, P1 §2.4
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100), (2, "E", 3, 100)]), [(3, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 800)
        for sala in mapa.todas_las_salas():
            self.assertEqual(sala.enemigos_activos, [], f"sala {sala.id}")   # la 3 sigue sin cargar ni activar a nadie

    def test_cazador_dormido_se_activa_cuando_el_jugador_entra_a_su_sala(self):  # supuesto de activación, P1 §2.4
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100), (2, "E", 3, 100)]), [(3, "e-1", RANGO_ESPECTRO)])
        recorrer(partida, ["E", "E"])
        self.assertTrue(cazador_de(mapa, "e-1").activo)

    def test_cazador_que_muere_en_combate_no_actua_en_su_turno_programado(self):  # FR-TER-015
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_SABUESO)])
        cazador = cazador_de(mapa, "e-1")
        cazador.vida = 1
        partida.ejecutar_accion(A("atacar", "e-1"))
        self.assertFalse(cazador.esta_vivo())
        avanzar_hasta(partida, 300)
        self.assertEqual(indices_de_ataque(partida, "e-1"), [])

    def test_cazador_con_vida_cero_y_turno_pendiente_no_produce_ninguna_accion(self):  # FR-TER-015
        partida, mapa = armar_partida(grafo([(1, "E", 2, 100)]), [(1, "e-1", RANGO_SABUESO)])
        cazador = cazador_de(mapa, "e-1")
        cazador.vida = 0                  # muerto sin cancelar su evento: el turno debe ignorarlo
        avanzar_hasta(partida, 300)
        self.assertEqual(indices_de_ataque(partida, "e-1"), [])
        self.assertEqual(cazador.tiempo_siguiente, 100)


LLAVE = "itm_llave_atajo"
PERGAMINO = "itm_pergamino"
FICHA_LLAVE = {"id": LLAVE, "clase": "llave", "nombre": "Llave del atajo", "peso": 1, "valor": 1, "abre": 1}
FICHA_PERGAMINO = {"id": PERGAMINO, "clase": "pergamino_retroceso", "nombre": "Pergamino", "peso": 1, "valor": 1}


def cerrar_con_llave(salidas, origen, direccion, llave):
    """Marca la salida y su lado opuesto como cerrados con esa llave."""
    destino = salidas[origen][direccion]["sala"]
    for sala, salida in ((origen, direccion), (destino, direccion_opuesta(direccion))):
        salidas[sala][salida].update({"cerrada": True, "llave": llave})
    return salidas


def armar_servicio(salidas, cazadores, objetos=None, fichas_extra=()):
    """ServicioPartida sobre una cripta sintética. `objetos` es {sala: [ids de ficha]}. La sala 1 es la inicial."""
    objetos = objetos or {}
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    contenido = [{"sala": i, "enemigos": [], "objetos": list(objetos.get(i, [])), "trampas": []} for i in salidas]
    fichas = list(fichas_extra)
    for sala, instancia, rango in cazadores:
        for entrada in contenido:
            if entrada["sala"] == sala:
                entrada["enemigos"].append({"instancia": instancia, "tipo": id_ficha(rango)})
        if id_ficha(rango) not in [f["id"] for f in fichas]:
            fichas.append(ficha_cazador(rango, 100))
    general = {"id": "c1", "version": "v1", "salas_total": len(salas), "paginas": 1, "salas_por_pagina": 50,
               "sala_inicial": 1, "sala_salida": max(salidas), "llave_salida": "itm_llave", "presupuesto_solicitudes": 9,
               "inventario_max": 10, "jugador": {"vida_max": 100000, "ataque": 6, "defensa": 2, "velocidad": 1000}}
    cliente = ClienteFalso(fichas, contenido, [{"pagina": 1, "total_paginas": 1, "salas": salas}], general)
    servicio = ServicioPartida(ClienteGeneral(cliente), ContadorSolicitudes(), asincrono=False)
    servicio.iniciar_nueva("c1", 3)
    return servicio


def mapa_de(servicio):
    return servicio.partida._mapa


def sala_del_jugador(servicio):
    return servicio.partida._jugador.sala_actual


# Desde la 1 hay dos caminos a la 4 (por la 3 cuesta 200) y uno a la 2 (cuesta 100). Para el jugador en la 2
# el mejor paso del cazador es el este, y para el jugador en la 4 es el norte.
DOS_CAMINOS = [(1, "E", 2, 100), (1, "N", 3, 100), (3, "E", 4, 100), (2, "S", 4, 500)]


class TestInvalidacionDeLaTablaDelCazador(unittest.TestCase):
    def test_abrir_una_puerta_con_llave_que_acorta_la_ruta_cambia_la_decision(self):  # FR-TER-015
        # Cerrada la puerta 1-2 el rodeo cuesta 1000 y supera el rango 600 asi que el cazador espera en t=100
        conexiones = [(1, "E", 2, 100), (1, "N", 5, 300), (5, "E", 6, 400), (6, "S", 2, 300)]
        salidas = cerrar_con_llave(grafo(conexiones), 1, "E", LLAVE)
        servicio = armar_servicio(salidas, [(1, "e-1", RANGO_SABUESO)], {5: [LLAVE]}, [FICHA_LLAVE])
        partida, mapa = servicio.partida, mapa_de(servicio)
        for accion in (A("mover", "N"), A("recoger", LLAVE), A("mover", "E"), A("mover", "S")):
            self.assertTrue(servicio.ejecutar(accion).aceptada)
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual((cazador.sala_actual, cazador.tiempo_siguiente), (1, 200))   # esperó con la tabla del rodeo
        self.assertTrue(servicio.ejecutar(A("abrir", direccion_opuesta("E"))).aceptada)
        avanzar_hasta(partida, 200)
        self.assertEqual((cazador.sala_actual, cazador.tiempo_siguiente), (2, 300))   # ahora la ruta cuesta 100

    def test_usar_el_pergamino_y_volver_a_una_sala_anterior_cambia_la_decision(self):  # FR-TER-015
        servicio = armar_servicio(grafo(DOS_CAMINOS), [(1, "e-1", RANGO_SABUESO)], {1: [PERGAMINO]}, [FICHA_PERGAMINO])
        partida, mapa = servicio.partida, mapa_de(servicio)
        self.assertTrue(servicio.ejecutar(A("recoger", PERGAMINO)).aceptada)
        recorrer(partida, ["E"])
        avanzar_hasta(partida, 90)
        recorrer(partida, ["S"])          # el jugador pasa a la 4 y el turno de t=100 se decide con ella como destino
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual(cazador.sala_actual, 3)
        self.assertTrue(servicio.ejecutar(A("pergamino")).aceptada)
        self.assertEqual((sala_del_jugador(servicio), cazador.sala_actual), (2, 1))
        avanzar_hasta(partida, 100)
        self.assertEqual((cazador.sala_actual, cazador.tiempo_siguiente), (2, 200))   # decide para la sala 2 y no la 4

    def test_activar_un_cazador_de_rango_mayor_no_deja_una_tabla_corta_para_el_nuevo(self):  # FR-TER-015
        # Salas 1 (sabueso) -400- 2 -10- 3 (espectro dormido) y 2 -990- 5. El jugador termina en la 5 a distancia 1000
        # del espectro, que solo la alcanza con su rango 2400. Con velocidad 1000 cada acción del jugador dura un décimo de su costo
        conexiones = [(1, "E", 2, 400), (2, "E", 3, 10), (2, "N", 5, 990)]
        servicio = armar_servicio(grafo(conexiones), [(1, "e-1", RANGO_SABUESO), (3, "e-2", RANGO_ESPECTRO)])
        partida, mapa = servicio.partida, mapa_de(servicio)
        recorrer(partida, ["E"])            # t=0 el jugador pasa a la 2 y su siguiente turno es t=40
        avanzar_hasta(partida, 100)         # t=100 el sabueso (distancia 400) pasa a la 2 y su siguiente turno es t=500
        sabueso = cazador_de(mapa, "e-1")
        self.assertEqual((sabueso.sala_actual, sabueso.tiempo_siguiente), (2, 500))
        recorrer(partida, ["E"])            # t=100 entra a la 3 y despierta al espectro con primer turno t=200
        espectro = cazador_de(mapa, "e-2")
        self.assertTrue(espectro.activo)
        self.assertEqual(espectro.tiempo_siguiente, 200)
        recorrer(partida, ["O", "N"])       # t=101 vuelve a la 2 y t=102 llega a la 5 con su siguiente turno en t=201
        avanzar_hasta(partida, 200)         # t=200 el espectro (distancia 10 + 990) da su primer paso por la salida de 10
        self.assertEqual(indices_de_ataque(partida, "e-2"), [])
        self.assertEqual((espectro.sala_actual, espectro.tiempo_siguiente), (2, 200 + 10))

    def test_cargar_una_partida_guardada_decide_como_desde_cero(self):  # FR-TER-015
        servicio = armar_servicio(grafo(DOS_CAMINOS), [(1, "e-1", RANGO_SABUESO)])
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "partida.sav"
            recorrer(servicio.partida, ["E"])
            servicio.guardar(ruta)        # jugador en la 2 y el turno del cazador en t=100 sin ejecutarse
            avanzar_hasta(servicio.partida, 90)
            recorrer(servicio.partida, ["S"])
            self.assertEqual(cazador_de(mapa_de(servicio), "e-1").sala_actual, 3)    # decidió para la sala 4
            servicio.cargar(ruta)
        partida, mapa = servicio.partida, mapa_de(servicio)
        self.assertEqual(sala_del_jugador(servicio), 2)
        avanzar_hasta(partida, 100)
        cazador = cazador_de(mapa, "e-1")
        self.assertEqual((cazador.sala_actual, cazador.tiempo_siguiente), (2, 200))


if __name__ == "__main__":
    unittest.main()
