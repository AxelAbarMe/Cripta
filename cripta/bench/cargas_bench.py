"""Cargas sintéticas para --bench (§5.3). Cada función mide UN subsistema y, cuando el
Documento de Decisiones lo exige (§8.5), mide TAMBIÉN la alternativa descartada, con
los mismos datos, para que la comparación sea justa. Ninguna toca red, vista ni una
cripta real: todo son datos generados aquí (o en tests/cripta_artificial.py) con una semilla fija (reproducible).


`escala` multiplica los tamaños de las cargas (1.0 = rápido; 5.0 = mediciones más finas).
"""
import copy
import gc
import json
import os
import platform
import random
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass, fields, is_dataclass, replace
from pathlib import Path

from cripta.constantes import direccion_opuesta
from cripta.dto.entidad_dto import entidad_desde_json
from cripta.dto.llave_ubicacion_dto import LlaveUbicacionDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.sala_dto import SalaDTO
from cripta.dto.salida_dto import SalidaDTO
from cripta.estructuras.lista_doble_enlazada import ListaDobleEnlazada
from cripta.estructuras.heap_min import HeapMinimo
from cripta.estructuras.ordenamiento_selector import elegir_algoritmo, ordenar_auto
from cripta.estructuras.ordenamientos import Ordenamiento
from cripta.estructuras.vector import VectorOrdenado
from cripta.infraestructura import guardado_binario as gb
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.estado_guardado import (
    EnemigoGuardado, EstadoPartida, EstadoRNG, EventoGuardado, JugadorGuardado,
    ObjetoGuardado, SalaGuardada, TrampaGuardada,
)
from cripta.modelo import combate
from cripta.modelo.accion import Accion
from cripta.modelo.buscador_rutas import BuscadorRutas
from cripta.modelo.enemigo import Enemigo
from cripta.modelo.historial_retroceso import HistorialRetroceso
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.jugador import Jugador
from cripta.modelo.linea_tiempo import LineaTiempo
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.partida import Partida
from cripta.modelo.reloj import RelojEventos, calcular_intervalo
from cripta.modelo.resolubilidad import VerificadorResolubilidad
from cripta.modelo.conocimiento_jugador import ConocimientoJugador
from cripta.modelo.ruta_conocida import siguiente_paso
from cripta.servicios.servicio_partida import ServicioPartida


SEMILLA_BENCH = 20260928


@dataclass(frozen=True)
class Resultado:
    subsistema: str
    caso: str
    segundos: float
    operaciones: int
    nota: str = ""
    es_razon: bool = False


    @property
    def micros_por_operacion(self) -> float:
        return self.segundos / self.operaciones * 1e6 if self.operaciones else 0.0


def _medir(funcion, repeticiones: int = 3) -> float:
    """Mejor de `repeticiones` corridas (reduce el ruido del sistema operativo)."""
    mejor = None
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        funcion()
        dt = time.perf_counter() - t0
        mejor = dt if mejor is None or dt < mejor else mejor
    return mejor


def _comparar(descartada: str, t_descartada: float, elegida: str, t_elegida: float) -> str:
    """Texto que dice cuántas veces más lenta o más rápida es la alternativa descartada que la
    elegida, con el número siempre mayor que 1 (por ejemplo "5.3x más rápido", no "0.2x")."""
    if t_descartada > t_elegida:
        return f"{descartada} es {t_descartada / t_elegida:.1f}x más lento que {elegida}"
    return f"{descartada} es {t_elegida / t_descartada:.1f}x más rápido que {elegida}"


# ============================================================ 1. AGENDA (§4.1)
class _AgendaLineal:
    """ALTERNATIVA DESCARTADA: lista sin orden, el mínimo se busca recorriéndola."""


    def __init__(self):
        self.eventos = []  # (tiempo, secuencia, id)


    def programar(self, tiempo, secuencia, ident):
        self.eventos.append((tiempo, secuencia, ident))


    def extraer_minimo(self):
        mejor = 0
        for i in range(1, len(self.eventos)):
            if self.eventos[i] < self.eventos[mejor]:
                mejor = i
        return self.eventos.pop(mejor)


def bench_agenda(escala: float = 1.0):
    resultados = []
    operaciones = max(500, int(3000 * escala))
    for pendientes in (100, 500, 2000):
        azar = random.Random(SEMILLA_BENCH)
        tiempos = [azar.randint(0, 500) for _ in range(pendientes)]


        def con_heap():
            reloj = RelojEventos()
            for k in range(pendientes):
                reloj.programar(tiempos[k], lambda: None)
            for _ in range(operaciones):
                evento = reloj.ejecutar_siguiente()
                reloj.programar(evento.tiempo + 66, evento.accion)


        def con_lista():
            agenda = _AgendaLineal()
            for k in range(pendientes):
                agenda.programar(tiempos[k], k, k)
            secuencia = pendientes
            for _ in range(operaciones):
                tiempo, _seq, ident = agenda.extraer_minimo()
                agenda.programar(tiempo + 66, secuencia, ident)
                secuencia += 1


        th, tl = _medir(con_heap, 2), _medir(con_lista, 2)
        resultados.append(Resultado("agenda", f"{pendientes} pendientes: heap (elegida)", th, operaciones))
        resultados.append(Resultado("agenda", f"{pendientes} pendientes: lista lineal (descartada)", tl, operaciones,
                                    f"{tl / th:.1f}x más lenta que el heap"))
    # cancelaciones (borrado perezoso) y reprogramaciones
    reloj = RelojEventos()
    eventos = [reloj.programar(i % 400, lambda: None) for i in range(operaciones)]


    def cancelar_y_reprogramar():
        for i, ev in enumerate(eventos):
            if i % 3 == 0:
                reloj.cancelar(ev)
            elif i % 3 == 1:
                reloj.reprogramar(ev, ev.tiempo + 25)
    resultados.append(Resultado("agenda", "cancelar 1/3 y reprogramar 1/3 (perezoso)", _medir(cancelar_y_reprogramar, 1), operaciones))
    return resultados


# ============================================================ 2. CACHÉ (§4.4)
class _Ficha:
    def __init__(self, i):
        self.id = f"itm_{i:05d}"


def bench_cache(escala: float = 1.0):
    resultados = []
    consultas = max(2000, int(20000 * escala))
    for tamano in (25, 1000):
        fichas = [_Ficha(i) for i in range(tamano)]
        azar = random.Random(SEMILLA_BENCH)
        pedidas = [fichas[azar.randrange(tamano)].id for _ in range(consultas)]
        vector = VectorOrdenado(clave=lambda f: f.id)
        for f in fichas:
            vector.insertar(f)


        def busqueda_binaria():
            for ident in pedidas:
                vector.buscar(ident)


        def busqueda_lineal():
            for ident in pedidas:
                for f in fichas:
                    if f.id == ident:
                        break


        tb, tl = _medir(busqueda_binaria), _medir(busqueda_lineal)
        resultados.append(Resultado("caché", f"buscar en {tamano} fichas: VectorOrdenado (elegida)", tb, consultas))
        resultados.append(Resultado("caché", f"buscar en {tamano} fichas: recorrido lineal (descartada)", tl, consultas,
                                    _comparar("el recorrido lineal", tl, "VectorOrdenado", tb)))


        # "usé esta ficha" -> pasa a ser la más reciente
        lista = ListaDobleEnlazada()
        nodos = [lista.agregar(i) for i in range(tamano)]
        plana = list(range(tamano))
        indices = [azar.randrange(tamano) for _ in range(consultas)]


        def lru_lista_doble():
            for i in indices:
                lista.mover_al_inicio(nodos[i])


        def lru_lista_plana():
            for i in indices:
                plana.remove(i)
                plana.insert(0, i)


        t1, t2 = _medir(lru_lista_doble), _medir(lru_lista_plana)
        resultados.append(Resultado("caché", f"marcar uso LRU con {tamano} fichas: lista doble (elegida)", t1, consultas))
        resultados.append(Resultado("caché", f"marcar uso LRU con {tamano} fichas: list.remove+insert (descartada)", t2, consultas,
                                    _comparar("list.remove+insert", t2, "la lista doble", t1)))
    return resultados


def bench_recuperacion_disco(escala: float = 1.0):
    """Recuperar una ficha liberada de memoria = una lectura de disco (§4.4)."""
    cantidad = max(50, int(300 * escala))
    with tempfile.TemporaryDirectory() as directorio:
        disco = CacheDisco(AlmacenDiscoArchivos(directorio))
        for i in range(cantidad):
            disco.guardar_ficha("cat-bench", entidad_desde_json(
                {"id": f"itm_{i:04d}", "clase": "arma", "nombre": f"Arma {i}", "peso": 2, "valor": 15, "ataque_bonus": 3}))


        def recuperar():
            for i in range(cantidad):
                disco.leer_ficha("cat-bench", f"itm_{i:04d}")


        t = _medir(recuperar)
    return [Resultado("disco", "recuperar ficha liberada (lectura de disco + parseo)", t, cantidad,
                      "referencia del API: ~400 ms por solicitud de red")]


# ========================================================== 3. INVENTARIO (§4.5)
def _medir_sin_contar_preparacion(preparar, operar, repeticiones: int = 3) -> float:
    """Como _medir, pero solo cronometra `operar`: `preparar` arma los datos antes de cada
    repetición y su tiempo no se cuenta (por ejemplo, construir la lista que se va a medir)."""
    mejor = None
    for _ in range(repeticiones):
        datos = preparar()
        t0 = time.perf_counter()
        operar(datos)
        dt = time.perf_counter() - t0
        mejor = dt if mejor is None or dt < mejor else mejor
    return mejor


