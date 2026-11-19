"""Pruebas de ServicioReplay (--replay, §4.11) con la cripta congelada de tests/datos/.

Se ejecuta desde la raíz del proyecto con:
    python -m unittest tests.servicios.test_servicio_replay -v
"""
import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from cripta import __main__ as principal
from cripta.excepciones import CriptaBitacoraError
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.modelo.accion import Accion as A
from cripta.servicios.servicio_partida import ServicioPartida
from cripta.servicios.servicio_replay import ServicioReplay
from tests.servicios.test_servicio_partida import CRIPTA, armar

GUION = [A("mover", "N"), A("esperar")]
RAIZ = Path(__file__).resolve().parents[2]
LOG_CON_PERGAMINO = RAIZ / "docs" / "ejemplos" / "partida_cripta-02.log"   # 8 acciones vigentes y un pergamino que revierte la novena


def armar_fixtures():
    # Servicio sobre las criptas de fixtures/, que es donde viven los logs de docs/ejemplos
    return ServicioPartida(ClienteGeneral(ClienteOffline(str(RAIZ / "fixtures"))), ContadorSolicitudes(), asincrono=False)


def partida_viva(ruta):
    # Juega en vivo las mismas acciones del log: es la partida contra la que se compara el replay
    encabezado, acciones = LectorBitacoraPartida(str(ruta)).leer()
    servicio = armar_fixtures()
    servicio.iniciar_nueva(encabezado["id_cripta"], encabezado["semilla"], None)
    for datos in acciones:
        assert servicio.ejecutar(A.desde_dict(datos)).aceptada
    return servicio


