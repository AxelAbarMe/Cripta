"""Pruebas de la carga linea_tiempo del bench: registro en CARGAS, ejecución sin vista, conteos deterministas y escenarios de K.
No repite la prueba de humo de tests/bench/test_cargas_bench.py, que ya recorre todas las cargas a escala mínima.
Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.servicios.test_servicio_bench -v
"""
import contextlib
import functools
import io
import re
import unittest
from unittest import mock

from cripta.bench.cargas_bench import CARGAS, Resultado
from cripta.controlador.controlador_cripta import ControladorCripta
from cripta.servicios.servicio_bench import ServicioBench, ejecutar_bench_cli
from cripta.vista.vista_consola import VistaConsola

ESCALA_MINIMA = 0.01
CARGA = "linea_tiempo"
ESCENARIOS = (("K=100", r"\bK=100\b"), ("K=500", r"\bK=500\b"), ("K=1000", r"\bK=1000\b"),
              ("sin checkpoints", r"\bsin checkpoints\b"))   # K=100 no debe confundirse con K=1000


def _funcion():
    # La función de la carga tal como la registra CARGAS: la prueba falla con un motivo claro si no está
    for nombre, funcion in CARGAS:
        if nombre == CARGA:
            return funcion
    raise AssertionError(f"La carga {CARGA!r} no está registrada en CARGAS")


@functools.lru_cache(maxsize=None)
def _correr(_corrida):
    # Cada corrida llama a la carga como lo hace ServicioBench: con la escala como único argumento
    return _funcion()(ESCALA_MINIMA)


@contextlib.contextmanager
def _sin_vista():
    # Si algo de la carga intenta construir la vista o el controlador interactivo, la prueba falla
    with mock.patch.object(VistaConsola, "__init__", side_effect=AssertionError("se instanció la vista")), \
            mock.patch.object(ControladorCripta, "__init__", side_effect=AssertionError("se instanció el controlador")):
        yield


@functools.lru_cache(maxsize=None)
def _correr_con_servicio():
    with _sin_vista():
        servicio = ServicioBench(escala=ESCALA_MINIMA)
        return servicio, servicio.ejecutar([CARGA])


@functools.lru_cache(maxsize=None)
def _correr_en_la_linea_de_comandos():
    salida = io.StringIO()
    with _sin_vista(), contextlib.redirect_stdout(salida):
        codigo = ejecutar_bench_cli(["--solo", CARGA, "--escala", str(ESCALA_MINIMA)])
    return codigo, salida.getvalue()


def _resultados_de(etiqueta, patron, resultados):
    return [r for r in resultados if re.search(patron, r.caso)]


class TestRegistroDeLaCarga(unittest.TestCase):
    def test_linea_tiempo_esta_registrada_una_sola_vez_en_cargas(self):  # FR-LIN-018
        nombres = [nombre for nombre, _ in CARGAS]
        self.assertEqual(nombres.count(CARGA), 1)
        self.assertTrue(callable(_funcion()))

    def test_todos_los_resultados_son_del_subsistema(self):  # FR-LIN-018
        resultados = _correr(1)
        self.assertGreater(len(resultados), 0)
        for resultado in resultados:
            self.assertIsInstance(resultado, Resultado)
            self.assertEqual(resultado.subsistema, CARGA)

    def test_el_servicio_la_acepta_en_solo_y_la_ejecuta_sin_vista(self):  # FR-LIN-018, SC-LIN-003
        _, salida = _correr_con_servicio()
        self.assertEqual(list(salida), [CARGA])
        duracion, resultados = salida[CARGA]
        self.assertGreater(duracion, 0)
        self.assertGreater(len(resultados), 0)

    def test_la_linea_de_comandos_la_acepta_y_termina_bien(self):  # FR-LIN-018
        codigo, texto = _correr_en_la_linea_de_comandos()
        self.assertEqual(codigo, 0)
        self.assertIn("LINEA_TIEMPO", texto)

    def test_la_carga_directa_tampoco_instancia_la_vista(self):  # FR-LIN-018
        with _sin_vista():
            self.assertGreater(len(_funcion()(ESCALA_MINIMA)), 0)


