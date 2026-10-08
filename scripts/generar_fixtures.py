# Descarga una cripta real y su catálogo a fixtures/, con el formato que lee ClienteOffline (--offline).
# Uso, desde la raíz del proyecto:
#   python -m scripts.generar_fixtures             (usa la primera cripta publicada)
#   python -m scripts.generar_fixtures cripta-01   (usa la cripta indicada)
# El formato de cada archivo está documentado en docs/FORMATO_OFFLINE.md.
import json
import sys
from pathlib import Path

from cripta.constantes import MAX_ELEMENTOS_POR_LOTE
from cripta.infraestructura.cliente_http import ClienteHttp
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes

RAIZ = Path("fixtures")


def guardar(ruta: Path, datos) -> None:
    # Escribe el JSON tal como lo mandó el API, con sangría para que se pueda leer y comparar en git
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def en_lotes(elementos: list) -> list:
    # Parte la lista en lotes del tamaño máximo que acepta el API
    return [elementos[i:i + MAX_ELEMENTOS_POR_LOTE] for i in range(0, len(elementos), MAX_ELEMENTOS_POR_LOTE)]


def agregar_si_falta(lista: list, elemento) -> None:
    if elemento is not None and elemento not in lista:
        lista.append(elemento)


def descargar(cliente: ClienteHttp, id_cripta: str | None) -> str:
    # Se usa _get y no los métodos públicos porque estos devuelven DTOs,
    # y los fixtures tienen que guardar el JSON original del API.
    criptas = cliente._get("/criptas", "listar criptas")
    guardar(RAIZ / "criptas.json", criptas)
    if id_cripta is None:
        id_cripta = criptas["criptas"][0]["id"]
    carpeta = RAIZ / id_cripta

    general = cliente._get(f"/criptas/{id_cripta}", f"datos generales de {id_cripta}")
    guardar(carpeta / "general.json", general)
    guardar(carpeta / "version.json", cliente._get(f"/criptas/{id_cripta}/version", f"versión de {id_cripta}"))

    # Esqueleto: un archivo por página. Se juntan los ids de sala y las llaves de las puertas.
    ids_salas = []
    ids_catalogo = []
    for pagina in range(1, general["paginas"] + 1):
        datos = cliente._get(f"/criptas/{id_cripta}/salas", f"esqueleto de {id_cripta} (página {pagina})",
                             {"pagina": pagina})
        guardar(carpeta / "salas" / f"pagina_{pagina}.json", datos)
        for sala in datos["salas"]:
            ids_salas.append(sala["id"])
            for salida in sala["salidas"].values():
                agregar_si_falta(ids_catalogo, salida.get("llave"))

    # Contenido: el API lo da por lotes, pero se guarda un archivo por sala
    for lote in en_lotes(ids_salas):
        parametro = ",".join(str(s) for s in lote)
        datos = cliente._get(f"/criptas/{id_cripta}/contenido", f"contenido de {id_cripta} (salas {parametro})",
                             {"salas": parametro})
        for entrada in datos["contenido"]:
            guardar(carpeta / "contenido" / f"{entrada['sala']}.json", entrada)
            for enemigo in entrada.get("enemigos", []):
                agregar_si_falta(ids_catalogo, enemigo["tipo"])
            for objeto in entrada.get("objetos", []):
                agregar_si_falta(ids_catalogo, objeto)
            for trampa in entrada.get("trampas", []):
                agregar_si_falta(ids_catalogo, trampa["tipo"])
    agregar_si_falta(ids_catalogo, general["llave_salida"])

    # Catálogo: por lotes, un archivo por ficha. Lo que suelta un enemigo puede no estar en
    # ninguna sala, así que se agrega a la lista y se sigue pidiendo hasta que no quede nada nuevo.
    descargados = 0
    while descargados < len(ids_catalogo):
        lote = ids_catalogo[descargados:descargados + MAX_ELEMENTOS_POR_LOTE]
        datos = cliente._get("/catalogo", f"catálogo (ids {','.join(lote)})", {"ids": ",".join(lote)})
        for ficha in datos["entidades"]:
            guardar(RAIZ / "catalogo" / f"{ficha['id']}.json", ficha)
            for id_suelto in ficha.get("suelta", []):
                agregar_si_falta(ids_catalogo, id_suelto)
        descargados += len(lote)
    guardar(RAIZ / "catalogo" / "version.json", cliente._get("/catalogo/version", "versión de catálogo"))
    return id_cripta


def verificar(id_cripta: str) -> None:
    # Lee todo lo guardado con ClienteOffline: si algún archivo no tiene la forma esperada, falla aquí
    offline = ClienteOffline(str(RAIZ))
    offline.listar_criptas()
    general = offline.obtener_general(id_cripta)
    offline.obtener_version_cripta(id_cripta)
    ids_salas = []
    for pagina in range(1, general.paginas + 1):
        ids_salas.extend(sala.id for sala in offline.obtener_pagina_esqueleto(id_cripta, pagina).salas)
    ids_catalogo = []
    for lote in en_lotes(ids_salas):
        for contenido in offline.obtener_contenido(id_cripta, lote).salas:
            for enemigo in contenido.enemigos:
                agregar_si_falta(ids_catalogo, enemigo.tipo)
            for objeto in contenido.objetos:
                agregar_si_falta(ids_catalogo, objeto)
            for trampa in contenido.trampas:
                agregar_si_falta(ids_catalogo, trampa.tipo)
    fichas = 0
    for lote in en_lotes(ids_catalogo):
        fichas += len(offline.obtener_catalogo(lote).entidades)
    offline.obtener_version_catalogo()
    print(f"Verificación offline OK: {len(ids_salas)} salas, {fichas} fichas del contenido leídas sin errores")


def main() -> None:
    contador = ContadorSolicitudes()
    cliente = ClienteHttp(contador)
    id_cripta = descargar(cliente, sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Fixtures de {id_cripta} guardados en {RAIZ.resolve()}")
    print(contador.reporte())
    verificar(id_cripta)


if __name__ == "__main__":
    main()