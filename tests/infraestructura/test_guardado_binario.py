"""Pruebas del formato binario de guardado (§4.10): GuardadoBinario y la comparación con JSON.

Los tests de tests/modelo/test_guardado_*.py revisan que una partida real, guardada y cargada,
siga igual. Estos revisan el formato del archivo: que el índice quede ordenado, que se pueda
cargar una sola sala, que los valores que no caben den error y que un archivo dañado se rechace.
Usan el mismo estado de prueba que el bench.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.infraestructura.test_guardado_binario -v
"""
import random
import shutil
import struct
import tempfile
import unittest
from dataclasses import fields, replace
from pathlib import Path

from cripta.bench.cargas_bench import estado_sintetico
from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura import guardado_binario
from cripta.infraestructura.estado_guardado import ConocimientoGuardado, EstadoPartida, EstadoRNG
from cripta.infraestructura.guardado_binario import FORMATO_VERSION, GuardadoBinario, cargar_json, guardar_json

N_SALAS = 50
FIXTURE_PARTE_1 = Path(__file__).resolve().parents[1] / "datos" / "guardado_parte1.sav"   # guardado real de la Parte I


def _rng(semilla, sorteos):
    # Estado del azar con valor en gauss_next y el generador que lo produjo, para comparar la secuencia
    azar = random.Random(semilla)
    for _ in range(sorteos):
        azar.random()
    azar.gauss(0, 1)
    return EstadoRNG.desde_random(azar), azar


def _conocimiento(salas, variante):
    # Conocimiento de la 002 con estados, puertas y costos que incluyen None y enteros
    estados = tuple(("desconocida", "avistada", "explorada")[(i + variante) % 3] for i in range(salas + 1))
    puertas = tuple(tuple(("no_observada", "abierta", "cerrada", "no_observada")[(i + j + variante) % 4]
                          for j in range(4)) for i in range(salas + 1))
    costos = tuple(tuple(None if (i + j + variante) % 3 == 0 else 20 + i * 10 + j for j in range(4))
                   for i in range(salas + 1))
    return ConocimientoGuardado(estados, puertas, costos)


def _punto(numero, semilla, sorteos, reloj, variante):
    # Punto de control con su propio estado completo, su estado del azar y su conocimiento
    from cripta.infraestructura.estado_guardado import PuntoControlGuardado
    rng, _azar = _rng(semilla, sorteos)
    estado = replace(estado_sintetico(3), rng=rng, reloj_actual=reloj, acciones_jugador=numero,
                     conocimiento=_conocimiento(3, variante))
    return PuntoControlGuardado(numero, estado, variante)


def _linea():
    # Línea de tiempo con acciones de los tres tipos de argumento, ajustes y dos checkpoints
    from cripta.infraestructura.estado_guardado import AccionGuardada, AjusteGuardado, LineaGuardada
    acciones = (
        AccionGuardada("mover", "N", 0), AccionGuardada("esperar", None, 100), AccionGuardada("usar", 1, 200),
        AccionGuardada("recoger", "itm_antorcha", 325), AccionGuardada("mover", "E", 350),
        AccionGuardada("atacar", "e-201", 450), AccionGuardada("esperar", None, 550),
    )
    ajustes = (
        AjusteGuardado(2, "quitar", "p0", ""), AjusteGuardado(2, "agregar", "i-1", "itm_pergamino_retroceso"),
        AjusteGuardado(5, "quitar", "p1", ""),
    )
    return LineaGuardada(3, _punto(0, 1, 0, 0, 0), acciones, ajustes, (_punto(3, 1, 30, 300, 1), _punto(6, 1, 60, 700, 2)))


def _estado_con_linea():
    # Estado principal con el conocimiento de la 002 y la línea de tiempo completa
    return replace(estado_sintetico(N_SALAS), conocimiento=_conocimiento(N_SALAS, 0), linea=_linea())


