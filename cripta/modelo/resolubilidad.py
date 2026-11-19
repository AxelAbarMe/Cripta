"""Verificacion de resolubilidad de una cripta antes de jugar.
Modulo de dominio puro: sin red, archivos ni vista.
Cubre FR-RES-001 a FR-RES-012, FR-RES-018 a FR-RES-022.
"""
from dataclasses import dataclass

from cripta.constantes import direccion_opuesta
from cripta.estructuras.cola import Cola
from cripta.estructuras.heap_min import HeapMinimo
from cripta.estructuras.ordenamientos import Ordenamiento


# ---------------------------------------------------------------------------
# T005 — Entidades de datos inmutables
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class FronteraBloqueadaPuerta:
    """Puerta cerrada adyacente a la region alcanzable que impide continuar."""
    sala_origen: int
    direccion: str
    llave: str | None
    sala_destino: int


@dataclass(frozen=True, slots=True)
class CicloDependenciaLlaves:
    """Dependencia circular concreta entre llaves que se bloquean mutuamente."""
    llaves: tuple

    def formato(self) -> str:
        """Cadena legible del ciclo, p. ej. 'itm_a -> itm_b -> itm_a'."""
        return " -> ".join(self.llaves)


@dataclass(frozen=True, slots=True)
class UbicacionLlaveDiagnostico:
    """Diagnostico del paradero de una llave requerida por la frontera."""
    id_llave: str
    sala: int | None
    enemigo: str | None
    estado: str   # 'obtenible' | 'no_obtenible' | 'sin_ubicacion'


@dataclass(frozen=True, slots=True)
class ResultadoResolubilidad:
    """Diagnostico inmutable completo del analisis de resolubilidad."""
    es_resoluble: bool
    llaves_obtenidas: tuple
    llaves_no_obtenibles: tuple
    frontera_bloqueada: tuple
    ubicaciones_llaves: tuple
    ciclos_dependencia: tuple
    motivo_no_resoluble: str | None

    def reporte_texto(self) -> str:
        """Texto legible y estructurado del reporte para consola."""
        linea = "=" * 79
        partes = [linea]
        if self.es_resoluble:
            partes.append("Estado: RESOLUBLE")
            partes.append(linea)
            partes.append("La cripta es completable.")
            partes.append("")
            partes.append("Secuencia causal de obtencion de llaves:")
            for i, llave in enumerate(self.llaves_obtenidas, 1):
                partes.append(f"  {i}. {llave}")
        else:
            partes.append("Estado: NO RESOLUBLE")
            partes.append(linea)
            partes.append("ADVERTENCIA: La cripta no puede completarse bajo las reglas del juego.")
            if self.motivo_no_resoluble:
                partes.append(f"Motivo: {self.motivo_no_resoluble}")
            partes.append("")
            partes.append(f"Llaves no obtenibles ({len(self.llaves_no_obtenibles)}):")
            for llave in self.llaves_no_obtenibles:
                partes.append(f"  - {llave}")
            partes.append("")
            partes.append(f"Frontera bloqueada ({len(self.frontera_bloqueada)} puertas):")
            for p in self.frontera_bloqueada:
                req = f"requiere '{p.llave}'" if p.llave else "sin llave requerida"
                partes.append(f"  - Sala {p.sala_origen} -> {p.direccion} -> Sala {p.sala_destino} ({req})")
            if self.ciclos_dependencia:
                partes.append("")
                partes.append(f"Dependencias circulares detectadas ({len(self.ciclos_dependencia)} ciclo(s)):")
                for i, ciclo in enumerate(self.ciclos_dependencia, 1):
                    partes.append(f"  - Ciclo {i}: {ciclo.formato()}")
        partes.append(linea)
        return "\n".join(partes)


# ---------------------------------------------------------------------------
# T006 — Catalogo ordenado y busqueda binaria manual + tablas contiguas
# ---------------------------------------------------------------------------

def _busqueda_binaria(catalogo: list, clave: str) -> int:
    """Devuelve el indice de clave en catalogo ordenado, o -1 si no existe."""
    izq, der = 0, len(catalogo) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if catalogo[medio] == clave:
            return medio
        if catalogo[medio] < clave:
            izq = medio + 1
        else:
            der = medio - 1
    return -1