def bench_inventario(escala: float = 1.0):
    resultados = []
    for n in (10, 10000):
        repeticiones = max(200, int(2000 * escala)) if n == 10 else max(50, int(300 * escala))


        def preparar_lista_doble():
            lista = ListaDobleEnlazada()
            nodos = [lista.agregar(i) for i in range(n)]
            return lista, nodos


        def con_lista_doble(datos):
            lista, nodos = datos
            for k in range(repeticiones):
                nodo = nodos[(n // 2 + k) % n]
                lista.eliminar_nodo(nodo)              # soltar el objeto que se está viendo: O(1)
                nodos[(n // 2 + k) % n] = lista.agregar(k)


        def preparar_list():
            return list(range(n))


        def con_list(plana):
            for k in range(repeticiones):
                pos = (n // 2 + k) % n
                plana.pop(pos)                        # desplaza todo lo posterior: O(n)
                plana.append(k)


        t1 = _medir_sin_contar_preparacion(preparar_lista_doble, con_lista_doble)
        t2 = _medir_sin_contar_preparacion(preparar_list, con_list)
        resultados.append(Resultado("inventario", f"soltar en medio, n={n}: lista doble (elegida)", t1, repeticiones))
        comparacion = _comparar("list.pop(i)", t2, "la lista doble", t1)
        if n == 10:
            comparacion += "  <- con inventario_max típico (~10) la diferencia es despreciable"
        resultados.append(Resultado("inventario", f"soltar en medio, n={n}: list.pop(i) (descartada)", t2, repeticiones,
                                    comparacion))
    return resultados


# ==================================================== 4. HISTORIAL (§4.6)
def bench_historial(escala: float = 1.0):
    """Inversa por operación (elegida) vs copiar el estado completo (descartada: el PDF la
    prohíbe en el juego; aquí solo se mide para justificar por qué)."""
    acciones = max(100, int(500 * escala))
    salas = 200
    estado = {"salas": [{"id": i, "objetos": list(range(5)), "trampas": [i, i + 1], "puertas": [False] * 4} for i in range(salas)],
              "actores": [{"vida": 12, "sala": i % salas, "t": i} for i in range(60)], "reloj": 0}


    def inversas():
        historial = HistorialRetroceso()
        vida = [30]
        for _ in range(acciones):
            historial.iniciar_intervalo()
            for _ in range(6):                        # una acción típica: ataque, veneno, respuesta enemiga...
                vida[0] -= 1
                historial.registrar(lambda: vida.__setitem__(0, vida[0] + 1))
            historial.cerrar_intervalo()


    def copias():
        guardadas = []
        for _ in range(acciones):
            guardadas.append(copy.deepcopy(estado))
            if len(guardadas) > 5:
                guardadas.pop(0)


    def deshacer():
        historial = HistorialRetroceso()
        vida = [30]
        for _ in range(5):
            historial.iniciar_intervalo()
            for _ in range(6):
                vida[0] -= 1
                historial.registrar(lambda: vida.__setitem__(0, vida[0] + 1))
            historial.cerrar_intervalo()
        for _ in range(5):
            historial.deshacer_ultimo_intervalo()


    t1, t2, t3 = _medir(inversas), _medir(copias, 1), _medir(deshacer)
    return [
        Resultado("historial", "registrar acción (6 inversas): operaciones inversas (elegida)", t1, acciones),
        Resultado("historial", f"registrar acción: copia completa de {salas} salas + 60 actores (descartada, prohibida)", t2, acciones,
                  f"{t2 / t1:.0f}x más lenta y guarda 5 estados enteros"),
        Resultado("historial", "deshacer 5 acciones (30 inversas)", t3, 5),
    ]


# ================================================== 5. ORDENAMIENTO (§4.9)
class _Costoso:
    """Elemento cuya comparación se cuenta: modela un orden caro de evaluar."""
    comparaciones = 0


    def __init__(self, valor):
        self.valor = valor


    def __lt__(self, otro):
        _Costoso.comparaciones += 1
        return self.valor < otro.valor


def bench_ordenamiento(escala: float = 1.0):
    resultados = []
    azar = random.Random(SEMILLA_BENCH)


    def casi_ordenado(n):
        datos = list(range(n))
        for _ in range(max(1, n // 50)):
            i, j = azar.randrange(n), azar.randrange(n)
            datos[i], datos[j] = datos[j], datos[i]
        return datos


    for n in (10, 50, 200, 1000):
        casos = (("aleatorio", azar.sample(range(n * 10), n)), ("casi ordenado (2%)", casi_ordenado(n)),
                 ("inverso", list(range(n, 0, -1))))
        repeticiones = max(3, int(200 * escala / n)) if n < 1000 else 1
        for nombre, datos in casos:
            algoritmos = [("inserción", "insertion_sort"), ("mergesort", "merge_sort")]
            if n <= 200:
                algoritmos.append(("burbuja (descartada)", "bubble_sort"))
            tiempos = []
            for etiqueta, metodo in algoritmos:
                def correr():
                    for _ in range(repeticiones):
                        getattr(Ordenamiento(list(datos)), metodo)()
                tiempos.append((etiqueta, _medir(correr, 2) / repeticiones))


            def auto():
                for _ in range(repeticiones):
                    ordenar_auto(list(datos))
            t_auto = _medir(auto, 2) / repeticiones
            mejor = min(t for _e, t in tiempos[:2])
            elegido = elegir_algoritmo(datos)
            for etiqueta, t in tiempos:
                resultados.append(Resultado("ordenamiento", f"n={n} {nombre}: {etiqueta}", t, 1))
            resultados.append(Resultado("ordenamiento", f"n={n} {nombre}: AUTOMÁTICO -> {elegido}", t_auto, 1,
                                        f"{t_auto / mejor:.2f}x del mejor de los dos"))
    # comparaciones costosas: cuántas comparaciones hace cada algoritmo
    for n in (50, 200):
        for nombre, datos in (("aleatorio", azar.sample(range(n * 10), n)), ("casi ordenado (2%)", casi_ordenado(n))):
            cuentas = []
            for etiqueta, metodo in (("inserción", "insertion_sort"), ("mergesort", "merge_sort")):
                _Costoso.comparaciones = 0
                Ordenamiento([_Costoso(v) for v in datos]).__getattribute__(metodo)()
                cuentas.append((etiqueta, _Costoso.comparaciones))
            elegido = elegir_algoritmo(datos, comparacion_costosa=True)
            resultados.append(Resultado("ordenamiento", f"comparaciones n={n} {nombre}", 0.0, 1,
                                        f"inserción={cuentas[0][1]}, merge={cuentas[1][1]} -> elige {elegido} si comparar es caro"))
    return resultados


# ==================================================== 6. GUARDADO (§4.10)
def estado_sintetico(n_salas: int, semilla: int = SEMILLA_BENCH) -> EstadoPartida:
    azar = random.Random(semilla)
    ids = list(range(1, n_salas + 1))
    azar.shuffle(ids)
    salas = []
    for i in ids:
        salas.append(SalaGuardada(
            i, True, (i % 2 == 0, False, i % 3 == 0, False), -1 if i % 4 else i * 10,
            ("itm_daga", "itm_antorcha")[: 1 + i % 2],
            (TrampaGuardada(f"t-{i}", "trp_dardos", i % 3 != 0),) if i % 5 == 0 else (),
            tuple(EnemigoGuardado(f"e-{i}{k}", "ent_rata_gigante", 7, k == 1, i, 66 + i) for k in range(1 + i % 3))))
    jugador = JugadorGuardado(24, 30, 6, 2, 100, 3, 250, 10, 1,
                              tuple(ObjetoGuardado(f"o-{k}", "itm_daga", k == 0) for k in range(8)))
    eventos = tuple(EventoGuardado(100 + k, k, k % 7, f"e-{k}1", k, k * 2) for k in range(min(300, n_salas * 2)))
    return EstadoPartida("cripta-bench", "a3f91c", "cat-2026-08-01", semilla,
                         EstadoRNG.desde_random(random.Random(semilla)), 190, 999, 70, 12, jugador,
                         tuple(salas), eventos, tuple(f"mensaje {k}" for k in range(20)))


def bench_guardado(escala: float = 1.0):
    resultados = []
    binario = gb.GuardadoBinario()
    with tempfile.TemporaryDirectory() as directorio:
        for n_salas in (50, 500, 5000):
            estado = estado_sintetico(n_salas)
            ruta_bin = os.path.join(directorio, "p.sav")
            ruta_json = os.path.join(directorio, "p.json")
            tam_bin = binario.guardar(ruta_bin, estado)
            tam_json = gb.guardar_json(ruta_json, estado)
            r = 3
            resultados.append(Resultado("guardado", f"{n_salas} salas: TAMAÑO binario vs JSON", 0.0, 1,
                                        f"binario={tam_bin} B, json={tam_json} B ({tam_json / tam_bin:.1f}x el binario)"))
            resultados.append(Resultado("guardado", f"{n_salas} salas: guardar binario", _medir(lambda: binario.guardar(ruta_bin, estado), r), 1))
            resultados.append(Resultado("guardado", f"{n_salas} salas: guardar JSON", _medir(lambda: gb.guardar_json(ruta_json, estado), r), 1))
            tb = _medir(lambda: binario.cargar(ruta_bin), r)
            tj = _medir(lambda: gb.cargar_json(ruta_json), r)
            resultados.append(Resultado("guardado", f"{n_salas} salas: cargar todo binario", tb, 1))
            resultados.append(Resultado("guardado", f"{n_salas} salas: cargar todo JSON", tj, 1,
                                        _comparar("cargar JSON", tj, "cargar binario", tb)))
            objetivo = n_salas // 2
            ts = _medir(lambda: binario.cargar_sala(ruta_bin, objetivo), 5)
            resultados.append(Resultado("guardado", f"{n_salas} salas: cargar UNA sala (binario, con índice)", ts, 1,
                                        f"{tb / ts:.0f}x más rápido que cargar todo"))
    return resultados


# ============================================ 7. CICLO DE EVENTOS (§5.2)
def bench_ciclo_eventos(escala: float = 1.0):
    """Entre dos decisiones del jugador actúan cientos de eventos: debe tomar < 20 ms."""
    resultados = []
    for actores in (100, 300, 600):
        azar = random.Random(SEMILLA_BENCH)
        jugador = Jugador(type("J", (), {"vida_max": 10**9, "ataque": 6, "defensa": 2, "velocidad": 100})(), 1, 10)
        ficha = type("F", (), {"id": "ent_rata", "nombre": "Rata", "vida_max": 10**9, "ataque": 5, "defensa": 1,
                               "velocidad": 150, "comportamiento": "rastreador", "suelta": (), "rango": None})()
        reloj = RelojEventos()
        enemigos = [Enemigo(f"e-{i}", ficha, 1) for i in range(actores)]


        def turno(enemigo):
            def accion():
                if not enemigo.esta_vivo():
                    return
                combate.atacar(enemigo, jugador, azar)
                reloj.programar_en(calcular_intervalo(100, enemigo.velocidad), accion)
            return accion


        for i, enemigo in enumerate(enemigos):
            reloj.programar(66 + i % 5, turno(enemigo))


        # varios ciclos consecutivos; se reporta el peor
        peores = 0.0
        for k in range(20):
            objetivo = reloj.tiempo_actual + 100
            t0 = time.perf_counter()
            n_eventos = 0
            while True:
                reloj.ejecutar_siguiente()
                n_eventos += 1
                if reloj.tiempo_actual >= objetivo:
                    break
            peores = max(peores, time.perf_counter() - t0)
        cumple = "CUMPLE" if peores * 1000 < 20 else "NO CUMPLE"
        resultados.append(Resultado("ciclo de eventos", f"{actores} actores activos, peor de 20 ciclos ({n_eventos} eventos)", peores, 1,
                                    f"{peores * 1000:.2f} ms  -> {cumple} el límite de 20 ms (§5.2)"))
    return resultados


# ===================================== 8. CICLO CON LA PARTIDA REAL (§5.2)
def _recorrido_en_zigzag(filas: int, columnas: int):
    """Direcciones para recorrer la cuadrícula fila por fila (E, S, O, S, E...) sin entrar a la
    última fila: en la cripta artificial la sala de salida es la última y entrar ahí termina la partida."""
    pasos = []
    for fila in range(filas - 1):
        pasos.extend(["E" if fila % 2 == 0 else "O"] * (columnas - 1))
        if fila < filas - 2:
            pasos.append("S")
    return pasos


def _jugar_y_medir(lado: int):
    """Una corrida: arma la partida, recorre la cripta, espera 50 veces y devuelve
    (tiempos de cada acción en segundos, enemigos activos al final)."""
    # Imports locales: tests/ no es parte del paquete cripta; si fallaran, solo fallaría esta carga
    from tests.cliente_falso import ClienteFalso
    from tests.cripta_artificial import construir


    datos = construir(lado, lado)
    cliente = ClienteFalso(datos["fichas"], datos["contenido"], datos["paginas"], datos["general"])
    servicio = ServicioPartida(ClienteGeneral(cliente), ContadorSolicitudes(), asincrono=False)
    servicio.iniciar_nueva(datos["general"]["id"], semilla=SEMILLA_BENCH)
    jugador = servicio.partida._jugador
    jugador.vida_max = jugador.vida = 10 ** 9      # que los enemigos no terminen la partida antes de medir


    tiempos = []
    acciones = [Accion("mover", d) for d in _recorrido_en_zigzag(lado, lado)] + [Accion("esperar")] * 50
    for accion in acciones:
        t0 = time.perf_counter()
        servicio.ejecutar(accion)
        tiempos.append(time.perf_counter() - t0)
    activos = 0
    for sala in servicio.partida._mapa.todas_las_salas():
        activos += len(sala.enemigos_activos)
    servicio.cerrar()
    return tiempos, activos


def _mediana(valores):
    ordenados = list(valores)
    ordenar_auto(ordenados)
    return ordenados[len(ordenados) // 2]


def _resumen_mediciones(funcion, repeticiones: int = 3):
    """Devuelve mediana y máximo de corridas completas medidas por reloj de pared."""
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - inicio)
    return _mediana(tiempos), max(tiempos)


def bench_partida_real(escala: float = 1.0, corridas: int = 3):
    """§5.2 con el modelo real: Partida + ServicioPartida sobre una cripta artificial, sin red (ClienteFalso
    responde al instante) ni vista. El jugador recorre la cripta despertando enemigos y después espera;
    se mide cada ejecutar(), que es un ciclo completo entre dos decisiones del jugador. Cada tamaño se
    corre varias veces y se reporta la mediana, porque el peor caso de una sola corrida varía mucho."""
    resultados = []
    for lado in (5, 10, max(15, int(20 * escala))):
        peores, medianas = [], []
        for _ in range(corridas):
            tiempos, activos = _jugar_y_medir(lado)
            peores.append(max(tiempos))
            medianas.append(_mediana(tiempos))
        peor = _mediana(peores)  # mediana de los peores de cada corrida
        mediana = _mediana(medianas)
        cumple = "CUMPLE" if peor * 1000 < 20 else "NO CUMPLE"
        peor_ms = f"{peor * 1000:.2f}"
        mediana_ms = f"{mediana * 1000:.2f}"
        detalle = ", ".join(f"{p * 1000:.2f}" for p in peores)
        resultados.append(Resultado(
            "partida real",
            f"{lado * lado} salas, {activos} enemigos activos al final, {len(tiempos)} acciones x {corridas} corridas",
            peor, 1, f"tiempo típico de una acción: {mediana_ms} ms, peor caso: {peor_ms} ms "
                     f"(peor de cada corrida: {detalle} ms; se toma el del medio: {peor_ms}) "
                     f"-> {cumple} el límite de 20 ms (§5.2, decide la mediana de los peores casos)"))
    return resultados


# =========================================== 9. SOLICITUDES DE RED (§4.2 y §4.3)
def bench_solicitudes(escala: float = 1.0):
    """Cuántas solicitudes de red cuesta recorrer una cripta con lotes (precarga de contenido y
    catálogo, lo elegido) contra pedir cada cosa por separado (lo descartado). No mide tiempo:
    cuenta las llamadas que registra ClienteFalso. Lo descartado se calcula a partir de lo que
    realmente se necesitó: una solicitud por cada sala visitada y una por cada ficha distinta."""
    # Imports locales: tests/ no es parte del paquete cripta; si fallaran, solo fallaría esta carga
    from tests.cliente_falso import ClienteFalso
    from tests.cripta_artificial import construir


    resultados = []
    for lado in (10, max(15, int(20 * escala))):
        datos = construir(lado, lado)
        cliente = ClienteFalso(datos["fichas"], datos["contenido"], datos["paginas"], datos["general"])
        servicio = ServicioPartida(ClienteGeneral(cliente), ContadorSolicitudes(), asincrono=False)
        servicio.iniciar_nueva(datos["general"]["id"], semilla=SEMILLA_BENCH)
        jugador = servicio.partida._jugador
        jugador.vida_max = jugador.vida = 10 ** 9      # que los enemigos no terminen la partida antes de tiempo
        pasos = _recorrido_en_zigzag(lado, lado)
        for direccion in pasos:
            servicio.ejecutar(Accion("mover", direccion))
        servicio.cerrar()


        salas_visitadas = len(pasos) + 1                # la sala inicial más una por cada movimiento
        lotes_contenido = cliente.contar("obtener_contenido")
        lotes_catalogo = cliente.contar("obtener_catalogo")
        fichas = VectorOrdenado()                       # fichas distintas que se llegaron a pedir
        for metodo, ids in cliente.llamadas:
            if metodo == "obtener_catalogo":
                for ficha_id in ids:
                    if not fichas.contiene(ficha_id):
                        fichas.insertar(ficha_id)


        resultados.append(Resultado(
            "solicitudes", f"{lado * lado} salas, {salas_visitadas} visitadas: contenido", 0.0, 1,
            f"con precarga en lotes: {lotes_contenido} solicitudes; una por sala visitada (descartada): "
            f"{salas_visitadas} solicitudes"))
        resultados.append(Resultado(
            "solicitudes", f"{lado * lado} salas, {salas_visitadas} visitadas: catálogo", 0.0, 1,
            f"por lotes: {lotes_catalogo} solicitudes; una por ficha (descartada): {len(fichas)} solicitudes"))
    return resultados


# ============================== 10. CAZADORES (capacidad 001, FR-TER-020)
SEMILLA_CARGAS_TERRENO = 42
RANGO_SABUESO_BENCH = 600
RANGO_ESPECTRO_BENCH = 2400
COSTO_SALIDA_MIN_BENCH = 20
COSTO_SALIDA_MAX_BENCH = 490
LADO_CRIPTA_TERRENO = 20
CAZADORES_POR_ESCENARIO = (1, 10, 30)
MEZCLA_SABUESOS = 25
MEZCLA_ESPECTROS = 11
CAZADORES_INVALIDACION = 20
TICKS_INVALIDACION = 100
PASOS_ALEJAMIENTO = 8
VELOCIDAD_CAZADOR_INVALIDACION = 25
PUERTAS_INESTABLES = 5
PERIODO_CIERRE_TICKS = 15
TICK_REAPERTURA = 7
PASOS_CALENTAMIENTO_REFERENCIA = 150
LIMITE_CICLO_MS = 20.0
LIMITE_PASO_MS = 5.0
DIRECTORIO_FIXTURES_BENCH = Path(__file__).resolve().parents[2] / "fixtures"


def elegir_cripta_de_referencia(criptas):
    """La cripta con más salas del listado. Un empate lo decide el menor id. Ningún id está fijado en el código."""
    return min(criptas, key=lambda cripta: (-cripta.salas, cripta.id))


def cripta_de_referencia():
    """La cripta de referencia de las cargas con partida real, elegida entre las de fixtures."""
    return elegir_cripta_de_referencia(ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH)).listar_criptas())


class _Medidor:
    """Acumula segundos y cantidad de llamadas de lo que se mide."""


    def __init__(self):
        self.segundos = 0.0
        self.llamadas = 0


class _BuscadorContado(BuscadorRutas):
    """BuscadorRutas que cuenta decisiones y ejecuciones de Dijkstra, y su tiempo si se pide."""


    def __init__(self, medir_tiempo: bool = False):
        super().__init__()
        self.busquedas = _Medidor()
        self.decisiones = 0
        self._medir_tiempo = medir_tiempo


    def decidir_paso(self, cazador, sala_jugador_id, mapa):
        # Cuenta la decisión y delega en la búsqueda original
        self.decisiones += 1
        return super().decidir_paso(cazador, sala_jugador_id, mapa)


    def _calcular(self, mapa, sala_jugador_id, rango_max):
        # Cuenta la ejecución y, si se pide, acumula su tiempo
        self.busquedas.llamadas += 1
        if not self._medir_tiempo:
            super()._calcular(mapa, sala_jugador_id, rango_max)
            return
        t0 = time.perf_counter()
        super()._calcular(mapa, sala_jugador_id, rango_max)
        self.busquedas.segundos += time.perf_counter() - t0


class _BuscadorRecalculaSiempre(_BuscadorContado):
    """ALTERNATIVA DESCARTADA: cada decisión de cazador ejecuta su propia búsqueda con su rango."""


    def calcular_o_reutilizar(self, mapa, sala_jugador_id, rango_max):
        # Nunca reutiliza la tabla ni la comparte entre cazadores
        self._calcular(mapa, sala_jugador_id, rango_max)


def _conexiones_cripta_terreno():
    """Cuadrícula cuadrada con costos de salida pseudoaleatorios de semilla fija."""
    azar = random.Random(SEMILLA_CARGAS_TERRENO)
    lado = LADO_CRIPTA_TERRENO
    conexiones = []
    for fila in range(lado):
        for columna in range(lado):
            sala = fila * lado + columna + 1
            if columna < lado - 1:
                conexiones.append((sala, "E", sala + 1, azar.randint(COSTO_SALIDA_MIN_BENCH, COSTO_SALIDA_MAX_BENCH)))
            if fila < lado - 1:
                conexiones.append((sala, "S", sala + lado, azar.randint(COSTO_SALIDA_MIN_BENCH, COSTO_SALIDA_MAX_BENCH)))
    return conexiones


def _rangos_mixtos(cantidad: int):
    """Rangos con la proporción de sabuesos y espectros de la mezcla, con al menos un espectro."""
    total = MEZCLA_SABUESOS + MEZCLA_ESPECTROS
    espectros = max(1, (cantidad * MEZCLA_ESPECTROS + total // 2) // total)
    return [RANGO_SABUESO_BENCH] * (cantidad - espectros) + [RANGO_ESPECTRO_BENCH] * espectros


def _armar_partida_terreno(salidas, rangos, buscador, velocidad_cazador: int = 100):
    """Partida sobre la cripta sintética con todos los cazadores en la sala 1 y el buscador indicado."""
    # Import local: tests/ no es parte del paquete cripta
    from tests.cripta_cazadores import armar_partida
    cazadores = [(1, f"cz-{i:03d}", rango) for i, rango in enumerate(rangos)]
    partida, mapa = armar_partida(salidas, cazadores, velocidad_jugador=100, velocidad_cazador=velocidad_cazador,
                                  semilla=SEMILLA_CARGAS_TERRENO)
    partida._jugador.vida_max = partida._jugador.vida = 10 ** 9
    partida._buscador = buscador
    return partida, mapa


def _envolver_consulta_de_costos(mapa) -> _Medidor:
    """Mide costo_de_conexion envolviendo la llamada en esta instancia, sin tocar CriptaMapa."""
    medidor = _Medidor()
    original = mapa.costo_de_conexion


    def medida(sala_id, direccion):
        t0 = time.perf_counter()
        try:
            return original(sala_id, direccion)
        finally:
            medidor.segundos += time.perf_counter() - t0
            medidor.llamadas += 1
    mapa.costo_de_conexion = medida
    return medidor


def _paso_aleatorio_aceptado(partida, mapa, azar, prohibido: int):
    """Mueve al jugador por una salida abierta al azar, o espera si no puede moverse. Devuelve la acción ejecutada."""
    origen = partida._jugador.sala_actual
    opciones = [d for d, destino in mapa.vecinos(origen)
                if destino != prohibido and mapa.puerta_transitable(origen, d)]
    if opciones:
        inicio = azar.randrange(len(opciones))
        for k in range(len(opciones)):
            accion = Accion("mover", opciones[(inicio + k) % len(opciones)])
            if partida.ejecutar_accion(accion).aceptada:
                return accion
    accion = Accion("esperar")
    partida.ejecutar_accion(accion)
    return accion


def _dar_paso_aleatorio(partida, mapa, azar, prohibido: int) -> None:
    """Mueve al jugador por una salida abierta al azar, o espera si no puede moverse."""
    _paso_aleatorio_aceptado(partida, mapa, azar, prohibido)


def _tiempos_de_pasos(partida, mapa, azar, ciclos: int, prohibido: int):
    """Tiempo de cada ciclo completo entre dos decisiones del jugador."""
    tiempos = []
    gc.collect()   # cada escenario no paga la basura acumulada por los anteriores
    for _ in range(ciclos):
        t0 = time.perf_counter()
        _dar_paso_aleatorio(partida, mapa, azar, prohibido)
        tiempos.append(time.perf_counter() - t0)
    return tiempos


def _correr_terreno(salidas, rangos, ciclos: int, fabrica_buscador, medir_consultas: bool = False):
    """Una corrida de ruta_cazador. Devuelve los tiempos, el buscador y el medidor de consultas."""
    partida, mapa = _armar_partida_terreno(salidas, rangos, fabrica_buscador())
    medidor = _envolver_consulta_de_costos(mapa) if medir_consultas else None
    tiempos = _tiempos_de_pasos(partida, mapa, random.Random(SEMILLA_CARGAS_TERRENO), ciclos, max(salidas))
    return tiempos, partida._buscador, medidor


def _tiempos_limpios(salidas, rangos, ciclos: int, corridas: int, fabrica_buscador):
    """Tiempos de ciclo de varias corridas sin instrumentos de medición."""
    tiempos = []
    for _ in range(corridas):
        tiempos.extend(_correr_terreno(salidas, rangos, ciclos, fabrica_buscador)[0])
    return tiempos


def _ms(segundos: float) -> str:
    return f"{segundos * 1000:.3f}"


def bench_ruta_cazador(escala: float = 1.0, corridas: int = 2):
    """Cálculo compartido (elegida) contra cálculo individual por cazador (descartada) en una cripta sintética."""
    # Import local: tests/ no es parte del paquete cripta
    from tests.cripta_cazadores import grafo
    salidas = grafo(_conexiones_cripta_terreno())
    ciclos = max(20, int(60 * escala))
    resultados = []
    for etiqueta, rango in (("R=600", RANGO_SABUESO_BENCH), ("R=2400", RANGO_ESPECTRO_BENCH), ("mixto 25:11", None)):
        for h in CAZADORES_POR_ESCENARIO:
            if rango is None and h < 2:
                continue
            rangos = _rangos_mixtos(h) if rango is None else [rango] * h
            caso = f"{etiqueta}, H={h}"
            t_comp = _tiempos_limpios(salidas, rangos, ciclos, corridas, BuscadorRutas)
            t_ind = _tiempos_limpios(salidas, rangos, ciclos, corridas, _BuscadorRecalculaSiempre)
            med_comp, med_ind = _mediana(t_comp), _mediana(t_ind)
            _t, bus_comp, cons_comp = _correr_terreno(salidas, rangos, ciclos, lambda: _BuscadorContado(True), True)
            _t, bus_ind, cons_ind = _correr_terreno(salidas, rangos, ciclos, lambda: _BuscadorRecalculaSiempre(True), True)
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: ciclo con cálculo compartido (elegida)", med_comp, 1,
                f"mediana de {len(t_comp)} ciclos, peor {_ms(max(t_comp))} ms"))
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: compartido, búsqueda sola", bus_comp.busquedas.segundos, ciclos,
                f"{bus_comp.busquedas.llamadas} búsquedas para {bus_comp.decisiones} decisiones, "
                f"total de la corrida de {ciclos} ciclos, no por ciclo"))
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: compartido, consultas de costo_de_conexion", cons_comp.segundos, ciclos,
                f"{cons_comp.llamadas} consultas ({cons_comp.segundos / max(1, cons_comp.llamadas) * 1e6:.2f} µs cada una), "
                f"medidas con envoltura que suma su propio costo"))
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: ciclo con cálculo individual (descartada)", med_ind, 1,
                f"mediana de {len(t_ind)} ciclos, peor {_ms(max(t_ind))} ms"))
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: individual, búsqueda sola", bus_ind.busquedas.segundos, ciclos,
                f"{bus_ind.busquedas.llamadas} búsquedas para {bus_ind.decisiones} decisiones, "
                f"total de la corrida de {ciclos} ciclos, no por ciclo"))
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: individual, consultas de costo_de_conexion", cons_ind.segundos, ciclos,
                f"{cons_ind.llamadas} consultas ({cons_ind.segundos / max(1, cons_ind.llamadas) * 1e6:.2f} µs cada una)"))
            resultados.append(Resultado(
                "ruta_cazador", f"{caso}: razón individual/compartido", 0.0, 1,
                f"razón de tiempo {med_ind / med_comp:.2f} y de búsquedas "
                f"{bus_ind.busquedas.llamadas / max(1, bus_comp.busquedas.llamadas):.2f}", es_razon=True))
    return resultados


