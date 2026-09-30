"""ServicioPrecarga: esqueleto completo, contenido de salas por lotes anticipados y
población de salas con sus enemigos.

Problema: entrar a una sala exige tener su contenido, cada solicitud tarda ~400 ms,
pero cuesta lo mismo pedir 1 sala que 10, y el presupuesto de solicitudes es fijo.

Estrategia:
  * Anticipación por lotes: al entrar a una sala se hace un recorrido en anchura (BFS)
    sobre el esqueleto (que ya está completo) y, si alguna sala a `radio_anticipacion`
    pasos o menos aún no se ha solicitado, se pide UN lote con las 10 salas sin
    solicitar más cercanas (por distancia y luego orden N,S,E,O: determinista).
    Como cada lote toma min(10, salas sin pedir), el total de solicitudes de
    contenido nunca pasa de ceil(salas/10).
  * Sin repetir: `_solicitadas` (VectorOrdenado de ids) registra toda sala pedida,
    recibida o cargada desde disco; se consulta al SOLICITAR, no al recibir, así las
    decisiones no dependen de cuándo llegue una respuesta.
  * Disco: una sala con contenido persistido y vigente (misma versión de la cripta)
    se carga sin red y no consume lote.
  * Hilo de red: los lotes los ejecuta UN hilo trabajador en orden FIFO (una Cola
    propia protegida por Condition), así el jugador no espera mientras piensa.
  * Determinismo (§2.4): el modelo NUNCA lee contenido que no haya sido incorporado, y
    la incorporación solo ocurre dentro de asegurar_contenido(), en el orden en que se
    solicitaron los lotes, esperando la respuesta si aún no llega. Cuándo llega la
    respuesta (latencia) puede variar; lo que el modelo ve y en qué orden, no. Esperar
    no toca ningún reloj virtual: este módulo no conoce el reloj.
  * Fallos: si un lote falla, sus salas se "des-solicitan" y el error se propaga solo
    a quien necesitaba esa sala; el resto de la partida sigue y puede reintentar.
"""
import threading

from cripta.constantes import MAX_ELEMENTOS_POR_LOTE
from cripta.estructuras.cola import Cola
from cripta.estructuras.ordenamientos import Ordenamiento
from cripta.estructuras.vector import VectorOrdenado
from cripta.excepciones import CriptaDatosNoEncontradosError, CriptaError
from cripta.modelo.enemigo import Enemigo


class _Lote:
    __slots__ = ("secuencia", "salas", "evento", "respuesta", "error", "incorporado")

    def __init__(self, secuencia: int, salas):
        self.secuencia = secuencia
        self.salas = tuple(salas)
        self.evento = threading.Event()
        self.respuesta = None
        self.error = None
        self.incorporado = False


