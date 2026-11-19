"""Pruebas del flujo de resolubilidad en controlador y CLI (FR-RES-013 a 016, 024)."""
import contextlib
import io
import unittest
from types import SimpleNamespace
from unittest import mock

from cripta import __main__ as principal
from cripta.controlador.controlador_cripta import ControladorCripta
from cripta.excepciones import CriptaApiError, CriptaDatosInvalidosError
from tests.servicios.test_servicio_partida import armar, iniciar


class ServicioPartidaFalso:
    def __init__(self, resultado):
        self.resultado_resolubilidad = resultado
        self.inicios = []
        self.cierres = 0
        self.partida = SimpleNamespace(vista=lambda: None, mensajes=lambda: ())

    def listar_criptas(self):
        return (SimpleNamespace(id="cripta-prueba"),)

    def iniciar_nueva(self, cripta_id, semilla, ruta_bitacora):
        self.inicios.append((cripta_id, semilla, ruta_bitacora))

    def cerrar(self):
        self.cierres += 1


class VistaFalsa:
    def __init__(self, opciones=("iniciar", "salir")):
        self.opciones = list(opciones)
        self.reportes = []
        self.ordenes_pedidas = 0

    def pedir_opcion_menu(self):
        return self.opciones.pop(0)

    def elegir_cripta(self, criptas):
        return criptas[0].id

    def mostrar_reporte_resolubilidad(self, resultado, forzada=False):
        self.reportes.append((resultado, forzada))

    def mostrar_estado(self, vista, mensajes):
        pass

    def pedir_orden(self, vista):
        from cripta.controlador.controlador_cripta import Orden
        self.ordenes_pedidas += 1
        return Orden("salir")

    def confirmar(self, pregunta):
        return True


class TestControladorResolubilidad(unittest.TestCase):
    def test_servicio_partida_adjunto_resultado_antes_de_crear_partida(self):  # FR-RES-013
        resultado = SimpleNamespace(es_resoluble=True)
        eventos = []
        servicio, _, _ = armar()
        try:
            with mock.patch("cripta.servicios.servicio_partida.ServicioResolubilidad") as verificador, \
                    mock.patch("cripta.servicios.servicio_partida.Partida") as partida:
                verificador.return_value.verificar.return_value = resultado
                verificador.return_value.verificar.side_effect = lambda _id, **_datos: eventos.append("verificacion") or resultado
                partida.side_effect = lambda *args, **kwargs: (
                    eventos.append("partida") or SimpleNamespace(iniciar=lambda: None)
                )
                servicio.iniciar_nueva("cripta-01", 5)
            self.assertIs(servicio.resultado_resolubilidad, resultado)
            verificador.return_value.verificar.assert_called_once_with("cripta-01", general=mock.ANY, mapa=mock.ANY)
            self.assertEqual(eventos, ["verificacion", "partida"])
        finally:
            servicio.cerrar()

    def test_inicio_resoluble_muestra_reporte_y_arranca(self):  # FR-RES-013
        resultado = SimpleNamespace(es_resoluble=True)
        servicio, vista = ServicioPartidaFalso(resultado), VistaFalsa()
        controlador = ControladorCripta(servicio, vista)
        with mock.patch.object(controlador, "_bucle_principal") as bucle:
            controlador._jugar()
        self.assertEqual(len(vista.reportes), 1)
        self.assertEqual(vista.reportes[0], (resultado, False))
        self.assertEqual(len(servicio.inicios), 1)
        bucle.assert_called_once_with()

    def test_no_resoluble_sin_forzar_aborta_inicio_ApendiceB(self):  # FR-RES-014
        resultado = SimpleNamespace(es_resoluble=False)
        servicio, vista = ServicioPartidaFalso(resultado), VistaFalsa()
        controlador = ControladorCripta(servicio, vista)
        with mock.patch.object(controlador, "_bucle_principal") as bucle:
            controlador._jugar()
        self.assertEqual(vista.reportes, [(resultado, False)])
        self.assertEqual(servicio.inicios, [("cripta-prueba", None, "partida.log")])
        bucle.assert_not_called()

    def test_no_resoluble_con_forzar_muestra_advertencia_y_arranca(self):  # FR-RES-015
        resultado = SimpleNamespace(es_resoluble=False)
        servicio, vista = ServicioPartidaFalso(resultado), VistaFalsa()
        controlador = ControladorCripta(servicio, vista, forzar=True)
        with mock.patch.object(controlador, "_bucle_principal") as bucle:
            controlador._jugar()
        self.assertEqual(vista.reportes, [(resultado, True)])
        bucle.assert_called_once_with()

    def test_verificar_codigo_salida_y_sin_instanciar_vista(self):  # FR-RES-016, FR-RES-024, SC-005
        resultados = (SimpleNamespace(reporte_texto=lambda: "resoluble"),
                      SimpleNamespace(reporte_texto=lambda: "no resoluble"))
        casos = [(resultado, 0) for resultado in resultados]
        casos.extend(((CriptaDatosInvalidosError("esqueleto", "x", "invalido"), 1),
                      (CriptaApiError("red", 500, "falla"), 2)))
        for efecto, esperado in casos:
            with self.subTest(codigo=esperado):
                with mock.patch.object(principal, "ServicioResolubilidad") as servicio_resolubilidad:
                    if isinstance(efecto, Exception):
                        servicio_resolubilidad.return_value.verificar.side_effect = efecto
                    else:
                        servicio_resolubilidad.return_value.verificar.return_value = efecto
                    with mock.patch("cripta.vista.vista_consola.VistaConsola") as vista_consola:
                        salida = io.StringIO()
                        error = io.StringIO()
                        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(error):
                            codigo = principal.main(["--offline", "--verificar", "cripta-prueba"])
                    self.assertEqual(codigo, esperado)
                    vista_consola.assert_not_called()
                    if esperado == 0:
                        self.assertIn(efecto.reporte_texto(), salida.getvalue())
                    else:
                        self.assertTrue(error.getvalue())


if __name__ == "__main__":
    unittest.main()