class TestGuardadoBinario(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)
        self.ruta = self.carpeta / "partida.sav"
        self.guardado = GuardadoBinario()
        self.estado = estado_sintetico(N_SALAS)   # las salas vienen desordenadas a propósito
        self.guardado.guardar(self.ruta, self.estado)

    def sala_original(self, sala_id):
        for sala in self.estado.salas:
            if sala.sala_id == sala_id:
                return sala
        return None

    def test_cargar_da_el_mismo_estado(self):
        cargado = self.guardado.cargar(self.ruta)
        # Todo lo que no es salas, igual
        self.assertEqual(replace(cargado, salas=()), replace(self.estado, salas=()))
        # Las salas: las mismas, cada una igual a la original
        self.assertEqual(len(cargado.salas), N_SALAS)
        for sala in cargado.salas:
            self.assertEqual(sala, self.sala_original(sala.sala_id))

    def test_las_salas_vuelven_ordenadas_por_id(self):
        # Se guardaron desordenadas; el índice las deja en orden (§4.9), y cargar() respeta ese orden
        cargado = self.guardado.cargar(self.ruta)
        self.assertEqual([s.sala_id for s in cargado.salas], list(range(1, N_SALAS + 1)))

    def test_cargar_una_sola_sala(self):
        for sala_id in (1, 25, N_SALAS):            # la primera, una del medio y la última del índice
            self.assertEqual(self.guardado.cargar_sala(self.ruta, sala_id), self.sala_original(sala_id))
        self.assertIsNone(self.guardado.cargar_sala(self.ruta, N_SALAS + 1))

    def test_leer_encabezado_sin_cargar_salas(self):
        e = self.estado
        self.assertEqual(self.guardado.leer_encabezado(self.ruta),
                         (e.cripta_id, e.cripta_version, e.catalogo_version, e.semilla, N_SALAS))

    def test_valores_que_no_caben_son_error_y_no_tocan_el_archivo_anterior(self):
        vida_enorme = replace(self.estado, jugador=replace(self.estado.jugador, vida=2**40))
        with self.assertRaises(ValueError):
            self.guardado.guardar(self.ruta, vida_enorme)
        with self.assertRaises(ValueError):
            self.guardado.guardar(self.ruta, replace(self.estado, mensajes=("x" * 70000,)))
        # El guardado que ya estaba sigue sano
        self.assertEqual(self.guardado.leer_encabezado(self.ruta)[4], N_SALAS)

    def danar(self, inicio, nuevos_bytes):
        # Reemplaza bytes del archivo a partir de `inicio`
        crudo = self.ruta.read_bytes()
        self.ruta.write_bytes(crudo[:inicio] + nuevos_bytes + crudo[inicio + len(nuevos_bytes):])

    def test_n_salas_absurdo_es_error(self):
        self.danar(8, struct.pack("<I", 10_000_000))     # bytes 8-11 del encabezado: n_salas
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar_sala(self.ruta, 25)

    def test_archivo_cortado_es_error(self):
        crudo = self.ruta.read_bytes()
        self.ruta.write_bytes(crudo[: len(crudo) // 2])
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)

    def test_archivo_que_no_es_de_cripta_o_de_otra_version_es_error(self):
        self.danar(0, b"XXXX")                           # bytes 0-3: el magic "CRPT"
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)
        self.guardado.guardar(self.ruta, self.estado)
        self.danar(4, struct.pack("<H", 99))             # bytes 4-5: versión del formato
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)

    def test_json_reconstruye_lo_mismo(self):
        # La comparación de tiempos del bench solo es justa si cargar_json arma el mismo estado
        ruta_json = self.carpeta / "partida.json"
        guardar_json(ruta_json, self.estado)
        self.assertEqual(cargar_json(ruta_json), self.estado)


