'''Vista de consola de Cripta: menú, juego, puntajes y final dibujados con ASCII.
Implementa los 13 métodos de VistaBase; no conoce el modelo ni el servicio.
Las posiciones se muestran desde 1 y se envían al controlador desde 0.
Ctrl+C o fin de entrada equivalen a salir. Requiere una consola de al menos 113 columnas.
'''
import textwrap

from cripta.controlador.controlador_cripta import CRITERIOS_ORDEN, Orden
from cripta.vista.vista_base import VistaBase

ANCHO = 113
_CELDA = 27
_ANCHO_IZQ = 66
_ANCHO_DER = 46
_DIRECCIONES = ("N", "S", "E", "O")
AUTORES = ("Saul", "Isaac", "Axel")
FECHA_CREACION = "18 de octubre de 2026"
VERSION_JUEGO = "0.8"
CURSO = "Estructuras de Datos - II Ciclo 2026"
_CONTROLES = (
    "n/s/e/o  moverse", "abrir <dir>  abrir puerta", "atacar <#>  ataca enemigo", "esperar  pasar el tiempo",
    "recoger <#>  del suelo", "sig / ant  mover cursor", "usar / equipar / soltar", "ordenar peso|valor|nombre",
    "pergamino  deshacer", "guardar  guardar partida", "cargar  cargar partida", "salir  volver al menu",
)


# ------------------------------------------------------------ dibujo
def _caja(titulo: str, lineas: list[str], ancho: int, borde: str = "-", lado: str = "|", esquina: str = "+") -> list[str]:
    # Caja de ancho fijo con el título dentro del borde superior; las líneas largas se recortan.
    interior = ancho - 4
    encabezado = f"{borde * 2} {titulo} " if titulo else ""
    arriba = esquina + encabezado.ljust(ancho - 2, borde) + esquina
    cuerpo = [f"{lado} {linea[:interior].ljust(interior)} {lado}" for linea in lineas]
    return [arriba] + cuerpo + [esquina + borde * (ancho - 2) + esquina]


def _tabla(titulo: str, encabezados: tuple, filas: list[tuple]) -> list[str]:
    # Tabla con título; cada columna toma el ancho de su contenido más largo.
    anchos = [max(len(str(fila[i])) for fila in [encabezados] + filas) for i in range(len(encabezados))]
    total = sum(anchos) + 3 * len(anchos) + 1
    if total < len(titulo) + 4:
        anchos[-1] += len(titulo) + 4 - total
        total = len(titulo) + 4

    def fila(celdas):
        return "| " + " | ".join(str(c).ljust(anchos[i]) for i, c in enumerate(celdas)) + " |"
    separador = "+" + "+".join("-" * (a + 2) for a in anchos) + "+"
    return (["+" + "=" * (total - 2) + "+", "|" + titulo.center(total - 2) + "|", separador.replace("-", "="),
             fila(encabezados), separador] + [fila(f) for f in filas] + [separador])


def _unir_columnas(izquierda: list[str], derecha: list[str]) -> list[str]:
    # Pone dos bloques lado a lado, rellenando el más corto con espacios.
    alto = max(len(izquierda), len(derecha))
    izquierda = izquierda + [" " * _ANCHO_IZQ] * (alto - len(izquierda))
    derecha = derecha + [" " * _ANCHO_DER] * (alto - len(derecha))
    return [a + " " + b for a, b in zip(izquierda, derecha)]


