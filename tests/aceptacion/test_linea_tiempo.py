"""Aceptación de la línea de tiempo (004): historias 1 a 5 de spec.md y casos B-LIN-001 a B-LIN-006.
Complementa tests/modelo/test_partida_linea_tiempo.py con servicio, controlador, guardado, replay y línea de comandos.
Matriz: B-LIN-001 y 004 en TestConsultaDeExtremoAExtremo, B-LIN-002 en TestPergaminoEnLaLineaVigente,
B-LIN-003 y SC-LIN-001 en TestConsultaDeExtremoAExtremo, B-LIN-005 y SC-LIN-005 en TestReplayHastaAceptacion,
B-LIN-006 y SC-LIN-006 en TestGuardarYCargarLaLinea y TestArchivoDeLaParte1Aceptacion, SC-LIN-007 en varias clases.
Se ejecuta con:  py -m unittest tests.aceptacion.test_linea_tiempo -v
"""
import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from cripta import __main__ as principal
from cripta.controlador.controlador_cripta import Orden
from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.modelo.accion import Accion as A
from cripta.modelo.inventario import ObjetoInventario
from cripta.servicios.servicio_replay import ServicioReplay
from tests.controlador import test_controlador_cripta as tcc
from tests.servicios import test_servicio_partida as tsp
from tests.servicios import test_servicio_partida_guardado as tsg
from tests.servicios import test_servicio_replay as tsr

RAIZ = Path(__file__).resolve().parents[2]
FIXTURE_PARTE_1 = RAIZ / "tests" / "datos" / "guardado_parte1.sav"
GUION = [A("recoger", "itm_antorcha"), A("mover", "N"), A("esperar"), A("atacar", "e-201"), A("esperar")]


def _campos(estado):
    # Los campos comunes entre la vista viva y el resumen histórico
    return (estado.tiempo, estado.sala_id, estado.vida, estado.vida_max, estado.ataque, estado.defensa,
            estado.velocidad, estado.efectos_activos)


def _dar_pergamino(servicio, identificador="p0"):
    # Pone un pergamino de retroceso en el inventario sin pasar por la bitácora
    ficha = servicio._catalogo.obtener("itm_pergamino_retroceso")
    servicio.partida._jugador.inventario.recoger(ObjetoInventario(identificador, ficha))


def _reiniciar_base(servicio):
    # La vida de prueba forma parte del estado inicial de la línea de tiempo
    servicio.partida._estado_base = servicio.partida._capturar()


def _observable(servicio, ruta_log=None):
    # Todo lo que una consulta no debe cambiar, incluida la bitácora en disco
    partida = servicio.partida
    contenido = Path(ruta_log).read_bytes() if ruta_log else None
    return (partida.vista(), partida.mensajes(), partida.puntaje(), len(partida._historial),
            len(partida.linea_tiempo()), partida.linea_tiempo().cantidad_checkpoints(),
            partida._reloj.tiempo_actual, partida._reloj.siguiente_secuencia, partida._azar.getstate(), contenido)


