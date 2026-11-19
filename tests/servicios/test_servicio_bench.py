"""Pruebas de las cargas niebla_rutas, linea_tiempo, historial_cazadores y resolubilidad."""
import contextlib
import functools
import inspect
import io
import json
import re
import unittest
from types import SimpleNamespace
from unittest import mock

from cripta.bench import cargas_bench
from cripta.bench.cargas_bench import (
    CARGAS, DIRECTORIO_FIXTURES_BENCH, Resultado, _comparar_costos_con_mapa,
    _comparar_revelacion, _comparar_reversion, _elegir_fixture_referencia,
    _seleccion_lineal, _siguiente_paso_costos_guardados,
)
from cripta.controlador.controlador_cripta import ControladorCripta
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.modelo.resolubilidad import VerificadorResolubilidad
from cripta.modelo.ruta_conocida import siguiente_paso
from cripta.servicios.servicio_bench import ServicioBench, ejecutar_bench_cli
from cripta.vista.vista_consola import VistaConsola


class TestServicioBench(unittest.TestCase):
    def test_revelacion_y_reversion_equivalentes(self):
        """FR-NIE-018, SC-NIE-004: las alternativas dejan conocimiento equivalente."""
        referencia = _elegir_fixture_referencia()
        revelacion = _comparar_revelacion(referencia, 7, 41)
        reversion = _comparar_reversion(referencia, 7, 41)
        self.assertTrue(revelacion[0])
        self.assertTrue(reversion[0])
        self.assertEqual(len(revelacion[1]), 2)
        self.assertEqual(len(revelacion[2]), 2)
        self.assertGreater(revelacion[1][0], 0)
        self.assertGreater(revelacion[2][0], 0)
        self.assertEqual(len(reversion[1]), 2)
        self.assertEqual(len(reversion[2]), 2)
        self.assertGreater(reversion[1][0], 0)
        self.assertGreater(reversion[2][0], 0)
        self.assertGreater(reversion[3], 0)


    def test_rutas_y_costos_equivalentes_sobre_fixture_mayor(self):
        """FR-NIE-018, SC-NIE-002 y SC-NIE-004: algoritmos coinciden sin fijar id."""
        referencia = _elegir_fixture_referencia()
        self.assertGreater(referencia["salas"], 0)
        self.assertGreater(referencia["salidas"], 0)
        otra_referencia = _elegir_fixture_referencia()
        self.assertTrue(referencia["consultas"])
        self.assertEqual(referencia["consultas"], otra_referencia["consultas"])
        conocimiento = referencia["conocimiento"]
        for origen, destino in referencia["consultas"]:
            with self.subTest(origen=origen, destino=destino):
                self.assertIsNotNone(siguiente_paso(conocimiento, origen, destino))
                self.assertEqual(
                    siguiente_paso(conocimiento, origen, destino),
                    _seleccion_lineal(conocimiento, origen, destino),
                )
                self.assertEqual(
                    siguiente_paso(conocimiento, origen, destino),
                    _siguiente_paso_costos_guardados(conocimiento, origen, destino),
                )
        self.assertTrue(_comparar_costos_con_mapa(referencia))
        maximo = 0
        elegidos = []
        for carpeta in DIRECTORIO_FIXTURES_BENCH.iterdir():
            ruta = carpeta / "general.json"
            if not ruta.is_file():
                continue
            with ruta.open(encoding="utf-8") as archivo:
                total = json.load(archivo)["salas_total"]
            if total > maximo:
                maximo, elegidos = total, [carpeta.name]
            elif total == maximo:
                elegidos.append(carpeta.name)
        self.assertEqual(referencia["salas"], maximo)
        self.assertEqual(referencia["id"], min(elegidos))


ESCALA_MINIMA = 0.01
CARGA = "linea_tiempo"
ESCENARIOS = (("K=50", 50), ("K=100", 100), ("K=500", 500), ("K=1000", 1000),
              ("sin puntos periódicos", None))


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