def _puertas_a_dos_pasos(partida, mapa):
    """Conexiones que parten de las vecinas de la sala del jugador sin volver a ella."""
    origen = partida._jugador.sala_actual
    elegidas = []
    for _d, vecina in mapa.vecinos(origen):
        for direccion, lejana in mapa.vecinos(vecina):
            if lejana != origen and len(elegidas) < PUERTAS_INESTABLES:
                elegidas.append((vecina, direccion))
    return elegidas


def _correr_invalidacion(salidas, fabrica_buscador, inestable: bool):
    """Alejamiento del jugador y luego los ticks de espera. Devuelve segundos, buscador y puertas usadas."""
    partida, mapa = _armar_partida_terreno(salidas, [RANGO_ESPECTRO_BENCH] * CAZADORES_INVALIDACION,
                                           fabrica_buscador(), VELOCIDAD_CAZADOR_INVALIDACION)
    azar = random.Random(SEMILLA_CARGAS_TERRENO)
    for _ in range(PASOS_ALEJAMIENTO):
        partida.ejecutar_accion(Accion("mover", ("E", "S")[azar.randrange(2)]))
    partida._buscador.busquedas = _Medidor()
    partida._buscador.decisiones = 0
    puertas = _puertas_a_dos_pasos(partida, mapa) if inestable else []
    cerradas = False
    gc.collect()   # cada escenario no paga la basura acumulada por los anteriores
    t0 = time.perf_counter()
    for tick in range(1, TICKS_INVALIDACION + 1):
        if puertas and tick % PERIODO_CIERRE_TICKS == 0:
            for sala, direccion in puertas:
                mapa.cerrar_puerta(sala, direccion)
            partida._buscador.invalidar()
            cerradas = True
        elif puertas and cerradas and tick % PERIODO_CIERRE_TICKS == TICK_REAPERTURA:
            for sala, direccion in puertas:
                mapa.abrir_puerta(sala, direccion)
            partida._buscador.invalidar()
            cerradas = False
        partida.ejecutar_accion(Accion("esperar"))
    return time.perf_counter() - t0, partida._buscador, len(puertas)


