"""ClienteGeneral: envuelve a cualquier ClienteCripta (HTTP u offline) y serializa
las llamadas con un Lock.

La precarga corre en un hilo aparte (servicio_precarga) mientras el hilo principal
también puede pedir catálogo. Sin el Lock, dos solicitudes reales se solaparían y
ContadorSolicitudes (un simple `+= 1`) no es seguro entre hilos.

El presupuesto NO se revisa aquí: ClienteHttp._get ya lo revisa antes de cada intento
(también antes de un reintento por 429). Como _get corre dentro del Lock, revisar y
contar es atómico: dos hilos no pueden pasar la revisión con una sola solicitud restante.
"""
import threading

class ClienteGeneral:
    def __init__(self, cliente):
        self._cliente = cliente
        self._candado = threading.Lock()

    def _llamar(self, metodo, *args):
        with self._candado:
            return metodo(*args)

    def listar_criptas(self):
        return self._llamar(self._cliente.listar_criptas)

    def obtener_general(self, cripta_id):
        return self._llamar(self._cliente.obtener_general, cripta_id)

    def obtener_version_cripta(self, cripta_id):
        return self._llamar(self._cliente.obtener_version_cripta, cripta_id)

    def obtener_pagina_esqueleto(self, cripta_id, pagina):
        return self._llamar(self._cliente.obtener_pagina_esqueleto, cripta_id, pagina)

    def obtener_contenido(self, cripta_id, salas):
        return self._llamar(self._cliente.obtener_contenido, cripta_id, salas)

    def obtener_catalogo(self, ids):
        return self._llamar(self._cliente.obtener_catalogo, ids)

    def obtener_version_catalogo(self):
        return self._llamar(self._cliente.obtener_version_catalogo)