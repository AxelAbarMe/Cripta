'''Controlador de Cripta: coordina menú, partida, puntajes y final entre la vista y ServicioPartida.
No conoce teclado, texto ni gráficos: la vista (consola o gráfica) le entrega objetos Orden.
Solo lee VistaPartida y ResultadoAccion; toda acción pasa por servicio.ejecutar().
Captura CriptaError, FileNotFoundError, RuntimeError y ValueError y los muestra sin cerrar la partida.
'''
from dataclasses import dataclass

from cripta.excepciones import CriptaError
from cripta.modelo.accion import Accion
from cripta.modelo.resultado_partida import ResumenPuntaje, VistaPartida

CRITERIOS_ORDEN = ("peso", "valor", "nombre")
_ERRORES = (CriptaError, FileNotFoundError, RuntimeError, ValueError)


@dataclass(frozen=True, slots=True)
class Orden:
    '''Intención del usuario, igual para consola y gráfica. `argumento` según el tipo:
    mover/abrir: "N","S","E","O"; atacar/recoger: posición en vista.enemigos / vista.objetos_suelo;
    ordenar: "peso","valor" o "nombre"; el resto no lleva.
    Tipos: mover, abrir, atacar, esperar, recoger, usar, equipar, soltar, pergamino,
    siguiente, anterior, ordenar, guardar, cargar, salir.
    '''
    tipo: str
    argumento: str | int | None = None


@dataclass(frozen=True, slots=True)
class DatosFinales:
    '''Lo que la pantalla final muestra del jugador y la partida; el controlador lo arma al terminar.
    `vista` es el último estado del jugador y `reporte` el texto de servicio.reporte_final() (§5.1).
    '''
    nombre: str | None
    desenlace: str
    cripta_id: str
    cripta_nombre: str
    cripta_version: str
    semilla: int
    vista: VistaPartida | None
    resumen: ResumenPuntaje | None
    reporte: str


