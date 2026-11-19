"""Búsqueda de rutas sobre el conocimiento disponible al jugador."""
from cripta.estructuras.heap_min import HeapMinimo


def siguiente_paso(conocimiento, origen: int, destino: int) -> str | None:
    """Devuelve la dirección del primer paso mínimo, o None si no hay ruta."""
    if (conocimiento.estado_de_sala(origen) != "explorada"
            or conocimiento.estado_de_sala(destino) != "explorada"):
        return None
    if origen == destino:
        return None

    proyeccion = conocimiento.proyectar()
    maximo_id = max(sala.id_sala for sala in proyeccion)
    distancias = [None] * (maximo_id + 1)
    entrantes = [[] for _ in distancias]
    for sala in proyeccion:
        if sala.estado != "explorada":
            continue
        for salida in sala.salidas:
            if salida.estado_puerta == "abierta":
                entrantes[salida.id_sala_destino].append(
                    (sala.id_sala, salida.costo)
                )

    distancias[destino] = 0
    pendientes = HeapMinimo()
    pendientes.insertar((0, destino))
    while not pendientes.esta_vacio():
        costo_actual, sala_actual = pendientes.eliminar_minimo()
        if costo_actual != distancias[sala_actual]:
            continue
        for anterior, costo in entrantes[sala_actual]:
            nuevo_costo = costo_actual + costo
            if distancias[anterior] is None or nuevo_costo < distancias[anterior]:
                distancias[anterior] = nuevo_costo
                pendientes.insertar((nuevo_costo, anterior))

    mejor = None
    mejor_id = None
    sala_origen = conocimiento.sala_conocida(origen)
    for salida in sala_origen.salidas:
        resto = distancias[salida.id_sala_destino]
        if salida.estado_puerta != "abierta" or resto is None:
            continue
        costo_total = salida.costo + resto
        if (mejor is None or costo_total < mejor
                or (costo_total == mejor and salida.id_sala_destino < mejor_id)):
            mejor = costo_total
            mejor_id = salida.id_sala_destino
            direccion = salida.direccion
    return direccion if mejor is not None else None
