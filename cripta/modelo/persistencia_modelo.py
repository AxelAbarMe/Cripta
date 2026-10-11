"""Conversión del modelo vivo a EstadoPartida (guardado, §4.10).

Solo convierte datos: no escribe archivos (eso lo hace GuardadoBinario) y no conoce la
interfaz. La agenda se guarda como EventoGuardado (tipo + sujeto + dos números) porque las
acciones del reloj son funciones y no se pueden escribir en un archivo.
"""
from cripta.constantes import DIRECCIONES
from cripta.estructuras.ordenamiento_selector import ordenar_auto
from cripta.excepciones import CriptaError
from cripta.infraestructura.estado_guardado import (
    EnemigoGuardado,
    EstadoPartida,
    EstadoRNG,
    EventoGuardado,
    JugadorGuardado,
    ObjetoGuardado,
    SalaGuardada,
    TrampaGuardada,
)
from cripta.modelo.enemigo import Enemigo
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.trampa import Trampa

def _jugador_guardado(jugador) -> JugadorGuardado:
    inventario = jugador.inventario
    posicion = inventario.posicion_actual()
    objetos = tuple(
        ObjetoGuardado(
            o.instancia_id,
            o.ficha.id,
            o is inventario.arma_equipada or o is inventario.armadura_equipada,
        )
        for o in inventario.objetos_en_orden()
    )
    return JugadorGuardado(
        vida=jugador.vida,
        vida_max=jugador.vida_max,
        ataque=jugador.ataque_base,
        defensa=jugador.defensa_base,
        velocidad=jugador.velocidad,           # la actual: incluye los efectos de velocidad activos
        sala_actual=jugador.sala_actual,
        tiempo_siguiente=jugador.tiempo_siguiente,
        capacidad_inventario=inventario.capacidad_max,
        indice_cursor=-1 if posicion is None else posicion,
        objetos=objetos,
    )


def _enemigo_guardado(enemigo) -> EnemigoGuardado:
    return EnemigoGuardado(
        enemigo.instancia_id, enemigo.tipo_catalogo, enemigo.vida,
        enemigo.activo, enemigo.sala_actual, enemigo.tiempo_siguiente,
    )


def _sala_guardada(sala, preparada: bool) -> SalaGuardada:
    puertas = sala.puertas
    cerradas = (puertas.norte, puertas.sur, puertas.este, puertas.oeste)
    rastro = -1 if sala.rastro_ultima_visita is None else sala.rastro_ultima_visita
    if not preparada:
        # Una sala cuyo contenido solo se precargó (el jugador nunca llegó a ella) no es estado del
        # juego sino de la caché: al cargar se vuelve a pedir. Pero un enemigo activo que llegó
        # caminando desde otra sala SÍ es estado del juego y no debe perderse.
        activos = tuple(_enemigo_guardado(e) for e in sala.enemigos_activos)
        return SalaGuardada(sala.id, False, cerradas, rastro, (), (), activos)
    trampas = tuple(TrampaGuardada(t.instancia_id, t.tipo_catalogo, t.armada) for t in sala.trampas)
    enemigos = tuple(_enemigo_guardado(e) for e in sala.enemigos_dormidos + sala.enemigos_activos)
    return SalaGuardada(sala.id, True, cerradas, rastro, tuple(sala.objetos_en_suelo), trampas, enemigos)


def _evento_guardado(evento) -> EventoGuardado:
    if evento.datos is None:
        raise CriptaError(f"El evento pendiente '{evento.descripcion}' no se puede guardar: no declara sus datos.")
    tipo, sujeto, a, b = evento.datos
    return EventoGuardado(evento.tiempo, evento.secuencia, tipo, sujeto, a, b)


