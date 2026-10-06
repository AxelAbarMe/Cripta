from cripta.constantes import MAX_ELEMENTOS_POR_LOTE


def validar_lote(elementos: list, nombre_campo: str) -> None:
    # El API acepta de 1 a MAX_ELEMENTOS_POR_LOTE elementos distintos por lote (§3.4)
    # Se revisa ANTES de pedir nada, para no gastar una solicitud en un lote que el servidor rechazaria
    if not elementos:
        raise ValueError(f"El lote de {nombre_campo} no puede estar vacío.")
    if len(elementos) > MAX_ELEMENTOS_POR_LOTE:
        raise ValueError(
            f"El lote de {nombre_campo} admite hasta {MAX_ELEMENTOS_POR_LOTE} "
            f"elementos, se recibieron {len(elementos)}."
        )
    if _tiene_repetidos(elementos):
        raise ValueError(f"El lote de {nombre_campo} tiene elementos repetidos.")


def _tiene_repetidos(elementos: list) -> bool:
    # Chequeo manual de repetidos: con 10 elementos como maximo, dos ciclos son suficientes
    # y no hace falta ninguna estructura extra.
    for i in range(len(elementos)):
        for j in range(i + 1, len(elementos)):
            if elementos[i] == elementos[j]:
                return True
    return False