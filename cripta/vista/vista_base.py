'''Contrato de la Vista de Cripta: lo que el ControladorCripta espera de cualquier interfaz.
VistaConsola hereda de esta clase e implementa los 13 métodos, otra interfaz solo tendría que hacer lo mismo.
La vista solo lee VistaPartida y ResultadoAccion; nunca toca el modelo ni el servicio.
Sus órdenes salen como objetos Orden y recibe DatosFinales (ambos en controlador/controlador_cripta.py).
'''
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cripta.controlador.controlador_cripta import DatosFinales, Orden
    from cripta.modelo.puntajes import Puntaje
    from cripta.modelo.resultado_partida import ResumenPuntaje, VistaPartida


class VistaBase(ABC):
    # ---------------------------------------------------------------- menú
    @abstractmethod
    def pedir_opcion_menu(self) -> str:
        '''Muestra el menú principal y devuelve "iniciar", "creditos", "puntajes" o "salir".'''

    @abstractmethod
    def mostrar_creditos(self) -> None:
        '''Muestra los créditos y espera a que el usuario continúe.'''

    @abstractmethod
    def mostrar_puntajes_globales(self, puntajes: "tuple[Puntaje, ...]") -> None:
        '''Muestra todos los puntajes guardados (o un mensaje si no hay) y espera a que el usuario continúe.'''

    @abstractmethod
    def elegir_cripta(self, criptas) -> str | None:
        '''Muestra las criptas de GET /criptas y devuelve el id elegido, o None para volver al menú.'''

    # --------------------------------------------------------------- juego
    @abstractmethod
    def mostrar_estado(self, vista: "VistaPartida", mensajes: tuple[str, ...]) -> None:
        '''Presenta controles, sala, salidas, enemigos, suelo, estadísticas, avisos y los últimos 20 mensajes.'''

    @abstractmethod
    def pedir_orden(self, vista: "VistaPartida") -> "Orden":
        '''Bloquea hasta que el usuario decide y devuelve un Orden (consola: texto; gráfica: clic o tecla).'''

    @abstractmethod
    def mostrar_aviso(self, texto: str) -> None:
        '''Mensaje informativo: acción rechazada, guardado exitoso, orden inválida.'''

    @abstractmethod
    def mostrar_error(self, texto: str) -> None:
        '''Error de infraestructura o de uso ya capturado por el controlador.'''

    @abstractmethod
    def mostrar_inventario_ordenado(self, criterio: str, objetos) -> None:
        '''Lista del inventario ordenada por "peso", "valor" o "nombre"; objetos con .ficha.nombre/.peso/.valor.'''

    @abstractmethod
    def pedir_texto(self, pregunta: str) -> str | None:
        '''Pide una línea de texto (nombre del jugador); vacío o None significa omitir.'''

    @abstractmethod
    def confirmar(self, pregunta: str) -> bool:
        '''Pregunta sí/no y devuelve True si el usuario acepta.'''

    # ------------------------------------------------------ puntajes y final
    @abstractmethod
    def mostrar_resultado(self, desenlace: str, resumen: "ResumenPuntaje | None", nombre: str | None,
                          ranking: "tuple[Puntaje, ...]", puntajes: "tuple[Puntaje, ...]") -> None:
        '''Pantalla de victoria/derrota con estadísticas y puntajes globales; espera a que el usuario continúe.'''

    @abstractmethod
    def mostrar_final(self, datos: "DatosFinales") -> None:
        '''Resumen del jugador y la partida; al continuar el controlador vuelve al menú principal.'''