"""ClienteGeneral: envuelve a cualquier ClienteCripta (HTTP u offline) y hace dos
cosas antes de cada solicitud, de forma atómica:

  1. Serializa las llamadas con un Lock. La precarga corre en un hilo aparte
     (servicio_precarga) mientras el hilo principal también puede pedir catálogo;
     sin esto dos solicitudes reales se solaparían, ContadorSolicitudes (un simple
     `+= 1`) no es seguro entre hilos y además se golpearía el límite de frecuencia.
  2. Verifica el presupuesto de la cripta (ServicioPresupuesto) ANTES de salir a la
     red: si no queda, lanza CriptaLimiteError sin gastar nada (§5.1).

Nota de alcance: la verificación cubre la solicitud inicial; un reintento por HTTP
429 dentro de ClienteHttp cuenta contra el contador pero no vuelve a pasar por aquí.
"""
import threading


class ClienteGeneral:
    def __init__(self, cliente, servicio_presupuesto=None):
        self._cliente = cliente
        self._presupuesto = servicio_presupuesto
        self._candado = threading.Lock()

    def _llamar(self, metodo, *args):
        with self._candado:
            if self._presupuesto is not None:
                self._presupuesto.verificar_disponible(1)
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