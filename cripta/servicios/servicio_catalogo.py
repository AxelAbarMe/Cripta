"""ServicioCatalogo: resolución de referencias del catálogo + caché en memoria con desalojo + recuperación desde disco.

Tres niveles, del más barato al más caro:
  1. memoria (tope --cache-size)
  2. disco (CacheDisco, validado por versión) -> "recuperación": una lectura de disco, NUNCA una solicitud de red
  3. red, SIEMPRE por lotes de hasta 10 ids: cuando hay que ir a la red por un id, el lote se completa con otros ids pendientes ya descubiertos.

Decisiones de estructura (para docs/DecisionesDiseño.md, §4.4):
  - Índice de búsqueda: VectorOrdenado por id (búsqueda binaria O(log n)).
  - Política de desalojo: LRU con ListaDobleEnlazada. Cada entrada guarda su nodo,
    así "usé esta ficha" (mover al frente) y "desalojar la menos usada" (quitar la
    cola) son O(1) sin recorrer nada. Se justifica por localidad: el jugador
    revisita salas cercanas y los mismos tipos (ratas, pociones) reaparecen.
  - Fichas en uso: `fichas_en_uso` devuelve los ids referenciados
    por instancias activas (enemigos vivos, inventario, suelo/trampas de la sala
    actual). Solo se consulta al desalojar; cada id se marca en su entrada mediante
    el propio índice (O(k log n)) y se recorre el LRU desde la cola saltando marcas.
    Si TODAS las residentes están en uso, la caché excede el tope temporalmente:
    el enunciado prohíbe soltar una ficha en uso.
  - Pendientes: ids descubiertos se acumulan en un VectorOrdenado (sin repetidos
    automáticamente, y el orden de los lotes es determinista: por id).
"""
from cripta.constantes import CACHE_TAMANO_DEFAULT, MAX_ELEMENTOS_POR_LOTE
from cripta.estructuras.lista_doble_enlazada import ListaDobleEnlazada
from cripta.estructuras.vector import VectorOrdenado
from cripta.excepciones import CriptaDatosNoEncontradosError


class _Entrada:
    __slots__ = ("id", "ficha", "nodo", "en_uso")

    def __init__(self, ficha):
        self.id = ficha.id
        self.ficha = ficha
        self.nodo = None
        self.en_uso = False


class EstadisticasCatalogo:
    def __init__(self):
        self.aciertos = 0            # ficha encontrada en memoria
        self.fallos = 0              # ficha NO estaba en memoria
        self.recuperadas_disco = 0   # fallos resueltos con una lectura de disco
        self.descargadas_red = 0     # fichas traídas por HTTP
        self.lotes_red = 0           # solicitudes de catálogo realizadas
        self.desalojadas = 0

    def reporte(self) -> str:
        return (
            f"Catálogo: aciertos={self.aciertos}, fallos={self.fallos}, "
            f"recuperadas de disco={self.recuperadas_disco}, "
            f"descargadas={self.descargadas_red} en {self.lotes_red} lote(s), "
            f"desalojadas={self.desalojadas}"
        )


