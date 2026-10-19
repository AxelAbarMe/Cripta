'''Comprueba que un error de red (por ejemplo un 429 persistente) no cierra el juego: se muestra y se vuelve al menú.
Usa un servicio y una vista falsos; no necesita red ni pantalla.
Ejecutar: python -m unittest tests.controlador.test_controlador_errores
'''
import unittest

from cripta.controlador.controlador_cripta import ControladorCripta
from cripta.excepciones import CriptaApiError


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


if __name__ == "__main__":
    unittest.main()