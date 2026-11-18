"""Casos de aceptaci?n de niebla e ir a para los escenarios cubiertos por T013."""
import unittest
from types import SimpleNamespace

from cripta.modelo.accion import Accion
from cripta.infraestructura.estado_guardado import EV_ANTORCHA_APAGAR, EV_TURNO_ACTOR
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.enemigo import Enemigo
from cripta.modelo.trampa import Trampa
from tests.modelo.test_conocimiento_jugador import crear_partida_sintetica, salida

ANTORCHA = SimpleNamespace(id="antorcha-t013", clase="antorcha", nombre="Antorcha", peso=1, valor=1, duracion=2000)


class PruebasAceptacionNiebla(unittest.TestCase):
    """B-NIE-004 y B-NIE-005: FR-NIE-005, FR-NIE-024, SC-NIE-001 y SC-NIE-005."""

    def test_B_NIE_004_antorcha_revela_vecinas_sin_cargar_amenazas(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Vecina", "salidas": {"O": salida(2)}},
        ))
        ficha_enemigo = SimpleNamespace(
            id="enemigo-t013", nombre="Guardián", vida_max=10, ataque=1, defensa=0,
            velocidad=100, comportamiento="guardián", suelta=(), rango=None,
        )
        enemigo = Enemigo("enemigo-dormido", ficha_enemigo, 3)
        trampa = Trampa("trampa-vecina", "trp_dardos")
        vecina_objetivo = partida._mapa.obtener(3)
        vecina_objetivo.enemigos_dormidos.append(enemigo)
        vecina_objetivo.trampas.append(trampa)
        partida._jugador.inventario.recoger(ObjetoInventario("antorcha-t013", ANTORCHA))
        self.assertTrue(partida.ejecutar_accion(Accion("usar", 0)).aceptada)
        vida_previa = partida._jugador.vida
        self.assertTrue(any(evento.datos and evento.datos[0] == EV_ANTORCHA_APAGAR
                            for evento in partida._reloj.eventos_vigentes()))

        resultado = partida.ejecutar_accion(Accion("mover", "E"))

        self.assertTrue(resultado.aceptada)
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "explorada")
        self.assertFalse(vecina_objetivo.contenido_cargado)
        self.assertEqual(vecina_objetivo.enemigos_dormidos, [enemigo])
        self.assertEqual(vecina_objetivo.enemigos_activos, [])
        self.assertEqual(vecina_objetivo.trampas, [trampa])
        self.assertFalse(enemigo.activo)
        self.assertIsNone(enemigo.evento_pendiente)
        self.assertFalse(any(evento.datos and evento.datos[0] == EV_TURNO_ACTOR and evento.datos[1] == enemigo.instancia_id
                             for evento in partida._reloj.eventos_vigentes()))
        self.assertTrue(trampa.armada)
        self.assertEqual(partida._jugador.vida, vida_previa)

    def test_B_NIE_005_pergamino_revierte_entrada_y_revelacion_por_antorcha(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Inicio", "salidas": {"E": salida(2)}},
            {"id": 2, "nombre": "Centro", "salidas": {"O": salida(1), "E": salida(3)}},
            {"id": 3, "nombre": "Vecina", "salidas": {"O": salida(2)}},
        ))
        partida._jugador.inventario.recoger(ObjetoInventario("antorcha-t013", ANTORCHA))
        partida._jugador.inventario.recoger(ObjetoInventario(
            "pergamino-1", SimpleNamespace(clase="pergamino_retroceso")
        ))
        self.assertTrue(partida.ejecutar_accion(Accion("usar", 0)).aceptada)
        previo = partida._conocimiento.proyectar()

        partida.ejecutar_accion(Accion("mover", "E"))
        self.assertEqual(partida._conocimiento.estado_de_sala(3), "explorada")
        partida.ejecutar_accion(Accion("pergamino"))

        self.assertEqual(partida._jugador.sala_actual, 1)
        self.assertEqual(partida._conocimiento.proyectar(), previo)


if __name__ == "__main__":
    unittest.main()
