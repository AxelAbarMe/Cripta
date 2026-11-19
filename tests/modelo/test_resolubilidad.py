"""Pruebas de resolubilidad y diagnostico causal (T001 a T004).
Cubre FR-RES-001 a FR-RES-012, FR-RES-018, FR-RES-019, FR-RES-022, SC-003 y SC-004.
Se ejecuta con: py -m unittest tests.modelo.test_resolubilidad -v
"""
import unittest

from cripta.constantes import direccion_opuesta
from cripta.dto.llave_ubicacion_dto import LlaveUbicacionDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.modelo.cripta_mapa import CriptaMapa

try:
    from cripta.modelo.resolubilidad import (
        CicloDependenciaLlaves,
        FronteraBloqueadaPuerta,
        ResultadoResolubilidad,
        UbicacionLlaveDiagnostico,
        VerificadorResolubilidad,
    )
except ImportError:
    CicloDependenciaLlaves = None
    FronteraBloqueadaPuerta = None
    ResultadoResolubilidad = None
    UbicacionLlaveDiagnostico = None
    VerificadorResolubilidad = None


def armar_mapa_desde_salas(salas_dict):
    """Construye CriptaMapa a partir de un diccionario de salas y salidas."""
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salas_dict.items()]
    mapa = CriptaMapa()
    mapa.agregar_pagina(PaginaEsqueletoDTO.desde_json({"pagina": 1, "total_paginas": 1, "salas": salas}))
    mapa.sincronizar_puertas()
    return mapa


def armar_mapa_conexiones(conexiones):
    """Construye un CriptaMapa simetrico a partir de una lista de conexiones."""
    claves_vistas = []
    for conn in conexiones:
        origen, direccion, destino = conn[0], conn[1], conn[2]
        claves = ((origen, direccion), (destino, direccion_opuesta(direccion)))
        for clave in claves:
            if clave in claves_vistas:
                raise ValueError(f"Dirección repetida en el fixture: {clave}")
            claves_vistas.append(clave)

    salidas = {}
    for conn in conexiones:
        origen, direccion, destino = conn[0], conn[1], conn[2]
        cerrada = conn[3] if len(conn) > 3 else False
        llave = conn[4] if len(conn) > 4 else None
        costo = conn[5] if len(conn) > 5 else 100
        salidas.setdefault(origen, {})[direccion] = {
            "sala": destino,
            "cerrada": cerrada,
            "llave": llave,
            "costo": costo,
        }
        opuesta = direccion_opuesta(direccion)
        salidas.setdefault(destino, {})[opuesta] = {
            "sala": origen,
            "cerrada": cerrada,
            "llave": llave,
            "costo": costo,
        }
    return armar_mapa_desde_salas(salidas)


def fixture_cripta_lineal_simple():
    """Cripta lineal simple con sala 1 a 2 abierta y 2 a 3 cerrada con llave."""
    conexiones = [
        (1, "E", 2, False, None),
        (2, "E", 3, True, "itm_llave_salida"),
    ]
    mapa = armar_mapa_conexiones(conexiones)
    llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo=None),)
    return mapa, 1, 3, "itm_llave_salida", llaves


def fixture_cripta_con_ciclo():
    """Cripta con ciclo de bloqueo mutuo entre dos llaves."""
    conexiones = [
        (1, "E", 2, False, None),
        (2, "E", 3, True, "itm_llave_a"),
        (2, "S", 4, True, "itm_llave_b"),
        (2, "N", 5, True, "itm_llave_salida"),
    ]
    mapa = armar_mapa_conexiones(conexiones)
    llaves = (
        LlaveUbicacionDTO(id="itm_llave_a", sala=4, enemigo=None),
        LlaveUbicacionDTO(id="itm_llave_b", sala=3, enemigo=None),
        LlaveUbicacionDTO(id="itm_llave_salida", sala=5, enemigo=None),
    )
    return mapa, 1, 5, "itm_llave_salida", llaves


def fixture_cripta_con_enemigo_errante():
    """Cripta donde un enemigo errante suelta la llave en su sala inicial."""
    conexiones = [
        (1, "E", 2, False, None),
        (2, "E", 3, True, "itm_llave_salida"),
    ]
    mapa = armar_mapa_conexiones(conexiones)
    llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo="ent_errante_1"),)
    return mapa, 1, 3, "itm_llave_salida", llaves