class PruebaReplay(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "partida.log"
        self.original, _, _ = armar()
        self.original.iniciar_nueva(CRIPTA, 7, str(self.ruta))
        for accion in GUION:
            self.assertTrue(self.original.ejecutar(accion).aceptada)

    def tearDown(self):
        self.original.cerrar()
        self._carpeta.cleanup()

    def _reproducir(self, ruta=None):
        servicio, _, _ = armar()
        return ServicioReplay(servicio).reproducir(str(ruta or self.ruta))

    def _reescribir(self, cambiar):
        nueva = Path(self._carpeta.name) / "modificada.log"
        nueva.write_text(cambiar(self.ruta.read_text(encoding="utf-8")), encoding="utf-8")
        return nueva

    def test_reproduce_la_misma_partida(self):
        resultado = self._reproducir()
        self.assertTrue(resultado.fiel)
        self.assertEqual((resultado.acciones_reproducidas, resultado.acciones_en_log), (2, 2))
        self.assertEqual(resultado.puntaje, self.original.partida.puntaje())
        self.assertEqual(resultado.desenlace, self.original.partida.desenlace())

    def test_muestra_un_paso_por_accion_con_sus_mensajes(self):
        resultado = self._reproducir()
        self.assertEqual(len(resultado.pasos), 2)
        self.assertTrue(resultado.pasos[0].startswith("[1] mover N -> t=100"))
        self.assertIn(resultado.pasos[0], resultado.informe())

    def test_no_modifica_el_log(self):
        antes = self.ruta.read_bytes()
        self._reproducir()
        self.assertEqual(self.ruta.read_bytes(), antes)

    def test_version_distinta_no_se_reproduce(self):
        ruta = self._reescribir(lambda texto: texto.replace('"version_catalogo": "', '"version_catalogo": "x', 1))
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertEqual(resultado.acciones_reproducidas, 0)
        self.assertIsNone(resultado.desenlace)
        self.assertIn("catálogo", resultado.problemas[0])

    def test_log_parcial_no_se_reproduce(self):
        ruta = self._reescribir(lambda texto: texto.replace("}\n", ', "parcial": true}\n', 1))
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertIn("parcial", resultado.problemas[0])

    def test_accion_que_no_se_acepta_reporta_la_linea(self):
        ruta = self._reescribir(lambda texto: texto + '{"tipo": "abrir", "direccion": "S"}\n')
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertEqual(resultado.acciones_reproducidas, 2)
        self.assertIn("línea 4", resultado.problemas[0])

    def test_accion_invalida_reporta_la_linea(self):
        ruta = self._reescribir(lambda texto: texto + '{"tipo": "volar"}\n')
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertIn("línea 4", resultado.problemas[0])

    def test_ultima_linea_incompleta_se_avisa_y_se_reproduce(self):
        ruta = self._reescribir(lambda texto: texto + '{"tipo": "mov')
        resultado = self._reproducir(ruta)
        self.assertTrue(resultado.fiel)
        self.assertEqual(len(resultado.avisos), 1)

    def test_log_inexistente(self):
        with self.assertRaises(CriptaBitacoraError):
            self._reproducir(Path(self._carpeta.name) / "nada.log")

    def test_accion_invalida_despues_de_comentario_reporta_linea_real(self):
        """FR-NIE-016, comentario cuenta en la ubicación real de la acción inválida."""
        texto = self.ruta.read_text(encoding="utf-8").splitlines()
        texto.insert(1, "# ir a 2")
        texto.append('{"tipo": "volar"}')
        ruta = Path(self._carpeta.name) / "invalida_con_comentario.log"
        ruta.write_text("\n".join(texto) + "\n", encoding="utf-8")
        resultado = self._reproducir(ruta)
        self.assertFalse(resultado.fiel)
        self.assertIn("línea 5", resultado.problemas[0])

    def test_comentario_de_viaje_no_altera_replay(self):
        """FR-NIE-016, escenario de viaje: replay omite comentario y conserva el estado final."""
        texto = self.ruta.read_text(encoding="utf-8").splitlines()
        texto.insert(1, "# ir a 2")
        ruta_comentada = Path(self._carpeta.name) / "con_comentario.log"
        ruta_comentada.write_text("\n".join(texto) + "\n", encoding="utf-8")
        resultado = self._reproducir(ruta_comentada)
        resultado_sin_comentario = self._reproducir(self.ruta)
        self.assertTrue(resultado.fiel)
        self.assertEqual((resultado.acciones_reproducidas, resultado.acciones_en_log), (2, 2))
        self.assertEqual(resultado.desenlace, resultado_sin_comentario.desenlace)
        self.assertEqual(resultado.puntaje, resultado_sin_comentario.puntaje)


class TestReplayHasta(unittest.TestCase):
    def setUp(self):
        self.viva = partida_viva(LOG_CON_PERGAMINO)
        self.addCleanup(self.viva.cerrar)
        self.reloj_final = self.viva.partida.vista().tiempo

    def reproducir(self, hasta=None, ruta=LOG_CON_PERGAMINO):
        servicio = armar_fixtures()
        return ServicioReplay(servicio).reproducir(str(ruta), hasta=hasta)

    def test_el_log_de_ejemplo_tiene_un_pergamino_que_recorta_la_linea(self):  # SC-LIN-005
        linea = self.viva.partida.linea_tiempo()
        self.assertEqual(len(linea), 8)
        self.assertGreaterEqual(len(linea.ajustes_en(8)), 1)

    def test_hasta_consulta_con_el_mismo_componente_que_historia(self):  # FR-LIN-008, SC-LIN-005
        for instante in (0, 1, self.reloj_final // 2, self.reloj_final - 1, self.reloj_final):
            with self.subTest(t=instante):
                resultado = self.reproducir(instante)
                self.assertEqual(resultado.historia, self.viva.partida.consultar_instante(instante))
                self.assertEqual(resultado.instante, instante)
                self.assertFalse(resultado.termino_antes)

    def test_la_linea_del_replay_incluye_el_recorte_del_pergamino(self):  # FR-LIN-008, FR-LIN-007
        # Un instante que solo existió en la rama revertida ya no se consulta: se limita al reloj final
        resultado = self.reproducir(self.reloj_final + 1)
        self.assertEqual(resultado.instante, self.reloj_final)
        self.assertEqual(resultado.historia, self.viva.partida.consultar_instante(self.reloj_final))

    def test_hasta_mayor_que_el_reloj_final_muestra_el_final_e_indica_el_final_anticipado(self):  # FR-LIN-009, B-LIN-005
        for hasta in (self.reloj_final + 1, self.reloj_final + 5000):
            with self.subTest(hasta=hasta):
                resultado = self.reproducir(hasta)
                self.assertTrue(resultado.termino_antes)
                self.assertEqual(resultado.instante, self.reloj_final)
                self.assertIn(f"terminó antes de t={hasta}", resultado.informe())
                self.assertIn(f"Historia t={self.reloj_final}", resultado.informe())

    def test_hasta_igual_al_reloj_final_no_es_final_anticipado(self):  # FR-LIN-009
        resultado = self.reproducir(self.reloj_final)
        self.assertFalse(resultado.termino_antes)
        self.assertNotIn("terminó antes", resultado.informe())

    def test_el_estado_final_coincide_con_la_partida_viva(self):  # FR-LIN-008, FR-LIN-009
        historia = self.reproducir(self.reloj_final + 1).historia
        vista = self.viva.partida.vista()
        self.assertEqual((historia.tiempo, historia.sala_id, historia.vida, historia.vida_max),
                         (vista.tiempo, vista.sala_id, vista.vida, vista.vida_max))
        self.assertEqual(historia.efectos_activos, vista.efectos_activos)
        self.assertEqual(len(historia.inventario), vista.inventario_cantidad)

    def test_sin_hasta_no_hay_consulta(self):  # FR-LIN-008
        resultado = self.reproducir()
        self.assertTrue(resultado.fiel)
        self.assertIsNone(resultado.historia)
        self.assertIsNone(resultado.instante)
        self.assertFalse(resultado.termino_antes)
        self.assertNotIn("Historia t=", resultado.informe())

    def test_el_informe_muestra_los_siete_grupos(self):  # FR-LIN-004, SC-LIN-001
        informe = self.reproducir(self.reloj_final // 2).informe()
        self.assertIn(f"Historia t={self.reloj_final // 2}", informe)
        for grupo in ("Tiempo", "Sala", "Vida", "Inventario", "Efectos", "Enemigos", "Mapa conocido"):
            self.assertIn(grupo, informe)

    def test_la_reproduccion_sigue_siendo_fiel_con_hasta(self):  # FR-LIN-008
        resultado = self.reproducir(0)
        self.assertTrue(resultado.fiel)
        self.assertEqual(resultado.acciones_reproducidas, resultado.acciones_en_log)
        self.assertEqual(resultado.desenlace, self.viva.partida.desenlace())

    def test_un_hasta_invalido_se_rechaza_sin_reproducir(self):  # FR-LIN-023
        for invalido in (-1, "5", 1.5, True, [3]):
            with self.subTest(hasta=invalido):
                with self.assertRaises(ValueError) as contexto:
                    self.reproducir(invalido)
                self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_no_modifica_el_log_ni_crea_archivos(self):  # FR-LIN-008
        carpeta = LOG_CON_PERGAMINO.parent
        antes = (LOG_CON_PERGAMINO.read_bytes(), sorted(os.listdir(carpeta)))
        self.reproducir(self.reloj_final)
        self.assertEqual((LOG_CON_PERGAMINO.read_bytes(), sorted(os.listdir(carpeta))), antes)

    def test_un_log_parcial_no_se_consulta(self):  # FR-LIN-008
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "parcial.log"
            ruta.write_text(LOG_CON_PERGAMINO.read_text(encoding="utf-8").replace("}\n", ', "parcial": true}\n', 1),
                            encoding="utf-8")
            resultado = self.reproducir(100, ruta)
        self.assertFalse(resultado.fiel)
        self.assertIsNone(resultado.historia)
        self.assertIsNone(resultado.instante)


class TestReplayHastaConPartidaSencilla(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "partida.log"
        self.original, _, _ = armar()
        self.addCleanup(self.original.cerrar)
        self.original.iniciar_nueva(CRIPTA, 7, str(self.ruta))
        for accion in [A("esperar")] * 3:
            self.assertTrue(self.original.ejecutar(accion).aceptada)

    def reproducir(self, hasta):
        servicio, _, _ = armar()
        return ServicioReplay(servicio).reproducir(str(self.ruta), hasta=hasta)

    def test_el_resumen_coincide_con_historia_en_cada_instante(self):  # FR-LIN-008, SC-LIN-005
        for instante in (0, 50, 100, 150, 299, 300):
            with self.subTest(t=instante):
                resultado = self.reproducir(instante)
                self.assertEqual(resultado.historia, self.original.partida.consultar_instante(instante))

    def test_hasta_despues_del_final_consulta_el_reloj_final(self):  # FR-LIN-009, B-LIN-005
        resultado = self.reproducir(1000)
        self.assertTrue(resultado.termino_antes)
        self.assertEqual(resultado.instante, 300)
        self.assertEqual(resultado.historia, self.original.partida.consultar_instante(300))
        self.assertIn("terminó antes de t=1000", resultado.informe())


class TestReplayHastaEnLaLineaDeComandos(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.datos = Path(carpeta.name)

    def correr(self, *argumentos):
        # main() real sobre las fixtures, con la vista y el controlador sustituidos para comprobar que no se usan
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida), mock.patch.object(principal, "DIRECTORIO_DATOS", self.datos), \
                mock.patch.object(principal, "VistaConsola") as vista, \
                mock.patch.object(principal, "ControladorCripta") as controlador, \
                mock.patch.object(principal, "DIRECTORIO_FIXTURES", str(RAIZ / "fixtures")):
            codigo = principal.main(list(argumentos))
        vista.assert_not_called()
        controlador.assert_not_called()
        return codigo, salida.getvalue()

    def rechazar(self, *argumentos):
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as contexto:
            self.correr(*argumentos)
        return contexto.exception.code, error.getvalue()

    def test_replay_con_hasta_imprime_la_historia_sin_iniciar_la_vista(self):  # FR-LIN-008, SC-LIN-005
        codigo, salida = self.correr("--offline", "--replay", str(LOG_CON_PERGAMINO), "--hasta", "150")
        self.assertEqual(codigo, 0)
        self.assertIn("Historia t=150", salida)
        self.assertNotIn("terminó antes", salida)

    def test_hasta_cero_es_valido(self):  # FR-LIN-008
        codigo, salida = self.correr("--offline", "--replay", str(LOG_CON_PERGAMINO), "--hasta", "0")
        self.assertEqual(codigo, 0)
        self.assertIn("Historia t=0", salida)

    def test_hasta_despues_del_final_indica_el_final_anticipado(self):  # FR-LIN-009, B-LIN-005
        codigo, salida = self.correr("--offline", "--replay", str(LOG_CON_PERGAMINO), "--hasta", "999999")
        self.assertEqual(codigo, 0)
        self.assertIn("terminó antes de t=999999", salida)

    def test_replay_sin_hasta_sigue_igual(self):  # FR-LIN-008
        codigo, salida = self.correr("--offline", "--replay", str(LOG_CON_PERGAMINO))
        self.assertEqual(codigo, 0)
        self.assertNotIn("Historia t=", salida)

    def test_hasta_sin_replay_se_rechaza(self):  # FR-LIN-008
        codigo, error = self.rechazar("--offline", "--hasta", "100")
        motivo = error.split("error:", 1)[-1]      # el uso de argparse también nombra --replay: solo cuenta el motivo
        self.assertEqual(codigo, 2)
        self.assertIn("--hasta", motivo)
        self.assertIn("--replay", motivo)

    def test_un_hasta_invalido_se_rechaza_con_motivo(self):  # FR-LIN-023
        for invalido in ("abc", "-1", "2.5", ""):
            with self.subTest(hasta=invalido):
                codigo, error = self.rechazar("--offline", "--replay", str(LOG_CON_PERGAMINO), "--hasta", invalido)
                motivo = error.split("error:", 1)[-1]
                self.assertEqual(codigo, 2)
                self.assertIn("--hasta", motivo)
                self.assertIn("mayor o igual a 0", motivo)


if __name__ == "__main__":
    unittest.main()