class VistaConsola(VistaBase):
    def __init__(self, entrada=input, salida=print):
        # entrada y salida se pueden reemplazar para probar sin teclado ni pantalla.
        self._entrada = entrada
        self._salida = salida
        self._pendientes: list[str] = []     # avisos y paneles que salen justo encima de la entrada
        self._en_juego = False

    # ------------------------------------------------------- entrada
    def _leer(self, indicador: str) -> str | None:
        # Devuelve None si se cierra la entrada (Ctrl+D) o se interrumpe (Ctrl+C).
        try:
            return self._entrada(indicador)
        except (EOFError, KeyboardInterrupt):
            return None

    def _preguntar(self, texto: str) -> str | None:
        # Entrada claramente marcada: una línea [ ENTRADA ] con la pregunta y el indicador >>>.
        self._salida(f"\n[ ENTRADA ] {texto}")
        return self._leer(">>> ")

    def _continuar(self, texto: str = "Presiona Enter para continuar") -> None:
        self._leer(f"\n[ ENTRADA ] {texto}  >>> ")

    def _bloque(self, lineas: list[str]) -> None:
        # Imprime el bloque centrado en ANCHO columnas.
        margen = " " * max(0, (ANCHO - max(len(linea) for linea in lineas)) // 2)
        for linea in lineas:
            self._salida(margen + linea)

    def _volcar_pendientes(self, en_juego: bool) -> None:
        for linea in self._pendientes:
            self._salida(linea)
        self._pendientes.clear()
        self._en_juego = en_juego

    # ------------------------------------------------------- menú
    def pedir_opcion_menu(self) -> str:
        '''Dibuja el menú principal y devuelve iniciar, creditos, puntajes o salir.'''
        self._volcar_pendientes(False)
        self._salida("")
        self._bloque(_caja("", ["C  R  I  P  T  A".center(56), "Mazmorra dirigida por eventos".center(56)],
                           60, borde="*", lado="*", esquina="*"))
        self._bloque(_caja("MENU PRINCIPAL", ["", "[1]  INICIAR PARTIDA", "[2]  CREDITOS",
                                              "[3]  VER PUNTAJES", "[4]  SALIR", ""], 60, borde="="))
        while True:
            texto = self._preguntar("Elige una opcion (1-4)")
            if texto is None:
                return "salir"
            opcion = texto.strip().lower()
            for numero, nombre in (("1", "iniciar"), ("2", "creditos"), ("3", "puntajes"), ("4", "salir")):
                if opcion in (numero, nombre):
                    return nombre
            self._salida("Opcion invalida.")

    def mostrar_creditos(self) -> None:
        self._volcar_pendientes(False)
        self._salida("")
        self._bloque(_caja("CREDITOS", ["", "Proyecto : CRIPTA", f"Curso    : {CURSO}",
                                        "Autores  : " + ", ".join(AUTORES),
                                        f"Creado   : {FECHA_CREACION}", f"Version  : {VERSION_JUEGO}", ""], 60, borde="="))
        self._continuar("Presiona Enter para volver al menu")

    def mostrar_puntajes_globales(self, puntajes) -> None:
        self._volcar_pendientes(False)
        self._salida("")
        if not puntajes:
            self._bloque(_caja("PUNTAJES GLOBALES", ["", "Todavia no hay puntajes guardados.", ""], 60, borde="="))
        else:
            self._bloque(self._tabla_puntajes("PUNTAJES GLOBALES", puntajes, None, None))
        self._continuar("Presiona Enter para volver al menu")

    def elegir_cripta(self, criptas) -> str | None:
        '''Tabla de criptas; devuelve el id de la elegida, o None con 0 para volver al menú.'''
        self._volcar_pendientes(False)
        self._salida("")
        filas = [(n, c.nombre, c.salas, c.dificultad) for n, c in enumerate(criptas, start=1)]
        self._bloque(_tabla("SELECCIONA UNA CRIPTA", ("#", "Cripta", "Salas", "Dificultad"), filas))
        while True:
            texto = self._preguntar("Numero de la cripta (0 = volver al menu)")
            if texto is None or texto.strip() == "0":
                return None
            if texto.strip().isdigit() and 1 <= int(texto) <= len(criptas):
                return criptas[int(texto) - 1].id
            self._salida("Opcion invalida.")

    # ------------------------------------------------------- juego: entrada
    def pedir_orden(self, vista) -> Orden:
        '''Repite la pregunta hasta recibir un comando válido.'''
        while True:
            texto = self._preguntar("Escribe un comando y pulsa Enter  (ej: n | atacar 1 | recoger 1 | ordenar peso)")
            if texto is None:
                return Orden("salir")
            orden = self._interpretar(texto.strip().lower().split())
            if orden is not None:
                return orden
            self._salida("Comando no reconocido: mira los controles de arriba.")

    def _interpretar(self, partes: list[str]) -> Orden | None:
        # Convierte las palabras escritas en una Orden; None si no se entiende.
        if not partes:
            return None
        comando, argumento = partes[0], partes[1] if len(partes) > 1 else None
        if comando.upper() in _DIRECCIONES and argumento is None:
            return Orden("mover", comando.upper())
        if comando in ("mover", "abrir"):
            direccion = argumento.upper() if argumento else None
            return Orden(comando, direccion) if direccion in _DIRECCIONES else None
        if comando in ("atacar", "recoger"):
            if argumento is not None and argumento.isdigit():
                return Orden(comando, int(argumento) - 1)
            return None
        if comando == "ordenar":
            return Orden("ordenar", argumento) if argumento in CRITERIOS_ORDEN else None
        if comando in ("esperar", "usar", "equipar", "soltar", "pergamino", "guardar", "cargar", "salir"):
            return Orden(comando)
        if comando in ("sig", "ant"):
            return Orden("siguiente" if comando == "sig" else "anterior")
        return None

    def pedir_texto(self, pregunta: str) -> str | None:
        return self._preguntar(pregunta)

    def confirmar(self, pregunta: str) -> bool:
        respuesta = self._preguntar(f"{pregunta} (s/n)")
        return respuesta is not None and respuesta.strip().lower() in ("s", "si", "sí")

    # ------------------------------------------------------- juego: pantalla
    def mostrar_estado(self, vista, mensajes: tuple[str, ...]) -> None:
        '''Pantalla de juego: encabezado, controles, paneles a la izquierda, minimapa y avisos a la derecha, mensajes.'''
        escribir = self._salida
        escribir("")
        for linea in _caja("", [f"CRIPTA  |  Sala {vista.sala_id}: {vista.sala_nombre}  |  Tiempo virtual: {vista.tiempo}"],
                           ANCHO, borde="="):
            escribir(linea)
        for linea in self._controles():
            escribir(linea)
        for linea in _unir_columnas(self._paneles_izquierdos(vista), self._paneles_derechos(vista)):
            escribir(linea)
        for linea in _caja("MENSAJES (ultimos 20)", [f"  {m}" for m in mensajes] or ["(sin mensajes)"], ANCHO):
            escribir(linea)
        self._volcar_pendientes(True)

    @staticmethod
    def _controles() -> list[str]:
        # Controles siempre visibles: 4 por fila, cada uno en su celda.
        lineas = []
        for inicio in range(0, len(_CONTROLES), 4):
            fila = _CONTROLES[inicio:inicio + 4]
            lineas.append("+" + ("-" * _CELDA + "+") * len(fila))
            lineas.append("|" + "|".join((" " + texto).ljust(_CELDA)[:_CELDA] for texto in fila) + "|")
        lineas.append("+" + ("-" * _CELDA + "+") * 4)
        return lineas

    def _paneles_izquierdos(self, vista) -> list[str]:
        salidas = ", ".join(f"{s.direccion}->{s.destino}" + (" [CERRADA]" if s.cerrada else "") for s in vista.salidas)
        sala = [f"{vista.sala_nombre}  (sala {vista.sala_id})", "Salidas: " + (salidas or "ninguna")]
        if vista.trampas:
            sala.append("Trampas: " + ", ".join(
                f"{t.nombre} ({'armada' if t.armada else 'desarmada'})" for t in vista.trampas))
        enemigos = [f"{n}. {e.etiqueta}   PV {e.vida}/{e.vida_max}" for n, e in enumerate(vista.enemigos, start=1)]
        suelo = [f"{n}. {o.nombre}" for n, o in enumerate(vista.objetos_suelo, start=1)]
        lleno = 0 if vista.vida_max <= 0 else max(0, min(10, vista.vida * 10 // vista.vida_max))
        jugador = [f"Vida {vista.vida}/{vista.vida_max}  [{'#' * lleno}{'.' * (10 - lleno)}]",
                   f"Ataque {vista.ataque} | Defensa {vista.defensa} | Velocidad {vista.velocidad}",
                   f"Arma: {vista.arma_equipada or '-'} | Armadura: {vista.armadura_equipada or '-'}",
                   "Efectos: " + (", ".join(vista.efectos_activos) or "ninguno")]
        actual = "vacio" if vista.objeto_actual is None else f"{vista.objeto_actual} (#{vista.objeto_actual_indice + 1})"
        inventario = [f"Objetos {vista.inventario_cantidad}/{vista.inventario_capacidad} | Cursor: {actual}",
                      f"Pergaminos: {vista.pergaminos} | Se pueden deshacer: {vista.retrocesos_posibles}"]
        return (_caja("SALA", sala, _ANCHO_IZQ) + _caja("ENEMIGOS", enemigos or ["(ninguno)"], _ANCHO_IZQ)
                + _caja("SUELO", suelo or ["(vacio)"], _ANCHO_IZQ) + _caja("JUGADOR", jugador, _ANCHO_IZQ)
                + _caja("INVENTARIO", inventario, _ANCHO_IZQ))

    def _paneles_derechos(self, vista) -> list[str]:
        interior = _ANCHO_DER - 4
        mapa = [linea.center(interior) for linea in self._minimapa(vista)]
        mapa += ["", "@ = estas aqui     X = puerta cerrada".center(interior),
                 "N:3 = al norte esta la sala 3".center(interior)]
        avisos = []
        if vista.enemigos:
            avisos.append(f"[!] ENEMIGO: hay {len(vista.enemigos)} en esta sala")
        if vista.objetos_suelo:
            avisos.append(f"[*] OBJETOS: hay {len(vista.objetos_suelo)} en el suelo")
        return _caja("MINIMAPA", mapa, _ANCHO_DER) + _caja("AVISOS", avisos or ["(nada que destacar)"], _ANCHO_DER)

    @staticmethod
    def _minimapa(vista) -> list[str]:
        # Tu sala va en un cuadro doble (#=#) con @; las vecinas en cuadros simples con dirección:sala,
        # unidas por --- / | si la puerta está abierta y -X- / X si está cerrada. Siempre 11 líneas.
        def salida(direccion):
            for s in vista.salidas:
                if s.direccion == direccion:
                    return s
            return None

        def cuadro(salida_vecina):
            if salida_vecina is None:
                return ["         "] * 3
            texto = f"{salida_vecina.direccion}:{salida_vecina.destino}".center(7)
            return ["+-------+", f"|{texto}|", "+-------+"]
        centro = ["#=======#", f"#{('@ ' + str(vista.sala_id)).center(7)}#", "#=======#"]
        norte, sur, este, oeste = salida("N"), salida("S"), salida("E"), salida("O")

        def conector(s):
            return "   " if s is None else ("-X-" if s.cerrada else "---")

        def vertical(s):
            marca = " " if s is None else ("X" if s.cerrada else "|")
            return " " * 12 + marca.center(9)
        medio = []
        for i in range(3):
            c_izq = conector(oeste) if i == 1 else "   "
            c_der = conector(este) if i == 1 else "   "
            medio.append(cuadro(oeste)[i] + c_izq + centro[i] + c_der + cuadro(este)[i])
        arriba = [" " * 12 + linea for linea in cuadro(norte)]
        abajo = [" " * 12 + linea for linea in cuadro(sur)]
        return [linea.ljust(33) for linea in arriba + [vertical(norte)] + medio + [vertical(sur)] + abajo]

    # ------------------------------------------------------- avisos
    def mostrar_aviso(self, texto: str) -> None:
        self._avisar(f"[!] {texto}")

    def mostrar_error(self, texto: str) -> None:
        self._avisar(f"[Error] {texto}")

    def _avisar(self, linea: str) -> None:
        # En juego el aviso espera y sale justo encima de la entrada; fuera del juego sale de inmediato.
        if self._en_juego:
            self._pendientes.append(linea)
        else:
            self._salida(linea)

    def mostrar_inventario_ordenado(self, criterio: str, objetos) -> None:
        lineas = [f"{n}. {o.ficha.nombre}  (peso {o.ficha.peso}, valor {o.ficha.valor})"
                  for n, o in enumerate(objetos, start=1)]
        self._pendientes += _caja(f"INVENTARIO ORDENADO POR {criterio.upper()}", lineas or ["(vacio)"], ANCHO)

    # ------------------------------------------------------- puntajes y final
    def mostrar_resultado(self, desenlace, resumen, nombre, ranking, puntajes) -> None:
        '''Banner de victoria/derrota, tabla de estadísticas y puntajes globales con el jugador nuevo marcado.'''
        self._volcar_pendientes(False)
        titulo = "*** V I C T O R I A ***" if desenlace == "victoria" else "*** D E R R O T A ***"
        self._salida("")
        self._bloque(_caja("", ["", titulo.center(76), ""], 80, borde="="))
        if resumen is not None:
            posicion = self._posicion(ranking, nombre, resumen)
            filas = [("Jugador", nombre or "(sin nombre)"), ("Resultado", desenlace.upper()),
                     ("Acciones del jugador", resumen.acciones_jugador),
                     ("Enemigos derrotados", resumen.enemigos_derrotados), ("Tiempo final", resumen.tiempo_final),
                     ("Puesto en esta cripta", f"{posicion} de {len(ranking)}" if posicion else "-")]
            self._salida("")
            self._bloque(_tabla("ESTADISTICAS DE LA PARTIDA", ("Dato", "Valor"), filas))
        self._salida("")
        if puntajes:
            self._bloque(self._tabla_puntajes("PUNTAJES GLOBALES", puntajes, nombre, resumen))
        else:
            self._bloque(_caja("PUNTAJES GLOBALES", ["", "Todavia no hay puntajes guardados.", ""], 60, borde="="))
        self._continuar("Presiona Enter para continuar")

    @staticmethod
    def _posicion(ranking, nombre, resumen) -> int | None:
        for posicion, p in enumerate(ranking, start=1):
            if VistaConsola._es_nuevo(p, nombre, resumen):
                return posicion
        return None

    @staticmethod
    def _es_nuevo(p, nombre, resumen) -> bool:
        # El puntaje recién registrado: mismo nombre y mismas estadísticas que la partida terminada.
        return (nombre is not None and resumen is not None and p.nombre_jugador == nombre
                and p.acciones_jugador == resumen.acciones_jugador
                and p.enemigos_derrotados == resumen.enemigos_derrotados
                and p.tiempo_final == resumen.tiempo_final and p.victoria == resumen.victoria)

    def _tabla_puntajes(self, titulo, puntajes, nombre, resumen) -> list[str]:
        # La columna vacía lleva >> en la fila del jugador que acaba de terminar.
        filas = [(">>" if self._es_nuevo(p, nombre, resumen) else "", n, p.nombre_jugador[:20], p.cripta_id,
                  "victoria" if p.victoria else "derrota", p.acciones_jugador, p.enemigos_derrotados, p.tiempo_final)
                 for n, p in enumerate(puntajes, start=1)]
        return _tabla(titulo, ("", "#", "Jugador", "Cripta", "Resultado", "Acciones", "Derrotados", "Tiempo"), filas)

    def mostrar_final(self, datos) -> None:
        '''Resumen del jugador, de la partida y del reporte de red y caché; Enter vuelve al menú.'''
        self._volcar_pendientes(False)
        v, r = datos.vista, datos.resumen

        def dato(valor):
            return "-" if valor is None else valor
        jugador = [("Nombre", datos.nombre or "(sin nombre)"),
                   ("Vida final", f"{v.vida}/{v.vida_max}" if v else "-"), ("Ataque", dato(v and v.ataque)),
                   ("Defensa", dato(v and v.defensa)), ("Velocidad", dato(v and v.velocidad)),
                   ("Arma", dato(v and (v.arma_equipada or "-"))), ("Armadura", dato(v and (v.armadura_equipada or "-"))),
                   ("Pergaminos", dato(v and v.pergaminos)),
                   ("Objetos", f"{v.inventario_cantidad}/{v.inventario_capacidad}" if v else "-")]
        partida = [("Cripta", f"{datos.cripta_nombre} ({datos.cripta_id})"), ("Version de la cripta", datos.cripta_version),
                   ("Semilla", datos.semilla), ("Desenlace", datos.desenlace.upper()),
                   ("Acciones del jugador", dato(r and r.acciones_jugador)),
                   ("Enemigos derrotados", dato(r and r.enemigos_derrotados)), ("Tiempo final", dato(r and r.tiempo_final))]
        self._salida("")
        self._bloque(_caja("", ["", "RESUMEN FINAL".center(76), ""], 80, borde="*", lado="*", esquina="*"))
        self._salida("")
        self._bloque(_tabla("DATOS DEL JUGADOR", ("Dato", "Valor"), jugador))
        self._salida("")
        self._bloque(_tabla("DATOS DE LA PARTIDA", ("Dato", "Valor"), partida))
        self._salida("")
        reporte = [parte for linea in datos.reporte.splitlines() for parte in (textwrap.wrap(linea, 96) or [""])]
        self._bloque(_caja("RED Y CACHE", reporte, 100))
        self._continuar("Presiona Enter para volver al menu principal")