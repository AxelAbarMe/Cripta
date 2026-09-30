"""Generador de una cripta en cuadrícula (filas x columnas) para pruebas y bench.
Devuelve los JSON tal como los daría el API, sin números de una cripta real."""


def construir(filas: int, columnas: int, con_enemigos: bool = True, salas_por_pagina: int = 50):
    def sid(r, c):
        return r * columnas + c + 1

    salas = []
    for r in range(filas):
        for c in range(columnas):
            salidas = {}
            if r > 0:
                salidas["N"] = {"sala": sid(r - 1, c)}
            if r < filas - 1:
                salidas["S"] = {"sala": sid(r + 1, c)}
            if c < columnas - 1:
                salidas["E"] = {"sala": sid(r, c + 1)}
            if c > 0:
                salidas["O"] = {"sala": sid(r, c - 1)}
            salas.append({"id": sid(r, c), "nombre": f"Sala {sid(r, c)}", "salidas": salidas})
    total = len(salas)
    paginas = []
    n_paginas = (total + salas_por_pagina - 1) // salas_por_pagina
    for p in range(n_paginas):
        paginas.append({"pagina": p + 1, "total_paginas": n_paginas,
                        "salas": salas[p * salas_por_pagina:(p + 1) * salas_por_pagina]})

    contenido = []
    for s in salas:
        i = s["id"]
        enemigos = []
        if con_enemigos and i % 3 == 0:
            enemigos = [{"instancia": f"e-{i}{k}", "tipo": "ent_rata" if k == 1 else "ent_murcielago"} for k in (2, 1)]
        contenido.append({"sala": i, "enemigos": enemigos, "objetos": ["itm_daga"] if i % 2 == 0 else ["itm_antorcha"],
                          "trampas": [{"instancia": f"t-{i}", "tipo": "trp_dardos"}] if i % 5 == 0 else []})

    fichas = [
        {"id": "ent_rata", "clase": "enemigo", "nombre": "Rata gigante", "vida_max": 12, "ataque": 5, "defensa": 1,
         "velocidad": 150, "comportamiento": "rastreador", "suelta": ["itm_pocion"]},
        {"id": "ent_murcielago", "clase": "enemigo", "nombre": "Murciélago", "vida_max": 8, "ataque": 3, "defensa": 0,
         "velocidad": 200, "comportamiento": "errante"},
        {"id": "itm_daga", "clase": "arma", "nombre": "Daga", "peso": 2, "valor": 15, "ataque_bonus": 3},
        {"id": "itm_antorcha", "clase": "antorcha", "nombre": "Antorcha", "peso": 1, "valor": 5, "duracion": 2000},
        {"id": "itm_pocion", "clase": "pocion", "nombre": "Poción", "peso": 1, "valor": 8, "cura": 10},
        {"id": "trp_dardos", "clase": "trampa", "nombre": "Dardos", "daño": 4, "rearme": 300},
    ]
    general = {"id": "c1", "version": "v1", "salas_total": total, "paginas": n_paginas, "salas_por_pagina": salas_por_pagina,
               "sala_inicial": 1, "sala_salida": total, "llave_salida": "itm_llave", "presupuesto_solicitudes": 9,
               "inventario_max": 10, "jugador": {"vida_max": 30, "ataque": 6, "defensa": 2, "velocidad": 100}}
    return {"paginas": paginas, "contenido": contenido, "fichas": fichas, "general": general, "total": total}