def _resultados_de(etiqueta, resultados):
    return [r for r in resultados if r.caso.startswith(f"{etiqueta}:")]


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
    def test_reporta_los_cinco_escenarios(self):  # FR-LIN-014, SC-LIN-003
        resultados = _correr(1)
        for etiqueta, _ in ESCENARIOS:
            with self.subTest(escenario=etiqueta):
                self.assertEqual(len(_resultados_de(etiqueta, resultados)), 1)


    def test_cada_escenario_informa_memoria_y_la_consulta_con_mediana_y_maximo(self):  # FR-LIN-016, FR-LIN-018, SC-LIN-004
        resultados = _correr(1)
        for etiqueta, _ in ESCENARIOS:
            with self.subTest(escenario=etiqueta):
                propios = _resultados_de(etiqueta, resultados)
                notas = " ".join(r.nota for r in propios)
                for campo in ("memoria", "registro medio", "mediana", "máximo observado", "peor ciclo"):
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


    def test_cadencia_real_y_misma_carga_y_consultas_en_cada_corrida(self):  # FR-LIN-013, FR-LIN-014, FR-LIN-015, FR-LIN-018
        escenarios = []
        acciones = 1050


        def observar(etiqueta, corrida, posiciones):
            escenarios.append((etiqueta, corrida.partida, posiciones))
            return Resultado(CARGA, etiqueta, 0, len(posiciones))


        with mock.patch.object(cargas_bench, "_acciones_de_la_carga", return_value=acciones), \
                mock.patch.object(cargas_bench, "_resultado_de_escenario", side_effect=observar):
            _funcion()(ESCALA_MINIMA)


        self.assertEqual([etiqueta for etiqueta, _, _ in escenarios], [etiqueta for etiqueta, _ in ESCENARIOS])
        _, partida_base, consultas = escenarios[0]
        referencia = partida_base.linea_tiempo()
        self.assertTrue(any(tipo == "instante" for tipo, _ in consultas))
        for indice, ((_, k), (etiqueta, partida, posiciones)) in enumerate(zip(ESCENARIOS, escenarios)):
            with self.subTest(escenario=etiqueta):
                for _, previa, _ in escenarios[:indice]:
                    self.assertIsNot(partida, previa)
                linea = partida.linea_tiempo()
                self.assertIs(posiciones, consultas)
                self.assertEqual(linea._acciones, referencia._acciones)
                self.assertEqual(linea._tiempos, referencia._tiempos)
                esperados = [] if k is None else list(range(k, acciones + 1, k))
                self.assertEqual([punto.numero_acciones for punto in linea._puntos], esperados)
                self.assertEqual([punto.estado[0].acciones_jugador for punto in linea._puntos], esperados)
                if esperados:
                    for numero in (esperados[0], esperados[-1]):
                        self.assertIn(("accion", numero), consultas)
                        previo = linea.buscar_checkpoint(numero - 1)
                        self.assertEqual(previo.numero_acciones if previo else 0, numero - k)


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
        for etiqueta, _ in ESCENARIOS:
            with self.subTest(escenario=etiqueta):
                self.assertEqual(len(_resultados_de(etiqueta, _correr(1))),
                                 len(_resultados_de(etiqueta, _correr(2))))


