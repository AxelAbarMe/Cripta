"""RepositorioPuntajes: guarda y lee la tabla de puntajes local (§2.12).

TablaPuntajes vive en el modelo y no sabe nada de archivos. Esta clase la convierte
a JSON y la guarda a través de AlmacenDiscoPuerto, igual que hace CacheDisco con la caché.

Formato: {"formato": 2, "puntajes": [{...}, {...}]}, en el orden en que se registraron (2: se agregó "victoria").Formato: {"formato": 2, "puntajes": [{...}, {...}]}, en el orden en que se registraron.
Cada puntaje lleva nombre, cripta, versión, acciones, enemigos derrotados, tiempo final y si fue
victoria (cuando se agregó el campo "victoria" se cambió del formato 1 al 2)."""
import json

from cripta.excepciones import CriptaPuntajesError
from cripta.modelo.puntajes import Puntaje, TablaPuntajes

CLAVE_PUNTAJES = "puntajes.json"
FORMATO_PUNTAJES = 2  # cambiarlo si cambian los campos de Puntaje (2: se agregó "victoria")

_CAMPOS_TEXTO = ("nombre_jugador", "cripta_id", "cripta_version")
_CAMPOS_ENTEROS = ("acciones_jugador", "enemigos_derrotados", "tiempo_final")
_CAMPOS_BOOLEANOS = ("victoria",)   


class RepositorioPuntajes:
    def __init__(self, almacen):
        self._almacen = almacen

    def cargar(self) -> TablaPuntajes:
        """Lee la tabla guardada. Si todavía no existe el archivo, devuelve una tabla vacía.
        Si existe pero está dañado, lanza CriptaPuntajesError (no se devuelve vacía: el
        siguiente guardar() la sobrescribiría y se perderían todos los puntajes)."""
        tabla = TablaPuntajes()
        crudo = self._almacen.leer(CLAVE_PUNTAJES)
        if crudo is None:
            return tabla  # primera partida: todavía no hay archivo
        try:
            datos = json.loads(crudo.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CriptaPuntajesError(f"el archivo no es JSON válido ({error})") from error
        if not isinstance(datos, dict) or datos.get("formato") != FORMATO_PUNTAJES:
            raise CriptaPuntajesError(f"formato desconocido (se esperaba formato {FORMATO_PUNTAJES})")
        filas = datos.get("puntajes")
        if not isinstance(filas, list):
            raise CriptaPuntajesError("falta la lista de puntajes")
        for numero, fila in enumerate(filas, start=1):
            tabla.agregar(self._puntaje_desde(fila, numero))
        return tabla

    def guardar(self, tabla: TablaPuntajes) -> None:
        """Escribe la tabla completa. AlmacenDiscoArchivos escribe a un temporal y lo
        renombra, así que un cierre a la mitad no deja el archivo a medio escribir."""
        datos = {
            "formato": FORMATO_PUNTAJES,
            "puntajes": [self._puntaje_a_dict(puntaje) for puntaje in tabla.registros()],
        }
        texto = json.dumps(datos, ensure_ascii=False, indent=2)
        self._almacen.escribir(CLAVE_PUNTAJES, texto.encode("utf-8"))

    def registrar(self, puntaje: Puntaje) -> TablaPuntajes:
        """Para el final de una partida: lee la tabla, agrega el puntaje, la guarda y la devuelve."""
        tabla = self.cargar()
        tabla.agregar(puntaje)
        self.guardar(tabla)
        return tabla

    @staticmethod
    def _puntaje_a_dict(puntaje: Puntaje) -> dict:
        # Solo para escribir JSON (§7 permite dict en el borde con JSON)
        resultado = {}
        for campo in _CAMPOS_TEXTO + _CAMPOS_ENTEROS + _CAMPOS_BOOLEANOS:
            resultado[campo] = getattr(puntaje, campo)
        return resultado

    @staticmethod
    def _puntaje_desde(fila, numero: int) -> Puntaje:
        # Revisa cada campo antes de construir el Puntaje, para que el error diga
        # exactamente qué fila y qué campo están mal
        if not isinstance(fila, dict):
            raise CriptaPuntajesError(f"el puntaje {numero} no es un objeto JSON")
        for campo in _CAMPOS_TEXTO:
            if not isinstance(fila.get(campo), str):
                raise CriptaPuntajesError(f"el puntaje {numero} no tiene un texto válido en «{campo}»")
        for campo in _CAMPOS_ENTEROS:
            valor = fila.get(campo)
            # bool es subclase de int en Python: True pasaría como 1 si no se excluye
            if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
                raise CriptaPuntajesError(f"el puntaje {numero} no tiene un entero válido en «{campo}»")
        for campo in _CAMPOS_BOOLEANOS:
            if not isinstance(fila.get(campo), bool):
                raise CriptaPuntajesError(f"el puntaje {numero} no tiene un valor verdadero/falso en «{campo}»")
            
        return Puntaje(
            nombre_jugador=fila["nombre_jugador"],
            cripta_id=fila["cripta_id"],
            cripta_version=fila["cripta_version"],
            acciones_jugador=fila["acciones_jugador"],
            enemigos_derrotados=fila["enemigos_derrotados"],
            tiempo_final=fila["tiempo_final"],
            victoria=fila["victoria"],
        )