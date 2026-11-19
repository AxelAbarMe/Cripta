"""Conversión del modelo vivo a EstadoPartida (guardado, §4.10).

Solo convierte datos: no escribe archivos (eso lo hace GuardadoBinario) y no conoce la
interfaz. La agenda se guarda como EventoGuardado (tipo + sujeto + dos números) porque las
acciones del reloj son funciones y no se pueden escribir en un archivo.
"""
from types import SimpleNamespace

from cripta.constantes import DIRECCIONES
from cripta.estructuras.ordenamiento_selector import ordenar_auto
from cripta.estructuras.vector import VectorOrdenado
from cripta.excepciones import CriptaError, CriptaFormatoIncompatibleError
from cripta.infraestructura.estado_guardado import (
    AccionGuardada,
    AjusteGuardado,
    ContenidoSalaGuardado,
    EnemigoGuardado,
    ConocimientoGuardado,
    EstadoPartida,
    EstadoRNG,
    EventoGuardado,
    JugadorGuardado,
    LineaGuardada,
    ObjetoGuardado,
    PuntoControlGuardado,
    SalaGuardada,
    TrampaGuardada,
)
from cripta.modelo.accion import Accion
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.linea_tiempo import LineaTiempo
from cripta.modelo.enemigo import Enemigo
from cripta.modelo.conocimiento_jugador import ConocimientoJugador
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


def puertas_cerradas(sala) -> tuple[bool, bool, bool, bool]:
    puertas = sala.puertas
    return (puertas.norte, puertas.sur, puertas.este, puertas.oeste)


def _salas_guardadas(mapa, salas_preparadas, puertas_iniciales):
    for indice, sala in enumerate(mapa.todas_las_salas()):
        preparada = salas_preparadas.contiene(sala.id)
        cerradas = puertas_cerradas(sala)
        if (puertas_iniciales is not None and not preparada
                and sala.rastro_ultima_visita is None and not sala.enemigos_activos
                and cerradas == puertas_iniciales[indice]):
            continue
        yield _sala_guardada(sala, preparada, cerradas)


def _sala_guardada(sala, preparada: bool, cerradas) -> SalaGuardada:
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
                 salas_preparadas, acciones_jugador, enemigos_derrotados, mensajes, conocimiento,
                 linea=None, siguiente_instancia=0, puertas_iniciales=None) -> EstadoPartida:
    salas = tuple(_salas_guardadas(mapa, salas_preparadas, puertas_iniciales))
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
        conocimiento=ConocimientoGuardado(*conocimiento.exportar_celdas()),
        linea=linea,
        siguiente_instancia=siguiente_instancia,
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


def restaurar_conocimiento(mapa, sala_actual: int, proyeccion):
    conocimiento = ConocimientoJugador(mapa, sala_actual)
    if proyeccion is None:
        conocimiento.al_entrar(sala_actual, False)
        return conocimiento
    conocimiento.importar_celdas((proyeccion.estados, proyeccion.puertas, proyeccion.costos))
    return conocimiento


def restaurar_sala(sala, guardada, precarga, catalogo, enemigos, trampas) -> None:
    """Repone el estado de una sala. `enemigos` y `trampas` son VectorOrdenado por instancia_id:
    se llenan para que la agenda pueda encontrar a quién pertenece cada evento."""
    if guardada.contenido_cargado:
        precarga.preparar_sala(sala.id)              # contenido y fichas (infraestructura)
    _aplicar_estado_sala(sala, guardada, catalogo, enemigos, trampas)


def restaurar_sala_materializada(sala, guardada, catalogo, enemigos, trampas) -> None:
    """Igual que restaurar_sala pero sin precarga: el estado guardado ya trae todo el contenido de la sala."""
    if guardada.contenido_cargado:
        sala.contenido_cargado = True
    _aplicar_estado_sala(sala, guardada, catalogo, enemigos, trampas)


def _aplicar_estado_sala(sala, guardada, catalogo, enemigos, trampas) -> None:
    for direccion, cerrada in zip(DIRECCIONES, guardada.puertas_cerradas):
        if cerrada:
            sala.puertas.cerrar(direccion)
        else:
            sala.puertas.abrir(direccion)
    sala.rastro_ultima_visita = None if guardada.rastro < 0 else guardada.rastro
    if guardada.contenido_cargado:
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


# ----------------------------------------------------------------------------------------------
# Reconstrucción aislada (línea de tiempo): contenido inicial de las salas ya materializadas y
# un mapa nuevo que comparte solo el esqueleto estático. Nada de esto usa red, disco ni precarga.
# ----------------------------------------------------------------------------------------------
class ContenidoInicial:
    """Contenido de una sala justo después de prepararla: objetos, trampas y enemigos dormidos."""
    __slots__ = ("sala_id", "objetos", "trampas", "enemigos")

    def __init__(self, sala_id, objetos, trampas, enemigos):
        self.sala_id = sala_id
        self.objetos = objetos        # ids de catálogo
        self.trampas = trampas        # (instancia, tipo)
        self.enemigos = enemigos      # (instancia, tipo, vida)