def _construir_catalogo(llaves_ids: list) -> list:
    """Ordena los ids con merge_sort y deduplica en pasada lineal. O(K log K)."""
    if not llaves_ids:
        return []
    copia = list(llaves_ids)
    Ordenamiento(copia).merge_sort()
    resultado = [copia[0]]
    for i in range(1, len(copia)):
        if copia[i] != copia[i - 1]:
            resultado.append(copia[i])
    return resultado


def _inicializar_tablas(catalogo: list, max_sala_id: int, llaves_ubicaciones: tuple):
    """Construye las tablas contiguas indexadas por entero. O(K + V)."""
    k = len(catalogo)
    llave_obtenida = [False] * k
    puertas_pendientes = [[] for _ in range(k)]
    ubicaciones_por_llave = [[] for _ in range(k)]
    llaves_en_sala = [[] for _ in range(max_sala_id + 1)]

    for ubicacion in llaves_ubicaciones:
        idx = _busqueda_binaria(catalogo, ubicacion.id)
        if idx >= 0:
            ubicaciones_por_llave[idx].append(ubicacion)
            if 0 <= ubicacion.sala <= max_sala_id:
                llaves_en_sala[ubicacion.sala].append(idx)

    return llave_obtenida, puertas_pendientes, ubicaciones_por_llave, llaves_en_sala


def _ordenar_frontera(lista: list) -> list:
    """Ordena las puertas de la frontera bloqueada por origen, dir y llave."""
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2
    izq = _ordenar_frontera(lista[:mid])
    der = _ordenar_frontera(lista[mid:])
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        a = (izq[i][0], izq[i][1], izq[i][2] or "")
        b = (der[j][0], der[j][1], der[j][2] or "")
        if a <= b:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


def _ordenar_ciclos(lista: list) -> list:
    """Ordena los ciclos por el menor identificador de llave en orden ascendente."""
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2
    izq = _ordenar_ciclos(lista[:mid])
    der = _ordenar_ciclos(lista[mid:])
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i].llaves[0] <= der[j].llaves[0]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


# ---------------------------------------------------------------------------
# T008 — Deteccion de ciclos de dependencia por DFS tricolor
# ---------------------------------------------------------------------------