class _ConPartida(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.dir = Path(carpeta.name)
        self.ruta_log = self.dir / "partida.log"

    def jugar(self, guion=GUION, **opciones):
        # Servicio con cripta de pruebas y una fotografía viva antes de cada acción y otra al final
        servicio, _, _ = tsp.armar(**opciones)
        self.addCleanup(servicio.cerrar)
        tsp.iniciar(servicio, str(self.ruta_log))
        _reiniciar_base(servicio)
        fotos = []
        for accion in guion:
            fotos.append(servicio.partida.vista())
            self.assertTrue(servicio.ejecutar(accion).aceptada)
        fotos.append(servicio.partida.vista())
        return servicio, fotos


class TestConsultaDeExtremoAExtremo(_ConPartida):
    def setUp(self):
        super().setUp()
        self.servicio, self.fotos = self.jugar()
        self.partida = self.servicio.partida

    def test_t_posterior_al_reloj_se_rechaza_y_no_cambia_nada(self):  # B-LIN-001, FR-LIN-006, FR-LIN-023, SC-LIN-007
        antes = _observable(self.servicio, self.ruta_log)
        reloj = self.partida.vista().tiempo
        for instante in (reloj + 1, reloj + 1000):
            with self.assertRaises(ValueError) as contexto:
                self.partida.consultar_instante(instante)
            self.assertNotEqual(str(contexto.exception).strip(), "")
        self.assertEqual(_observable(self.servicio, self.ruta_log), antes)

    def test_instantes_con_decision_muestran_el_estado_justo_antes_de_ella(self):  # B-LIN-003, FR-LIN-002
        for foto in self.fotos[:-1]:
            with self.subTest(t=foto.tiempo):
                self.assertEqual(_campos(self.partida.consultar_instante(foto.tiempo)), _campos(foto))

    def test_el_reloj_actual_es_una_consulta_valida(self):  # FR-LIN-006
        self.assertEqual(_campos(self.partida.consultar_instante(self.partida.vista().tiempo)),
                         _campos(self.fotos[-1]))

    def test_cada_instante_devuelve_su_reloj_y_la_vida_nunca_sube(self):  # B-LIN-003, FR-LIN-001
        final = self.partida.vista().tiempo
        vidas = []
        for instante in range(0, final + 1, 10):
            resumen = self.partida.consultar_instante(instante)
            self.assertEqual(resumen.tiempo, instante)
            vidas.append(resumen.vida)
        self.assertEqual(vidas, sorted(vidas, reverse=True))
        self.assertLess(vidas[-1], vidas[0])

    def test_entre_dos_decisiones_la_sala_es_la_de_una_de_ellas(self):  # FR-LIN-001, FR-LIN-004
        salas = {foto.tiempo: foto.sala_id for foto in self.fotos}
        decisiones = sorted(salas)
        for inicio, fin in zip(decisiones, decisiones[1:]):
            for instante in range(inicio, fin):
                self.assertIn(self.partida.consultar_instante(instante).sala_id, (salas[inicio], salas[fin]))

    def test_cada_estado_antes_de_una_accion_coincide_con_el_vivo(self):  # US2, FR-LIN-003
        for k, foto in enumerate(self.fotos[:-1], start=1):
            with self.subTest(k=k):
                self.assertEqual(_campos(self.partida.consultar_accion(k)), _campos(foto))

    def test_el_resumen_trae_los_siete_grupos_en_toda_consulta_valida(self):  # SC-LIN-001, FR-LIN-004
        consultas = [self.partida.consultar_accion(k) for k in range(1, len(GUION) + 1)]
        consultas += [self.partida.consultar_instante(t) for t in (0, 75, 250)]
        for resumen in consultas:
            self.assertIsInstance(resumen.tiempo, int)
            self.assertIsInstance(resumen.sala_id, int)
            self.assertIsInstance(resumen.vida, int)
            self.assertIsInstance(resumen.inventario, tuple)
            self.assertIsInstance(resumen.efectos_activos, tuple)
            self.assertIsInstance(resumen.enemigos, tuple)
            self.assertGreaterEqual(len(resumen.mapa_conocido), 1)

    def test_los_enemigos_de_la_sala_traen_su_vida_del_momento(self):  # FR-LIN-004
        antes = self.partida.consultar_accion(4)
        despues = self.partida.consultar_accion(5)
        self.assertEqual(sorted(e.instancia for e in antes.enemigos), ["e-201", "e-202"])
        vida = lambda resumen: {e.instancia: e.vida for e in resumen.enemigos}["e-201"]
        self.assertLess(vida(despues), vida(antes))

    def test_el_mapa_conocido_crece_con_la_exploracion(self):  # FR-LIN-004, FR-LIN-019
        inicial = self.partida.consultar_accion(1).mapa_conocido
        final = self.partida.consultar_accion(5).mapa_conocido
        self.assertNotEqual(inicial, final)
        self.assertGreater(len(final), len(inicial))

    def test_una_consulta_valida_no_cambia_nada_y_no_se_registra(self):  # US1.5, US1.7, B-LIN-004, FR-LIN-005, SC-LIN-002
        antes = _observable(self.servicio, self.ruta_log)
        for instante in (0, 99, 100, 250, self.partida.vista().tiempo):
            self.partida.consultar_instante(instante)
        for k in range(1, len(GUION) + 1):
            self.partida.consultar_accion(k)
        self.assertEqual(_observable(self.servicio, self.ruta_log), antes)
        _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
        self.assertEqual(len(acciones), len(GUION))

    def test_la_partida_sigue_igual_que_una_de_control_sin_consultas(self):  # B-LIN-004, FR-LIN-005
        control, _ = self.jugar()
        for k in range(1, len(GUION) + 1):
            self.partida.consultar_accion(k)
            self.partida.consultar_instante(k * 60)
        for servicio in (self.servicio, control):
            for _ in range(3):
                servicio.ejecutar(A("esperar"))
        self.assertEqual(self.partida.vista(), control.partida.vista())
        self.assertEqual(self.partida.mensajes(), control.partida.mensajes())

    def test_las_consultas_rechazadas_no_cambian_nada(self):  # US1.8, US2.2, FR-LIN-023, SC-LIN-007
        antes = _observable(self.servicio, self.ruta_log)
        cantidad = len(GUION)
        for k in (0, -1, cantidad + 1, cantidad + 50):
            with self.subTest(k=k):
                with self.assertRaises(IndexError) as contexto:
                    self.partida.consultar_accion(k)
                self.assertNotEqual(str(contexto.exception).strip(), "")
        for malo in (-1, "10", 2.5, None):
            with self.subTest(t=malo):
                with self.assertRaises((ValueError, TypeError)):
                    self.partida.consultar_instante(malo)
        self.assertEqual(_observable(self.servicio, self.ruta_log), antes)


class TestNumeracionDeAcciones(_ConPartida):
    def test_las_ordenes_rechazadas_no_cuentan_ni_se_anotan(self):  # US2.3, FR-LIN-003
        servicio, _ = self.jugar([A("esperar")])
        self.assertFalse(servicio.ejecutar(A("mover", "O")).aceptada)
        self.assertFalse(servicio.ejecutar(A("atacar", "e-999")).aceptada)
        self.assertEqual(len(servicio.partida.linea_tiempo()), 1)
        _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
        self.assertEqual(len(acciones), 1)
        self.assertTrue(servicio.ejecutar(A("esperar")).aceptada)
        self.assertEqual(len(servicio.partida.linea_tiempo()), 2)

    def test_cada_paso_de_un_viaje_es_una_accion_numerada(self):  # US2.4, FR-LIN-003, FR-LIN-020
        # Un viaje de varias salas es una secuencia de movimientos y cada uno debe numerarse por separado
        servicio, fotos = self.jugar([A("mover", "N"), A("mover", "N"), A("mover", "S"), A("mover", "S")])
        partida = servicio.partida
        self.assertEqual(len(partida.linea_tiempo()), 4)
        self.assertEqual([partida.consultar_accion(k).sala_id for k in range(1, 5)], [1, 2, 3, 2])
        self.assertEqual(partida.consultar_instante(partida.vista().tiempo).sala_id, 1)


class TestPergaminoEnLaLineaVigente(_ConPartida):
    def preparar(self):
        servicio, fotos = self.jugar([A("esperar")] * 3, checkpoint_cada=2)
        _dar_pergamino(servicio)
        self.assertTrue(servicio.ejecutar(A("pergamino")).aceptada)
        return servicio, fotos

    def test_el_pergamino_recorta_la_linea_y_no_se_numera(self):  # B-LIN-002, US1.6, FR-LIN-003, FR-LIN-007
        servicio, fotos = self.preparar()
        partida = servicio.partida
        self.assertEqual(len(partida.linea_tiempo()), 2)
        self.assertEqual(partida.vista().tiempo, fotos[2].tiempo)
        for k in (1, 2):
            self.assertEqual(_campos(partida.consultar_accion(k)), _campos(fotos[k - 1]))
        for k in (0, 3):
            with self.assertRaises(IndexError):
                partida.consultar_accion(k)

    def test_un_t_posterior_al_reloj_restaurado_se_rechaza(self):  # B-LIN-002, FR-LIN-006
        servicio, fotos = self.preparar()
        partida = servicio.partida
        for instante in (fotos[2].tiempo + 1, fotos[3].tiempo):
            with self.assertRaises(ValueError):
                partida.consultar_instante(instante)
        self.assertEqual(_campos(partida.consultar_instante(fotos[1].tiempo)), _campos(fotos[1]))

    def test_la_numeracion_continua_desde_la_ultima_accion_vigente(self):  # B-LIN-002, FR-LIN-003, FR-LIN-007
        servicio, _ = self.preparar()
        vivo = servicio.partida.vista()
        self.assertTrue(servicio.ejecutar(A("esperar")).aceptada)
        self.assertEqual(len(servicio.partida.linea_tiempo()), 3)
        self.assertEqual(_campos(servicio.partida.consultar_accion(3)), _campos(vivo))

    def test_la_bitacora_conserva_el_pergamino_aunque_la_linea_lo_recorta(self):  # B-LIN-002, FR-LIN-003, FR-LIN-008
        self.preparar()
        _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
        self.assertEqual([a["tipo"] for a in acciones], ["esperar", "esperar", "esperar", "pergamino"])


class TestConsultaPorControlador(tcc.BaseControlador):
    ESPERAS = [Orden("esperar")] * 3

    def setUp(self):
        super().setUp()
        self.ruta_log = self.dir / "p.log"

    def consultar(self, *consultas):
        vista = tcc.VistaFalsa(ordenes=self.ESPERAS + [Orden("historia", c) for c in consultas])
        self.jugar(vista)
        return vista

    def test_la_consulta_valida_no_se_registra_en_partida_log(self):  # US1.7, FR-LIN-005
        vista = self.consultar("100", "#2", "0")
        self.assertEqual(len(vista.historias), 3)
        _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
        self.assertEqual(len(acciones), 3)

    def test_la_consulta_rechazada_avisa_el_motivo_y_no_toca_la_bitacora(self):  # US1.8, FR-LIN-023, SC-LIN-007
        for argumento in ("9999", "#0", "#4", "abc", "#", None):
            with self.subTest(argumento=argumento):
                vista = self.consultar(argumento)
                self.assertEqual(vista.historias, [])
                self.assertEqual(len(vista.avisos), 1)
                self.assertNotEqual(vista.avisos[0].strip(), "")
                self.assertEqual(vista.estados[-1][0].tiempo, 300)
                _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
                self.assertEqual(len(acciones), 3)

    def test_las_consultas_del_mapa_y_de_historia_no_cuentan_como_acciones(self):  # US2.3, FR-LIN-003
        vista = self.consultar("#1", "#2")
        self.assertEqual([r for _, r in vista.historias], ["#1", "#2"])
        self.assertEqual(vista.estados[-1][0].tiempo, 300)
        _, acciones = LectorBitacoraPartida(str(self.ruta_log)).leer()
        self.assertEqual(len(acciones), 3)


class TestGuardarYCargarLaLinea(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.dir = Path(carpeta.name)

    def jugar(self, guion=tsg.ANTES):
        servicio = tsg.armar()
        self.addCleanup(servicio.cerrar)
        tsg.iniciar(servicio)
        _reiniciar_base(servicio)
        for accion in guion:
            self.assertTrue(servicio.ejecutar(accion).aceptada)
        return servicio

    def cargar_copia(self, original):
        ruta = self.dir / "partida.bin"
        original.guardar(ruta)
        copia = tsg.armar()
        self.addCleanup(copia.cerrar)
        copia.cargar(ruta)
        return copia

    def comparar_toda_la_linea(self, original, copia):
        a, b = original.partida, copia.partida
        self.assertEqual(len(a.linea_tiempo()), len(b.linea_tiempo()))
        for k in range(1, len(a.linea_tiempo()) + 1):
            self.assertEqual(a.consultar_accion(k), b.consultar_accion(k))
        for instante in range(0, a.vista().tiempo + 1, 25):
            self.assertEqual(a.consultar_instante(instante), b.consultar_instante(instante))

    def test_historia_antes_y_despues_de_cargar_es_la_misma(self):  # US4.1, FR-LIN-010, SC-LIN-006
        original = self.jugar()
        self.comparar_toda_la_linea(original, self.cargar_copia(original))

    def test_v2_carga_puntos_completos_y_reducidos_con_la_misma_historia_que_replay(self):  # FR-LIN-008, FR-LIN-010
        with mock.patch("cripta.servicios.servicio_partida.CHECKPOINT_CADA_DEFECTO", 1):
            original, servicio_replay = tsr.armar_fixtures(), tsr.armar_fixtures()
        self.addCleanup(original.cerrar)
        log = str(tsr.LOG_CON_PERGAMINO)
        encabezado, acciones = LectorBitacoraPartida(log).leer()
        original.iniciar_nueva(encabezado["id_cripta"], encabezado["semilla"])
        partida = original.partida
        self.assertTrue(original.ejecutar(A.desde_dict(acciones[0])).aceptada)
        partida.linea_tiempo().buscar_checkpoint(1).estado = partida._capturar()
        for datos in acciones[1:]:
            self.assertTrue(original.ejecutar(A.desde_dict(datos)).aceptada)

        ruta = self.dir / "partida.bin"
        original.guardar(ruta)
        copia = tsr.armar_fixtures()
        self.addCleanup(copia.cerrar)
        copia.cargar(ruta)
        estado = copia.partida.a_estado_guardado(copia.version_catalogo)
        self.assertEqual(estado, partida.a_estado_guardado(original.version_catalogo))
        completo, reducido = estado.linea.checkpoints[:2]
        self.assertEqual(len(completo.estado.salas), len(estado.salas))
        self.assertLess(len(reducido.estado.salas), len(estado.salas))
        self.comparar_toda_la_linea(original, copia)

        instante = reducido.estado.reloj_actual
        replay = ServicioReplay(servicio_replay).reproducir(log, hasta=instante)
        self.assertTrue(replay.fiel)
        self.assertEqual(replay.historia, copia.partida.consultar_instante(instante))

    def test_la_linea_recortada_por_un_pergamino_se_conserva(self):  # US4.1, FR-LIN-007, FR-LIN-010
        original = self.jugar()
        _dar_pergamino(original)
        self.assertTrue(original.ejecutar(A("pergamino")).aceptada)
        copia = self.cargar_copia(original)
        self.comparar_toda_la_linea(original, copia)
        with self.assertRaises(IndexError):
            copia.partida.consultar_accion(len(tsg.ANTES))

    def test_tras_cargar_se_puede_seguir_jugando_y_consultando(self):  # FR-LIN-010, FR-LIN-021
        original = self.jugar()
        copia = self.cargar_copia(original)
        for servicio in (original, copia):
            for accion in tsg.DESPUES[:3]:
                servicio.ejecutar(accion)
        self.comparar_toda_la_linea(original, copia)

    def test_consultar_tras_cargar_no_cambia_la_partida(self):  # FR-LIN-005, FR-LIN-010
        copia = self.cargar_copia(self.jugar())
        antes = _observable(copia)
        copia.partida.consultar_accion(2)
        copia.partida.consultar_instante(100)
        self.assertEqual(_observable(copia), antes)


class TestArchivoDeLaParte1Aceptacion(tcc.BaseControlador):
    def setUp(self):
        super().setUp()
        self.ruta = self.dir / "p.sav"
        shutil.copyfile(FIXTURE_PARTE_1, self.ruta)
        self.bytes_antes = self.ruta.read_bytes()

    def test_cargar_un_archivo_de_la_parte_1_informa_la_version_y_no_lo_toca(self):  # US4.2, B-LIN-006, FR-LIN-011
        vista = tcc.VistaFalsa(ordenes=[Orden("esperar"), Orden("cargar"), Orden("esperar")])
        self.jugar(vista)
        self.assertEqual(len(vista.errores), 1)
        self.assertIn("versión", vista.errores[0])
        self.assertEqual(self.ruta.read_bytes(), self.bytes_antes)
        self.assertEqual([e[0].tiempo for e in vista.estados], [0, 100, 100, 200])

    def test_no_se_ofrece_migracion_ni_se_carga_en_silencio(self):  # B-LIN-006, FR-LIN-011, FR-LIN-012, SC-LIN-006
        vista = tcc.VistaFalsa(ordenes=[Orden("esperar"), Orden("cargar")])
        self.jugar(vista)
        mensajes = " ".join(vista.avisos + vista.errores + vista.preguntas).lower()
        self.assertNotIn("migr", mensajes)
        self.assertNotIn("cargada desde", mensajes)
        self.assertEqual(len(vista.errores), 1)

    def test_el_servicio_la_rechaza_sin_perder_la_partida_en_curso(self):  # B-LIN-006, FR-LIN-011
        servicio = tsg.armar()
        self.addCleanup(servicio.cerrar)
        tsg.iniciar(servicio)
        servicio.ejecutar(A("esperar"))
        antes = tsg.juego(tsg.estado_de(servicio))
        with self.assertRaises(CriptaFormatoIncompatibleError):
            servicio.cargar(self.ruta)
        self.assertEqual(tsg.juego(tsg.estado_de(servicio)), antes)
        self.assertEqual(self.ruta.read_bytes(), self.bytes_antes)


class TestCheckpointCadaAceptacion(unittest.TestCase):
    def correr(self, *argumentos):
        # main() con el servicio, la vista y el controlador sustituidos para ver qué recibe cada uno
        error = io.StringIO()
        with contextlib.redirect_stderr(error), contextlib.redirect_stdout(io.StringIO()), \
                mock.patch.object(principal, "ServicioPartida") as servicio, \
                mock.patch.object(principal, "VistaConsola") as vista, \
                mock.patch.object(principal, "ControladorCripta") as controlador:
            try:
                codigo = principal.main(["--offline", *argumentos])
            except SystemExit as salida:
                codigo = salida.code
        return codigo, error.getvalue(), servicio, vista, controlador

    def test_un_k_invalido_se_rechaza_al_iniciar_con_su_motivo(self):  # US5.1, FR-LIN-022, SC-LIN-007
        for invalido in ("0", "-3", "abc", "2.5", ""):
            with self.subTest(k=invalido):
                codigo, error, servicio, vista, controlador = self.correr("--checkpoint-cada", invalido)
                self.assertEqual(codigo, 2)
                self.assertIn("--checkpoint-cada", error)
                self.assertIn("entero mayor o igual a 1", error)
                servicio.assert_not_called()
                vista.assert_not_called()
                controlador.assert_not_called()

    def test_un_k_valido_llega_al_servicio_y_la_partida_inicia(self):  # US5, FR-LIN-013, FR-LIN-022
        for valido in ("1", "7", "5000"):
            with self.subTest(k=valido):
                codigo, _, servicio, _, controlador = self.correr("--checkpoint-cada", valido)
                self.assertEqual(codigo, 0)
                self.assertEqual(servicio.call_args.kwargs["checkpoint_cada"], int(valido))
                controlador.return_value.ejecutar.assert_called_once()

    def test_la_consulta_no_depende_del_k_elegido(self):  # FR-LIN-013, FR-LIN-015, FR-LIN-017
        resumenes = {}
        for k in (1, 2, 1000):
            servicio, _, _ = tsp.armar(checkpoint_cada=k)
            self.addCleanup(servicio.cerrar)
            tsp.iniciar(servicio)
            _reiniciar_base(servicio)
            for accion in GUION:
                self.assertTrue(servicio.ejecutar(accion).aceptada)
            partida = servicio.partida
            resumenes[k] = ([partida.consultar_accion(n) for n in range(1, len(GUION) + 1)],
                            [partida.consultar_instante(t) for t in range(0, partida.vista().tiempo + 1, 50)])
        self.assertEqual(resumenes[1], resumenes[2])
        self.assertEqual(resumenes[1], resumenes[1000])


class TestReplayHastaAceptacion(unittest.TestCase):
    def setUp(self):
        self.viva = tsr.partida_viva(tsr.LOG_CON_PERGAMINO)
        self.addCleanup(self.viva.cerrar)
        self.final = self.viva.partida.vista().tiempo

    def reproducir(self, hasta):
        return ServicioReplay(tsr.armar_fixtures()).reproducir(str(tsr.LOG_CON_PERGAMINO), hasta=hasta)

    def test_el_replay_da_el_mismo_resumen_que_historia_con_un_pergamino_en_la_bitacora(self):  # US3.1, FR-LIN-008, SC-LIN-005
        for instante in range(0, self.final + 1, max(1, self.final // 12)):
            with self.subTest(t=instante):
                resultado = self.reproducir(instante)
                self.assertEqual(resultado.historia, self.viva.partida.consultar_instante(instante))
                self.assertTrue(resultado.fiel)

    def test_el_replay_reproduce_toda_la_bitacora_incluido_lo_revertido(self):  # US3.1, FR-LIN-007, FR-LIN-008, SC-LIN-005
        # La bitácora tiene 8 acciones vigentes, una revertida y el pergamino que la revierte
        resultado = self.reproducir(0)
        self.assertTrue(resultado.fiel)
        self.assertEqual(len(self.viva.partida.linea_tiempo()), 8)
        self.assertEqual(resultado.acciones_reproducidas, resultado.acciones_en_log)
        self.assertEqual(resultado.acciones_en_log, 10)

    def test_hasta_despues_del_final_muestra_el_estado_final_e_indica_el_fin_anticipado(self):  # US3.2, B-LIN-005, FR-LIN-009
        resultado = self.reproducir(self.final + 500)
        self.assertTrue(resultado.termino_antes)
        self.assertEqual(resultado.instante, self.final)
        self.assertEqual(resultado.historia, self.viva.partida.consultar_instante(self.final))
        self.assertIn(f"terminó antes de t={self.final + 500}", resultado.informe())

    def test_por_la_linea_de_comandos_no_se_instancia_la_vista(self):  # US3.1, FR-LIN-008, SC-LIN-005
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida), mock.patch.object(principal, "VistaConsola") as vista, \
                mock.patch.object(principal, "ControladorCripta") as controlador, \
                mock.patch.object(principal, "DIRECTORIO_FIXTURES", str(RAIZ / "fixtures")), \
                tempfile.TemporaryDirectory() as datos, mock.patch.object(principal, "DIRECTORIO_DATOS", Path(datos)):
            codigo = principal.main(["--offline", "--replay", str(tsr.LOG_CON_PERGAMINO), "--hasta", str(self.final + 9)])
        self.assertEqual(codigo, 0)
        self.assertIn("terminó antes", salida.getvalue())
        vista.assert_not_called()
        controlador.assert_not_called()


if __name__ == "__main__":
    unittest.main()
