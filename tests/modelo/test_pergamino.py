"""Pruebas del retroceso con el pergamino (J8b), con la cripta real de fixtures/.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.modelo.test_pergamino -v
"""
import unittest
from types import SimpleNamespace as N

from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga

PERGAMINO = N(id="itm_pergamino", clase="pergamino_retroceso", nombre="Pergamino de retroceso", peso=1, valor=1)


def crear_partida(pergaminos=1, semilla=5, suelo_pergamino=False):
    cliente = ClienteOffline("fixtures")
    general = cliente.obtener_general("cripta-01")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "cripta-01", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(general.paginas)
    obtener = catalogo.obtener
    catalogo.obtener = lambda id_: PERGAMINO if id_ == PERGAMINO.id else obtener(id_)   # el pergamino no existe en cripta-01
    partida = Partida(general, mapa, catalogo, precarga, semilla)
    for k in range(pergaminos):
        partida._jugador.inventario.recoger(ObjetoInventario(f"p{k}", PERGAMINO))
    partida.iniciar()
    if suelo_pergamino:   # después de iniciar: al cargar el contenido de la sala el suelo se reemplaza
        mapa.obtener(1).agregar_objeto(PERGAMINO.id)
    return partida, mapa


class PruebaPergamino(unittest.TestCase):
    def test_deshace_un_movimiento_con_trampa_y_ataques(self):
        p, mapa = crear_partida()
        p.ejecutar_accion(A("mover", "N"))
        self.assertLess(p.vista().vida, 30)
        self.assertEqual(len(p.vista().enemigos), 2)
        r = p.ejecutar_accion(A("pergamino"))
        v = p.vista()
        self.assertTrue(r.aceptada)
        self.assertEqual((v.sala_id, v.vida, v.tiempo, v.pergaminos, v.retrocesos_posibles), (1, 30, 0, 0, 0))
        sala2 = mapa.obtener(2)
        self.assertEqual((len(sala2.enemigos_dormidos), len(sala2.enemigos_activos)), (2, 0))
        self.assertTrue(sala2.trampas[0].armada)
        self.assertIsNone(sala2.rastro_ultima_visita)
        self.assertEqual(p.puntaje().acciones_jugador, 0)

    def test_repetir_la_accion_da_el_mismo_resultado(self):
        p, _ = crear_partida()
        primero = p.ejecutar_accion(A("mover", "N")).mensajes
        p.ejecutar_accion(A("pergamino"))
        segundo = p.ejecutar_accion(A("mover", "N")).mensajes
        self.assertEqual(primero, segundo)   # el azar también se restaura: no se puede "volver a tirar"

    def test_dos_pergaminos_seguidos_retroceden_dos_acciones(self):
        p, _ = crear_partida(pergaminos=2)
        for _ in range(3):
            p.ejecutar_accion(A("esperar"))
        self.assertEqual(p.vista().tiempo, 300)
        p.ejecutar_accion(A("pergamino"))
        self.assertEqual(p.vista().tiempo, 200)
        p.ejecutar_accion(A("pergamino"))
        self.assertEqual((p.vista().tiempo, p.puntaje().acciones_jugador, p.vista().pergaminos), (100, 1, 0))

    def test_nunca_mas_de_cinco_acciones_hacia_atras(self):
        p, _ = crear_partida(pergaminos=6)
        for _ in range(7):
            p.ejecutar_accion(A("esperar"))
        resultados = [p.ejecutar_accion(A("pergamino")) for _ in range(6)]
        self.assertEqual([r.aceptada for r in resultados], [True] * 5 + [False])
        self.assertEqual((p.vista().tiempo, p.vista().pergaminos), (200, 1))

    def test_sin_pergamino_o_sin_historial_se_rechaza_sin_gastar_tiempo(self):
        p, _ = crear_partida(pergaminos=0)
        p.ejecutar_accion(A("esperar"))
        r = p.ejecutar_accion(A("pergamino"))
        self.assertFalse(r.aceptada)
        self.assertEqual(r.tiempo, 100)
        p2, _ = crear_partida(pergaminos=1)
        r = p2.ejecutar_accion(A("pergamino"))
        self.assertFalse(r.aceptada)
        self.assertEqual(p2.vista().pergaminos, 1)   # no se consumió

    def test_una_accion_rechazada_no_deja_nada_que_deshacer(self):
        p, _ = crear_partida()
        p.ejecutar_accion(A("esperar"))
        self.assertFalse(p.ejecutar_accion(A("mover", "S")).aceptada)   # sala 1 no tiene salida al sur
        p.ejecutar_accion(A("pergamino"))
        self.assertEqual((p.vista().tiempo, p.puntaje().acciones_jugador), (0, 0))   # deshizo la espera, no la rechazada

    def test_los_objetos_vuelven_al_suelo_y_salen_del_inventario(self):
        p, _ = crear_partida()
        p.ejecutar_accion(A("recoger", "itm_antorcha"))
        self.assertEqual(p.vista().objetos_suelo, ())
        p.ejecutar_accion(A("pergamino"))
        v = p.vista()
        self.assertEqual([o.ficha_id for o in v.objetos_suelo], ["itm_antorcha"])
        self.assertEqual(v.inventario_cantidad, 0)

    def test_un_pergamino_recogido_en_el_intervalo_no_se_devuelve_al_suelo(self):
        p, mapa = crear_partida(pergaminos=1, suelo_pergamino=True)
        p.ejecutar_accion(A("recoger", PERGAMINO.id))
        self.assertEqual(p.vista().pergaminos, 2)
        p.ejecutar_accion(A("pergamino"))
        v = p.vista()
        self.assertEqual(v.pergaminos, 1)                                   # 2 al invocar, menos el usado
        self.assertNotIn(PERGAMINO.id, [o.ficha_id for o in v.objetos_suelo])   # y no vuelve al suelo
        self.assertEqual(v.tiempo, 0)                                       # lo demás sí se deshizo

    def test_un_pergamino_soltado_en_el_intervalo_no_vuelve_al_inventario(self):
        p, _ = crear_partida(pergaminos=2)
        p.ejecutar_accion(A("soltar", 0))
        self.assertEqual(p.vista().pergaminos, 1)
        p.ejecutar_accion(A("pergamino"))
        self.assertEqual(p.vista().pergaminos, 0)    # 1 al invocar, menos el usado
        self.assertIn(PERGAMINO.id, [o.ficha_id for o in p.vista().objetos_suelo])


if __name__ == "__main__":
    unittest.main()