def _detectar_ciclos(
    mapa,
    visitada: list,
    max_sala_id: int,
    llaves_no_obtenibles: tuple,
    ubicaciones_por_llave: list,
    catalogo: list,
    sala_salida: int,
    llave_salida: str,
) -> tuple:
    """Detecta ciclos representativos en grafo bipartito de bloques y llaves."""
    m_llaves = len(llaves_no_obtenibles)
    if m_llaves == 0:
        return ()

    # 1. Agrupar salas inalcanzables en bloques conexos por puertas abiertas
    bloque_de_sala = [-1] * (max_sala_id + 1)
    bloques_salas = []

    for s in range(1, max_sala_id + 1):
        if mapa.obtener(s) is None or visitada[s] or bloque_de_sala[s] >= 0:
            continue
        nuevo_bloque = len(bloques_salas)
        salas_bloque = [s]
        bloque_de_sala[s] = nuevo_bloque
        cola_bloque = Cola()
        cola_bloque.enqueue(s)
        while not cola_bloque.is_empty():
            curr = cola_bloque.dequeue()
            sala_obj = mapa.obtener(curr)
            for d, dst in mapa.vecinos(curr):
                if mapa.obtener(dst) is None or visitada[dst] or bloque_de_sala[dst] >= 0:
                    continue
                esta_cerrada = sala_obj.puertas.esta_cerrada(d)
                otro = mapa.obtener(dst)
                if otro is not None:
                    op = direccion_opuesta(d)
                    if otro.puertas.esta_cerrada(op):
                        esta_cerrada = True
                if not esta_cerrada:
                    bloque_de_sala[dst] = nuevo_bloque
                    salas_bloque.append(dst)
                    cola_bloque.enqueue(dst)
        bloques_salas.append(salas_bloque)

    b_bloques = len(bloques_salas)
    total_nodos = m_llaves + b_bloques
    g_dep = [[] for _ in range(total_nodos)]

    # Aristas Llave -> Bloque (bloque donde reside la llave no obtenible)
    for i in range(m_llaves):
        k_nombre = llaves_no_obtenibles[i]
        idx_cat = _busqueda_binaria(catalogo, k_nombre)
        if idx_cat >= 0:
            for ub in ubicaciones_por_llave[idx_cat]:
                if 1 <= ub.sala <= max_sala_id and not visitada[ub.sala]:
                    b_id = bloque_de_sala[ub.sala]
                    if b_id >= 0:
                        nodo_b = m_llaves + b_id
                        ya_esta = False
                        for nb in g_dep[i]:
                            if nb == nodo_b:
                                ya_esta = True
                                break
                        if not ya_esta:
                            g_dep[i].append(nodo_b)

    # Aristas Bloque -> Llave (puertas cerradas que entran al bloque)
    for b_id in range(b_bloques):
        nodo_b = m_llaves + b_id
        for s in bloques_salas[b_id]:
            sala_obj = mapa.obtener(s)
            for d, dst in mapa.vecinos(s):
                dst_obj = mapa.obtener(dst)
                if dst_obj is None:
                    continue
                otro_b = bloque_de_sala[dst] if not visitada[dst] else -1
                if visitada[dst] or (otro_b != b_id):
                    esta_cerrada = sala_obj.puertas.esta_cerrada(d)
                    op = direccion_opuesta(d)
                    if dst_obj.puertas.esta_cerrada(op):
                        esta_cerrada = True
                    if esta_cerrada:
                        llave_p, _ = mapa.datos_de_puerta(s, d)
                        if llave_p is None and dst_obj.esqueleto.salida(op) is not None:
                            llave_p, _ = mapa.datos_de_puerta(dst, op)
                        if llave_p is not None:
                            k_idx = _busqueda_binaria(list(llaves_no_obtenibles), llave_p)
                            if k_idx >= 0:
                                ya_esta = False
                                for nk in g_dep[nodo_b]:
                                    if nk == k_idx:
                                        ya_esta = True
                                        break
                                if not ya_esta:
                                    g_dep[nodo_b].append(k_idx)

    # DFS tricolor
    ciclos = []
    grupo_resuelto = [False] * m_llaves

    for i in range(m_llaves):
        if grupo_resuelto[i]:
            continue
        color = [0] * total_nodos
        pila = []

        def dfs(u):
            color[u] = 1
            pila.append(u)
            for v in g_dep[u]:
                if v < m_llaves and grupo_resuelto[v]:
                    continue
                if color[v] == 1:
                    idx = -1
                    for pos_idx in range(len(pila)):
                        if pila[pos_idx] == v:
                            idx = pos_idx
                            break
                    camino = pila[idx:]
                    llaves_ciclo = [x for x in camino if x < m_llaves]
                    if llaves_ciclo:
                        min_x = llaves_ciclo[0]
                        min_pos = 0
                        for pos_k in range(1, len(llaves_ciclo)):
                            if llaves_ciclo[pos_k] < min_x:
                                min_x = llaves_ciclo[pos_k]
                                min_pos = pos_k
                        rotado = llaves_ciclo[min_pos:] + llaves_ciclo[:min_pos]
                        tupla_llaves = tuple(llaves_no_obtenibles[x] for x in rotado) + (llaves_no_obtenibles[min_x],)
                        ciclos.append(CicloDependenciaLlaves(llaves=tupla_llaves))
                        for x in llaves_ciclo:
                            grupo_resuelto[x] = True
                        return True
                elif color[v] == 0:
                    if dfs(v):
                        return True
            pila.pop()
            color[u] = 2
            return False

        dfs(i)

    return tuple(_ordenar_ciclos(ciclos))


# ---------------------------------------------------------------------------
# T007 y T009 — VerificadorResolubilidad: __init__, verificar y verificar_ingenuo_reiniciado
# ---------------------------------------------------------------------------