class TestCriptaDeReferenciaComun(unittest.TestCase):
    def test_elige_la_cripta_con_mas_salas(self):  # AGENTS.md 7, P2 5.6
        criptas = [SimpleNamespace(id="cripta-a", salas=40), SimpleNamespace(id="cripta-b", salas=300),
                   SimpleNamespace(id="cripta-c", salas=120)]
        self.assertEqual(cargas_bench.elegir_cripta_de_referencia(criptas).id, "cripta-b")


    def test_el_empate_de_salas_lo_decide_el_menor_id(self):  # AGENTS.md 7, P2 5.6
        criptas = [SimpleNamespace(id="cripta-z", salas=300), SimpleNamespace(id="cripta-m", salas=300),
                   SimpleNamespace(id="cripta-x", salas=10)]
        self.assertEqual(cargas_bench.elegir_cripta_de_referencia(criptas).id, "cripta-m")


    def test_el_orden_del_listado_no_cambia_la_eleccion(self):  # AGENTS.md 7
        criptas = [SimpleNamespace(id="cripta-b", salas=7), SimpleNamespace(id="cripta-a", salas=7)]
        self.assertEqual(cargas_bench.elegir_cripta_de_referencia(criptas).id,
                         cargas_bench.elegir_cripta_de_referencia(list(reversed(criptas))).id)


    def test_la_de_los_fixtures_es_la_de_mayor_numero_de_salas(self):  # AGENTS.md 7, P2 5.6
        listado = ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH)).listar_criptas()
        elegida = cargas_bench.cripta_de_referencia()
        self.assertEqual(elegida.salas, max(cripta.salas for cripta in listado))


    def test_el_codigo_ya_no_fija_una_cripta_concreta(self):  # AGENTS.md 7
        self.assertFalse(hasattr(cargas_bench, "CRIPTA_REFERENCIA"))


    def test_ciclo_referencia_informa_la_cripta_elegida(self):  # P2 5.6
        resultados = cargas_bench.bench_ciclo_referencia(ESCALA_MINIMA, corridas=1)
        self.assertTrue(resultados[0].caso.startswith(f"{cargas_bench.cripta_de_referencia().id},"))


    def test_las_dos_cargas_usan_la_misma_funcion_de_eleccion(self):  # AGENTS.md 7, P2 5.6
        with mock.patch.object(cargas_bench, "elegir_cripta_de_referencia",
                               wraps=cargas_bench.elegir_cripta_de_referencia) as espia:
            cargas_bench.bench_ciclo_referencia(ESCALA_MINIMA, corridas=1)
            tras_ciclo = espia.call_count
            _funcion()(ESCALA_MINIMA)
            tras_linea = espia.call_count
        self.assertGreaterEqual(tras_ciclo, 1)
        self.assertGreater(tras_linea, tras_ciclo)


CARGA_CAZADORES = "historial_cazadores"


def _funcion_cazadores():
    # La función tal como la registra CARGAS: la prueba falla con un motivo claro si falta
    for nombre, funcion in CARGAS:
        if nombre == CARGA_CAZADORES:
            return funcion
    raise AssertionError(f"La carga {CARGA_CAZADORES!r} no está registrada en CARGAS")


@functools.lru_cache(maxsize=None)
def _correr_cazadores(_corrida):
    with _sin_vista():
        return _funcion_cazadores()(ESCALA_MINIMA)


def _inversas_y_reversion(resultados):
    inversas = [r for r in resultados if "operaciones inversas" in r.caso]
    reversion = [r for r in resultados if "revertir" in r.caso]
    return inversas, reversion


