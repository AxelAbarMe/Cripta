"""Guardado binario de la partida con formato propio (§4.10), usando struct.

Disposición del archivo (todo little-endian):

    [ ENCABEZADO 24 B ] [ ÍNDICE n*16 B ] [ BLOQUE GLOBAL ] [ BLOQUE SALA ] * n

  ENCABEZADO  "<4sHHIQI" = magic b"CRPT" | versión del formato | reservado |
              n_salas | offset del bloque global | longitud del bloque global
  ÍNDICE      n registros de fixed 16 B "<IQI" = id de sala | offset | longitud,
              ORDENADOS por id de sala con el selector automático (§4.9).
  GLOBAL      cripta/versiones, semilla, estado del RNG, reloj, contadores, jugador
              e inventario, agenda de eventos y mensajes.
  SALA        estado mutable de una sala (puertas, rastro, suelo, trampas, enemigos).

Recuperar UNA sala sin leer el archivo completo: como los registros del índice miden
lo mismo y están ordenados, cargar_sala() hace búsqueda binaria directamente sobre el
archivo (seek + read de 16 B por paso, O(log n) lecturas) y luego lee solo el bloque
de esa sala. Ni el índice completo ni las demás salas se leen.

Compatibilidad: el encabezado lleva un magic y la versión del formato; cualquier
diferencia (o un archivo truncado) lanza CriptaFormatoIncompatibleError en vez de
interpretar bytes ajenos.

Al final del módulo hay guardar_json/cargar_json, solo para las comparaciones de
tamaño y tiempo de carga que exige el enunciado.
"""
import dataclasses
import json
import os
import struct

from cripta.estructuras.ordenamiento_selector import ordenar_auto
from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura.estado_guardado import (
    EnemigoGuardado, EstadoPartida, EstadoRNG, EventoGuardado, JugadorGuardado,
    ObjetoGuardado, SalaGuardada, TrampaGuardada,
)

MAGIC = b"CRPT"
FORMATO_VERSION = 1
_ESTADO_RNG_ENTEROS = 625

# Formatos precompilados: struct.Struct interpreta el texto del formato una vez y se reutiliza
# en cada número, en vez de reinterpretar "<I" en cada llamada a struct.pack / struct.unpack.

# Letras: < orden de bytes fijo | s texto | B, H, I, Q enteros sin signo de 1, 2, 4 y 8 bytes
# | i, q enteros con signo de 4 y 8 bytes | d decimal de 8 byte

_ENCABEZADO = struct.Struct("<4sHHIQI")   # magic (4s), versión (H), reservado (H), n_salas (I), offset global (Q), largo global (I)
_REGISTRO_INDICE = struct.Struct("<IQI")  # id de sala (I), offset (Q), largo (I): 16 bytes por sala
_U8 = struct.Struct("<B")    # entero sin signo, 1 byte (0 a 255)
_U16 = struct.Struct("<H")   # entero sin signo, 2 bytes (0 a 65 535)
_U32 = struct.Struct("<I")   # entero sin signo, 4 bytes
_I32 = struct.Struct("<i")   # entero con signo, 4 bytes
_I64 = struct.Struct("<q")   # entero con signo, 8 bytes
_F64 = struct.Struct("<d")   # decimal, 8 bytes

# Grupos de campos fijos que siempre van juntos: se escriben y leen con UNA llamada en vez de una por campo

_ESTADO_RNG = struct.Struct(f"<{_ESTADO_RNG_ENTEROS}I")  # los 625 enteros del RNG
_SALA_FIJO = struct.Struct("<iBBq")       # sala_id, contenido_cargado, banderas de puertas, rastro
_ENEMIGO_FIJO = struct.Struct("<iBiq")    # vida, activo, sala_actual, tiempo_siguiente

_MAX_U16 = 2**16 - 1  # tope de las cantidades y del largo de los textos, que se guardan en u16


