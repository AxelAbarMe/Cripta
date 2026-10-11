"""Conversión del modelo vivo a EstadoPartida (guardado, §4.10).

Solo convierte datos: no escribe archivos (eso lo hace GuardadoBinario) y no conoce la
interfaz. La agenda se guarda como EventoGuardado (tipo + sujeto + dos números) porque las
acciones del reloj son funciones y no se pueden escribir en un archivo.
"""
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
        # juego sino de la caché: al cargar se vuelve a pedir, así no se pierden sus enemigos sin crear.
        return SalaGuardada(sala.id, False, cerradas, rastro, (), (), ())
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