class TestHistorialConCazadores(unittest.TestCase):
    def test_esta_registrada_una_sola_vez_en_cargas(self):  # P2 5.6
        nombres = [nombre for nombre, _ in CARGAS]
        self.assertEqual(nombres.count(CARGA_CAZADORES), 1)


    def test_los_resultados_son_del_subsistema_y_hay_dos_casos(self):  # P2 5.6
        resultados = _correr_cazadores(1)
        for resultado in resultados:
            self.assertIsInstance(resultado, Resultado)
            self.assertEqual(resultado.subsistema, CARGA_CAZADORES)
        inversas, reversion = _inversas_y_reversion(resultados)
        self.assertEqual((len(inversas), len(reversion)), (1, 1))


    def test_corre_sin_instanciar_la_vista(self):  # P2 5.6, P2 6
        _correr_cazadores(1)


    def test_informa_la_cripta_los_cazadores_activos_y_las_acciones(self):  # P2 5.6
        inversas, _ = _inversas_y_reversion(_correr_cazadores(1))
        caso = inversas[0].caso
        self.assertGreater(int(re.search(r"(\d+) cazadores activos", caso).group(1)), 0)
        self.assertGreater(int(re.search(r"(\d+) acciones", caso).group(1)), 0)
        self.assertIn(cargas_bench.cripta_de_referencia().id, caso)


    def test_las_inversas_por_accion_traen_mediana_y_maximo(self):  # P2 5.6
        inversas, _ = _inversas_y_reversion(_correr_cazadores(1))
        encontrado = re.search(r"mediana (\d+) y máximo (\d+)", inversas[0].nota)
        mediana, maximo = int(encontrado.group(1)), int(encontrado.group(2))
        self.assertGreaterEqual(mediana, 1)
        self.assertGreaterEqual(maximo, mediana)


    def test_el_tiempo_de_revertir_trae_mediana_y_maximo(self):  # P2 5.6
        _, reversion = _inversas_y_reversion(_correr_cazadores(1))
        encontrado = re.search(r"mediana ([\d.]+) µs y máximo ([\d.]+) µs", reversion[0].nota)
        self.assertGreater(float(encontrado.group(1)), 0)
        self.assertGreaterEqual(float(encontrado.group(2)), float(encontrado.group(1)))


    def test_se_revierte_cada_accion_medida(self):  # P2 5.6
        inversas, reversion = _inversas_y_reversion(_correr_cazadores(1))
        acciones = int(re.search(r"(\d+) acciones", inversas[0].caso).group(1))
        self.assertEqual(reversion[0].operaciones, acciones)
        self.assertGreater(reversion[0].segundos, 0)


    def test_se_compara_con_la_carga_sintetica_de_la_parte_1(self):  # P2 5.6
        _, reversion = _inversas_y_reversion(_correr_cazadores(1))
        self.assertIn("sintética", reversion[0].nota)
        self.assertIn("6 inversas", reversion[0].nota)
        self.assertRegex(reversion[0].nota, r"por inversa")


    def test_los_conteos_son_deterministas(self):  # P2 5.6
        primera, _ = _inversas_y_reversion(_correr_cazadores(1))
        with _sin_vista():
            segunda, _ = _inversas_y_reversion(_funcion_cazadores()(ESCALA_MINIMA))
        self.assertEqual((primera[0].caso, primera[0].nota), (segunda[0].caso, segunda[0].nota))


    def test_el_caso_no_lleva_tiempos_medidos(self):  # P2 5.6
        for resultado in _correr_cazadores(1):
            self.assertNotRegex(resultado.caso, r"\d\s*(ms|µs|s)\b")


    def test_el_servicio_la_acepta_en_solo(self):  # P2 5.6
        with _sin_vista():
            salida = ServicioBench(escala=ESCALA_MINIMA).ejecutar([CARGA_CAZADORES])
        self.assertEqual(list(salida), [CARGA_CAZADORES])


SEMILLA_A = 20260928
SEMILLA_B = 7
CARGA_RESOLUBILIDAD = "resolubilidad"
CARGA_COTA = "resolubilidad_cota"


def _generar(k, salas_por_segmento, semilla):
    # Falla con un motivo claro si el generador aún no existe
    generador = getattr(cargas_bench, "_generar_cripta_encadenada", None)
    if generador is None:
        raise AssertionError("cargas_bench no define _generar_cripta_encadenada")
    return generador(k, salas_por_segmento, semilla)


def _huella(cripta):
    # Todo lo observable de la cripta como listas, para compararla sin depender de la identidad de objetos
    mapa, sala_inicial, sala_salida, llave_salida, llaves = cripta
    conexiones = []
    for sala in mapa.todas_las_salas():
        for direccion, destino in mapa.vecinos(sala.id):
            conexiones.append((sala.id, direccion, destino, mapa.datos_de_puerta(sala.id, direccion),
                               mapa.costo_de_conexion(sala.id, direccion)))
    return conexiones, sala_inicial, sala_salida, llave_salida, [(u.id, u.sala, u.enemigo) for u in llaves]


