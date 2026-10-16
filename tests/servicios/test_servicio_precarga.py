"""Pruebas de ServicioPrecarga (§4.2): lotes de contenido, el hilo de red y la población de salas.

Revisan que nunca se pidan más lotes de los necesarios, que una respuesta que no llega no deje
al jugador esperando para siempre (y que si llega tarde se ignore), que pedir una sala después
de cerrar falle enseguida, y que los enemigos de una sala queden ordenados por id (§2.4).

Para controlar cuándo "llega" una respuesta sin depender de esperas con time.sleep, se usa un
cliente que se queda bloqueado hasta que el test lo suelta.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.servicios.test_servicio_precarga -v
"""
import threading
import time
import unittest

from cripta.excepciones import CriptaApiError, CriptaError
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from tests.cliente_falso import ClienteFalso
from tests.cripta_artificial import construir


class ClienteQueEspera(ClienteFalso):
    """Responde obtener_contenido solo cuando el test hace soltar.set()."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soltar = threading.Event()

    def obtener_contenido(self, cripta_id, salas):
        self.soltar.wait(timeout=5)       # el tope evita que un test roto se quede colgado
        return super().obtener_contenido(cripta_id, salas)


def armar(datos, clase_cliente=ClienteFalso, **opciones):
    cliente = clase_cliente(datos["fichas"], datos["contenido"], datos["paginas"], datos["general"])
    mapa = CriptaMapa()
    precarga = ServicioPrecarga(cliente, "c1", mapa, **opciones)
    precarga.cargar_esqueleto(len(datos["paginas"]))
    return precarga, cliente, mapa


class TestLotes(unittest.TestCase):
    def test_recorrer_toda_la_cripta_usa_el_minimo_de_lotes(self):
        # 25 salas en lotes de hasta 10: nunca más de 3 solicitudes de contenido
        datos = construir(filas=5, columnas=5)
        precarga, cliente, mapa = armar(datos, asincrono=False)
        for sala_id in range(1, 26):
            self.assertTrue(precarga.asegurar_contenido(sala_id).contenido_cargado)
        self.assertEqual(cliente.contar("obtener_contenido"), 3)

    def test_con_hilo_de_red_la_sala_llega_igual(self):
        datos = construir(filas=5, columnas=5)
        precarga, _, _ = armar(datos)                      # asincrono=True: lo normal en el juego
        self.addCleanup(precarga.cerrar)
        self.assertTrue(precarga.asegurar_contenido(1).contenido_cargado)


class TestHiloDeRed(unittest.TestCase):
    def setUp(self):
        datos = construir(filas=5, columnas=5)
        self.precarga, self.cliente, self.mapa = armar(datos, clase_cliente=ClienteQueEspera, espera_maxima=0.2)
        self.addCleanup(self.precarga.cerrar)
        self.addCleanup(self.cliente.soltar.set)          # por si un test falla con el cliente bloqueado

    def test_si_la_respuesta_no_llega_a_tiempo_es_error_y_no_se_queda_esperando(self):
        inicio = time.perf_counter()
        with self.assertRaises(CriptaApiError):
            self.precarga.asegurar_contenido(1)
        self.assertLess(time.perf_counter() - inicio, 2)  # esperó la espera máxima (0.2 s), no para siempre

    def test_la_respuesta_tardia_se_ignora_y_se_puede_reintentar(self):
        with self.assertRaises(CriptaApiError):
            self.precarga.asegurar_contenido(1)
        self.cliente.soltar.set()                          # ahora sí llega la respuesta vieja...
        self.precarga._lotes[0].evento.wait(timeout=2)     # ...se espera a que el hilo la termine
        self.assertFalse(self.mapa.obtener(1).contenido_cargado)   # ...y no se usó: el lote ya estaba cerrado
        # Reintento: la sala se volvió a pedir en un lote nuevo, y esta vez llega
        self.assertTrue(self.precarga.asegurar_contenido(1).contenido_cargado)
        self.assertEqual(self.cliente.contar("obtener_contenido"), 2)

    def test_pedir_una_sala_despues_de_cerrar_falla_enseguida(self):
        self.cliente.soltar.set()
        self.precarga.asegurar_contenido(1)                # crea el hilo de red y trae el primer lote
        self.precarga.cerrar()                             # el hilo termina
        inicio = time.perf_counter()
        with self.assertRaises(CriptaError) as contexto:
            self.precarga.asegurar_contenido(25)           # está lejos: necesita un lote nuevo
        # No es el error de "no llegó a tiempo": falló de una vez, sin esperar
        self.assertNotIsInstance(contexto.exception, CriptaApiError)
        self.assertLess(time.perf_counter() - inicio, 0.2)


class TestPoblarSala(unittest.TestCase):
    def enemigos_de_la_sala(self, cantidad, invertidos):
        datos = construir(filas=2, columnas=2)
        numeros = list(range(cantidad))
        if invertidos:
            numeros.reverse()
        # La sala 3 (posición 2 de la lista) recibe `cantidad` ratas, en el orden de `numeros`
        datos["contenido"][2]["enemigos"] = [{"instancia": f"e-{k:03d}", "tipo": "ent_rata"} for k in numeros]
        cliente = ClienteFalso(datos["fichas"], datos["contenido"], datos["paginas"], datos["general"])
        mapa = CriptaMapa()
        precarga = ServicioPrecarga(cliente, "c1", mapa, servicio_catalogo=ServicioCatalogo(cliente),
                                    asincrono=False)
        precarga.cargar_esqueleto(len(datos["paginas"]))
        sala = precarga.preparar_sala(3)
        return [enemigo.instancia_id for enemigo in sala.enemigos_dormidos]

    def test_los_enemigos_quedan_ordenados_por_id(self):
        casos = ((2, True), (40, False), (40, True))      # pocos (caso real), muchos en orden, muchos al revés
        for cantidad, invertidos in casos:
            with self.subTest(cantidad=cantidad, invertidos=invertidos):
                ids = self.enemigos_de_la_sala(cantidad, invertidos)
                self.assertEqual(ids, [f"e-{k:03d}" for k in range(cantidad)])


if __name__ == "__main__":
    unittest.main()