def fixture_cripta_con_varios_ordenes_validos():
    """Cripta con multiples ramas validas independientes con llaves."""
    conexiones = [
        (1, "N", 2, False, None),
        (1, "S", 3, False, None),
        (2, "E", 4, True, "itm_llave_beta"),
        (3, "E", 5, True, "itm_llave_alfa"),
        (5, "E", 6, True, "itm_llave_salida"),
    ]
    mapa = armar_mapa_conexiones(conexiones)
    llaves = (
        LlaveUbicacionDTO(id="itm_llave_beta", sala=2, enemigo=None),
        LlaveUbicacionDTO(id="itm_llave_alfa", sala=3, enemigo=None),
        LlaveUbicacionDTO(id="itm_llave_salida", sala=5, enemigo=None),
    )
    return mapa, 1, 6, "itm_llave_salida", llaves


class TestResolubilidad(unittest.TestCase):
    """Casos de prueba para VerificadorResolubilidad (T001 a T004)."""

    def setUp(self):
        """Verifica la disponibilidad del modulo de dominio antes de cada prueba."""
        global VerificadorResolubilidad
        if VerificadorResolubilidad is None:
            from cripta.modelo.resolubilidad import VerificadorResolubilidad

    # --- Bloque T002: Recorrido incremental basico ---

    def test_cripta_resoluble_directa(self):  # FR-RES-001, FR-RES-002, SC-004
        """Verifica resolubilidad directa en cripta lineal simple."""
        mapa, ini, salida, llave_salida, llaves = fixture_cripta_lineal_simple()
        verificador = VerificadorResolubilidad(mapa, ini, salida, llave_salida, llaves)
        resultado = verificador.verificar()
        self.assertTrue(resultado.es_resoluble)
        self.assertEqual(resultado.llaves_obtenidas, ("itm_llave_salida",))
        self.assertEqual(resultado.llaves_no_obtenibles, ())
        self.assertEqual(resultado.frontera_bloqueada, ())

    def test_llaves_no_consumibles(self):  # FR-RES-002, FR-RES-003
        """Comprueba que una misma llave abre multiples puertas consecutivas."""
        conexiones = [
            (1, "E", 2, False, None),
            (2, "E", 3, True, "itm_llave_comun"),
            (3, "E", 4, True, "itm_llave_comun"),
            (4, "E", 5, True, "itm_llave_salida"),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (
            LlaveUbicacionDTO(id="itm_llave_comun", sala=2, enemigo=None),
            LlaveUbicacionDTO(id="itm_llave_salida", sala=4, enemigo=None),
        )
        verificador = VerificadorResolubilidad(mapa, 1, 5, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertTrue(resultado.es_resoluble)
        self.assertEqual(resultado.llaves_obtenidas, ("itm_llave_comun", "itm_llave_salida"))

    def test_trampas_no_bloquean(self):  # FR-RES-006
        """Verifica que peligros y trampas en la ruta no impiden resolubilidad."""
        mapa, ini, salida, llave_salida, llaves = fixture_cripta_lineal_simple()
        verificador = VerificadorResolubilidad(mapa, ini, salida, llave_salida, llaves)
        resultado = verificador.verificar()
        self.assertTrue(resultado.es_resoluble)

    def test_puerta_abierta_a_sala_salida_sin_llave_salida_no_resoluble(self):  # FR-RES-001, SC-004
        """Acceso a sala de salida sin cruzar puerta con llave_salida es no resoluble."""
        conexiones = [
            (1, "E", 2, False, None),
            (1, "S", 3, False, None),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=3, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertIsNotNone(resultado.motivo_no_resoluble)

    def test_cripta_desconectada_sin_puertas(self):  # FR-RES-001, SC-004
        """Laberinto desconectado sin puertas hacia la salida es no resoluble."""
        salas = {
            1: {"E": {"sala": 2}},
            2: {"O": {"sala": 1}},
            3: {},
        }
        mapa = armar_mapa_desde_salas(salas)
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=3, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 3, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertEqual(len(resultado.frontera_bloqueada), 0)
        self.assertIn("itm_llave_salida", resultado.llaves_no_obtenibles)

    def test_sala_inicial_sin_salidas_transitables(self):  # FR-RES-001, FR-RES-010
        """Sala inicial con solo puertas cerradas sin llaves en sala 1."""
        conexiones = [
            (1, "E", 2, True, "itm_llave_1"),
            (1, "S", 3, True, "itm_llave_2"),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (
            LlaveUbicacionDTO(id="itm_llave_1", sala=2, enemigo=None),
            LlaveUbicacionDTO(id="itm_llave_2", sala=3, enemigo=None),
            LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo=None),
        )
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertEqual(len(resultado.frontera_bloqueada), 2)

    def test_llave_salida_inmediatamente_accesible(self):  # FR-RES-001, SC-004
        """Llave de salida y puerta final accesibles directamente desde sala inicial."""
        conexiones = [
            (1, "E", 2, True, "itm_llave_salida"),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertTrue(resultado.es_resoluble)
        self.assertEqual(resultado.llaves_obtenidas, ("itm_llave_salida",))

    # --- Bloque T003: Diagnostico, determinismo y enemigos ---

    def test_llave_salida_tras_propia_puerta_ApendiceB(self):  # FR-RES-001, FR-RES-012, SC-004
        """Llave de salida tras la puerta que ella misma abre forma ciclo."""
        conexiones = [
            (1, "E", 2, True, "itm_llave_salida"),
            (2, "E", 3, True, "itm_llave_salida"),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 3, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertTrue(len(resultado.ciclos_dependencia) >= 1)
        self.assertEqual(resultado.ciclos_dependencia[0].llaves, ("itm_llave_salida", "itm_llave_salida"))
        self.assertEqual(resultado.ciclos_dependencia[0].formato(), "itm_llave_salida -> itm_llave_salida")

    def test_llaves_obtenibles_campo_suelta_enemigo_errante_ApendiceB(self):  # FR-RES-005
        """Llave portada por enemigo errante es obtenible en su sala inicial."""
        mapa, ini, salida, llave_salida, llaves = fixture_cripta_con_enemigo_errante()
        verificador = VerificadorResolubilidad(mapa, ini, salida, llave_salida, llaves)
        resultado = verificador.verificar()
        self.assertTrue(resultado.es_resoluble)
        self.assertEqual(resultado.llaves_obtenidas, ("itm_llave_salida",))

    def test_varios_ordenes_validos_producen_misma_secuencia_ApendiceB(self):  # FR-RES-007, FR-RES-008, SC-003
        """Desempate determinista por menor identificador ante varios ordenes validos."""
        mapa1, ini1, sal1, ll1, ubis1 = fixture_cripta_con_varios_ordenes_validos()
        mapa2, ini2, sal2, ll2, ubis2 = fixture_cripta_con_varios_ordenes_validos()
        v1 = VerificadorResolubilidad(mapa1, ini1, sal1, ll1, ubis1)
        v2 = VerificadorResolubilidad(mapa2, ini2, sal2, ll2, ubis2)
        res1 = v1.verificar()
        res2 = v2.verificar()
        self.assertEqual(res1.llaves_obtenidas, res2.llaves_obtenidas)
        self.assertEqual(res1.llaves_obtenidas[0], "itm_llave_alfa")
        self.assertEqual(res1.llaves_obtenidas[1], "itm_llave_beta")

    def test_doble_ciclo_con_fixture_consistente(self):  # FR-RES-009, FR-RES-010, FR-RES-012
        """Reporta un ciclo representativo por cada grupo de bloqueo mutuo."""
        conexiones = [
            (1, "N", 2, True, "itm_c1_b"),
            (1, "S", 3, True, "itm_c1_a"),
            (1, "E", 7),
            (7, "N", 4, True, "itm_c2_y"),
            (7, "S", 5, True, "itm_c2_x"),
            (7, "E", 6, True, "itm_llave_salida"),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (
            LlaveUbicacionDTO(id="itm_c1_a", sala=2, enemigo=None), LlaveUbicacionDTO(id="itm_c1_b", sala=3, enemigo=None),
            LlaveUbicacionDTO(id="itm_c2_x", sala=4, enemigo=None), LlaveUbicacionDTO(id="itm_c2_y", sala=5, enemigo=None)
        )
        verificador = VerificadorResolubilidad(mapa, 1, 6, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertEqual(
            [c.formato() for c in resultado.ciclos_dependencia],
            ["itm_c1_a -> itm_c1_b -> itm_c1_a", "itm_c2_x -> itm_c2_y -> itm_c2_x"],
        )

    def test_puerta_cerrada_sin_llave(self):  # FR-RES-010, FR-RES-022
        """Puerta cerrada sin llave es permanentemente infranqueable."""
        conexiones = [
            (1, "E", 2, True, None),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertTrue(any(p.llave is None for p in resultado.frontera_bloqueada))

    def test_llave_exigida_sin_ubicacion(self):  # FR-RES-011, FR-RES-022
        """Puerta cerrada que exige llave no listada se reporta como sin_ubicacion."""
        conexiones = [
            (1, "E", 2, True, "itm_fantasma"),
        ]
        mapa = armar_mapa_conexiones(conexiones)
        llaves = ()
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertTrue(
            any(u.id_llave == "itm_fantasma" and u.estado == "sin_ubicacion" for u in resultado.ubicaciones_llaves)
        )

    def test_puertas_bilaterales(self):  # FR-RES-019
        """Puerta declarada cerrada en un solo sentido rige en ambos lados."""
        salas = {
            1: {"E": {"sala": 2, "cerrada": False}},
            2: {"O": {"sala": 1, "cerrada": True, "llave": "itm_llave_bilateral"}},
        }
        mapa = armar_mapa_desde_salas(salas)
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        resultado = verificador.verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertTrue(
            any(
                p.sala_origen == 1 and p.direccion == "E" and p.llave == "itm_llave_bilateral"
                for p in resultado.frontera_bloqueada
            )
        )

    # --- Bloque T004: Recorrido incremental y alternativa ingenua ---

    def test_equivalencia_verificar_e_ingenuo_reiniciado(self):  # FR-RES-018, FR-RES-020
        """Ambos metodos coinciden en criptas resolubles y no resolubles."""
        casos = [
            fixture_cripta_lineal_simple(),
            fixture_cripta_con_ciclo(),
            fixture_cripta_con_enemigo_errante(),
            fixture_cripta_con_varios_ordenes_validos(),
            (armar_mapa_conexiones([(1, "E", 3), (3, "E", 2), (1, "N", 2, True, "itm_llave_salida")]),
             1, 2, "itm_llave_salida", (LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None),)),
            (armar_mapa_conexiones([(1, "E", 2, True, "itm_llave_salida")]),
             1, 2, "itm_llave_salida", (LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo=None),)),
        ]
        for mapa, ini, salida, llave_salida, llaves in casos:
            with self.subTest(sala_salida=salida, llaves=llaves):
                verificador = VerificadorResolubilidad(mapa, ini, salida, llave_salida, llaves)
                res_incremental = verificador.verificar()
                res_ingenuo = verificador.verificar_ingenuo_reiniciado()
                self.assertEqual(res_incremental.es_resoluble, res_ingenuo.es_resoluble)

    def test_dos_rutas_a_la_salida_cuenta_la_puerta_con_llave_salida(self):  # FR-RES-001, FR-RES-002
        """Una segunda ruta registra la entrada por la puerta de llave de salida."""
        mapa = armar_mapa_conexiones([
            (1, "E", 3), (3, "E", 2), (1, "N", 2, True, "itm_llave_salida")
        ])
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None),)
        verificador = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves)
        self.assertTrue(verificador.verificar().es_resoluble)
        self.assertTrue(verificador.verificar_ingenuo_reiniciado().es_resoluble)

    def test_llave_salida_dentro_de_la_sala_de_salida_ApendiceB(self):  # FR-RES-001, FR-RES-012
        """La llave tras la puerta que ella abre produce un ciclo propio."""
        mapa = armar_mapa_conexiones([(1, "E", 2, True, "itm_llave_salida")])
        llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo=None),)
        resultado = VerificadorResolubilidad(mapa, 1, 2, "itm_llave_salida", llaves).verificar()
        self.assertFalse(resultado.es_resoluble)
        self.assertEqual([c.formato() for c in resultado.ciclos_dependencia],
                         ["itm_llave_salida -> itm_llave_salida"])

    def test_orden_de_entrada_no_cambia_el_resultado(self):  # FR-RES-008
        """Permutar las ubicaciones no cambia el resultado determinista."""
        mapa, ini, salida, llave_salida, llaves = fixture_cripta_con_varios_ordenes_validos()
        original = VerificadorResolubilidad(mapa, ini, salida, llave_salida, llaves).verificar()
        invertido = VerificadorResolubilidad(mapa, ini, salida, llave_salida, tuple(reversed(llaves))).verificar()
        self.assertEqual(original, invertido)

    def test_metodo_verificar_ingenuo_reiniciado_separado(self):  # FR-RES-018, FR-RES-020
        """Verifica que verificar_ingenuo_reiniciado existe como metodo separado."""
        self.assertTrue(hasattr(VerificadorResolubilidad, "verificar_ingenuo_reiniciado"))
        self.assertTrue(callable(getattr(VerificadorResolubilidad, "verificar_ingenuo_reiniciado")))


if __name__ == "__main__":
    unittest.main()
