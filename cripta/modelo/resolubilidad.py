"""Verificacion de resolubilidad de una cripta antes de jugar.
Modulo de dominio puro: sin red, archivos ni vista.
Cubre FR-RES-001 a FR-RES-012, FR-RES-018 a FR-RES-022.
"""
from dataclasses import dataclass

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
    # deduplicar en pasada lineal
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


# ---------------------------------------------------------------------------
# T007 — VerificadorResolubilidad: __init__ y verificar()
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
        ids_en_puertas: list = []
        for sala in mapa.todas_las_salas():
            for direccion, _ in mapa.vecinos(sala.id):
                llave_puerta, _ = mapa.datos_de_puerta(sala.id, direccion)
                if llave_puerta is not None:
                    ids_en_puertas.append(llave_puerta)

        ids_todos: list = [llave_salida]
        for uid in ids_en_puertas:
            ids_todos.append(uid)
        for ub in llaves_ubicaciones:
            ids_todos.append(ub.id)

        catalogo = _construir_catalogo(ids_todos)
        k = len(catalogo)

        # Calcular max_sala_id para tablas contiguas
        max_sala_id = 0
        for sala in mapa.todas_las_salas():
            if sala.id > max_sala_id:
                max_sala_id = sala.id

        llave_obtenida, puertas_pendientes, ubicaciones_por_llave, llaves_en_sala = \
            _inicializar_tablas(catalogo, max_sala_id, llaves_ubicaciones)

        # Tablas de salas
        visitada = [False] * (max_sala_id + 1)
        llaves_obtenidas_orden: list = []

        # Para la condicion de victoria: entro_por_llave_salida
        entro_por_llave_salida = False
        idx_llave_salida = _busqueda_binaria(catalogo, llave_salida)

        # Recorrido incremental con Cola FIFO propia
        cola = Cola()
        cola.enqueue(sala_inicial)
        visitada[sala_inicial] = True

        # HeapMinimo para desempate deterministico por menor id de llave
        candidatas = HeapMinimo()

        def _activar_llave(idx_k: int) -> None:
            """Marca la llave como obtenida y desbloquea puertas que esperaban."""
            if llave_obtenida[idx_k]:
                return
            llave_obtenida[idx_k] = True
            llaves_obtenidas_orden.append(catalogo[idx_k])
            for origen, direc, destino in puertas_pendientes[idx_k]:
                if not visitada[destino]:
                    # Verificar si esta conexion entrega la condicion de victoria
                    nonlocal entro_por_llave_salida
                    if destino == sala_salida and idx_k == idx_llave_salida:
                        entro_por_llave_salida = True
                    visitada[destino] = True
                    cola.enqueue(destino)

        def _recoger_llaves_de_sala(sala_id: int) -> None:
            """Pone en candidatas las llaves de sala_id que aun no se tienen."""
            if sala_id > max_sala_id:
                return
            for idx_k in llaves_en_sala[sala_id]:
                if not llave_obtenida[idx_k]:
                    candidatas.insertar(idx_k)

        # Fase principal
        while True:
            # Drenar la cola de salas
            while not cola.is_empty():
                sala_id = cola.dequeue()
                _recoger_llaves_de_sala(sala_id)
                for direccion, destino in mapa.vecinos(sala_id):
                    # Leer datos bilaterales de la puerta
                    llave_puerta, _ = mapa.datos_de_puerta(sala_id, direccion)
                    esta_cerrada = mapa.obtener(sala_id).puertas.esta_cerrada(direccion)
                    # Tambien sincronizar: si el otro extremo la declara cerrada
                    otro = mapa.obtener(destino)
                    if otro is not None:
                        from cripta.constantes import direccion_opuesta
                        op = direccion_opuesta(direccion)
                        if otro.puertas.esta_cerrada(op):
                            esta_cerrada = True
                            if llave_puerta is None:
                                llave_puerta, _ = mapa.datos_de_puerta(destino, op)

                    if not esta_cerrada:
                        # Puerta abierta
                        if destino == sala_salida and idx_llave_salida < 0:
                            # La llave_salida no existe en catalogo, igual contamos
                            pass
                        if not visitada[destino]:
                            visitada[destino] = True
                            cola.enqueue(destino)
                    else:
                        # Puerta cerrada: registrar en puertas_pendientes si hay llave
                        if llave_puerta is not None:
                            idx_k = _busqueda_binaria(catalogo, llave_puerta)
                            if idx_k >= 0:
                                if llave_obtenida[idx_k]:
                                    # Ya la tenemos: encolar destino si no visitado
                                    if not visitada[destino]:
                                        if destino == sala_salida and idx_k == idx_llave_salida:
                                            entro_por_llave_salida = True
                                        visitada[destino] = True
                                        cola.enqueue(destino)
                                else:
                                    # Esperar a que se obtenga la llave
                                    ya_registrada = False
                                    for t in puertas_pendientes[idx_k]:
                                        if t[0] == sala_id and t[1] == direccion:
                                            ya_registrada = True
                                            break
                                    if not ya_registrada:
                                        puertas_pendientes[idx_k].append((sala_id, direccion, destino))
                            # else: llave_puerta es "sin_ubicacion", no se puede franquear
                            else:
                                # Llave requerida no esta en catalogo: puerta infranqueable
                                # Se registra igualmente para la frontera (sin indice)
                                pass
                        # else: puerta sin llave => permanentemente infranqueable

            # Cola vacia: activar la siguiente llave disponible de menor id
            if not candidatas.esta_vacio():
                idx_k = candidatas.eliminar_minimo()
                _activar_llave(idx_k)
            else:
                break  # No hay mas llaves disponibles

        # Verificar condicion de victoria (Regla 1 de data-model.md)
        # La llave_salida debe haberse obtenido Y sala_salida alcanzada por puerta que la requiere
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

        # Construir diagnostico de no resolubilidad
        llaves_no_obtenibles: list = []
        for i in range(k):
            if not llave_obtenida[i]:
                llaves_no_obtenibles.append(catalogo[i])

        # Frontera bloqueada: puertas cerradas con al menos un extremo visitado
        frontera_raw: list = []
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
                        from cripta.constantes import direccion_opuesta
                        op = direccion_opuesta(direccion)
                        if otro.puertas.esta_cerrada(op):
                            esta_cerrada = True
                if esta_cerrada:
                    llave_p, _ = mapa.datos_de_puerta(sala.id, direccion)
                    # Verificar tambien si el otro extremo declara la llave
                    if llave_p is None:
                        otro2 = mapa.obtener(destino)
                        if otro2 is not None:
                            from cripta.constantes import direccion_opuesta
                            op2 = direccion_opuesta(direccion)
                            llave_p2, _ = mapa.datos_de_puerta(destino, op2) if otro2.esqueleto.salida(op2) is not None else (None, None)
                            if llave_p2 is not None:
                                llave_p = llave_p2
                    frontera_raw.append((sala.id, direccion, llave_p, destino))

        # Ordenar frontera: (sala_origen, direccion, llave or "")
        Ordenamiento(frontera_raw).merge_sort() if False else None
        # Orden manual con merge_sort sobre lista de tuplas
        def _ordenar_frontera(lista: list) -> list:
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

        frontera_raw = _ordenar_frontera(frontera_raw)
        frontera_bloqueada = tuple(
            FronteraBloqueadaPuerta(sala_origen=f[0], direccion=f[1], llave=f[2], sala_destino=f[3])
            for f in frontera_raw
        )

        # Diagnostico de ubicaciones de llaves no obtenidas
        # Incluir llaves requeridas por la frontera con estado sin_ubicacion si no estan en catalogo
        ids_en_frontera: list = []
        for f in frontera_raw:
            if f[2] is not None:
                ids_en_frontera.append(f[2])

        ubicaciones_diag: list = []
        # Llaves no obtenibles con ubicacion conocida
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
                    estado="no_obtenible",
                ))

        # Llaves en frontera que no estan en catalogo de ubicaciones (sin_ubicacion)
        for id_f in ids_en_frontera:
            if id_f not in llaves_no_obtenibles and _busqueda_binaria(catalogo, id_f) < 0:
                ya_incluida = False
                for u in ubicaciones_diag:
                    if u.id_llave == id_f:
                        ya_incluida = True
                        break
                if not ya_incluida:
                    ubicaciones_diag.append(UbicacionLlaveDiagnostico(
                        id_llave=id_f,
                        sala=None,
                        enemigo=None,
                        estado="sin_ubicacion",
                    ))

        # Llaves requeridas por frontera que estan en catalogo pero no obtenibles
        for id_f in ids_en_frontera:
            idx_k = _busqueda_binaria(catalogo, id_f)
            if idx_k >= 0 and not llave_obtenida[idx_k]:
                ya_incluida = False
                for u in ubicaciones_diag:
                    if u.id_llave == id_f:
                        ya_incluida = True
                        break
                if not ya_incluida:
                    if ubicaciones_por_llave[idx_k]:
                        ub = ubicaciones_por_llave[idx_k][0]
                        ubicaciones_diag.append(UbicacionLlaveDiagnostico(
                            id_llave=id_f,
                            sala=ub.sala,
                            enemigo=ub.enemigo,
                            estado="no_obtenible",
                        ))
                    else:
                        ubicaciones_diag.append(UbicacionLlaveDiagnostico(
                            id_llave=id_f,
                            sala=None,
                            enemigo=None,
                            estado="sin_ubicacion",
                        ))

        # Motivo de no resolubilidad
        if not llave_salida_obtenida:
            motivo = (f"no es posible obtener la llave de salida ('{llave_salida}') "
                      f"desde la region alcanzable")
        else:
            motivo = (f"no es posible alcanzar la sala de salida ({sala_salida}) "
                      f"atravesando una puerta que requiera la llave de salida ('{llave_salida}')")

        # NOTA T007: ciclos_dependencia devuelve tupla vacia provisional hasta T008.
        return ResultadoResolubilidad(
            es_resoluble=False,
            llaves_obtenidas=tuple(llaves_obtenidas_orden),
            llaves_no_obtenibles=tuple(llaves_no_obtenibles),
            frontera_bloqueada=frontera_bloqueada,
            ubicaciones_llaves=tuple(ubicaciones_diag),
            ciclos_dependencia=(),   # provisional: se completa en T008
            motivo_no_resoluble=motivo,
        )

    def verificar_ingenuo_reiniciado(self) -> ResultadoResolubilidad:
        """Alternativa descartada para --bench: repite BFS completo por cada llave."""
        mapa = self._mapa
        sala_inicial = self._sala_inicial
        sala_salida = self._sala_salida
        llave_salida = self._llave_salida
        llaves_ubicaciones = self._llaves_ubicaciones

        # Recopilar catalogo igual que en verificar()
        ids_todos: list = [llave_salida]
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
        llaves_obtenidas_orden: list = []
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
                # Recoger llaves en esta sala
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
                        from cripta.constantes import direccion_opuesta
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
