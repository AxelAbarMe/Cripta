"""Ayudantes compartidos por las pruebas y las cargas del cazador, sobre criptas sintéticas.
Arman mapas y partidas en memoria con ClienteFalso, sin datos de ninguna cripta real.
"""
from cripta.constantes import direccion_opuesta
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from tests.cliente_falso import ClienteFalso

RANGO_SABUESO = 600       # rango real del sabueso óseo según el plan
RANGO_ESPECTRO = 2400     # rango real del espectro acechador según el plan


def grafo(conexiones):
    """Convierte [(origen, direccion, destino, costo), ...] en las salidas de ambos lados de cada conexión."""
    salidas = {}
    for origen, direccion, destino, costo in conexiones:
        salidas.setdefault(origen, {})[direccion] = {"sala": destino, "costo": costo}
        salidas.setdefault(destino, {})[direccion_opuesta(direccion)] = {"sala": origen, "costo": costo}
    return salidas


def construir_mapa(conexiones):
    """CriptaMapa sin partida, para probar la búsqueda de rutas sola."""
    salidas = grafo(conexiones)
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    mapa = CriptaMapa()
    mapa.agregar_pagina(PaginaEsqueletoDTO.desde_json({"pagina": 1, "total_paginas": 1, "salas": salas}))
    mapa.sincronizar_puertas()
    return mapa


def id_ficha(rango):
    return "ent_cz_sin_rango" if rango is None else f"ent_cz_{rango}"


def ficha_cazador(rango, velocidad):
    ficha = {"id": id_ficha(rango), "clase": "enemigo", "nombre": "Cazador", "vida_max": 1000, "ataque": 10,
             "defensa": 0, "velocidad": velocidad, "comportamiento": "cazador"}
    if rango is not None:
        ficha["rango"] = rango
    return ficha


def armar_partida(salidas, cazadores, velocidad_jugador=1000, velocidad_cazador=100, semilla=3):
    """La sala 1 es la inicial. `cazadores` es [(sala, instancia, rango), ...] y rango puede ser None.
    El jugador es veloz para poder recorrer varias salidas antes del primer turno del cazador (t=100)."""
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    contenido = [{"sala": i, "enemigos": [], "objetos": [], "trampas": []} for i in salidas]
    fichas = []
    for sala, instancia, rango in cazadores:
        for entrada in contenido:
            if entrada["sala"] == sala:
                entrada["enemigos"].append({"instancia": instancia, "tipo": id_ficha(rango)})
        if id_ficha(rango) not in [f["id"] for f in fichas]:
            fichas.append(ficha_cazador(rango, velocidad_cazador))
    general = {"id": "c1", "version": "v1", "salas_total": len(salas), "paginas": 1, "salas_por_pagina": 50,
               "sala_inicial": 1, "sala_salida": max(salidas), "llave_salida": "itm_llave",
               "presupuesto_solicitudes": 9, "inventario_max": 10,
               "jugador": {"vida_max": 100000, "ataque": 6, "defensa": 2, "velocidad": velocidad_jugador}}
    cliente = ClienteFalso(fichas, contenido, [{"pagina": 1, "total_paginas": 1, "salas": salas}], general)
    datos = cliente.obtener_general("c1")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "c1", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(datos.paginas)
    partida = Partida(datos, mapa, catalogo, precarga, semilla)
    partida.iniciar()
    return partida, mapa


def tiempo(partida):
    return partida.vista().tiempo


def recorrer(partida, direcciones):
    for direccion in direcciones:
        if not partida.ejecutar_accion(A("mover", direccion)).aceptada:
            raise AssertionError(f"El jugador no pudo moverse hacia {direccion}")


def avanzar_hasta(partida, instante):
    """El jugador espera hasta que el reloj llega a `instante`. Un enemigo con turno en ese instante ya actuó."""
    for _ in range(2000):
        if tiempo(partida) >= instante or partida.desenlace() != "en_curso":
            return
        partida.ejecutar_accion(A("esperar"))
    raise AssertionError("El reloj no llegó al instante pedido")


def cazador_de(mapa, instancia):
    for sala in mapa.todas_las_salas():
        for enemigo in list(sala.enemigos_activos) + list(sala.enemigos_dormidos):
            if enemigo.instancia_id == instancia:
                return enemigo
    raise AssertionError(f"No existe el enemigo {instancia}")