class _Escritor:
    def __init__(self):
        self.datos = bytearray()

    def _empacar(self, formato: struct.Struct, *valores) -> None:
        # struct ya rechaza un valor que no cabe en su tipo (o que no es entero), pero con un
        # struct.error poco claro: se convierte en ValueError diciendo qué valores fallaron.
        # Sin costo extra cuando todo está bien: el try solo actúa si hay error.
        try:
            self.datos += formato.pack(*valores)
        except struct.error as error:
            raise ValueError(f"No se pudo guardar {valores!r} con el formato {formato.format!r}: {error}") from None

    # Cada método escribe UN valor de tamaño fijo. Nombre: u = sin signo, i = con signo,
    # f = decimal; el número son los bits (8 bits = 1 byte). Todos pasan por _empacar:
    def bool_(self, v):
        self._empacar(_U8, 1 if v else 0)  # verdadero/falso como 1 o 0, en 1 byte

    def u8(self, v):
        self._empacar(_U8, v)  # 0 a 255, 1 byte

    def u16(self, v):
        self._empacar(_U16, v)  # 0 a 65 535, 2 bytes

    def u32(self, v):
        self._empacar(_U32, v)  # positivo, 4 bytes

    def i32(self, v):
        self._empacar(_I32, v)  # con negativos, 4 bytes

    def i64(self, v):
        self._empacar(_I64, v)  # con negativos, 8 bytes

    def f64(self, v):
        self._empacar(_F64, v)  # decimal, 8 bytes

    def grupo(self, formato: struct.Struct, *valores):
        self._empacar(formato, *valores)  # varios campos fijos de una vez

    def cantidad(self, n: int, que: str):
        # Las cantidades de elementos (objetos, trampas, mensajes...) se guardan en u16
        if n > _MAX_U16:
            raise ValueError(f"Demasiados {que} para guardar: {n} (máximo {_MAX_U16})")
        self.u16(n)

    def cadena(self, texto: str):
        crudo = texto.encode("utf-8")
        if len(crudo) > _MAX_U16:
            raise ValueError(f"Texto demasiado largo para guardar ({len(crudo)} bytes): {texto[:30]!r}...")
        self.u16(len(crudo))
        self.datos += crudo


class _Lector:
    def __init__(self, datos: bytes):
        self._datos = datos
        self._pos = 0

    def _tomar(self, formato: struct.Struct):
        try:
            valores = formato.unpack_from(self._datos, self._pos)
        except struct.error:
            raise CriptaFormatoIncompatibleError("archivo truncado o dañado") from None
        self._pos += formato.size
        return valores

    def bool_(self): return self._tomar(_U8)[0] != 0
    def u8(self): return self._tomar(_U8)[0]
    def u16(self): return self._tomar(_U16)[0]
    def u32(self): return self._tomar(_U32)[0]
    def i32(self): return self._tomar(_I32)[0]
    def i64(self): return self._tomar(_I64)[0]
    def f64(self): return self._tomar(_F64)[0]
    def grupo(self, formato: struct.Struct): return self._tomar(formato)  # tupla con varios campos fijos

    def cadena(self) -> str:
        n = self.u16()
        crudo = self._datos[self._pos:self._pos + n]
        if len(crudo) != n:
            raise CriptaFormatoIncompatibleError("archivo truncado o dañado")
        self._pos += n
        try:
            return crudo.decode("utf-8")
        except UnicodeDecodeError:
            raise CriptaFormatoIncompatibleError("texto dañado en el archivo") from None


# ----------------------------------------------------------------- sala
def _escribir_sala(w: _Escritor, s: SalaGuardada) -> None:
    banderas = 0
    for bit, cerrada in enumerate(s.puertas_cerradas):
        if cerrada:
            banderas |= 1 << bit
    w.grupo(_SALA_FIJO, s.sala_id, 1 if s.contenido_cargado else 0, banderas, s.rastro)
    w.cantidad(len(s.objetos_suelo), "objetos en el suelo")
    for objeto in s.objetos_suelo:
        w.cadena(objeto)
    w.cantidad(len(s.trampas), "trampas")
    for t in s.trampas:
        w.cadena(t.instancia_id); w.cadena(t.tipo); w.bool_(t.armada)
    w.cantidad(len(s.enemigos), "enemigos")
    for e in s.enemigos:
        w.cadena(e.instancia_id); w.cadena(e.tipo)
        w.grupo(_ENEMIGO_FIJO, e.vida, 1 if e.activo else 0, e.sala_actual, e.tiempo_siguiente)