def _funcion_de(nombre):
    for registrado, funcion in CARGAS:
        if registrado == nombre:
            return funcion
    raise AssertionError(f"La carga {nombre!r} no está registrada en CARGAS")


class TestGeneradorEncadenado(unittest.TestCase):
    def test_bench_resolubilidad_reproducible(self):  # FR-RES-020, SC-007
        primera = _huella(_generar(5, 4, SEMILLA_A))
        segunda = _huella(_generar(5, 4, SEMILLA_A))
        otra = _huella(_generar(5, 4, SEMILLA_B))
        self.assertEqual(primera, segunda)
        self.assertNotEqual(primera, otra)

    def test_arma_k_llaves_y_k_por_salas_por_segmento_salas(self):  # FR-RES-020, SC-007
        for k, por_segmento in ((3, 2), (5, 4), (10, 20)):
            with self.subTest(k=k, salas_por_segmento=por_segmento):
                mapa, _, _, _, llaves = _generar(k, por_segmento, SEMILLA_A)
                self.assertEqual(len(mapa.todas_las_salas()), k * por_segmento)
                self.assertGreaterEqual(len(llaves), k)

    def test_la_cripta_generada_es_resoluble_con_ambos_recorridos(self):  # FR-RES-020, SC-007
        for k, por_segmento in ((3, 2), (8, 5)):
            with self.subTest(k=k, salas_por_segmento=por_segmento):
                mapa, inicial, salida, llave_salida, llaves = _generar(k, por_segmento, SEMILLA_A)
                verificador = VerificadorResolubilidad(mapa, inicial, salida, llave_salida, llaves)
                self.assertTrue(verificador.verificar().es_resoluble)
                self.assertTrue(verificador.verificar_ingenuo_reiniciado().es_resoluble)

    def test_con_k_y_salas_por_segmento_minimos_sigue_funcionando(self):  # FR-RES-020, SC-007
        mapa, inicial, salida, llave_salida, llaves = _generar(1, 1, SEMILLA_A)
        self.assertGreaterEqual(len(mapa.todas_las_salas()), 1)
        self.assertGreaterEqual(len(llaves), 1)
        verificador = VerificadorResolubilidad(mapa, inicial, salida, llave_salida, llaves)
        self.assertTrue(verificador.verificar().es_resoluble)
        self.assertTrue(verificador.verificar_ingenuo_reiniciado().es_resoluble)


class TestCargasDeResolubilidad(unittest.TestCase):
    def test_estan_registradas_una_sola_vez_en_cargas(self):  # FR-RES-020, SC-007
        nombres = [nombre for nombre, _ in CARGAS]
        for carga in (CARGA_RESOLUBILIDAD, CARGA_COTA):
            with self.subTest(carga=carga):
                self.assertEqual(nombres.count(carga), 1)

    def test_corren_a_escala_minima_sin_red_y_sin_vista(self):  # FR-RES-020, SC-007
        for carga in (CARGA_RESOLUBILIDAD, CARGA_COTA):
            with self.subTest(carga=carga), _sin_vista():
                resultados = _funcion_de(carga)(ESCALA_MINIMA)
                self.assertGreater(len(resultados), 0)
                for resultado in resultados:
                    self.assertIsInstance(resultado, Resultado)

    def test_la_cota_elige_la_cripta_con_la_funcion_de_eleccion(self):  # FR-RES-020, SC-007
        with mock.patch.object(cargas_bench, "elegir_cripta_de_referencia",
                               wraps=cargas_bench.elegir_cripta_de_referencia) as espia:
            _funcion_de(CARGA_COTA)(ESCALA_MINIMA)
        self.assertGreaterEqual(espia.call_count, 1)

    def test_la_cota_no_fija_el_id_de_una_cripta(self):  # FR-RES-020, SC-007
        fuente = inspect.getsource(_funcion_de(CARGA_COTA))
        for cripta in ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH)).listar_criptas():
            self.assertNotIn(cripta.id, fuente)


if __name__ == "__main__":
    unittest.main()
