"""Conversión DTO -> JSON (lo inverso de los `desde_json` de dto/). La caché en disco
guarda el MISMO formato que devuelve el API, así que leerla de vuelta reutiliza los
`desde_json` existentes sin duplicar lógica de parseo. Aquí los dict solo se usan
para escribir JSON (json.dumps los exige); no son índices ni cachés (§7)."""
import dataclasses
import json


def a_bytes(datos) -> bytes:
    return json.dumps(datos, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def desde_bytes(datos: bytes):
    return json.loads(datos.decode("utf-8"))


def ficha_a_json(ficha) -> dict:
    """Ficha de catálogo (cualquiera de las 9 clases). Los nombres de campo de los DTO
    coinciden con las claves del API (incluido `daño` en TrampaDTO), así que asdict
    produce directamente el JSON original."""
    return dataclasses.asdict(ficha)


def salida_a_json(salida) -> dict:
    datos = {"sala": salida.sala_destino}
    if salida.cerrada:
        datos["cerrada"] = True
    if salida.llave is not None:
        datos["llave"] = salida.llave
    if salida.cierre_automatico is not None:
        datos["cierre_automatico"] = salida.cierre_automatico
    return datos


def sala_a_json(sala) -> dict:
    salidas = {}
    for direccion in ("N", "S", "E", "O"):
        salida = sala.salida(direccion)
        if salida is not None:
            salidas[direccion] = salida_a_json(salida)
    return {"id": sala.id, "nombre": sala.nombre, "salidas": salidas}


def pagina_esqueleto_a_json(pagina) -> dict:
    return {
        "pagina": pagina.pagina,
        "total_paginas": pagina.total_paginas,
        "salas": [sala_a_json(s) for s in pagina.salas],
    }


def contenido_sala_a_json(contenido) -> dict:
    enemigos = []
    for e in contenido.enemigos:
        datos = {"instancia": e.instancia, "tipo": e.tipo}
        if e.vida is not None:
            datos["vida"] = e.vida
        enemigos.append(datos)
    return {
        "sala": contenido.id,
        "enemigos": enemigos,
        "objetos": list(contenido.objetos),
        "trampas": [{"instancia": t.instancia, "tipo": t.tipo} for t in contenido.trampas],
    }