def bench_invalidacion(escala: float = 1.0):
    """Invalidación selectiva (elegida) contra recalcular en cada turno de cazador (descartada)."""
    # Import local: tests/ no es parte del paquete cripta
    from tests.cripta_cazadores import grafo
    salidas = grafo(_conexiones_cripta_terreno())
    resultados = []
    for etiqueta, inestable in (("puertas estables", False),
                                (f"{PUERTAS_INESTABLES} puertas con cierre cada {PERIODO_CIERRE_TICKS} ticks", True)):
        total_e, bus_e, usadas = _correr_invalidacion(salidas, lambda: _BuscadorContado(True), inestable)
        total_d, bus_d, _usadas = _correr_invalidacion(salidas, lambda: _BuscadorRecalculaSiempre(True), inestable)
        caso = f"{CAZADORES_INVALIDACION} cazadores, {TICKS_INVALIDACION} ticks, {etiqueta}"
        resultados.append(Resultado(
            "invalidacion", f"{caso}: invalidación selectiva (elegida)", total_e, TICKS_INVALIDACION,
            f"{bus_e.busquedas.llamadas} búsquedas para {bus_e.decisiones} decisiones "
            f"(total de los {TICKS_INVALIDACION} ticks, no por ciclo), "
            f"{_ms(bus_e.busquedas.segundos)} ms en búsquedas, {usadas} puertas inestables"))
        resultados.append(Resultado(
            "invalidacion", f"{caso}: recalcular siempre (descartada)", total_d, TICKS_INVALIDACION,
            f"{bus_d.busquedas.llamadas} búsquedas para {bus_d.decisiones} decisiones "
            f"(total de los {TICKS_INVALIDACION} ticks, no por ciclo), "
            f"{_ms(bus_d.busquedas.segundos)} ms en búsquedas"))
        resultados.append(Resultado(
            "invalidacion", f"{caso}: razón recalcular siempre/selectiva", 0.0, 1,
            f"razón de tiempo {total_d / total_e:.2f} y de búsquedas "
            f"{bus_d.busquedas.llamadas / max(1, bus_e.busquedas.llamadas):.2f}", es_razon=True))
    return resultados


def _cazadores_activos(mapa):
    activos = []
    for sala in mapa.todas_las_salas():
        for enemigo in sala.enemigos_activos:
            if enemigo.comportamiento == "cazador":
                activos.append(enemigo)
    return activos


def _activar_cazadores_reales(partida, mapa) -> None:
    """Carga cada sala como lo hace el juego al entrar y activa los cazadores reales que tenga."""
    for sala_id in [sala.id for sala in mapa.todas_las_salas()]:
        with partida._historial.sin_registrar():
            sala = partida._precarga.preparar_sala(sala_id)
        partida._marcar_preparada(sala.id)
        if any(e.comportamiento == "cazador" for e in sala.enemigos_dormidos):
            partida._activar_enemigos_de(sala)


def _correr_referencia(ciclos: int, calentamiento: int):
    """Una corrida sobre la cripta de referencia. Devuelve tiempos, activos y perseguidores por ciclo."""
    servicio = ServicioPartida(ClienteGeneral(ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH))),
                               ContadorSolicitudes(), asincrono=False)
    servicio.iniciar_nueva(cripta_de_referencia().id, semilla=SEMILLA_BENCH)
    partida = servicio.partida
    mapa = partida._mapa
    partida._jugador.vida_max = partida._jugador.vida = 10 ** 9
    prohibido = servicio.datos_generales.sala_salida
    azar = random.Random(SEMILLA_CARGAS_TERRENO)
    _activar_cazadores_reales(partida, mapa)
    activos = len(_cazadores_activos(mapa))
    for _ in range(calentamiento):
        _dar_paso_aleatorio(partida, mapa, azar, prohibido)
    tiempos, perseguidores = [], []
    gc.collect()   # cada escenario no paga la basura acumulada por los anteriores
    for _ in range(ciclos):
        t0 = time.perf_counter()
        _dar_paso_aleatorio(partida, mapa, azar, prohibido)
        tiempos.append(time.perf_counter() - t0)
        perseguidores.append(_cazadores_en_rango(partida, mapa))   # fuera de la medición del ciclo
    servicio.cerrar()
    return tiempos, activos, perseguidores


def _cazadores_en_rango(partida, mapa) -> int:
    """Cazadores activos cuya distancia al jugador no supera su rango. Usa un buscador aparte para no alterar la medición."""
    activos = _cazadores_activos(mapa)
    rangos = [c.rango for c in activos if c.rango is not None]
    if not rangos:
        return 0
    contador = BuscadorRutas()
    contador.calcular_o_reutilizar(mapa, partida._jugador.sala_actual, max(rangos))
    cantidad = 0
    for cazador in activos:
        distancia = contador.distancia(cazador.sala_actual)
        if cazador.rango is not None and distancia is not None and distancia <= cazador.rango:
            cantidad += 1
    return cantidad


def bench_ciclo_referencia(escala: float = 1.0, corridas: int = 3):
    """Ciclo completo de Partida sobre la cripta de referencia de fixtures con muchos cazadores activos."""
    ciclos = max(20, int(100 * escala))
    calentamiento = max(60, int(PASOS_CALENTAMIENTO_REFERENCIA * escala))
    peores, medianas, en_rango = [], [], []
    for _ in range(corridas):
        tiempos, activos, perseguidores = _correr_referencia(ciclos, calentamiento)
        peores.append(max(tiempos))
        medianas.append(_mediana(tiempos))
        en_rango.extend(perseguidores)
    peor = _mediana(peores)
    cumple = "CUMPLE" if peor * 1000 < LIMITE_CICLO_MS else "NO CUMPLE"
    detalle = ", ".join(_ms(p) for p in peores)
    return [Resultado(
        "ciclo_referencia", f"{cripta_de_referencia().id}, {activos} cazadores activos al medir, "
                            f"en persecución por ciclo: promedio {sum(en_rango) / len(en_rango):.1f} y máximo {max(en_rango)}, "
                            f"{ciclos} ciclos x {corridas} corridas",
        peor, 1,
        f"ciclo típico {_ms(_mediana(medianas))} ms, peor caso {_ms(peor)} ms (peor de cada corrida: {detalle} ms) "
        f"-> {cumple} el límite de {LIMITE_CICLO_MS:.0f} ms")]


SEMILLA_NIEBLA = 20261118


def _elegir_fixture_referencia():
    """Carga el fixture íntegro de mayor tamaño sin fijar el identificador."""
    elegido = cripta_de_referencia().id
    cliente = ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH))
    general = cliente.obtener_general(elegido)
    version = cliente.obtener_version_cripta(elegido)
    if general.version != version.version:
        raise ValueError(f"Versión inconsistente en el fixture {elegido}")
    mapa = CriptaMapa()
    for pagina in range(1, general.paginas + 1):
        mapa.agregar_pagina(cliente.obtener_pagina_esqueleto(elegido, pagina))
    mapa.sincronizar_puertas()
    salas = mapa.todas_las_salas()
    if len(salas) != general.salas_total:
        raise ValueError(f"El fixture {elegido} declara {general.salas_total} salas y contiene {len(salas)}")
    puertas_abiertas = 0
    for sala in salas:
        for direccion, _destino in mapa.vecinos(sala.id):
            if not mapa.puerta_transitable(sala.id, direccion):
                mapa.abrir_puerta(sala.id, direccion)
                puertas_abiertas += 1
    conocimiento = ConocimientoJugador(mapa, general.sala_inicial)
    for sala in salas:
        conocimiento.al_entrar(sala.id, False)
    salidas = sum(len(mapa.vecinos(sala.id)) for sala in salas)
    azar = random.Random(SEMILLA_NIEBLA)
    consultas = []
    pares_probados = 0
    max_intentos = 1200
    pares_vistos = []
    while len(consultas) < 12 and pares_probados < max_intentos:
        origen = salas[azar.randrange(len(salas))].id
        destino = salas[azar.randrange(len(salas))].id
        consulta = (origen, destino)
        pares_probados += 1
        if origen == destino or consulta in pares_vistos:
            continue
        pares_vistos.append(consulta)
        if siguiente_paso(conocimiento, origen, destino) is not None:
            consultas.append(consulta)
    return {"id": elegido, "salas": len(salas), "salidas": salidas,
            "mapa": mapa, "conocimiento": conocimiento, "consultas": consultas,
            "semilla": SEMILLA_NIEBLA, "puertas_abiertas": puertas_abiertas,
            "pares_probados": pares_probados, "pares_con_ruta": len(consultas)}