def _leer_sala(r: _Lector) -> SalaGuardada:
    sala_id, contenido_cargado, banderas, rastro = r.grupo(_SALA_FIJO)
    puertas = tuple(bool(banderas & (1 << bit)) for bit in range(4))
    objetos = tuple(r.cadena() for _ in range(r.u16()))
    trampas = tuple(TrampaGuardada(r.cadena(), r.cadena(), r.bool_()) for _ in range(r.u16()))
    enemigos = tuple(_leer_enemigo(r) for _ in range(r.u16()))
    return SalaGuardada(sala_id, contenido_cargado != 0, puertas, rastro, objetos, trampas, enemigos)


def _leer_enemigo(r: _Lector) -> EnemigoGuardado:
    instancia, tipo = r.cadena(), r.cadena()
    vida, activo, sala_actual, tiempo_siguiente = r.grupo(_ENEMIGO_FIJO)
    return EnemigoGuardado(instancia, tipo, vida, activo != 0, sala_actual, tiempo_siguiente)


# --------------------------------------------------------------- global
def _escribir_global(w: _Escritor, e: EstadoPartida) -> None:
    w.cadena(e.cripta_id); w.cadena(e.cripta_version); w.cadena(e.catalogo_version)
    w.i64(e.semilla)
    w.u32(e.rng.version)
    if len(e.rng.estado) != _ESTADO_RNG_ENTEROS:
        raise ValueError(f"El estado del RNG debe tener {_ESTADO_RNG_ENTEROS} enteros")
    w.grupo(_ESTADO_RNG, *e.rng.estado)
    w.bool_(e.rng.gauss_next is not None)
    w.f64(e.rng.gauss_next if e.rng.gauss_next is not None else 0.0)
    w.i64(e.reloj_actual); w.i64(e.siguiente_secuencia)
    w.i32(e.acciones_jugador); w.i32(e.enemigos_derrotados)
    j = e.jugador
    for valor in (j.vida, j.vida_max, j.ataque, j.defensa, j.velocidad, j.sala_actual):
        w.i32(valor)
    w.i64(j.tiempo_siguiente)
    w.i32(j.capacidad_inventario); w.i32(j.indice_cursor)
    w.cantidad(len(j.objetos), "objetos en el inventario")
    for o in j.objetos:
        w.cadena(o.instancia_id); w.cadena(o.ficha_id); w.bool_(o.equipado)
    w.u32(len(e.eventos))
    for ev in e.eventos:
        w.i64(ev.tiempo); w.i64(ev.secuencia); w.u8(ev.tipo); w.cadena(ev.sujeto)
        w.i64(ev.a); w.i64(ev.b)
    w.cantidad(len(e.mensajes), "mensajes")
    for mensaje in e.mensajes:
        w.cadena(mensaje)


def _leer_global(r: _Lector):
    cripta_id, cripta_version, catalogo_version = r.cadena(), r.cadena(), r.cadena()
    semilla = r.i64()
    rng_version = r.u32()
    estado = r.grupo(_ESTADO_RNG)  # tupla con los 625 enteros
    hay_gauss = r.bool_()
    gauss = r.f64()
    rng = EstadoRNG(rng_version, estado, gauss if hay_gauss else None)
    reloj, siguiente = r.i64(), r.i64()
    acciones, derrotados = r.i32(), r.i32()
    vida, vida_max, ataque, defensa, velocidad, sala_actual = (r.i32() for _ in range(6))
    tiempo_sig = r.i64()
    capacidad, cursor = r.i32(), r.i32()
    objetos = tuple(ObjetoGuardado(r.cadena(), r.cadena(), r.bool_()) for _ in range(r.u16()))
    jugador = JugadorGuardado(vida, vida_max, ataque, defensa, velocidad, sala_actual, tiempo_sig, capacidad, cursor, objetos)
    eventos = tuple(EventoGuardado(r.i64(), r.i64(), r.u8(), r.cadena(), r.i64(), r.i64()) for _ in range(r.u32()))
    mensajes = tuple(r.cadena() for _ in range(r.u16()))
    return (cripta_id, cripta_version, catalogo_version, semilla, rng, reloj, siguiente,
            acciones, derrotados, jugador, eventos, mensajes)


