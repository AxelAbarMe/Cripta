"""Pruebas de desde_estado_guardado (J9, etapa 2: de EstadoPartida a la partida viva), con la cripta real de fixtures/.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.modelo.test_guardado_vuelta -v
"""
import dataclasses
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as N

from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.guardado_binario import GuardadoBinario
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.efectos import EfectoCambioVelocidad, EfectoVeneno
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga

VERSION_CATALOGO = "cat-prueba"
PERGAMINO = N(id="itm_pergamino", clase="pergamino_retroceso", nombre="Pergamino de retroceso", peso=1, valor=1)


def armar_mundo():
    """Objetos nuevos y vacíos de partida: es lo que tendría quien carga un guardado en otra ejecución."""
    cliente = ClienteOffline("fixtures")
    general = cliente.obtener_general("cripta-01")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "cripta-01", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(general.paginas)
    obtener = catalogo.obtener
    catalogo.obtener = lambda id_: PERGAMINO if id_ == PERGAMINO.id else obtener(id_)   # cripta-01 no trae pergaminos
    return general, mapa, catalogo, precarga


def crear_partida(semilla=5, pergaminos=0):
    general, mapa, catalogo, precarga = armar_mundo()
    partida = Partida(general, mapa, catalogo, precarga, semilla)
    partida._jugador.vida_max = partida._jugador.vida = 1000   # para que las ratas no maten durante la prueba
    for k in range(pergaminos):
        partida._jugador.inventario.recoger(ObjetoInventario(f"p{k}", PERGAMINO))
    partida.iniciar()
    return partida


def cargar(estado):
    general, mapa, catalogo, precarga = armar_mundo()
    return Partida.desde_estado_guardado(estado, general, mapa, catalogo, precarga)


def jugar(partida, acciones):
    for accion in acciones:
        partida.ejecutar_accion(accion)


def foto(partida):
    """Todo lo observable de una partida: su estado completo, su vista y sus mensajes."""
    return partida.a_estado_guardado(VERSION_CATALOGO), partida.vista(), partida.mensajes()