def _seleccion_lineal(conocimiento, origen, destino, proyeccion=None):
    """Calcula el primer paso por selección lineal, solo como referencia de medición."""
    if origen == destino or conocimiento.estado_de_sala(destino) != "explorada":
        return None
    salas = conocimiento.proyectar() if proyeccion is None else proyeccion
    maximo = max((sala.id_sala for sala in salas), default=-1)
    distancias = [None] * (maximo + 1)
    visitadas = [False] * (maximo + 1)
    entrantes = [[] for _ in distancias]
    for sala in salas:
        if sala.estado != "explorada":
            continue
        for salida in sala.salidas:
            if salida.estado_puerta == "abierta":
                entrantes[salida.id_sala_destino].append((sala.id_sala, salida.costo))
    distancias[destino] = 0
    while True:
        actual = None
        for sala_id in range(len(distancias)):
            if (distancias[sala_id] is not None and not visitadas[sala_id]
                    and (actual is None or (distancias[sala_id], sala_id) <
                         (distancias[actual], actual))):
                actual = sala_id
        if actual is None:
            break
        visitadas[actual] = True
        for anterior, costo in entrantes[actual]:
            nuevo = distancias[actual] + costo
            if distancias[anterior] is None or nuevo < distancias[anterior]:
                distancias[anterior] = nuevo
    mejor = None
    paso = None
    sala_origen = conocimiento.sala_conocida(origen)
    for salida in sala_origen.salidas:
        resto = distancias[salida.id_sala_destino]
        if salida.estado_puerta != "abierta" or resto is None:
            continue
        total = salida.costo + resto
        if (mejor is None or total < mejor or
                (total == mejor and salida.id_sala_destino < paso[0])):
            mejor = total
            paso = (salida.id_sala_destino, salida.direccion)
    return paso[1] if paso is not None else None


def _comparar_costos_con_mapa(referencia):
    """Contrasta los costos conocidos con consultas al mapa real para consultas iguales."""
    conocimiento, mapa = referencia["conocimiento"], referencia["mapa"]
    for origen, destino in referencia["consultas"]:
        guardado = _siguiente_paso_costos_guardados(conocimiento, origen, destino)
        if guardado != _siguiente_paso_costos_mapa(conocimiento, mapa, origen, destino):
            return False
    return True


def _siguiente_paso_costos_guardados(conocimiento, origen, destino, proyeccion=None):
    """Busca con heap usando los costos guardados en la proyección conocida."""
    if (conocimiento.estado_de_sala(origen) != "explorada"
            or conocimiento.estado_de_sala(destino) != "explorada" or origen == destino):
        return None
    salas = conocimiento.proyectar() if proyeccion is None else proyeccion
    distancias = [None] * (max(s.id_sala for s in salas) + 1)
    entrantes = [[] for _ in distancias]
    for sala in salas:
        if sala.estado != "explorada":
            continue
        for salida in sala.salidas:
            if salida.estado_puerta == "abierta":
                entrantes[salida.id_sala_destino].append((sala.id_sala, salida.costo))
    distancias[destino] = 0
    pendientes = HeapMinimo()
    pendientes.insertar((0, destino))
    while not pendientes.esta_vacio():
        costo_actual, actual = pendientes.eliminar_minimo()
        if costo_actual != distancias[actual]:
            continue
        for anterior, costo in entrantes[actual]:
            nuevo = costo_actual + costo
            if distancias[anterior] is None or nuevo < distancias[anterior]:
                distancias[anterior] = nuevo
                pendientes.insertar((nuevo, anterior))
    mejor = None
    paso = None
    for salida in conocimiento.sala_conocida(origen).salidas:
        resto = distancias[salida.id_sala_destino]
        if salida.estado_puerta != "abierta" or resto is None:
            continue
        total = salida.costo + resto
        if mejor is None or total < mejor or (total == mejor and salida.id_sala_destino < paso[0]):
            mejor, paso = total, (salida.id_sala_destino, salida.direccion)
    return paso[1] if paso else None


def _siguiente_paso_costos_mapa(conocimiento, mapa, origen, destino, proyeccion=None):
    """Busca con heap consultando al mapa el costo de cada arista relajada."""
    if (conocimiento.estado_de_sala(origen) != "explorada"
            or conocimiento.estado_de_sala(destino) != "explorada" or origen == destino):
        return None
    salas = conocimiento.proyectar() if proyeccion is None else proyeccion
    distancias = [None] * (max(s.id_sala for s in salas) + 1)
    entrantes = [[] for _ in distancias]
    for sala in salas:
        if sala.estado != "explorada":
            continue
        for salida in sala.salidas:
            if salida.estado_puerta == "abierta":
                entrantes[salida.id_sala_destino].append((sala.id_sala, salida.direccion))
    distancias[destino] = 0
    pendientes = HeapMinimo()
    pendientes.insertar((0, destino))
    while not pendientes.esta_vacio():
        costo_actual, actual = pendientes.eliminar_minimo()
        if costo_actual != distancias[actual]:
            continue
        for anterior, direccion in entrantes[actual]:
            costo = mapa.costo_de_conexion(anterior, direccion)
            nuevo = costo_actual + costo
            if distancias[anterior] is None or nuevo < distancias[anterior]:
                distancias[anterior] = nuevo
                pendientes.insertar((nuevo, anterior))
    mejor = None
    paso = None
    for salida in conocimiento.sala_conocida(origen).salidas:
        resto = distancias[salida.id_sala_destino]
        if salida.estado_puerta != "abierta" or resto is None:
            continue
        total = mapa.costo_de_conexion(origen, salida.direccion) + resto
        if mejor is None or total < mejor or (total == mejor and salida.id_sala_destino < paso[0]):
            mejor, paso = total, (salida.id_sala_destino, salida.direccion)
    return paso[1] if paso else None


def _resumen_tiempos(tiempos):
    return _mediana(tiempos), max(tiempos)


def _comparar_revelacion(referencia, escala, semilla, repeticiones=3):
    """Mide actualización incremental y pasada ingenua para los mismos ingresos."""
    mapa = referencia["mapa"]
    salas = mapa.todas_las_salas()
    azar = random.Random(semilla)
    entradas = [salas[azar.randrange(len(salas))].id for _ in range(max(1, int(escala)))]
    tiempos_incrementales = []
    tiempos_ingenuos = []
    equivalente = True
    for _ in range(repeticiones):
        incremental = ConocimientoJugador(mapa, salas[0].id)
        ingenuo = ["desconocida"] * (max(s.id for s in salas) + 1)
        ingenuo[salas[0].id] = "explorada"
        for _direccion, destino in mapa.vecinos(salas[0].id):
            ingenuo[destino] = "avistada"
        for entrada in entradas:
            t0 = time.perf_counter()
            incremental.al_entrar(entrada, True)
            tiempos_incrementales.append(time.perf_counter() - t0)
            t0 = time.perf_counter()
            ingenuo[entrada] = "explorada"
            for _direccion, destino in mapa.vecinos(entrada):
                ingenuo[destino] = "explorada"
            for sala in salas:
                for _direccion, destino in mapa.vecinos(sala.id):
                    if ingenuo[sala.id] == "explorada" and ingenuo[destino] == "desconocida":
                        ingenuo[destino] = "avistada"
            tiempos_ingenuos.append(time.perf_counter() - t0)
        equivalente = equivalente and all(
            incremental.estado_de_sala(s.id) == ingenuo[s.id] for s in salas
        )
    return equivalente, _resumen_tiempos(tiempos_incrementales), _resumen_tiempos(tiempos_ingenuos)


def _comparar_reversion(referencia, escala, semilla, repeticiones=3):
    """Mide registrar y revertir frente a registrar y restaurar una copia."""
    mapa = referencia["mapa"]
    salas = mapa.todas_las_salas()
    azar = random.Random(semilla)
    entradas = [salas[azar.randrange(len(salas))].id for _ in range(max(1, int(escala)))]
    tiempos_inversas = []
    tiempos_copia = []
    equivalente = True
    cantidad = 0
    for _ in range(repeticiones):
        conocimiento = ConocimientoJugador(mapa, salas[0].id)
        historial = HistorialRetroceso()
        conocimiento.registrador = historial.registrar_cambio
        inicial = copy.deepcopy(conocimiento.exportar_celdas())
        historial.iniciar_intervalo()
        t0 = time.perf_counter()
        for entrada in entradas:
            conocimiento.al_entrar(entrada, True)
        historial.cerrar_intervalo()
        cantidad = historial.deshacer_ultimo_intervalo()
        tiempos_inversas.append(time.perf_counter() - t0)
        equivalente = equivalente and conocimiento.exportar_celdas() == inicial
        t0 = time.perf_counter()
        conocimiento.registrador = None
        copia = copy.deepcopy(inicial)
        for entrada in entradas:
            conocimiento.al_entrar(entrada, True)
        conocimiento.importar_celdas(copia)
        tiempos_copia.append(time.perf_counter() - t0)
        equivalente = equivalente and conocimiento.exportar_celdas() == inicial
    return equivalente, _resumen_tiempos(tiempos_inversas), _resumen_tiempos(tiempos_copia), cantidad


def bench_niebla_rutas(escala: float = 1.0):
    """Mide rutas, revelación incremental y reversión con fixtures offline."""
    referencia = _elegir_fixture_referencia()
    consultas = referencia["consultas"]
    dato = (f"fixture={referencia['id']}, salas={referencia['salas']}, salidas={referencia['salidas']}, "
            f"puertas abiertas={referencia['puertas_abiertas']}, pares probados={referencia['pares_probados']}, "
            f"pares con ruta={referencia['pares_con_ruta']}, semilla={referencia['semilla']}, "
            f"Python={platform.python_version()}")
    conocimiento = referencia["conocimiento"]
    consultas_con_ruta = [(origen, destino) for origen, destino in consultas
                          if siguiente_paso(conocimiento, origen, destino) is not None]
    if not consultas_con_ruta:
        raise ValueError("Ninguna consulta de niebla_rutas tiene una ruta")
    tiempos_produccion = []
    tiempos_lineal = []
    tiempos_guardados = []
    tiempos_mapa = []
    equivalentes_costos = True
    for origen, destino in consultas_con_ruta:
        for tiempos, funcion in (
                (tiempos_produccion, lambda: siguiente_paso(conocimiento, origen, destino)),
                (tiempos_lineal, lambda: _seleccion_lineal(conocimiento, origen, destino)),
                (tiempos_guardados, lambda: _siguiente_paso_costos_guardados(
                    conocimiento, origen, destino)),
                (tiempos_mapa, lambda: _siguiente_paso_costos_mapa(
                    conocimiento, referencia["mapa"], origen, destino))):
            for _ in range(3):
                inicio = time.perf_counter()
                obtenido = funcion()
                tiempos.append(time.perf_counter() - inicio)
                if tiempos is tiempos_guardados or tiempos is tiempos_mapa:
                    equivalentes_costos = equivalentes_costos and obtenido == siguiente_paso(
                        conocimiento, origen, destino)
    mediana_produccion, maximo_produccion = _resumen_tiempos(tiempos_produccion)
    mediana_lineal, maximo_lineal = _resumen_tiempos(tiempos_lineal)
    mediana_guardados, maximo_guardados = _resumen_tiempos(tiempos_guardados)
    mediana_mapa, maximo_mapa = _resumen_tiempos(tiempos_mapa)
    cumple = "CUMPLE" if maximo_produccion * 1000 <= LIMITE_PASO_MS else "NO CUMPLE"
    resultado = [Resultado("niebla_rutas", f"ruta de producción, {len(consultas_con_ruta)} consultas con ruta",
                           mediana_produccion, 1,
                           f"mediana por cálculo {_ms(mediana_produccion)} ms, máximo por cálculo "
                           f"{_ms(maximo_produccion)} ms. {cumple} el límite de {LIMITE_PASO_MS:.0f} ms. {dato}")]
    resultado.append(Resultado("niebla_rutas", "selección lineal manual, mismas consultas",
                               mediana_lineal, 1,
                               f"mediana por cálculo {_ms(mediana_lineal)} ms, máximo por cálculo "
                               f"{_ms(maximo_lineal)} ms. {dato}"))
    resultado.append(Resultado("niebla_rutas", "costos guardados frente a costo_de_conexion",
                               mediana_guardados, 1,
                               f"costos guardados: mediana {_ms(mediana_guardados)} ms y máximo "
                               f"{_ms(maximo_guardados)} ms. Consulta al mapa: mediana {_ms(mediana_mapa)} ms "
                               f"y máximo {_ms(maximo_mapa)} ms. Equivalencia con ruta real: "
                               f"{equivalentes_costos}. {dato}"))
    for tamano in (max(1, int(10 * escala)), max(1, int(50 * escala)), max(1, int(200 * escala))):
        semilla = referencia["semilla"] + tamano
        ok, incremental, ingenua = _comparar_revelacion(referencia, tamano, semilla)
        resultado.append(Resultado("niebla_rutas", f"revelación, R={tamano}", incremental[0], 1,
                                   f"incremental: mediana {_ms(incremental[0])} ms y máximo "
                                   f"{_ms(incremental[1])} ms. Pasada ingenua: mediana "
                                   f"{_ms(ingenua[0])} ms y máximo {_ms(ingenua[1])} ms. "
                                   f"Equivalencia: {ok}. {dato}"))
    cantidad = max(1, int(20 * escala))
    ok, inversas_tiempo, copia_tiempo, inversas = _comparar_reversion(
        referencia, cantidad, referencia["semilla"])
    resultado.append(Resultado("niebla_rutas", "reversión por inversas frente a copia completa",
                               inversas_tiempo[0], max(1, inversas),
                               f"registrar y revertir por inversas: mediana {_ms(inversas_tiempo[0])} ms "
                               f"y máximo {_ms(inversas_tiempo[1])} ms. Copiar y restaurar: mediana "
                               f"{_ms(copia_tiempo[0])} ms y máximo {_ms(copia_tiempo[1])} ms. "
                               f"inversas={inversas}. Equivalencia: {ok}. {dato}"))
    return resultado


