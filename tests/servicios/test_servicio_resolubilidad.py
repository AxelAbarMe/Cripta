"""Pruebas de ServicioResolubilidad (T010).
Valida obtencion remota, cache versionada, limites de presupuesto y errores.
Cubre FR-RES-017, FR-RES-021, FR-RES-023, SC-006 y SC-008.
Se ejecuta con: py -m unittest tests.servicios.test_servicio_resolubilidad -v
"""
import tempfile
import unittest
from pathlib import Path

from cripta.dto.llave_ubicacion_dto import LlaveUbicacionDTO
from cripta.excepciones import CriptaDatosInvalidosError, CriptaLimiteError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.modelo.resolubilidad import ResultadoResolubilidad
from cripta.servicios.servicio_resolubilidad import ServicioResolubilidad
from tests.cliente_falso import ClienteFalso


class ClienteContado:
    """Envuelve ClienteCripta y descuenta presupuesto en cada solicitud."""

    def __init__(self, cliente, contador):
        self._cliente = cliente
        self._contador = contador

    def __getattr__(self, attr):
        metodo = getattr(self._cliente, attr)

        def envolver(*args, **kwargs):
            if self._contador.restantes < 1:
                raise CriptaLimiteError(self._contador.presupuesto_maximo)
            self._contador.registrar_solicitud()
            return metodo(*args, **kwargs)

        return envolver


def crear_datos_prueba(costo_opuesto: int = 100, presupuesto: int = 10):
    """Genera datos de prueba para dos salas conectadas por puerta cerrada."""
    general_json = {
        "id": "c1",
        "version": "v1",
        "salas_total": 2,
        "paginas": 1,
        "salas_por_pagina": 10,
        "sala_inicial": 1,
        "sala_salida": 2,
        "llave_salida": "itm_llave_salida",
        "presupuesto_solicitudes": presupuesto,
        "inventario_max": 5,
        "jugador": {"vida_max": 20, "ataque": 5, "defensa": 1, "velocidad": 100},
    }
    paginas_json = [{
        "pagina": 1,
        "total_paginas": 1,
        "salas": [
            {
                "id": 1,
                "nombre": "Sala 1",
                "salidas": {"E": {"sala": 2, "cerrada": True, "llave": "itm_llave_salida", "costo": 100}},
            },
            {
                "id": 2,
                "nombre": "Sala 2",
                "salidas": {"O": {"sala": 1, "cerrada": True, "llave": "itm_llave_salida", "costo": costo_opuesto}},
            },
        ],
    }]
    llaves = [LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None)]
    return general_json, paginas_json, llaves


class TestServicioResolubilidad(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)
        self.cache_disco = CacheDisco(AlmacenDiscoArchivos(self.carpeta))

    def test_obtiene_llaves_por_red_y_persiste_en_cache(self):
        # FR-RES-017, SC-006: obtiene llaves via cliente y las guarda en cache de disco
        general_json, paginas_json, llaves = crear_datos_prueba()
        cliente = ClienteFalso(general_json=general_json, paginas_json=paginas_json, llaves=llaves)
        contador = ContadorSolicitudes()
        servicio = ServicioResolubilidad(cliente, contador, self.cache_disco)

        res = servicio.verificar("c1")

        self.assertIsInstance(res, ResultadoResolubilidad)
        self.assertEqual(cliente.contar("obtener_llaves"), 1)
        en_cache = self.cache_disco.leer_llaves("c1", "v1")
        self.assertIsNotNone(en_cache)
        self.assertEqual(en_cache, tuple(llaves))

    def test_segunda_llamada_usa_cache_sin_consumir_presupuesto(self):
        # FR-RES-017, FR-RES-023, SC-006: la segunda consulta usa cache y no llama a cliente
        general_json, paginas_json, llaves = crear_datos_prueba()
        cliente = ClienteFalso(general_json=general_json, paginas_json=paginas_json, llaves=llaves)
        contador = ContadorSolicitudes()
        servicio = ServicioResolubilidad(cliente, contador, self.cache_disco)

        servicio.verificar("c1")
        self.assertEqual(cliente.contar("obtener_llaves"), 1)

        servicio.verificar("c1")
        self.assertEqual(cliente.contar("obtener_llaves"), 1)

    def test_presupuesto_agotado_antes_de_llaves_lanza_error_sin_reporte(self):
        # FR-RES-023, SC-008: presupuesto insuficiente antes de llaves lanza CriptaLimiteError
        general_json, paginas_json, llaves = crear_datos_prueba(presupuesto=2)
        cliente_base = ClienteFalso(general_json=general_json, paginas_json=paginas_json, llaves=llaves)
        contador = ContadorSolicitudes()
        cliente = ClienteContado(cliente_base, contador)
        servicio = ServicioResolubilidad(cliente, contador, cache_disco=None)

        with self.assertRaises(CriptaLimiteError):
            servicio.verificar("c1")

    def test_costos_contradictorios_en_esqueleto_lanzan_error(self):
        # FR-RES-021: costos opuestos desiguales propagan CriptaDatosInvalidosError
        general_json, paginas_json, llaves = crear_datos_prueba(costo_opuesto=250)
        cliente = ClienteFalso(general_json=general_json, paginas_json=paginas_json, llaves=llaves)
        contador = ContadorSolicitudes()
        servicio = ServicioResolubilidad(cliente, contador, cache_disco=None)

        with self.assertRaises(CriptaDatosInvalidosError):
            servicio.verificar("c1")

    def test_retorna_resultado_resolubilidad_completo_sobre_fixture_resoluble(self):
        # FR-RES-017, SC-006: retorna ResultadoResolubilidad exitoso con secuencia de llaves
        general_json, paginas_json, llaves = crear_datos_prueba()
        cliente = ClienteFalso(general_json=general_json, paginas_json=paginas_json, llaves=llaves)
        contador = ContadorSolicitudes()
        servicio = ServicioResolubilidad(cliente, contador, self.cache_disco)

        res = servicio.verificar("c1")

        self.assertIsInstance(res, ResultadoResolubilidad)
        self.assertTrue(res.es_resoluble)
        self.assertEqual(res.llaves_obtenidas, ("itm_llave_salida",))


if __name__ == "__main__":
    unittest.main()