def contenido_inicial_de(sala) -> ContenidoInicial:
    # Se toma justo al preparar la sala, antes de que el jugador cambie algo en ella
    objetos = tuple(sala.objetos_en_suelo)
    trampas = tuple((t.instancia_id, t.tipo_catalogo) for t in sala.trampas)
    enemigos = tuple((e.instancia_id, e.tipo_catalogo, e.vida) for e in sala.enemigos_dormidos)
    return ContenidoInicial(sala.id, objetos, trampas, enemigos)


def materializar_sala(sala, contenido, catalogo) -> None:
    # Pone en la sala su contenido inicial usando solo fichas del catálogo ya cargado
    sala.objetos_en_suelo = list(contenido.objetos)
    sala.trampas = [Trampa(instancia, tipo) for instancia, tipo in contenido.trampas]
    sala.enemigos_dormidos = [
        Enemigo(instancia, catalogo.obtener(tipo), sala.id, vida) for instancia, tipo, vida in contenido.enemigos
    ]
    sala.contenido_cargado = True


class PrecargaMaterializada:
    """Sustituye a la precarga en la reconstrucción: entrega salas sin red, disco ni solicitudes."""

    def __init__(self, mapa, contenidos, catalogo):
        self._mapa = mapa
        self._contenidos = contenidos   # VectorOrdenado de ContenidoInicial por sala_id
        self._catalogo = catalogo

    def preparar_sala(self, sala_id: int):
        sala = self._mapa.obtener(sala_id)
        if not sala.contenido_cargado:
            contenido = self._contenidos.buscar(sala_id)
            if contenido is None:
                sala.contenido_cargado = True
            else:
                materializar_sala(sala, contenido, self._catalogo)
        return sala

    def precargar_desde(self, sala_id: int) -> None:
        return None


def linea_a_guardada(linea, base, contenidos) -> LineaGuardada:
    """Línea vigente completa como datos planos. `base` es (estado, siguiente_instancia) y `contenidos`
    el VectorOrdenado de ContenidoInicial. Los puntos de control de la línea guardan la misma pareja."""
    acciones = []
    for numero in range(1, len(linea) + 1):
        accion = linea.accion(numero)
        acciones.append(AccionGuardada(accion.tipo, accion.argumento, linea.tiempo_de(numero)))
    ajustes = []
    for posicion in range(len(linea) + 1):
        for operacion in linea.ajustes_en(posicion):
            ficha = operacion[2] if len(operacion) > 2 else ""
            ajustes.append(AjusteGuardado(posicion, operacion[0], operacion[1], ficha))
    puntos = []
    numero = len(linea)
    punto = linea.buscar_checkpoint(numero)
    while punto is not None:
        puntos.append(PuntoControlGuardado(punto.numero_acciones, punto.estado[0], punto.estado[1]))
        punto = linea.buscar_checkpoint(punto.numero_acciones - 1)
    puntos.reverse()
    guardados = tuple(
        ContenidoSalaGuardado(c.sala_id, c.objetos, c.trampas, c.enemigos) for c in contenidos.elementos()
    )
    return LineaGuardada(linea.frecuencia, PuntoControlGuardado(0, base[0], base[1]), tuple(acciones),
                         tuple(ajustes), tuple(puntos), guardados)


def linea_desde_guardada(guardada):
    """Inversa de linea_a_guardada: devuelve (LineaTiempo, base, contenidos) con las mismas parejas en memoria."""
    try:
        linea = LineaTiempo(guardada.frecuencia)
        for posicion in range(len(guardada.acciones) + 1):
            if posicion > 0:
                a = guardada.acciones[posicion - 1]
                linea.registrar_accion(Accion(a.tipo, a.argumento), a.tiempo)
            for punto in guardada.checkpoints:
                if punto.numero_acciones == posicion:
                    linea.registrar_checkpoint((punto.estado, punto.siguiente_instancia))
            operaciones = []
            for ajuste in guardada.ajustes:
                if ajuste.posicion == posicion:
                    operaciones.append((ajuste.operacion, ajuste.instancia_id) if ajuste.operacion == "quitar"
                                       else (ajuste.operacion, ajuste.instancia_id, ajuste.ficha_id))
            if len(operaciones) > 0:
                linea.registrar_ajuste(operaciones)
    except ValueError as error:
        raise CriptaFormatoIncompatibleError(f"la línea de tiempo guardada es inconsistente: {error}") from None
    contenidos = VectorOrdenado(clave=lambda c: c.sala_id)
    for c in guardada.contenidos:
        contenidos.insertar(ContenidoInicial(c.sala_id, c.objetos, c.trampas, c.enemigos))
    return linea, (guardada.base.estado, guardada.base.siguiente_instancia), contenidos


def copiar_mapa_estatico(mapa):
    """Mapa nuevo con las mismas salas de esqueleto y sin nada del estado vivo."""
    copia = CriptaMapa()
    copia.agregar_pagina(SimpleNamespace(salas=tuple(sala.esqueleto for sala in mapa.todas_las_salas())))
    return copia