def bench_historial_cazadores(escala: float = 1.0):
    """Costo del retroceso con cazadores activos (P2 5.6) sobre la cripta de referencia, frente a la carga historial.
    Cada acción se ejecuta, se revierte con la acción pergamino real y se vuelve a ejecutar."""
    acciones = max(60, int(500 * escala))
    calentamiento = max(60, int(PASOS_CALENTAMIENTO_REFERENCIA * escala))
    cripta = cripta_de_referencia()
    servicio = ServicioPartida(ClienteGeneral(ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH))),
                               ContadorSolicitudes(), asincrono=False)
    servicio.iniciar_nueva(cripta.id, semilla=SEMILLA_BENCH)
    try:
        partida = servicio.partida
        mapa = partida._mapa
        partida._jugador.vida_max = partida._jugador.vida = 10 ** 9
        prohibido = servicio.datos_generales.sala_salida
        azar = random.Random(SEMILLA_CARGAS_TERRENO)
        _activar_cazadores_reales(partida, mapa)
        cazadores = len(_cazadores_activos(mapa))
        for _ in range(calentamiento):
            _dar_paso_aleatorio(partida, mapa, azar, prohibido)
        ficha = servicio._catalogo.obtener("itm_pergamino_retroceso")
        historial = partida._historial
        inversas, tiempos = [], []
        deshacer = historial.deshacer_ultimo_intervalo


        def deshacer_contando():
            cantidad = deshacer()
            inversas.append(cantidad)
            return cantidad


        historial.deshacer_ultimo_intervalo = deshacer_contando
        try:
            gc.collect()
            for numero in range(acciones):
                accion = _paso_aleatorio_aceptado(partida, mapa, azar, prohibido)
                partida._jugador.inventario.recoger(ObjetoInventario(f"pergamino-bench-{numero}", ficha))
                inicio = time.perf_counter()
                revertida = partida.ejecutar_accion(Accion("pergamino"))
                tiempos.append(time.perf_counter() - inicio)
                if not revertida.aceptada or not partida.ejecutar_accion(accion).aceptada:
                    raise ValueError(f"No se pudo revertir y repetir la acción {numero + 1} de la medición")
        finally:
            del historial.deshacer_ultimo_intervalo
    finally:
        servicio.cerrar()
    sintetica = bench_historial(escala)
    registrar = next(r for r in sintetica if r.caso.startswith("registrar acción (6 inversas)"))
    deshacer_sintetico = next(r for r in sintetica if r.caso.startswith("deshacer 5 acciones"))
    deshacer_us = deshacer_sintetico.micros_por_operacion
    medio_us = _mediana(tiempos) * 1e6
    por_inversa = sum(tiempos) * 1e6 / sum(inversas)
    contexto = f"{cripta.id}, {cazadores} cazadores activos al medir, {acciones} acciones"
    return [
        Resultado("historial_cazadores", f"{contexto}: operaciones inversas por acción", 0.0, 1,
                  f"mediana {_mediana(inversas)} y máximo {max(inversas)} inversas por acción, mínimo {min(inversas)}. "
                  f"La carga sintética historial usa 6 inversas por acción y no tiene cazadores", es_razon=True),
        Resultado("historial_cazadores", f"{contexto}: revertir el último intervalo como el pergamino",
                  sum(tiempos), acciones,
                  f"tiempo de la acción pergamino completa: mediana {medio_us:.1f} µs y máximo {max(tiempos) * 1e6:.1f} µs, "
                  f"{por_inversa:.2f} µs por inversa en promedio. Carga sintética historial (6 inversas por acción, "
                  f"sin cazadores): deshacer {deshacer_us:.2f} µs por acción, {deshacer_us / 6:.2f} µs por inversa, "
                  f"registrar {registrar.micros_por_operacion:.2f} µs por acción. "
                  f"Con cazadores la mediana de revertir es {medio_us / deshacer_us:.1f}x la sintética")]


# ================================== 11. LÍNEA DE TIEMPO (capacidad 004, FR-LIN-014 a FR-LIN-018)
SEMILLA_LINEA_TIEMPO = 20261117
ACCIONES_LINEA_COMPLETA = 5000        # a escala 1 (FR-LIN-018)
ACCIONES_LINEA_MINIMAS = 250          # con escalas pequeñas, para que la prueba de humo sea rápida
CONSULTAS_LINEA_COMPLETA = 16         # consultas aleatorias a escala 1, más las de frontera
CONSULTAS_LINEA_MINIMAS = 4
VIDA_MAXIMA_LINEA = 10 ** 9           # se fija en los datos generales ANTES de iniciar: la reconstrucción parte del estado inicial
LIMITE_CONSULTA_MS = 50.0             # P2 §6.1
K_COMPARACION_LINEA = 100
ESCENARIOS_K_LINEA = (("K=50", 50), ("K=100", 100), ("K=500", 500), ("K=1000", 1000),
                     ("sin puntos periódicos", None))
ESTIMACION_MEMORIA = ("estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, "
                      "sin descontar lo que comparten (cota superior)")


class _ClienteMedido:
    """Cliente de fixtures que cuenta sus llamadas y sube la vida máxima del jugador en los datos generales."""


    def __init__(self, base, vida_maxima: int):
        self._base = base
        self._vida_maxima = vida_maxima
        self.llamadas = 0


    def __getattr__(self, nombre):
        metodo = getattr(self._base, nombre)


        def llamar(*argumentos):
            self.llamadas += 1
            resultado = metodo(*argumentos)
            if nombre == "obtener_general":
                resultado = replace(resultado, jugador=replace(resultado.jugador, vida_max=self._vida_maxima))
            return resultado
        return llamar


class _CorridaLinea:
    """Una partida de medición ya jugada: la partida, lo que costó cada acción y los registros para la inversión."""


    def __init__(self):
        self.cliente = None
        self.servicio = None
        self.partida = None
        self.tiempos = []              # segundos de cada acción del jugador
        self.registro = 0.0            # segundos en anotar acciones y checkpoints en la línea
        self.registros_inversion = []  # por acción, los valores anteriores de lo que cambió
        self.segundos_inversion = 0.0  # lo que cuesta calcular esos registros
        self.foto_final = None
        self.salas = 0
        self.salidas = 0


def _foto_basica(partida):
    # Lo visible del estado en una lista mutable, para la alternativa de inversión
    jugador, sala = partida._jugador, partida._sala_actual()
    inventario = tuple((o.instancia_id, getattr(o.ficha, "id", "")) for o in jugador.inventario.objetos_en_orden())
    enemigos = tuple((e.instancia, e.vida, e.vida_max) for e in partida._enemigos_vista(sala))
    return [sala.id, jugador.vida, jugador.vida_max, jugador.ataque_efectivo, jugador.defensa_efectiva,
            jugador.velocidad, inventario, partida._efectos_activos(), enemigos]


def _foto_de_resumen(resumen):
    # La misma lista armada desde un ResumenHistorico
    inventario = tuple((o.instancia_id, o.ficha_id) for o in resumen.inventario)
    enemigos = tuple((e.instancia, e.vida, e.vida_max) for e in resumen.enemigos)
    return [resumen.sala_id, resumen.vida, resumen.vida_max, resumen.ataque, resumen.defensa, resumen.velocidad,
            inventario, resumen.efectos_activos, enemigos]


def _cambios_entre(antes, despues):
    # Pares (posición, valor anterior) de lo que cambió: es lo único que guarda la alternativa de inversión
    return tuple((i, antes[i]) for i in range(len(antes)) if antes[i] != despues[i])


def _foto_antes_de_la_accion(foto_final, registros, k):
    # Deshace desde la última acción hasta la k para quedar justo antes de ella
    foto = list(foto_final)
    for j in range(len(registros) - 1, k - 2, -1):
        for posicion, anterior in registros[j]:
            foto[posicion] = anterior
    return foto


def _tamano_profundo(objeto) -> int:
    # Bytes de un objeto y de todo lo que contiene: tuplas, listas, dataclasses y objetos con __slots__
    total = sys.getsizeof(objeto)
    if isinstance(objeto, (tuple, list)):
        for elemento in objeto:
            total += _tamano_profundo(elemento)
    elif is_dataclass(objeto) and not isinstance(objeto, type):
        for campo in fields(objeto):
            total += _tamano_profundo(getattr(objeto, campo.name))
    elif hasattr(objeto, "__slots__"):
        for nombre in objeto.__slots__:
            if hasattr(objeto, nombre):
                total += _tamano_profundo(getattr(objeto, nombre))
    return total


def _kib(bytes_: int) -> str:
    return f"{bytes_ / 1024:.1f}"


def _acciones_de_la_carga(escala: float) -> int:
    return max(ACCIONES_LINEA_MINIMAS, int(ACCIONES_LINEA_COMPLETA * escala))


def _consultas_de_la_carga(escala: float) -> int:
    return max(CONSULTAS_LINEA_MINIMAS, int(CONSULTAS_LINEA_COMPLETA * escala))


@contextmanager
def _jugar_linea(acciones: int, k: int | None, id_cripta: str, medir_inversion: bool = False):
    """Juega una partida con puntos de control creados durante las acciones medidas."""
    corrida = _CorridaLinea()
    corrida.cliente = _ClienteMedido(ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH)), VIDA_MAXIMA_LINEA)
    frecuencia = acciones + 1 if k is None else k
    corrida.servicio = ServicioPartida(ClienteGeneral(corrida.cliente), ContadorSolicitudes(),
                                       asincrono=False, checkpoint_cada=frecuencia)
    try:
        corrida.servicio.iniciar_nueva(id_cripta, semilla=SEMILLA_LINEA_TIEMPO)
        partida = corrida.partida = corrida.servicio.partida
        mapa = partida._mapa
        corrida.salas = len(mapa)
        corrida.salidas = sum(len(mapa.vecinos(sala.id)) for sala in mapa.todas_las_salas())
        registrar = partida._registrar_en_linea
        ejecutar = partida.ejecutar_accion


        def registrar_midiendo(*argumentos):
            inicio = time.perf_counter()
            registrar(*argumentos)
            corrida.registro += time.perf_counter() - inicio


        def ejecutar_midiendo(accion):
            inicio = time.perf_counter()
            resultado = ejecutar(accion)
            duracion = time.perf_counter() - inicio
            if resultado.aceptada:
                corrida.tiempos.append(duracion)
            return resultado


        partida._registrar_en_linea = registrar_midiendo
        partida.ejecutar_accion = ejecutar_midiendo
        prohibido = corrida.servicio.datos_generales.sala_salida
        azar = random.Random(SEMILLA_LINEA_TIEMPO)
        antes = _foto_basica(partida) if medir_inversion else None
        try:
            gc.collect()
            for _ in range(acciones):
                _dar_paso_aleatorio(partida, mapa, azar, prohibido)
                if medir_inversion:
                    inicio = time.perf_counter()
                    despues = _foto_basica(partida)
                    corrida.registros_inversion.append(_cambios_entre(antes, despues))
                    corrida.segundos_inversion += time.perf_counter() - inicio
                    antes = despues
        finally:
            del partida._registrar_en_linea
            del partida.ejecutar_accion
        corrida.foto_final = antes
        linea = partida.linea_tiempo()
        if len(linea) != acciones or len(corrida.tiempos) != acciones:
            raise ValueError(f"La partida de medición registró {len(linea)} acciones y "
                             f"{len(corrida.tiempos)} ciclos de los {acciones} esperados")
        _verificar_cadencia(linea, k)
        yield corrida
    finally:
        corrida.servicio.cerrar()