def _validar_encabezado(crudo: bytes):
    if len(crudo) < _ENCABEZADO.size:
        raise CriptaFormatoIncompatibleError("archivo demasiado corto")
    magic, version, _reservado, n_salas, offset_global, longitud_global = _ENCABEZADO.unpack(crudo[:_ENCABEZADO.size])
    if magic != MAGIC:
        raise CriptaFormatoIncompatibleError("no es un archivo de guardado de Cripta")
    if version != FORMATO_VERSION:
        raise CriptaFormatoIncompatibleError(
            f"versión de formato {version}, este programa entiende la {FORMATO_VERSION}")
    return n_salas, offset_global, longitud_global


def _validar_estructura(tamano_archivo: int, n_salas: int, offset_global: int, longitud_global: int) -> None:
    # Un encabezado dañado puede traer números absurdos (por ejemplo, millones de salas):
    # se comparan con el tamaño real del archivo antes de leer nada más.
    fin_indice = _ENCABEZADO.size + n_salas * _REGISTRO_INDICE.size
    if fin_indice > tamano_archivo:
        raise CriptaFormatoIncompatibleError(f"el índice dice {n_salas} salas, pero el archivo es demasiado corto")
    if offset_global < fin_indice or offset_global + longitud_global > tamano_archivo:
        raise CriptaFormatoIncompatibleError("el bloque global apunta fuera del archivo")


def _validar_bloque(tamano_archivo: int, offset: int, longitud: int) -> None:
    if offset + longitud > tamano_archivo:
        raise CriptaFormatoIncompatibleError("un bloque de sala apunta fuera del archivo")


# ------------------------------------------------------------ API pública
class GuardadoBinario:
    def guardar(self, ruta, estado: EstadoPartida) -> int:
        """Escribe el guardado de forma atómica y devuelve los bytes escritos."""
        bloques = []
        for sala in estado.salas:
            w = _Escritor()
            _escribir_sala(w, sala)
            bloques.append((sala.sala_id, bytes(w.datos)))
        w_global = _Escritor()
        _escribir_global(w_global, estado)
        bloque_global = bytes(w_global.datos)

        n = len(bloques)
        offset_global = _ENCABEZADO.size + n * _REGISTRO_INDICE.size
        offset = offset_global + len(bloque_global)
        registros = []
        for sala_id, crudo in bloques:
            registros.append((sala_id, offset, len(crudo)))
            offset += len(crudo)
        ordenar_auto(registros)  # el índice queda ordenado por id de sala (§4.9)

        contenido = bytearray(_ENCABEZADO.pack(MAGIC, FORMATO_VERSION, 0, n, offset_global, len(bloque_global)))
        for registro in registros:
            contenido += _REGISTRO_INDICE.pack(*registro)
        contenido += bloque_global
        for _sala_id, crudo in bloques:
            contenido += crudo

        temporal = str(ruta) + ".tmp"
        with open(temporal, "wb") as archivo:
            archivo.write(contenido)
        os.replace(temporal, ruta)
        return len(contenido)

    def cargar(self, ruta) -> EstadoPartida:
        with open(ruta, "rb") as archivo:
            crudo = archivo.read()
        n_salas, offset_global, longitud_global = _validar_encabezado(crudo)
        _validar_estructura(len(crudo), n_salas, offset_global, longitud_global)
        (cripta_id, cripta_version, catalogo_version, semilla, rng, reloj, siguiente, acciones,
         derrotados, jugador, eventos, mensajes) = _leer_global(_Lector(crudo[offset_global:offset_global + longitud_global]))
        salas = []
        for i in range(n_salas):
            _sala_id, offset, longitud = _REGISTRO_INDICE.unpack_from(crudo, _ENCABEZADO.size + i * _REGISTRO_INDICE.size)
            _validar_bloque(len(crudo), offset, longitud)
            salas.append(_leer_sala(_Lector(crudo[offset:offset + longitud])))
        return EstadoPartida(cripta_id, cripta_version, catalogo_version, semilla, rng, reloj, siguiente,
                             acciones, derrotados, jugador, tuple(salas), eventos, mensajes)

    def cargar_sala(self, ruta, sala_id: int):
        """Devuelve la SalaGuardada de `sala_id` (o None) SIN leer el archivo completo:
        encabezado + O(log n) registros del índice + el bloque de esa sala."""
        with open(ruta, "rb") as archivo:
            n_salas, offset_global, longitud_global = _validar_encabezado(archivo.read(_ENCABEZADO.size))
            tamano = os.fstat(archivo.fileno()).st_size  # tamaño del archivo sin leerlo
            _validar_estructura(tamano, n_salas, offset_global, longitud_global)
            bajo, alto = 0, n_salas - 1
            while bajo <= alto:
                medio = (bajo + alto) // 2
                archivo.seek(_ENCABEZADO.size + medio * _REGISTRO_INDICE.size)
                registro = archivo.read(_REGISTRO_INDICE.size)
                if len(registro) != _REGISTRO_INDICE.size:
                    raise CriptaFormatoIncompatibleError("índice truncado")
                id_medio, offset, longitud = _REGISTRO_INDICE.unpack(registro)
                if id_medio == sala_id:
                    _validar_bloque(tamano, offset, longitud)
                    archivo.seek(offset)
                    return _leer_sala(_Lector(archivo.read(longitud)))
                if id_medio < sala_id:
                    bajo = medio + 1
                else:
                    alto = medio - 1
        return None

    def leer_encabezado(self, ruta):
        """(cripta_id, cripta_version, catalogo_version, semilla, n_salas) sin cargar salas."""
        with open(ruta, "rb") as archivo:
            n_salas, offset_global, longitud_global = _validar_encabezado(archivo.read(_ENCABEZADO.size))
            archivo.seek(offset_global)
            r = _Lector(archivo.read(longitud_global))
            cripta_id, cripta_version, catalogo_version = r.cadena(), r.cadena(), r.cadena()
            semilla = r.i64()
        return cripta_id, cripta_version, catalogo_version, semilla, n_salas