class TestEscenariosDeK(unittest.TestCase):
    def test_reporta_K_100_500_1000_y_sin_checkpoints(self):  # FR-LIN-014, SC-LIN-003
        resultados = _correr(1)
        for etiqueta, patron in ESCENARIOS:
            with self.subTest(escenario=etiqueta):
                self.assertGreater(len(_resultados_de(etiqueta, patron, resultados)), 0)

    def test_cada_escenario_informa_memoria_y_la_consulta_con_mediana_y_maximo(self):  # FR-LIN-016, FR-LIN-018, SC-LIN-004
        resultados = _correr(1)
        for etiqueta, patron in ESCENARIOS:
            with self.subTest(escenario=etiqueta):
                propios = _resultados_de(etiqueta, patron, resultados)
                notas = " ".join(r.nota for r in propios)
                for campo in ("memoria", "mediana", "máximo"):
                    self.assertIn(campo, notas)
                for resultado in propios:
                    self.assertGreaterEqual(resultado.segundos, 0)
                    self.assertGreaterEqual(resultado.operaciones, 1)
                    self.assertFalse(resultado.es_razon)

    def test_el_cumplimiento_del_limite_de_50_ms_se_informa_con_lo_medido(self):  # FR-LIN-018, SC-LIN-003
        notas = " ".join(r.nota for r in _correr(1))
        self.assertIn("50 ms", notas)
        self.assertRegex(notas, r"\bN?O? ?CUMPLE\b")

    def test_los_escenarios_aparecen_en_el_reporte_de_texto_y_en_el_markdown(self):  # FR-LIN-014
        servicio, salida = _correr_con_servicio()
        texto = servicio.reporte_texto(salida)
        markdown = servicio.reporte_markdown(salida)
        self.assertIn(f"escala={ESCALA_MINIMA}", texto)
        self.assertIn("LINEA_TIEMPO", texto)
        self.assertTrue(any(linea.startswith(f"| {CARGA} |") for linea in markdown.splitlines()))
        for etiqueta, _ in ESCENARIOS:
            self.assertIn(etiqueta, texto)
            self.assertIn(etiqueta, markdown)


class TestConteosDeterministas(unittest.TestCase):
    def test_se_informa_la_semilla_las_acciones_y_las_salas(self):  # FR-LIN-018, SC-LIN-003
        casos = [r.caso for r in _correr(1)]
        completos = [c for c in casos if re.search(r"semilla \d+", c) and re.search(r"\d+ acciones", c)
                     and re.search(r"\d+ salas", c)]
        self.assertGreater(len(completos), 0)
        caso = completos[0]
        for patron in (r"semilla (\d+)", r"(\d+) acciones", r"(\d+) salas"):
            self.assertGreater(int(re.search(patron, caso).group(1)), 0)

    def test_dos_corridas_dan_los_mismos_conteos(self):  # FR-LIN-018, SC-LIN-003
        primera = [(r.caso, r.operaciones) for r in _correr(1)]
        segunda = [(r.caso, r.operaciones) for r in _correr(2)]
        self.assertEqual(primera, segunda)

    def test_los_casos_no_llevan_tiempos_medidos(self):  # FR-LIN-018
        # Lo medido va en la nota: el texto del caso identifica el escenario y debe ser igual entre corridas
        for resultado in _correr(1):
            self.assertNotRegex(resultado.caso, r"\d\s*(ms|µs|s)\b")

    def test_la_misma_escala_da_el_mismo_numero_de_resultados_por_escenario(self):  # FR-LIN-018
        for etiqueta, patron in ESCENARIOS:
            with self.subTest(escenario=etiqueta):
                self.assertEqual(len(_resultados_de(etiqueta, patron, _correr(1))),
                                 len(_resultados_de(etiqueta, patron, _correr(2))))


if __name__ == "__main__":
    unittest.main()
