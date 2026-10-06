"""Cargas sintéticas para --bench (§5.3). Cada función mide UN subsistema y, cuando el
Documento de Decisiones lo exige (§8.5), mide TAMBIÉN la alternativa descartada, con
los mismos datos, para que la comparación sea justa. Ninguna toca red, vista ni una
cripta real: todo son datos generados aquí con una semilla fija (reproducible).

`escala` multiplica los tamaños de las cargas (1.0 = rápido; 5.0 = mediciones más finas).
"""
import copy
import os
import random
import tempfile
import time
from dataclasses import dataclass

from cripta.dto.entidad_dto import entidad_desde_json
from cripta.estructuras.lista_doble_enlazada import ListaDobleEnlazada
from cripta.estructuras.ordenamiento_selector import elegir_algoritmo, ordenar_auto
from cripta.estructuras.ordenamientos import Ordenamiento
from cripta.estructuras.vector import VectorOrdenado
from cripta.infraestructura import guardado_binario as gb
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.infraestructura.estado_guardado import (
    EnemigoGuardado, EstadoPartida, EstadoRNG, EventoGuardado, JugadorGuardado,
    ObjetoGuardado, SalaGuardada, TrampaGuardada,
)
from cripta.modelo import combate
from cripta.modelo.enemigo import Enemigo
from cripta.modelo.historial_retroceso import HistorialRetroceso
from cripta.modelo.jugador import Jugador
from cripta.modelo.reloj import RelojEventos, calcular_intervalo

SEMILLA_BENCH = 20260928


@dataclass(frozen=True)
class Resultado:
    subsistema: str
    caso: str
    segundos: float
    operaciones: int
    nota: str = ""

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
                                    f"{tl / tb:.1f}x {'más lenta' if tl > tb else 'más rápida'}"))

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
                                    f"{t2 / t1:.1f}x {'más lenta' if t2 > t1 else 'más rápida'}"))
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
def bench_inventario(escala: float = 1.0):
    resultados = []
    for n in (10, 10000):
        repeticiones = max(200, int(2000 * escala)) if n == 10 else max(50, int(300 * escala))

        def con_lista_doble():
            lista = ListaDobleEnlazada()
            nodos = [lista.agregar(i) for i in range(n)]
            for k in range(repeticiones):
                nodo = nodos[(n // 2 + k) % n]
                lista.eliminar_nodo(nodo)              # soltar el objeto que se está viendo: O(1)
                nodos[(n // 2 + k) % n] = lista.agregar(k)

        def con_list():
            plana = list(range(n))
            for k in range(repeticiones):
                pos = (n // 2 + k) % n
                plana.pop(pos)                        # desplaza todo lo posterior: O(n)
                plana.append(k)

        t1, t2 = _medir(con_lista_doble), _medir(con_list)
        resultados.append(Resultado("inventario", f"soltar en medio, n={n}: lista doble (elegida)", t1, repeticiones))
        resultados.append(Resultado("inventario", f"soltar en medio, n={n}: list.pop(i) (descartada)", t2, repeticiones,
                                    f"{t2 / t1:.1f}x {'más lenta' if t2 > t1 else 'más rápida'}"
                                    + ("  <- con inventario_max típico (~10) la diferencia es despreciable" if n == 10 else "")))
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
            resultados.append(Resultado("guardado", f"{n_salas} salas: cargar todo JSON", tj, 1, f"{tj / tb:.1f}x el binario"))
            objetivo = ids_medio = n_salas // 2
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
                               "velocidad": 150, "comportamiento": "rastreador", "suelta": ()})()
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
        meta = 66 + 100                                 # un intervalo entre dos decisiones del jugador
        ejecutados = [0]

        def ciclo():
            while True:
                siguiente = reloj.ejecutar_siguiente()
                ejecutados[0] += 1
                if reloj.tiempo_actual >= meta + ejecutados[0] // actores * 0:
                    break
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


CARGAS = (
    ("agenda", bench_agenda),
    ("cache", bench_cache),
    ("disco", bench_recuperacion_disco),
    ("inventario", bench_inventario),
    ("historial", bench_historial),
    ("ordenamiento", bench_ordenamiento),
    ("guardado", bench_guardado),
    ("ciclo", bench_ciclo_eventos),
)