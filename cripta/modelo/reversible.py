"""Base para los objetos del modelo cuyos cambios se pueden deshacer (pergamino de retroceso, §2.11).

Si el objeto tiene un `registrador` (una función que recibe una operación inversa), cada vez que
se le asigna un atributo se registra cómo devolverlo a su valor anterior. Solo se guarda el valor
que se pisa, nunca una copia del estado completo (§4.6). Sin registrador no hace nada extra.
"""


class Reversible:
    registrador = None           # función(inversa) o None; la asigna quien arma el retroceso
    _no_reversibles = ()         # nombres de atributos que no deben deshacerse

    def __setattr__(self, nombre, valor):
        registrador = self.registrador
        if registrador is not None and nombre != "registrador" and nombre not in self._no_reversibles and hasattr(self, nombre):
            anterior = getattr(self, nombre)
            registrador(lambda: object.__setattr__(self, nombre, anterior))
        object.__setattr__(self, nombre, valor)

    def _registrar_inversa(self, inversa) -> None:
        """Para cambios que no son una asignación (por ejemplo, agregar a una lista)."""
        if self.registrador is not None:
            self.registrador(inversa)