class ServicioCatalogo:
    def __init__(self, cliente, tamano_maximo: int = CACHE_TAMANO_DEFAULT, cache_disco=None,
                 fichas_en_uso=None, version_catalogo: str | None = None):
        if tamano_maximo < 1:
            raise ValueError("El tamaño de la caché debe ser al menos 1")
        self._cliente = cliente
        self._tope = tamano_maximo
        self._disco = cache_disco
        self._fichas_en_uso = fichas_en_uso if fichas_en_uso is not None else (lambda: ())
        self._version = version_catalogo
        self._indice = VectorOrdenado(clave=lambda entrada: entrada.id)
        self._lru = ListaDobleEnlazada()  # cabeza = más recientemente usada
        self._pendientes = VectorOrdenado()  # ids descubiertos aún sin resolver
        self.estadisticas = EstadisticasCatalogo()

    # ------------------------------------------------------------------ API
    def obtener(self, ficha_id: str):
        entrada = self._indice.buscar(ficha_id)
        if entrada is not None:
            self.estadisticas.aciertos += 1
            self._lru.mover_al_inicio(entrada.nodo)
            return entrada.ficha
        self.estadisticas.fallos += 1
        ficha = self._recuperar_de_disco(ficha_id)
        if ficha is not None:
            return ficha
        return self._descargar_prioritaria(ficha_id)

    def solicitar(self, ids) -> None:
        """Registra ids descubiertos para pedirlos juntos más adelante (§4.3)."""
        for ficha_id in ids:
            if not self._indice.contiene(ficha_id) and not self._pendientes.contiene(ficha_id):
                self._pendientes.insertar(ficha_id)

    def resolver_pendientes(self) -> list:
        """Pide en lotes de 10 todo lo pendiente que no esté en memoria ni en disco."""
        descargadas = []
        self._purgar_pendientes()
        while len(self._pendientes) > 0:
            lote = list(self._pendientes.elementos())[:MAX_ELEMENTOS_POR_LOTE]
            descargadas.extend(self._pedir_lote(lote, prioritario=None))
        return descargadas

    def obtener_varias(self, ids) -> tuple:
        """Resuelve varios ids con el mínimo de solicitudes: los descubiertos juntos
        viajan juntos. Devuelve las fichas en el mismo orden que `ids`."""
        self.solicitar(ids)
        descargadas = self.resolver_pendientes()
        resultado = []
        contadas = []  # ids recién descargados que ya se contaron como fallo
        for ficha_id in ids:
            ficha = None
            if ficha_id not in contadas:
                ficha = self._buscar_en(descargadas, ficha_id)
            if ficha is not None:
                # La trajo la red en este mismo llamado: es un fallo de caché, pero solo la primera vez
                self.estadisticas.fallos += 1
                contadas.append(ficha_id)
            else:
                # Ya estaba en memoria o en disco, o es una repetición: obtener() cuenta acierto o fallo
                ficha = self.obtener(ficha_id)
            resultado.append(ficha)
        return tuple(resultado)

    def ids_en_memoria(self) -> tuple:
        """Ids residentes, de la más a la menos recientemente usada (útil para pruebas)."""
        ids = []
        nodo = self._lru.head
        while nodo is not None:
            ids.append(nodo.data.id)
            nodo = nodo.next
        return tuple(ids)

    def hay_pendientes(self) -> bool:
        return len(self._pendientes) > 0

    def __len__(self) -> int:
        return len(self._indice)

    # ------------------------------------------------------------- internos
    def _version_catalogo(self) -> str:
        # Una sola consulta de versión por ejecución, y solo si hay caché en disco
        # que validar/alimentar; sin disco no hace falta gastar esa solicitud.
        if self._version is None:
            self._version = self._cliente.obtener_version_catalogo().version
        return self._version

    def _recuperar_de_disco(self, ficha_id: str):
        if self._disco is None:
            return None
        ficha = self._disco.leer_ficha(self._version_catalogo(), ficha_id)
        if ficha is None:
            return None
        self.estadisticas.recuperadas_disco += 1
        self._pendientes.eliminar(ficha_id)
        self._insertar(ficha)
        return ficha

    def _purgar_pendientes(self) -> None:
        # No se pide por red lo que ya está en memoria o persistido y vigente (§4.3).
        for ficha_id in self._pendientes.elementos():
            en_memoria = self._indice.contiene(ficha_id)
            en_disco = self._disco is not None and self._disco.existe_ficha(self._version_catalogo(), ficha_id)
            if en_memoria or en_disco:
                self._pendientes.eliminar(ficha_id)

    def _descargar_prioritaria(self, ficha_id: str):
        self._pendientes.eliminar(ficha_id)
        self._purgar_pendientes()
        lote = [ficha_id]
        for pendiente in self._pendientes.elementos():
            if len(lote) >= MAX_ELEMENTOS_POR_LOTE:
                break
            lote.append(pendiente)
        fichas = self._pedir_lote(lote, prioritario=ficha_id)
        ficha = self._buscar_en(fichas, ficha_id)
        if ficha is None:
            raise CriptaDatosNoEncontradosError(f"ficha de catálogo {ficha_id}", "respuesta del servidor")
        return ficha

    def _pedir_lote(self, ids, prioritario) -> list:
        if self._disco is not None:
            self._version_catalogo()  # antes de pedir: la versión etiqueta lo que se guardará
        respuesta = self._cliente.obtener_catalogo(list(ids))
        self.estadisticas.lotes_red += 1
        for ficha_id in ids:
            self._pendientes.eliminar(ficha_id)
        fichas = list(respuesta.entidades)
        # La ficha prioritaria se inserta al final: queda como la más reciente y no
        # se desaloja a sí misma si el lote es mayor que el tope.
        for ficha in fichas:
            if ficha.id != prioritario:
                self._registrar_descargada(ficha)
        for ficha in fichas:
            if ficha.id == prioritario:
                self._registrar_descargada(ficha)
        return fichas

    def _registrar_descargada(self, ficha) -> None:
        self.estadisticas.descargadas_red += 1
        if self._disco is not None:
            self._disco.guardar_ficha(self._version_catalogo(), ficha)
        if not self._indice.contiene(ficha.id):
            self._insertar(ficha)
        # Un enemigo revela qué objetos suelta: se anotan como pendientes para que
        # viajen en algún lote futuro (segundo nivel de descubrimiento de ids).
        suelta = getattr(ficha, "suelta", ())
        if suelta:
            self.solicitar(suelta)

    def _insertar(self, ficha) -> None:
        entrada = _Entrada(ficha)
        entrada.nodo = self._lru.agregar_inicio(entrada)
        self._indice.insertar(entrada)
        while len(self._indice) > self._tope:
            victima = self._elegir_victima()
            if victima is None:
                break  # todas en uso: se tolera exceder el tope (ver docstring del módulo)
            self._lru.eliminar_nodo(victima.nodo)
            self._indice.eliminar(victima.id)
            self.estadisticas.desalojadas += 1

    def _elegir_victima(self):
        marcadas = []
        for ficha_id in self._fichas_en_uso():
            entrada = self._indice.buscar(ficha_id)
            if entrada is not None:
                entrada.en_uso = True
                marcadas.append(entrada)
        victima = None
        nodo = self._lru.tail
        # Se excluye la cabeza: es la ficha recién insertada, que nunca debe ser la víctima.
        while nodo is not None and nodo is not self._lru.head:
            if not nodo.data.en_uso:
                victima = nodo.data
                break
            nodo = nodo.prev
        for entrada in marcadas:
            entrada.en_uso = False
        return victima

    @staticmethod
    def _buscar_en(fichas, ficha_id):
        for ficha in fichas:
            if ficha.id == ficha_id:
                return ficha
        return None