def _verificar_cadencia(linea: LineaTiempo, k: int | None) -> None:
    posiciones = [punto.numero_acciones for punto in linea._puntos]
    esperadas = [] if k is None else list(range(k, len(linea) + 1, k))
    if posiciones != esperadas:
        raise ValueError(f"Cadencia de puntos incorrecta para K={k}: {posiciones}, se esperaba {esperadas}")


def _posiciones_de_consulta(acciones: int, reloj: int, cantidad: int):
    """Muestra pseudoaleatoria y estados inmediatamente anteriores a puntos de control."""
    azar = random.Random(SEMILLA_LINEA_TIEMPO + 1)
    posiciones = []
    for i in range(cantidad):
        posiciones.append(("accion", azar.randint(1, acciones)) if i % 2 == 0 else ("instante", azar.randint(0, reloj)))
    for _, k in ESCENARIOS_K_LINEA:
        if k is not None and k <= acciones:
            for numero in (k, acciones // k * k):
                posicion = ("accion", numero)
                if posicion not in posiciones:
                    posiciones.append(posicion)
    return posiciones


def _tiempos_de_consulta(partida, posiciones):
    tiempos = []
    gc.collect()
    for tipo, valor in posiciones:
        inicio = time.perf_counter()
        if tipo == "accion":
            partida.consultar_accion(valor)
        else:
            partida.consultar_instante(valor)
        tiempos.append(time.perf_counter() - inicio)
    return tiempos


def _memoria_de_la_linea(linea: LineaTiempo):
    # (acciones, ajustes, checkpoints) en bytes, con la estimación de _tamano_profundo
    acciones = _tamano_profundo(linea._acciones) + _tamano_profundo(linea._tiempos)
    ajustes = _tamano_profundo(linea._ajustes_posicion) + _tamano_profundo(linea._ajustes_instancias)
    return acciones, ajustes, _tamano_profundo(linea._puntos)


def _resultado_de_escenario(etiqueta, corrida, posiciones):
    partida = corrida.partida
    linea = partida.linea_tiempo()
    tiempos = _tiempos_de_consulta(partida, posiciones)
    ordenar_auto(tiempos)
    cantidad = len(tiempos)
    mediana = (tiempos[(cantidad - 1) // 2] + tiempos[cantidad // 2]) / 2
    peor_consulta = tiempos[-1]
    peor_ciclo = max(corrida.tiempos)
    acciones, ajustes, puntos = _memoria_de_la_linea(linea)
    cumple_consulta = "CUMPLE" if peor_consulta * 1000 < LIMITE_CONSULTA_MS else "NO CUMPLE"
    cumple_ciclo = "CUMPLE" if peor_ciclo * 1000 < LIMITE_CICLO_MS else "NO CUMPLE"
    nota = (f"memoria de la línea {_kib(acciones + ajustes + puntos)} KiB (acciones {_kib(acciones)}, "
            f"ajustes {_kib(ajustes)}, puntos {_kib(puntos)}). "
            f"registro medio {corrida.registro / len(linea) * 1e6:.1f} µs/acción, incluida la captura cuando toca. "
            f"Consulta: mediana {_ms(mediana)} ms, máximo observado {_ms(peor_consulta)} ms -> "
            f"{cumple_consulta} el límite de {LIMITE_CONSULTA_MS:.0f} ms (P2 §6.1). "
            f"peor ciclo {_ms(peor_ciclo)} ms -> {cumple_ciclo} el límite de {LIMITE_CICLO_MS:.0f} ms. "
            f"{ESTIMACION_MEMORIA}")
    return Resultado("linea_tiempo", f"{etiqueta}: {len(linea)} acciones, {linea.cantidad_checkpoints()} puntos periódicos, "
                                     f"{cantidad} consultas", sum(tiempos), cantidad, nota)


def _comparar_inversion(corrida, linea, posiciones):
    """T030: re-simular desde un checkpoint (elegida) frente a deshacer cambios serializables desde el final (descartada)."""
    partida, n = corrida.partida, len(linea)
    por_accion = [valor for tipo, valor in posiciones if tipo == "accion"]
    tiempos_resimular = _tiempos_de_consulta(partida, [("accion", k) for k in por_accion])
    tiempos_inversion, coinciden = [], 0
    gc.collect()
    for k in por_accion:
        inicio = time.perf_counter()
        foto = _foto_antes_de_la_accion(corrida.foto_final, corrida.registros_inversion, k)
        tiempos_inversion.append(time.perf_counter() - inicio)
        if foto == _foto_de_resumen(partida.consultar_accion(k)):
            coinciden += 1
    acciones, ajustes, puntos = _memoria_de_la_linea(linea)
    memoria_resimular = acciones + ajustes + puntos
    memoria_inversion = _tamano_profundo(corrida.registros_inversion) + _tamano_profundo(corrida.foto_final)
    reg_resimular = corrida.registro / n
    reg_inversion = corrida.segundos_inversion / n
    return [
        Resultado("linea_tiempo", f"re-simular desde checkpoint (elegida): {n} acciones, {len(por_accion)} consultas por acción",
                  _mediana(tiempos_resimular), len(por_accion),
                  f"registrar {reg_resimular * 1e6:.1f} µs por acción (incluye crear los checkpoints), memoria "
                  f"{_kib(memoria_resimular)} KiB, consulta mediana {_ms(_mediana(tiempos_resimular))} ms y máximo "
                  f"{_ms(max(tiempos_resimular))} ms. Reconstruye el estado completo, con azar y agenda"),
        Resultado("linea_tiempo", f"reconstruir hacia atrás con cambios serializables (descartada): {n} acciones, "
                                  f"{len(por_accion)} consultas por acción",
                  _mediana(tiempos_inversion), len(por_accion),
                  f"registrar {reg_inversion * 1e6:.1f} µs por acción, memoria {_kib(memoria_inversion)} KiB, consulta "
                  f"mediana {_ms(_mediana(tiempos_inversion))} ms y máximo {_ms(max(tiempos_inversion))} ms (deshace "
                  f"desde el final, así que el costo crece con las acciones que faltan). Modelo de cota inferior: "
                  f"solo registra los 9 campos visibles (sala, vida, estadísticas, inventario, efectos y enemigos de la sala), "
                  f"no el azar, la agenda ni el mapa conocido. Coincide con la re-simulación en {coinciden} de {len(por_accion)} "
                  f"consultas. {ESTIMACION_MEMORIA}")]


def _comparar_busquedas(corrida, linea):
    """T031: búsqueda binaria manual (elegida) frente a lineal (descartada) del límite temporal y del checkpoint."""
    n = len(linea)
    reloj = corrida.partida.vista().tiempo
    azar = random.Random(SEMILLA_LINEA_TIEMPO + 2)
    consultas = 400
    instantes = [azar.randint(0, reloj) for _ in range(consultas)]
    numeros = [azar.randint(1, n) for _ in range(consultas)]
    tiempos_de_acciones = linea._tiempos
    puntos = linea._puntos


    def binaria_instante():
        inspecciones, resultados = 0, []
        for t in instantes:
            resultados.append(linea.contar_hasta_instante(t, True))
            inspecciones += linea.inspecciones_ultima_busqueda
        return inspecciones, resultados


    def lineal_instante():
        inspecciones, resultados = 0, []
        for t in instantes:
            cuenta = 0
            for valor in tiempos_de_acciones:
                inspecciones += 1
                if valor > t:
                    break
                cuenta += 1
            resultados.append(cuenta)
        return inspecciones, resultados


    def binaria_checkpoint():
        inspecciones, resultados = 0, []
        for k in numeros:
            punto = linea.buscar_checkpoint(k)
            inspecciones += linea.inspecciones_ultima_busqueda
            resultados.append(None if punto is None else punto.numero_acciones)
        return inspecciones, resultados


    def lineal_checkpoint():
        inspecciones, resultados = 0, []
        for k in numeros:
            elegido = None
            for punto in puntos:
                inspecciones += 1
                if punto.numero_acciones > k:
                    break
                elegido = punto.numero_acciones
            resultados.append(elegido)
        return inspecciones, resultados


    salida = []
    for nombre, elegida, descartada, tamano in (("límite temporal a acción", binaria_instante, lineal_instante, n),
                                                 ("checkpoint anterior", binaria_checkpoint, lineal_checkpoint,
                                                  len(puntos))):
        gc.collect()
        insp_b, res_b = elegida()
        insp_l, res_l = descartada()
        t_b, t_l = _medir(elegida), _medir(descartada)
        igual = "mismo resultado en las consultas" if res_b == res_l else "RESULTADOS DISTINTOS"
        salida.append(Resultado(
            "linea_tiempo", f"búsqueda {nombre}: binaria manual (elegida) frente a lineal (descartada), "
                            f"{tamano} elementos, {consultas} consultas", t_b, consultas,
            f"binaria {t_b / consultas * 1e6:.2f} µs por consulta con {insp_b / consultas:.1f} inspecciones en promedio; "
            f"lineal {t_l / consultas * 1e6:.2f} µs con {insp_l / consultas:.1f}; {_comparar('lineal', t_l, 'binaria', t_b)}; "
            f"{igual}. La binaria cuenta la llamada al método y la lineal es un bucle directo sobre la lista"))
    return salida


def _clonar_linea(base: LineaTiempo) -> LineaTiempo:
    clon = LineaTiempo(base.frecuencia)
    clon._acciones = base._acciones.copy()
    clon._tiempos = base._tiempos.copy()
    clon._puntos = base._puntos.copy()
    clon._ajustes_posicion = base._ajustes_posicion.copy()
    clon._ajustes_instancias = base._ajustes_instancias.copy()
    return clon


def _truncar_filtrando(linea: LineaTiempo, limite: int) -> int:
    """ALTERNATIVA DESCARTADA: recorre todas las acciones y checkpoints y conserva los que no pasan del límite.
    Devuelve cuántos registros examinó."""
    examinados = 0
    acciones, tiempos, puntos = [], [], []
    for indice in range(len(linea._acciones)):
        examinados += 1
        if indice < limite:
            acciones.append(linea._acciones[indice])
            tiempos.append(linea._tiempos[indice])
    for punto in linea._puntos:
        examinados += 1
        if punto.numero_acciones <= limite:
            puntos.append(punto)
    linea._acciones, linea._tiempos, linea._puntos = acciones, tiempos, puntos
    return examinados


def _comparar_recorte(base: LineaTiempo):
    """T032: recortar desde el final (elegida) frente a escanear y filtrar (descartada), como hace el pergamino."""
    n = len(base)
    repeticiones = 30
    segundos_elegida = segundos_descartada = 0.0
    examinados = quitados = 0
    for _ in range(repeticiones):
        linea = _clonar_linea(base)
        antes = len(linea._acciones) + linea.cantidad_checkpoints()
        gc.collect()
        inicio = time.perf_counter()
        linea.truncar(n - 1)
        segundos_elegida += time.perf_counter() - inicio
        quitados = antes - len(linea._acciones) - linea.cantidad_checkpoints()
        linea = _clonar_linea(base)
        gc.collect()
        inicio = time.perf_counter()
        examinados = _truncar_filtrando(linea, n - 1)
        segundos_descartada += time.perf_counter() - inicio
    return Resultado(
        "linea_tiempo", f"recorte por pergamino: desde el final (elegida) frente a escaneo y filtrado (descartada), "
                        f"{n} acciones, {repeticiones} repeticiones", segundos_elegida, repeticiones,
        f"desde el final {segundos_elegida / repeticiones * 1e6:.2f} µs y {quitados} registros procesados por recorte; "
        f"escaneo y filtrado {segundos_descartada / repeticiones * 1e6:.2f} µs y {examinados} registros examinados; "
        f"{_comparar('el filtrado', segundos_descartada, 'el recorte desde el final', segundos_elegida)}")


def _comparar_restauracion(corrida, linea):
    """T032: restaurar el estado de un checkpoint con la ruta que prepara salas (descartada) frente a la vía
    materializada sin precarga (elegida). La E/S se mide como llamadas al cliente de fixtures."""
    partida = corrida.partida
    punto = linea.buscar_checkpoint(len(linea) // 2)
    if punto is None:
        punto = linea.buscar_checkpoint(len(linea))
    if punto is None:
        return Resultado("linea_tiempo", "restauración de un checkpoint: sin checkpoints en esta escala", 0.0, 1,
                         "no hay un checkpoint desde el cual restaurar")
    estado = punto.estado[0]
    con_contenido = sum(1 for sala in estado.salas if sala.contenido_cargado)
    repeticiones = 5
    tiempos_materializada, tiempos_con_precarga = [], []
    llamadas_materializada = llamadas_con_precarga = 0
    for _ in range(repeticiones):
        gc.collect()
        antes = corrida.cliente.llamadas
        inicio = time.perf_counter()
        partida._crear_aislada(punto.estado)
        tiempos_materializada.append(time.perf_counter() - inicio)
        llamadas_materializada += corrida.cliente.llamadas - antes


        servicio = ServicioPartida(ClienteGeneral(corrida.cliente), ContadorSolicitudes(), asincrono=False)
        general, version = corrida.servicio.datos_generales, corrida.servicio.version_catalogo
        mapa = servicio._armar(general, version)     # el esqueleto se carga fuera de la medición
        gc.collect()
        antes = corrida.cliente.llamadas
        inicio = time.perf_counter()
        copia = Partida(general, mapa, servicio._catalogo, servicio._precarga, estado.semilla)
        with copia._historial.sin_registrar():
            copia._restaurar(estado)                 # restaurar_sala llama a preparar_sala en cada sala con contenido
        tiempos_con_precarga.append(time.perf_counter() - inicio)
        llamadas_con_precarga += corrida.cliente.llamadas - antes
        servicio.cerrar()
    t_m, t_p = _mediana(tiempos_materializada), _mediana(tiempos_con_precarga)
    return Resultado(
        "linea_tiempo", f"restauración de un checkpoint: vía materializada (elegida) frente a preparar salas (descartada), "
                        f"{con_contenido} salas con contenido, {repeticiones} repeticiones", t_m, repeticiones,
        f"materializada {_ms(t_m)} ms y {llamadas_materializada / repeticiones:.1f} llamadas al cliente por consulta; "
        f"con preparar_sala {_ms(t_p)} ms y {llamadas_con_precarga / repeticiones:.1f} llamadas "
        f"({con_contenido} llamadas a preparar_sala); {_comparar('preparar salas', t_p, 'la vía materializada', t_m)}. "
        f"Cada llamada al cliente de fixtures lee un archivo: es la E/S de la consulta")


def bench_linea_tiempo(escala: float = 1.0):
    """Mide la línea de tiempo con cinco corridas comparables y conserva las alternativas de la fase E."""
    acciones = _acciones_de_la_carga(escala)
    referencia = cripta_de_referencia()
    base = None
    resultados = []
    for etiqueta, k in ESCENARIOS_K_LINEA:
        with _jugar_linea(acciones, k, referencia.id) as corrida:
            linea = corrida.partida.linea_tiempo()
            reloj = corrida.partida._reloj.tiempo_actual
            carga = (linea._acciones, linea._tiempos, reloj)
            if base is None:
                base = carga
                posiciones = _posiciones_de_consulta(acciones, reloj, _consultas_de_la_carga(escala))
                resultados.append(Resultado(
                    "linea_tiempo", f"{referencia.id}, semilla {SEMILLA_LINEA_TIEMPO}, {acciones} acciones, "
                                    f"{corrida.salas} salas, {corrida.salidas} salidas",
                    sum(corrida.tiempos), acciones,
                    f"tiempo acumulado de ciclos de {etiqueta}. Cinco partidas independientes con la misma semilla "
                    f"y carga. Vida máxima {VIDA_MAXIMA_LINEA} "
                    f"fijada antes de iniciar. {len(posiciones)} consultas comunes por acción e instante, "
                    "incluidos estados inmediatamente anteriores a puntos de control"))
            elif carga != base:
                raise ValueError(f"La corrida {etiqueta} generó acciones o instantes distintos a la primera")
            resultados.append(_resultado_de_escenario(etiqueta, corrida, posiciones))


    with _jugar_linea(acciones, K_COMPARACION_LINEA, referencia.id, medir_inversion=True) as corrida:
        linea = corrida.partida.linea_tiempo()
        resultados += _comparar_inversion(corrida, linea, posiciones)
        resultados += _comparar_busquedas(corrida, linea)
        resultados.append(_comparar_recorte(linea))
        resultados.append(_comparar_restauracion(corrida, linea))
    return resultados


# ================================== 12. RESOLUBILIDAD (capacidad 003, FR-RES-020, SC-001, SC-007)
LLAVE_SALIDA_SINTETICA = "itm_llave_salida"
SALAS_POR_SEGMENTO_RESOLUBILIDAD = 20
LLAVES_RESOLUBILIDAD = (10, 20, 40)
REPETICIONES_RESOLUBILIDAD = 3
LIMITE_RESOLUBILIDAD_MS = 200.0
COSTO_MIN_RESOLUBILIDAD = 20
COSTO_MAX_RESOLUBILIDAD = 490


def _unir_salas(conexiones, origen, direccion, destino, azar, llave=None):
    """Agrega la conexión en los dos sentidos con un costo del azar. Con llave, la puerta queda cerrada."""
    costo = azar.randint(COSTO_MIN_RESOLUBILIDAD, COSTO_MAX_RESOLUBILIDAD)
    conexiones[origen].append((direccion, destino, llave, costo))
    conexiones[destino].append((direccion_opuesta(direccion), origen, llave, costo))


def _mapa_desde_conexiones(conexiones) -> CriptaMapa:
    """Arma el CriptaMapa con una página de esqueleto construida directamente con los DTO."""
    salas = []
    for sala in range(1, len(conexiones)):
        norte = sur = este = oeste = None
        for direccion, destino, llave, costo in conexiones[sala]:
            salida = SalidaDTO(destino, llave is not None, llave, None, costo)
            if direccion == "N":
                norte = salida
            elif direccion == "S":
                sur = salida
            elif direccion == "E":
                este = salida
            else:
                oeste = salida
        salas.append(SalaDTO(sala, f"Sala {sala}", norte, sur, este, oeste))
    mapa = CriptaMapa()
    mapa.agregar_pagina(PaginaEsqueletoDTO(pagina=1, total_paginas=1, salas=tuple(salas)))
    mapa.sincronizar_puertas()
    return mapa


def _generar_cripta_encadenada(k: int, salas_por_segmento: int, semilla: int):
    """Cripta de k segmentos en cadena, cada uno tras una puerta cerrada que exige la llave del segmento.
    La llave de salida es una ubicación más (como en llaves.json del API) y abre la última puerta.
    Devuelve (mapa, sala_inicial, sala_salida, llave_salida, ubicaciones de llaves)."""
    azar = random.Random(semilla)
    if k * salas_por_segmento == 1:
        salas_por_segmento = 2          # con una sola sala no hay puerta de salida, el mínimo viable son dos
    total = k * salas_por_segmento
    conexiones = [[] for _ in range(total + 1)]
    ids = [f"itm_llave_{i:04d}" for i in range(k)]
    ids[k - 1] = LLAVE_SALIDA_SINTETICA
    if salas_por_segmento == 1 and k >= 2:
        ids[k - 2] = LLAVE_SALIDA_SINTETICA          # la última sala es la salida y su puerta es la del segmento anterior
    ubicaciones = []
    for i in range(k):
        base = i * salas_por_segmento
        ultimo = i == k - 1
        utiles = salas_por_segmento - 1 if ultimo else salas_por_segmento
        if utiles == 0:
            continue
        lateral = base + utiles if utiles >= 2 else 0
        en_corredor = utiles - 1 if lateral else utiles
        for sala in range(base + 1, base + en_corredor):
            _unir_salas(conexiones, sala, "E", sala + 1, azar)
        ultima_del_corredor = base + en_corredor
        if lateral:
            _unir_salas(conexiones, base + 1 + azar.randrange(en_corredor), "N", lateral, azar)
            sala_llave = lateral
        else:
            sala_llave = base + 1 + azar.randrange(en_corredor)
        ubicaciones.append(LlaveUbicacionDTO(ids[i], sala_llave, None))
        destino = total if ultimo else base + salas_por_segmento + 1
        _unir_salas(conexiones, ultima_del_corredor, "E", destino, azar, ids[i])
    return _mapa_desde_conexiones(conexiones), 1, total, LLAVE_SALIDA_SINTETICA, tuple(ubicaciones)


def _verificador_de(cripta) -> VerificadorResolubilidad:
    mapa, sala_inicial, sala_salida, llave_salida, ubicaciones = cripta
    return VerificadorResolubilidad(mapa, sala_inicial, sala_salida, llave_salida, ubicaciones)


def bench_resolubilidad(escala: float = 1.0):
    """Recorrido incremental (elegida) frente a reiniciar el recorrido por cada llave (descartada)."""
    resultados = []
    por_segmento = max(1, int(SALAS_POR_SEGMENTO_RESOLUBILIDAD * escala))
    for base in LLAVES_RESOLUBILIDAD:
        k = max(1, int(base * escala))
        verificador = _verificador_de(_generar_cripta_encadenada(k, por_segmento, SEMILLA_BENCH))
        if not verificador.verificar().es_resoluble:
            raise ValueError(f"La cripta sintética de {k} llaves debería ser resoluble")
        t_incremental = _medir(verificador.verificar, REPETICIONES_RESOLUBILIDAD)
        t_ingenuo = _medir(verificador.verificar_ingenuo_reiniciado, REPETICIONES_RESOLUBILIDAD)
        salas = k * por_segmento
        resultados.append(Resultado("resolubilidad", f"{k} llaves encadenadas, {salas} salas: recorrido incremental (elegida)",
                                    t_incremental, 1))
        resultados.append(Resultado("resolubilidad", f"{k} llaves encadenadas, {salas} salas: recorrido ingenuo reiniciado (descartada)",
                                    t_ingenuo, 1, _comparar("recorrido_ingenuo_reiniciado", t_ingenuo,
                                                            "recorrido_incremental", t_incremental)))
    return resultados


def _cripta_publicada(cliente, id_cripta: str):
    """Lee de fixtures lo que necesita el verificador, sin pasar por el servicio para poder medir solo la verificación."""
    general = cliente.obtener_general(id_cripta)
    mapa = CriptaMapa()
    for pagina in range(1, general.paginas + 1):
        mapa.agregar_pagina(cliente.obtener_pagina_esqueleto(id_cripta, pagina))
    mapa.sincronizar_puertas()
    llaves = tuple(cliente.obtener_llaves(id_cripta))
    return mapa, general.sala_inicial, general.sala_salida, general.llave_salida, llaves


def bench_resolubilidad_cota(escala: float = 1.0):
    """Verificación de la cripta publicada con más salas contra el límite de 200 ms (SC-001)."""
    cliente = ClienteOffline(str(DIRECTORIO_FIXTURES_BENCH))
    elegida = elegir_cripta_de_referencia(cliente.listar_criptas())
    verificador = _verificador_de(_cripta_publicada(cliente, elegida.id))
    segundos = _medir(verificador.verificar, REPETICIONES_RESOLUBILIDAD)
    cumple = "CUMPLE" if segundos * 1000 < LIMITE_RESOLUBILIDAD_MS else "FALLA"
    return [Resultado("resolubilidad_cota", f"verificación {elegida.id} ({elegida.salas} salas)", segundos, 1,
                      f"{_ms(segundos)} ms (límite {LIMITE_RESOLUBILIDAD_MS:.1f} ms: {cumple})")]


CARGAS = (
    ("agenda", bench_agenda),
    ("cache", bench_cache),
    ("disco", bench_recuperacion_disco),
    ("inventario", bench_inventario),
    ("historial", bench_historial),
    ("historial_cazadores", bench_historial_cazadores),
    ("ordenamiento", bench_ordenamiento),
    ("guardado", bench_guardado),
    ("ciclo", bench_ciclo_eventos),
    ("partida", bench_partida_real),
    ("solicitudes", bench_solicitudes),
    ("ruta_cazador", bench_ruta_cazador),
    ("invalidacion", bench_invalidacion),
    ("ciclo_referencia", bench_ciclo_referencia),
    ("niebla_rutas", bench_niebla_rutas),
    ("linea_tiempo", bench_linea_tiempo),
    ("resolubilidad", bench_resolubilidad),
    ("resolubilidad_cota", bench_resolubilidad_cota),
)