class ControladorCripta:
    def __init__(self, servicio, vista, ruta_guardado: str = "partida.sav",
                 ruta_bitacora: str = "partida.log", semilla: int | None = None, leer_puntajes=None):
        # servicio: ServicioPartida; vista: VistaBase (consola o gráfica);
        # leer_puntajes: función sin argumentos que devuelve todos los puntajes guardados (None = sin tabla).
        self._servicio = servicio
        self._vista = vista
        self._ruta_guardado = ruta_guardado
        self._ruta_bitacora = ruta_bitacora
        self._semilla = semilla
        self._leer_puntajes = leer_puntajes
        self._criptas = ()

    def ejecutar(self) -> None:
        '''Menú principal en bucle hasta elegir salir; siempre cierra el servicio al terminar.'''
        try:
            while True:
                opcion = self._vista.pedir_opcion_menu()
                if opcion == "iniciar":
                    self._jugar()
                elif opcion == "creditos":
                    self._vista.mostrar_creditos()
                elif opcion == "puntajes":
                    self._ver_puntajes()
                else:
                    return
        finally:
            self._servicio.cerrar()

    # ------------------------------------------------------------ flujo
    def _jugar(self) -> None:
        # Una partida: elegir cripta y jugar; al terminar se muestran puntajes y final. Siempre libera la precarga.
        try:
            if self._iniciar_partida():
                self._bucle_principal()
        finally:
            self._servicio.cerrar()

    def _ver_puntajes(self) -> None:
        # Opción "ver puntajes" del menú.
        if self._leer_puntajes is None:
            self._vista.mostrar_aviso("La tabla de puntajes no está configurada.")
            return
        ok, puntajes = self._intentar(self._leer_puntajes)
        if ok:
            self._vista.mostrar_puntajes_globales(puntajes)

    def _iniciar_partida(self) -> bool:
        # Lista las criptas, deja elegir una (None = volver al menú) y arranca la partida.
        ok, criptas = self._intentar(self._servicio.listar_criptas)
        if not ok:
            return False
        self._criptas = criptas
        cripta_id = self._vista.elegir_cripta(criptas)
        if cripta_id is None:
            return False
        ok, _ = self._intentar(self._servicio.iniciar_nueva, cripta_id, self._semilla, self._ruta_bitacora)
        return ok

    def _bucle_principal(self) -> None:
        # Muestra el estado, pide una orden y la procesa hasta volver al menú o terminar la partida.
        while True:
            vista = self._mostrar_estado()
            if vista is None:
                if not self._vista.confirmar("No se pudo leer el estado de la partida. ¿Reintentar?"):
                    return
                continue
            orden = self._vista.pedir_orden(vista)
            if orden.tipo == "salir":
                if self._vista.confirmar("¿Volver al menú principal? Se perderá el progreso no guardado."):
                    return
                continue
            if self._procesar(orden, vista):
                return

    def _mostrar_estado(self):
        # Devuelve la VistaPartida mostrada, o None si la infraestructura falló al consultarla.
        ok, datos = self._intentar(lambda: (self._servicio.partida.vista(), self._servicio.partida.mensajes()))
        if not ok:
            return None
        self._vista.mostrar_estado(datos[0], datos[1])
        return datos[0]

    def _procesar(self, orden: Orden, vista) -> bool:
        # Devuelve True cuando la partida terminó (victoria o derrota).
        if orden.tipo in ("siguiente", "anterior"):
            self._mover_cursor(orden.tipo)
        elif orden.tipo == "ordenar":
            self._mostrar_ordenado(orden.argumento)
        elif orden.tipo == "guardar":
            self._guardar()
        elif orden.tipo == "cargar":
            self._cargar()
        else:
            accion = self._traducir(orden, vista)
            return accion is not None and self._ejecutar_accion(accion)
        return False

    # ------------------------------------------------- orden -> acción
    def _traducir(self, orden: Orden, vista) -> Accion | None:
        # Convierte posiciones de la vista en ids reales; None si la orden no se puede formar.
        tipo, arg = orden.tipo, orden.argumento
        if tipo in ("mover", "abrir"):
            return self._crear_accion(tipo, arg)
        if tipo == "esperar":
            return Accion("esperar")
        if tipo == "atacar":
            if not self._posicion_valida(arg, vista.enemigos, "No hay ese enemigo en la sala."):
                return None
            return Accion("atacar", vista.enemigos[arg].instancia)
        if tipo == "recoger":
            if not self._posicion_valida(arg, vista.objetos_suelo, "No hay ese objeto en el suelo."):
                return None
            return Accion("recoger", vista.objetos_suelo[arg].ficha_id)
        if tipo in ("usar", "equipar", "soltar"):
            if vista.objeto_actual_indice is None:
                self._vista.mostrar_aviso("No hay un objeto seleccionado en el inventario.")
                return None
            return Accion(tipo, vista.objeto_actual_indice)
        if tipo == "pergamino":
            if vista.retrocesos_posibles <= 0:
                self._vista.mostrar_aviso("No hay ninguna acción que se pueda deshacer.")
                return None
            return Accion("pergamino")
        self._vista.mostrar_aviso(f"Orden desconocida: {tipo!r}.")
        return None

    def _crear_accion(self, tipo: str, argumento) -> Accion | None:
        # Accion valida la dirección y lanza ValueError si la vista envía una inválida.
        ok, accion = self._intentar(Accion, tipo, argumento)
        return accion if ok else None

    def _posicion_valida(self, posicion, elementos, mensaje: str) -> bool:
        valida = isinstance(posicion, int) and not isinstance(posicion, bool) and 0 <= posicion < len(elementos)
        if not valida:
            self._vista.mostrar_aviso(mensaje)
        return valida

    # ---------------------------------------------------------- acciones
    def _ejecutar_accion(self, accion: Accion) -> bool:
        # Una acción rechazada se avisa con su motivo; una aceptada que termina la partida la finaliza.
        ok, resultado = self._intentar(self._servicio.ejecutar, accion)
        if not ok:
            return False
        if not resultado.aceptada:
            self._vista.mostrar_aviso(resultado.motivo_rechazo)
            return False
        if resultado.desenlace != "en_curso":
            self._finalizar(resultado.desenlace)
            return True
        return False

    def _finalizar(self, desenlace: str) -> None:
        # Pide el nombre, registra el puntaje y muestra las pantallas de resultado y final.
        vista = self._mostrar_estado()
        ok, resumen = self._intentar(lambda: self._servicio.partida.puntaje())
        resumen = resumen if ok else None
        nombre = self._pedir_nombre()
        ranking = ()
        if nombre:
            ok, ranking = self._intentar(self._servicio.registrar_puntaje, nombre)
            ranking = ranking if ok else ()
        self._vista.mostrar_resultado(desenlace, resumen, nombre, ranking, self._puntajes_globales())
        general = self._servicio.datos_generales
        self._vista.mostrar_final(DatosFinales(
            nombre, desenlace, general.id, self._nombre_cripta(general.id), general.version,
            self._servicio.semilla, vista, resumen, self._servicio.reporte_final()))

    def _pedir_nombre(self) -> str | None:
        texto = self._vista.pedir_texto("Escribe tu nombre para la tabla de puntajes (Enter para omitir)")
        return texto.strip() if texto and texto.strip() else None

    def _puntajes_globales(self) -> tuple:
        # Todos los puntajes guardados; vacío si no hay tabla o falló la lectura.
        if self._leer_puntajes is None:
            return ()
        ok, puntajes = self._intentar(self._leer_puntajes)
        return puntajes if ok else ()

    def _nombre_cripta(self, cripta_id: str) -> str:
        for cripta in self._criptas:
            if cripta.id == cripta_id:
                return cripta.nombre
        return cripta_id

    # -------------------------------------------------------- inventario
    def _mover_cursor(self, sentido: str) -> None:
        # Mueve el cursor del inventario (no consume tiempo); la vista lo refleja en el siguiente estado.
        if sentido == "siguiente":
            self._intentar(lambda: self._servicio.partida.inventario_siguiente())
        else:
            self._intentar(lambda: self._servicio.partida.inventario_anterior())

    def _mostrar_ordenado(self, criterio) -> None:
        # Vista ordenada por peso, valor o nombre; no altera el orden real del inventario.
        if criterio not in CRITERIOS_ORDEN:
            self._vista.mostrar_aviso(f"Criterio de orden inválido: {criterio!r}.")
            return
        ok, objetos = self._intentar(lambda: self._servicio.partida.inventario_ordenado(criterio))
        if ok:
            self._vista.mostrar_inventario_ordenado(criterio, objetos)

    # ---------------------------------------------------- guardar y cargar
    def _guardar(self) -> None:
        ok, _ = self._intentar(self._servicio.guardar, self._ruta_guardado)
        if ok:
            self._vista.mostrar_aviso(f"Partida guardada en {self._ruta_guardado}.")

    def _cargar(self) -> None:
        # Cargar reemplaza la partida actual, por eso se confirma antes.
        if not self._vista.confirmar("Se reemplazará la partida actual. ¿Continuar?"):
            return
        ok, _ = self._intentar(self._servicio.cargar, self._ruta_guardado, self._ruta_bitacora)
        if not ok:
            return
        self._vista.mostrar_aviso(f"Partida cargada desde {self._ruta_guardado}.")
        if not self._servicio.bitacora_completa:
            self._vista.mostrar_aviso("La bitácora de esta partida está incompleta: no se podrá reproducir fielmente.")

    # ------------------------------------------------------------ errores
    def _intentar(self, operacion, *argumentos):
        # Ejecuta la operación; si falla muestra el error y devuelve (False, None) sin cortar el programa.
        try:
            return True, operacion(*argumentos)
        except _ERRORES as error:
            self._vista.mostrar_error(str(error))
            return False, None