# ----------------------------------------- comparación con JSON (§4.10)
def guardar_json(ruta, estado: EstadoPartida) -> int:
    texto = json.dumps(dataclasses.asdict(estado), ensure_ascii=False, separators=(",", ":"))
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)
    return os.path.getsize(ruta)


def cargar_json(ruta) -> EstadoPartida:
    """Carga completa reconstruyendo las mismas clases que devuelve el formato binario,
    para que la comparación de tiempos sea justa (no solo json.loads)."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        d = json.load(archivo)
    j = d["jugador"]
    jugador = JugadorGuardado(
        j["vida"], j["vida_max"], j["ataque"], j["defensa"], j["velocidad"], j["sala_actual"],
        j["tiempo_siguiente"], j["capacidad_inventario"], j["indice_cursor"],
        tuple(ObjetoGuardado(o["instancia_id"], o["ficha_id"], o["equipado"]) for o in j["objetos"]))
    salas = tuple(
        SalaGuardada(
            s["sala_id"], s["contenido_cargado"], tuple(s["puertas_cerradas"]), s["rastro"],
            tuple(s["objetos_suelo"]),
            tuple(TrampaGuardada(t["instancia_id"], t["tipo"], t["armada"]) for t in s["trampas"]),
            tuple(EnemigoGuardado(e["instancia_id"], e["tipo"], e["vida"], e["activo"], e["sala_actual"],
                                  e["tiempo_siguiente"]) for e in s["enemigos"]))
        for s in d["salas"])
    return EstadoPartida(
        d["cripta_id"], d["cripta_version"], d["catalogo_version"], d["semilla"],
        EstadoRNG(d["rng"]["version"], tuple(d["rng"]["estado"]), d["rng"]["gauss_next"]),
        d["reloj_actual"], d["siguiente_secuencia"], d["acciones_jugador"], d["enemigos_derrotados"],
        jugador, salas,
        tuple(EventoGuardado(e["tiempo"], e["secuencia"], e["tipo"], e["sujeto"], e["a"], e["b"]) for e in d["eventos"]),
        tuple(d["mensajes"]))