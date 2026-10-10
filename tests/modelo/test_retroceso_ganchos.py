"""Pruebas de los ganchos de retroceso: cada objeto del modelo registra cómo deshacer sus cambios.

Se ejecuta con:  python -m unittest tests.modelo.test_retroceso_ganchos -v
"""
import unittest
from types import SimpleNamespace as N

from cripta.dto.sala_dto import SalaDTO
from cripta.modelo.actor import Actor
from cripta.modelo.historial_retroceso import HistorialRetroceso
from cripta.modelo.inventario import Inventario, ObjetoInventario
from cripta.modelo.reloj import RelojEventos
from cripta.modelo.sala import Sala
from cripta.modelo.trampa import Trampa


def _ficha(id_catalogo, clase):
    return N(id=id_catalogo, clase=clase, nombre=id_catalogo, peso=1, valor=1)


class PruebaGanchosDeRetroceso(unittest.TestCase):
    def test_reloj_restaura_tiempo_secuencia_y_eventos(self):
        historial, reloj = HistorialRetroceso(), RelojEventos()
        reloj.registrador = historial.registrar_cambio
        nada = lambda: None
        reloj.programar(10, nada)
        e2 = reloj.programar(20, nada)
        historial.iniciar_intervalo()
        reloj.ejecutar_siguiente()
        reloj.programar(30, nada)
        reloj.cancelar(e2)
        historial.cerrar_intervalo()
        self.assertEqual((reloj.tiempo_actual, reloj.siguiente_secuencia), (10, 3))
        historial.deshacer_ultimo_intervalo()
        self.assertEqual((reloj.tiempo_actual, reloj.siguiente_secuencia), (0, 2))
        reloj.ejecutar_siguiente()
        self.assertEqual(reloj.tiempo_actual, 10)    # el evento ejecutado volvió a la agenda
        reloj.ejecutar_siguiente()
        self.assertEqual(reloj.tiempo_actual, 20)    # el evento cancelado volvió a la agenda
        self.assertTrue(reloj.esta_vacia())          # el evento programado en el intervalo desapareció

    def test_actor_trampa_puertas_y_sala(self):
        historial = HistorialRetroceso()
        actor = Actor("x", 30, 5, 2, 100, 1)
        trampa = Trampa("t1", "trp")
        sala = Sala(SalaDTO.desde_json({"id": 1, "nombre": "A", "salidas": {"N": {"sala": 2, "cerrada": True, "llave": "k"}}}))
        for objeto in (actor, trampa, sala, sala.puertas):
            objeto.registrador = historial.registrar_cambio
        sala.objetos_en_suelo = ["a", "b"]
        sala.enemigos_dormidos = ["e1", "e2"]
        historial.iniciar_intervalo()
        actor.recibir_daño(10)
        actor.recibir_daño(5)
        actor.sala_actual = 7
        trampa.desarmar()
        sala.puertas.abrir("N")
        sala.marcar_visita(50)
        sala.quitar_objeto("a")
        sala.agregar_objeto("c")
        sala.activar_enemigos_dormidos()
        historial.cerrar_intervalo()
        self.assertEqual((actor.vida, actor.sala_actual, trampa.armada), (15, 7, False))
        historial.deshacer_ultimo_intervalo()
        self.assertEqual((actor.vida, actor.sala_actual, trampa.armada), (30, 1, True))
        self.assertTrue(sala.puertas.esta_cerrada("N"))
        self.assertIsNone(sala.rastro_ultima_visita)
        self.assertEqual(sala.objetos_en_suelo, ["a", "b"])
        self.assertEqual((sala.enemigos_dormidos, sala.enemigos_activos), (["e1", "e2"], []))

    def _inventario(self, historial, clases):
        inventario = Inventario(6)
        inventario.registrador = historial.registrar_cambio
        for k, (id_catalogo, clase) in enumerate(clases):
            inventario.recoger(ObjetoInventario(f"o{k}", _ficha(id_catalogo, clase)))
        return inventario

    @staticmethod
    def _orden(inventario):
        return [o.ficha.id for o in inventario.vista_ordenada("peso")]   # pesos iguales: queda el orden real

    def test_inventario_deshace_recoger_equipar_y_soltar(self):
        historial = HistorialRetroceso()
        inv = self._inventario(historial, [("a1", "arma"), ("p1", "pocion"), ("ar1", "armadura"), ("p2", "pocion")])
        historial.iniciar_intervalo()
        inv.recoger(ObjetoInventario("o9", _ficha("x1", "pocion")))
        inv.ir_a_posicion(2)
        inv.equipar_actual()
        inv.ir_a_posicion(3)
        inv.soltar_actual()
        inv.ir_a_posicion(1)
        inv.soltar_actual()
        inv.recoger(ObjetoInventario("o10", _ficha("y1", "pocion")))
        inv.soltar_actual()
        historial.cerrar_intervalo()
        self.assertEqual(self._orden(inv), ["ar1", "p1", "x1"])
        historial.deshacer_ultimo_intervalo()
        self.assertEqual(self._orden(inv), ["a1", "p1", "ar1", "p2"])
        self.assertEqual((inv.arma_equipada, inv.armadura_equipada, len(inv)), (None, None, 4))

    def test_inventario_restaura_el_equipo_de_un_objeto_soltado(self):
        historial = HistorialRetroceso()
        inv = self._inventario(historial, [("p1", "pocion"), ("a1", "arma"), ("p2", "pocion")])
        inv.ir_a_posicion(1)
        inv.equipar_actual()
        historial.iniciar_intervalo()
        inv.ir_a_posicion(0)
        inv.soltar_actual()          # suelta el arma equipada (quedó al frente)
        historial.cerrar_intervalo()
        self.assertIsNone(inv.arma_equipada)
        historial.deshacer_ultimo_intervalo()
        self.assertEqual(self._orden(inv), ["a1", "p1", "p2"])
        self.assertEqual(inv.arma_equipada.ficha.id, "a1")

    def test_historial_ignora_cambios_fuera_de_intervalo_y_en_pausa(self):
        historial, actor = HistorialRetroceso(), Actor("x", 30, 5, 2, 100, 1)
        actor.registrador = historial.registrar_cambio
        actor.recibir_daño(5)                       # sin intervalo abierto: no es un error y no se registra
        historial.iniciar_intervalo()
        with historial.sin_registrar():
            actor.recibir_daño(5)                   # en pausa: no se registra
        actor.recibir_daño(5)
        historial.cerrar_intervalo()
        historial.deshacer_ultimo_intervalo()
        self.assertEqual(actor.vida, 20)            # solo se revirtió el último daño


if __name__ == "__main__":
    unittest.main()