class VerificadorResolubilidad:
    """Ejecuta el analisis de resolubilidad y diagnostico causal sobre el grafo."""

    def __init__(self, mapa, sala_inicial: int, sala_salida: int,
                 llave_salida: str, llaves_ubicaciones: tuple):
        """Recibe el mapa y la configuracion de llaves. No toca red ni disco."""
        self._mapa = mapa
        self._sala_inicial = sala_inicial
        self._sala_salida = sala_salida
        self._llave_salida = llave_salida
        self._llaves_ubicaciones = llaves_ubicaciones

    def verificar(self) -> ResultadoResolubilidad:
        """Recorrido incremental unico O(V + E + K log K). Retorna el resultado."""
        mapa = self._mapa
        sala_inicial = self._sala_inicial
        sala_salida = self._sala_salida
        llave_salida = self._llave_salida
        llaves_ubicaciones = self._llaves_ubicaciones

        # Recopilar todos los ids de llaves que aparecen en puertas o ubicaciones
        ids_en_puertas = []
        for sala in mapa.todas_las_salas():
            for direccion, _ in mapa.vecinos(sala.id):
                llave_puerta, _ = mapa.datos_de_puerta(sala.id, direccion)
                if llave_puerta is not None:
                    ids_en_puertas.append(llave_puerta)

        ids_todos = [llave_salida]
        for uid in ids_en_puertas:
            ids_todos.append(uid)
        for ub in llaves_ubicaciones:
            ids_todos.append(ub.id)

        catalogo = _construir_catalogo(ids_todos)
        k = len(catalogo)

        max_sala_id = 0
        for sala in mapa.todas_las_salas():
            if sala.id > max_sala_id:
                max_sala_id = sala.id

        llave_obtenida, puertas_pendientes, ubicaciones_por_llave, llaves_en_sala = \
            _inicializar_tablas(catalogo, max_sala_id, llaves_ubicaciones)

        visitada = [False] * (max_sala_id + 1)
        llaves_obtenidas_orden = []

        entro_por_llave_salida = False
        idx_llave_salida = _busqueda_binaria(catalogo, llave_salida)

        cola = Cola()
        cola.enqueue(sala_inicial)
        visitada[sala_inicial] = True

        candidatas = HeapMinimo()

        def _activar_llave(idx_k: int) -> None:
            nonlocal entro_por_llave_salida
            if llave_obtenida[idx_k]:
                return
            llave_obtenida[idx_k] = True
            llaves_obtenidas_orden.append(catalogo[idx_k])
            for origen, direc, destino in puertas_pendientes[idx_k]:
                if destino == sala_salida and idx_k == idx_llave_salida:
                    entro_por_llave_salida = True
                if not visitada[destino]:
                    visitada[destino] = True
                    cola.enqueue(destino)

        def _recoger_llaves_de_sala(sala_id: int) -> None:
            if sala_id > max_sala_id:
                return
            for idx_k in llaves_en_sala[sala_id]:
                if not llave_obtenida[idx_k]:
                    candidatas.insertar(idx_k)

        while True:
            while not cola.is_empty():
                sala_id = cola.dequeue()
                _recoger_llaves_de_sala(sala_id)
                for direccion, destino in mapa.vecinos(sala_id):
                    llave_puerta, _ = mapa.datos_de_puerta(sala_id, direccion)
                    esta_cerrada = mapa.obtener(sala_id).puertas.esta_cerrada(direccion)
                    otro = mapa.obtener(destino)
                    if otro is not None:
                        op = direccion_opuesta(direccion)
                        if otro.puertas.esta_cerrada(op):
                            esta_cerrada = True
                            if llave_puerta is None:
                                llave_puerta, _ = mapa.datos_de_puerta(destino, op)

                    if not esta_cerrada:
                        if not visitada[destino]:
                            visitada[destino] = True
                            cola.enqueue(destino)
                    else:
                        if llave_puerta is not None:
                            idx_k = _busqueda_binaria(catalogo, llave_puerta)
                            if idx_k >= 0:
                                if llave_obtenida[idx_k]:
                                    if destino == sala_salida and idx_k == idx_llave_salida:
                                        entro_por_llave_salida = True
                                    if not visitada[destino]:
                                        visitada[destino] = True
                                        cola.enqueue(destino)
                                else:
                                    ya_registrada = False
                                    for t in puertas_pendientes[idx_k]:
                                        if t[0] == sala_id and t[1] == direccion:
                                            ya_registrada = True
                                            break
                                    if not ya_registrada:
                                        puertas_pendientes[idx_k].append((sala_id, direccion, destino))

            if not candidatas.esta_vacio():
                idx_k = candidatas.eliminar_minimo()
                _activar_llave(idx_k)
            else:
                break

        # Condicion de victoria (Regla 1 de data-model.md)
        idx_ls = idx_llave_salida
        llave_salida_obtenida = (idx_ls >= 0 and llave_obtenida[idx_ls])
        es_resoluble = llave_salida_obtenida and entro_por_llave_salida

        if es_resoluble:
            return ResultadoResolubilidad(
                es_resoluble=True,
                llaves_obtenidas=tuple(llaves_obtenidas_orden),
                llaves_no_obtenibles=(),
                frontera_bloqueada=(),
                ubicaciones_llaves=(),
                ciclos_dependencia=(),
                motivo_no_resoluble=None,
            )

        # Diagnostico de no resolubilidad
        llaves_no_obtenibles = []
        for i in range(k):
            if not llave_obtenida[i]:
                llaves_no_obtenibles.append(catalogo[i])

        # Frontera bloqueada
        frontera_raw = []
        for sala in mapa.todas_las_salas():
            if not visitada[sala.id]:
                continue
            for direccion, destino in mapa.vecinos(sala.id):
                if visitada[destino]:
                    continue
                esta_cerrada = sala.puertas.esta_cerrada(direccion)
                if not esta_cerrada:
                    otro = mapa.obtener(destino)
                    if otro is not None:
                        op = direccion_opuesta(direccion)
                        if otro.puertas.esta_cerrada(op):
                            esta_cerrada = True
                if esta_cerrada:
                    llave_p, _ = mapa.datos_de_puerta(sala.id, direccion)
                    if llave_p is None:
                        otro2 = mapa.obtener(destino)
                        if otro2 is not None:
                            op2 = direccion_opuesta(direccion)
                            llave_p2, _ = (
                                mapa.datos_de_puerta(destino, op2)
                                if otro2.esqueleto.salida(op2) is not None
                                else (None, None)
                            )
                            if llave_p2 is not None:
                                llave_p = llave_p2
                    frontera_raw.append((sala.id, direccion, llave_p, destino))

        frontera_raw = _ordenar_frontera(frontera_raw)
        frontera_bloqueada = tuple(
            FronteraBloqueadaPuerta(sala_origen=f[0], direccion=f[1], llave=f[2], sala_destino=f[3])
            for f in frontera_raw
        )

        # Ubicaciones de llaves no obtenidas
        ubicaciones_diag = []
        for id_llave_no_obt in llaves_no_obtenibles:
            idx_k = _busqueda_binaria(catalogo, id_llave_no_obt)
            if idx_k >= 0 and ubicaciones_por_llave[idx_k]:
                ub = ubicaciones_por_llave[idx_k][0]
                estado = "obtenible" if llave_obtenida[idx_k] else "no_obtenible"
                ubicaciones_diag.append(UbicacionLlaveDiagnostico(
                    id_llave=id_llave_no_obt,
                    sala=ub.sala,
                    enemigo=ub.enemigo,
                    estado=estado,
                ))
            else:
                ubicaciones_diag.append(UbicacionLlaveDiagnostico(
                    id_llave=id_llave_no_obt,
                    sala=None,
                    enemigo=None,
                    estado="sin_ubicacion",
                ))

        if not llave_salida_obtenida:
            motivo = (f"no es posible obtener la llave de salida ('{llave_salida}') "
                      f"desde la region alcanzable")
        else:
            motivo = (f"no es posible alcanzar la sala de salida ({sala_salida}) "
                      f"atravesando una puerta que requiera la llave de salida ('{llave_salida}')")

        ciclos = _detectar_ciclos(
            mapa,
            visitada,
            max_sala_id,
            tuple(llaves_no_obtenibles),
            ubicaciones_por_llave,
            catalogo,
            sala_salida,
            llave_salida,
        )

        return ResultadoResolubilidad(
            es_resoluble=False,
            llaves_obtenidas=tuple(llaves_obtenidas_orden),
            llaves_no_obtenibles=tuple(llaves_no_obtenibles),
            frontera_bloqueada=frontera_bloqueada,
            ubicaciones_llaves=tuple(ubicaciones_diag),
            ciclos_dependencia=ciclos,
            motivo_no_resoluble=motivo,
        )

    def verificar_ingenuo_reiniciado(self) -> ResultadoResolubilidad:
        """Alternativa descartada para --bench: repite BFS completo por cada llave."""
        mapa = self._mapa
        sala_inicial = self._sala_inicial
        sala_salida = self._sala_salida
        llave_salida = self._llave_salida
        llaves_ubicaciones = self._llaves_ubicaciones

        ids_todos = [llave_salida]
        for sala in mapa.todas_las_salas():
            for direccion, _ in mapa.vecinos(sala.id):
                llave_puerta, _ = mapa.datos_de_puerta(sala.id, direccion)
                if llave_puerta is not None:
                    ids_todos.append(llave_puerta)
        for ub in llaves_ubicaciones:
            ids_todos.append(ub.id)

        catalogo = _construir_catalogo(ids_todos)
        k = len(catalogo)
        max_sala_id = 0
        for sala in mapa.todas_las_salas():
            if sala.id > max_sala_id:
                max_sala_id = sala.id

        _, _, ubicaciones_por_llave, llaves_en_sala = \
            _inicializar_tablas(catalogo, max_sala_id, llaves_ubicaciones)

        llaves_poseidas = [False] * k
        llaves_obtenidas_orden = []
        entro_por_llave_salida = False
        idx_ls = _busqueda_binaria(catalogo, llave_salida)

        hay_cambio = True
        while hay_cambio:
            hay_cambio = False
            visitada = [False] * (max_sala_id + 1)
            cola = Cola()
            cola.enqueue(sala_inicial)
            visitada[sala_inicial] = True

            while not cola.is_empty():
                sala_id = cola.dequeue()
                if sala_id <= max_sala_id:
                    for idx_k in llaves_en_sala[sala_id]:
                        if not llaves_poseidas[idx_k]:
                            llaves_poseidas[idx_k] = True
                            llaves_obtenidas_orden.append(catalogo[idx_k])
                            hay_cambio = True

                for direccion, destino in mapa.vecinos(sala_id):
                    llave_puerta, _ = mapa.datos_de_puerta(sala_id, direccion)
                    esta_cerrada = mapa.obtener(sala_id).puertas.esta_cerrada(direccion)
                    otro = mapa.obtener(destino)
                    if otro is not None:
                        op = direccion_opuesta(direccion)
                        if otro.puertas.esta_cerrada(op):
                            esta_cerrada = True
                            if llave_puerta is None:
                                llave_puerta, _ = mapa.datos_de_puerta(destino, op)

                    puede_pasar = False
                    if not esta_cerrada:
                        puede_pasar = True
                    elif llave_puerta is not None:
                        idx_k = _busqueda_binaria(catalogo, llave_puerta)
                        if idx_k >= 0 and llaves_poseidas[idx_k]:
                            puede_pasar = True
                            if destino == sala_salida and idx_k == idx_ls:
                                entro_por_llave_salida = True

                    if puede_pasar and not visitada[destino]:
                        visitada[destino] = True
                        cola.enqueue(destino)

        llave_salida_obtenida = (idx_ls >= 0 and llaves_poseidas[idx_ls])
        es_resoluble = llave_salida_obtenida and entro_por_llave_salida

        return ResultadoResolubilidad(
            es_resoluble=es_resoluble,
            llaves_obtenidas=tuple(llaves_obtenidas_orden),
            llaves_no_obtenibles=(),
            frontera_bloqueada=(),
            ubicaciones_llaves=(),
            ciclos_dependencia=(),
            motivo_no_resoluble=None if es_resoluble else "no resoluble (metodo ingenuo)",
        )