class ServicioPrecarga:
    def __init__(self, cliente, cripta_id: str, mapa, servicio_catalogo=None, cache_disco=None,
                 version_cripta: str | None = None, radio_anticipacion: int = 2, asincrono: bool = True):
        if cache_disco is not None and version_cripta is None:
            raise ValueError("Con caché en disco hace falta la versión de la cripta")
        self._cliente = cliente
        self._cripta_id = cripta_id
        self._mapa = mapa
        self._catalogo = servicio_catalogo
        self._disco = cache_disco
        self._version = version_cripta
        self._radio = radio_anticipacion
        self._asincrono = asincrono

        self._solicitadas = VectorOrdenado()                              # ids de sala pedidas/recibidas/en disco
        self._lotes = []                                                   # en orden de solicitud (list permitido, §7)
        self._primer_no_incorporado = 0
        self._indice_lote = VectorOrdenado(clave=lambda par: par[0])      # (sala_id, lote)
        self._enemigos_por_crear = VectorOrdenado(clave=lambda c: c.sala)  # ContenidoSalaDTO con enemigos
        self._pobladas = VectorOrdenado()                                  # salas cuyos enemigos ya se instanciaron

        self._cola = Cola()
        self._cond = threading.Condition()
        self._cerrado = False
        self._hilo = None

        self.lotes_de_red = 0
        self.salas_desde_disco = 0

    # ------------------------------------------------------------ esqueleto
    def cargar_esqueleto(self, paginas_total: int) -> None:
        """Descarga (o lee de disco) todas las páginas y arma el mapa (§3.2)."""
        for pagina in range(1, paginas_total + 1):
            dto = None
            if self._disco is not None:
                dto = self._disco.leer_pagina(self._cripta_id, self._version, pagina)
            if dto is None:
                dto = self._cliente.obtener_pagina_esqueleto(self._cripta_id, pagina)
                if self._disco is not None:
                    self._disco.guardar_pagina(self._cripta_id, self._version, dto)
            self._mapa.agregar_pagina(dto)

    # ------------------------------------------------------------- anticipar
    def precargar_desde(self, sala_id: int):
        """Llamar al entrar a una sala. Pide un lote solo si hace falta (ver módulo)."""
        if len(self._solicitadas) >= len(self._mapa):
            return None  # todo pedido: O(1)
        hace_falta = False
        for destino, distancia in self._recorrer(sala_id):
            if distancia > self._radio:
                break
            if not self._solicitadas.contiene(destino):
                hace_falta = True
                break
        if not hace_falta:
            return None
        return self._solicitar_cercanas(sala_id)

    def _recorrer(self, origen: int):
        """BFS determinista (orden N,S,E,O) que produce (sala, distancia)."""
        cola = Cola()
        vistas = VectorOrdenado()
        vistas.insertar(origen)
        cola.enqueue((origen, 0))
        while not cola.is_empty():
            actual, distancia = cola.dequeue()
            yield actual, distancia
            for _direccion, destino in self._mapa.vecinos(actual):
                if destino in self._mapa and not vistas.contiene(destino):
                    vistas.insertar(destino)
                    cola.enqueue((destino, distancia + 1))

    def _solicitar_cercanas(self, origen: int):
        para_red = []
        for sala_id, _distancia in self._recorrer(origen):
            if self._solicitadas.contiene(sala_id):
                continue
            if self._cargar_de_disco(sala_id):
                continue
            para_red.append(sala_id)
            if len(para_red) >= MAX_ELEMENTOS_POR_LOTE:
                break
        if not para_red:
            return None
        return self._crear_lote(para_red)

    def _cargar_de_disco(self, sala_id: int) -> bool:
        if self._disco is None:
            return False
        contenido = self._disco.leer_contenido_sala(self._cripta_id, self._version, sala_id)
        if contenido is None:
            return False
        self._solicitadas.insertar(sala_id)
        self._incorporar_contenido(contenido)
        self.salas_desde_disco += 1
        return True

    def _crear_lote(self, salas):
        lote = _Lote(len(self._lotes), salas)
        self._lotes.append(lote)
        for sala_id in lote.salas:
            self._solicitadas.insertar(sala_id)
            self._indice_lote.insertar((sala_id, lote))
        self.lotes_de_red += 1
        if self._asincrono:
            self._encolar(lote)
        else:
            self._ejecutar(lote)
        return lote

    # ----------------------------------------------------------- hilo de red
    def _encolar(self, lote) -> None:
        with self._cond:
            self._cola.enqueue(lote)
            if self._hilo is None:
                self._hilo = threading.Thread(target=self._bucle_hilo, name="precarga-red", daemon=True)
                self._hilo.start()
            self._cond.notify()

    def _bucle_hilo(self) -> None:
        while True:
            with self._cond:
                while self._cola.is_empty() and not self._cerrado:
                    self._cond.wait()
                if self._cola.is_empty():
                    return
                lote = self._cola.dequeue()
            self._ejecutar(lote)

    def _ejecutar(self, lote) -> None:
        try:
            lote.respuesta = self._cliente.obtener_contenido(self._cripta_id, list(lote.salas))
        except Exception as error:  # se reporta a quien espere este lote, no se pierde en el hilo
            lote.error = error
        finally:
            lote.evento.set()

    def cerrar(self) -> None:
        """Detiene el hilo sin gastar más solicitudes: los lotes aún en cola se cancelan."""
        with self._cond:
            self._cerrado = True
            while not self._cola.is_empty():
                lote = self._cola.dequeue()
                lote.error = CriptaError("Precarga cancelada al cerrar la partida")
                lote.evento.set()
            self._cond.notify_all()
        if self._hilo is not None:
            self._hilo.join(timeout=5)

    # ------------------------------------------------------------ incorporar
    def asegurar_contenido(self, sala_id: int):
        """Garantiza que el contenido de `sala_id` esté en el modelo ANTES de confirmar
        un movimiento (§2.5, §4.2). Si aún viaja, espera (tiempo real, no virtual)."""
        sala = self._mapa.obtener(sala_id)
        if sala is None:
            raise CriptaDatosNoEncontradosError(f"sala {sala_id}", "esqueleto de la cripta")
        if sala.contenido_cargado:
            return sala
        if not self._solicitadas.contiene(sala_id):
            self._solicitar_cercanas(sala_id)
            if sala.contenido_cargado:
                return sala  # estaba en disco
        lote = self._indice_lote.buscar(sala_id)[1]
        error = self._incorporar_hasta(lote)
        if not sala.contenido_cargado:
            raise error if error is not None else CriptaDatosNoEncontradosError(f"contenido de sala {sala_id}", "respuesta del servidor")
        return sala

    def _incorporar_hasta(self, objetivo):
        """Incorpora lotes EN ORDEN DE SOLICITUD hasta `objetivo` inclusive (§2.4)."""
        error_objetivo = None
        while self._primer_no_incorporado < len(self._lotes):
            lote = self._lotes[self._primer_no_incorporado]
            self._primer_no_incorporado += 1
            if not lote.incorporado:
                lote.evento.wait()
                error = self._incorporar_lote(lote)
                if lote is objetivo:
                    error_objetivo = error
            if lote is objetivo:
                break
        return error_objetivo

    def _incorporar_lote(self, lote):
        lote.incorporado = True
        error = lote.error
        if error is None:
            for contenido in lote.respuesta.salas:
                self._incorporar_contenido(contenido)
                if self._disco is not None:
                    self._disco.guardar_contenido_sala(self._cripta_id, self._version, contenido)
            lote.respuesta = None
        # Des-solicitar lo que no llegó, para poder reintentarlo después.
        for sala_id in lote.salas:
            sala = self._mapa.obtener(sala_id)
            if sala is None or not sala.contenido_cargado:
                self._solicitadas.eliminar(sala_id)
                self._indice_lote.eliminar(sala_id)
                if error is None:
                    error = CriptaDatosNoEncontradosError(f"contenido de sala {sala_id}", "respuesta del servidor")
        return error

    def _incorporar_contenido(self, contenido) -> None:
        sala = self._mapa.obtener(contenido.sala)
        if sala is None:
            return
        sala.cargar_contenido(contenido)
        if len(contenido.enemigos) > 0 and not self._pobladas.contiene(contenido.sala):
            self._enemigos_por_crear.insertar(contenido)
        if self._catalogo is not None:
            ids = [e.tipo for e in contenido.enemigos] + list(contenido.objetos) + [t.tipo for t in contenido.trampas]
            self._catalogo.solicitar(ids)  # se resolverán juntos, por lotes (§4.3)

    # -------------------------------------------------------------- poblar
    def preparar_sala(self, sala_id: int):
        """Contenido + fichas de catálogo de la sala + enemigos instanciados (dormidos).
        Los ids se resuelven por lotes junto con los de las demás salas ya incorporadas."""
        if self._catalogo is None:
            raise ValueError("preparar_sala necesita un ServicioCatalogo")
        sala = self.asegurar_contenido(sala_id)
        pendiente = self._enemigos_por_crear.buscar(sala_id)
        ids = [e.tipo for e in (pendiente.enemigos if pendiente else ())]
        ids += list(sala.objetos_en_suelo) + [t.tipo_catalogo for t in sala.trampas]
        fichas = self._catalogo.obtener_varias(ids) if ids else ()
        if pendiente is None:
            return sala
        indice = VectorOrdenado(clave=lambda f: f.id)
        for ficha in fichas:
            if not indice.contiene(ficha.id):
                indice.insertar(ficha)
        creados = []
        for e in pendiente.enemigos:
            creados.append((e.instancia, Enemigo(e.instancia, indice.buscar(e.tipo), sala_id, e.vida)))
        Ordenamiento(creados).insertion_sort()  # orden ascendente por id de instancia (§2.4)
        sala.enemigos_dormidos.extend(enemigo for _id, enemigo in creados)
        self._enemigos_por_crear.eliminar(sala_id)
        self._pobladas.insertar(sala_id)
        return sala

    # ------------------------------------------------------------- reporte
    def reporte(self) -> str:
        return (f"Precarga: {len(self._solicitadas)}/{len(self._mapa)} salas solicitadas, "
                f"{self.lotes_de_red} lote(s) de red, {self.salas_desde_disco} sala(s) desde disco")