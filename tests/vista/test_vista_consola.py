"""Pruebas de VistaConsola con entrada y salida simuladas.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.vista.test_vista_consola -v
"""
import unittest

from cripta.controlador.controlador_cripta import Orden
from cripta.vista.vista_consola import ANCHO, VistaConsola, _caja_mensajes


def crear(*respuestas):
    """Devuelve (vista, salida): `respuestas` se entregan una por una; al acabarse simula Ctrl+D."""
    pendientes, salida = list(respuestas), []

    def entrada(_indicador):
        if not pendientes:
            raise EOFError
        return pendientes.pop(0)
    return VistaConsola(entrada, salida.append), salida


class TestComandos(unittest.TestCase):
    def interpretar(self, texto):
        vista, _ = crear(texto)
        return vista.pedir_orden(None)

    def test_direcciones_en_una_letra_o_con_mover(self):
        self.assertEqual(self.interpretar("n"), Orden("mover", "N"))
        self.assertEqual(self.interpretar("MOVER o"), Orden("mover", "O"))

    def test_abrir_lleva_la_direccion(self):
        self.assertEqual(self.interpretar("abrir e"), Orden("abrir", "E"))

    def test_las_posiciones_se_muestran_desde_1_y_se_envian_desde_0(self):
        self.assertEqual(self.interpretar("atacar 1"), Orden("atacar", 0))
        self.assertEqual(self.interpretar("recoger 3"), Orden("recoger", 2))

    def test_ordenar_solo_acepta_los_criterios_validos(self):
        self.assertEqual(self.interpretar("ordenar valor"), Orden("ordenar", "valor"))
        vista, salida = crear("ordenar color", "esperar")
        self.assertEqual(vista.pedir_orden(None), Orden("esperar"))
        self.assertTrue(any("no reconocido" in linea for linea in salida))

    def test_comandos_sin_argumento_y_cursor_del_inventario(self):
        for texto in ("esperar", "usar", "equipar", "soltar", "guardar", "cargar", "salir"):
            self.assertEqual(self.interpretar(texto), Orden(texto))
        self.assertEqual(self.interpretar("sig"), Orden("siguiente"))
        self.assertEqual(self.interpretar("ant"), Orden("anterior"))

    def test_pergamino_admite_de_1_a_5(self):
        self.assertEqual(self.interpretar("pergamino"), Orden("pergamino", 1))
        self.assertEqual(self.interpretar("pergamino 5"), Orden("pergamino", 5))
        vista, _ = crear("pergamino 6", "pergamino 0", "esperar")
        self.assertEqual(vista.pedir_orden(None), Orden("esperar"))

    def test_comando_invalido_se_repite_hasta_recibir_uno_valido(self):
        vista, salida = crear("", "xyz", "atacar", "atacar x", "s")
        self.assertEqual(vista.pedir_orden(None), Orden("mover", "S"))
        self.assertEqual(sum("no reconocido" in linea for linea in salida), 4)

    def test_fin_de_entrada_equivale_a_salir(self):
        vista, _ = crear()
        self.assertEqual(vista.pedir_orden(None), Orden("salir"))

    def test_confirmar_acepta_s_si_y_rechaza_lo_demas(self):
        for texto, esperado in (("s", True), ("SI", True), ("sí", True), ("n", False), ("", False)):
            vista, _ = crear(texto)
            self.assertEqual(vista.confirmar("¿Seguro?"), esperado, texto)
        vista, _ = crear()
        self.assertFalse(vista.confirmar("¿Seguro?"))


class TestMenuYCripta(unittest.TestCase):
    def test_elegir_cripta_devuelve_el_id_o_none(self):
        from types import SimpleNamespace as N
        criptas = (N(id="c-1", nombre="Uno", salas=20, dificultad=1), N(id="c-2", nombre="Dos", salas=60, dificultad=2))
        vista, _ = crear("2")
        self.assertEqual(vista.elegir_cripta(criptas), "c-2")
        vista, _ = crear("9", "abc", "1")
        self.assertEqual(vista.elegir_cripta(criptas), "c-1")
        vista, _ = crear("0")
        self.assertIsNone(vista.elegir_cripta(criptas))
        vista, _ = crear()
        self.assertIsNone(vista.elegir_cripta(criptas))


class TestCajaDeMensajes(unittest.TestCase):
    MENSAJES = ("Entras a Sala 2.", "Recoges Llave de bronce.", "Equipas Daga oxidada.")

    def test_cada_mensaje_lleva_su_indice_desde_1(self):
        texto = "\n".join(_caja_mensajes(self.MENSAJES))
        for numero, mensaje in enumerate(self.MENSAJES, start=1):
            self.assertIn(f"{numero}. {mensaje}", texto)

    def test_con_20_mensajes_van_del_1_al_20_en_orden(self):
        mensajes = tuple(f"Mensaje {k}" for k in range(1, 21))
        texto = "\n".join(_caja_mensajes(mensajes))
        for k in range(1, 21):
            self.assertIn(f"{k}. Mensaje {k}", texto)

    def test_la_caja_conserva_el_ancho_fijo(self):
        mensajes = tuple("texto largo " * 12 for _ in range(20))
        for linea in _caja_mensajes(mensajes):
            self.assertEqual(len(linea), ANCHO)

    def test_un_mensaje_largo_se_ajusta_con_sangria_del_tamano_de_su_indice(self):
        lineas = _caja_mensajes(("palabra " * 20,))
        self.assertTrue(any(l.startswith("|    palabra") for l in lineas))     # sangría de 3 ("1. ")

    def test_sin_mensajes(self):
        self.assertIn("(sin mensajes)", "\n".join(_caja_mensajes(())))


if __name__ == "__main__":
    unittest.main()