def crear_estado(*, cripta_id, cripta_version, catalogo_version, semilla, azar, reloj, jugador, mapa,
                 salas_preparadas, acciones_jugador, enemigos_derrotados, mensajes) -> EstadoPartida:
    salas = tuple(_sala_guardada(s, salas_preparadas.contiene(s.id)) for s in mapa.todas_las_salas())
    # Los eventos viajan ordenados por (tiempo, secuencia), así el archivo es el mismo para el mismo estado
    pares = [(e.tiempo, e.secuencia, _evento_guardado(e)) for e in reloj.eventos_vigentes()]
    ordenar_auto(pares)
    return EstadoPartida(
        cripta_id=cripta_id,
        cripta_version=cripta_version,
        catalogo_version=catalogo_version,
        semilla=semilla,
        rng=EstadoRNG.desde_random(azar),
        reloj_actual=reloj.tiempo_actual,
        siguiente_secuencia=reloj.siguiente_secuencia,
        acciones_jugador=acciones_jugador,
        enemigos_derrotados=enemigos_derrotados,
        jugador=_jugador_guardado(jugador),
        salas=salas,
        eventos=tuple(e for _t, _s, e in pares),
        mensajes=tuple(mensajes),
    )
    
    
# ----------------------------------------------------------------------------------------------
# La "vuelta": de EstadoPartida a los objetos del modelo (§4.10). Estas funciones solo reponen
# datos; las acciones de la agenda las recrea Partida, porque son métodos suyos.
# ----------------------------------------------------------------------------------------------
def restaurar_jugador(jugador, guardado, catalogo) -> None:
    jugador.vida_max = guardado.vida_max
    jugador.vida = guardado.vida
    jugador.ataque_base = guardado.ataque
    jugador.defensa_base = guardado.defensa
    jugador.velocidad = guardado.velocidad          # la que tenía al guardar (incluye efectos activos)
    jugador.sala_actual = guardado.sala_actual
    jugador.tiempo_siguiente = guardado.tiempo_siguiente
    inventario = jugador.inventario
    for o in guardado.objetos:                       # vienen en el orden real del inventario
        objeto = ObjetoInventario(o.instancia_id, catalogo.obtener(o.ficha_id))
        inventario.recoger(objeto)
        if o.equipado and objeto.ficha.clase == "arma":
            inventario.arma_equipada = objeto
        elif o.equipado and objeto.ficha.clase == "armadura":
            inventario.armadura_equipada = objeto
    if guardado.indice_cursor >= 0:
        inventario.ir_a_posicion(guardado.indice_cursor)


def restaurar_sala(sala, guardada, precarga, catalogo, enemigos, trampas) -> None:
    """Repone el estado de una sala. `enemigos` y `trampas` son VectorOrdenado por instancia_id:
    se llenan para que la agenda pueda encontrar a quién pertenece cada evento."""
    for direccion, cerrada in zip(DIRECCIONES, guardada.puertas_cerradas):
        if cerrada:
            sala.puertas.cerrar(direccion)
        else:
            sala.puertas.abrir(direccion)
    sala.rastro_ultima_visita = None if guardada.rastro < 0 else guardada.rastro
    if guardada.contenido_cargado:
        precarga.preparar_sala(sala.id)              # contenido y fichas (infraestructura)
        sala.objetos_en_suelo = list(guardada.objetos_suelo)
        sala.trampas = []
        for t in guardada.trampas:
            trampa = Trampa(t.instancia_id, t.tipo)
            trampa.armada = t.armada
            sala.trampas.append(trampa)
            trampas.insertar(trampa)
        sala.enemigos_dormidos.clear()               # los que acaba de crear preparar_sala: manda lo guardado
    for g in guardada.enemigos:
        enemigo = Enemigo(g.instancia_id, catalogo.obtener(g.tipo), g.sala_actual, g.vida)
        enemigo.tiempo_siguiente = g.tiempo_siguiente
        if g.activo:
            enemigo.activar()
            sala.enemigos_activos.append(enemigo)
        else:
            sala.enemigos_dormidos.append(enemigo)
        enemigos.insertar(enemigo)


def siguiente_instancia_tras(inventario) -> int:
    """El contador de ids "i-N" de los objetos recogidos no se guarda: se retoma después del mayor
    id que aún está en el inventario, así un objeto nuevo nunca repite el id de uno existente."""
    mayor = 0
    for objeto in inventario.objetos_en_orden():
        prefijo, _, numero = objeto.instancia_id.partition("-")
        if prefijo == "i" and numero.isdigit():
            mayor = max(mayor, int(numero))
    return mayor