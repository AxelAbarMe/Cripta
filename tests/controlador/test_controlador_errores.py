'''Comprueba que un error de red (por ejemplo un 429 persistente) no cierra el juego: se muestra y se vuelve al menú.
Usa un servicio y una vista falsos; no necesita red ni pantalla.
Ejecutar: python -m unittest tests.controlador.test_controlador_errores
'''
import tempfile
import unittest
from pathlib import Path

from cripta.controlador.controlador_cripta import ControladorCripta, Orden
from cripta.excepciones import CriptaApiError
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.partida_log import LectorBitacoraPartida
from cripta.servicios.servicio_partida import ServicioPartida


class ServicioFalso:
    # Solo lo que usa el controlador al listar criptas y cerrar.
    def listar_criptas(self):
        raise CriptaApiError("listar criptas", 429, "el servidor sigue limitando la frecuencia")

    def cerrar(self):
        self.cerrado = True


class VistaFalsa:
    # Elige "iniciar" una vez y luego "salir"; guarda los errores mostrados.
    def __init__(self):
        self.opciones = ["iniciar", "salir"]
        self.errores = []

    def pedir_opcion_menu(self):
        return self.opciones.pop(0)

    def mostrar_error(self, texto):
        self.errores.append(texto)


class TestControladorErrores(unittest.TestCase):
    def test_error_de_red_al_iniciar_se_muestra_y_vuelve_al_menu(self):
        servicio, vista = ServicioFalso(), VistaFalsa()
        ControladorCripta(servicio, vista).ejecutar()      # no debe lanzar excepción
        self.assertEqual(len(vista.errores), 1)
        self.assertIn("HTTP 429", vista.errores[0])
        self.assertEqual(vista.opciones, [])               # siguió al menú y salió normalmente
        self.assertTrue(servicio.cerrado)


class VistaDeDesplazamientos:
    # Entrega las órdenes del guion y, antes de cada una, fotografía el estado observable de la partida
    def __init__(self, servicio, ruta_bitacora, ordenes):
        self.servicio, self.ruta_bitacora, self.ordenes = servicio, ruta_bitacora, list(ordenes)
        self.fotos, self.avisos, self.errores = [], [], []
        self.opciones = ["iniciar", "salir"]

    def pedir_opcion_menu(self):
        return self.opciones.pop(0)

    def elegir_cripta(self, criptas):
        return criptas[0].id

    def mostrar_estado(self, vista, mensajes):
        pass

    def pedir_orden(self, vista):
        partida = self.servicio.partida
        self.fotos.append((vista, partida.mensajes(), len(partida._historial), partida.puntaje(),
                           Path(self.ruta_bitacora).read_bytes()))
        return self.ordenes.pop(0)

    def mostrar_aviso(self, texto):
        self.avisos.append(texto)

    def mostrar_error(self, texto):
        self.errores.append(texto)

    def confirmar(self, pregunta):
        return True


class TestDesplazamientoRechazado(unittest.TestCase):
    def test_desplazamiento_rechazado_avisa_y_no_cambia_nada(self):  # FR-TER-023
        # Desde la sala 1 se avanza al norte. En la sala 2 la salida E tiene la puerta cerrada y no hay salida O.
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = str(Path(carpeta) / "partida.log")
            servicio = ServicioPartida(ClienteGeneral(ClienteOffline("tests/datos")), ContadorSolicitudes(),
                                       asincrono=False)
            guion = [Orden("mover", "N"), Orden("mover", "E"), Orden("mover", "O"), Orden("salir")]
            vista = VistaDeDesplazamientos(servicio, ruta, guion)
            ControladorCripta(servicio, vista, ruta_bitacora=ruta, semilla=5).ejecutar()

            self.assertEqual(vista.errores, [])
            self.assertEqual(len(vista.fotos), 4)
            antes, tras_puerta, tras_sin_salida = vista.fotos[1], vista.fotos[2], vista.fotos[3]
            # (a) un mensaje descriptivo por cada rechazo
            self.assertEqual(len(vista.avisos), 2)
            self.assertIn("cerrada", vista.avisos[0])
            self.assertIn("No hay salida", vista.avisos[1])
            for despues in (tras_puerta, tras_sin_salida):
                # (b) el reloj virtual no avanza y (c) no cambian el estado del juego ni el historial de retroceso
                self.assertEqual(despues[0].tiempo, antes[0].tiempo)
                self.assertEqual(despues[0], antes[0])
                self.assertEqual(despues[2], antes[2])
                self.assertEqual(despues[3], antes[3])
                # (d) la bitácora no recibe ninguna línea
                self.assertEqual(despues[4], antes[4])
            encabezado, anotadas = LectorBitacoraPartida(ruta).leer()
            self.assertEqual([a["tipo"] for a in anotadas], ["mover"])
            self.assertEqual(anotadas[0]["direccion"], "N")


if __name__ == "__main__":
    unittest.main()