class TestGuardadoLineaDeTiempo(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "partida.sav"
        self.guardado = GuardadoBinario()
        self.estado = _estado_con_linea()
        self.guardado.guardar(self.ruta, self.estado)
        self.cargado = self.guardado.cargar(self.ruta)

    def test_la_linea_completa_vuelve_igual(self):  # FR-LIN-010, SC-LIN-006
        self.assertEqual(self.cargado.linea, self.estado.linea)

    def test_las_acciones_vuelven_en_orden_y_con_el_tipo_de_su_argumento(self):  # FR-LIN-010
        acciones = self.cargado.linea.acciones
        self.assertEqual(acciones, self.estado.linea.acciones)
        self.assertEqual([type(a.argumento) for a in acciones], [str, type(None), int, str, str, str, type(None)])
        self.assertEqual([a.tiempo for a in acciones], [0, 100, 200, 325, 350, 450, 550])

    def test_los_ajustes_vuelven_en_orden_con_su_posicion(self):  # FR-LIN-005, FR-LIN-010
        ajustes = self.cargado.linea.ajustes
        self.assertEqual(ajustes, self.estado.linea.ajustes)
        self.assertEqual([a.posicion for a in ajustes], [2, 2, 5])
        self.assertEqual([a.operacion for a in ajustes], ["quitar", "agregar", "quitar"])

    def test_los_checkpoints_vuelven_en_orden_con_su_estado_completo(self):  # FR-LIN-010, FR-LIN-016
        originales = self.estado.linea.checkpoints
        puntos = self.cargado.linea.checkpoints
        self.assertEqual([p.numero_acciones for p in puntos], [3, 6])
        for punto, original in zip(puntos, originales):
            self.assertEqual(replace(punto.estado, salas=()), replace(original.estado, salas=()))
            self.assertEqual(punto.estado.salas, original.estado.salas)
            self.assertEqual(punto.siguiente_instancia, original.siguiente_instancia)

    def test_cada_checkpoint_conserva_su_conocimiento(self):  # FR-LIN-019, FR-LIN-021
        for punto, original in zip(self.cargado.linea.checkpoints, self.estado.linea.checkpoints):
            self.assertEqual(punto.estado.conocimiento, original.estado.conocimiento)
            self.assertIsNotNone(punto.estado.conocimiento)

    def test_cada_checkpoint_continua_la_misma_secuencia_aleatoria(self):  # FR-LIN-017
        for punto, sorteos in zip(self.cargado.linea.checkpoints, (30, 60)):
            self.assertEqual(punto.estado.rng, _rng(1, sorteos)[0])
            restaurado = random.Random()
            punto.estado.rng.aplicar_a(restaurado)
            esperado = _rng(1, sorteos)[1]
            self.assertEqual([restaurado.random() for _ in range(5)], [esperado.random() for _ in range(5)])
            self.assertEqual(restaurado.gauss(0, 1), esperado.gauss(0, 1))

    def test_el_estado_base_vuelve_igual(self):  # FR-LIN-010, FR-LIN-017
        base = self.cargado.linea.base
        self.assertEqual(base.numero_acciones, 0)
        self.assertEqual(base.estado.rng, self.estado.linea.base.estado.rng)
        self.assertEqual(base.estado.conocimiento, self.estado.linea.base.estado.conocimiento)
        self.assertEqual(base, self.estado.linea.base)

    def test_la_frecuencia_k_vuelve_igual(self):  # FR-LIN-013, FR-LIN-010
        self.assertEqual(self.cargado.linea.frecuencia, 3)

    def test_una_linea_vacia_vuelve_igual(self):  # FR-LIN-010
        from cripta.infraestructura.estado_guardado import LineaGuardada
        vacia = LineaGuardada(100, _punto(0, 1, 0, 0, 0), (), (), ())
        self.guardado.guardar(self.ruta, replace(self.estado, linea=vacia))
        self.assertEqual(self.guardado.cargar(self.ruta).linea, vacia)

    def test_un_estado_sin_linea_vuelve_sin_linea(self):  # FR-LIN-010
        self.guardado.guardar(self.ruta, estado_sintetico(N_SALAS))
        self.assertIsNone(self.guardado.cargar(self.ruta).linea)

    def test_el_resto_del_estado_no_cambia_por_llevar_linea(self):  # FR-LIN-010, FR-LIN-021
        sin_salas = lambda estado: replace(estado, salas=(), linea=None)
        self.assertEqual(sin_salas(self.cargado), sin_salas(self.estado))
        self.assertEqual(len(self.cargado.salas), N_SALAS)
        for sala in self.cargado.salas:   # las salas vuelven ordenadas por id, así que se comparan una a una
            original = [s for s in self.estado.salas if s.sala_id == sala.sala_id][0]
            self.assertEqual(sala, original)

    def test_cargar_una_sala_y_leer_el_encabezado_siguen_funcionando(self):  # FR-LIN-010
        for sala in self.estado.salas[:3]:
            self.assertEqual(self.guardado.cargar_sala(self.ruta, sala.sala_id), sala)
        e = self.estado
        self.assertEqual(self.guardado.leer_encabezado(self.ruta),
                         (e.cripta_id, e.cripta_version, e.catalogo_version, e.semilla, N_SALAS))

    def test_un_argumento_de_accion_que_no_se_puede_guardar_no_toca_el_archivo_anterior(self):  # FR-LIN-010
        from cripta.infraestructura.estado_guardado import AccionGuardada
        antes = self.ruta.read_bytes()
        linea = replace(self.estado.linea, acciones=(AccionGuardada("esperar", 1.5, 0),))
        with self.assertRaises(ValueError):
            self.guardado.guardar(self.ruta, replace(self.estado, linea=linea))
        self.assertEqual(self.ruta.read_bytes(), antes)

    def test_un_archivo_con_linea_cortado_es_error(self):  # FR-LIN-010, FR-LIN-011
        crudo = self.ruta.read_bytes()
        for fraccion in (2, 3, 4):
            self.ruta.write_bytes(crudo[: len(crudo) * (fraccion - 1) // fraccion])
            with self.assertRaises(CriptaFormatoIncompatibleError):
                self.guardado.cargar(self.ruta)


class TestGuardadoContadorDeInstancias(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "partida.sav"
        self.guardado = GuardadoBinario()

    def test_el_contador_vuelve_igual(self):  # FR-LIN-010, FR-LIN-021
        for contador in (0, 1, 7, 123456):
            self.guardado.guardar(self.ruta, replace(estado_sintetico(N_SALAS), siguiente_instancia=contador))
            self.assertEqual(self.guardado.cargar(self.ruta).siguiente_instancia, contador)

    def test_el_contador_forma_parte_de_la_igualdad_del_estado(self):  # FR-LIN-021
        estado = estado_sintetico(N_SALAS)
        self.assertNotEqual(replace(estado, siguiente_instancia=3), replace(estado, siguiente_instancia=4))

    def test_cada_checkpoint_conserva_el_contador_de_su_estado(self):  # FR-LIN-010, FR-LIN-017
        linea = _linea()
        puntos = tuple(replace(p, estado=replace(p.estado, siguiente_instancia=p.siguiente_instancia + 10))
                       for p in linea.checkpoints)
        base = replace(linea.base, estado=replace(linea.base.estado, siguiente_instancia=5))
        estado = replace(estado_sintetico(N_SALAS), siguiente_instancia=9,
                         linea=replace(linea, base=base, checkpoints=puntos))
        self.guardado.guardar(self.ruta, estado)
        cargado = self.guardado.cargar(self.ruta)
        self.assertEqual(cargado.siguiente_instancia, 9)
        self.assertEqual(cargado.linea.base.estado.siguiente_instancia, 5)
        self.assertEqual([p.estado.siguiente_instancia for p in cargado.linea.checkpoints], [11, 12])

    def test_un_contador_que_no_cabe_es_error_y_no_toca_el_archivo_anterior(self):  # FR-LIN-010
        self.guardado.guardar(self.ruta, estado_sintetico(N_SALAS))
        antes = self.ruta.read_bytes()
        with self.assertRaises(ValueError):
            self.guardado.guardar(self.ruta, replace(estado_sintetico(N_SALAS), siguiente_instancia=2**40))
        self.assertEqual(self.ruta.read_bytes(), antes)


class TestGuardadoConocimiento(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "partida.sav"
        self.guardado = GuardadoBinario()

    def test_el_conocimiento_se_compara_como_parte_del_estado(self):  # FR-LIN-021
        campo = [f for f in fields(EstadoPartida) if f.name == "conocimiento"][0]
        self.assertTrue(campo.compare)

    def test_el_conocimiento_vuelve_igual(self):  # FR-LIN-019, FR-LIN-021, SC-LIN-006
        estado = replace(estado_sintetico(N_SALAS), conocimiento=_conocimiento(N_SALAS, 0))
        self.guardado.guardar(self.ruta, estado)
        cargado = self.guardado.cargar(self.ruta)
        self.assertIsNotNone(cargado.conocimiento)
        self.assertEqual(cargado.conocimiento, estado.conocimiento)

    def test_los_costos_vuelven_con_sus_none_y_enteros(self):  # FR-LIN-019, FR-LIN-021
        estado = replace(estado_sintetico(N_SALAS), conocimiento=_conocimiento(N_SALAS, 1))
        self.guardado.guardar(self.ruta, estado)
        costos = self.guardado.cargar(self.ruta).conocimiento.costos
        self.assertEqual(costos, estado.conocimiento.costos)
        planos = [c for fila in costos for c in fila]
        self.assertIn(None, planos)
        self.assertTrue(all(c is None or type(c) is int for c in planos))

    def test_los_estados_y_las_puertas_vuelven_como_texto(self):  # FR-LIN-019, FR-LIN-021
        estado = replace(estado_sintetico(N_SALAS), conocimiento=_conocimiento(N_SALAS, 2))
        self.guardado.guardar(self.ruta, estado)
        conocimiento = self.guardado.cargar(self.ruta).conocimiento
        self.assertEqual(conocimiento.estados, estado.conocimiento.estados)
        self.assertEqual(conocimiento.puertas, estado.conocimiento.puertas)

    def test_sin_conocimiento_vuelve_sin_conocimiento(self):  # FR-LIN-021
        self.guardado.guardar(self.ruta, estado_sintetico(N_SALAS))
        self.assertIsNone(self.guardado.cargar(self.ruta).conocimiento)


class TestArchivoDeLaParte1(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)
        self.ruta = self.carpeta / "partida.sav"
        shutil.copyfile(FIXTURE_PARTE_1, self.ruta)
        self.bytes_antes = self.ruta.read_bytes()
        self.modificado_antes = self.ruta.stat().st_mtime_ns
        self.guardado = GuardadoBinario()

    def test_la_fixture_es_un_guardado_de_la_parte_1(self):  # FR-LIN-011
        self.assertEqual(self.bytes_antes[:4], b"CRPT")
        self.assertEqual(struct.unpack("<H", self.bytes_antes[4:6])[0], 1)

    def test_el_formato_nuevo_cambia_de_version(self):  # FR-LIN-011, B-LIN-006
        self.assertNotEqual(FORMATO_VERSION, 1)
        otra = self.carpeta / "nuevo.sav"
        self.guardado.guardar(otra, estado_sintetico(3))
        self.assertEqual(struct.unpack("<H", otra.read_bytes()[4:6])[0], FORMATO_VERSION)

    def test_cargar_un_archivo_de_la_parte_1_da_un_error_claro_de_version(self):  # FR-LIN-011, B-LIN-006, SC-LIN-006
        with self.assertRaises(CriptaFormatoIncompatibleError) as contexto:
            self.guardado.cargar(self.ruta)
        mensaje = str(contexto.exception)
        self.assertIn("versión", mensaje)
        self.assertIn("1", mensaje)
        self.assertIn(str(FORMATO_VERSION), mensaje)

    def test_cargar_una_sala_y_leer_el_encabezado_tambien_lo_rechazan(self):  # FR-LIN-011, B-LIN-006
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar_sala(self.ruta, 1)
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.leer_encabezado(self.ruta)

    def test_el_archivo_no_se_modifica_ni_se_borra(self):  # FR-LIN-011, B-LIN-006
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)
        self.assertTrue(self.ruta.exists())
        self.assertEqual(self.ruta.read_bytes(), self.bytes_antes)
        self.assertEqual(self.ruta.stat().st_mtime_ns, self.modificado_antes)
        self.assertEqual(sorted(p.name for p in self.carpeta.iterdir()), ["partida.sav"])

    def test_no_se_carga_en_silencio_aunque_se_intente_varias_veces(self):  # FR-LIN-011
        for _ in range(3):
            with self.assertRaises(CriptaFormatoIncompatibleError):
                self.guardado.cargar(self.ruta)
        self.assertEqual(self.ruta.read_bytes(), self.bytes_antes)

    def test_no_se_ofrece_migracion(self):  # FR-LIN-012, B-LIN-006
        nombres = dir(guardado_binario) + dir(GuardadoBinario)
        self.assertEqual([n for n in nombres if "migr" in n.lower()], [])


if __name__ == "__main__":
    unittest.main()