class PruebaGuardadoVuelta(unittest.TestCase):
    def test_ida_y_vuelta_deja_la_misma_partida(self):
        p = crear_partida(semilla=11)
        jugar(p, [A("mover", "N"), A("esperar"), A("atacar", "e-201"), A("esperar")])
        estado = p.a_estado_guardado(VERSION_CATALOGO)
        b = cargar(estado)
        self.assertEqual(foto(b), foto(p))
        self.assertEqual(b.puntaje(), p.puntaje())

    def test_continuar_una_partida_cargada_da_lo_mismo_que_no_haberla_guardado(self):
        p = crear_partida(semilla=3)
        jugar(p, [A("mover", "N"), A("esperar"), A("atacar", "e-201")])
        b = cargar(p.a_estado_guardado(VERSION_CATALOGO))
        continuacion = [A("atacar", "e-202"), A("esperar"), A("atacar", "e-202"), A("mover", "S"), A("esperar")]
        jugar(p, continuacion)
        jugar(b, continuacion)
        self.assertEqual(foto(b), foto(p))

    def test_por_el_archivo_binario(self):
        p = crear_partida(semilla=7)
        jugar(p, [A("recoger", "itm_antorcha"), A("usar", 0), A("mover", "N"), A("esperar")])
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "partida.bin"
            GuardadoBinario().guardar(ruta, p.a_estado_guardado(VERSION_CATALOGO))
            b = cargar(GuardadoBinario().cargar(ruta))
        self.assertEqual(foto(b), foto(p))
        continuacion = [A("esperar")] * 20          # la antorcha (2000) se apaga a los 2000: aquí aún no
        jugar(p, continuacion)
        jugar(b, continuacion)
        self.assertEqual(foto(b), foto(p))

    def test_antorcha_trampa_y_puerta_con_cierre_automatico_siguen_pendientes(self):
        p = crear_partida(semilla=5)
        jugar(p, [A("recoger", "itm_antorcha"), A("usar", 0), A("mover", "N")])
        p._jugador.inventario.recoger(ObjetoInventario("k1", p._catalogo.obtener("itm_llave_bronce")))
        jugar(p, [A("abrir", "E")])
        b = cargar(p.a_estado_guardado(VERSION_CATALOGO))
        self.assertEqual(foto(b), foto(p))
        self.assertIn("Antorcha", b.vista().efectos_activos)
        continuacion = [A("mover", "E")] + [A("esperar")] * 6
        jugar(p, continuacion)
        jugar(b, continuacion)
        self.assertEqual(foto(b), foto(p))
        self.assertTrue([m for m in b.mensajes() if "cierra sola" in m])     # el cierre automático ocurrió tras cargar

    def test_enemigo_que_camino_a_una_sala_sin_visitar_no_se_pierde(self):
        p = crear_partida(semilla=1)
        jugar(p, [A("mover", "N")])
        enemigo = p._mapa.obtener(2).enemigos_activos[0]
        p._mover_enemigo(enemigo, "N")               # sale a la sala 3, que el jugador nunca pisó
        self.assertFalse(p._salas_preparadas.contiene(3))
        b = cargar(p.a_estado_guardado(VERSION_CATALOGO))
        self.assertEqual([e.instancia_id for e in b._mapa.obtener(3).enemigos_activos], [enemigo.instancia_id])
        continuacion = [A("esperar")] * 6
        jugar(p, continuacion)
        jugar(b, continuacion)
        self.assertEqual(foto(b), foto(p))

    def test_veneno_y_cambio_de_velocidad_activos(self):
        p = crear_partida(semilla=2)
        EfectoVeneno(p._reloj, p._jugador, 2).iniciar()
        EfectoCambioVelocidad(p._reloj, p._jugador, 50, 300).aplicar()
        jugar(p, [A("esperar"), A("esperar")])
        estado = p.a_estado_guardado(VERSION_CATALOGO)
        self.assertEqual(sorted(e.tipo for e in estado.eventos), [1, 3])   # un pulso de veneno y el fin de velocidad
        b = cargar(estado)
        self.assertIsNotNone(b._jugador.veneno_activo)
        self.assertEqual(foto(b), foto(p))
        continuacion = [A("esperar")] * 8            # pasan los pulsos y termina el efecto de velocidad
        jugar(p, continuacion)
        jugar(b, continuacion)
        self.assertEqual(foto(b), foto(p))
        self.assertEqual(b.vista().velocidad, 100)

    def test_el_pergamino_no_deshace_lo_anterior_al_guardado_pero_si_lo_posterior(self):
        p = crear_partida(pergaminos=2)
        jugar(p, [A("esperar"), A("esperar")])
        estado = p.a_estado_guardado(VERSION_CATALOGO)
        b = cargar(estado)
        r = b.ejecutar_accion(A("pergamino"))
        self.assertFalse(r.aceptada)                  # historial vacío tras cargar
        self.assertEqual(b.vista().pergaminos, 2)
        jugar(b, [A("mover", "N")])
        self.assertTrue(b.ejecutar_accion(A("pergamino")).aceptada)
        despues = b.a_estado_guardado(VERSION_CATALOGO)

        def juego(e):   # lo que es estado del juego (que una sala tenga su contenido cargado es infraestructura)
            return (e.reloj_actual, e.rng, e.eventos, e.jugador.vida, e.jugador.sala_actual,
                    [(s.sala_id, s.rastro, s.puertas_cerradas) for s in e.salas])
        self.assertEqual(juego(despues), juego(estado))

    def test_una_cripta_distinta_se_rechaza(self):
        estado = crear_partida().a_estado_guardado(VERSION_CATALOGO)
        general, mapa, catalogo, precarga = armar_mundo()
        otra = dataclasses.replace(general, version="otra-version")
        with self.assertRaises(CriptaFormatoIncompatibleError):
            Partida.desde_estado_guardado(estado, otra, mapa, catalogo, precarga)


if __name__ == "__main__":
    unittest.main()